"""
Awesome Chain - A LangChain-based framework
for autonomous AI agents with tool calling,
file reading, and skill invocation capabilities.
"""

__version__ = "1.0.0"
__author__ = "Awesome Team"

from src.awesome_chain.core.agent import Agent
from src.awesome_chain.core.tool_registry import ToolRegistry
from src.awesome_chain.core.skill_manager import SkillManager

__all__ = [
    "Agent",
    "ToolRegistry",
    "SkillManager",
]
