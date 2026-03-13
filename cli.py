#!/usr/bin/env python3
"""
Awesome Chain CLI

Command-line interface for Awesome Chain framework.
"""

import argparse
import sys
from typing import Optional

sys.path.insert(0, '.')
from src.awesome_chain import Agent, ToolRegistry, SkillManager


# Windows-safe print function
def safe_print(text: str) -> None:
    """Print text safely, handling encoding issues."""
    try:
        print(text)
    except UnicodeEncodeError:
        # Fallback for Windows terminal encoding issues
        print(text.encode('gbk', errors='ignore').decode('gbk', errors='ignore'))


def interactive_mode(agent: Agent, model: str) -> None:
    """Run agent in interactive mode."""
    safe_print("=" * 60)
    safe_print("Awesome Chain - Interactive Mode")
    safe_print("Type 'exit' or 'quit' to exit, 'clear' to clear history")
    safe_print(f"Model: {model}")
    safe_print(f"Agent Mode: {'ReAct' if agent.use_react else 'Tool Calling'}")
    safe_print("=" * 60)
    safe_print("")

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() in ['exit', 'quit']:
                safe_print("\nGoodbye!")
                break

            if user_input.lower() == 'clear':
                agent.clear_history()
                safe_print("History cleared.")
                continue

            if user_input.lower() == 'tools':
                safe_print("\n" + "-" * 60)
                safe_print(agent.list_available_tools())
                safe_print("-" * 60)
                continue

            if user_input.lower() == 'skills':
                safe_print("\n" + "-" * 60)
                safe_print(agent.list_available_skills())
                safe_print("-" * 60)
                continue

            if user_input.lower() == 'mode':
                safe_print(f"\nCurrent mode: {'ReAct' if agent.use_react else 'Tool Calling'}")
                continue

            if not user_input:
                continue

            result = agent.run(user_input)
            safe_print(f"\nAgent: {result}")

        except KeyboardInterrupt:
            safe_print("\n\nUse 'exit' or 'quit' to exit.")
        except Exception as e:
            safe_print(f"\nError: {e}")


def run_command(agent: Agent, prompt: str, return_intermediate: bool = False) -> None:
    """Run a single command."""
    if return_intermediate:
        result = agent.run(prompt, return_intermediate=True)
        safe_print("\nOutput:")
        safe_print(result.get("output", ""))

        steps = result.get("intermediate_steps", [])
        if steps:
            safe_print("\nIntermediate Steps:")
            for i, (action, observation) in enumerate(steps, 1):
                safe_print(f"\n  Step {i}:")
                safe_print(f"    Tool: {action.tool}")
                safe_print(f"    Input: {action.tool_input}")
                safe_print(f"    Output: {str(observation)[:200]}...")
    else:
        result = agent.run(prompt)
        safe_print("\n" + result)


def list_tools() -> None:
    """List all available tools."""
    safe_print("\n" + "=" * 60)
    safe_print("Available Tools")
    safe_print("=" * 60)
    safe_print(ToolRegistry.list_tools())


def list_skills() -> None:
    """List all available skills."""
    safe_print("\n" + "=" * 60)
    safe_print("Available Skills")
    safe_print("=" * 60)
    safe_print(SkillManager.list_skills())


def load_skill(agent: Agent, skill_path: str, name: Optional[str] = None) -> None:
    """Load a skill."""
    try:
        skill = SkillManager.load_skill(skill_path, name)
        safe_print(f"\nLoaded skill: {skill.name}")
        safe_print(f"  Description: {skill.description}")
        safe_print(f"  Tools: {', '.join(skill.get_tool_names())}")
    except Exception as e:
        safe_print(f"\nError loading skill: {e}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Awesome Chain - LangChain-based AI Agent Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (default)
  python cli.py

  # Run with custom model
  python cli.py --model gpt-4

  # Run a single command
  python cli.py --run "Read file data/samples/example.txt，并分析内容"

  # Use ReAct mode (recommended for GLM/Qwen models)
  python cli.py --react --run "Read file data/samples/example.txt"

  # List tools
  python cli.py --list-tools

  # Load and use a skill
  python cli.py --skill awesome_chain.skills.examples.data_analysis --run "Analyze data/samples/example.txt"
        """
    )

    # Agent options
    parser.add_argument(
        "--model", "-m",
        default="glm-4.7-fp8",
        help="Model to use (default: glm-4.7-fp8)"
    )
    parser.add_argument(
        "--temperature", "-t",
        type=float,
        default=0.7,
        help="Sampling temperature (default: 0.7)"
    )
    parser.add_argument(
        "--anthropic",
        action="store_true",
        help="Use Anthropic instead of OpenAI"
    )
    parser.add_argument(
        "--react",
        action="store_true",
        help="Force using ReAct agent (better compatibility with GLM/Qwen models)"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Quiet mode (less verbose output)"
    )

    # Action options
    action_group = parser.add_mutually_exclusive_group()
    action_group.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Interactive mode (default)"
    )
    action_group.add_argument(
        "--run", "-r",
        help="Run a single command"
    )
    action_group.add_argument(
        "--list-tools",
        action="store_true",
        help="List all available tools"
    )
    action_group.add_argument(
        "--list-skills",
        action="store_true",
        help="List all available skills"
    )

    # Skill options
    parser.add_argument(
        "--skill", "-s",
        action="append",
        help="Load a skill (can be used multiple times)"
    )

    # Output options
    parser.add_argument(
        "--steps",
        action="store_true",
        help="Show intermediate steps"
    )
    parser.add_argument(
        "--output", "-o",
        help="Write output to file"
    )

    args = parser.parse_args()

    # Create agent
    agent = Agent(
        model_name=args.model,
        temperature=args.temperature,
        verbose=not args.quiet,
        use_anthropic=args.anthropic,
        force_react=args.react
    )

    # Load skills
    if args.skill:
        for skill_spec in args.skill:
            parts = skill_spec.split(":", 1)
            if len(parts) == 2:
                skill_path, skill_name = parts
            else:
                skill_path = parts[0]
                skill_name = None
            load_skill(agent, skill_path, skill_name)

    # Execute action
    output = None

    if args.list_tools:
        list_tools()
        return

    if args.list_skills:
        list_skills()
        return

    if args.run:
        output = run_command(agent, args.run, return_intermediate=args.steps)
    else:
        interactive_mode(agent, args.model)

    # Write output to file if specified
    if args.output and output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(str(output))
        safe_print(f"\nOutput written to {args.output}")


if __name__ == "__main__":
    main()
