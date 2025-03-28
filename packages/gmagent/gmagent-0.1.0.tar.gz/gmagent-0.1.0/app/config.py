"""Application configuration.

This module provides a single source of configuration for the entire application.
"""

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings.

    Attributes:
        GM_TOKEN: GM API token.
        GM_SERV_ADDR: GM API server address.
        API_V1_STR: API version prefix.
        PROJECT_NAME: Project name used in API documentation.
        DEBUG: Enable debug mode.
        STRATEGIES_DIR: Directory for storing strategy files.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # GM API settings
    GM_TOKEN: Optional[str] = None
    GM_SERV_ADDR: str = "http://127.0.0.1:7001"

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "GM Agent API"
    DEBUG: bool = False

    # File storage settings
    STRATEGIES_DIR: str = "strategies"


# Create a singleton instance of settings to be imported elsewhere
settings = Settings()
