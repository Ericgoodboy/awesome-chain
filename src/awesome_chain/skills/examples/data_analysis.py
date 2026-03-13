"""
Data Analysis Skill

Provides tools for analyzing and processing data files.
Can perform statistical calculations on numerical data.
"""

SKILL_METADATA = {
    "version": "1.0.0",
    "author": "Awesome Team",
    "tags": ["data", "analysis", "statistics"]
}

import re
from src.awesome_chain.core.tool_registry import tool
from src.awesome_chain.tools.file_tools import read_file


@tool
def calculate_stats(data_stream: str) -> str:
    """
    Calculate basic statistics from numeric data.

    Args:
        data_stream: String containing numbers (comma or space separated)

    Returns:
        Statistics including mean, median, min, max
    """
    try:
        # Extract numbers from the data
        numbers = []
        for match in re.finditer(r'-?\d+\.?\d*', data_stream):
            numbers.append(float(match.group()))

        if not numbers:
            return "No numeric data found"

        numbers.sort()
        count = len(numbers)
        mean = sum(numbers) / count
        median = numbers[count // 2] if count % 2 == 1 else (numbers[count // 2 - 1] + numbers[count // 2]) / 2
        minimum = numbers[0]
        maximum = numbers[-1]

        result = {
            "count": count,
            "mean": round(mean, 2),
            "median": round(median, 2),
            "min": round(minimum, 2),
            "max": round(maximum, 2),
            "range": round(maximum - minimum, 2)
        }

        import json
        return json.dumps(result, indent=2)

    except Exception as e:
        return f"Error calculating statistics: {str(e)}"


@tool
def analyze_text_file(file_path: str) -> str:
    """
    Analyze a text file and provide statistics.

    Args:
        file_path: Path to the text file

    Returns:
        File statistics
    """
    try:
        content = read_file(file_path)

        if content.startswith("Error"):
            return content

        # Calculate statistics
        lines = content.split('\n')
        words = content.split()
        chars = len(content)
        chars_no_spaces = len(content.replace(' ', '').replace('\t', '').replace('\n', ''))

        stats = {
            "file": file_path,
            "lines": len(lines),
            "words": len(words),
            "characters": chars,
            "characters_no_spaces": chars_no_spaces,
            "avg_line_length": round(chars / len(lines), 2) if lines else 0,
            "empty_lines": sum(1 for line in lines if not line.strip())
        }

        import json
        return json.dumps(stats, indent=2)

    except Exception as e:
        return f"Error analyzing text file: {str(e)}"


@tool
def find_patterns(text: str, pattern: str) -> str:
    """
    Find all occurrences of a regex pattern in text.

    Args:
        text: Text to search
        pattern: Regular expression pattern

    Returns:
        List of matches
    """
    try:
        matches = re.findall(pattern, text)
        import json
        return json.dumps({
            "pattern": pattern,
            "match_count": len(matches),
            "matches": matches[:20]  # Limit to first 20
        }, indent=2)
    except Exception as e:
        return f"Error finding patterns: {str(e)}"
