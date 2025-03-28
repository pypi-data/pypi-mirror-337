"""FastAPI server implementation for GM API endpoints."""

from typing import Any, Dict, List, Optional, Union
import datetime

from fastapi import FastAPI, HTTPException, Query, Body, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.api.core import gm_api_core
from app.config import settings

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for accessing GM trading functionality",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(f"{settings.API_V1_STR}/current_time")
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


@app.get(f"{settings.API_V1_STR}/current_price")
async def get_current_price(
    symbol: str = Query(..., description="Stock symbol")
) -> Any:
    """Get current price for a symbol."""
    return await gm_api_core.get_current_price(symbol)


@app.get(f"{settings.API_V1_STR}/daily_history")
async def get_daily_history(
    symbol: str = Query(..., description="Stock symbol"),
    start_date: str = Query(..., description="Start date in format YYYY-MM-DD"),
    end_date: str = Query(..., description="End date in format YYYY-MM-DD"),
) -> Any:
    """Get daily price history for a symbol."""
    return await gm_api_core.get_daily_history(symbol, start_date, end_date)


@app.get(f"{settings.API_V1_STR}/minute_history")
async def get_minute_history(
    symbol: str = Query(..., description="Stock symbol"),
    start_time: str = Query(
        ..., description="Start time in format YYYY-MM-DD HH:MM:SS"
    ),
    end_time: str = Query(..., description="End time in format YYYY-MM-DD HH:MM:SS"),
) -> Any:
    """Get minute price history for a symbol."""
    return await gm_api_core.get_minute_history(symbol, start_time, end_time)


@app.get(f"{settings.API_V1_STR}/sector/category")
async def get_sector_category(
    sector_type: Optional[str] = Query(None, description="Optional sector type filter")
) -> Any:
    """Get sector category information."""
    return await gm_api_core.get_sector_category(sector_type)


@app.get(f"{settings.API_V1_STR}/sector/constituents")
async def get_sector_constituents(
    category_id: str = Query(..., description="Sector category ID")
) -> Any:
    """Get sector constituents."""
    return await gm_api_core.get_sector_constituents(category_id)


@app.get(f"{settings.API_V1_STR}/symbol/sector")
async def get_symbol_sector(
    symbol: str = Query(..., description="Stock symbol"),
    sector_type: Optional[str] = Query(None, description="Optional sector type filter"),
) -> Any:
    """Get sector information for a symbol."""
    return await gm_api_core.get_symbol_sector(symbol, sector_type)


class StrategyRequest(BaseModel):
    """Request model for strategy execution."""

    code: str


@app.post(f"{settings.API_V1_STR}/strategy/run")
async def run_strategy(request: StrategyRequest = Body(...)) -> Dict[str, Any]:
    """Run a trading strategy."""
    return await gm_api_core.run_strategy(request.code)


@app.get(f"{settings.API_V1_STR}/symbols")
async def get_symbols(
    sec_type1: int = Query(..., description="Primary security type code"),
    sec_type2: int = Query(0, description="Secondary security type code"),
    exchanges: Optional[str] = Query(
        None, description="Exchange(s) to filter, comma-separated"
    ),
    symbols: Optional[str] = Query(
        None, description="Symbol(s) to filter, comma-separated"
    ),
    skip_suspended: bool = Query(True, description="Skip suspended securities"),
    skip_st: bool = Query(True, description="Skip ST securities"),
    trade_date: str = Query("", description="Trade date in format YYYY-MM-DD"),
) -> Any:
    """Get a list of available symbols."""
    # Convert comma-separated strings to lists if provided
    exchanges_list = (
        exchanges.split(",") if exchanges and "," in exchanges else exchanges
    )
    symbols_list = symbols.split(",") if symbols and "," in symbols else symbols

    return await gm_api_core.get_symbols(
        sec_type1=sec_type1,
        sec_type2=sec_type2,
        exchanges=exchanges_list,
        symbols=symbols_list,
        skip_suspended=skip_suspended,
        skip_st=skip_st,
        trade_date=trade_date,
    )


@app.get(f"{settings.API_V1_STR}/symbol_infos")
async def get_symbol_infos(
    symbols: str = Query(..., description="Symbol(s) to query, comma-separated")
) -> Any:
    """Get detailed information for specified symbols."""
    # Convert comma-separated string to list
    symbols_list = symbols.split(",")
    return await gm_api_core.get_symbol_infos(symbols=symbols_list)
