def write_file(file_path: str, content: str):
    """
    Writes content to a specified file, overwriting it if it exists.

    For the model: Use this to write or overwrite a file with new content.

    Args:
        file_path (str): The path to the file to write to.
        content (str): The content to write to the file.

    Returns:
        str: A confirmation message.

    Raises:
        IOError: If an error occurs while writing to the file.
    """
    try:
        with open(file_path, "w") as f:
            f.write(content)
        return f"Successfully wrote to '{file_path}'."
    except IOError as e:
        raise IOError(f"Error writing to file '{file_path}': {e}")
