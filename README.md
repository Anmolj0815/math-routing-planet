Math Agentic-RAG System

This project implements an Agentic-RAG (Retrieval-Augmented Generation) system for solving math-related queries. It combines:

Google Gemini (LLM + Embeddings) for reasoning and semantic search

LangGraph for building an agent workflow (router, retriever, web search fallback)

FAISS for vector similarity search over ingested documents

FastAPI + Streamlit for backend and frontend integration

The system can:

Retrieve answers from pre-ingested math-related documents (textbooks, syllabus PDFs, etc.)

Perform web search when no relevant context is found

Generate structured, step-by-step math solutions

🚀 Features

Document Ingestion: Upload PDF documents (e.g., textbooks, syllabus, problem banks)

Vector Store: Uses FAISS with Gemini embeddings for efficient semantic search

Agent Workflow (LangGraph):

Router Node: Decides whether to use knowledge base or web search

Knowledge Base Node: Retrieves relevant document chunks

Web Search Node: Uses Tavily API for fallback searching

Response Generator: Produces structured answers with explanations

Frontend: Streamlit UI for uploading documents and asking math questions

Backend: FastAPI service exposing /api/query and /api/ingest endpoints
