from pydantic import BaseModel
from typing import List, Optional

class IngestRequest(BaseModel):
    urls: List[str]

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    decision: str
    amount: Optional[float] = None
    justification: str
    clauses_used: List[str]
