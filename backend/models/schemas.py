from pydantic import BaseModel

class IngestRequest(BaseModel):
    """
    Schema for repository ingestion requests.
    Used by: POST /api/repo/ingest
    """
    repo_url: str

class IngestResponse(BaseModel):
    """
    Schema for repository ingestion responses.
    Returned by: POST /api/repo/ingest
    """
    repo_name: str
    file_count: int
    chunk_count: int
    message: str

class ChatRequest(BaseModel):
    """
    Schema for repository chat queries.
    Used by: POST /api/chat
    """
    repo_name: str
    question: str

class ChatResponse(BaseModel):
    """
    Schema for codebase QA responses.
    Returned by: POST /api/chat
    """
    answer: str
    sources: list[str]

class FileTreeResponse(BaseModel):
    """
    Schema representing the structure/files of an ingested repository.
    Returned by: GET /api/repo/{repo_name}/files
    """
    repo_name: str
    files: list[str]
