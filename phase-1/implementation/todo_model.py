"""
Todo data model for the in-memory console todo application.
"""
from typing import Optional
from dataclasses import dataclass


@dataclass
class Todo:
    """
    Represents a single todo task in the application.

    Attributes:
        id: Unique identifier for the task
        title: Main description of the task (required)
        description: Additional details about the task (optional)
        completed: Tracks the completion status of the task
    """
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    def __post_init__(self):
        """Validate the Todo object after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty or whitespace only")

    def toggle_completion(self) -> 'Todo':
        """Toggle the completion status of the task."""
        self.completed = not self.completed
        return self

    def __str__(self) -> str:
        """String representation of the Todo object."""
        status = "x" if self.completed else " "
        return f"{self.id}. [{status}] {self.title}" + \
               (f" - {self.description}" if self.description else "")