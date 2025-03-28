"""Test configuration."""

import os
import pytest
from typing import Any, Generator

from fastapi.testclient import TestClient
from app.config import settings
from app.fastapi_server import app


@pytest.fixture
def client() -> Generator[TestClient, Any, None]:
    """Create a FastAPI test client.

    Returns:
        Generator yielding a FastAPI test client.
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session", autouse=True)
def test_env() -> Generator[None, None, None]:
    """Set up test environment with test settings.

    This fixture runs automatically for all tests and sets
    test-specific environment variables.

    Yields:
        None
    """
    # Store original settings
    original_token = settings.GM_TOKEN
    original_serv_addr = settings.GM_SERV_ADDR

    # Set test values
    os.environ["GM_TOKEN"] = "test_token"
    os.environ["GM_SERV_ADDR"] = "test.api.gmquant.cn:7001"

    # Force settings reload
    from app.config import Settings

    test_settings = Settings()

    # Update the global settings instance
    settings.GM_TOKEN = test_settings.GM_TOKEN
    settings.GM_SERV_ADDR = test_settings.GM_SERV_ADDR

    yield

    # Restore original settings
    settings.GM_TOKEN = original_token
    settings.GM_SERV_ADDR = original_serv_addr

    # Clean up environment variables
    if "GM_TOKEN" in os.environ:
        del os.environ["GM_TOKEN"]
    if "GM_SERV_ADDR" in os.environ:
        del os.environ["GM_SERV_ADDR"]
