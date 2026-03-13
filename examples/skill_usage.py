"""
Skill Usage Example

Demonstrates how to create, load, and use skills in Awesome Chain.
"""

import sys
sys.path.insert(0, '.')

from src.awesome_chain import Agent, SkillManager
from src.awesome_chain.core.tool_registry import tool
from src.awesome_chain.core.skill_manager import skill


def main():
    """Run the skill usage example."""
    print("=" * 70)
    print("Awesome Chain - Skill Usage Example")
    print("=" * 70)
    print()

    # Create agent
    agent = Agent(verbose=True, use_anthropic=False)

    # Example 1: Using built-in skills
    print("\n" + "=" * 70)
    print("Example 1: Loading built-in data_analysis skill")
    print("=" * 70)

    # Load skill
    data_skill = SkillManager.load_skill(
        "awesome_chain.skills.examples.data_analysis",
        name="data_analysis"
    )

    print(f"Loaded skill: {data_skill.name}")
    print(f"Description: {data_skill.description}")
    print(f"Available tools: {', '.join(data_skill.get_tool_names())}")
    print()

    result = agent.run(
        "Using the data_analysis skill tools, analyze the text file at data/samples/example.txt"
    )
    print(f"\nAgent Response:\n{result}")

    # Example 2: Using code_review skill
    print("\n" + "=" * 70)
    print("Example 2: Loading built-in code_review skill")
    print("=" * 70)

    code_skill = SkillManager.load_skill(
        "awesome_chain.skills.examples.code_review",
        name="code_review"
    )

    print(f"Loaded skill: {code_skill.name}")
    print(f"Tools: {', '.join(code_skill.get_tool_names())}")
    print()

    sample_code = """
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    left = [x for x in arr[1:] if x <= pivot]
    right = [x for x in arr[1:] if x > pivot]
    return quicksort(left) + [pivot] + quicksort(right)
"""
    result = agent.run(f"Use the analyze_code tool from code_review skill to analyze:\n{sample_code}")
    print(f"\nAgent Response:\n{result}")

    # Example 3: Creating a custom skill dynamically
    print("\n" + "=" * 70)
    print("Example 3: Creating and loading a custom skill dynamically")
    print("=" * 70)

    # Write a custom skill file
    import os
    custom_skill_content = '''
"""
Custom Analytics Skill
Provides analytics and reporting tools.
"""

SKILL_METADATA = {
    "version": "1.0.0",
    "author": "Custom User",
    "tags": ["analytics", "reports"]
}

from src.awesome_chain.core.tool_registry import tool
import json
from datetime import datetime


@tool
def generate_report(title: str, data: str) -> str:
    """
    Generate a formatted report.

    Args:
        title: Report title
        data: Report data (JSON string)

    Returns:
        Formatted report
    """
    try:
        parsed_data = json.loads(data)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report = f"""
{'='*60}
{title}
{'='*60}
Generated: {timestamp}

SUMMARY:
- Total Items: {len(parsed_data) if isinstance(parsed_data, list) else parsed_data.get('count', 'N/A')}

DETAILS:
{json.dumps(parsed_data, indent=2)}

END OF REPORT
{'='*60}
"""
        return report.strip()
    except Exception as e:
        return f"Error generating report: {str(e)}"


@tool
def calculate_trend(values: str) -> str:
    """
    Calculate trend analysis for a series of values.

    Args:
        values: JSON array of numbers

    Returns:
        Trend analysis
    """
    try:
        nums = json.loads(values)
        if not nums:
            return "No data provided"

        first = nums[0]
        last = nums[-1]
        change = last - first
        percent = (change / first * 100) if first != 0 else 0

        trend = "increasing" if change > 0 else "decreasing" if change < 0 else "stable"

        return json.dumps({
            "first_value": first,
            "last_value": last,
            "absolute_change": round(change, 2),
            "percent_change": round(percent, 2),
            "trend": trend
        }, indent=2)
    except Exception as e:
        return f"Error calculating trend: {str(e)}"
'''

    # Save custom skill
    skills_dir = "src/awesome_chain/skills/examples"
    os.makedirs(skills_dir, exist_ok=True)
    custom_skill_path = os.path.join(skills_dir, "custom_analytics.py")

    with open(custom_skill_path, 'w') as f:
        f.write(custom_skill_content)

    print(f"Created custom skill at: {custom_skill_path}")

    # Load the custom skill
    custom_skill = SkillManager.load_skill(
        "awesome_chain.skills.examples.custom_analytics",
        name="custom_analytics"
    )

    print(f"Loaded custom skill: {custom_skill.name}")
    print(f"Metadata: {custom_skill.metadata}")
    print(f"Tools: {', '.join(custom_skill.get_tool_names())}")
    print()

    # Use the custom skill
    report_data = json.dumps({"sales": [100, 150, 200, 175, 250]})
    result = agent.run(f"""
    Use the calculate_trend tool from custom_analytics skill to analyze this data: {report_data}
    Then use generate_report to create a report titled "Sales Analysis Report"
    """)
    print(f"\nAgent Response:\n{result}")

    # Example 4: List all loaded skills
    print("\n" + "=" * 70)
    print("Example 4: All loaded skills")
    print("=" * 70)
    print(SkillManager.list_skills())

    # Example 5: Unload and reload skill
    print("\n" + "=" * 70)
    print("Example 5: Reloading a skill")
    print("=" * 70)

    SkillManager.unload_skill("data_analysis")
    print("Unloaded data_analysis skill")

    reloaded = SkillManager.reload_skill("data_analysis")
    if reloaded:
        print(f"Reloaded skill: {reloaded.name}")

    # Example 6: Execute tool directly from skill
    print("\n" + "=" * 70)
    print("Example 6: Direct tool execution from skill")
    print("=" * 70)

    skill_result = SkillManager.execute_skill_tool(
        skill_name="data_analysis",
        tool_name="calculate_stats",
        data_stream="10, 20, 30, 40, 50, 60, 70, 80, 90, 100"
    )
    print(f"Direct execution result:\n{skill_result}")

    print("\n" + "=" * 70)
    print("Skill usage example completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
