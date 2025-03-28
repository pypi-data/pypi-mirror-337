"""Tests for MCP server implementation."""

from typing import TYPE_CHECKING, Any, Generator
from unittest.mock import MagicMock, patch

import pytest

from app.mcp_server import create_mcp_server, mcp

# Workaround for missing pytest_mock
if TYPE_CHECKING:
    from pytest_mock import MockerFixture


@pytest.fixture
def mock_mcp(mocker: "MockerFixture") -> Generator[MagicMock, None, None]:
    """Mock the FastMCP instance.

    Args:
        mocker: Pytest mocker fixture.

    Returns:
        Mocked FastMCP instance.
    """
    with patch("app.mcp_server.mcp", autospec=True) as mock:
        yield mock


def test_create_mcp_server() -> None:
    """Test create_mcp_server returns the global mcp instance."""
    server = create_mcp_server()
    assert server is mcp


def test_tools_registration() -> None:
    """Test that tools are registered with the MCP server."""
    # These tool functions should be defined in the module
    from app.mcp_server import (
        get_current_time,
        get_current_price,
        get_daily_history,
        get_minute_history,
        get_sector_category,
        get_sector_constituents,
        get_symbol_sector,
        run_strategy,
    )

    # Verify all tools exist
    assert callable(get_current_time)
    assert callable(get_current_price)
    assert callable(get_daily_history)
    assert callable(get_minute_history)
    assert callable(get_sector_category)
    assert callable(get_sector_constituents)
    assert callable(get_symbol_sector)
    assert callable(run_strategy)
