"""
Basic Agent Example

Demonstrates the core functionality of Awesome Chain:
- Tool calling
- File reading
- Multi-turn conversations
"""

import sys
sys.path.insert(0, '.')

from src.awesome_chain import Agent
from src.awesome_chain.core.tool_registry import tool


def main():
    """Run the basic agent example."""
    print("=" * 60)
    print("Awesome Chain - Basic Agent Example")
    print("=" * 60)
    print()

    # Create agent
    agent = Agent(verbose=True, use_anthropic=False)

    # List available tools
    print("Available Tools:")
    print(agent.list_available_tools())
    print()

    # Example 1: File reading
    print("\n" + "=" * 60)
    print("Example 1: Reading a file")
    print("=" * 60)
    result = agent.run("Read the file data/samples/example.txt")
    print(f"\nAgent Response:\n{result}")

    # Example 2: File statistics with skill
    print("\n" + "=" * 60)
    print("Example 2: Using data_analysis skill")
    print("=" * 60)

    # Load skill
    agent.load_skill("data_analysis", "awesome_chain.skills.examples.data_analysis")
    print()

    result = agent.run("Use the analyze_text_file tool to analyze data/samples/example.txt")
    print(f"\nAgent Response:\n{result}")

    # Example 3: List files
    print("\n" + "=" * 60)
    print("Example 3: List files in data directory")
    print("=" * 60)
    result = agent.run("List all files in the data/samples directory")
    print(f"\nAgent Response:\n{result}")

    # Example 4: Search files
    print("\n" + "=" * 60)
    print("Example 4: Search for .txt files")
    print("=" * 60)
    result = agent.run("Search for all .txt files in the data directory")
    print(f"\nAgent Response:\n{result}")

    # Example 5: Code review with skill
    print("\n" + "=" * 60)
    print("Example 5: Using code_review skill")
    print("=" * 60)

    # Load code review skill
    agent.load_skill("code_review", "awesome_chain.skills.examples.code_review")
    print()

    code = """
def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

for i in range(10):
    print(fibonacci(i))
"""
    result = agent.run(f"Analyze this code using the analyze_code tool:\n{code}")
    print(f"\nAgent Response:\n{result}")

    # Example 6: Multi-turn conversation
    print("\n" + "=" * 60)
    print("Example 6: Multi-turn conversation")
    print("=" * 60)
    print()

    # First turn
    agent.clear_history()
    result1 = agent.run("What files are in the data/samples directory?")
    print(f"\nQ: What files are in the data/samples directory?")
    print(f"A: {result1}")

    # Second turn (has context from first)
    result2 = agent.run("Summarize the content of example.txt")
    print(f"\nQ: Summarize the content of example.txt")
    print(f"A: {result2}")

    print("\n" + "=" * 60)
    print("Example completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
