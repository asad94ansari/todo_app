# Data Model: Phase I — In-Memory Console Todo App

**Feature**: Phase I — In-Memory Python Console Todo App
**Created**: 2026-02-06

## Entity Definitions

### Todo Entity

**Description**: Represents a single todo task in the application

**Fields**:
- `id`: Integer (Primary Identifier)
  - Purpose: Unique identifier for the task
  - Constraints: Positive integer, sequential assignment starting from 1
  - Validation: Must be unique within the application session

- `title`: String (Required)
  - Purpose: The main description of the task
  - Constraints: Non-empty, non-whitespace only
  - Validation: Length > 0 after trimming whitespace

- `description`: String (Optional)
  - Purpose: Additional details about the task
  - Constraints: May be empty or null
  - Validation: No specific constraints beyond basic string validation

- `completed`: Boolean
  - Purpose: Tracks the completion status of the task
  - Constraints: True/False only
  - Validation: Strict boolean value

**State Transitions**:
- Default state: `completed = False`
- Toggle operation: Switches between True and False states
- No other state transitions defined

## Repository Structure

### In-Memory Storage Model
- **Storage Type**: Dictionary mapping `id` (int) to `Todo` objects
- **Access Pattern**: Direct lookup by ID in O(1) time
- **Iteration Pattern**: Dictionary values access for listing operations

### ID Generation Strategy
- **Starting Value**: 1 (first task gets ID 1)
- **Increment Pattern**: Sequential integer increment
- **Collision Prevention**: Increment counter after successful addition

## Validation Rules

### At Creation Time:
- `title` must be provided and not empty after whitespace trimming
- `id` is automatically assigned, cannot be provided by user
- `completed` defaults to `False`

### At Update Time:
- `id` cannot be changed
- `title` remains required (non-empty after whitespace trimming)
- `description` may be updated to any string value
- `completed` can be toggled or set explicitly

### At Deletion Time:
- Task must exist in storage
- Operation is irreversible
- ID counter does not decrease after deletion

## Relationships
- No relationships defined (standalone entities)
- All entities exist independently within the application context