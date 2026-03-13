"""
Skills directory for dynamic skill loading.

A skill is a Python module that:
1. Contains tool functions decorated with @tool
2. Optionally defines SKILL_METADATA dict
3. Has a docstring describing the skill

Example skill structure:
```python
\"\"\"
Data Analysis Skill
Provides tools for analyzing data files.
\"\"\"

from src.awesome_chain.core.tool_registry import tool

SKILL_METADATA = {
    "version": "1.0.0",
    "author": "Team",
    "tags": ["data", "analysis"]
}

@tool
def analyze_csv(file_path: str) -> str:
    '''Analyze a CSV file and return statistics.'''
    # Implementation
    pass
```
"""

from src.awesome_chain.core.skill_manager import SkillManager, skill
