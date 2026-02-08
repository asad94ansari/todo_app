# Phase II - Full-Stack Todo Web Application

This is the implementation of the Phase II todo application as specified in the project requirements. It provides a full-stack web application with a Next.js frontend and FastAPI backend, implementing JWT-based authentication and persistent storage.

## Features

- User registration and authentication with JWT tokens
- Secure todo management with user isolation
- Full CRUD operations for todos (Create, Read, Update, Delete)
- Real-time task completion toggling
- Responsive UI with Tailwind CSS
- Secure session management
- User data isolation (User A cannot see User B's data)

## Architecture

The application follows a clean architecture pattern:

- **Backend**: FastAPI with SQLModel ORM
- **Database**: PostgreSQL (configured for Neon Serverless)
- **Authentication**: JWT-based authentication with secure password hashing
- **Frontend**: Next.js 14 with TypeScript and Tailwind CSS
- **UI Components**: Reusable components with Lucide icons
- **API Communication**: Fetch API with proper error handling

## Running the Application

### Backend Setup

1. Navigate to the backend directory:
```bash
cd phase-2/backend
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

4. Set up environment variables by copying the .env file and updating values:
```bash
cp .env.example .env
# Edit .env with your database configuration and secret keys
```

5. Run the backend server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000` with interactive API documentation at `http://localhost:8000/docs`.

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd phase-2/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables by creating a .env.local file:
```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

4. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`.

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Todos
- `GET /api/todos` - Get all user's todos
- `POST /api/todos` - Create a new todo
- `GET /api/todos/{id}` - Get a specific todo
- `PUT /api/todos/{id}` - Update a specific todo
- `PATCH /api/todos/{id}/toggle` - Toggle completion status
- `DELETE /api/todos/{id}` - Delete a specific todo

### Health Check
- `GET /health` - Health check endpoint

## Security Features

- Passwords are securely hashed using bcrypt
- JWT tokens for session management
- User isolation - users can only access their own todos
- Input validation and sanitization
- Protected routes with authentication middleware
- CORS configured for secure frontend-backend communication

## Technologies Used

### Backend
- FastAPI - Modern, fast web framework for Python
- SQLModel - SQL databases with Python objects
- Pydantic - Data validation and settings management
- PostgreSQL - Relational database
- JWT - Secure token-based authentication
- Bcrypt - Password hashing

### Frontend
- Next.js 14 - React framework
- TypeScript - Type-safe JavaScript
- Tailwind CSS - Utility-first CSS framework
- Lucide - Beautiful icon library
- Axios - HTTP client for API requests
- Zod - Schema validation