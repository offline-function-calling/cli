import os
import shutil

def move_file(source_path: str, destination_path: str):
    """
    Moves or renames a file or directory.

    For the model: Use this to move or rename files and directories.

    Args:
        source_path (str): The path of the file or directory to move.
        destination_path (str): The destination path.

    Returns:
        str: A confirmation message.

    Raises:
        FileNotFoundError: If the source does not exist.
        OSError: If an error occurs during the move.
    """
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"The source path '{source_path}' does not exist.")
    try:
        shutil.move(source_path, destination_path)
        return f"Successfully moved '{source_path}' to '{destination_path}'."
    except OSError as e:
        raise OSError(f"Error moving '{source_path}': {e}")
