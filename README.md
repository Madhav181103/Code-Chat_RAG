# 🧠 CodeChat — Chat With Any GitHub Repo (RAG)

> Paste a public GitHub repo URL, and ask questions about the codebase in plain English — powered by Retrieval-Augmented Generation.

## How It Works
1. Paste a repo URL → backend clones it
2. Backend chunks every source file and embeds each chunk (Gemini Embeddings)
3. Chunks are stored in a local Chroma vector database
4. When you ask a question, the top-5 most relevant chunks are retrieved and handed to Gemini along with your question
5. Gemini answers using ONLY that retrieved code, and cites which files it used

## Tech Stack
| Layer | Tech |
|-------|------|
| Backend | Python, FastAPI, LangChain |
| Embeddings + LLM | Google Gemini (embedding-001 + gemini-1.5-flash) |
| Vector Store | ChromaDB (local, persisted to disk) |
| Repo Cloning | GitPython |
| Frontend | React (Vite), Axios |

## Local Setup
```bash
# Backend
cd backend
python -m venv venv
# Activate virtualenv:
# On Unix: source venv/bin/activate
# On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # Add your GEMINI_API_KEY
uvicorn main:app --reload

# Frontend (new terminal)
cd frontend
cp .env.example .env
npm install
npm run dev
```

## Example Questions To Try
- "What does this repo do?"
- "Where is authentication handled?"
- "Explain the main entry point"
- "Are there any database models? List them."

## Architecture Diagram
```
repo URL → clone → chunk files → embed chunks → store in Chroma → [user question] → retrieve top-K chunks → Gemini → answer + sources
```
