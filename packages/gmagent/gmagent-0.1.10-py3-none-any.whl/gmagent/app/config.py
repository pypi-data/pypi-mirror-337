"""Application configuration.

This module provides a single source of configuration for the entire application.
"""

import os
import platform
import uuid
from pathlib import Path
from typing import Optional, Any

from pydantic_settings import BaseSettings, SettingsConfigDict


def get_default_strategy_path() -> str:
    """Get the default strategy path based on the operating system.

    Returns:
        str: Default path for storing strategy files.
    """
    if platform.system() == "Windows":
        return str(Path.home() / "tmp")
    return "/tmp"


def generate_strategy_id() -> str:
    """Generate a unique strategy ID.

    Returns:
        str: A unique strategy identifier.
    """
    return str(uuid.uuid4())


class Settings(BaseSettings):
    """Application settings.

    Attributes:
        GM_TOKEN: GM API token.
        GM_SERV_ADDR: GM API server address.
        API_V1_STR: API version prefix.
        PROJECT_NAME: Project name used in API documentation.
        DEBUG: Enable debug mode.
        STRATEGY_PATH: Directory for storing strategy files.
        STRATEGY_ID: Unique identifier for the strategy instance, defaults to UUID if not set.
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
    STRATEGY_ID: str = ""

    def model_post_init(self, _: Any) -> None:
        """Post initialization hook to set default strategy_id if empty."""
        if not self.STRATEGY_ID:
            self.STRATEGY_ID = generate_strategy_id()


# Create a singleton instance of settings to be imported elsewhere
settings = Settings()
