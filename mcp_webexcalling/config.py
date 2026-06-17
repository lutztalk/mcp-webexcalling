"""Configuration management for MCP Webex Calling Server.

Settings are resolved with the following precedence (highest first):

1. Process environment variables (e.g. the ``env`` block in
   ``claude_desktop_config.json``, or ``export WEBEX_ACCESS_TOKEN=...``).
2. A ``.env`` file located at the project root.

This mirrors the behaviour every other tool in the ecosystem expects and
matches what the README/SETUP docs describe. Environment variables win so
that secrets injected by a launcher (Claude Desktop, systemd, Docker, CI)
are always honoured.
"""

from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def find_env_file() -> str:
    """Find the .env file relative to the project root."""
    current_file = Path(__file__).resolve()
    # mcp_webexcalling/ -> project root
    project_root = current_file.parent.parent
    return str(project_root / ".env")


class Settings(BaseSettings):
    """Application settings loaded from environment variables and ``.env``.

    Field names map to upper-cased environment variables, e.g.
    ``webex_access_token`` -> ``WEBEX_ACCESS_TOKEN``.
    """

    # Authentication
    webex_access_token: str = Field(default="")
    webex_base_url: str = Field(default="https://webexapis.com/v1")

    # The analytics/reporting (CDR) APIs live on a different host.
    webex_analytics_base_url: str = Field(
        default="https://analytics.webexapis.com/v1"
    )

    # HTTP behaviour
    webex_request_timeout: float = Field(default=30.0)
    webex_max_retries: int = Field(default=3)
    webex_retry_backoff: float = Field(default=0.5)
    webex_max_connections: int = Field(default=20)

    # Logging: one of CRITICAL/ERROR/WARNING/INFO/DEBUG
    webex_log_level: str = Field(default="INFO")

    model_config = SettingsConfigDict(
        env_file=find_env_file(),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


# Cache the resolved settings so we don't re-read the .env file repeatedly.
_cached_settings: Optional[Settings] = None


def get_settings(require_token: bool = True) -> Settings:
    """Return application settings.

    Resolution order (handled natively by pydantic-settings):
        1. Environment variables
        2. ``.env`` file at the project root
        3. Field defaults

    Args:
        require_token: When True (the default) a clear ``ValueError`` is raised
            if no access token could be resolved. Set to False for callers that
            supply their own credentials and only want the other settings.

    Raises:
        ValueError: If ``require_token`` is True and no token is configured.
    """
    global _cached_settings
    if _cached_settings is None:
        # Settings() never raises for a missing token now (the field has a
        # default of ""), so any error here is a genuine configuration problem.
        _cached_settings = Settings()

    settings = _cached_settings

    if require_token and not settings.webex_access_token:
        raise ValueError(
            "WEBEX_ACCESS_TOKEN is not set. Provide it via an environment "
            "variable (recommended for Claude Desktop's `env` block) or add "
            f"WEBEX_ACCESS_TOKEN=your_token to a .env file at {find_env_file()}."
        )

    return settings


def reset_settings_cache() -> None:
    """Clear the cached settings (useful for tests or config reloads)."""
    global _cached_settings
    _cached_settings = None
