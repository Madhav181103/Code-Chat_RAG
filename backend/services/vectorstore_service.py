import os
import shutil
from langchain_community.vectorstores import Chroma
from services.embedding_service import get_embedding_function
from config import settings

def build_vectorstore(repo_name: str, chunks: list[dict]) -> Chroma:
    """
    Creates (or overwrites) a Chroma collection named after repo_name.
    Persist directory: os.path.join(settings.CHROMA_PERSIST_DIR, repo_name)
    Uses Chroma.from_texts() to build and return the vector store.
    """
    persist_directory = os.path.join(settings.CHROMA_PERSIST_DIR, repo_name)
    
    # Overwrite check: If the persistent database directory already exists, delete it.
    # This prevents duplicate data and ensures that re-ingesting a repository creates a 
    # clean, fresh database index rather than appending chunks to the old database.
    if os.path.exists(persist_directory):
        shutil.rmtree(persist_directory)
        
    # Ensure the parent persist directory exists
    os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)
    
    texts = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    ids = [c["id"] for c in chunks]
    embedding = get_embedding_function()
    
    vectorstore = Chroma.from_texts(
        texts=texts,
        metadatas=metadatas,
        ids=ids,
        embedding=embedding,
        persist_directory=persist_directory
    )
    
    return vectorstore

def load_vectorstore(repo_name: str) -> Chroma:
    """
    Loads an EXISTING Chroma collection for a repo that was already ingested.
    
    Why persisting to disk (and not keeping it only in memory) matters:
    1. Performance/Caching: Embedding a codebase requires calling the Gemini API
       for every single text chunk, which takes time and costs money. Persisting to disk
       serves as an efficient cache.
    2. Resilience: If the FastAPI server restarts, already-ingested repositories 
       do not need to be re-cloned or re-embedded. We can load the index instantly.
    """
    persist_directory = os.path.join(settings.CHROMA_PERSIST_DIR, repo_name)
    
    if not os.path.exists(persist_directory):
        raise FileNotFoundError(f"No persistent vector store found for repository: {repo_name}")
        
    embedding = get_embedding_function()
    
    return Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding
    )
