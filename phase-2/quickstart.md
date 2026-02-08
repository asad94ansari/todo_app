# Quickstart Guide: Phase II — Full-Stack Todo Web Application

**Feature**: Phase II — Full-Stack Todo Web Application
**Created**: 2026-02-06

## Overview
This guide explains how to set up and run the full-stack todo application with Next.js frontend and FastAPI backend.

## Prerequisites
- Node.js 18+ for Next.js frontend
- Python 3.13+ for FastAPI backend
- PostgreSQL-compatible database (Neon Serverless)
- Environment variables configured

## Project Structure
```
phase-2/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── models/              # SQLModel database models
│   ├── schemas/             # Pydantic schemas
│   ├── routers/             # API route definitions
│   ├── database/            # Database configuration
│   └── auth/                # Better Auth integration
└── frontend/
    ├── pages/               # Next.js pages
    ├── components/          # Reusable UI components
    ├── services/            # API service layer
    ├── lib/                 # Utility functions
    ├── styles/              # Global styles
    └── public/              # Static assets
```

## Backend Setup (FastAPI)

### 1. Navigate to backend directory
```bash
cd phase-2/backend
```

### 2. Create virtual environment and install dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install fastapi uvicorn sqlmodel python-multipart better-auth psycopg2-binary python-dotenv
```

### 3. Set up environment variables
Create a `.env` file in the backend directory:
```env
DATABASE_URL="postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require"
SECRET_KEY="your-secret-key-here"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Run the backend server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

## Frontend Setup (Next.js)

### 1. Navigate to frontend directory
```bash
cd phase-2/frontend
```

### 2. Initialize Next.js project
```bash
npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
npm install axios zod @hookform/resolvers
```

### 3. Set up environment variables
Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_BASE_URL="http://localhost:8000"
NEXT_PUBLIC_BETTER_AUTH_URL="http://localhost:8000"
```

### 4. Run the frontend development server
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Running Both Servers

### Backend Commands:
```bash
cd phase-2/backend
source venv/bin/activate  # Activate virtual environment
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Commands:
```bash
cd phase-2/frontend
npm run dev
```

## API Endpoints Reference
- Health check: `GET http://localhost:8000/health`
- Todos: `GET/POST/PUT/DELETE http://localhost:8000/api/todos`
- Toggle completion: `PATCH http://localhost:8000/api/todos/{id}/toggle`

## Environment Variables Required

### Backend (.env):
- `DATABASE_URL`: Neon PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

### Frontend (.env.local):
- `NEXT_PUBLIC_API_BASE_URL`: Backend API base URL
- `NEXT_PUBLIC_BETTER_AUTH_URL`: Authentication service URL

## Authentication Flow
1. User registers/login via Better Auth forms
2. JWT token is obtained and stored
3. Token is included in headers for protected API calls
4. Logout clears the stored token

## CORS Configuration
The backend is configured to allow requests from the frontend origin during development.