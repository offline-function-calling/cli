import re
from pathlib import Path
from typing import List, Tuple

from .interface import ChatInterface


class FileHandler:
    """Handles file path detection and validation from user input."""

    def __init__(self, interface: ChatInterface):
        self.interface = interface

        ext_pattern = r"\.[a-zA-Z0-9]{2,6}\b"
        path_chars = r"[\w\-. \/\\\\]"

        self.patterns = [
            re.compile(r"file://(" + path_chars + r"*" + ext_pattern + r")", re.IGNORECASE),
            re.compile(r"\b([A-Za-z]:[\\/]" + path_chars + r"*" + ext_pattern + r")", re.IGNORECASE),
            re.compile(r"(?<![\w/\\:])(/" + path_chars + r"*" + ext_pattern + r")"),
            re.compile(r"\b((?:~|(?:\.\.?))[\\/]" + path_chars + r"*" + ext_pattern + r")"),
            re.compile(r"""
                (['"])
                (
                    (?:(?!\1).)*?
                    [/\\]
                    (?:(?!\1).)*?
                    """ + ext_pattern + r"""
                )
                \1
            """, re.VERBOSE),
            re.compile(r"\b([\w\-.]+\.(?:pdf|docx|xlsx|txt|csv|json|xml|log|py|js|html|css|zip|tar|gz|jpg|jpeg|png|gif|mp4|mov))\b", re.IGNORECASE)
        ]

    def extract_files(self, prompt: str) -> Tuple[str, List[str]]:
        """Extract valid file paths from prompt, returning cleaned prompt and file list."""
        found_files_set = set()
        cleaned_prompt = prompt

        for pattern in self.patterns:
            matches = list(pattern.finditer(cleaned_prompt))

            for match in reversed(matches):
                if len(match.groups()) > 1:
                    path_str = match.group(2)
                elif match.groups():
                    path_str = match.group(1)
                else:
                    continue

                if self._is_like_file_path(path_str):
                    cleaned_prompt = (
                        cleaned_prompt[: match.start()]
                        + cleaned_prompt[match.end() :]
                    )
                    
                    try:
                        expanded_path = Path(path_str).expanduser().resolve()
                    except (RuntimeError, ValueError):
                        self.interface.show_warning(f"Could not resolve path: {path_str}")
                        continue
                    
                    found_files_set.add(str(expanded_path))
                    if not expanded_path.exists() or not expanded_path.is_file():
                        self.interface.show_warning(f"File not found: {path_str}")

        cleaned_prompt = re.sub(r"\s+", " ", cleaned_prompt).strip()
        return cleaned_prompt, sorted(list(found_files_set))

    def _is_like_file_path(self, path_str: str) -> bool:
        """Check if string looks like a valid file path."""
        if not path_str or len(path_str) < 2:
            return False

        if any(char in path_str for char in ["<", ">", "|", "*", "?", "\n", "\r"]):
            return False
            
        if "://" in path_str and not path_str.lower().startswith("file://"):
            return False

        try:
            Path(path_str.replace("file://", "", 1))
            return True
        except (ValueError, OSError):
            return False
