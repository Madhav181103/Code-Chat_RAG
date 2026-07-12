# 🧠 CodeChat — RAG Codebase Q&A Tool

Full-stack codebase chat application powered by Python (FastAPI), LangChain, ChromaDB, Google Gemini API, and React (Vite).

## Project Structure
- `backend/`: FastAPI server for repository cloning, code chunking, indexing, and chat QA retrieval.
- `frontend/`: React Vite app featuring repository input, file tree explorer, code viewer, and QA chat panel.

## Features
- **Git Repository Cloning**: Paste any public GitHub URL to clone it locally.
- **RAG Code Analysis**: Chunks and indexes the codebase using Gemini Embeddings and ChromaDB.
- **Q&A Chat**: Ask questions about the codebase with semantic code searches.
- **Interactive Code Viewer**: See files side-by-side with chat and highlight citations.

## Tech Stack
- **Backend**: FastAPI, LangChain, ChromaDB, Google Gemini API, GitPython
- **Frontend**: React (Vite), Axios, Custom CSS (dark glassmorphism)
