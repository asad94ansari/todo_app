"""
Main FastAPI application for the agent service.
This serves the chat API endpoints.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .chat_endpoint import app as chat_app

# Create main app
app = FastAPI(
    title="Todo Chat API",
    description="AI-powered chat interface for todo management",
    version="1.0.0"
)

# Add CORS middleware to allow communication with the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the chat API routes
app.include_router(chat_app)

@app.get("/")
async def root():
    """Root endpoint for the agent service."""
    return {"message": "Todo Chat API - AI-Powered Todo Management"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "todo-chat-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)