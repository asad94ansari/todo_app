# Application Interface Contract: Console Todo App

**Feature**: Phase I — In-Memory Python Console Todo App
**Contract Version**: 1.0
**Created**: 2026-02-06

## Purpose
Defines the interface contracts for the console todo application, specifying command formats, expected responses, and error handling patterns.

## Command Interface

### ADD Command
**Format**: `ADD "title" ["description"]`
**Parameters**:
- `title` (required): String containing the task title (quoted if contains spaces)
- `description` (optional): String containing additional task details

**Success Response**: `Added task #ID: title`
**Error Responses**:
- `"Error: Title cannot be empty"` - when title is missing or whitespace only
- `"Error: Invalid command format"` - when command is malformed

### LIST Command
**Format**: `LIST`
**Parameters**: None

**Success Response**: Formatted list of all tasks in the format:
```
ID. [status] title - description (if exists)
```
Where status is `[ ]` for incomplete and `[x]` for complete

### UPDATE Command
**Format**: `UPDATE id "title" ["description"]`
**Parameters**:
- `id` (required): Integer representing the task ID
- `title` (required): New title for the task
- `description` (optional): New description for the task

**Success Response**: `Task #ID updated successfully`
**Error Responses**:
- `"Error: Task with ID X does not exist"` - when ID is not found
- `"Error: Title cannot be empty"` - when title is invalid

### DELETE Command
**Format**: `DELETE id`
**Parameters**:
- `id` (required): Integer representing the task ID

**Success Response**: `Task #ID deleted successfully`
**Error Responses**:
- `"Error: Task with ID X does not exist"` - when ID is not found

### COMPLETE Command
**Format**: `COMPLETE id`
**Parameters**:
- `id` (required): Integer representing the task ID

**Success Response**: `Task #ID marked as [complete/incomplete]`
**Error Responses**:
- `"Error: Task with ID X does not exist"` - when ID is not found

### HELP Command
**Format**: `HELP`
**Parameters**: None

**Response**: List of available commands with brief descriptions

### EXIT Command
**Format**: `EXIT`
**Parameters**: None

**Response**: None (application terminates)

## Error Handling Standards

### Error Message Format
All error messages follow the format: `"Error: [descriptive message]"`

### Validation Checks
1. Command format validation
2. Task ID existence validation
3. Input data validation (e.g., non-empty titles)

## State Management
- All state exists in memory only
- No persistence between application runs
- State is managed through the internal Todo repository

## Input/Output Specifications
- Input: Plain text commands via stdin
- Output: Plain text responses via stdout
- Errors: Error messages via stderr