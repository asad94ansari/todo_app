"""
Validation utilities for the todo application.
"""


def validate_task_title(title: str) -> bool:
    """
    Validate that a task title is not empty or whitespace only.

    Args:
        title: The title to validate

    Returns:
        True if the title is valid, False otherwise
    """
    return bool(title and title.strip())


def validate_task_id(task_id: str) -> bool:
    """
    Validate that a task ID is a valid integer string.

    Args:
        task_id: The task ID string to validate

    Returns:
        True if the ID is valid, False otherwise
    """
    try:
        int(task_id)
        return True
    except ValueError:
        return False


def sanitize_input(input_str: str) -> str:
    """
    Sanitize user input by stripping leading/trailing whitespace.

    Args:
        input_str: The input string to sanitize

    Returns:
        Sanitized string with whitespace stripped
    """
    return input_str.strip() if input_str else ""