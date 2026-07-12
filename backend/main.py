import os
import logging
import traceback
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config import settings

from routes import repo_routes, chat_routes, file_routes

app = FastAPI(title="CodeChat API")

# Add CORS Middleware to allow React frontend (reads CLIENT_URL from env, defaults to local port 5173)
client_url = os.getenv("CLIENT_URL", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[client_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    return {"message": "CodeChat API is running"}

# Register repository, chat and file routes
app.include_router(repo_routes.router)
app.include_router(chat_routes.router)
app.include_router(file_routes.router)

# Configure basic logging formatting
logging.basicConfig(level=logging.ERROR, format="%(asctime)s [%(levelname)s] %(message)s")

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    # Log the real traceback internally to the console/files, but hide it from the client
    # to avoid leaking repository paths, library versions, or raw credentials.
    tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    logging.error(f"Unhandled Exception: {str(exc)}\nTraceback:\n{tb}")
    
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please try again."}
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)
