import base64
import logging
from io import BytesIO
from pathlib import Path

# Importation de Langchain pour la gestion des LLM et embeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, OllamaLLM

# Importation des fonctions de partition depuis 'unstructured'
from unstructured.partition.csv import partition_csv
from unstructured.partition.doc import partition_doc
from unstructured.partition.docx import partition_docx
from unstructured.partition.epub import partition_epub
from unstructured.partition.html import partition_html
from unstructured.partition.json import partition_json
from unstructured.partition.md import partition_md
from unstructured.partition.odt import partition_odt
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.ppt import partition_ppt
from unstructured.partition.pptx import partition_pptx
from unstructured.partition.rst import partition_rst
from unstructured.partition.text import partition_text
from unstructured.partition.tsv import partition_tsv
from unstructured.partition.xlsx import partition_xlsx
from unstructured.partition.xml import partition_xml

from .models import ImageEmbedding, KnowledgeBase, TableEmbedding, TextEmbedding

logging.basicConfig(level=logging.INFO)
debug = False


# Extraction des composantes des fichiers HTML
def extract_html_components(file_path):
    try:
        elements = partition_html(filename=file_path)
        if debug:
            logging.info("Elements extracted from HTML: %s", elements)
    except Exception as e:
        logging.info("Error extracting HTML components: %s", e)
        return None

    return classify_elements(elements)


# Extraction des composantes des fichiers PDF
def extract_pdf_components(file_path):
    try:
        elements = partition_pdf(
            filename=file_path,
            infer_table_structure=True,
            strategy="hi_res"
        )
        if debug:
            logging.info("Elements extracted from PDF: %s", elements)
    except Exception as e:
        logging.info("Error extracting PDF components: %s", e)
        return None

    return classify_elements(elements)

# Extraction des composantes des fichiers DOC
def extract_doc_components(file_path):
    try:
        elements = partition_doc(filename=file_path)
        if debug:
            logging.info("Elements extracted from DOC: %s", elements)
    except Exception as e:
        logging.info("Error extracting DOC components: %s", e)
        return None

    return classify_elements(elements)

# Extraction des composantes des fichiers DOCX
def extract_docx_components(file_path):
    try:
        elements = partition_docx(filename=file_path)
        if debug:
            logging.info("Elements extracted from DOCX: %s", elements)
    except Exception as e:
        logging.info("Error extracting DOCX components: %s", e)
        return None

    return classify_elements(elements)

# Extraction des composantes des fichiers ODT
def extract_odt_components(file_path):
    try:
        elements = partition_odt(filename=file_path)
        if debug:
            logging.info("Elements extracted from ODT: %s", elements)
    except Exception as e:
        logging.info("Error extracting ODT components: %s", e)
        return None

    return classify_elements(elements)

# Extraction des composantes des fichiers PPT
def extract_ppt_components(file_path):
    try:
        elements = partition_ppt(filename=file_path)
        if debug:
            logging.info("Elements extracted from PPT: %s", elements)
    except Exception as e:
        logging.info("Error extracting PPT components: %s", e)
        return None

    return classify_elements(elements)

# Extraction des composantes des fichiers PPTX
def extract_pptx_components(file_path):
    try:
        elements = partition_pptx(filename=file_path)
        if debug:
            logging.info("Elements extracted from PPTX: {elements}")
    except Exception as e:
        logging.info("Error extracting PPTX components: %s", e)
        return None

    return classify_elements(elements)

# Extraction des composantes des fichiers XLSX
def extract_xlsx_components(file_path):
    try:
        elements = partition_xlsx(filename=file_path)
        if debug:
            logging.info("Elements extracted from XLSX: %s ", elements)
    except Exception as e:
        logging.info("Error extracting XLSX components: %s", e)
        return None

    return classify_elements(elements)

# Extraction des composantes des fichiers CSV
def extract_csv_components(file_path):
    try:
        elements = partition_csv(filename=file_path)
        if debug:
            logging.info("Elements extracted from CSV: {elements}")
    except Exception as e:
        logging.info("Error extracting CSV components: %s", e)
        return None

    return classify_elements(elements)

# Extraction des composantes des fichiers TSV
def extract_tsv_components(file_path):
    try:
        elements = partition_tsv(filename=file_path)
        if debug:
            logging.info("Elements extracted from TSV: %s", elements)
    except Exception as e:
        logging.info("Error extracting TSV components: %s", e)
        return None

    return classify_elements(elements)

# Extraction des composantes des fichiers TXT
def extract_txt_components(file_path):
    try:
        elements = partition_text(filename=file_path)
        if debug:
            logging.info("Elements extracted from TXT: %s", elements)
    except Exception as e:
        logging.info("Error extracting TXT components: %s", e)
        return None

    return classify_elements(elements)

# Extraction des composantes des fichiers EPUB
def extract_epub_components(file_path):
    try:
        elements = partition_epub(filename=file_path)
        if debug:
            logging.info("Elements extracted from EPUB: %s", elements)
    except Exception as e:
        logging.info("Error extracting EPUB components: %s", e)
        return None

    return classify_elements(elements)

# Extraction des composantes des fichiers XML
def extract_xml_components(file_path):
    try:
        elements = partition_xml(filename=file_path)
        if debug:
            logging.info("Elements extracted from XML: %s", elements)
    except Exception as e:
        logging.info("Error extracting XML components: %s", e)
        return None

    return classify_elements(elements)

# Extraction des composantes des fichiers JSON
def extract_json_components(file_path):
    try:
        elements = partition_json(filename=file_path)
        if debug:
            logging.info("Elements extracted from JSON: %s", elements)
    except Exception as e:
        logging.info("Error extracting JSON components: %s", e)
        return None

    return classify_elements(elements)

# Extraction des composantes des fichiers Markdown
def extract_md_components(file_path):
    try:
        elements = partition_md(filename=file_path)
        if debug:
            logging.info("Elements extracted from Markdown: %s", elements)
    except Exception as e:
        logging.info("Error extracting Markdown components: %s", e)
        return None

    return classify_elements(elements)

# Extraction des composantes des fichiers reStructuredText
def extract_rst_components(file_path):
    try:
        elements = partition_rst(filename=file_path)
        if debug:
            logging.info("Elements extracted from RST: %s", elements)
    except Exception as e:
        logging.info("Error extracting RST components: %s", e)
        return None

    return classify_elements(elements)

# Classification des éléments extraits
def classify_elements(elements):

    logging.info("Nombre d'éléments extraits : %d", len(elements))

    text_elements = [el for el in elements if el.category in ["Text", "NarrativeText", "Title", "Heading", "List"]]
    table_elements = [el for el in elements if el.category == "Table"]
    image_elements = [el for el in elements if el.category == "Image"]

    full_text = "\n".join([el.text for el in text_elements])
    cleaned_text = " ".join(full_text.split())
    logging.info("------> Text Cleaning")

    # Text chunking
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    all_splits = text_splitter.split_text(cleaned_text)
    logging.info("------> Text Chunking")

    # Afficher les tableaux extraits
    logging.info("------> Table Extraction")
    if debug:
        for table in table_elements:
            logging.info(table.text)
            logging.info(table.metadata.text_as_html)

    # Afficher les images extraites
    logging.info("------> Image Extraction")
    if debug:
        for image in image_elements:
            logging.info("Image trouvée avec les métadonnées : %s", image.metadata)

    if debug:
        logging.info("Text elements: {text_elements}")
        logging.info("Image elements: {image_elements")
        logging.info("Table elements: {table_elements}")

    return {
        "text": all_splits,
        "images": image_elements,
        "tables": table_elements
    }

# Fonction pour transformer une image en base64
def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

# Description de l'image à l'aide d'Ollama
def describe_image_with_llm(images, model_name="llama3.2"):
    descriptions = []

    for i, image in enumerate(images):
        output_path = Path(f"image_{i}.png")
        with output_path.open("wb") as img_file:
            img_file.write(image.content)

    llm = OllamaLLM(base_url="http://localhost:11434/generate", model=model_name)

    # Générer une description pour chaque image
    for i, _ in enumerate(images):
        prompt = f"Describe the following image extracted from a document: image_{i}.png"

        # Appeler le modèle Llama pour générer la description
        description = llm.generate([prompt])
        descriptions.append(description)

        logging.info("Description de l'image %d: %s", i, description)

    return descriptions

# Analyse des tableaux avec Ollama
def analyze_table_with_llm(table_data, model_name="llama3.2"):
    prompt = f"Analyze the following table and provide insights: {table_data}"

    llm = OllamaLLM(base_url="http://localhost:11434/generate", model=model_name)
    return llm.generate([prompt])

def extract_pdf(file_path):
    logging.info("--- Start PDF Extraction ---")
    components = extract_pdf_components(file_path)
    logging.info("--- End PDF Extraction ---")
    return components

def extract_doc(file_path):
    logging.info("--- Start DOC Extraction ---")
    components = extract_doc_components(file_path)
    logging.info("--- End DOC Extraction ---")
    return components

def extract_docx(file_path):
    logging.info("--- Start DOCX Extraction ---")
    components = extract_docx_components(file_path)
    logging.info("--- End DOCX Extraction ---")
    return components

def extract_odt(file_path):
    logging.info("--- Start ODT Extraction ---")
    components = extract_odt_components(file_path)
    logging.info("--- End ODT Extraction ---")
    return components

def extract_ppt(file_path):
    logging.info("--- Start PPT Extraction ---")
    components = extract_ppt_components(file_path)
    logging.info("--- End PPT Extraction ---")
    return components

def extract_pptx(file_path):
    logging.info("--- Start PPTX Extraction ---")
    components = extract_pptx_components(file_path)
    logging.info("--- End PPTX Extraction ---")
    return components

def extract_xlsx(file_path):
    logging.info("--- Start XLSX Extraction ---")
    components = extract_xlsx_components(file_path)
    logging.info("--- End XLSX Extraction ---")
    return components

def extract_csv(file_path):
    logging.info("--- Start CSV Extraction ---")
    components = extract_csv_components(file_path)
    logging.info("--- End CSV Extraction ---")
    return components

def extract_tsv(file_path):
    logging.info("--- Start TSV Extraction ---")
    components = extract_tsv_components(file_path)
    logging.info("--- End TSV Extraction ---")
    return components

def extract_txt(file_path):
    logging.info("--- Start TXT Extraction ---")
    components = extract_txt_components(file_path)
    logging.info("--- End TXT Extraction ---")
    return components

def extract_epub(file_path):
    logging.info("--- Start EPUB Extraction ---")
    components = extract_epub_components(file_path)
    logging.info("--- End EPUB Extraction ---")
    return components

def extract_html(file_path):
    logging.info("--- Start HTML Extraction ---")
    components = extract_html_components(file_path)
    logging.info("--- End HTML Extraction ---")
    return components

def extract_xml(file_path):
    logging.info("--- Start XML Extraction ---")
    components = extract_xml_components(file_path)
    logging.info("--- End XML Extraction ---")
    return components

def extract_json(file_path):
    logging.info("--- Start JSON Extraction ---")
    components = extract_json_components(file_path)
    logging.info("--- End JSON Extraction ---")
    return components

def extract_md(file_path):
    logging.info("--- Start Markdown Extraction ---")
    components = extract_md_components(file_path)
    logging.info("--- End Markdown Extraction ---")
    return components

def extract_rst(file_path):
    logging.info("--- Start RST Extraction ---")
    components = extract_rst_components(file_path)
    logging.info("--- End RST Extraction ---")
    return components

# Orchestration complète pour traiter les fichiers
def process_file(file_path, file_type):
    file_extractors = {
        "pdf": extract_pdf,
        "doc": extract_doc,
        "docx": extract_docx,
        "odt": extract_odt,
        "ppt": extract_ppt,
        "pptx": extract_pptx,
        "xlsx": extract_xlsx,
        "csv": extract_csv,
        "tsv": extract_tsv,
        "txt": extract_txt,
        "epub": extract_epub,
        "html": extract_html,
        "xml": extract_xml,
        "json": extract_json,
        "md": extract_md,
        "rst": extract_rst
    }

    if file_type not in file_extractors:
        error_message = "Unsupported file type"
        raise ValueError(error_message)

    components = file_extractors[file_type](file_path)

    if components:
        if debug:
            logging.info("Text chunked: %s", components["text"])
            logging.info("Images: %s", components["images"])
            logging.info("Tables: %s", components["tables"])

        # Image and table analysis
        # img_description = describe_image_with_llm(components['images'])
        # logging.info("Image description: %s", img_description)

        """
        for table in components['tables']:
            table_analysis = analyze_table_with_llm(table)
            print(f"Table analysis: {table_analysis}")
        """
    return components


# Embedding du texte avec Ollama
def embed_text_with_llm(chunks, model_name="llama3.2"):
    embed = OllamaEmbeddings(
        model=model_name,
    )
    if debug:
        logging.info(chunks)

    logging.info("---------> Text Embedding in progress...")
    embedding = embed.embed_documents(chunks)
    logging.info("---------> Embeddings produced: %d", len(embedding))

    if debug:
        logging.info(embedding)

    return embedding


# Embedding des tableaux avec Ollama
def embed_table_with_llm(table_data, model_name="llama3.2"):
    prompt = f"Embed the following table: {table_data}"
    llm = OllamaLLM(base_url="http://localhost:11434/generate", model=model_name)
    return llm.generate([prompt])


# Embedding des images avec Ollama
def embed_image_with_llm(image, model_name="llama3.2"):
    img_base64 = image_to_base64(image)
    prompt = f"Embed the following image in detail: {img_base64}"
    llm = OllamaLLM(base_url="http://localhost:11434/generate", model=model_name)
    return llm.generate([prompt])


# Orchestration pour l'embedding après l'extraction des composants
def embed_file_components(file_path, file_type, components):
    # Step 1: Create FileMetadata entry
    # file_metadata = KnowledgeBase.objects.create(file_path=file_path, file_type=file_type)

    # Step 2: Embedding du texte
    logging.info("------> Start Text Embedding")
    embedded_text = embed_text_with_llm(components["text"])
    logging.info("<------ End Text Embedding")

    # Save text embeddings in database
    """
    for chunk, embedding in zip(components["text"], embedded_text, strict=False):
        TextEmbedding.objects.create(
            file=file_metadata,
            text_chunk=chunk,
            embedding=embedding
        )
    """

    # Embedding des images (if applicable)
    embedded_images = []
    if components["images"]:
        logging.info("------> Start Images Embedding")
        """
        for image in components['images']:
            embedding = embed_image_with_llm(image)
            embedded_images.append(embedding)

            ImageEmbedding.objects.create(
                file=file_metadata,
                image_data=image.metadata,  # Assuming image metadata is sufficient
                embedding=embedding
            )
        """
        logging.info("<------ End Image Embedding")

    # Embedding des tableaux (if applicable)
    embedded_tables = []
    if components["tables"]:
        logging.info("------> Start Table Embedding")
        """
        for table in components['tables']:
            embedding = embed_table_with_llm(table)
            embedded_tables.append(embedding)

            TableEmbedding.objects.create(
                file=file_metadata,
                table_data=table.text,  # Assuming table.text is the relevant content
                embedding=embedding
            )
        """
        logging.info("<------ End Table Embedding")

    return {
        "embedded_text": embedded_text,
        "embedded_tables": embedded_tables,
        "embedded_images": embedded_images
    }

# Process complet incluant l'Embedding
def process_file_with_embeddings(file_path, file_type):
    components = process_file(file_path, file_type)

    if components:
        # Embedding après classification des éléments
        logging.info("--- Start Embeddings ---")
        embeddings = embed_file_components(file_path, file_type, components)
        logging.info("--- End Embeddings ---")
        if debug:
            logging.info("Text embeddings: {embeddings['embedded_text']}")
            logging.info("Image embeddings: {embeddings['embedded_images']}")
            logging.info("Table embeddings: {embeddings['embedded_tables']}")

        return embeddings

    return None
