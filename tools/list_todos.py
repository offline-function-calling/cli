import os

def list_todos():
    """
    Lists all tasks in the todo list.

    For the model: Use this to list all the tasks in the user's todo list.

    Args:
        None

    Returns:
        str: The content of the todo list, or a message if it's empty.
    """
    todo_file = os.path.expanduser("~/todos.md")
    if not os.path.exists(todo_file):
        return "Your todo list is empty."
    try:
        with open(todo_file, "r") as f:
            return f.read()
    except IOError as e:
        return f"Error reading todo list: {e}"
