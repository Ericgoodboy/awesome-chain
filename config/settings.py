"""
Configuration settings for Awesome Chain.
"""

import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()


class Settings:
    """Application settings."""

    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

    # Anthropic Configuration
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")

    # Model Settings
    MODEL_NAME: str = os.getenv("MODEL_NAME", "deepseek-chat")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "4096"))  # Increased for better responses

    # Path Settings
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR: str = os.path.join(BASE_DIR, "data")
    SAMPLES_DIR: str = os.path.join(DATA_DIR, "samples")
    SKILLS_DIR: str = os.path.join(BASE_DIR, "src", "awesome_chain", "skills")

    # Vector Store
    CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", os.path.join(DATA_DIR, "chroma"))

    @classmethod
    def validate(cls) -> bool:
        """Validate required settings."""
        if not cls.OPENAI_API_KEY and not cls.ANTHROPIC_API_KEY:
            print("Warning: No API key found. Set OPENAI_API_KEY or ANTHROPIC_API_KEY.")
            return False
        return True


# Global settings instance
settings = Settings()
