"""
MCP Server for the AI Chatbot Integration.
This server exposes task management tools to the OpenAI agent via MCP protocol.
"""
import asyncio
import json
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from .database.connection import get_db_session
from .auth.validator import validate_user_auth

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Todo MCP Server",
    description="MCP server for todo management tools",
    version="1.0.0"
)

class ToolCall(BaseModel):
    tool_name: str
    parameters: Dict[str, Any]

class ToolResult(BaseModel):
    result: Any
    success: bool
    message: str = ""

@app.get("/health")
async def health_check():
    """Health check endpoint for the MCP server."""
    return {"status": "healthy", "service": "todo-mcp-server"}

@app.post("/mcp/tool")
async def call_tool(tool_call: ToolCall, user_id: int = Depends(validate_user_auth)):
    """
    Generic endpoint to call any registered tool.
    This follows the MCP protocol pattern for tool invocation.
    """
    try:
        # Based on the tool name, call the appropriate function
        if tool_call.tool_name == "add_todo":
            from .tools.add_todo import add_todo
            result = await add_todo(user_id, **tool_call.parameters)
        elif tool_call.tool_name == "get_todos":
            from .tools.get_todos import get_todos
            result = await get_todos(user_id, **tool_call.parameters)
        elif tool_call.tool_name == "update_todo_status":
            from .tools.update_todo_status import update_todo_status
            result = await update_todo_status(user_id, **tool_call.parameters)
        else:
            raise HTTPException(status_code=404, detail=f"Tool {tool_call.tool_name} not found")

        return ToolResult(result=result, success=True)
    except Exception as e:
        return ToolResult(result=None, success=False, message=str(e))

# Additional MCP-specific endpoints can be added here
@app.get("/mcp/tools")
async def list_tools():
    """List all available tools in the MCP server."""
    tools = [
        {
            "name": "add_todo",
            "description": "Create a new task for the authenticated user",
            "parameters": {
                "title": "string (required) - The title of the new task",
                "description": "string (optional) - Additional details about the task",
                "due_date": "string (optional) - Due date in ISO format",
                "priority": "string (optional) - Priority level (low, medium, high)"
            }
        },
        {
            "name": "get_todos",
            "description": "Retrieve tasks for the authenticated user with optional filtering",
            "parameters": {
                "status": "string (optional) - Filter by status (all, completed, pending)",
                "limit": "number (optional) - Maximum number of tasks to return (default: 20)",
                "offset": "number (optional) - Number of tasks to skip (for pagination)"
            }
        },
        {
            "name": "update_todo_status",
            "description": "Update the completion status of a specific task",
            "parameters": {
                "task_id": "number (required) - The ID of the task to update",
                "status": "boolean (required) - The new completion status (true for completed, false for pending)",
                "notes": "string (optional) - Additional notes about the update"
            }
        }
    ]
    return {"tools": tools}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)