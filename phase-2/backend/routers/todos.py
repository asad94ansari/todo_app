"""
Todos router for the todo application.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select, desc
from typing import List, Optional
from ..database.database import get_session
from ..models.todo import Todo, TodoCreate, TodoRead, TodoUpdate, TodoToggle
from ..models.user import User
from ..auth.auth import get_current_user

router = APIRouter()

@router.get("/todos", response_model=List[TodoRead], tags=["todos"])
def get_todos(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    completed: Optional[bool] = Query(None)
):
    """Get all todos for the current user."""
    query = select(Todo).where(Todo.user_id == current_user.id)

    if completed is not None:
        query = query.where(Todo.completed == completed)

    query = query.order_by(desc(Todo.created_at)).offset(offset).limit(limit)

    todos = session.exec(query).all()
    return todos

@router.post("/todos", response_model=TodoRead, status_code=status.HTTP_201_CREATED, tags=["todos"])
def create_todo(
    todo: TodoCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new todo for the current user."""
    db_todo = Todo.model_validate(todo.model_dump())
    db_todo.user_id = current_user.id
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

@router.get("/todos/{todo_id}", response_model=TodoRead, tags=["todos"])
def get_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific todo by ID."""
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this todo")
    return todo

@router.put("/todos/{todo_id}", response_model=TodoRead, tags=["todos"])
def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a specific todo by ID."""
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this todo")

    update_data = todo_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(todo, field, value)

    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@router.patch("/todos/{todo_id}/toggle", response_model=TodoRead, tags=["todos"])
def toggle_todo(
    todo_id: int,
    todo_toggle: TodoToggle,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Toggle the completion status of a todo."""
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this todo")

    todo.completed = todo_toggle.completed
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["todos"])
def delete_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a specific todo by ID."""
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this todo")

    session.delete(todo)
    session.commit()
    return