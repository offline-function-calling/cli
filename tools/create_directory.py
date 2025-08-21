import os

def create_directory(directory_path: str):
    """
    Creates a new directory.

    For the model: Use this to create a new directory.

    Args:
        directory_path (str): The path of the directory to create.

    Returns:
        str: A confirmation message.

    Raises:
        FileExistsError: If the directory already exists.
        OSError: If an error occurs during creation.
    """
    if os.path.exists(directory_path):
        raise FileExistsError(f"The directory '{directory_path}' already exists.")
    try:
        os.makedirs(directory_path)
        return f"Successfully created directory '{directory_path}'."
    except OSError as e:
        raise OSError(f"Error creating directory '{directory_path}': {e}")
