# Data Model: Phase III — AI Chatbot Integration

**Feature**: Phase III — AI Chatbot Integration
**Created**: 2026-02-07

## Entity Definitions

### ChatMessage Entity

**Description**: Represents a single exchange in the conversation between user and AI agent

**Fields**:
- `id`: Integer/UUID (Primary Key)
  - Purpose: Unique identifier for the message
  - Constraints: Auto-generated, unique
  - Validation: Not nullable, follows UUID or auto-increment pattern

- `role`: String (Required)
  - Purpose: Specifies the sender of the message (user or assistant)
  - Constraints: Must be either "user" or "assistant"
  - Validation: Enum validation to ensure valid values

- `content`: String (Required)
  - Purpose: The actual text content of the message
  - Constraints: Non-empty, maximum reasonable length
  - Validation: Length > 0 after trimming whitespace

- `conversation_id`: String (Required)
  - Purpose: Links the message to its conversation thread
  - Constraints: Identifies the conversation session
  - Validation: Not nullable, reasonable length limit

- `timestamp`: DateTime (Required)
  - Purpose: When the message was created
  - Constraints: Auto-set on creation
  - Validation: System-generated, UTC timezone

- `user_id`: Integer/UUID (Required)
  - Purpose: Links the message to the authenticated user
  - Constraints: Must reference an existing user
  - Validation: Foreign key constraint to users table

### Conversation Context

**Description**: Represents a logical conversation thread with contextual state

**Fields**:
- `id`: String (Primary Key)
  - Purpose: Unique identifier for the conversation
  - Constraints: Session identifier for grouping messages
  - Validation: Unique identifier for the conversation thread

- `user_id`: Integer/UUID (Required)
  - Purpose: Links the conversation to the authenticated user
  - Constraints: Must reference an existing user
  - Validation: Foreign key constraint to users table

- `created_at`: DateTime (Required)
  - Purpose: When the conversation started
  - Constraints: Auto-set on creation
  - Validation: System-generated, UTC timezone

- `last_active`: DateTime (Required)
  - Purpose: When the conversation was last used
  - Constraints: Auto-updated on activity
  - Validation: System-managed, UTC timezone

- `expires_at`: DateTime (Optional)
  - Purpose: When the conversation context expires
  - Constraints: Sets TTL for context
  - Validation: If present, must be after created_at

### Tool Response Mapping

**Description**: Links agent actions to their database operation results

**Fields**:
- `id`: Integer/UUID (Primary Key)
  - Purpose: Unique identifier for the tool response record
  - Constraints: Auto-generated, unique
  - Validation: Not nullable, follows UUID or auto-increment pattern

- `conversation_id`: String (Required)
  - Purpose: Links to the conversation where the action occurred
  - Constraints: References an active conversation
  - Validation: Must exist in conversations table

- `message_id`: Integer/UUID (Required)
  - Purpose: Links to the specific message that triggered the tool action
  - Constraints: References a specific chat message
  - Validation: Foreign key to chat_messages table

- `tool_name`: String (Required)
  - Purpose: Identifies which tool was called
  - Constraints: Valid tool name (add_todo, get_todos, update_todo_status)
  - Validation: Enum validation for known tools

- `tool_input`: JSON (Required)
  - Purpose: Captures the parameters sent to the tool
  - Constraints: Valid JSON structure
  - Validation: Properly formatted JSON

- `tool_output`: JSON (Optional)
  - Purpose: Captures the result returned by the tool
  - Constraints: Valid JSON structure
  - Validation: Properly formatted JSON

- `status`: String (Required)
  - Purpose: Indicates the success/failure of the tool call
  - Constraints: Success, error, or pending
  - Validation: Enum validation (success/error/pending)

## Relationships

### ChatMessage to User
- **Relationship Type**: Many-to-One (Many messages belong to one user)
- **Cardinality**: 0..* ChatMessages → 1 User
- **Constraint**: Foreign key from ChatMessage.user_id to User.id
- **Cascade Behavior**: Messages remain if user is deleted (audit trail)

### ChatMessage to Conversation
- **Relationship Type**: Many-to-One (Many messages belong to one conversation)
- **Cardinality**: 0..* ChatMessages → 1 Conversation
- **Constraint**: Foreign key from ChatMessage.conversation_id to Conversation.id
- **Cascade Behavior**: Messages are deleted when conversation is deleted

### Tool Response to Message
- **Relationship Type**: One-to-One (One tool response corresponds to one message)
- **Cardinality**: 1 ToolResponse → 1 ChatMessage
- **Constraint**: Foreign key from ToolResponse.message_id to ChatMessage.id
- **Cascade Behavior**: Tool responses deleted when associated message is deleted

## Validation Rules

### At Creation Time:
- ChatMessage content must be provided and not empty after whitespace trimming
- Role must be either "user" or "assistant"
- User must be authenticated before message creation
- Conversation must exist before adding messages

### At Update Time:
- Messages are immutable once created (append-only model)
- Conversation context may update last_active timestamp
- Tool responses are immutable once processed

### Access Control:
- Users can only access their own conversations and messages
- Agents validate user context before performing actions
- Authentication required for all conversation operations