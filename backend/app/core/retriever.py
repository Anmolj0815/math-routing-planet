from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os


def get_vector_store(embeddings=None):
    """Return FAISS vector store."""
    if embeddings is None:
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001", google_api_key=os.getenv("GOOGLE_API_KEY")
        )

    vector_store = FAISS.from_texts(
        ["This is a placeholder document."],
        embedding=embeddings
    )
    return vector_store
