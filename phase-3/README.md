# Phase III - AI Chatbot Integration

This is the implementation of the Phase III AI Chatbot Integration as specified in the project requirements. It adds natural language task management to the existing todo application using OpenAI Agents and MCP protocol.

## Features

- AI-powered chat interface for natural language task management
- MCP server exposing task management tools to OpenAI agents
- Integration with existing Phase 2 database and authentication
- Responsive chat component in Next.js with lucide-react icons
- User isolation - AI agent respects user authentication and authorization

## Architecture

The application follows a modular architecture pattern:

- **MCP Server**: FastAPI-based server exposing tools via MCP protocol
- **Agent Service**: OpenAI agent service connecting natural language to MCP tools
- **Chat API**: Stateless endpoint for handling conversations
- **Frontend Integration**: Chat window component integrated into existing UI
- **Authentication**: User ID verification for all agent actions
- **Database**: Integration with existing Phase 2 SQLModel database

## Running the Application

### MCP Server Setup

1. Navigate to the MCP server directory:
```bash
cd phase-3/mcp-server
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables in a `.env` file:
```env
DATABASE_URL=postgresql://username:password@host:port/database
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
OPENAI_API_KEY=your-openai-api-key
```

5. Run the MCP server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

### Agent Service Setup

1. Navigate to the agent service directory:
```bash
cd phase-3/agent-service
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables in a `.env` file:
```env
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4-turbo
SECRET_KEY=your-super-secret-key
MCP_SERVER_URL=http://localhost:8080
```

5. Run the agent service:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### Frontend Integration

1. Navigate to the Phase 2 frontend directory:
```bash
cd phase-2/frontend
```

2. Copy the chat component to the appropriate location:
```bash
cp -r ../phase-3/frontend-updates/components/ChatWindow.tsx src/components/
cp -r ../phase-3/frontend-updates/services/chat-api.ts src/services/
```

3. Install required frontend dependencies:
```bash
npm install lucide-react
```

4. Update your dashboard or layout to include the chat functionality.

## API Endpoints

### MCP Server (Port 8080)
- Health check: `GET http://localhost:8080/health`
- Tool listing: `GET http://localhost:8080/mcp/tools`
- Tool execution: `POST http://localhost:8080/mcp/tool`

### Agent Service (Port 8001)
- Chat endpoint: `POST http://localhost:8081/api/chat`
- Chat history: `GET http://localhost:8081/api/chat/history`
- New conversation: `POST http://localhost:8081/api/chat/new`
- Health check: `GET http://localhost:8081/health`

## MCP Tools

### add_todo
- Creates a new task for the authenticated user
- Parameters: title (required), description (optional), due_date (optional), priority (optional)

### get_todos
- Retrieves tasks for the authenticated user with optional filtering
- Parameters: status (optional), limit (optional), offset (optional)

### update_todo_status
- Updates the completion status of a specific task
- Parameters: task_id (required), status (required), notes (optional)

## Security Features

- All agent actions validated against user's authentication context
- Input sanitization for natural language processing
- Proper token handling and validation
- User isolation - users can only access their own data via chat

## Technologies Used

### Backend
- FastAPI - Modern, fast web framework for Python
- OpenAI API - For natural language processing and agent capabilities
- SQLModel - SQL databases with Python objects
- Pydantic - Data validation and settings management
- PostgreSQL - Relational database (via Phase 2 integration)

### Frontend
- Next.js 15 - React framework
- TypeScript - Type-safe JavaScript
- Tailwind CSS - Utility-first CSS framework
- Lucide - Beautiful icon library
- React - User interface library