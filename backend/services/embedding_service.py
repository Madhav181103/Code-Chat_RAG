from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import settings

def get_embedding_function() -> GoogleGenerativeAIEmbeddings:
    """
    Returns a configured GoogleGenerativeAIEmbeddings instance using model
    "models/embedding-001" and settings.GEMINI_API_KEY.
    This is passed into Chroma so Chroma can embed both stored chunks AND
    incoming user queries with the exact same model. 
    
    CRITICAL NOTE: Mixing embedding models between storage (indexing) and query 
    (search retrieval) time makes similarity search mathematically meaningless 
    since they project text into different vector space dimensions/distributions.
    """
    return GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=settings.GEMINI_API_KEY
    )
