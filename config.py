"""
Configuration settings for the agentic website development system.
"""
import os
from typing import Dict, Any

# Browser Configuration
BROWSER_CONFIG = {
    "headless": True,
}

# Server Configuration
SERVER_PORT = 5000
SERVER_HOST = "localhost"
SERVER_TIMEOUT = 10.0

# Testing Configuration
MAX_TEST_ITERATIONS = 3
MAX_AGENT_STEPS = 5

# LLM Configuration
DEFAULT_MODEL = "gpt-4o"

# Load environment variables from .env file if available
def get_env_var(name: str, default: Any = None) -> Any:
    """Get environment variable or return default value."""
    return os.environ.get(name, default)

# LLM API keys should be set in environment variables
OPENAI_API_KEY = get_env_var("OPENAI_API_KEY") 