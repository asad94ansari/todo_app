# Todo Backend API

This is the backend API for the Todo application, built with FastAPI and SQLModel.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the application:
```bash
uvicorn main:app --reload
```

## API Documentation

API documentation is available at `http://localhost:8000/docs` when the application is running.

## Features

- JWT-based authentication
- Secure user registration and login
- Todo CRUD operations
- User data isolation
- Input validation with Pydantic