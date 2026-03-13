"""
Code Review Skill

Provides tools for code analysis and review.
Supports basic code quality checks and complexity analysis.
"""

SKILL_METADATA = {
    "version": "1.0.0",
    "author": "Awesome Team",
    "tags": ["code", "review", "quality"]
}

import re
from src.awesome_chain.core.tool_registry import tool


@tool
def analyze_code(code: str, language: str = "python") -> str:
    """
    Analyze code for basic quality metrics.

    Args:
        code: Source code to analyze
        language: Programming language (python, javascript, etc.)

    Returns:
        Code analysis results
    """
    lines = code.split('\n')

    # Basic metrics
    total_lines = len(lines)
    non_empty_lines = [line for line in lines if line.strip()]
    code_lines = [line for line in non_empty_lines if not line.strip().startswith('#')]
    comment_lines = [line for line in non_empty_lines if line.strip().startswith('#')]

    # Indentation analysis
    avg_indent = 0
    if code_lines:
        indents = []
        for line in code_lines:
            match = re.match(r'^(\s+)', line)
            if match:
                indents.append(len(match.group(1)))
        avg_indent = round(sum(indents) / len(indents), 2) if indents else 0

    # Function/class detection
    functions = len(re.findall(r'def\s+\w+\s*\(', code))
    classes = len(re.findall(r'class\s+\w+', code))

    # Complexity estimation (very basic)
    complexity = functions + classes + len(re.findall(r'\bif\b|\bfor\b|\bwhile\b', code))

    result = {
        "file": "<inline code>",
        "language": language,
        "total_lines": total_lines,
        "code_lines": len(code_lines),
        "comment_lines": len(comment_lines),
        "empty_lines": total_lines - len(non_empty_lines),
        "functions": functions,
        "classes": classes,
        "average_indent": avg_indent,
        "estimated_complexity": complexity,
        "code_to_comment_ratio": round(len(code_lines) / max(len(comment_lines), 1), 2)
    }

    # Simple recommendations
    recommendations = []
    if result["code_to_comment_ratio"] > 10:
        recommendations.append("Consider adding more comments for better documentation")
    if avg_indent > 8:
        recommendations.append("Deep nesting detected - consider refactoring")
    if complexity > 50:
        recommendations.append("High complexity detected - consider modularizing code")

    result["recommendations"] = recommendations

    import json
    return json.dumps(result, indent=2)


@tool
def check_style(code: str) -> str:
    """
    Perform basic style checks on code.

    Args:
        code: Source code to check

    Returns:
        Style issues found
    """
    issues = []

    lines = code.split('\n')
    for i, line in enumerate(lines, 1):
        # Check for long lines
        if len(line) > 100 and len(line.strip()) > 0:
            issues.append(f"Line {i}: Line exceeds 100 characters")

        # Check for trailing whitespace
        if line.rstrip() != line.rstrip('\n\r') and len(line.strip()) > 0:
            issues.append(f"Line {i}: Trailing whitespace")

        # Check for mixed tabs and spaces
        if '\t' in line and '  ' in line:
            issues.append(f"Line {i}: Mixed tabs and spaces")

    import json
    return json.dumps({
        "total_issues": len(issues),
        "issues": issues[:50]  # Limit to first 50
    }, indent=2)


@tool
def extract_structure(code: str) -> str:
    """
    Extract the structure of code (functions, classes, imports).

    Args:
        code: Source code to analyze

    Returns:
        Code structure
    """
    structure = {
        "imports": [],
        "classes": [],
        "functions": []
    }

    # Extract imports
    for match in re.finditer(r'^import\s+([^\n]+)|^from\s+([^\s]+)\s+import', code, re.MULTILINE):
        imports = match.group(1) or match.group(2)
        structure["imports"].append(imports.strip())

    # Extract classes
    for match in re.finditer(r'class\s+(\w+)\s*(?:\([^)]*\))?\s*:', code):
        structure["classes"].append({
            "name": match.group(1),
            "line": code[:match.start()].count('\n') + 1
        })

    # Extract functions
    for match in re.finditer(r'def\s+(\w+)\s*\([^)]*\)\s*(?:->\s*[^\s:]+)?\s*:', code):
        structure["functions"].append({
            "name": match.group(1),
            "line": code[:match.start()].count('\n') + 1
        })

    import json
    return json.dumps(structure, indent=2)
