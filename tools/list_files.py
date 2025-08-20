import os


def list_files(directory: str = "."):
    """
    Lists all files and subdirectories within a specified directory on the local filesystem.

    For the model: Use this to explore the filesystem. The output is a JSON object
    with two keys: 'directories' and 'files', each containing a list of names.
    Parse this JSON and present it clearly to the user, perhaps with bullet points.

    Args:
        directory (str, optional): The path to the directory to inspect.
                                   Defaults to the current working directory.

    Returns:
        dict: A JSON object containing lists of directories and files.

    Raises:
        FileNotFoundError: If the specified directory does not exist.
        PermissionError: If the agent does not have permission to read the directory.
    """
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"The directory '{directory}' does not exist.")

    items = os.listdir(directory)
    dirs = [item for item in items if os.path.isdir(os.path.join(directory, item))]
    files = [item for item in items if os.path.isfile(os.path.join(directory, item))]

    return {"directories": dirs, "files": files}
