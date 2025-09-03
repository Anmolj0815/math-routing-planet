# retriever.py
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os

def get_vector_store(embeddings=None):
    """
    Returns a FAISS vector store.
    If embeddings are not provided, initializes Gemini embeddings.
    """
    if embeddings is None:
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",  # Gemini embeddings model
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

    # Initialize FAISS with at least one dummy doc
    vector_store = FAISS.from_texts(
        ["This is a placeholder document."],
        embedding=embeddings
    )
    return vector_store
