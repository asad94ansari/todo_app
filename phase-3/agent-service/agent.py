"""
AI Orchestrator agent for the todo chatbot.
Uses OpenAI Agents SDK to connect with MCP tools.
"""
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import openai

load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

class TodoAssistantAgent:
    """
    AI Orchestrator agent that handles natural language requests
    and translates them to MCP tool calls.
    """
    def __init__(self):
        """
        Initialize the Todo Assistant Agent.
        This sets up the OpenAI assistant with the appropriate tools.
        """
        # Define the tools that the agent can use
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_todo",
                    "description": "Create a new task for the authenticated user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "The title of the new task"
                            },
                            "description": {
                                "type": "string",
                                "description": "Additional details about the task"
                            },
                            "due_date": {
                                "type": "string",
                                "description": "Due date in ISO format"
                            },
                            "priority": {
                                "type": "string",
                                "description": "Priority level (low, medium, high)"
                            }
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_todos",
                    "description": "Retrieve tasks for the authenticated user with optional filtering",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "description": "Filter by status (all, completed, pending)"
                            },
                            "limit": {
                                "type": "number",
                                "description": "Maximum number of tasks to return (default: 20)"
                            },
                            "offset": {
                                "type": "number",
                                "description": "Number of tasks to skip (for pagination)"
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_todo_status",
                    "description": "Update the completion status of a specific task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "number",
                                "description": "The ID of the task to update"
                            },
                            "status": {
                                "type": "boolean",
                                "description": "The new completion status (true for completed, false for pending)"
                            },
                            "notes": {
                                "type": "string",
                                "description": "Additional notes about the update"
                            }
                        },
                        "required": ["task_id", "status"]
                    }
                }
            }
        ]

        # Create or retrieve an assistant
        try:
            # Try to retrieve an existing assistant
            self.assistant = openai.beta.assistants.retrieve(os.getenv("ASSISTANT_ID", ""))
        except:
            # If assistant doesn't exist, create a new one
            self.assistant = openai.beta.assistants.create(
                name="Todo Assistant",
                description="An AI assistant that helps users manage their todo lists",
                model=os.getenv("OPENAI_MODEL", "gpt-4-turbo"),  # Use appropriate model
                tools=self.tools,
                # Note: In a real implementation, we would need to connect this to MCP tools
                # This is a simplified version for demonstration
            )

            # Save the assistant ID to environment for future use
            # In practice, you'd save this to a database or config file
            print(f"New assistant created with ID: {self.assistant.id}")

    def process_message(self, message: str, user_id: int, conversation_id: Optional[str] = None) -> str:
        """
        Process a user message and return the agent's response.

        Args:
            message: The user's message
            user_id: The ID of the authenticated user
            conversation_id: Optional conversation identifier

        Returns:
            The agent's response as a string
        """
        try:
            # In a real implementation, this would connect to MCP tools
            # For this example, we'll simulate the process

            # Create a thread for this conversation
            thread = openai.beta.threads.create()

            # Add the user message to the thread
            openai.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=message
            )

            # Run the assistant on the thread
            run = openai.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=self.assistant.id,
                # In a real MCP implementation, we would need to specify tool handling
            )

            # Wait for the run to complete
            import time
            while run.status in ["queued", "in_progress"]:
                time.sleep(0.5)
                run = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

            # Get the messages from the thread
            messages = openai.beta.threads.messages.list(thread_id=thread.id)

            # Extract the assistant's response
            assistant_responses = [
                msg.content[0].text.value
                for msg in messages.data
                if msg.role == "assistant"
            ]

            if assistant_responses:
                return assistant_responses[0]
            else:
                return "I couldn't process your request. Please try again."

        except Exception as e:
            # Log the error in a real implementation
            print(f"Error processing message: {e}")
            return "Sorry, I encountered an error processing your request. Please try again."


# For a more complete implementation using actual MCP tools, we would need to:
# 1. Make HTTP requests to the MCP server endpoints
# 2. Handle the responses from the MCP tools
# 3. Format the responses appropriately for the chat interface