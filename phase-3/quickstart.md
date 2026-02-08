# Quickstart Guide: Phase III — AI Chatbot Integration

**Feature**: Phase III — AI Chatbot Integration
**Created**: 2026-02-07

## Overview
This guide explains how to set up and run the AI chatbot integration for the todo application, enabling natural language task management.

## Prerequisites
- OpenAI API key
- Python 3.13+ for MCP server and agent service
- Node.js 18+ for frontend updates
- Existing Phase 2 database and authentication system
- MCP Python SDK
- Environment variables configured

## Project Structure
```
phase-3/
├── mcp-server/
│   ├── main.py              # MCP server entry point
│   ├── tools/               # Task management MCP tools
│   ├── database/            # Database connection for tools
│   └── auth/                # Authentication validation for tools
├── agent-service/
│   ├── main.py              # Agent service entry point
│   ├── agent.py             # OpenAI Agent configuration
│   ├── chat_endpoint.py     # Stateless chat API
│   └── utils/               # Helper functions
└── frontend-updates/
    ├── components/
    │   └── ChatWindow.tsx   # Chat interface component
    ├── pages/               # Any new pages for chat features
    └── services/
        └── chat-api.ts      # Chat API service layer
```

## MCP Server Setup

### 1. Navigate to MCP server directory
```bash
cd phase-3/mcp-server
```

### 2. Create virtual environment and install dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install fastapi uvicorn python-mcp-sdk openai python-jwt sqlmodel psycopg2-binary python-dotenv
```

### 3. Set up environment variables
Create a `.env` file in the MCP server directory:
```env
OPENAI_API_KEY="your-openai-api-key-here"
DATABASE_URL="postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require"
SECRET_KEY="your-jwt-secret-key"
MCP_SERVER_PORT=8080
```

### 4. Run the MCP server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

The MCP server will be available at `http://localhost:8080` and will expose the task management tools.

## Agent Service Setup

### 1. Navigate to agent service directory
```bash
cd phase-3/agent-service
```

### 2. Install dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install fastapi uvicorn openai python-jwt python-dotenv
```

### 3. Set up environment variables
Create a `.env` file in the agent service directory:
```env
OPENAI_API_KEY="your-openai-api-key-here"
MCP_SERVER_URL="http://localhost:8080"
SECRET_KEY="your-jwt-secret-key"
AGENT_SERVICE_PORT=8001
```

### 4. Run the agent service
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

The agent service will be available at `http://localhost:8001` with the chat endpoint at `POST /api/chat`.

## Frontend Integration

### 1. Navigate to frontend updates directory
```bash
cd phase-3/frontend-updates
```

### 2. Update the Next.js application with chat functionality
The chat window component is integrated into the existing Phase 2 application at `components/ChatWindow.tsx`.

### 3. Install required frontend dependencies
```bash
npm install lucide-react react-markdown
```

### 4. Set up environment variables
Update your existing `.env.local` file with:
```env
NEXT_PUBLIC_CHAT_API_URL="http://localhost:8001"
```

### 5. Update the existing frontend application
Integrate the chat component into your dashboard layout, ensuring it shares authentication context with the existing application.

## Running the Complete System

### 1. MCP Server:
```bash
cd phase-3/mcp-server
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

### 2. Agent Service:
```bash
cd phase-3/agent-service
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### 3. Update Frontend (in Phase 2 directory):
```bash
cd ../phase-2/frontend  # or wherever your main frontend is
npm run dev
```

## Chat API Endpoint
- Chat endpoint: `POST http://localhost:8001/api/chat`
- Requires valid JWT token in Authorization header
- Expects JSON: `{ "message": "user message", "conversation_id": "optional session id" }`
- Returns: `{ "reply": "agent response", "conversation_id": "session id" }`

## Authentication Flow
1. User authenticates via existing Phase 2 system
2. JWT token is passed to chat API requests
3. Agent validates user context before executing any tools
4. Tools verify user owns any task they're attempting to modify