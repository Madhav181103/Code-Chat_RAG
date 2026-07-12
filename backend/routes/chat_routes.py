from fastapi import APIRouter, HTTPException
from models.schemas import ChatRequest, ChatResponse
from services.rag_service import answer_question

router = APIRouter(prefix="/api/chat", tags=["Codebase Chat"])

@router.post("", response_model=ChatResponse)
async def chat_with_repo(request: ChatRequest):
    """
    Handles user queries about a specific repository by retrieving context from 
    its ChromaDB collection and querying Gemini to generate a response.
    """
    repo_name = request.repo_name.strip()
    question = request.question.strip()
    
    try:
        result = answer_question(repo_name, question)
    except FileNotFoundError as e:
        # Raised if load_vectorstore detects the db path does not exist
        raise HTTPException(
            status_code=404,
            detail="Repo not found. Please ingest it first via /api/repo/ingest"
        )
    except Exception as e:
        # Generic safety boundary for embedding client issues or configuration discrepancies
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while answering your question: {str(e)}"
        )
        
    return ChatResponse(
        answer=result["answer"],
        sources=result["sources"]
    )
