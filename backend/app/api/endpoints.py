from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from ..core.processing import ingest_documents_from_urls
from ..core.agent import math_agent_executor

router = APIRouter()

class IngestRequest(BaseModel):
    urls: List[str]

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    decision: str
    amount: Optional[float] = None
    justification: str
    clauses_used: List[str]

@router.post("/ingest")
async def ingest_documents(request: IngestRequest):
    try:
        success = ingest_documents_from_urls(request.urls)
        if not success:
            raise HTTPException(status_code=500, detail="Document ingestion failed.")
        return {"message": "Documents ingested successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    try:
        result = await math_agent_executor.invoke({"input": request.query})
        
        # NOTE: You must replace this with the actual structured output from your agent.
        return {
            "decision": "placeholder_decision",
            "amount": 0.0,
            "justification": "This is a placeholder justification based on the processed query.",
            "clauses_used": ["placeholder_clause_1", "placeholder_clause_2"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
