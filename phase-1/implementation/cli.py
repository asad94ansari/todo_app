"""
Command-line interface for the todo application.
"""
import re
from typing import Tuple, Optional
try:
    from implementation.service import TodoService
    from implementation.todo_model import Todo
except ImportError:
    from service import TodoService
    from todo_model import Todo


class TodoCLI:
    """
    Handles user input and output for the todo application.

    The CLI provides a command-driven interface for interacting with
    the todo service, parsing commands and displaying results.
    """

    def __init__(self):
        """Initialize the CLI with a service instance."""
        self.service = TodoService()
        self.running = True

    def run(self):
        """Start the main command loop."""
        print("Welcome to the Todo Application!")
        print("Available commands: ADD, LIST, UPDATE, DELETE, COMPLETE, HELP, EXIT")
        print("Type 'HELP' for detailed command information.\n")

        while self.running:
            try:
                user_input = input("> ").strip()
                if user_input:
                    self.process_command(user_input)
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break

    def process_command(self, command_line: str):
        """
        Process a single command from the user.

        Args:
            command_line: The full command line input from the user
        """
        parts = command_line.split(maxsplit=1)
        command = parts[0].upper()

        if command == "ADD":
            self.handle_add(parts[1] if len(parts) > 1 else "")
        elif command == "LIST":
            self.handle_list()
        elif command == "UPDATE":
            self.handle_update(parts[1] if len(parts) > 1 else "")
        elif command == "DELETE":
            self.handle_delete(parts[1] if len(parts) > 1 else "")
        elif command == "COMPLETE":
            self.handle_complete(parts[1] if len(parts) > 1 else "")
        elif command == "HELP":
            self.handle_help()
        elif command == "EXIT":
            self.handle_exit()
        else:
            print(f"Unknown command: {command}. Type 'HELP' for available commands.")

    def handle_add(self, args: str):
        """
        Handle the ADD command.

        Args:
            args: Arguments following the ADD command
        """
        # Extract title and description using regex
        # Format: "title" ["description"] or just "title"
        match = re.match(r'^"([^"]*)"(?:\s+"([^"]*)")?$', args)

        if not match:
            print('Invalid format for ADD. Use: ADD "title" ["description"]')
            return

        title = match.group(1)
        description = match.group(2) if match.group(2) else None

        try:
            new_task = self.service.add_task(title, description)
            print(f"Added task #{new_task.id}: {title}")
        except ValueError as e:
            print(f"Error: {str(e)}")

    def handle_list(self, args: str = ""):
        """
        Handle the LIST command.

        Args:
            args: Arguments following the LIST command (ignored)
        """
        tasks = self.service.list_tasks()

        if not tasks:
            print("No tasks found.")
        else:
            for task in tasks:
                print(task)

    def handle_update(self, args: str):
        """
        Handle the UPDATE command.

        Args:
            args: Arguments following the UPDATE command
        """
        # Extract id, title and description using regex
        # Format: id "title" ["description"]
        match = re.match(r'^(\d+)\s+"([^"]*)"(?:\s+"([^"]*)")?$', args)

        if not match:
            print('Invalid format for UPDATE. Use: UPDATE id "title" ["description"]')
            return

        task_id = int(match.group(1))
        title = match.group(2)
        description = match.group(3) if match.group(3) else None

        if not self.service.task_exists(task_id):
            print(f"Error: Task with ID {task_id} does not exist")
            return

        try:
            success = self.service.update_task(task_id, title, description)
            if success:
                print(f"Task #{task_id} updated successfully")
            else:
                print(f"Error: Failed to update task with ID {task_id}")
        except ValueError as e:
            print(f"Error: {str(e)}")

    def handle_delete(self, args: str):
        """
        Handle the DELETE command.

        Args:
            args: Arguments following the DELETE command
        """
        parts = args.split()
        if not parts:
            print("Invalid format for DELETE. Use: DELETE id")
            return

        try:
            task_id = int(parts[0])

            if not self.service.task_exists(task_id):
                print(f"Error: Task with ID {task_id} does not exist")
                return

            success = self.service.delete_task(task_id)
            if success:
                print(f"Task #{task_id} deleted successfully")
            else:
                print(f"Error: Failed to delete task with ID {task_id}")
        except ValueError:
            print("Invalid task ID. Please provide a valid number.")

    def handle_complete(self, args: str):
        """
        Handle the COMPLETE command.

        Args:
            args: Arguments following the COMPLETE command
        """
        parts = args.split()
        if not parts:
            print("Invalid format for COMPLETE. Use: COMPLETE id")
            return

        try:
            task_id = int(parts[0])

            if not self.service.task_exists(task_id):
                print(f"Error: Task with ID {task_id} does not exist")
                return

            success = self.service.complete_task(task_id)
            if success:
                # Get the updated task to show its new status
                tasks = self.service.list_tasks()
                task = next((t for t in tasks if t.id == task_id), None)
                if task:
                    status = "complete" if task.completed else "incomplete"
                    print(f"Task #{task_id} marked as {status}")
                else:
                    print(f"Error: Failed to retrieve updated task with ID {task_id}")
            else:
                print(f"Error: Failed to update task with ID {task_id}")
        except ValueError:
            print("Invalid task ID. Please provide a valid number.")

    def handle_help(self, args: str = ""):
        """
        Handle the HELP command.

        Args:
            args: Arguments following the HELP command (ignored)
        """
        print("\nAvailable Commands:")
        print("ADD \"title\" [\"description\"] - Create a new todo task")
        print("LIST - Display all current tasks with their status")
        print("UPDATE id \"title\" [\"description\"] - Update an existing task")
        print("DELETE id - Remove a task by ID")
        print("COMPLETE id - Toggle completion status of a task")
        print("HELP - Show this help message")
        print("EXIT - Quit the application\n")

    def handle_exit(self, args: str = ""):
        """
        Handle the EXIT command.

        Args:
            args: Arguments following the EXIT command (ignored)
        """
        self.running = False
        print("Goodbye!")