import os
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from langchain_community.tools import TavilySearchResults
from typing import TypedDict, List

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


class AgentState(TypedDict):
    query: str
    context: List[str]
    answer: str


def retrieve(state: AgentState, vectorstore: FAISS):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    docs = retriever.get_relevant_documents(state["query"])
    state["context"] = [doc.page_content for doc in docs]
    return state


def web_search(state: AgentState):
    tool = TavilySearchResults(max_results=3)
    results = tool.invoke({"query": state["query"]})
    snippets = [r["content"] for r in results]
    state["context"] = snippets
    return state


def generate(state: AgentState):
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


def router(state: AgentState):
    if state["context"]:
        return "generate"
    else:
        return "web_search"


def build_math_agent(vectorstore: FAISS):
    workflow = StateGraph(AgentState)

    workflow.add_node("retrieve", lambda s: retrieve(s, vectorstore))
    workflow.add_node("web_search", web_search)
    workflow.add_node("generate", generate)

    workflow.set_entry_point("retrieve")
    workflow.add_conditional_edges("retrieve", router, {"generate": "generate", "web_search": "web_search"})
    workflow.add_edge("web_search", "generate")
    workflow.add_edge("generate", END)

    return workflow.compile()


def generate_response(query: str, vectorstore: FAISS) -> str:
    agent = build_math_agent(vectorstore)
    result = agent.invoke({"query": query, "context": [], "answer": ""})
    return result["answer"]
