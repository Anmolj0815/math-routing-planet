from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..core.processing import ingest_documents_from_urls
from ..core.retriever import get_vector_store
from ..core.agent import generate_response

router = APIRouter()

# Global vector store (shared after ingestion)
vector_store = None


class IngestRequest(BaseModel):
    urls: list[str]


class QueryRequest(BaseModel):
    query: str


@router.post("/ingest")
async def ingest_docs(request: IngestRequest):
    global vector_store
    vector_store = ingest_documents_from_urls(request.urls)
    if vector_store:
        return {"status": "success", "message": "Documents ingested successfully."}
    raise HTTPException(status_code=400, detail="Failed to ingest documents")


@router.post("/query")
async def process_query(request: QueryRequest):
    global vector_store
    if not vector_store:
        vector_store = get_vector_store()

    try:
        answer = generate_response(request.query, vector_store)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
