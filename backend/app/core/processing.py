import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .retriever import get_vector_store
from langchain_google_genai import GoogleGenerativeAIEmbeddings


def ingest_documents_from_urls(urls: List[str]):
    documents = []
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001", google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    for url in urls:
        try:
            loader = PyPDFLoader(url)
            documents.extend(loader.load())
        except Exception as e:
            print(f"⚠️ Error loading document from {url}: {e}")

    if not documents:
        print("❌ No documents loaded.")
        return None

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_documents = text_splitter.split_documents(documents)

    vector_store = get_vector_store(embeddings)
    vector_store.add_documents(split_documents)

    print(f"✅ Ingested {len(split_documents)} document chunks.")
    return vector_store
