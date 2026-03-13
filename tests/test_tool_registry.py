"""
Tests for the ToolRegistry class.
"""

import unittest
import sys
sys.path.insert(0, '.')

from src.awesome_chain.core.tool_registry import ToolRegistry


class TestToolRegistryGet(unittest.TestCase):
    """Test cases for ToolRegistry.get() method."""

    def setUp(self):
        """Set up test fixtures."""
        self.tool_name = "test_get_tool"
        self.tool_description = "A test tool for get() method."
        
        # Ensure registry is clean before each test
        ToolRegistry.clear()
        
        # Register a test tool
        @ToolRegistry.register
        def test_get_tool(value: str) -> str:
            """A test tool for get() method."""
            return f"Result: {value}"

    def tearDown(self):
        """Clean up after each test."""
        ToolRegistry.clear()

    def test_get_existing_tool(self):
        """Test getting an existing tool by name."""
        tool = ToolRegistry.get(self.tool_name)
        
        self.assertIsNotNone(tool)
        self.assertEqual(tool.name, self.tool_name)
        self.assertEqual(tool.description, self.tool_description)

    def test_get_nonexistent_tool(self):
        """Test getting a tool that doesn't exist."""
        tool = ToolRegistry.get("nonexistent_tool")
        
        self.assertIsNone(tool)

    def test_get_tool_after_registration(self):
        """Test getting a tool immediately after registration."""
        new_tool_name = "newly_registered_tool"
        
        # Register a new tool
        @ToolRegistry.register
        def newly_registered_tool(x: int) -> int:
            """A newly registered tool."""
            return x * 2
        
        # Try to get the newly registered tool
        tool = ToolRegistry.get(new_tool_name)
        
        self.assertIsNotNone(tool)
        self.assertEqual(tool.name, new_tool_name)

    def test_get_tool_after_unregistration(self):
        """Test getting a tool after it has been unregistered."""
        # First verify tool exists
        tool = ToolRegistry.get(self.tool_name)
        self.assertIsNotNone(tool)
        
        # Unregister the tool
        ToolRegistry.unregister(self.tool_name)
        
        # Try to get the unregistered tool
        tool = ToolRegistry.get(self.tool_name)
        self.assertIsNone(tool)

    def test_get_multiple_tools_by_name(self):
        """Test getting multiple different tools by name."""
        tool_names = ["tool_alpha", "tool_beta", "tool_gamma"]
        
        # Register multiple tools
        @ToolRegistry.register
        def tool_alpha() -> str:
            """Alpha tool."""
            return "alpha"
        
        @ToolRegistry.register
        def tool_beta() -> str:
            """Beta tool."""
            return "beta"
        
        @ToolRegistry.register
        def tool_gamma() -> str:
            """Gamma tool."""
            return "gamma"
        
        # Verify each tool can be retrieved by name
        for tool_name in tool_names:
            tool = ToolRegistry.get(tool_name)
            self.assertIsNotNone(tool, f"Tool '{tool_name}' should exist")
            self.assertEqual(tool.name, tool_name)

    def test_get_returns_structured_tool(self):
        """Test that get() returns a StructuredTool instance."""
        from langchain_core.tools import StructuredTool
        
        tool = ToolRegistry.get(self.tool_name)
        
        self.assertIsInstance(tool, StructuredTool)

    def test_get_with_empty_registry(self):
        """Test getting a tool from an empty registry."""
        # Clear all tools
        ToolRegistry.clear()
        
        # Try to get any tool
        tool = ToolRegistry.get("any_tool")
        self.assertIsNone(tool)


if __name__ == '__main__':
    unittest.main()
