from django import forms


class PDFUploadForm(forms.Form):
    pdf_files = forms.FileField(
        label="Upload PDF files",
        required=True,
        widget=forms.ClearableFileInput(attrs={"multiple": True})
    )
