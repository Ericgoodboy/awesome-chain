# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Awesome Chain is a LangChain-based Python framework for building autonomous AI agents with tool calling and skill invocation capabilities. The framework supports file operations, web search, command execution, and extensible skill modules.

## Common Development Commands

### Environment Setup
```bash
# Create virtual environment (recommended)
python -m venv .venv
# Activate (Windows)
.venv\Scripts\activate
# Activate (Unix)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (black, isort, mypy)
pip install black isort mypy
```

### Running the Agent
```bash
# Interactive mode (default)
python cli.py
python run.py  # shortcut

# Run a single command
python cli.py --run "Read file data/samples/example.txt"

# Use ReAct mode for GLM/Qwen/DeepSeek models
python cli.py --react --run "List files in data directory"

# Specify custom model
python cli.py --model glm-4.7-fp8 --temperature 0.5

# List available tools
python cli.py --list-tools

# List available skills
python cli.py --list-skills

# Load and use a skill
python cli.py --skill awesome_chain.skills.examples.data_analysis --run "Analyze data/samples/example.txt"

# Show intermediate reasoning steps
python cli.py --run "Your question" --steps
```

### Testing
```bash
# Run all tests
python -m unittest discover tests

# Run specific test module
python -m unittest tests.test_agent
python -m unittest tests.test_tool_registry

# Run single test class
python -m unittest tests.test_agent.TestAgent
```

### Code Quality
```bash
# Format code with black
black src/ tests/ examples/

# Sort imports with isort
isort src/ tests/ examples/

# Type checking with mypy
mypy src/
```

### Examples
```bash
# Run basic examples
python examples/basic_agent.py
```

## Architecture

### Core Components

1. **Agent (`src/awesome_chain/core/agent.py`)**: Main agent class that orchestrates tool calling and skill invocation. Uses LangChain's agent frameworks (ReAct or function calling) depending on model compatibility. Maintains conversation history and tool registry.

2. **Tool Registry (`src/awesome_chain/core/tool_registry.py`)**: Global registry for tools. Built-in tools include file operations (`read_file`, `write_file`, `list_files`, `search_files`), web tools (`search_web`, `fetch_url`), and command execution (`execute_command`). Tools are automatically registered on import via `_register_builtins()`.

3. **Skill Manager (`src/awesome_chain/core/skill_manager.py`)**: Dynamic skill loader. Skills are Python modules containing tool functions decorated with `@tool`. Skills can be loaded at runtime and their tools become available to the agent.

4. **Tools (`src/awesome_chain/tools/`)**: Tool implementations. `base_tools.py` provides decorators, `file_tools.py` and `web_tools.py` contain specific tool functions. Tools are registered via the `@tool` decorator or `ToolRegistry.register()`.

5. **Skills (`src/awesome_chain/skills/`)**: Example skills in `examples/` subdirectory. Each skill module defines functions with `@tool` decorator and optional `SKILL_METADATA`. Skills are loaded by module path.

### Key Patterns

- **Tool Registration**: Functions decorated with `@tool` are automatically registered in `ToolRegistry`. Built-in tools register on import of `tool_registry.py`.
- **Skill Loading**: Skills are loaded via `SkillManager.load_skill(module_path)` which discovers tool functions in the module.
- **Agent Modes**: The agent automatically selects ReAct mode for models like GLM, Qwen, DeepSeek, Llama, Mistral (detected by name). Force ReAct with `--react` flag or `force_react=True`.
- **Path Resolution**: Relative file paths are resolved relative to `DATA_DIR` (from `config/settings.py`).
- **Error Handling**: Tool functions return error messages as strings starting with "Error:".
- **Conversation History**: Agent maintains `chat_history` list of LangChain messages.

### Configuration

- **Settings**: `config/settings.py` loads environment variables from `.env` file. Required: `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`. Model defaults to `deepseek-chat`.
- **Data Directory**: `data/` contains sample files. `data/samples/example.txt` is used in examples.
- **Prompt System**: `src/awesome_chain/prompt/` contains prompt templates loaded via `util.load_prompt()`.

### Development Notes

- **Import Paths**: Many files use `sys.path.insert(0, '.')` to allow imports from root. Package structure uses `src/awesome_chain/`.
- **Windows Support**: `cli.py` includes `safe_print()` for encoding issues. `awesome.bat` provides Windows launcher.
- **Model Compatibility**: ReAct mode (`--react`) works better with non-OpenAI models. Tool calling mode works with OpenAI-compatible APIs.
- **Async Support**: Agent has `arun()` method for async execution.
- **Testing**: Tests use `unittest` framework and import modules directly with path modification.