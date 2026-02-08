# Phase I - In-Memory Console Todo App

This is the implementation of the Phase I todo application as specified in the project requirements. It provides a command-line interface for managing todo tasks with in-memory storage only.

## Features

- Add new tasks with titles and optional descriptions
- List all tasks with their ID and completion status
- Update existing tasks by ID
- Delete tasks by ID
- Toggle task completion status
- Error handling for invalid inputs and non-existent tasks

## Architecture

The application follows a clean architecture pattern:

- **Models**: `todo_model.py` - Defines the Todo entity
- **Repository**: `repository.py` - Handles in-memory data storage
- **Service**: `service.py` - Implements business logic
- **CLI**: `cli.py` - Handles user interaction
- **Main**: `main.py` - Application entry point

## Commands

- `ADD "title" ["description"]` - Create a new todo task
- `LIST` - Display all current tasks with their status
- `UPDATE id "title" ["description"]` - Update an existing task
- `DELETE id` - Remove a task by ID
- `COMPLETE id` - Toggle completion status of a task
- `HELP` - Show available commands
- `EXIT` - Quit the application

## Running the Application

```bash
python main.py
```

## Testing

Unit and integration tests are available in the parent `phase-1` directory:
- `test_basic.py` - Basic functionality tests
- `test_edge_cases.py` - Edge case tests
- `integration_test.py` - Complete workflow tests

Run tests from the `phase-1` directory:
```bash
python test_basic.py
python test_edge_cases.py
python integration_test.py
```

## Dependencies

- Python 3.13+
- Standard library only (no external dependencies)