# API Contracts: Phase II — Full-Stack Todo Web Application

**Feature**: Phase II — Full-Stack Todo Web Application
**Contract Version**: 1.0
**Created**: 2026-02-06

## Purpose
Defines the API contracts for the FastAPI backend service that will be consumed by the Next.js frontend application.

## Base Configuration
- Base URL: `http://localhost:8000` (development) or production equivalent
- Content-Type: `application/json`
- Authentication: JWT token in Authorization header `Bearer {token}`
- All responses include appropriate HTTP status codes

## Authentication Endpoints (Handled by Better Auth)
- `/api/auth/register` - User registration (POST)
- `/api/auth/login` - User login (POST)
- `/api/auth/logout` - User logout (POST)

## Public Endpoints

### Health Check
- **Endpoint**: `GET /health`
- **Authentication**: None required
- **Description**: Returns the health status of the application
- **Response**:
  - Success (200): `{ "status": "healthy", "timestamp": "2026-02-06T10:00:00Z" }`
  - Error (500): `{ "error": "Service unavailable" }`

## Protected Endpoints (JWT Authentication Required)

### Todo Management

#### Get All User Todos
- **Endpoint**: `GET /api/todos`
- **Authentication**: Required
- **Description**: Retrieve all todos for the authenticated user
- **Query Parameters**:
  - `limit` (optional): Number of records to return (default: 50, max: 100)
  - `offset` (optional): Number of records to skip (default: 0)
  - `completed` (optional): Filter by completion status (true/false/all)
- **Headers**: `Authorization: Bearer {jwt_token}`
- **Response**:
  - Success (200): `{ "todos": [{...todo_object}], "total": 5 }`
  - Unauthorized (401): `{ "detail": "Not authenticated" }`
  - Forbidden (403): `{ "detail": "Access denied" }`

#### Create New Todo
- **Endpoint**: `POST /api/todos`
- **Authentication**: Required
- **Description**: Create a new todo for the authenticated user
- **Headers**: `Authorization: Bearer {jwt_token}`
- **Request Body**:
  ```json
  {
    "title": "string (required, max 255 chars)",
    "description": "string (optional)",
    "completed": "boolean (optional, default: false)"
  }
  ```
- **Response**:
  - Success (201): `{ "id": 1, "title": "...", "description": "...", "completed": false, "user_id": 1, "created_at": "...", "updated_at": "..." }`
  - Bad Request (400): `{ "detail": "Validation error", "errors": [...] }`
  - Unauthorized (401): `{ "detail": "Not authenticated" }`
  - Forbidden (403): `{ "detail": "Access denied" }`

#### Get Specific Todo
- **Endpoint**: `GET /api/todos/{todo_id}`
- **Authentication**: Required
- **Description**: Retrieve a specific todo by ID
- **Path Parameter**: `todo_id` - The ID of the todo to retrieve
- **Headers**: `Authorization: Bearer {jwt_token}`
- **Response**:
  - Success (200): `{ "id": 1, "title": "...", ... }`
  - Not Found (404): `{ "detail": "Todo not found" }`
  - Unauthorized (401): `{ "detail": "Not authenticated" }`
  - Forbidden (403): `{ "detail": "Access denied" }`

#### Update Todo
- **Endpoint**: `PUT /api/todos/{todo_id}`
- **Authentication**: Required
- **Description**: Update an existing todo for the authenticated user
- **Path Parameter**: `todo_id` - The ID of the todo to update
- **Headers**: `Authorization: Bearer {jwt_token}`
- **Request Body** (all fields optional):
  ```json
  {
    "title": "string (optional)",
    "description": "string (optional)",
    "completed": "boolean (optional)"
  }
  ```
- **Response**:
  - Success (200): `{ "id": 1, "title": "...", ... }`
  - Bad Request (400): `{ "detail": "Validation error", "errors": [...] }`
  - Not Found (404): `{ "detail": "Todo not found" }`
  - Unauthorized (401): `{ "detail": "Not authenticated" }`
  - Forbidden (403): `{ "detail": "Access denied" }`

#### Toggle Todo Completion
- **Endpoint**: `PATCH /api/todos/{todo_id}/toggle`
- **Authentication**: Required
- **Description**: Toggle the completion status of a todo
- **Path Parameter**: `todo_id` - The ID of the todo to update
- **Headers**: `Authorization: Bearer {jwt_token}`
- **Response**:
  - Success (200): `{ "id": 1, "completed": true, "updated_at": "..." }`
  - Not Found (404): `{ "detail": "Todo not found" }`
  - Unauthorized (401): `{ "detail": "Not authenticated" }`
  - Forbidden (403): `{ "detail": "Access denied" }`

#### Delete Todo
- **Endpoint**: `DELETE /api/todos/{todo_id}`
- **Authentication**: Required
- **Description**: Delete a specific todo by ID
- **Path Parameter**: `todo_id` - The ID of the todo to delete
- **Headers**: `Authorization: Bearer {jwt_token}`
- **Response**:
  - Success (204): No content returned
  - Not Found (404): `{ "detail": "Todo not found" }`
  - Unauthorized (401): `{ "detail": "Not authenticated" }`
  - Forbidden (403): `{ "detail": "Access denied" }`

## Error Response Format
All error responses follow the format:
```json
{
  "detail": "Human-readable error message",
  "status_code": 400
}
```

## Validation Rules
- All string inputs trimmed of leading/trailing whitespace
- Title must be 1-255 characters when provided
- All date/time values returned in ISO 8601 format
- User-specific data is filtered server-side to prevent unauthorized access