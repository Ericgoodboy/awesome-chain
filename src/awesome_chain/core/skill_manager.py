"""
Skill Manager for dynamic skill loading and execution.
"""

import importlib
import inspect
import sys
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field

from langchain_core.tools import StructuredTool

from src.awesome_chain.core.tool_registry import ToolRegistry


@dataclass
class Skill:
    """Represents a loaded skill."""
    name: str
    module_path: str
    description: str
    tools: List[StructuredTool] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_tool(self, name: str) -> Optional[StructuredTool]:
        """Get a tool from this skill."""
        for tool in self.tools:
            if tool.name == name:
                return tool
        return None

    def get_tool_names(self) -> List[str]:
        """Get all tool names in this skill."""
        return [tool.name for tool in self.tools]


class SkillManager:
    """Manager for loading and managing skills."""

    _skills: Dict[str, Skill] = {}
    _skills_dir: str = ""

    @classmethod
    def set_skills_dir(cls, path: str) -> None:
        """Set the directory to search for skills."""
        cls._skills_dir = Path(path)
        # Add to Python path if not already there
        path_str = str(Path(path).parent.parent.parent.parent)
        if path_str not in sys.path:
            sys.path.insert(0, path_str)

    @classmethod
    def load_skill(cls, module_path: str, name: Optional[str] = None) -> Skill:
        """
        Load a skill from a module path.

        Args:
            module_path: Python module path (e.g., "skills.examples.data_analysis")
            name: Optional skill name (defaults to module name)

        Returns:
            The loaded skill
        """
        try:
            module = importlib.import_module(module_path)

            skill_name = name or module_path.split(".")[-1]
            description = getattr(module, "__doc__", f"Skill: {skill_name}") or f"Skill: {skill_name}"
            metadata = getattr(module, "SKILL_METADATA", {})

            # Collect tools from the module
            tools = []
            for attr_name, attr_value in inspect.getmembers(module):
                if inspect.isfunction(attr_value) and hasattr(attr_value, '__name__'):
                    # Check if function is in tool registry
                    tool = ToolRegistry.get(attr_value.__name__)
                    if tool:
                        tools.append(tool)

            skill = Skill(
                name=skill_name,
                module_path=module_path,
                description=description,
                tools=tools,
                metadata=metadata
            )

            cls._skills[skill_name] = skill
            return skill

        except ImportError as e:
            raise ImportError(f"Failed to load skill '{module_path}': {e}")

    @classmethod
    def load_skills_from_directory(cls, directory: str) -> List[Skill]:
        """
        Load all skills from a directory.

        Args:
            directory: Directory to search for skill modules

        Returns:
            List of loaded skills
        """
        skills = []
        dir_path = Path(directory)

        if not dir_path.exists():
            return skills

        for py_file in dir_path.glob("**/*.py"):
            if py_file.name.startswith("_"):
                continue

            relative = py_file.relative_to(dir_path.parent)
            module_path = str(relative.with_suffix("")).replace("/", ".").replace("\\", ".")

            try:
                skill = cls.load_skill(module_path)
                skills.append(skill)
            except Exception as e:
                print(f"Warning: Failed to load skill from {module_path}: {e}")

        return skills

    @classmethod
    def get_skill(cls, name: str) -> Optional[Skill]:
        """Get a loaded skill by name."""
        return cls._skills.get(name)

    @classmethod
    def get_all_skills(cls) -> List[Skill]:
        """Get all loaded skills."""
        return list(cls._skills.values())

    @classmethod
    def get_skill_names(cls) -> List[str]:
        """Get all loaded skill names."""
        return list(cls._skills.keys())

    @classmethod
    def unload_skill(cls, name: str) -> bool:
        """Unload a skill."""
        if name in cls._skills:
            # Unregister tools
            skill = cls._skills[name]
            for tool in skill.tools:
                ToolRegistry.unregister(tool.name)
            del cls._skills[name]
            return True
        return False

    @classmethod
    def reload_skill(cls, name: str) -> Optional[Skill]:
        """Reload a skill module."""
        if name in cls._skills:
            skill = cls._skills[name]
            module_path = skill.module_path

            # Unload first
            cls.unload_skill(name)

            # Force reload
            if module_path in sys.modules:
                importlib.reload(sys.modules[module_path])

            # Load again
            return cls.load_skill(module_path, name)
        return None

    @classmethod
    def execute_skill_tool(cls, skill_name: str, tool_name: str, **kwargs) -> Any:
        """
        Execute a tool from a specific skill.

        Args:
            skill_name: Name of the skill
            tool_name: Name of the tool within the skill
            **kwargs: Arguments to pass to the tool

        Returns:
            Tool execution result
        """
        skill = cls.get_skill(skill_name)
        if not skill:
            raise ValueError(f"Skill '{skill_name}' not found")

        tool = skill.get_tool(tool_name)
        if not tool:
            raise ValueError(f"Tool '{tool_name}' not found in skill '{skill_name}'")

        return tool.func(**kwargs)

    @classmethod
    def list_skills(cls) -> str:
        """List all loaded skills."""
        output = "Loaded Skills:\n"
        for name, skill in cls._skills.items():
            output += f"\n  Skill: {name}\n"
            output += f"    Description: {skill.description}\n"
            output += f"    Tools: {', '.join(skill.get_tool_names())}\n"
        return output


def skill(name: Optional[str] = None, description: Optional[str] = None):
    """
    Decorator for skill functions.

    Registers the function as a tool within a skill context.
    """
    def decorator(func: Callable) -> Callable:
        # Use tool decorator internally
        return tool(name=name, description=description)(func)
    return decorator
