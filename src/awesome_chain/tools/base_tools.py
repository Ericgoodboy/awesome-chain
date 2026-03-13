"""
Base tool definitions and utilities.
"""

from typing import Any, Optional, Type, Callable
from functools import wraps

from src.awesome_chain.core.tool_registry import tool, ToolRegistry


def register_tool(
    func: Optional[Callable] = None,
    *,
    name: Optional[str] = None,
    description: Optional[str] = None
) -> Any:
    """
    Decorator or function to register a tool.

    Can be used as:
        @register_tool
        def my_tool(): ...

        @register_tool(name="custom_name")
        def my_tool(): ...

        register_tool(my_func, name="custom_name")
    """
    def decorator(f: Callable) -> Callable:
        return ToolRegistry.register(f, name=name, description=description)

    if func is not None:
        return decorator(func)
    return decorator


def create_tool(
    name: str,
    description: str,
    func: Callable
):
    """
    Create and register a tool programmatically.

    Args:
        name: Tool name
        description: Tool description
        func: Tool function
    """
    return ToolRegistry.register(func, name=name, description=description)


class ToolGroup:
    """Group related tools together."""

    def __init__(self, prefix: str):
        """
        Initialize tool group.

        Args:
            prefix: Prefix to add to all tool names in this group
        """
        self.prefix = prefix
        self._tools = []

    def add(self, name: str, description: str, func: Callable):
        """Add a tool to the group."""
        full_name = f"{self.prefix}.{name}"
        self._tools.append(ToolRegistry.register(
            func,
            name=full_name,
            description=description
        ))

    def get_all(self):
        """Get all tools in the group."""
        return self._tools
