"""
Application service layer for the todo application.
"""
from typing import List, Optional
try:
    from implementation.repository import TodoRepository
    from implementation.todo_model import Todo
except ImportError:
    from repository import TodoRepository
    from todo_model import Todo


class TodoService:
    """
    Encapsulates business logic for todo operations.

    The service layer provides a clean interface for todo operations
    while handling validation and error cases.
    """

    def __init__(self):
        """Initialize the service with a repository instance."""
        self.repository = TodoRepository()

    def add_task(self, title: str, description: Optional[str] = None) -> Todo:
        """
        Add a new task to the todo list.

        Args:
            title: The title of the task (required)
            description: Optional description of the task

        Returns:
            The created Todo object

        Raises:
            ValueError: If title is empty or contains only whitespace
        """
        return self.repository.add_todo(title, description)

    def list_tasks(self) -> List[Todo]:
        """
        List all tasks in the todo list.

        Returns:
            A list of all Todo objects
        """
        return self.repository.list_todos()

    def update_task(self, task_id: int, title: Optional[str] = None,
                    description: Optional[str] = None) -> bool:
        """
        Update an existing task.

        Args:
            task_id: The ID of the task to update
            title: New title for the task (optional)
            description: New description for the task (optional)

        Returns:
            True if the update was successful, False if task doesn't exist

        Raises:
            ValueError: If title is empty or contains only whitespace
        """
        result = self.repository.update_todo(task_id, title, description)
        return result is not None

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the deletion was successful, False if task doesn't exist
        """
        return self.repository.delete_todo(task_id)

    def complete_task(self, task_id: int) -> bool:
        """
        Toggle the completion status of a task.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            True if the toggle was successful, False if task doesn't exist
        """
        result = self.repository.toggle_completion(task_id)
        return result is not None

    def task_exists(self, task_id: int) -> bool:
        """
        Check if a task exists.

        Args:
            task_id: The ID of the task to check

        Returns:
            True if the task exists, False otherwise
        """
        return self.repository.exists(task_id)