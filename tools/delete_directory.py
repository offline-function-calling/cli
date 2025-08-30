import os
import shutil


def delete_directory(directory_path: str):
    """
    Deletes a directory and its contents recursively.

    For the model: Use this to delete a directory. This is a destructive action.

    Args:
        directory_path (str): The path of the directory to delete.

    Returns:
        str: A confirmation message.

    Raises:
        FileNotFoundError: If the directory does not exist.
        OSError: If an error occurs during deletion.
    """
    if not os.path.isdir(directory_path):
        raise FileNotFoundError(f"The directory '{directory_path}' does not exist.")
    try:
        shutil.rmtree(directory_path)
        return f"Successfully deleted directory '{directory_path}'."
    except OSError as e:
        raise OSError(f"Error deleting directory '{directory_path}': {e}")
