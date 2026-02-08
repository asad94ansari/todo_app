"""
Database initialization and migration logic for the todo application.
"""
from .database import engine
from ..models.user import User
from ..models.todo import Todo
from sqlmodel import SQLModel


def create_db_and_tables():
    """
    Create database tables if they don't exist.
    This function creates all tables defined in the models.
    """
    SQLModel.metadata.create_all(bind=engine)
    print("Database tables created successfully.")


if __name__ == "__main__":
    create_db_and_tables()