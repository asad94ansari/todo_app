# API Contracts: Phase III — AI Chatbot Integration

**Feature**: Phase III — AI Chatbot Integration
**Contract Version**: 1.0
**Created**: 2026-02-07

## Purpose
Defines the API contracts for the AI chatbot integration, including MCP tools, chat API endpoints, and agent communication protocols.

## MCP Tool Definitions

### add_todo Tool
- **Tool Name**: `add_todo`
- **Description**: Creates a new task for the authenticated user
- **Parameters**:
  - `title`: string (required) - The title of the new task
  - `description`: string (optional) - Additional details about the task
  - `due_date`: string (optional) - Due date in ISO format
  - `priority`: string (optional) - Priority level (low, medium, high)
- **Authentication**: Requires valid user ID in context
- **Returns**:
  - Success: `{ "id": 123, "status": "created", "message": "Task created successfully" }`
  - Error: `{ "error": "string", "message": "Human-readable error message" }`
- **Access Control**: Only creates tasks for the authenticated user

### get_todos Tool
- **Tool Name**: `get_todos`
- **Description**: Retrieves tasks for the authenticated user with optional filtering
- **Parameters**:
  - `status`: string (optional) - Filter by status (all, completed, pending)
  - `limit`: number (optional) - Maximum number of tasks to return (default: 20)
  - `offset`: number (optional) - Number of tasks to skip (for pagination)
- **Authentication**: Requires valid user ID in context
- **Returns**:
  - Success: `{ "todos": [{"id": 1, "title": "...", "completed": false, ...}], "total": 15 }`
  - Error: `{ "error": "string", "message": "Human-readable error message" }`
- **Access Control**: Only returns tasks for the authenticated user

### update_todo_status Tool
- **Tool Name**: `update_todo_status`
- **Description**: Updates the completion status of a specific task
- **Parameters**:
  - `task_id`: number (required) - The ID of the task to update
  - `status`: boolean (required) - The new completion status (true for completed, false for pending)
  - `notes`: string (optional) - Additional notes about the update
- **Authentication**: Requires valid user ID in context
- **Returns**:
  - Success: `{ "id": 123, "status": "updated", "completed": true, "message": "Task status updated successfully" }`
  - Error: `{ "error": "string", "message": "Human-readable error message" }`
- **Access Control**: Only updates tasks owned by the authenticated user

## Chat API Endpoints

### Send Message
- **Endpoint**: `POST /api/chat`
- **Authentication**: Required JWT token in Authorization header
- **Description**: Sends a message to the AI agent and returns the response
- **Headers**:
  - `Authorization: Bearer {jwt_token}`
  - `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "message": "string (required) - The user's message",
    "conversation_id": "string (optional) - Session identifier for context",
    "user_id": "number (required) - User ID (will be extracted from JWT)",
    "timestamp": "string (optional) - ISO date string for message ordering"
  }
  ```
- **Response**:
  - Success (200): `{ "reply": "string - Agent's response", "conversation_id": "string - Session identifier", "actions_taken": ["object - Tool calls executed"] }`
  - Unauthorized (401): `{ "error": "Authentication required" }`
  - Forbidden (403): `{ "error": "Access forbidden" }`
  - Bad Request (400): `{ "error": "string - Validation error message" }`
  - Server Error (500): `{ "error": "string - Server error message" }`

### Get Conversation History
- **Endpoint**: `GET /api/chat/history`
- **Authentication**: Required JWT token in Authorization header
- **Description**: Retrieves the conversation history for the current user
- **Query Parameters**:
  - `conversation_id`: string (required) - The conversation to retrieve
  - `limit`: number (optional) - Maximum number of messages to return (default: 20)
  - `offset`: number (optional) - Number of messages to skip (for pagination)
- **Headers**: `Authorization: Bearer {jwt_token}`
- **Response**:
  - Success (200): `{ "messages": [{"role": "string", "content": "string", "timestamp": "string"}], "conversation_id": "string" }`
  - Unauthorized (401): `{ "error": "Authentication required" }`
  - Forbidden (403): `{ "error": "Access forbidden" }`

### Start New Conversation
- **Endpoint**: `POST /api/chat/new`
- **Authentication**: Required JWT token in Authorization header
- **Description**: Starts a new conversation session
- **Headers**: `Authorization: Bearer {jwt_token}`
- **Response**:
  - Success (200): `{ "conversation_id": "string - New session identifier", "message": "Conversation started successfully" }`
  - Unauthorized (401): `{ "error": "Authentication required" }`

## Agent Configuration

### OpenAI Assistant Setup
- **Model**: Configured to use appropriate GPT model (e.g., gpt-4-turbo)
- **Instructions**: Custom system instructions for todo management
- **Tools**: Binds the three MCP tools (add_todo, get_todos, update_todo_status)
- **File Search**: Disabled (no file attachment needed)
- **Temperature**: Configured for consistent, reliable responses

## Error Response Format
All error responses follow the format:
```json
{
  "error": "Human-readable error message",
  "error_code": "string - Machine-readable error code",
  "timestamp": "ISO datetime string"
}
```

## Validation Rules
- All user-specific data is filtered server-side to prevent unauthorized access
- All tool calls validate the user context before executing operations
- Conversation history is limited to authenticated user's data only
- All dates/times are returned in ISO 8601 format