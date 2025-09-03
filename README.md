Math Agentic-RAG System

This project is an Agentic-RAG (Retrieval Augmented Generation) system designed to handle math-related queries using LangGraph, Gemini embeddings, and FAISS vector search. The system ingests PDF documents, builds a knowledge base, and answers user queries by combining retrieval from ingested data with web search when needed.

Features

Ingests and processes PDF documents directly from hardcoded URLs in the backend.

Uses Google Gemini embeddings for document representation.

Splits documents into chunks for efficient retrieval.

Stores and queries documents with FAISS vector database.

If the answer is not found in the knowledge base, the system falls back to web search.

Provides a simple Streamlit frontend to ask questions and view responses.

Project Structure
project/
│── app/
│   ├── main.py                # FastAPI entry point
│   ├── api/
│   │   └── endpoints.py        # API routes for query and ingestion
│   ├── core/
│   │   └── agent.py            # LangGraph agent and response logic
│   ├── retriever.py            # FAISS vectorstore setup
│   ├── processing.py           # Document ingestion pipeline
│── frontend/
│   └── app.py                  # Streamlit frontend
│── README.md                   # Project documentation

Setup
1. Clone Repository
git clone https://github.com/your-repo/math-agentic-rag.git
cd math-agentic-rag

2. Create Virtual Environment
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

3. Install Dependencies
pip install -r requirements.txt

4. Set Environment Variables

In your .env file or environment:

GOOGLE_API_KEY=your_gemini_api_key

Running the System
Start Backend (FastAPI)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Start Frontend (Streamlit)
cd frontend
streamlit run app.py

Document Ingestion

The system uses hardcoded PDF URLs inside processing.py. Update the list in:

# processing.py
urls = [
    "https://your-college-site.com/admission-rules.pdf",
    "https://your-college-site.com/maths-syllabus.pdf"
]


Once you update and run the backend, documents are automatically ingested into FAISS.

Querying

You can enter questions in the Streamlit frontend.

If the answer exists in the knowledge base, it is retrieved.

If not, the system performs a web search and generates an answer.

Future Improvements

Replace hardcoded URLs with a database or admin panel for managing sources.

Improve response formatting for math-heavy queries.

Add persistent FAISS storage for reloading without re-ingestion.
