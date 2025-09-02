from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from .retriever import get_vector_store
import os

class AgentState(TypedDict):
    query: str
    documents: List[Document]
    route: str
    response: str

tavily_tool = TavilySearchResults(api_key=os.getenv("TAVILY_API_KEY"))
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GEMINI_API_KEY"))

def retrieve_documents(state):
    embeddings=None
    vector_store = get_vector_store(embeddings=embeddings)
    retriever = vector_store.as_retriever()
    documents = retriever.invoke(state["query"])
    return {"documents": documents, "route": "knowledge_base"}

def web_search(state):
    tool_input = {"query": state["query"]}
    results = tavily_tool.invoke(tool_input)
    return {"documents": [Document(page_content=str(results))], "route": "web_search"}

def generate_response(state):
    prompt = ChatPromptTemplate.from_template("""
        Answer the user's query based on the following documents:
        {documents}
        Query: {query}
        Provide the answer in a structured JSON format with Decision, Amount, and Justification.
    """)
    document_chain = create_stuff_documents_chain(llm, prompt)
    response = document_chain.invoke({"documents": state["documents"], "query": state["query"]})
    return {"response": response}

def router_node(state):
    if "web" in state["query"].lower() or "search" in state["query"].lower():
        return "web_search"
    else:
        return "knowledge_base"

workflow = StateGraph(AgentState)

# This is the line that was missing and caused the error
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

math_agent_executor = workflow.compile()
