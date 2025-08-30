import os


def complete_todo(task_number: int):
    """
    Marks a task as complete in the todo list.

    For the model: Use this to mark a task as complete. The task number is 1-based.

    Args:
        task_number (int): The number of the task to mark as complete.

    Returns:
        str: A confirmation message or an error message.
    """
    todo_file = os.path.expanduser("~/todos.md")
    if not os.path.exists(todo_file):
        return "Your todo list is empty."
    try:
        with open(todo_file, "r") as f:
            lines = f.readlines()
        if not (1 <= task_number <= len(lines)):
            return f"Invalid task number. Please choose a number between 1 and {len(lines)}."

        task_index = task_number - 1
        if lines[task_index].startswith("- [x]"):
            return "Task is already marked as complete."

        lines[task_index] = lines[task_index].replace("- [ ]", "- [x]", 1)

        with open(todo_file, "w") as f:
            f.writelines(lines)

        return f"Marked task {task_number} as complete."
    except (IOError, IndexError) as e:
        return f"Error completing task: {e}"
