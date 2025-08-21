import os

def get_environment_variable(variable_name: str):
    """
    Gets the value of an environment variable.

    For the model: Use this to get the value of an environment variable.

    Args:
        variable_name (str): The name of the environment variable.

    Returns:
        str: The value of the environment variable, or None if it's not set.
    """
    return os.environ.get(variable_name)
