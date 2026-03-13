"""
Main Agent implementation for autonomous tool calling and skill invocation.
"""

import os
from typing import Optional, List, Dict, Any

from langchain_classic.agents import create_react_agent, AgentExecutor, create_tool_calling_agent
from langchain_openai import ChatOpenAI
# from langchain.agents import AgentExecutor, create_tool_calling_agent, create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.callbacks import BaseCallbackHandler

from config.settings import settings
from src.awesome_chain.core.tool_registry import ToolRegistry
from src.awesome_chain.core.skill_manager import SkillManager


# ReAct template for better model compatibility
REACT_PROMPT = PromptTemplate.from_template("""You are a helpful AI assistant with access to various tools.

Available tools:
{tools}

Tool names: {tool_names}

IMPORTANT: You MUST use tools when appropriate. For example:
- Use 'read_file' to read any file the user asks about
- Use 'list_files' to see what files are available
- Use 'write_file' to create or modify files
- Use 'calculate_stats' or 'analyze_text_file' for data analysis tasks

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}""")


class ThinkingCallbackHandler(BaseCallbackHandler):
    """Custom callback handler for displaying agent thinking process."""

    def __init__(self):
        self.step = 0

    def on_agent_action(self, action, **kwargs) -> Any:
        """Called when agent performs an action."""
        self.step += 1
        print(f"\n[Step {self.step}] Agent Action:")
        print(f"  Tool: {action.tool}")
        print(f"  Input: {action.tool_input}")
        return super().on_agent_action(action, **kwargs)

    def on_tool_end(self, output, **kwargs) -> Any:
        """Called when tool finishes."""
        print(f"  Output: {str(output)[:200]}...")
        return super().on_tool_end(output, **kwargs)


class Agent:
    """
    Main agent class for autonomous AI operations.

    Supports:
    - Tool calling with LangChain agents
    - File reading capabilities
    - Skill invocation
    - Multi-turn conversations
    """

    def __init__(
        self,
        model_name: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        verbose: bool = True,
        use_anthropic: bool = False,
        force_react: bool = False
    ):
        """
        Initialize the agent.

        Args:
            model_name: Model to use (default: from settings)
            temperature: Sampling temperature
            max_tokens: Maximum response tokens
            verbose: Enable verbose output
            use_anthropic: Use Anthropic instead of OpenAI
            force_react: Force using ReAct agent instead of function calling
        """
        settings.validate()

        self.model_name = model_name or settings.MODEL_NAME
        self.temperature = temperature or settings.TEMPERATURE
        self.max_tokens = max_tokens or settings.MAX_TOKENS
        self.verbose = verbose
        self.use_anthropic = use_anthropic
        self.force_react = force_react

        # Determine if we should use ReAct based on model
        model_lower = self.model_name.lower()
        self.use_react = self.force_react or any(
            x in model_lower for x in ["glm", "qwen", "deepseek", "llama", "mistral"]
        )

        # Initialize LLM
        self.llm = self._init_llm()

        # Initialize conversation history
        self.chat_history: List = []
        self._setup_default_tools()

    def _init_llm(self):
        """Initialize the language model."""
        # Check if model name indicates we need special handling
        model_name_lower = self.model_name.lower()

        return ChatOpenAI(
            model=self.model_name,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            openai_api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL,
            model_kwargs={
                # Add model-specific settings if needed
                "response_format": {"type": "text"}
            },
            timeout=60.0,
            max_retries=2
        )

    def _setup_default_tools(self):
        """Set up default tools."""
        self.custom_tools: List = ToolRegistry.get_all()

    def add_tool(self, tool) -> None:
        """Add a custom tool to the agent."""
        self.custom_tools.append(tool)

    def load_skill(self, skill_name: str, module_path: Optional[str] = None) -> None:
        """
        Load a skill and integrate its tools.

        Args:
            skill_name: Name of the skill
            module_path: Optional module path (if None, searches skills directory)
        """
        if module_path:
            skill = SkillManager.load_skill(module_path, skill_name)
        else:
            # Auto-discover skill
            from config.settings import settings
            SkillManager.set_skills_dir(settings.SKILLS_DIR)
            skill_file = os.path.join(settings.SKILLS_DIR, "examples", f"{skill_name}.py")
            module_path = f"awesome_chain.skills.examples.{skill_name}"
            skill = SkillManager.load_skill(module_path, skill_name)

        # Add skill tools to agent
        for tool in skill.tools:
            if tool not in self.custom_tools:
                self.custom_tools.append(tool)

        print(f"Loaded skill: {skill_name} with {len(skill.tools)} tools")

    def get_prompt_template(self) -> ChatPromptTemplate:
        """Get the prompt template for the agent."""
        return ChatPromptTemplate.from_messages([
            ("system", self._get_system_prompt()),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the agent."""
        tool_list = ", ".join([t.name for t in self.custom_tools])
        return f"""You are a helpful AI assistant with access to various tools.

Available tools: {tool_list}

IMPORTANT INSTRUCTIONS:
1. ALWAYS use the appropriate tools when possible - don't guess when you can use a tool
2. When a user asks to read a file, ALWAYS use the 'read_file' tool
3. When a user asks to analyze data or calculate statistics, use the 'calculate_stats' tool
4. When a user asks to list files, use the 'list_files' tool
5. After using tools, always provide a summary of what you found

You MUST use tools for:
- Reading files (use read_file)
- Listing directories (use list_files)
- Calculations (use calculate_stats if data_analysis skill is loaded)
- Any task where a tool can provide accurate information

Only respond without using tools for:
- General conversation
- Questions about code/logic
- Simple queries unrelated to files or data

When reading files, provide a summary of the contents.
When writing files, be careful not to overwrite important data."""

    def run(self, input_text: str, return_intermediate: bool = False) -> str:
        """
        Run the agent with the given input.

        Args:
            input_text: User input/prompt
            return_intermediate: Return intermediate steps

        Returns:
            Agent response
        """
        try:
            # Create agent based on mode
            if self.use_react:
                # Use ReAct agent for better compatibility
                agent = create_react_agent(self.llm, self.custom_tools, REACT_PROMPT)
                agent_executor = AgentExecutor(
                    agent=agent,
                    tools=self.custom_tools,
                    verbose=self.verbose,
                    handle_parsing_errors="Check your output",
                    max_iterations=15,
                    callbacks=[ThinkingCallbackHandler()] if self.verbose else [],
                    max_execution_time=300
                )

                result = agent_executor.invoke({"input": input_text})
                output = result.get("output", "")
            else:
                # Use tool calling agent
                prompt = self.get_prompt_template()
                agent = create_tool_calling_agent(self.llm, self.custom_tools, prompt)
                agent_executor = AgentExecutor(
                    agent=agent,
                    tools=self.custom_tools,
                    verbose=self.verbose,
                    handle_parsing_errors=True,
                    max_iterations=15,
                    chat_history=self.chat_history,
                    callbacks=[ThinkingCallbackHandler()] if self.verbose else [],
                    return_intermediate_steps=return_intermediate,
                    max_execution_time=300
                )

                result = agent_executor.invoke({
                    "input": input_text,
                    "chat_history": self.chat_history
                })
                output = result.get("output", "")

            # Update conversation history
            self.chat_history.append(HumanMessage(content=input_text))
            self.chat_history.append(AIMessage(content=output))

            if return_intermediate and not self.use_react:
                intermediate_steps = result.get("intermediate_steps", [])
                return {
                    "output": output,
                    "intermediate_steps": intermediate_steps
                }
            elif return_intermediate:
                # For ReAct, format intermediate steps
                intermediate_steps = result.get("intermediate_steps", [])
                return {
                    "output": output,
                    "intermediate_steps": intermediate_steps
                }

            return output

        except Exception as e:
            import traceback
            error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
            if self.verbose:
                print(f"\n{error_msg}")
            return f"Error: {str(e)}"

    def run_with_skill(
        self,
        input_text: str,
        skill_name: str,
        return_intermediate: bool = False
    ) -> str:
        """
        Run the agent with a specific skill loaded.

        Args:
            input_text: User input/prompt
            skill_name: Name of the skill to use
            return_intermediate: Return intermediate steps

        Returns:
            Agent response
        """
        # Load skill
        self.load_skill(skill_name)
        return self.run(input_text, return_intermediate=return_intermediate)

    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.chat_history.clear()

    def get_chat_history(self) -> List:
        """Get the chat history."""
        return self.chat_history.copy()

    async def arun(self, input_text: str) -> str:
        """Async version of run."""
        prompt = self.get_prompt_template()
        agent = create_tool_calling_agent(self.llm, self.custom_tools, prompt)

        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.custom_tools,
            verbose=self.verbose,
        )

        result = await agent_executor.ainvoke({
            "input": input_text,
            "chat_history": self.chat_history
        })

        return result["output"]

    def set_model(self, model_name: str) -> None:
        """Change the model."""
        self.model_name = model_name
        self.llm = self._init_llm()

    def list_available_tools(self) -> str:
        """List all available tools."""
        return ToolRegistry.list_tools()

    def list_available_skills(self) -> str:
        """List all available skills."""
        return SkillManager.list_skills()
