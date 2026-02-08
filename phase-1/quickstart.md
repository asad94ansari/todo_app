# Quickstart Guide: Phase I — In-Memory Console Todo App

**Feature**: Phase I — In-Memory Python Console Todo App
**Created**: 2026-02-06

## Overview
This guide explains how to run and use the in-memory console todo application. The application provides a command-line interface for managing todo tasks without any persistent storage.

## Running the Application
1. Navigate to the implementation directory: `cd phase-1/implementation`
2. Execute the main application file: `python todo_app.py`
3. The application will start and display a command prompt

## Available Commands
- `ADD "title" ["description"]` - Creates a new todo task
- `LIST` - Displays all current tasks with their status
- `UPDATE id "title" ["description"]` - Updates an existing task
- `DELETE id` - Removes a task by ID
- `COMPLETE id` - Toggles completion status of a task
- `HELP` - Shows available commands
- `EXIT` - Quits the application

## Example Usage
```
> ADD "Buy groceries" "Milk, eggs, bread"
Added task #1: Buy groceries

> ADD "Walk the dog"
Added task #2: Walk the dog

> LIST
1. [ ] Buy groceries - Milk, eggs, bread
2. [ ] Walk the dog

> COMPLETE 1
Task #1 marked as complete

> LIST
1. [x] Buy groceries - Milk, eggs, bread
2. [ ] Walk the dog

> EXIT
```

## Expected Behavior
- All data exists only in memory and is lost when the application closes
- Task IDs are assigned sequentially starting from 1
- Invalid commands or IDs will show helpful error messages
- The application runs continuously until the EXIT command is entered

## Error Handling
- Invalid task IDs will result in error messages
- Empty titles will be rejected
- Malformed commands will show usage instructions