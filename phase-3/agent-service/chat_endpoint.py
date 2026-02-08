"""
Chat API endpoint for the AI Orchestrator agent.
Implements the POST /api/chat endpoint for conversation handling.
"""
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import asyncio
from datetime import datetime

from .agent import TodoAssistantAgent

app = FastAPI()

class ChatRequest(BaseModel):
    """Request model for chat API."""
    message: str
    conversation_id: Optional[str] = None
    user_id: int  # Will be extracted from JWT in real implementation
    timestamp: Optional[str] = None

class ChatResponse(BaseModel):
    """Response model for chat API."""
    reply: str
    conversation_id: str
    actions_taken: List[Dict[str, Any]]
    timestamp: str

# Initialize the agent
agent = TodoAssistantAgent()

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatRequest) -> ChatResponse:
    """
    Main chat endpoint that accepts user messages and returns agent responses.

    Args:
        chat_request: The incoming chat request containing user message and context

    Returns:
        ChatResponse containing the agent's reply and metadata
    """
    try:
        # Process the message through the AI agent
        agent_response = agent.process_message(
            message=chat_request.message,
            user_id=chat_request.user_id,
            conversation_id=chat_request.conversation_id
        )

        # Create response with current timestamp
        response = ChatResponse(
            reply=agent_response,
            conversation_id=chat_request.conversation_id or f"conv_{int(datetime.now().timestamp())}",
            actions_taken=[],  # In a real implementation, we would track tool calls
            timestamp=datetime.now().isoformat()
        )

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")

class ChatHistoryRequest(BaseModel):
    """Request model for getting chat history."""
    conversation_id: str
    user_id: int
    limit: Optional[int] = 20
    offset: Optional[int] = 0

class ChatHistoryResponse(BaseModel):
    """Response model for chat history."""
    messages: List[Dict[str, Any]]
    conversation_id: str
    total_messages: int

@app.get("/api/chat/history", response_model=ChatHistoryResponse)
async def get_chat_history(request: ChatHistoryRequest = Depends()) -> ChatHistoryResponse:
    """
    Endpoint to retrieve conversation history.
    NOTE: This is a simplified version - in a real implementation,
    conversation history would be stored in a database.
    """
    # In a real implementation, this would fetch from a database
    # For now, return an empty history
    return ChatHistoryResponse(
        messages=[],
        conversation_id=request.conversation_id,
        total_messages=0
    )

class NewConversationRequest(BaseModel):
    """Request model for starting a new conversation."""
    user_id: int

class NewConversationResponse(BaseModel):
    """Response model for starting a new conversation."""
    conversation_id: str
    message: str

@app.post("/api/chat/new", response_model=NewConversationResponse)
async def start_new_conversation(request: NewConversationRequest) -> NewConversationResponse:
    """
    Endpoint to start a new conversation.
    """
    import time
    new_conv_id = f"conv_{request.user_id}_{int(time.time())}"

    return NewConversationResponse(
        conversation_id=new_conv_id,
        message="New conversation started successfully"
    )