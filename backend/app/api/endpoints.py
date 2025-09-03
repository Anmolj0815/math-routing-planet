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
        print(f"Processing query: {request.query}")
        
        # Call the agent
        result = await math_agent_executor.invoke({"input": request.query})
        
        print(f"Agent result: {result}")
        
        # Parse the agent result
        # The result structure depends on how your agent returns data
        # Common patterns:
        
        # Pattern 1: If result is a dict with 'output' key
        if isinstance(result, dict) and 'output' in result:
            agent_output = result['output']
        else:
            agent_output = str(result)
        
        # Now you need to parse the agent_output to extract:
        # - decision (APPROVED/REJECTED/etc.)
        # - amount (if any)
        # - justification
        # - clauses_used
        
        # Example parsing (adjust based on your agent's actual output format):
        decision = "PENDING"  # Default
        amount = None
        justification = agent_output  # Use full output as justification for now
        clauses_used = []
        
        # If your agent returns structured data, parse it properly
        # For example, if agent returns JSON-like structure:
        try:
            import json
            import re
            
            # Try to find decision in the output
            if "APPROVED" in agent_output.upper():
                decision = "APPROVED"
            elif "REJECTED" in agent_output.upper() or "DENIED" in agent_output.upper():
                decision = "REJECTED"
            else:
                decision = "UNDER_REVIEW"
            
            # Try to extract amount using regex
            amount_match = re.search(r'\$?(\d+(?:,\d{3})*(?:\.\d{2})?)', agent_output)
            if amount_match:
                amount_str = amount_match.group(1).replace(',', '')
                amount = float(amount_str)
            
            # Extract clauses (if mentioned in output)
            clause_patterns = [
                r'clause\s+(\d+)',
                r'section\s+(\w+)',
                r'article\s+(\w+)',
            ]
            
            for pattern in clause_patterns:
                matches = re.findall(pattern, agent_output, re.IGNORECASE)
                clauses_used.extend([f"Clause {match}" for match in matches])
            
        except Exception as parse_error:
            print(f"Parsing error: {parse_error}")
            # Keep defaults
        
        return {
            "decision": decision,
            "amount": amount,
            "justification": justification,
            "clauses_used": clauses_used if clauses_used else ["Based on document analysis"],
        }
        
    except Exception as e:
        print(f"Error in process_query: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")
