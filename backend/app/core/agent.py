import os
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from langchain_community.tools import TavilySearchResults

# ✅ Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# ----------- LangGraph State -----------
from typing import TypedDict, List

class AgentState(TypedDict):
    query: str
    context: List[str]
    answer: str


# ----------- Retriever Node -----------
def retrieve(state: AgentState, vectorstore: FAISS):
    """Retrieve top chunks from FAISS knowledge base."""
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    docs = retriever.get_relevant_documents(state["query"])
    state["context"] = [doc.page_content for doc in docs]
    return state


# ----------- Web Search Node -----------
def web_search(state: AgentState):
    """Fallback to web search if no context found."""
    tool = TavilySearchResults(max_results=3)
    results = tool.invoke({"query": state["query"]})
    snippets = [r["content"] for r in results]
    state["context"] = snippets
    return state


# ----------- Generator Node -----------
def generate(state: AgentState):
    """Generate final math solution using Gemini."""
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

    prompt = ChatPromptTemplate.from_template("""
    You are a **Math Problem Solving Assistant**.
    Solve the query step by step. 
    If context is provided, use it. 
    If not, solve using general math knowledge.
    
    Question: {query}
    
    Context:
    {context}
    
    Answer:
    """)

    chain = prompt | llm
    response = chain.invoke({"query": state["query"], "context": "\n".join(state["context"])})
    state["answer"] = response.content
    return state


# ----------- Router Node (decide KB or Web) -----------
def router(state: AgentState):
    """Decide whether to use knowledge base or web search."""
    if state["context"]:  # already filled by retriever
        return "generate"
    else:
        return "web_search"


# ----------- Build Math Agent Graph -----------
def build_math_agent(vectorstore: FAISS):
    workflow = StateGraph(AgentState)

    # Nodes
    workflow.add_node("retrieve", lambda s: retrieve(s, vectorstore))
    workflow.add_node("web_search", web_search)
    workflow.add_node("generate", generate)

    # Edges
    workflow.set_entry_point("retrieve")
    workflow.add_conditional_edges("retrieve", router, {"generate": "generate", "web_search": "web_search"})
    workflow.add_edge("web_search", "generate")
    workflow.add_edge("generate", END)

    return workflow.compile()


# ----------- Public API -----------
def generate_response(query: str, vectorstore: FAISS) -> str:
    """Run the Math Agent pipeline."""
    agent = build_math_agent(vectorstore)
    result = agent.invoke({"query": query, "context": [], "answer": ""})
    return result["answer"]
