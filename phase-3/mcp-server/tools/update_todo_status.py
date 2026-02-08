"""
update_todo_status tool implementation for the MCP server.
Updates the completion status of a specific task.
"""
from sqlmodel import Session, select
from typing import Optional
from datetime import datetime
import asyncio

from ..database.connection import engine
from phase_2.backend.models.user import User
from phase_2.backend.models.todo import Todo


async def update_todo_status(
    user_id: int,
    task_id: int,
    status: bool,
    notes: Optional[str] = None
) -> dict:
    """
    Update the completion status of a specific task.

    Args:
        user_id: The ID of the user making the request
        task_id: The ID of the task to update
        status: The new completion status (True for completed, False for pending)
        notes: Optional notes about the update

    Returns:
        A dictionary with the updated task information
    """
    # Connect to the database
    with Session(engine) as session:
        # Verify the user exists
        user = session.get(User, user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} does not exist")

        # Find the specific task belonging to the user
        query = select(Todo).where(Todo.id == task_id, Todo.user_id == user_id)
        todo = session.exec(query).first()

        if not todo:
            raise ValueError(f"Task with ID {task_id} not found for user {user_id}")

        # Update the completion status
        todo.completed = status
        # In a real implementation, we might also update notes or other fields
        # For now, we'll just update the status

        # Commit the changes
        session.add(todo)
        session.commit()
        session.refresh(todo)

        return {
            "id": todo.id,
            "title": todo.title,
            "description": todo.description,
            "completed": todo.completed,
            "user_id": todo.user_id,
            "created_at": todo.created_at.isoformat() if todo.created_at else None,
            "updated_at": todo.updated_at.isoformat() if todo.updated_at else None,
            "status": "updated",
            "notes": notes,
            "message": f"Task '{todo.title}' status updated to {'completed' if status else 'pending'}"
        }