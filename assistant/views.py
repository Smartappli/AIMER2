import mimetypes
import os
from pathlib import Path

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from AIMER2 import TemplateLayout

from .utils import process_file_with_embeddings


class AssistantView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in AIMER2/__init__.py file
        return TemplateLayout.init(self, super().get_context_data(**kwargs))


class UploadPage(AssistantView):
    template_name = "assistant/upload.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)


@csrf_exempt
def upload_and_process_files(request):
    if request.method == "POST":
        files = request.FILES.getlist("files")

        # Define the upload directory path
        upload_dir = settings.MEDIA_ROOT + "/" + "uploaded_files"

        # Check if the directory exists, if not create it
        upload_dir_path = Path(upload_dir)
        upload_dir_path.mkdir(parents=True, exist_ok=True)

        results = []  # List to store results for each file
        errors = []  # List to store errors for failed files

        for file in files:
            try:
                # Save each file to the directory
                file_name = file.name
                file_path = upload_dir + "/" + file_name
                destination_path = Path(file_path)
                with destination_path.open("wb+") as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

                # Detect the file type
                mime_type, _ = mimetypes.guess_type(file_path)
                if mime_type:
                    if mime_type == "application/pdf":
                        file_type = "pdf"
                    elif (
                        mime_type
                        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    ):
                        file_type = "docx"
                    elif mime_type == "application/msword":
                        file_type = "doc"
                    elif mime_type == "application/vnd.oasis.opendocument.text":
                        file_type = "odt"
                    elif (
                        mime_type
                        == "application/vnd.openxmlformats-officedocument.presentationml.presentation"
                    ):
                        file_type = "pptx"
                    elif mime_type == "application/vnd.ms-powerpoint":
                        file_type = "ppt"
                    elif mime_type == "application/vnd.ms-excel":
                        file_type = "xls"
                    elif (
                        mime_type
                        == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    ):
                        file_type = "xlsx"
                    elif mime_type == "text/csv":
                        file_type = "csv"
                    elif mime_type == "text/tab-separated-values":
                        file_type = "tsv"
                    else:
                        errors.append(
                            {
                                "file_name": file_name,
                                "error": "Unsupported file type",
                            }
                        )
                        continue
                else:
                    errors.append(
                        {
                            "file_name": file_name,
                            "error": "Could not determine file type",
                        }
                    )
                    continue

                # Process the file using the function from utils
                result = process_file_with_embeddings(file_path, file_type)

                # Append the result of processing to the list of results
                results.append(
                    {
                        "file_name": file_name,
                        "text": result["embedded_text"],
                        "image": result["embedded_images"],
                        "table": result["embedded_tables"],
                    }
                )

            except Exception as e:
                # Collect file-specific errors for partial failure handling
                errors.append({"file_name": file_name, "error": str(e)})

        # Return 207 if there were partial failures
        if errors:
            return JsonResponse(
                {
                    "message": "Some files processed successfully, but some failed.",
                    "results": results,
                    "errors": errors,
                },
                status=207,
            )

        return JsonResponse(
            {
                "message": "Files uploaded and processed successfully!",
                "results": results,
            },
            status=200,
        )

    return JsonResponse({"error": "Invalid request"}, status=400)
