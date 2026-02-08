"""
Smoke test for the todo application.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from service import TodoService


def test_basic_functionality():
    """Test basic functionality of the todo service."""
    service = TodoService()

    # Test adding tasks
    task1 = service.add_task("Buy groceries", "Milk, eggs, bread")
    assert task1.id == 1
    assert task1.title == "Buy groceries"
    assert task1.description == "Milk, eggs, bread"
    assert not task1.completed

    task2 = service.add_task("Walk the dog")
    assert task2.id == 2
    assert task2.title == "Walk the dog"
    assert task2.description is None
    assert not task2.completed

    # Test listing tasks
    tasks = service.list_tasks()
    assert len(tasks) == 2
    assert tasks[0].id == 1
    assert tasks[1].id == 2

    # Test completing a task
    success = service.complete_task(1)
    assert success
    tasks = service.list_tasks()
    completed_task = next(t for t in tasks if t.id == 1)
    assert completed_task.completed

    # Test toggling completion status back
    success = service.complete_task(1)
    assert success
    tasks = service.list_tasks()
    incomplete_task = next(t for t in tasks if t.id == 1)
    assert not incomplete_task.completed

    # Test updating a task
    success = service.update_task(2, "Walk the cat", "Play with the cat")
    assert success
    tasks = service.list_tasks()
    updated_task = next(t for t in tasks if t.id == 2)
    assert updated_task.title == "Walk the cat"
    assert updated_task.description == "Play with the cat"

    # Test deleting a task
    success = service.delete_task(1)
    assert success
    tasks = service.list_tasks()
    assert len(tasks) == 1
    remaining_task = tasks[0]
    assert remaining_task.id == 2

    print("All smoke tests passed!")


if __name__ == "__main__":
    test_basic_functionality()