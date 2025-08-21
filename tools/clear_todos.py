import os

def clear_todos():
    """
    Clears all tasks from the todo list.

    For the model: Use this to clear the entire todo list. This is a destructive action.

    Args:
        None

    Returns:
        str: A confirmation message.
    """
    todo_file = os.path.expanduser("~/todos.md")
    if os.path.exists(todo_file):
        try:
            os.remove(todo_file)
            return "Todo list cleared."
        except OSError as e:
            return f"Error clearing todo list: {e}"
    return "Todo list is already empty."
