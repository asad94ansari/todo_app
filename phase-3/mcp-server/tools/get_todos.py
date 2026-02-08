"""
get_todos tool implementation for the MCP server.
Retrieves tasks for the authenticated user with optional filtering.
"""
from sqlmodel import Session, select
from typing import Optional, List
from datetime import datetime
import asyncio

from ..database.connection import engine
from phase_2.backend.models.user import User
from phase_2.backend.models.todo import Todo


async def get_todos(
    user_id: int,
    status: Optional[str] = None,
    limit: Optional[int] = 20,
    offset: Optional[int] = 0
) -> dict:
    """
    Retrieve tasks for the authenticated user with optional filtering.

    Args:
        user_id: The ID of the user making the request
        status: Filter by status (all, completed, pending)
        limit: Maximum number of tasks to return (default: 20)
        offset: Number of tasks to skip (for pagination)

    Returns:
        A dictionary with the list of tasks and metadata
    """
    # Connect to the database
    with Session(engine) as session:
        # Verify the user exists
        user = session.get(User, user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} does not exist")

        # Build the query with filters
        query = select(Todo).where(Todo.user_id == user_id)

        # Apply status filter if specified
        if status:
            if status.lower() == "completed":
                query = query.where(Todo.completed == True)
            elif status.lower() == "pending":
                query = query.where(Todo.completed == False)
            # If status is "all" or any other value, don't apply filter

        # Apply pagination
        query = query.offset(offset).limit(limit)

        # Execute the query
        todos = session.exec(query).all()

        # Convert to dictionaries
        todos_data = []
        for todo in todos:
            todo_dict = {
                "id": todo.id,
                "title": todo.title,
                "description": todo.description,
                "completed": todo.completed,
                "user_id": todo.user_id,
                "created_at": todo.created_at.isoformat() if todo.created_at else None,
                "updated_at": todo.updated_at.isoformat() if todo.updated_at else None
            }
            todos_data.append(todo_dict)

        return {
            "todos": todos_data,
            "total": len(todos_data),
            "status_filter": status,
            "limit": limit,
            "offset": offset,
            "message": f"Retrieved {len(todos_data)} tasks for user {user_id}"
        }