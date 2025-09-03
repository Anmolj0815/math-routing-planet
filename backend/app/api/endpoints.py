from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
import traceback
import re
from .agent import math_agent_executor  # import from your package

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    decision: str
    amount: Optional[float] = None
    justification: str
    clauses_used: List[str]

@router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    try:
        print(f"📩 Received query: {request.query}")

        # --- Call graph ASYNC and with correct state key ---
        try:
            result_state = await math_agent_executor.ainvoke({"query": request.query})
            print(f"✅ Graph state out: {result_state}")
        except Exception as agent_error:
            print("❌ Error while calling graph:")
            print(traceback.format_exc())
            return QueryResponse(
                decision="ERROR",
                amount=None,
                justification=f"Agent execution failed: {str(agent_error)}",
                clauses_used=["No clauses extracted"]
            )

        # The graph writes final text into result_state["response"]
        agent_output = str(result_state.get("response", ""))

        # --- Parse into your schema ---
        decision = "UNDER_REVIEW"
        amount = None
        justification = agent_output
        clauses_used: List[str] = []

        # Try to find structured JSON first (since we told LLM to return JSON)
        try:
            import json
            parsed = json.loads(agent_output)
            # Normalize keys in a tolerant way
            decision = str(parsed.get("Decision", decision)).upper()
            amount = parsed.get("Amount", amount)
            justification = parsed.get("Justification", justification)
        except Exception:
            # If it wasn't valid JSON, fall back to regex parsing
            up = agent_output.upper()
            if "APPROVED" in up:
                decision = "APPROVED"
            elif "REJECTED" in up or "DENIED" in up:
                decision = "REJECTED"

            amt_match = re.search(r'\$?(\d+(?:,\d{3})*(?:\.\d{1,2})?)', agent_output)
            if amt_match:
                amount = float(amt_match.group(1).replace(",", ""))

        # Extract clause-like mentions, if any
        for pat in [r'clause\s+([\w\-\.]+)', r'section\s+([\w\-\.]+)', r'article\s+([\w\-\.]+)']:
            for m in re.findall(pat, agent_output, flags=re.IGNORECASE):
                clauses_used.append(f"Clause {m}")

        if not clauses_used:
            clauses_used = ["Based on document analysis"]

        return QueryResponse(
            decision=decision,
            amount=amount,
            justification=justification,
            clauses_used=clauses_used
        )

    except Exception as e:
        print("💥 Unexpected error in /query:")
        print(traceback.format_exc())
        # Never raise HTTPException; return JSON so the frontend never sees a 500
        return QueryResponse(
            decision="ERROR",
            amount=None,
            justification=f"Unexpected error: {str(e)}",
            clauses_used=["No clauses extracted"]
        )
