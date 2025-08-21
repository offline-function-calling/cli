import os
import fnmatch

def search_files(directory: str, pattern: str):
    """
    Searches for files matching a pattern in a directory and its subdirectories.

    For the model: Use this to find files. The pattern can include wildcards like *.txt.

    Args:
        directory (str): The directory to start the search from.
        pattern (str): The search pattern (e.g., '*.py', 'data_*.csv').

    Returns:
        list: A list of paths to matching files.
    """
    matches = []
    for root, _, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
    return matches
