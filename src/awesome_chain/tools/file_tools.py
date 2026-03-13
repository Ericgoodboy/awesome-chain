"""
File-related tools for reading and writing files.
"""

import os
import json
from pathlib import Path
from typing import Optional, List

from config.settings import settings
from src.awesome_chain.core.tool_registry import tool


@tool
def read_file(file_path: str) -> str:
    """
    Read the contents of a file.

    Args:
        file_path: Path to the file to read

    Returns:
        File contents as a string
    """
    try:
        # Resolve relative paths
        path = Path(file_path)
        if not path.is_absolute():
            # Check if path is relative to samples directory
            samples_file = Path(settings.SAMPLES_DIR) / file_path
            if samples_file.exists():
                path = samples_file
            else:
                # Check data directory
                data_file = Path(settings.DATA_DIR) / file_path
                if data_file.exists():
                    path = data_file

        if not path.exists():
            return f"Error: File not found at {path}"

        content = path.read_text(encoding='utf-8')

        # Truncate very large files
        max_length = 10000
        if len(content) > max_length:
            content = content[:max_length] + f"\n... [File truncated, showing first {max_length} characters]"

        return content

    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool
def write_file(file_path: str, content: str) -> str:
    """
    Write content to a file.

    Args:
        file_path: Path to the file to write
        content: Content to write

    Returns:
        Success message or error
    """
    try:
        path = Path(file_path)

        # Create parent directories if they don't exist
        path.parent.mkdir(parents=True, exist_ok=True)

        # Handle relative paths
        if not path.is_absolute():
            path = Path(settings.DATA_DIR) / file_path

        path.write_text(content, encoding='utf-8')

        return f"Successfully wrote {len(content)} characters to {path}"

    except Exception as e:
        return f"Error writing file: {str(e)}"


@tool
def list_files(directory: str = ".") -> str:
    """
    List files in a directory.

    Args:
        directory: Directory to list (default: current directory)

    Returns:
        List of files and directories
    """
    try:
        path = Path(directory)

        # Handle relative paths
        if not path.is_absolute():
            if directory == ".":
                path = Path(settings.BASE_DIR)
            else:
                path = Path(settings.DATA_DIR) / directory

        if not path.exists():
            return f"Error: Directory not found at {path}"

        if not path.is_dir():
            return f"Error: {path} is not a directory"

        items = []
        for item in sorted(path.iterdir()):
            item_type = "DIR" if item.is_dir() else "FILE"
            items.append(f"  [{item_type}] {item.name}")

        if not items:
            return "Directory is empty"

        return f"Contents of {path}:\n" + "\n".join(items)

    except Exception as e:
        return f"Error listing directory: {str(e)}"


@tool
def search_files(search_term: str, directory: str = ".") -> str:
    """
    Search for files by name or extension.

    Args:
        search_term: Search term (filename or extension)
        directory: Directory to search in

    Returns:
        List of matching files
    """
    try:
        path = Path(directory)

        if not path.is_absolute():
            if directory == ".":
                path = Path(settings.BASE_DIR)
            else:
                path = Path(settings.DATA_DIR) / directory

        if not path.exists():
            return f"Error: Directory not found at {path}"

        matches = []

        # Search in directory
        for item in path.rglob("*"):
            if item.is_file():
                # Check if search term matches filename
                if search_term.lower() in item.name.lower():
                    matches.append(str(item.relative_to(path)))

        if not matches:
            return f"No files found matching '{search_term}'"

        return f"Files matching '{search_term}':\n  " + "\n  ".join(matches)

    except Exception as e:
        return f"Error searching files: {str(e)}"


@tool
def read_json(file_path: str) -> str:
    """
    Read and parse a JSON file.

    Args:
        file_path: Path to the JSON file

    Returns:
        Parsed JSON as formatted string
    """
    try:
        path = Path(file_path)
        if not path.is_absolute():
            path = Path(settings.DATA_DIR) / file_path

        if not path.exists():
            return f"Error: File not found at {path}"

        data = json.loads(path.read_text(encoding='utf-8'))
        return json.dumps(data, indent=2, ensure_ascii=False)

    except json.JSONDecodeError as e:
        return f"Error: Invalid JSON in file - {str(e)}"
    except Exception as e:
        return f"Error reading JSON file: {str(e)}"


@tool
def write_json(file_path: str, data: str) -> str:
    """
    Write data to a JSON file.

    Args:
        file_path: Path to the JSON file
        data: JSON string to write

    Returns:
        Success message or error
    """
    try:
        path = Path(file_path)
        if not path.is_absolute():
            path = Path(settings.DATA_DIR) / file_path

        path.parent.mkdir(parents=True, exist_ok=True)

        # Parse and validate JSON
        parsed = json.loads(data)
        path.write_text(json.dumps(parsed, indent=2), encoding='utf-8')

        return f"Successfully wrote JSON to {path}"

    except json.JSONDecodeError as e:
        return f"Error: Invalid JSON - {str(e)}"
    except Exception as e:
        return f"Error writing JSON file: {str(e)}"


def register_file_tools() -> None:
    """Register all file tools manually."""
    # Tools are already registered via decorators
    pass
