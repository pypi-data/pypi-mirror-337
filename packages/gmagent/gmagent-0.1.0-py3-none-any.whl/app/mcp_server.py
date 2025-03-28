"""MCP server implementation for GM API endpoints using the Model Context Protocol."""

import datetime
import asyncio
from typing import Any, Dict, Optional, List, Union

from mcp.server.fastmcp import FastMCP

from app.api.core import gm_api_core

# Create the FastMCP instance
mcp = FastMCP("GM Trading API")


@mcp.tool()
async def get_current_time() -> Dict[str, Any]:
    """Get the current server time.

    Returns:
        Dictionary containing current timestamp in ISO format and unix timestamp.
    """
    now = datetime.datetime.now()
    now_tz = datetime.datetime.now().astimezone()
    timezone_name = str(now_tz.tzinfo) if now_tz.tzinfo else "UTC"

    return {
        "iso_time": now.isoformat(),
        "unix_timestamp": int(now.timestamp()),
        "timezone": timezone_name,
    }


@mcp.tool()
async def get_current_price(symbol: str) -> Any:
    """Get current price for a symbol.

    Args:
        symbol: The stock symbol to query.

    Returns:
        Current price information, either as a dictionary or a list of dictionaries.
    """
    return await gm_api_core.get_current_price(symbol)


@mcp.tool()
async def get_daily_history(symbol: str, start_date: str, end_date: str) -> Any:
    """Get daily price history for a symbol.

    Args:
        symbol: The stock symbol to query.
        start_date: Start date in format YYYY-MM-DD.
        end_date: End date in format YYYY-MM-DD.

    Returns:
        Daily price history as a list of dictionaries or a dictionary.
    """
    return await gm_api_core.get_daily_history(symbol, start_date, end_date)


@mcp.tool()
async def get_minute_history(symbol: str, start_time: str, end_time: str) -> Any:
    """Get minute price history for a symbol.

    Args:
        symbol: The stock symbol to query.
        start_time: Start time in format YYYY-MM-DD HH:MM:SS.
        end_time: End time in format YYYY-MM-DD HH:MM:SS.

    Returns:
        Minute price history as a list of dictionaries or a dictionary.
    """
    return await gm_api_core.get_minute_history(symbol, start_time, end_time)


@mcp.tool()
async def get_sector_category(sector_type: Optional[str] = None) -> Any:
    """Get sector category information.

    Args:
        sector_type: Optional sector type filter.

    Returns:
        Sector category information as a list of dictionaries or a dictionary.
    """
    return await gm_api_core.get_sector_category(sector_type)


@mcp.tool()
async def get_sector_constituents(category_id: str) -> Any:
    """Get sector constituents.

    Args:
        category_id: The category ID to query.

    Returns:
        Sector constituents as a list of dictionaries or a dictionary.
    """
    return await gm_api_core.get_sector_constituents(category_id)


@mcp.tool()
async def get_symbol_sector(symbol: str) -> Any:
    """
    Get the sector and industry category for a symbol.

    Args:
        symbol: The stock symbol to query.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries with sector information.
    """
    return await gm_api_core.get_symbol_sector(symbol)


@mcp.tool()
async def get_symbols(
    sec_type1: int,
    sec_type2: int = 0,
    exchanges: Optional[Union[str, List[str]]] = None,
    symbols: Optional[Union[str, List[str]]] = None,
    skip_suspended: bool = True,
    skip_st: bool = True,
    trade_date: str = "",
) -> Any:
    """
    Get a list of available symbols.

    Args:
        sec_type1: Primary security type code.
        sec_type2: Secondary security type code.
        exchanges: Exchange(s) to filter.
        symbols: Symbol(s) to filter.
        skip_suspended: Skip suspended securities.
        skip_st: Skip ST securities.
        trade_date: Trade date in format YYYY-MM-DD.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries with symbol information.
    """
    return await gm_api_core.get_symbols(
        sec_type1=sec_type1,
        sec_type2=sec_type2,
        exchanges=exchanges,
        symbols=symbols,
        skip_suspended=skip_suspended,
        skip_st=skip_st,
        trade_date=trade_date,
    )


@mcp.tool()
async def get_symbol_infos(symbols: List[str]) -> Any:
    """
    Get detailed information for specified symbols.

    Args:
        symbols: List of symbols to query.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries with detailed symbol information.
    """
    return await gm_api_core.get_symbol_infos(symbols=symbols)


@mcp.tool()
async def run_strategy(code: str) -> Dict[str, Any]:
    """Run a trading strategy.

    Args:
        code: The Python code for the strategy.

    Returns:
        Strategy execution result as a dictionary.
    """
    return await gm_api_core.run_strategy(code)


def create_mcp_server() -> FastMCP:
    """Create an MCP server instance.

    Returns:
        The FastMCP instance.
    """
    return mcp


# If run directly, start the MCP server
if __name__ == "__main__":
    mcp.run()
