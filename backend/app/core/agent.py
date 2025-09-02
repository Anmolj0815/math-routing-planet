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

# You'll need to add your Tavily API Key to Render's environment variables.
tavily_tool = TavilySearchResults(api_key=os.getenv("TAVILY_API_KEY"))
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GEMINI_API_KEY"))

# Define nodes
def retrieve_documents(state):
    print("---Retrieving documents from knowledge base---")
    vector_store = get_vector_store(embeddings=None)  # Pass actual embeddings here
    retriever = vector_store.as_retriever()
    documents = retriever.invoke(state["query"])
    return {"documents": documents, "route": "knowledge_base"}

def web_search(state):
    print("---Performing web search---")
    tool_input = {"query": state["query"]}
    results = tavily_tool.invoke(tool_input)
    # The MCP part would be integrated here to process results
    return {"documents": [Document(page_content=str(results))], "route": "web_search"}

def generate_response(state):
    print("---Generating final response---")
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
    print("---Routing query---")
    # This is a basic routing logic. You'll need to use an LLM for more advanced routing.
    # E.g., using a prompt like "Is this a specific, known math problem or a general query that requires search?"
    if "web" in state["query"].lower() or "search" in state["query"].lower():
        return "web_search"
    else:
        return "knowledge_base"

# Build the LangGraph
workflow = StateGraph(AgentState)
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
