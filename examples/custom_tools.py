"""
Custom Tools Example

Demonstrates how to create and register custom tools.
"""

import sys
sys.path.insert(0, '.')

from src.awesome_chain import Agent
from src.awesome_chain.core.tool_registry import tool
from src.awesome_chain.tools.base_tools import ToolGroup, create_tool


def main():
    """Run the custom tools example."""
    print("=" * 60)
    print("Awesome Chain - Custom Tools Example")
    print("=" * 60)
    print()

    # Method 1: Using @tool decorator
    @tool
    def calculate(expression: str) -> str:
        """
        Calculate a mathematical expression safely.

        Args:
            expression: Mathematical expression (e.g., "2 + 3 * 4")

        Returns:
            Calculation result
        """
        try:
            # Safe evaluation - limited operators
            allowed = {'+', '-', '*', '/', '(', ')', '.', ' '}
            if not all(c in '0123456789+-*/(). ' for c in expression):
                return "Error: Only basic arithmetic operators are allowed"

            result = eval(expression)
            return f"Result: {result}"
        except Exception as e:
            return f"Error: {str(e)}"

    @tool
    def convert_temperature(value: str, from_unit: str = "C", to_unit: str = "F") -> str:
        """
        Convert temperature between Celsius, Fahrenheit, and Kelvin.

        Args:
            value: Temperature value
            from_unit: Source unit (C, F, or K)
            to_unit: Target unit (C, F, or K)

        Returns:
            Converted temperature
        """
        try:
            temp = float(value)

            # Convert to Celsius first
            if from_unit.upper() == "F":
                celsius = (temp - 32) * 5 / 9
            elif from_unit.upper() == "K":
                celsius = temp - 273.15
            else:
                celsius = temp

            # Convert from Celsius to target
            if to_unit.upper() == "F":
                result = celsius * 9 / 5 + 32
            elif to_unit.upper() == "K":
                result = celsius + 273.15
            else:
                result = celsius

            return f"{temp}°{from_unit.upper()} = {round(result, 2)}°{to_unit.upper()}"
        except Exception as e:
            return f"Error: {str(e)}"

    # Method 2: Using ToolGroup for related tools
    math_group = ToolGroup("math")

    def area_circle(radius: float) -> str:
        """Calculate area of a circle."""
        return f"Area = {round(3.14159 * radius ** 2, 4)}"

    def area_rectangle(width: float, height: float) -> str:
        """Calculate area of a rectangle."""
        return f"Area = {round(width * height, 4)}"

    def area_triangle(base: float, height: float) -> str:
        """Calculate area of a triangle."""
        return f"Area = {round(0.5 * base * height, 4)}"

    math_group.add("circle_area", "Calculate area of a circle given radius", area_circle)
    math_group.add("rect_area", "Calculate area of a rectangle", area_rectangle)
    math_group.add("tri_area", "Calculate area of a triangle", area_triangle)

    # Method 3: Using create_tool function
    def reverse_string(text: str) -> str:
        """Reverse a string."""
        return f"Reversed: {text[::-1]}"

    create_tool(
        name="reverse",
        description="Reverse a string",
        func=reverse_string
    )

    print("Registered custom tools:")
    print("  - calculate: Calculate mathematical expressions")
    print("  - convert_temperature: Convert temperatures")
    print("  - math.circle_area: Calculate circle area")
    print("  - math.rect_area: Calculate rectangle area")
    print("  - math.tri_area: Calculate triangle area")
    print("  - reverse: Reverse a string")
    print()

    # Create agent and use custom tools
    agent = Agent(verbose=True, use_anthropic=False)

    # Test each tool
    print("\n" + "=" * 60)
    print("Testing calculate tool")
    print("=" * 60)
    result = agent.run("Use the calculate tool to compute: 123 * 456 + 789")
    print(f"\n{result}")

    print("\n" + "=" * 60)
    print("Testing convert_temperature tool")
    print("=" * 60)
    result = agent.run("Convert 100 degrees Celsius to Fahrenheit")
    print(f"\n{result}")

    print("\n" + "=" * 60)
    print("Testing math.circle_area tool")
    print("=" * 60)
    result = agent.run("Calculate the area of a circle with radius 5")
    print(f"\n{result}")

    print("\n" + "=" * 60)
    print("Testing reverse tool")
    print("=" * 60)
    result = agent.run("Use the reverse tool to reverse: Hello World")
    print(f"\n{result}")

    # Complex example
    print("\n" + "=" * 60)
    print("Complex Example: Multiple tool usage")
    print("=" * 60)
    result = agent.run("""
    Please help me with these calculations:
    1. What is 25 * 4 + 100?
    2. What's the area of a rectangle with width 10 and height 6?
    3. Reverse the result from question 1
    """)
    print(f"\n{result}")

    print("\n" + "=" * 60)
    print("Custom tools example completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
