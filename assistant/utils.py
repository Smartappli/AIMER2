import base64
from io import BytesIO

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
from unstructured.partition.tsv import partition_tsv
from unstructured.partition.text import partition_text
from unstructured.partition.xlsx import partition_xlsx
from unstructured.partition.xml import partition_xml

# Importation de Langchain pour la gestion des LLM et embeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaLLM
from langchain_ollama import OllamaEmbeddings
from .models import KnowledgeBase, TextEmbedding, TableEmbedding, ImageEmbedding

debug = False

# Extraction des composantes des fichiers HTML
def extract_html_components(file_path):
    try:
        elements = partition_html(filename=file_path)
        if debug:
            print("Elements extracted from HTML:", elements)
    except Exception as e:
        print(f"Error extracting HTML components: {e}")
        return None

    return classify_elements(elements)

# Extraction des composantes des fichiers PDF
def extract_pdf_components(file_path):
    try:
        elements = partition_pdf(
            filename=file_path,
            infer_table_structure=True,
            strategy='hi_res'
        )
        if debug:
            print("Elements extracted from PDF:", elements)
    except Exception as e:
        print(f"Error extracting PDF components: {e}")
        return None

    return classify_elements(elements)

# Extraction des composantes des fichiers DOC
def extract_doc_components(file_path):
    try:
        elements = partition_doc(filename=file_path)
        if debug:
            print("Elements extracted from DOC:", elements)
    except Exception as e:
        print(f"Error extracting DOC components: {e}")
        return None

    return classify_elements(elements)

# Extraction des composantes des fichiers DOCX
def extract_docx_components(file_path):
    try:
        elements = partition_docx(filename=file_path)
        if debug:
            print("Elements extracted from DOCX:", elements)
    except Exception as e:
        print(f"Error extracting DOCX components: {e}")
        return None

    return classify_elements(elements)

# Extraction des composantes des fichiers ODT
def extract_odt_components(file_path):
    try:
        elements = partition_odt(filename=file_path)
        if debug:
            print("Elements extracted from ODT:", elements)
    except Exception as e:
        print(f"Error extracting ODT components: {e}")
        return None

    return classify_elements(elements)

# Extraction des composantes des fichiers PPT
def extract_ppt_components(file_path):
    try:
        elements = partition_ppt(filename=file_path)
        if debug:
            print("Elements extracted from PPT:", elements)
    except Exception as e:
        print(f"Error extracting PPT components: {e}")
        return None

    return classify_elements(elements)

# Extraction des composantes des fichiers PPTX
def extract_pptx_components(file_path):
    try:
        elements = partition_pptx(filename=file_path)
        if debug:
            print("Elements extracted from PPTX:", elements)
    except Exception as e:
        print(f"Error extracting PPTX components: {e}")
        return None

    return classify_elements(elements)

# Extraction des composantes des fichiers XLSX
def extract_xlsx_components(file_path):
    try:
        elements = partition_xlsx(filename=file_path)
        if debug:
            print("Elements extracted from XLSX:", elements)
    except Exception as e:
        print(f"Error extracting XLSX components: {e}")
        return None

    return classify_elements(elements)

# Extraction des composantes des fichiers CSV
def extract_csv_components(file_path):
    try:
        elements = partition_csv(filename=file_path)
        if debug:
            print("Elements extracted from CSV:", elements)
    except Exception as e:
        print(f"Error extracting CSV components: {e}")
        return None

    return classify_elements(elements)

# Extraction des composantes des fichiers TSV
def extract_tsv_components(file_path):
    try:
        elements = partition_tsv(filename=file_path)
        if debug:
            print("Elements extracted from TSV:", elements)
    except Exception as e:
        print(f"Error extracting TSV components: {e}")
        return None

    return classify_elements(elements)

# Extraction des composantes des fichiers TXT
def extract_txt_components(file_path):
    try:
        elements = partition_text(filename=file_path)
        if debug:
            print("Elements extracted from TXT:", elements)
    except Exception as e:
        print(f"Error extracting TXT components: {e}")
        return None

    return classify_elements(elements)

# Extraction des composantes des fichiers EPUB
def extract_epub_components(file_path):
    try:
        elements = partition_epub(filename=file_path)
        if debug:
            print("Elements extracted from EPUB:", elements)
    except Exception as e:
        print(f"Error extracting EPUB components: {e}")
        return None

    return classify_elements(elements)

# Extraction des composantes des fichiers XML
def extract_xml_components(file_path):
    try:
        elements = partition_xml(filename=file_path)
        if debug:
            print("Elements extracted from XML:", elements)
    except Exception as e:
        print(f"Error extracting XML components: {e}")
        return None

    return classify_elements(elements)

# Extraction des composantes des fichiers JSON
def extract_json_components(file_path):
    try:
        elements = partition_json(filename=file_path)
        if debug:
            print("Elements extracted from JSON:", elements)
    except Exception as e:
        print(f"Error extracting JSON components: {e}")
        return None

    return classify_elements(elements)

# Extraction des composantes des fichiers Markdown
def extract_md_components(file_path):
    try:
        elements = partition_md(filename=file_path)
        if debug:
            print("Elements extracted from Markdown:", elements)
    except Exception as e:
        print(f"Error extracting Markdown components: {e}")
        return None

    return classify_elements(elements)

# Extraction des composantes des fichiers reStructuredText
def extract_rst_components(file_path):
    try:
        elements = partition_rst(filename=file_path)
        if debug:
            print("Elements extracted from RST:", elements)
    except Exception as e:
        print(f"Error extracting RST components: {e}")
        return None

    return classify_elements(elements)

# Classification des éléments extraits
def classify_elements(elements):

    print(f"Nombre d'éléments extraits : {len(elements)}")

    text_elements = [el for el in elements if el.category in ["Text", "NarrativeText", "Title", "Heading", "List"]]
    table_elements = [el for el in elements if el.category == "Table"]
    image_elements = [el for el in elements if el.category == "Image"]

    full_text = "\n".join([el.text for el in text_elements])
    cleaned_text = " ".join(full_text.split())
    print("------> Text Cleaning")

    # Text chunking
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    all_splits = text_splitter.split_text(cleaned_text)
    print("------> Text Chunking")

    # Afficher les tableaux extraits
    print("------> Table Extraction")
    if debug:
        for table in table_elements:
            print(table.text)
            print(table.metadata.text_as_html)

    # Afficher les images extraites
    print("------> Image Extraction")
    if debug:
        for image in image_elements:
            print(f"Image trouvée avec les métadonnées : {image.metadata}")

    if debug:
        print("Text elements:", text_elements)
        print("Image elements:", image_elements)
        print("Table elements:", table_elements)

    return {
        'text': all_splits,
        'images': image_elements,
        'tables': table_elements
    }

# Fonction pour transformer une image en base64
def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_str

# Description de l'image à l'aide d'Ollama
def describe_image_with_llm(images, model_name="llama3.2"):
    descriptions = []

    for i, image in enumerate(images):
        with open(f'image_{i}.png', 'wb') as img_file:
            img_file.write(image.content)

    llm = OllamaLLM(base_url="http://localhost:11434/generate", model=model_name)

    # Générer une description pour chaque image
    for i, image in enumerate(images):
        prompt = f"Describe the following image extracted from a document: image_{i}.png"

        # Appeler le modèle Llama pour générer la description
        description = llm.generate([prompt])
        descriptions.append(description)

        print(f"Description de l'image {i}: {description}")

    return descriptions

# Analyse des tableaux avec Ollama
def analyze_table_with_llm(table_data, model_name="llama3.2"):
    prompt = f"Analyze the following table and provide insights: {table_data}"

    llm = OllamaLLM(base_url="http://localhost:11434/generate", model=model_name)
    analysis = llm.generate([prompt])

    return analysis

# Orchestration complète pour traiter les fichiers
def process_file(file_path, file_type):
    if file_type == 'pdf':
        print("--- Start PDF Extraction ---")
        components = extract_pdf_components(file_path)
        print("--- End PDF Extraction ---")
    elif file_type == 'doc':
        print("--- Start DOC Extraction ---")
        components = extract_doc_components(file_path)
        print("--- End DOC Extraction ---")
    elif file_type == 'docx':
        print("--- Start DCX Extraction ---")
        components = extract_docx_components(file_path)
        print("--- End DCX Extraction ---")
    elif file_type == 'odt':
        print("--- Start ODT Extraction ---")
        components = extract_odt_components(file_path)
        print("--- End ODT Extraction ---")
    elif file_type == 'ppt':
        print("--- Start PPT Extraction ---")
        components = extract_ppt_components(file_path)
        print("--- End PPT Extraction ---")
    elif file_type == 'pptx':
        print("--- Start PPTX Extraction ---")
        components = extract_pptx_components(file_path)
        print("--- End PPTX Extraction ---")
    elif file_type == 'xlsx':
        print("--- Start XLSX Extraction ---")
        components = extract_xlsx_components(file_path)
        print("--- End XLSX Extraction ---")
    elif file_type == 'csv':
        print("--- Start CSV Extraction ---")
        components = extract_csv_components(file_path)
        print("--- End CSV Extraction ---")
    elif file_type == 'tsv':
        print("--- Start TSV Extraction ---")
        components = extract_tsv_components(file_path)
        print("--- End TSV Extraction ---")
    elif file_type == 'txt':
        print("--- Start TXT Extraction ---")
        components = extract_txt_components(file_path)
        print("--- End TXT Extraction ---")
    elif file_type == 'epub':
        print("--- Start EPUB Extraction ---")
        components = extract_epub_components(file_path)
        print("--- End EPUB Extraction ---")
    elif file_type == 'html':
        print("--- Start HTML Extraction ---")
        components = extract_html_components(file_path)
        print("--- End HTML Extraction ---")
    elif file_type == 'xml':
        print("--- Start XML Extraction ---")
        components = extract_xml_components(file_path)
        print("--- End XML Extraction ---")
    elif file_type == 'json':
        print("--- Start JSON Extraction ---")
        components = extract_json_components(file_path)
        print("--- End JSON Extraction ---")
    elif file_type == 'md':
        print("--- Start Markdown Extraction ---")
        components = extract_md_components(file_path)
        print("--- End Markdown Extraction ---")
    elif file_type == 'rst':
        print("--- Start RST Extraction ---")
        components = extract_rst_components(file_path)
        print("--- End RST Extraction ---")
    else:
        raise ValueError("Unsupported file type")

    if components:
        if debug:
            print(f"Text chunked: {components['text']}")
            print(f"Images: {components['images']}")
            print(f"Tables: {components['tables']}")

        # Image and table analysis
        # img_description = describe_image_with_llm(components['images'])
        # print(f"Image description: {img_description}")

        '''
        for table in components['tables']:
            table_analysis = analyze_table_with_llm(table)
            print(f"Table analysis: {table_analysis}")
        '''
    return components


# Embedding du texte avec Ollama
def embed_text_with_llm(chunks, model_name="llama3.2"):
    embed = OllamaEmbeddings(
        model=model_name,
    )
    if debug:
        print(chunks)

    print("---------> Text Embedding in progress...")
    embedding = embed.embed_documents(chunks)
    print(f"---------> Embeddings produced: {len(embedding)}")

    if debug:
        print(embedding)

    return embedding


# Embedding des tableaux avec Ollama
def embed_table_with_llm(table_data, model_name="llama3.2"):
    prompt = f"Embed the following table: {table_data}"
    llm = OllamaLLM(base_url="http://localhost:11434/generate", model=model_name)
    embedding = llm.generate([prompt])
    return embedding


# Embedding des images avec Ollama
def embed_image_with_llm(image, model_name="llama3.2"):
    img_base64 = image_to_base64(image)
    prompt = f"Embed the following image in detail: {img_base64}"
    llm = OllamaLLM(base_url="http://localhost:11434/generate", model=model_name)
    embedding = llm.generate([prompt])
    return embedding


# Orchestration pour l'embedding après l'extraction des composants
def embed_file_components(file_path, file_type, components):
    # Step 1: Create FileMetadata entry
    # file_metadata = KnowledgeBase.objects.create(file_path=file_path, file_type=file_type)

    # Step 2: Embedding du texte
    print("------> Start Text Embedding")
    embedded_text = embed_text_with_llm(components['text'])
    print("<------ End Text Embedding")

    # Save text embeddings in database
    for chunk, embedding in zip(components['text'], embedded_text):
        '''
        TextEmbedding.objects.create(
            file=file_metadata,
            text_chunk=chunk,
            embedding=embedding
        )
        '''

    # Embedding des images (if applicable)
    embedded_images = []
    if components['images']:
        print("------> Start Images Embedding")
        '''
        for image in components['images']:
            embedding = embed_image_with_llm(image)
            embedded_images.append(embedding)

            ImageEmbedding.objects.create(
                file=file_metadata,
                image_data=image.metadata,  # Assuming image metadata is sufficient
                embedding=embedding
            )
        '''
        print("<------ End Image Embedding")

    # Embedding des tableaux (if applicable)
    embedded_tables = []
    if components['tables']:
        print("------> Start Table Embedding")
        '''
        for table in components['tables']:
            embedding = embed_table_with_llm(table)
            embedded_tables.append(embedding)

            TableEmbedding.objects.create(
                file=file_metadata,
                table_data=table.text,  # Assuming table.text is the relevant content
                embedding=embedding
            )
        '''
        print("<------ End Table Embedding")

    return {
        'embedded_text': embedded_text,
        'embedded_tables': embedded_tables,
        'embedded_images': embedded_images
    }

# Process complet incluant l'Embedding
def process_file_with_embeddings(file_path, file_type):
    components = process_file(file_path, file_type)

    if components:
        # Embedding après classification des éléments
        print("--- Start Embeddings ---")
        embeddings = embed_file_components(file_path, file_type, components)
        print("--- End Embeddings ---")
        if debug:
            print(f"Text embeddings: {embeddings['embedded_text']}")
            print(f"Image embeddings: {embeddings['embedded_images']}")
            print(f"Table embeddings: {embeddings['embedded_tables']}")

        return embeddings

    return None
