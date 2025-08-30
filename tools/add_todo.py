import os


def add_todo(task: str):
    """
    Adds a new task to the todo list.

    For the model: Use this to add a new task to the user's todo list.

    Args:
        task (str): The task to add.

    Returns:
        str: A confirmation message.
    """
    todo_file = os.path.expanduser("~/todos.md")
    try:
        with open(todo_file, "a") as f:
            f.write(f"- [ ] {task}\n")
        return f"Added task: '{task}'"
    except IOError as e:
        return f"Error adding task: {e}"
