import os


def read_file(file_path: str):
    """
    Reads the entire content of a specified file.

    For the model: Use this to read the contents of a file. The output is a
    string containing the file's content.

    Args:
        file_path (str): The path to the file to read.

    Returns:
        str: The content of the file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        IOError: If an error occurs while reading the file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    try:
        with open(file_path, "r") as f:
            return f.read()
    except IOError as e:
        raise IOError(f"Error reading file '{file_path}': {e}")
