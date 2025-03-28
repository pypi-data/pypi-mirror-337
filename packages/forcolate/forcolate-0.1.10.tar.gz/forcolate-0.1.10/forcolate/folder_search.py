import win32com.client
import os
import re
from sentence_transformers import CrossEncoder
import urllib.parse
from docling.document_converter import DocumentConverter

def convert_documents_to_markdown(source):
    """
    Convert documents in the specified source directory to markdown.

    Args:
    - source (str): The local path or URL to the directory containing the documents.

    Yields:
    - str: The markdown content of each converted document.
    """
    converter = DocumentConverter()

    for path, dirnames, filenames in os.walk(source):
        for filename in filenames:
            file_path = os.path.join(path, filename)
            try:
                converted = converter.convert(file_path)
                result = converted.document.export_to_markdown()
                yield filename, result
            except Exception as e:
                print(f"Error converting {filename}: {e}")

def search_folder(source_directory, save_directory, query, threshold=0.0, limit=-1):
    """
    Process documents in a directory to find relevant documents based on a query.

    Parameters:
    - source_directory (str): Directory containing the documents to process.
    - save_directory (str): Directory to save the processed document files.
    - query (str): The search query to match against document content.
    - threshold (float): Minimum score threshold for saving a document.
    - limit (int): Maximum number of documents to assess.

    Returns:
    - List[str]: List of file paths where the processed documents are saved.
    """
    # Initialize Outlook application
    outlook = win32com.client.Dispatch('Outlook.Application').GetNamespace('MAPI')

    os.makedirs(save_directory, exist_ok=True)

    # Load a pre-trained CrossEncoder model from a local directory
    model_path = os.path.join(os.path.dirname(__file__), 'vendors', 'ms-marco-MiniLM-L6-v2')
    model = CrossEncoder(model_path)

    # List to store file paths
    file_paths = []

    # Convert documents to markdown and process them
    pairs = []
    document_names = []
    assess_limit = 0

    for filename, markdown_content in convert_documents_to_markdown(source_directory):
        if limit > 0 and assess_limit >= limit:
            break
        assess_limit += 1

        document_names.append(filename)
        pairs.append((query, markdown_content))

        # Predict and save if the batch is large enough or limit is reached
        if len(pairs) >= 100 or (limit > 0 and assess_limit >= limit):
            scores = model.predict(pairs)
            ranked_documents = sorted(zip(scores, document_names, pairs), reverse=True)

            filtered = [doc for doc in ranked_documents if doc[0] >= threshold]
            for index, document_triple in enumerate(filtered):
                score, name, document = document_triple
                # Generate a unique filename using a hash of the document content
                file_name = f"{index}_{name}_{score}.txt"
                file_name = re.sub(r'[^\w_.)( -]', '', file_name)

                file_path = os.path.join(save_directory, file_name)
                absolute_path = os.path.abspath(file_path)
                with open(absolute_path, 'w', encoding='utf-8') as file:
                    file.write(document[1])
                    file_url = urllib.parse.urljoin('file:', urllib.request.pathname2url(absolute_path))
                    file_paths.append(file_url)

            # Clear the lists to free up memory
            pairs.clear()
            document_names.clear()

    # Process any remaining documents
    if pairs:
        scores = model.predict(pairs)
        ranked_documents = sorted(zip(scores, document_names, pairs), reverse=True)

        filtered = [doc for doc in ranked_documents if doc[0] >= threshold]
        for index, document_triple in enumerate(filtered):
            score, name, document = document_triple
            # Generate a unique filename using a hash of the document content
            file_name = f"{index}_{name}_{score}.txt"
            file_name = re.sub(r'[^\w_.)( -]', '', file_name)

            file_path = os.path.join(save_directory, file_name)
            absolute_path = os.path.abspath(file_path)
            with open(absolute_path, 'w', encoding='utf-8') as file:
                file.write(document[1])
                file_url = urllib.parse.urljoin('file:', urllib.request.pathname2url(absolute_path))
                file_paths.append(file_url)

    # Return the list of file paths
    return file_paths
