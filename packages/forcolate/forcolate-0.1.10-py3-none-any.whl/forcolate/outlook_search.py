import win32com.client
import os
import re
from sentence_transformers import CrossEncoder
import urllib.parse

def search_outlook_emails(save_directory, query, threshold=0.0, limit=-1):
    """
    Process Outlook emails to find relevant documents based on a query.

    Parameters:
    - save_directory (str): Directory to save the processed email files.
    - query (str): The search query to match against email content.
    - threshold (float): Minimum score threshold for saving a document.
    - limit (int): Maximum number of emails to assess.

    Returns:
    - List[str]: List of file paths where the processed emails are saved.
    """
    # Initialize Outlook application
    outlook = win32com.client.Dispatch('Outlook.Application').GetNamespace('MAPI')

    os.makedirs(save_directory, exist_ok=True)

    # Load a pre-trained CrossEncoder model from a local directory
    model_path = os.path.join(os.path.dirname(__file__), 'vendors', 'ms-marco-MiniLM-L6-v2')
    model = CrossEncoder(model_path)

    # List to store file paths
    file_paths = []

    # Iterate through accounts and folders
    messageNames = []
    pairs = []

    assess_limit = 0
    for account in outlook.Folders:
        for folder in account.Folders:
            for message in folder.Items:
                if limit > 0 and assess_limit > limit:
                    break
                assess_limit += 1

                messageNames.append(message.Subject)
                pairs.append((query, message.Body))

    scores = model.predict(pairs)
    ranked_documents = sorted(zip(scores, messageNames, pairs), reverse=True)

    filtered = [doc for doc in ranked_documents if doc[0] >= threshold]
    for index, message_triple in enumerate(filtered):
        score, name, message = message_triple
        # Generate a unique filename using a hash of the email body
        file_name = f"{index}_{name}_{score}.txt"
        file_name = re.sub(r'[^\w_.)( -]', '', file_name)

        file_path = os.path.join(save_directory, file_name)
        absolute_path = os.path.abspath(file_path)
        with open(absolute_path, 'w', encoding='utf-8') as file:
            file.write(message[1])
            file_url = urllib.parse.urljoin('file:', urllib.request.pathname2url(absolute_path))
            file_paths.append(file_url)

    # Return the list of file paths
    return file_paths
