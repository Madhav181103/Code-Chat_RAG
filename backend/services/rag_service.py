from langchain_google_genai import ChatGoogleGenerativeAI
from config import settings
from services.vectorstore_service import load_vectorstore

def answer_question(repo_name: str, question: str, chat_history: list[dict] = None) -> dict:
    """
    Retrieves the top-k context chunks from ChromaDB for repo_name, builds a structured 
    codebase QA prompt, and queries the Gemini LLM for an answer.
    
    Returns:
        dict: { "answer": str, "sources": list[str] }
    """
    # 1. Load the persisted vector store index for the given repo
    vectorstore = load_vectorstore(repo_name)
    
    # Why k=5 is a reasonable starting point:
    # Too few chunks (e.g. k=1 or 2) might fail to capture all necessary context (like functions in other files 
    # that the main function depends on). Too many chunks (e.g. k=10+) introduces noisy/irrelevant context,
    # increases LLM token processing costs, and can cause slower response times.
    # 5 is a standard, balanced heuristic for an MVP that we can tune later.
    retrieved_docs = vectorstore.similarity_search(question, k=5)
    
    # 2. Build the codebase context string
    # We prefix each chunk text with its respective file_path so the LLM is explicitly aware of where 
    # the code lives and can ground its response inside the repository structure.
    context_parts = []
    for doc in retrieved_docs:
        file_path = doc.metadata.get("file_path", "unknown")
        context_parts.append(f"// File: {file_path}\n{doc.page_content}")
        
    context = "\n\n".join(context_parts)
    
    # 3. Assemble the bound prompt instructions
    prompt = f"""You are a senior software engineer explaining a codebase to a teammate.
Use ONLY the following code context to answer. If the answer isn't in the
context, say so honestly instead of guessing.

CODE CONTEXT:
{context}

QUESTION: {question}

Answer clearly, and mention which file(s) your answer is based on."""

    # 4. Invoke the model
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=settings.GEMINI_API_KEY
    )
    response = llm.invoke(prompt)
    
    # Why we return "sources" separately:
    # LLMs are prone to hallucinating or omitting citations and file paths in their written responses, 
    # even when strictly instructed to list them. By extracting and returning the ground-truth file_path 
    # list from the retrieval step, we ensure the UI can display reliable source cards/citations 
    # that are 100% accurate, regardless of what text the LLM generates.
    unique_sources = list(set(doc.metadata.get("file_path") for doc in retrieved_docs if doc.metadata.get("file_path")))
    
    return {
        "answer": response.content,
        "sources": unique_sources
    }
