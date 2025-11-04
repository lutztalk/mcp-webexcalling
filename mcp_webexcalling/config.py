"""Configuration management for MCP Webex Calling Server"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Direct access token (optional if using OAuth)
    webex_access_token: Optional[str] = None
    webex_base_url: str = "https://webexapis.com/v1"

    # OAuth credentials (optional if using direct token)
    webex_client_id: Optional[str] = None
    webex_client_secret: Optional[str] = None
    webex_redirect_uri: str = "http://localhost:8080/callback"
    webex_oauth_scope: str = (
        "spark:people_read "
        "spark-admin:locations_read "
        "spark-admin:organizations_read "
        "spark-admin:telephony_config_read "
        "spark-admin:read_call_history"
    )

    # Token storage (for OAuth)
    webex_refresh_token: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    def has_oauth_credentials(self) -> bool:
        """Check if OAuth credentials are configured"""
        return bool(self.webex_client_id and self.webex_client_secret)

    def has_access_token(self) -> bool:
        """Check if access token is available"""
        return bool(self.webex_access_token)


def get_settings() -> Settings:
    """Get application settings"""
    return Settings()

