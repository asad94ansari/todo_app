# Data Model: Phase II — Full-Stack Todo Web Application

**Feature**: Phase II — Full-Stack Todo Web Application
**Created**: 2026-02-06

## Entity Definitions

### User Entity

**Description**: Represents an authenticated user in the system

**Fields**:
- `id`: Integer/UUID (Primary Key)
  - Purpose: Unique identifier for the user
  - Constraints: Auto-generated, unique
  - Validation: Not nullable, follows UUID or auto-increment pattern

- `email`: String (Required)
  - Purpose: User's email address for login and identification
  - Constraints: Unique across all users, valid email format
  - Validation: Proper email format, uniqueness constraint at database level

- `password_hash`: String (Required)
  - Purpose: Securely stored hashed version of the user's password
  - Constraints: Minimum strength requirements (handled by auth system)
  - Validation: Never stored as plain text, always hashed

- `created_at`: DateTime (Required)
  - Purpose: Timestamp when the user account was created
  - Constraints: Auto-set on creation, immutable
  - Validation: System-generated, UTC timezone

- `updated_at`: DateTime (Required)
  - Purpose: Timestamp when the user account was last updated
  - Constraints: Auto-updated on changes
  - Validation: System-managed, UTC timezone

### Todo Entity

**Description**: Represents a todo item linked to a specific user

**Fields**:
- `id`: Integer/UUID (Primary Key)
  - Purpose: Unique identifier for the todo
  - Constraints: Auto-generated, unique
  - Validation: Not nullable, follows UUID or auto-increment pattern

- `title`: String (Required)
  - Purpose: The main description of the task
  - Constraints: Non-empty, maximum length reasonable (e.g., 255 characters)
  - Validation: Length > 0 after trimming whitespace

- `description`: String (Optional)
  - Purpose: Additional details about the task
  - Constraints: May be empty or null, maximum length reasonable
  - Validation: No specific constraints beyond basic string validation

- `completed`: Boolean
  - Purpose: Tracks the completion status of the task
  - Constraints: True/False only
  - Validation: Strict boolean value, defaults to False

- `user_id`: Integer/UUID (Foreign Key)
  - Purpose: Links the todo to its owner user
  - Constraints: Must reference an existing user
  - Validation: Foreign key constraint, not nullable

- `created_at`: DateTime (Required)
  - Purpose: Timestamp when the todo was created
  - Constraints: Auto-set on creation, immutable
  - Validation: System-generated, UTC timezone

- `updated_at`: DateTime (Required)
  - Purpose: Timestamp when the todo was last updated
  - Constraints: Auto-updated on changes
  - Validation: System-managed, UTC timezone

## Relationships

### User to Todo
- **Relationship Type**: One-to-Many (One user can have many todos)
- **Cardinality**: 1 User → 0..* Todos
- **Constraint**: Foreign key from Todo.user_id to User.id
- **Cascade Behavior**: When user is deleted, associated todos should also be deleted (CASCADE DELETE)

## Indexes

### On User Table:
- Primary Key: id
- Unique Index: email (for fast lookups during authentication)

### On Todo Table:
- Primary Key: id
- Foreign Key Index: user_id (for efficient user todo queries)
- Index: (user_id, created_at) - for efficient queries of user's todos sorted by date

## Validation Rules

### At Creation Time:
- User email must be valid and unique
- Todo title must be provided and not empty after whitespace trimming
- Todo must be associated with a valid user
- All datetime fields are auto-populated

### At Update Time:
- User email uniqueness maintained
- Todo title remains required (non-empty after whitespace trimming)
- Only the owning user can modify their todos
- Completed status can be toggled freely by the owner

### Access Control:
- Users can only access/modify their own todos
- Authentication required for all todo operations
- Admin users (if implemented) follow the same access patterns

## Database Schema

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Todos table
CREATE TABLE todos (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_todos_user_id ON todos(user_id);
CREATE INDEX idx_todos_user_created ON todos(user_id, created_at);
```