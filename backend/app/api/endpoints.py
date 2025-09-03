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
        print(f"📩 Received query: {request.query}")

        # --- Call the agent ---
        try:
            result = await math_agent_executor.invoke({"input": request.query})
            print(f"✅ Agent raw result: {result}")
        except Exception as agent_error:
            print("❌ Error while calling agent:")
            print(traceback.format_exc())
            # Return graceful JSON response
            return QueryResponse(
                decision="ERROR",
                amount=None,
                justification=f"Agent execution failed: {str(agent_error)}",
                clauses_used=["No clauses extracted"]
            )

        # --- Parse the result ---
        if isinstance(result, dict) and 'output' in result:
            agent_output = result['output']
        else:
            agent_output = str(result)

        print(f"📝 Parsed agent output: {agent_output}")

        # Default values
        decision = "UNDER_REVIEW"
        amount = None
        justification = agent_output
        clauses_used = []

        try:
            # Decision parsing
            if "APPROVED" in agent_output.upper():
                decision = "APPROVED"
            elif "REJECTED" in agent_output.upper() or "DENIED" in agent_output.upper():
                decision = "REJECTED"

            # Amount parsing
            amount_match = re.search(r'\$?(\d+(?:,\d{3})*(?:\.\d{2})?)', agent_output)
            if amount_match:
                amount_str = amount_match.group(1).replace(',', '')
                amount = float(amount_str)

            # Clause extraction
            clause_patterns = [
                r'clause\s+(\d+)',
                r'section\s+(\w+)',
                r'article\s+(\w+)',
            ]
            for pattern in clause_patterns:
                matches = re.findall(pattern, agent_output, re.IGNORECASE)
                clauses_used.extend([f"Clause {match}" for match in matches])

        except Exception as parse_error:
            print("⚠️ Parsing error:")
            print(traceback.format_exc())
            justification += f"\n\n(Parsing error: {str(parse_error)})"

        if not clauses_used:
            clauses_used = ["Based on document analysis"]

        # --- Always return structured JSON ---
        return QueryResponse(
            decision=decision,
            amount=amount,
            justification=justification,
            clauses_used=clauses_used,
        )

    except Exception as e:
        # Catch-all safeguard
        print("💥 Unexpected error in process_query:")
        print(traceback.format_exc())
        return QueryResponse(
            decision="ERROR",
            amount=None,
            justification=f"Unexpected error: {str(e)}",
            clauses_used=["No clauses extracted"]
        )
