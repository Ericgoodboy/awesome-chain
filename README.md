# Awesome Chain - LangChain Framework

A powerful Python-based framework built on LangChain that supports:

- **Autonomous Tool Calling**: LLM agents can intelligently select and use tools
- **File Reading**: Built-in file handling capabilities
- **Skill Invocation**: Dynamic skill loading and execution

## Project Structure

```
awesome-chain/
├── src/
│   ├── awesome_chain/
│   │   ├── __init__.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── agent.py          # Main agent implementation
│   │   │   ├── tool_registry.py   # Tool registration system
│   │   │   └── skill_manager.py   # Skill loading and management
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   ├── file_tools.py      # File reading/writing tools
│   │   │   ├── web_tools.py       # Web search/fetch tools
│   │   │   └── base_tools.py      # Base tool definitions
│   │   └── skills/
│   │       ├── __init__.py
│   │       └── examples/
│   │           ├── __init__.py
│   │           ├── data_analysis.py
│   │           └── code_review.py
├── examples/
│   ├── basic_agent.py
│   ├── custom_tools.py
│   └── skill_usage.py
├── data/
│   └── samples/
│       └── example.txt
├── config/
│   └── settings.py
├── tests/
│   ├── __init__.py
│   └── test_agent.py
├── requirements.txt
├── .env.example
└── README.md
```

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run basic example:**
   ```bash
   python examples/basic_agent.py
   ```

## CLI Usage

The framework includes a powerful CLI for quick access:

```bash
# Start in interactive mode (default)
python run.py

# Or use the full CLI
python cli.py

# Run a single command
python cli.py --run "Read file data/samples/example.txt"

# List available tools
python cli.py --list-tools

# List available skills
python cli.py --list-skills

# Load and use a specific skill
python cli.py --skill awesome_chain.skills.examples.data_analysis \
              --run "Analyze the example file"

# Use a custom model
python cli.py --model gpt-4 --temperature 0.5

# Show intermediate reasoning steps
python cli.py --run "Your question here" --steps

# Save output to file
python cli.py --run "Your question" -o output.txt
```

**Interactive Commands:** When in interactive mode, you can use:
- `exit` / `quit` - Exit the program
- `clear` - Clear conversation history
- `tools` - List all available tools
- `skills` - List all loaded skills

## Usage Examples

### Basic Agent

```python
from src.awesome_chain.core.agent import Agent

agent = Agent()
result = agent.run("Read file data/samples/example.txt and summarize it")
print(result)
```

### Custom Tools

```python
from src.awesome_chain.core.tool_registry import ToolRegistry
from src.awesome_chain.tools.base_tools import CustomTool

@CustomTool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression"""
    return eval(expression)

ToolRegistry.register(calculate)
```

### Skill Usage

```python
from src.awesome_chain.core.skill_manager import SkillManager

# Load a skill
skill = SkillManager.load_skill("skills.examples.data_analysis")
result = agent.run_with_skill(
    "Analyze the CSV file",
    skill=skill
)
```

## Features

### Tool System
- Dynamic tool registration
- Automatic tool discovery
- Type-safe tool definitions
- Async tool support

### Skill Framework
- Modular skill packages
- Hot-reload capability
- Skill chaining
- Context sharing

### Agent Capabilities
- Multi-turn conversations
- Memory management
- Tool orchestration
- Error recovery

## License

MIT
