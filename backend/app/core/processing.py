import os
from typing import Optional
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .retriever import get_vector_store
from langchain_google_genai import GoogleGenerativeAIEmbeddings


def ingest_documents_from_urls() -> Optional[any]:
    """
    Ingest documents directly from fixed hardcoded PDF URLs.
    Steps:
    1. Load PDFs from the provided URLs
    2. Split into smaller chunks
    3. Create embeddings using Gemini
    4. Store them into FAISS vectorstore
    Returns the vectorstore object if successful.
    """

    # ✅ Put your final PDF URLs here
    urls = [
        "https://www.tutor.com/cmspublicfiles/www/concept-list.pdf",
        # Add as many as you want here
    ]

    documents = []

    # ✅ Initialize Gemini Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    # ✅ Load PDFs
    for url in urls:
        try:
            loader = PyPDFLoader(url)
            docs = loader.load()
            documents.extend(docs)
            print(f"📄 Loaded {len(docs)} pages from {url}")
        except Exception as e:
            print(f"⚠️ Error loading document from {url}: {e}")

    if not documents:
        print("❌ No documents were loaded. Check URLs.")
        return None

    # ✅ Split docs into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    split_documents = text_splitter.split_documents(documents)

    # ✅ Create / load FAISS vectorstore
    vector_store = get_vector_store(embeddings)
    vector_store.add_documents(split_documents)

    print(f"✅ Ingested {len(split_documents)} chunks from {len(urls)} PDFs.")
    return vector_store
