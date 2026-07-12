from fastapi import APIRouter, HTTPException
from models.schemas import IngestRequest, IngestResponse
from services.git_service import clone_repo, get_repo_name
from utils.file_utils import walk_repo_files
from services.chunking_service import chunk_repo_files
from services.vectorstore_service import build_vectorstore
from config import settings

router = APIRouter(prefix="/api/repo", tags=["Repository Ingestion"])

@router.post("/ingest", response_model=IngestResponse)
async def ingest_repository(request: IngestRequest):
    repo_url = request.repo_url.strip()
    print(f"\n[Ingest] Starting ingestion process for repository URL: {repo_url}")
    
    # 1. Derive the repository folder name
    try:
        repo_name = get_repo_name(repo_url)
        print(f"[Ingest] Resolved repository name: {repo_name}")
    except Exception as e:
        print(f"[Ingest] Error parsing repository URL: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid repository URL provided.")
        
    # 2. Clone the repository
    print(f"[Ingest] Cloning repository '{repo_name}' to disk...")
    try:
        repo_path = clone_repo(repo_url)
        print(f"[Ingest] Repository cloned successfully to: {repo_path}")
    except ValueError as e:
        print(f"[Ingest] Clone failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
        
    # 3. Walk and filter the files
    print(f"[Ingest] Walking and scanning cloned directory for supported code files...")
    files = walk_repo_files(repo_path, settings.MAX_FILE_SIZE_KB)
    file_count = len(files)
    print(f"[Ingest] Found {file_count} valid files meeting filters and size limits.")
    
    if file_count == 0:
        print(f"[Ingest] Ingestion aborted: No supported code/text files found in the repository.")
        raise HTTPException(status_code=400, detail="No supported source files found in this repo")
        
    # 4. Segment files into chunks
    print(f"[Ingest] Segmenting files into code chunks...")
    chunks = chunk_repo_files(files)
    chunk_count = len(chunks)
    print(f"[Ingest] Segmented {file_count} files into {chunk_count} text chunks.")
    
    # 5. Generate embeddings and persist database
    print(f"[Ingest] Constructing vector embeddings and persisting to ChromaDB database...")
    try:
        build_vectorstore(repo_name, chunks)
        print(f"[Ingest] Database build complete and persisted successfully.")
    except Exception as e:
        print(f"[Ingest] Embeddings/ChromaDB build failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate embeddings: {str(e)}")
        
    message = f"Successfully ingested {file_count} files into {chunk_count} chunks"
    return IngestResponse(
        repo_name=repo_name,
        file_count=file_count,
        chunk_count=chunk_count,
        message=message
    )
