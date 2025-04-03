import os
import faiss
import pickle
from typing import List
from app.config import settings
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document


# Initialize OpenAI embeddings
embedding_model = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)

# Default FAISS storage path
VECTOR_DB_PATH = settings.vector_db_path


def create_vector_store(documents: List[Document], persist_path: str = VECTOR_DB_PATH) -> FAISS:
    """
    Creates and saves a FAISS vector store from a list of LangChain Documents.
    """
    vector_store = FAISS.from_documents(documents, embedding_model)
    vector_store.save_local(persist_path)
    return vector_store


def load_vector_store(persist_path: str = VECTOR_DB_PATH) -> FAISS:
    """
    Loads an existing FAISS vector store from disk.
    """
    if not os.path.exists(persist_path):
        raise FileNotFoundError(f"FAISS index not found at: {persist_path}")
    return FAISS.load_local(persist_path, embeddings=embedding_model)


def add_documents_to_store(documents: List[Document], persist_path: str = VECTOR_DB_PATH) -> None:
    """
    Adds new documents to an existing FAISS index and re-saves it.
    """
    vector_store = load_vector_store(persist_path)
    vector_store.add_documents(documents)
    vector_store.save_local(persist_path)


def query_vector_store(query: str, k: int = 5, persist_path: str = VECTOR_DB_PATH) -> List[Document]:
    """
    Queries the FAISS vector store for the top-k most relevant documents.
    """
    vector_store = load_vector_store(persist_path)
    return vector_store.similarity_search(query, k=k)
