import json
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

try:
    # Try relative import first (when run as module)
    from .config import SCRAPED_DATA_FILE, VECTOR_STORE_PATH, EMBEDDING_MODEL_NAME
except ImportError:
    # Fall back to absolute import (when run directly)
    from config import SCRAPED_DATA_FILE, VECTOR_STORE_PATH, EMBEDDING_MODEL_NAME

def load_docs_from_jsonl(file_path):
    """Loads documents from a JSON Lines file."""
    documents = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            doc = Document(
                page_content=data.get("content", ""),
                metadata={
                    "source": data.get("url", ""),
                    "title": data.get("title", "No Title"),
                }
            )
            if doc.page_content:
                documents.append(doc)
    return documents

def create_and_save_vector_store():
    """
    Loads data from the scraped JSONL, creates embeddings using an improved
    chunking strategy, and saves them to a FAISS vector store.
    """
    print(f"Loading documents from {SCRAPED_DATA_FILE}...")
    if not SCRAPED_DATA_FILE.exists():
        raise FileNotFoundError(
            f"Scraped data file not found at {SCRAPED_DATA_FILE}. "
            "Please run the scraper first."
        )
    documents = load_docs_from_jsonl(SCRAPED_DATA_FILE)
    print(f"Loaded {len(documents)} documents from the website.")

    # --- IMPROVEMENT: More effective chunking strategy ---
    # A smaller chunk size ensures each vector represents a more specific topic.
    # A small overlap helps maintain context between chunks so sentences aren't cut in half.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )
    split_docs = text_splitter.split_documents(documents)
    print(f"Split documents into {len(split_docs)} more focused chunks.")

    if not split_docs:
        raise ValueError("No chunks were created. Check if the scraped data file is empty or content is too short.")

    print("Creating embeddings for all chunks (this may take a while)...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    
    print("Creating and saving the FAISS vector store...")
    vector_store = FAISS.from_documents(split_docs, embeddings)
    VECTOR_STORE_PATH.mkdir(exist_ok=True)
    vector_store.save_local(str(VECTOR_STORE_PATH))
    print(f"Vector store successfully created and saved at {VECTOR_STORE_PATH}")

if __name__ == "__main__":
    create_and_save_vector_store()