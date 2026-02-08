"""
Edge case tests for the todo application.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'implementation'))

from implementation.service import TodoService


def test_edge_cases():
    """Test edge cases for the todo service."""
    service = TodoService()

    # Test adding a task with empty title (should fail)
    try:
        service.add_task("")
        assert False, "Expected ValueError for empty title"
    except ValueError:
        pass  # Expected

    # Test adding a task with whitespace-only title (should fail)
    try:
        service.add_task("   ")
        assert False, "Expected ValueError for whitespace-only title"
    except ValueError:
        pass  # Expected

    # Test updating a non-existent task (should return False)
    result = service.update_task(999, "New title")
    assert result is False

    # Test updating with empty title (should fail)
    task = service.add_task("Valid task")
    try:
        service.update_task(task.id, "")
        assert False, "Expected ValueError for empty title update"
    except ValueError:
        pass  # Expected

    # Test deleting a non-existent task (should return False)
    result = service.delete_task(999)
    assert result is False

    # Test completing a non-existent task (should return False)
    result = service.complete_task(999)
    assert result is False

    # Test adding task with description but no title (should fail)
    try:
        service.add_task("", "This is a description without a title")
        assert False, "Expected ValueError for empty title"
    except ValueError:
        pass  # Expected

    # Test adding task with valid title and description
    task = service.add_task("Valid title", "Valid description")
    assert task.title == "Valid title"
    assert task.description == "Valid description"

    # Test updating only description (keeping title)
    result = service.update_task(task.id, description="Updated description")
    assert result is True
    updated_tasks = service.list_tasks()
    updated_task = next(t for t in updated_tasks if t.id == task.id)
    assert updated_task.description == "Updated description"
    assert updated_task.title == "Valid title"  # Title should remain unchanged

    # Test updating only title (keeping description)
    result = service.update_task(task.id, title="Updated title")
    assert result is True
    updated_tasks = service.list_tasks()
    updated_task = next(t for t in updated_tasks if t.id == task.id)
    assert updated_task.title == "Updated title"
    assert updated_task.description == "Updated description"  # Description should remain unchanged

    print("All edge case tests passed!")


if __name__ == "__main__":
    test_edge_cases()