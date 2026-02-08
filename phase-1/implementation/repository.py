"""
In-memory task repository for the todo application.
"""
from typing import Dict, List, Optional
try:
    from implementation.todo_model import Todo
except ImportError:
    from todo_model import Todo


class TodoRepository:
    """
    Manages in-memory storage of todo items using a dictionary.

    The repository handles all data operations including adding, retrieving,
    updating, deleting, and listing todos.
    """

    def __init__(self):
        """Initialize the repository with an empty storage and ID counter."""
        self._storage: Dict[int, Todo] = {}
        self._next_id = 1

    def add_todo(self, title: str, description: Optional[str] = None) -> Todo:
        """
        Add a new todo to the repository.

        Args:
            title: The title of the todo
            description: Optional description of the todo

        Returns:
            The created Todo object with assigned ID
        """
        todo = Todo(id=self._next_id, title=title, description=description, completed=False)
        self._storage[self._next_id] = todo
        self._next_id += 1
        return todo

    def get_todo(self, todo_id: int) -> Optional[Todo]:
        """
        Retrieve a todo by its ID.

        Args:
            todo_id: The ID of the todo to retrieve

        Returns:
            The Todo object if found, None otherwise
        """
        return self._storage.get(todo_id)

    def list_todos(self) -> List[Todo]:
        """
        Get all todos in the repository.

        Returns:
            A list of all Todo objects
        """
        return list(self._storage.values())

    def update_todo(self, todo_id: int, title: Optional[str] = None,
                    description: Optional[str] = None) -> Optional[Todo]:
        """
        Update an existing todo's title and/or description.

        Args:
            todo_id: The ID of the todo to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            The updated Todo object if successful, None if todo doesn't exist
        """
        if todo_id not in self._storage:
            return None

        todo = self._storage[todo_id]

        if title is not None:
            # Validate that title is not empty after stripping whitespace
            if not title or not title.strip():
                raise ValueError("Title cannot be empty or whitespace only")
            todo.title = title

        if description is not None:
            todo.description = description

        return todo

    def delete_todo(self, todo_id: int) -> bool:
        """
        Delete a todo by its ID.

        Args:
            todo_id: The ID of the todo to delete

        Returns:
            True if the todo was deleted, False if it didn't exist
        """
        if todo_id not in self._storage:
            return False

        del self._storage[todo_id]
        return True

    def toggle_completion(self, todo_id: int) -> Optional[Todo]:
        """
        Toggle the completion status of a todo.

        Args:
            todo_id: The ID of the todo to toggle

        Returns:
            The updated Todo object if successful, None if todo doesn't exist
        """
        if todo_id not in self._storage:
            return None

        todo = self._storage[todo_id]
        todo.toggle_completion()
        return todo

    def exists(self, todo_id: int) -> bool:
        """
        Check if a todo with the given ID exists.

        Args:
            todo_id: The ID to check

        Returns:
            True if the todo exists, False otherwise
        """
        return todo_id in self._storage