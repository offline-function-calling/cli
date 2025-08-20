import re

from pathlib import Path
from typing import List, Tuple

from .interface import ChatInterface


class FileHandler:
    """Handles file path detection and validation from user input."""

    def __init__(self, interface: ChatInterface):
        self.interface = interface

        self.patterns = [
            re.compile(r"file://([^\s]+)", re.IGNORECASE),  # file:///path/to/file.ext
            re.compile(r'"([^"]+\.[a-zA-Z0-9]+)"'),  # "path/to/file.ext"
            re.compile(r"'([^']+\.[a-zA-Z0-9]+)'"),  # 'path/to/file.ext'
            re.compile(
                r"\b([~/.][\w\-./\\]*\.[a-zA-Z0-9]+)\b"
            ),  # ./file.txt, ~/docs/file.pdf
            re.compile(
                r"\b([A-Za-z]:[/\\][\w\-./\\]*\.[a-zA-Z0-9]+)\b"
            ),  # C:/path/file.txt (Windows)
            re.compile(
                r"\b(/[\w\-./]*\.[a-zA-Z0-9]+)\b"
            ),  # /absolute/path/file.txt (Unix)
        ]

    def extract_files(self, prompt: str) -> Tuple[str, List[str]]:
        """Extract valid file paths from prompt, returning cleaned prompt and file list."""
        found_files = []
        cleaned_prompt = prompt

        for pattern in self.patterns:
            matches = list(pattern.finditer(cleaned_prompt))

            for match in reversed(matches):
                path_str = match.group(1) if match.groups() else match.group(0)
                if path_str.startswith("file://"):
                    path_str = path_str[7:]

                if self._is_like_file_path(path_str):
                    expanded_path = Path(path_str).expanduser().resolve()

                    if expanded_path.exists() and expanded_path.is_file():
                        if str(expanded_path) not in found_files:
                            found_files.append(str(expanded_path))
                        cleaned_prompt = (
                            cleaned_prompt[: match.start()]
                            + cleaned_prompt[match.end() :]
                        )
                    else:
                        self.interface.show_warning(f"File not found: {path_str}")

        cleaned_prompt = re.sub(r"\s+", " ", cleaned_prompt).strip()
        return cleaned_prompt, found_files

    def _is_like_file_path(self, path_str: str) -> bool:
        """Check if string looks like a valid file path."""
        if not path_str or len(path_str) < 2:
            return False

        if any(char in path_str for char in ["<", ">", "|", "*", "?", "\n", "\r"]):
            return False
        if "://" in path_str and not path_str.startswith("file://"):
            return False
        if " " in path_str and not (
            path_str.startswith('"') or path_str.startswith("'")
        ):
            words = path_str.split()
            if len(words) > 3:
                return False

        try:
            Path(path_str.replace("file://", ""))
            return True
        except (ValueError, OSError):
            return False
