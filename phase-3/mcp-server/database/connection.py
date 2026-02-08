"""
Database connection module for the MCP server.
This connects to the Phase 2 SQLModel database.
"""
from sqlmodel import create_engine, Session
from typing import Generator
import os

# Use the same database URL as Phase 2
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

def get_db_session() -> Generator[Session, None, None]:
    """
    Dependency to get database session.
    This connects to the Phase 2 database to access user and todo data.
    """
    with Session(engine) as session:
        yield session