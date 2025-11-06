"""Configuration management for MCP Webex Calling Server"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


def find_env_file() -> str:
    """Find the .env file relative to the project root"""
    # Get the directory where this module is located
    current_file = Path(__file__).resolve()
    # Go up to the project root (mcp_webexcalling -> project root)
    project_root = current_file.parent.parent
    env_file = project_root / ".env"
    return str(env_file)


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    webex_access_token: str
    webex_base_url: str = "https://webexapis.com/v1"

    model_config = SettingsConfigDict(
        env_file=find_env_file(),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        # Environment variables take precedence over .env file
        # Field names are automatically converted to uppercase for env vars
        # e.g., webex_access_token -> WEBEX_ACCESS_TOKEN
    )


def _read_token_from_env_file() -> str | None:
    """Read WEBEX_ACCESS_TOKEN directly from .env file, ignoring environment variables"""
    env_file_path = find_env_file()
    if not os.path.exists(env_file_path):
        return None
    
    with open(env_file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key.upper() == 'WEBEX_ACCESS_TOKEN' and value:
                    return value
    return None


def get_settings() -> Settings:
    """Get application settings - always reads token from .env file"""
    # Temporarily remove WEBEX_ACCESS_TOKEN from environment so .env file is used
    original_token = os.environ.pop("WEBEX_ACCESS_TOKEN", None)
    
    try:
        # Read token directly from .env file
        token_from_file = _read_token_from_env_file()
        
        if token_from_file:
            # Set it in environment so Settings can pick it up
            os.environ["WEBEX_ACCESS_TOKEN"] = token_from_file
        
        # Load settings (will use .env file or the token we just set)
        settings = Settings()
        
        # If token is still missing, that's an error
        if not settings.webex_access_token:
            raise ValueError(
                f"WEBEX_ACCESS_TOKEN not found in .env file at {find_env_file()}. "
                f"Please add WEBEX_ACCESS_TOKEN=your_token to the .env file."
            )
        
    finally:
        # Restore original env var if it existed (though we prefer .env file)
        # Actually, don't restore - we want to use .env file value
        pass
    
    return settings

