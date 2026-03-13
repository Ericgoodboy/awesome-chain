"""
Tool Registry for managing and discovering tools.

Simplified approach: directly create tool functions and register them,
avoiding circular import issues with decorators.
"""

from __future__ import annotations
import functools
from typing import Dict, List, Callable, Optional, Union, Any
from pathlib import Path

from langchain_core.tools import tool as langchain_tool, StructuredTool


# Constants
MAX_FILE_CONTENT_LENGTH = 10000  # Maximum characters to read from a file


# Global tool registry (moved to ToolRegistry class attributes)


# Export tool decorator for external use
def tool(name: Optional[str] = None, description: Optional[str] = None):
    """
    Decorator for registering tools using LangChain's tool decorator.

    Args:
        name: Tool name (defaults to function name)
        description: Tool description (defaults to docstring)
    """
    def decorator(func: Callable) -> Callable:
        # Register the tool using ToolRegistry
        ToolRegistry.register(func, name=name, description=description)
        # Return the original function (registration is side effect)
        return func
    return decorator


class ToolRegistry:
    """Registry for managing tools."""

    # Class-level tool registries
    _tools: Dict[str, StructuredTool] = {}
    _tool_functions: Dict[str, Callable] = {}

    @staticmethod
    def register(func: Callable, name: Optional[str] = None,
                description: Optional[str] = None) -> StructuredTool:
        """
        Register a tool using LangChain's tool decorator.

        Args:
            func: Function to register as tool
            name: Tool name
            description: Tool description

        Returns:
            The registered tool
        """
        # Create base tool using LangChain's decorator
        tool_obj = langchain_tool(description=description)(func)

        if name is None:
            # Use the tool as-is (name will be function name)
            result = tool_obj
        else:
            # Create a new tool with the specified name
            result = StructuredTool(
                name=name,
                description=tool_obj.description,
                func=tool_obj.func,
                return_direct=tool_obj.return_direct,
                args_schema=tool_obj.args_schema
            )

        # Store in our registry
        ToolRegistry._tools[result.name] = result
        ToolRegistry._tool_functions[result.name] = func

        return result

    @staticmethod
    def get(name: str) -> Optional[StructuredTool]:
        """Get a tool by name."""
        return ToolRegistry._tools.get(name)

    @staticmethod
    def get_all() -> List[StructuredTool]:
        """Get all registered tools."""
        return list(ToolRegistry._tools.values())

    @staticmethod
    def get_names() -> List[str]:
        """Get all registered tool names."""
        return list(ToolRegistry._tools.keys())

    @staticmethod
    def unregister(name: str) -> bool:
        """Unregister a tool by name."""
        if name in ToolRegistry._tools:
            del ToolRegistry._tools[name]
            del ToolRegistry._tool_functions[name]
            return True
        return False

    @staticmethod
    def clear() -> None:
        """Clear all registered tools."""
        ToolRegistry._tools.clear()
        ToolRegistry._tool_functions.clear()

    @staticmethod
    def get_tool_function(name: str) -> Optional[Callable]:
        """Get the Python function behind a tool."""
        return ToolRegistry._tool_functions.get(name)

    @staticmethod
    def count() -> int:
        """Get the number of registered tools."""
        return len(ToolRegistry._tools)

    @staticmethod
    def list_tools() -> str:
        """List all tools with descriptions."""
        if not ToolRegistry._tools:
            return "No tools registered yet."
        output = "Registered Tools:\n"
        for name, t in ToolRegistry._tools.items():
            output += f"  - {name}: {t.description}\n"
        return output


# ============================================================================
# Helper Functions
# ============================================================================

def _resolve_path(path_str: str, base_dir: Optional[Path] = None) -> Path:
    """
    Resolve a path string to an absolute path.
    If the path is relative, it will be resolved relative to DATA_DIR.

    Args:
        path_str: Path string to resolve
        base_dir: Optional base directory for relative paths (defaults to DATA_DIR)

    Returns:
        Resolved absolute Path object
    """
    from config.settings import settings

    if base_dir is None:
        base_dir = Path(settings.DATA_DIR)

    path = Path(path_str)
    if not path.is_absolute():
        path = base_dir / path
    return path


def _handle_error(error: Exception, operation: str, context: str = "") -> str:
    """
    Format error messages consistently.

    Args:
        error: The exception that occurred
        operation: Description of the operation being performed
        context: Additional context information

    Returns:
        Formatted error message
    """
    error_msg = f"Error {operation}"
    if context:
        error_msg += f" ({context})"
    error_msg += f": {str(error)}"
    return error_msg


# ============================================================================
# File Tool Functions
# ============================================================================

def _read_file(file_path: str) -> str:
    """Read the contents of a file."""
    try:
        path = _resolve_path(file_path)

        if not path.exists():
            return f"Error: File not found at {path}"

        content = path.read_text(encoding='utf-8')

        if len(content) > MAX_FILE_CONTENT_LENGTH:
            content = content[:MAX_FILE_CONTENT_LENGTH] + f"\n... [File truncated, showing first {MAX_FILE_CONTENT_LENGTH} characters]"

        return content
    except Exception as e:
        return _handle_error(e, "reading file", file_path)


def _write_file(file_path: str, content: str) -> str:
    """Write content to a file."""
    try:
        path = _resolve_path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return f"Successfully wrote {len(content)} characters to {path}"
    except Exception as e:
        return _handle_error(e, "writing file", file_path)


def _list_files(directory: str = ".") -> str:
    """List files in a directory."""
    try:
        path = _resolve_path(directory)

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
        return _handle_error(e, "listing directory", directory)


def _search_files(search_term: str, directory: str = ".") -> str:
    """Search for files by name or extension."""
    try:
        path = _resolve_path(directory)

        if not path.exists():
            return f"Error: Directory not found at {path}"

        matches = []
        for item in path.rglob("*"):
            if item.is_file():
                if search_term.lower() in item.name.lower():
                    matches.append(str(item.relative_to(path)))

        if not matches:
            return f"No files found matching '{search_term}'"
        return f"Files matching '{search_term}':\n  " + "\n  ".join(matches)
    except Exception as e:
        return _handle_error(e, "searching files", f"'{search_term}' in '{directory}'")


def _read_json(file_path: str) -> str:
    """Read and parse a JSON file."""
    import json

    try:
        path = _resolve_path(file_path)
        if not path.exists():
            return f"Error: File not found at {path}"
        data = json.loads(path.read_text(encoding='utf-8'))
        return json.dumps(data, indent=2, ensure_ascii=False)
    except json.JSONDecodeError as e:
        return f"Error: Invalid JSON in file - {str(e)}"
    except Exception as e:
        return _handle_error(e, "reading JSON file", file_path)


def _write_json(file_path: str, data: str) -> str:
    """Write data to a JSON file."""
    import json

    try:
        path = _resolve_path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        parsed = json.loads(data)
        path.write_text(json.dumps(parsed, indent=2), encoding='utf-8')
        return f"Successfully wrote JSON to {path}"
    except json.JSONDecodeError as e:
        return f"Error: Invalid JSON - {str(e)}"
    except Exception as e:
        return _handle_error(e, "writing JSON file", file_path)


# ============================================================================
# Web Tool Functions
# ============================================================================

def _search_web(query: str, num_results: int = 5) -> str:
    """
    Search the web using DuckDuckGo.

    Args:
        query: Search query
        num_results: Number of results to return

    Returns:
        Search results
    """
    try:
        from ddgs import DDGS
        import json
        
        results = []
        with DDGS() as ddgs:
            search_results = ddgs.text(
                query,
                max_results=num_results
            )
            
            for result in search_results:
                results.append({
                    "title": result.get("title", ""),
                    "url": result.get("href", ""),
                    "snippet": result.get("body", "")
                })
        
        return json.dumps(results, indent=2, ensure_ascii=False)

    except Exception as e:
        return _handle_error(e, "searching web", f"query: '{query}'")


def _fetch_url(url: str) -> str:
    """
    Fetch content from a URL.

    Args:
        url: URL to fetch

    Returns:
        URL content
    """
    import requests
    from urllib.parse import urlparse

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        content_type = response.headers.get('content-type', '')
        
        if 'text/html' in content_type:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            for script in soup(['script', 'style', 'nav', 'footer', 'header']):
                script.decompose()
            text = soup.get_text(separator='\n', strip=True)
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            return '\n'.join(lines[:500])
        elif 'application/json' in content_type:
            import json
            return json.dumps(response.json(), indent=2, ensure_ascii=False)
        else:
            return response.text[:10000]

    except requests.exceptions.Timeout:
        return f"Error: Request to {url} timed out after 30 seconds"
    except requests.exceptions.RequestException as e:
        return f"Error fetching URL {url}: {str(e)}"
    except Exception as e:
        return _handle_error(e, "processing content from", url)


# ============================================================================
# Command Tool Functions
# ============================================================================

def _execute_command(command: str) -> str:
    """
    在本地 shell 中执行命令并返回输出。

    Args:
        command: 要执行的 shell 命令

    Returns:
        命令的标准输出（或错误信息）
    """
    import subprocess
    import shlex

    try:
        args = shlex.split(command)
        completed = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=30
        )
        if completed.returncode == 0:
            return completed.stdout.strip()
        else:
            return f"命令执行失败（返回码 {completed.returncode}）:\n{completed.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return "错误：命令执行超时（超过 30 秒）"
    except Exception as e:
        return _handle_error(e, "executing command", f"'{command}'")


# ============================================================================
# Tool Registration
# ============================================================================

def _register_builtins():
    """Register all built-in tools."""
    try:
        # List of (function, name, description) for built-in tools
        builtin_tools = [
            (_read_file, "read_file",
             "Read the contents of a file. Args: file_path (str): Path to the file to read"),
            (_search_files, "search_files",
             "Search for files by name or extension. Args: search_term (str): Search term (filename or extension), directory (str, optional): Directory to search in (default: '.')"),
            (_read_json, "read_json",
             "Read and parse a JSON file. Args: file_path (str): Path to the JSON file"),
            (_search_web, "search_web",
             "Search the web using DuckDuckGo. Args: query (str): Search query, num_results (int, optional): Number of results to return (default: 5)"),
            (_fetch_url, "fetch_url",
             "Fetch content from a URL. Args: url (str): URL to fetch"),
            (_execute_command, "execute_command",
             "Execute a command in local shell and return output. Args: command (str): Shell command to execute"),
        ]

        for func, name, description in builtin_tools:
            ToolRegistry.register(func, name=name, description=description)

        print(f"Registered {ToolRegistry.count()} tools:")
        for name in ToolRegistry.get_names():
            print(f"  - {name}")

    except Exception as e:
        import traceback
        print(f"Warning: Failed to load built-in tools: {e}")
        traceback.print_exc()


# Auto-register built-ins on import
_register_builtins()
