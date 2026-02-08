"""
add_todo tool implementation for the MCP server.
Creates a new task for the authenticated user.
"""
from sqlmodel import Session, select
from typing import Optional
from datetime import datetime
import asyncio

from ..database.connection import engine
from phase_2.backend.models.user import User
from phase_2.backend.models.todo import Todo


async def add_todo(
    user_id: int,
    title: str,
    description: Optional[str] = None,
    due_date: Optional[str] = None,
    priority: Optional[str] = None
) -> dict:
    """
    Create a new task for the authenticated user.

    Args:
        user_id: The ID of the user making the request
        title: The title of the new task
        description: Optional description for the task
        due_date: Optional due date for the task
        priority: Optional priority level (low, medium, high)

    Returns:
        A dictionary with the created task information
    """
    # Validate input
    if not title or not title.strip():
        raise ValueError("Title is required and cannot be empty")

    # Connect to the database
    with Session(engine) as session:
        # Verify the user exists
        user = session.get(User, user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} does not exist")

        # Create a new todo item
        new_todo = Todo(
            title=title.strip(),
            description=description,
            completed=False,  # New tasks are not completed by default
            user_id=user_id
        )

        # Add to the database
        session.add(new_todo)
        session.commit()
        session.refresh(new_todo)  # Refresh to get the ID

        return {
            "id": new_todo.id,
            "title": new_todo.title,
            "description": new_todo.description,
            "completed": new_todo.completed,
            "user_id": new_todo.user_id,
            "created_at": new_todo.created_at.isoformat() if new_todo.created_at else None,
            "updated_at": new_todo.updated_at.isoformat() if new_todo.updated_at else None,
            "status": "created",
            "message": f"Task '{new_todo.title}' created successfully"
        }