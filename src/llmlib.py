# This library contains usefull functions for working with LLMs.

from langchain_community.document_loaders import PyPDFLoader, UnstructuredHTMLLoader # load PDF and HTML files
from langchain_community.document_loaders.csv_loader import CSVLoader # load CSV files
from langchain.text_splitter import RecursiveCharacterTextSplitter
    

def load_document(file_type, file_path):
    """
    Load a document based on the file type. For pdf it loads each page as a separate document.
    You can access the content and metadata of each document after loading using document[0].page_content and document[0].metadata.
    
    Args:
        file_type (str): Type of the file ('csv', 'html', or 'pdf').
        file_path (str): Path to the file.
        
    Returns:
        list: Loaded documents.
    """
    # for html:
    # documents[0].page_content  # Access the content of the first document
    # documents[0].metadata  # Access the metadata of the first document
    if file_type == "csv":
        loader = CSVLoader(file_path=file_path)
    elif file_type == "html":
        loader = UnstructuredHTMLLoader(file_path=file_path)
    elif file_type == "pdf":
        loader = PyPDFLoader(file_path=file_path)
    else:
        raise ValueError("Unsupported file type. Choose from 'csv', 'html', or 'pdf'.")
    return loader.load()

def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    """
    Split documents into smaller chunks for processing.
    
    Args:
        documents (list): List of documents to be split.
        chunk_size (int): Size of each chunk.
        chunk_overlap (int): Overlap between chunks.
        
    Returns:
        list: List of split documents.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
         )
    return text_splitter.split_documents(documents)