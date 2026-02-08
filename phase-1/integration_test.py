"""
Final integration test with complete user workflow for the todo application.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'implementation'))

from implementation.cli import TodoCLI
from implementation.service import TodoService


def test_full_workflow():
    """Test the complete user workflow for the todo application."""
    service = TodoService()

    # Scenario 1: Add multiple tasks (from spec acceptance criteria)
    task1 = service.add_task("Buy groceries", "Milk, eggs, bread")
    task2 = service.add_task("Walk the dog")
    task3 = service.add_task("Finish report", "Submit by Friday")

    # Verify multiple tasks can be added in one session
    tasks = service.list_tasks()
    assert len(tasks) == 3

    # Scenario 2: List all tasks (from spec acceptance criteria)
    tasks = service.list_tasks()
    assert len(tasks) == 3
    # Verify all currently stored tasks are displayed with accurate information
    titles = {t.title for t in tasks}
    assert "Buy groceries" in titles
    assert "Walk the dog" in titles
    assert "Finish report" in titles

    # Scenario 3: Update and delete any existing task by ID (from spec acceptance criteria)
    # Update a task
    success = service.update_task(task2.id, "Walk the cat", "Play with the cat")
    assert success is True

    # Verify the update
    tasks = service.list_tasks()
    updated_task = next(t for t in tasks if t.id == task2.id)
    assert updated_task.title == "Walk the cat"
    assert updated_task.description == "Play with the cat"

    # Delete a task
    success = service.delete_task(task3.id)
    assert success is True

    # Verify deletion
    tasks = service.list_tasks()
    assert len(tasks) == 2
    titles = {t.title for t in tasks}
    assert "Finish report" not in titles  # Should be gone
    assert "Buy groceries" in titles     # Should still exist
    assert "Walk the cat" in titles      # Should still exist (was updated)

    # Scenario 4: Task completion status correctly toggled (from spec acceptance criteria)
    # Initially incomplete
    for task in service.list_tasks():
        assert not task.completed

    # Toggle completion
    success = service.complete_task(task1.id)
    assert success is True

    # Verify completion status
    tasks = service.list_tasks()
    task1_after_toggle = next(t for t in tasks if t.id == task1.id)
    assert task1_after_toggle.completed is True

    # Toggle back to incomplete
    success = service.complete_task(task1.id)
    assert success is True

    # Verify it's now incomplete
    tasks = service.list_tasks()
    task1_after_toggle = next(t for t in tasks if t.id == task1.id)
    assert task1_after_toggle.completed is False

    print("All integration tests passed!")
    print(f"- Added {len(service.list_tasks())} tasks in session")
    print(f"- Verified all {len(service.list_tasks())} tasks display accurately")
    print("- Successfully updated and deleted tasks by ID")
    print("- Task completion status correctly toggled")


def test_application_interface_contract():
    """Test that the application follows the interface contract."""
    service = TodoService()

    # Test sequential ID assignment starting from 1
    task1 = service.add_task("First task")
    task2 = service.add_task("Second task")
    assert task1.id == 1
    assert task2.id == 2

    # Test completion status toggling works properly
    assert not task1.completed  # Initially incomplete

    service.complete_task(task1.id)
    tasks = service.list_tasks()
    updated_task1 = next(t for t in tasks if t.id == task1.id)
    assert updated_task1.completed  # Now complete

    service.complete_task(task1.id)
    tasks = service.list_tasks()
    updated_task1 = next(t for t in tasks if t.id == task1.id)
    assert not updated_task1.completed  # Now incomplete again

    print("Interface contract tests passed!")


if __name__ == "__main__":
    test_full_workflow()
    test_application_interface_contract()
    print("\nAll acceptance criteria satisfied!")