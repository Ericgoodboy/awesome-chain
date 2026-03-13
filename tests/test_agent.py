"""
Tests for the Agent class.
"""

import unittest
import sys
sys.path.insert(0, '.')

from src.awesome_chain import Agent, ToolRegistry, SkillManager


class TestAgent(unittest.TestCase):
    """Test cases for Agent."""

    def setUp(self):
        """Set up test fixtures."""
        self.agent = Agent(verbose=False, use_anthropic=False)

    def test_agent_initialization(self):
        """Test agent initializes correctly."""
        self.assertIsNotNone(self.agent.llm)
        self.assertEqual(len(self.agent.chat_history), 0)
        self.assertGreater(len(self.agent.custom_tools), 0)

    def test_list_tools(self):
        """Test listing available tools."""
        tools = self.agent.list_available_tools()
        self.assertIn("read_file", tools)

    def test_clear_history(self):
        """Test clearing chat history."""
        self.agent.chat_history.append("test")
        self.agent.clear_history()
        self.assertEqual(len(self.agent.chat_history), 0)


class TestToolRegistry(unittest.TestCase):
    """Test cases for ToolRegistry."""

    def test_register_tool(self):
        """Test registering a custom tool."""
        @ToolRegistry.register
        def test_tool(value: str) -> str:
            """A test tool."""
            return f"Test: {value}"

        self.assertIn("test_tool", ToolRegistry.get_names())

        ToolRegistry.unregister("test_tool")

    def test_get_tool(self):
        """Test getting a tool by name."""
        tool = ToolRegistry.get("read_file")
        self.assertIsNotNone(tool)
        self.assertEqual(tool.name, "read_file")

    def test_unregister_tool(self):
        """Test unregistering a tool."""
        # First create a temp tool
        @ToolRegistry.register
        def temp_tool(x: str) -> str:
            return x

        result = ToolRegistry.unregister("temp_tool")
        self.assertTrue(result)
        self.assertNotIn("temp_tool", ToolRegistry.get_names())

        # Try to unregister non-existent tool
        result = ToolRegistry.unregister("non_existent")
        self.assertFalse(result)


class TestSkillManager(unittest.TestCase):
    """Test cases for SkillManager."""

    def test_load_builtin_skill(self):
        """Test loading a built-in skill."""
        skill = SkillManager.load_skill(
            "awesome_chain.skills.examples.data_analysis",
            name="data_analysis"
        )
        self.assertEqual(skill.name, "data_analysis")
        self.assertGreater(len(skill.tools), 0)

    def test_get_skill_names(self):
        """Test getting all skill names."""
        SkillManager.load_skill(
            "awesome_chain.skills.examples.code_review",
            name="code_review"
        )
        names = SkillManager.get_skill_names()
        self.assertIsInstance(names, list)
        self.assertIn("code_review", names)

    def test_execute_skill_tool(self):
        """Test executing a tool from a skill."""
        results = SkillManager.execute_skill_tool(
            skill_name="data_analysis",
            tool_name="calculate_stats",
            data_stream="1, 2, 3, 4, 5"
        )
        self.assertIn("mean", results)


if __name__ == "__main__":
    unittest.main()
