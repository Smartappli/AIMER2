import os
import uuid

import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.llms import Ollama
from unstructured.partition.pdf import partition_pdf

from .models import UploadedFile

# Initialisation du vectorstore global
embedding_function = OllamaEmbeddings(model="llama3.2", show_progress=True)
vectorstore = Chroma(persist_directory="vectorDB", embedding_function=embedding_function)


@csrf_exempt
def upload_view(request):
    """
    Vue pour le téléchargement de fichiers PDF.
    Sauvegarde des fichiers dans le système de fichiers et des métadonnées dans la base de données.
    """
    if request.method == "POST" and "pdf_file" in request.FILES:
        uploaded_files = request.FILES.getlist("pdf_file")  # Récupère tous les fichiers uploadés
        unique_ids = []  # Pour stocker les IDs uniques des fichiers uploadés

        for pdf_file in uploaded_files:
            unique_id = str(uuid.uuid4())  # Générer un ID unique pour chaque fichier

            # Sauvegarde du fichier dans le dossier pdfFiles
            file_path = f"pdfFiles/{unique_id}_{pdf_file.name}"
            with open(file_path, "wb") as f:
                f.write(pdf_file.read())

            # Sauvegarde des métadonnées dans la base de données
            uploaded_file = UploadedFile.objects.create(
                file_id=unique_id,
                file_name=pdf_file.name,
                status="uploaded"
            )
            unique_ids.append(uploaded_file.file_id)  # Ajoute l'ID du fichier à la liste

        return JsonResponse({"message": "Fichiers téléchargés avec succès", "unique_ids": unique_ids})

    return render(request, "chatbot/upload.html")


def generate_image_description(image):
    """
    Fonction pour générer une description d'image à l'aide de LLAVA et Ollama.
    """
    img_path = f"pdfFiles/images/{image.filename}"

    url = "http://localhost:11434/generate"  # Remplacez par l'URL de votre service Ollama
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llava-llama3",  # Utilisation du modèle llava-llama3
        "input": img_path,  # Le chemin de l'image
        "parameters": {
            "description": "Décrire cette image en quelques phrases."  # Instructions pour générer la description
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Vérifier si la requête a réussi
        result = response.json()
        description = result.get("output", "Description non disponible.")
    except Exception as e:
        print(f"Erreur lors de la génération de la description : {e}")
        description = "Erreur lors de la génération de la description."

    return description


def generate_table_description(table):
    """
    Fonction pour générer une description de tableau à l'aide de LLAVA et Ollama.
    """
    # Exemple de traitement pour obtenir une description du tableau
    # Cela pourrait nécessiter d'extraire des données textuelles du tableau
    table_data = table.to_text()  # Remplacez par la méthode d'extraction appropriée
    description = "Ceci est une description générée du tableau."  # Remplacez par la vraie génération
    return description


@csrf_exempt
def process_view(request):
    """
    Processes the uploaded files, extracts text, images, tables, and updates ChromaDB after processing.
    """
    if request.method == "POST":  # Ensure processing occurs only on POST request
        uploaded_files = UploadedFile.objects.filter(status="uploaded")

        os.makedirs("pdfFiles/images", exist_ok=True)  # Ensure the images directory exists

        for uploaded_file in uploaded_files:
            file_id = uploaded_file.file_id
            file_name = uploaded_file.file_name
            file_path = f"pdfFiles/{file_id}_{file_name}"

            if os.path.exists(file_path):
                try:
                    # Use partition_pdf to separate text, images, and tables
                    pdf_elements = partition_pdf(
                        filename=file_path,
                        extract_images_in_pdf=True,
                        infer_table_structure=True,
                        chunking_strategy="by_title",
                        max_characters=4000,
                        new_after_n_chars=3800,
                        combine_text_under_n_chars=2000,
                        image_output_dir_path="pdfFiles/images"
                    )

                    # Separate text, images, and tables
                    text_elements = [el for el in pdf_elements if el.type == "Text"]
                    image_elements = [el for el in pdf_elements if el.type == "Image"]
                    table_elements = [el for el in pdf_elements if el.type == "Table"]

                    # Split text into smaller chunks
                    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
                    text_chunks = text_splitter.split_documents(text_elements)

                    # Add texts to the vectorstore
                    vectorstore.add_documents(text_chunks, metadata=[{"unique_id": file_id, "status": "processed"}])

                    # Process images to generate descriptions
                    for image in image_elements:
                        image_description = generate_image_description(image)
                        vectorstore.add_documents([image], metadata=[{"unique_id": file_id, "description": image_description}])

                    # Process tables to generate descriptions
                    for table in table_elements:
                        table_description = generate_table_description(table)
                        vectorstore.add_documents([table], metadata=[{"unique_id": file_id, "description": table_description}])

                    vectorstore.persist()  # Persist vectorstore changes

                    # Update the file status in the database
                    uploaded_file.status = "processed"
                    uploaded_file.save()

                except Exception as e:
                    # Print a message and update the status in the database
                    print(f"Error processing file {file_name}: {e}")
                    uploaded_file.status = "processing_error"
                    uploaded_file.save()

        return JsonResponse({"message": "Processing complete"})

    return JsonResponse({"error": "Invalid request"}, status=400)


def display_files_view(request):
    """
    Displays the uploaded files and their processing status.
    """
    uploaded_files = UploadedFile.objects.all()  # Get all uploaded files

    return render(request, "chatbot/files.html", {"files": uploaded_files})


@csrf_exempt
def delete_file_view(request, file_id):
    """
    Vue pour supprimer un fichier et ses métadonnées de ChromaDB et du système de fichiers.
    """
    if request.method == "POST":
        # Récupérer l'objet UploadedFile correspondant à file_id
        try:
            uploaded_file = UploadedFile.objects.get(file_id=file_id)
            file_name = uploaded_file.file_name
            file_path = f"pdfFiles/{file_id}_{file_name}"

            # Supprimer le fichier du système de fichiers
            if os.path.exists(file_path):
                os.remove(file_path)

            # Supprimer le fichier de ChromaDB
            vectorstore.delete_document(file_id)

            # Supprimer l'objet de la base de données
            uploaded_file.delete()

            return JsonResponse({"message": "Fichier et métadonnées supprimés avec succès"})

        except UploadedFile.DoesNotExist:
            return JsonResponse({"error": "Fichier non trouvé"}, status=404)


@csrf_exempt
def chatbot_view(request):
    """
    Vue pour le chatbot, permettant de répondre aux questions des utilisateurs en utilisant un modèle LLM.
    """
    os.makedirs("pdfFiles", exist_ok=True)
    os.makedirs("vectorDB", exist_ok=True)

    if "prompt_template" not in request.session:
        request.session["prompt_template"] = """You are a knowledgeable chatbot, here to help with questions of the user. Your tone should be professional and informative.

        Context: {context}
        History: {history}

        User: {question}
        Chatbot:"""

    prompt = PromptTemplate(
        input_variables=["history", "context", "question"],
        template=request.session["prompt_template"],
    )

    memory = ConversationBufferMemory(
        memory_key="history",
        return_messages=True,
        input_key="question"
    )

    embedding_function = OllamaEmbeddings(model="llama3.2")
    vectorstore = Chroma(persist_directory="vectorDB", embedding_function=embedding_function)

    llm = Ollama(
        base_url="http://localhost:11434",
        model="llama3.2",
        verbose=True,
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
    )

    qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever())

    if request.method == "POST" and "user_input" in request.POST:
        user_input = request.POST["user_input"]
        response = qa_chain.run(user_input)

        if "chat_history" not in request.session:
            request.session["chat_history"] = []

        # Ajouter le nouvel échange à l'historique
        request.session["chat_history"].append({"user": user_input, "bot": response})

        return render(request, "chatbot/chatbot.html", {"response": response, "chat_history": request.session["chat_history"]})

    return render(request, "chatbot/chatbot.html", {"chat_history": request.session.get("chat_history", [])})
