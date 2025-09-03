from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.tools.tavily_search import TavilySearchResults
from .retriever import get_vector_store
import os

# ----------------- STATE -----------------
class AgentState(TypedDict):
    query: str
    documents: List[Document]
    route: str
    response: str

# ----------------- MODELS -----------------
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")  # ✅ force API key
)

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")  # ✅ force API key
)

tavily_tool = TavilySearchResults(api_key=os.getenv("TAVILY_API_KEY"))

# ----------------- NODES -----------------
def retrieve_documents(state: AgentState):
    vector_store = get_vector_store(embeddings=embeddings)
    retriever = vector_store.as_retriever()
    documents = retriever.invoke(state["query"])
    return {"documents": documents, "route": "knowledge_base"}

def web_search(state: AgentState):
    tool_input = {"query": state["query"]}
    results = tavily_tool.invoke(tool_input)
    return {"documents": [Document(page_content=str(results))], "route": "web_search"}

def generate_response(state: AgentState):
    prompt = ChatPromptTemplate.from_template("""
        You are a helpful **Math Tutor Agent**. 
        Use the following documents or knowledge to answer the student's math-related question.

        Question: {query}
        Documents: {documents}

        Provide a clear step-by-step solution and explanation.
        If relevant, include examples or formulas.
    """)
    document_chain = create_stuff_documents_chain(llm, prompt)
    response = document_chain.invoke(
        {"documents": state["documents"], "query": state["query"]}
    )
    return {"response": response}

def router_node(state: AgentState):
    if "web" in state["query"].lower() or "search" in state["query"].lower():
        return {"route": "web_search"}
    else:
        return {"route": "knowledge_base"}


# ----------------- WORKFLOW -----------------
workflow = StateGraph(AgentState)

workflow.add_node("router", router_node)
workflow.add_node("retrieve_documents", retrieve_documents)
workflow.add_node("web_search", web_search)
workflow.add_node("generate_response", generate_response)

workflow.add_conditional_edges(
    "router",
    lambda x: x["route"],   # ✅ route dict se nikalo
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
