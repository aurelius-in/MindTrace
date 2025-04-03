import os
from typing import List
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from app.config import settings

# Load embedding model once
embedding_model = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)

def get_db_path() -> str:
    return settings.vector_db_path


def save_vector_store(docs: List[Document], persist_path: str = None) -> FAISS:
    """
    Creates a new FAISS index from documents and saves it locally.
    """
    persist_path = persist_path or get_db_path()
    db = FAISS.from_documents(docs, embedding_model)
    db.save_local(persist_path)
    return db


def load_vector_store(persist_path: str = None) -> FAISS:
    """
    Loads an existing FAISS index from disk.
    """
    persist_path = persist_path or get_db_path()
    if not os.path.exists(persist_path):
        raise FileNotFoundError(f"Vector store not found at {persist_path}")
    return FAISS.load_local(persist_path, embeddings=embedding_model)


def add_to_vector_store(new_docs: List[Document], persist_path: str = None) -> None:
    """
    Adds new documents to an existing FAISS index and resaves it.
    """
    persist_path = persist_path or get_db_path()
    db = load_vector_store(persist_path)
    db.add_documents(new_docs)
    db.save_local(persist_path)
