# 🤖 Production RAG Assistant

A production-style Retrieval-Augmented Generation (RAG) assistant
that allows users to upload documents and ask questions based on
their content.

## 🚀 Features

- PDF / TXT / Markdown document ingestion
- Text preprocessing
- Intelligent document chunking
- Gemini embeddings
- FAISS vector database
- Semantic similarity search
- Query rewriting
- Document retrieval
- Reranking
- LLM-based answer generation
- Groundedness checking
- Source citations
- LangGraph workflow
- FastAPI backend
- Streamlit frontend
- Docker & Docker Compose support

## 🏗️ Architecture

User
 ↓
Streamlit UI
 ↓
FastAPI
 ↓
Document Ingestion
 ↓
Parsing
 ↓
Text Cleaning
 ↓
Chunking
 ↓
Embeddings
 ↓
FAISS
 ↓
Query Rewriting
 ↓
Retrieval
 ↓
Reranking
 ↓
LLM
 ↓
Groundedness
 ↓
Citations
 ↓
Answer

## 🛠️ Tech Stack

| Technology |      Purpose     |
|------------|------------------|
| Python     | Core programming |
| FastAPI    | Backend API      |
| Streamlit  | Frontend UI      |
| LangGraph  | RAG workflow     |
| FAISS      | Vector search    |
| Gemini     | Embeddings & LLM |
| LangChain  | Text processing  |
| PyMuPDF    | PDF parsing      |
| Docker     | Containerization |

## 📁 Project Structure

```text
production-rag/
│
├── app/
│   ├── api/
│   ├── embeddings/
│   ├── generation/
│   ├── graph/
│   ├── ingestion/
│   └── retrieval/
│
├── frontend/
│
├── data/
│   ├── uploads/
│   └── indexes/
│
├── .env
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md