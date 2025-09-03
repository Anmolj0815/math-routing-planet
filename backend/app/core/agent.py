from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List
from langchain_core.documents import Document
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from .retriever import get_vector_store
import os
import json

class AgentState(TypedDict):
    query: str
    documents: List[Document]
    route: str
    response: str  # final text response from the LLM

# --- LLM + Embeddings ---
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_KEY:
    raise RuntimeError("GEMINI_API_KEY not set")

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GEMINI_KEY)

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=GEMINI_KEY
)

# --- Optional Tavily tool (handle missing key gracefully) ---
TAVILY_KEY = os.getenv("TAVILY_API_KEY")
tavily_tool = TavilySearchResults(api_key=TAVILY_KEY) if TAVILY_KEY else None

def retrieve_documents(state: AgentState):
    vector_store = get_vector_store(embeddings=embeddings)
    retriever = vector_store.as_retriever()
    docs = retriever.invoke(state["query"])
    # Ensure docs are List[Document]
    if docs is None:
        docs = []
    return {"documents": docs, "route": "knowledge_base"}

def web_search(state: AgentState):
    if not tavily_tool:
        # Fallback if no Tavily API key
        msg = "Tavily API key not configured; falling back to empty results."
        return {"documents": [Document(page_content=msg)], "route": "web_search"}
    results = tavily_tool.invoke({"query": state["query"]})
    # keep it as a single Document with result JSON
    return {"documents": [Document(page_content=json.dumps(results, ensure_ascii=False))], "route": "web_search"}

def generate_response(state):
    prompt = ChatPromptTemplate.from_template("""
        You are a helpful math tutor. 
        Solve the following question step by step. 
        Show clear reasoning and intermediate steps before giving the final answer. 
        If the query is theoretical, explain the concept in detail with examples. 
        Always return your response in **plain text** with two sections:
        
        - Explanation: (step-by-step reasoning, formulas, or concept details)
        - Final Answer: (the simplified final result)

        Question: {query}
        Context documents (if any): {documents}
    """)
    
    document_chain = create_stuff_documents_chain(llm, prompt)
    response = document_chain.invoke({"documents": state["documents"], "query": state["query"]})
    return {"response": response}


def router_node(state: AgentState):
    q = state.get("query", "") or ""
    if "web" in q.lower() or "search" in q.lower():
        return "web_search"
    return "knowledge_base"

workflow = StateGraph(AgentState)

# router must be an actual node if you use conditional edges from it
workflow.add_node("router", router_node)
workflow.add_node("retrieve_documents", retrieve_documents)
workflow.add_node("web_search", web_search)
workflow.add_node("generate_response", generate_response)

workflow.add_conditional_edges(
    "router",
    router_node,
    {
        "knowledge_base": "retrieve_documents",
        "web_search": "web_search",
    },
)

workflow.add_edge("retrieve_documents", "generate_response")
workflow.add_edge("web_search", "generate_response")
workflow.add_edge("generate_response", END)
workflow.set_entry_point("router")

# Runnable graph (supports invoke / ainvoke)
math_agent_executor = workflow.compile()
