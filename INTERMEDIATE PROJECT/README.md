# 🤖 Intelligent Document Question-Answering Assistant

### Retrieval-Augmented Generation (RAG) Based Document Q&A System

An AI-powered Document Question-Answering Assistant that allows users to upload PDF/TXT documents or paste document content and ask questions using natural language.

The system uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from the document before generating an answer using a Gemini Large Language Model.

---

## 📌 Project Overview

Reading and searching through large documents manually can be time-consuming.

This project solves this problem by allowing users to:

- 📄 Upload PDF documents
- 📝 Upload TXT documents
- 📋 Paste document content
- 🔎 Ask natural-language questions
- 🧠 Retrieve relevant document sections
- 🤖 Generate answers using an LLM
- 💻 View the answer directly in the web interface

The system does not directly send the entire document to the LLM for every question. Instead, it uses embeddings and vector similarity search to retrieve the most relevant content first.

---

## 🏗️ System Architecture

```text
                 User
                   │
                   ▼
          Web Frontend
       HTML / CSS / JavaScript
                   │
          ┌────────┴────────┐
          │                 │
       PDF/TXT          Copy/Paste
          │                 │
          └────────┬────────┘
                   ▼
             FastAPI Backend
                   │
                   ▼
            Text Extraction
                   │
                   ▼
             Text Cleaning
                   │
                   ▼
                Chunking
                   │
                   ▼
          Gemini Embeddings
                   │
                   ▼
             FAISS Vector DB
                   │
                   │
             User Question
                   ▼
          Question Embedding
                   │
                   ▼
          Similarity Search
                   │
                   ▼
        Relevant Document Chunks
                   │
                   ▼
              Gemini LLM
                   │
                   ▼
            Final Answer
                   │
                   ▼
             Web Frontend