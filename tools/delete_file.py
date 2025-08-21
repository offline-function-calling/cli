import os

def delete_file(file_path: str):
    """
    Deletes a specified file.

    For the model: Use this to delete a file.

    Args:
        file_path (str): The path to the file to delete.

    Returns:
        str: A confirmation message.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        OSError: If an error occurs during deletion.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    try:
        os.remove(file_path)
        return f"Successfully deleted '{file_path}'."
    except OSError as e:
        raise OSError(f"Error deleting file '{file_path}': {e}")
