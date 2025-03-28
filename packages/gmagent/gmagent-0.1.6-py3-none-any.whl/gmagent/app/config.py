"""Application configuration.

This module provides a single source of configuration for the entire application.
"""

import os
import platform
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


def get_default_strategy_path() -> str:
    """Get the default strategy path based on the operating system.

    Returns:
        str: Default path for storing strategy files.
    """
    if platform.system() == "Windows":
        return str(Path.home() / "tmp")
    return "/tmp"


class Settings(BaseSettings):
    """Application settings.

    Attributes:
        GM_TOKEN: GM API token.
        GM_SERV_ADDR: GM API server address.
        API_V1_STR: API version prefix.
        PROJECT_NAME: Project name used in API documentation.
        DEBUG: Enable debug mode.
        STRATEGY_PATH: Directory for storing strategy files.
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
    STRATEGY_PATH: str = get_default_strategy_path()


# Create a singleton instance of settings to be imported elsewhere
settings = Settings()
