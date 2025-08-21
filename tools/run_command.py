import subprocess

def run_command(command: str):
    """
    Executes a shell command.

    For the model: Use this to run shell commands. Be careful with this tool.

    Args:
        command (str): The command to execute.

    Returns:
        dict: A dictionary containing the command's stdout, stderr, and return code.
    """
    try:
        process = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=False
        )
        return {
            "stdout": process.stdout,
            "stderr": process.stderr,
            "returncode": process.returncode,
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "returncode": 1,
        }
