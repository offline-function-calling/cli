import os

def get_file_size(file_path: str):
    """
    Gets the size of a file in bytes.

    For the model: Use this to get the size of a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        int: The size of the file in bytes.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    return os.path.getsize(file_path)
