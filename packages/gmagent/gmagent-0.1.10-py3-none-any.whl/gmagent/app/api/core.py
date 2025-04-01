"""Core API implementation shared between FastAPI and MCP servers."""

import os
import uuid
import subprocess
import asyncio
import re
from concurrent.futures import ThreadPoolExecutor
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, cast, Callable, TypeVar

import gm.api as gm_api
import pandas as pd
from fastapi import HTTPException

from ..config import settings

logger = logging.getLogger(__name__)

# Define type aliases for better readability
ApiResponse = Any  # Using Any for flexibility with the GM API responses

T = TypeVar("T")


class GMAPICore:
    """Core API implementation for GM API endpoints."""

    _executor = ThreadPoolExecutor(max_workers=10)

    def __init__(self) -> None:
        """Initialize the GM API client and ensure strategy directory exists."""
        # Initialize GM API with token and server address from settings
        self.token = settings.GM_TOKEN
        self.strategy_id = settings.STRATEGY_ID
        serv_addr = settings.GM_SERV_ADDR

        if self.token:
            try:
                gm_api.set_token(self.token)
            except Exception as e:
                print(f"Warning: Failed to set GM API token: {str(e)}")

        try:
            gm_api.set_serv_addr(serv_addr)
        except Exception as e:
            print(f"Warning: Failed to set GM API server address: {str(e)}")

        # Ensure strategy directory exists
        self.strategy_path = Path(settings.STRATEGY_PATH)
        try:
            self.strategy_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Strategy directory initialized at: {self.strategy_path}")
        except Exception as e:
            logger.error(f"Failed to create strategy directory: {str(e)}")
            raise RuntimeError(f"Failed to create strategy directory: {str(e)}")

    def _preprocess_strategy_code(self, code: str) -> str:
        """Preprocess strategy code by replacing strategy_id and token placeholders.

        Args:
            code: The original strategy code.

        Returns:
            str: Processed strategy code with replaced strategy_id and token.
        """
        # Replace strategy_id placeholder
        code = code.replace("your_strategy_id", self.strategy_id)

        # Replace token placeholder if we have a token
        if self.token:
            code = code.replace("your_token", self.token)

        return code

    async def run_in_thread(
        self, func: Callable[..., T], *args: Any, **kwargs: Any
    ) -> T:
        """
        Run a function in a separate thread and return the result.

        Args:
            func: The function to run.
            *args: Positional arguments to pass to the function.
            **kwargs: Keyword arguments to pass to the function.

        Returns:
            The result of the function call.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, lambda: func(*args, **kwargs))

    async def get_current_price(self, symbol: str) -> ApiResponse:
        """Get current price for a symbol.

        Args:
            symbol: The stock symbol to query.

        Returns:
            Current price information, either as a dictionary or a list of dictionaries.
        """
        try:
            result = gm_api.current(symbol)
            if isinstance(result, pd.DataFrame):
                # Convert DataFrame to records
                result = result.to_dict(orient="records")
                # If empty, return empty dict
                if not result:
                    return {}
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_daily_history(
        self, symbol: str, start_date: str, end_date: str
    ) -> ApiResponse:
        """Get daily price history for a symbol.

        Args:
            symbol: The stock symbol to query.
            start_date: Start date in format YYYY-MM-DD.
            end_date: End date in format YYYY-MM-DD.

        Returns:
            Daily price history as a list of dictionaries or a dictionary.
        """
        try:
            result = gm_api.history(
                symbol=symbol, frequency="1d", start_time=start_date, end_time=end_date
            )
            if isinstance(result, pd.DataFrame):
                result = result.to_dict(orient="records")
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_minute_history(
        self, symbol: str, start_time: str, end_time: str
    ) -> ApiResponse:
        """Get minute price history for a symbol.

        Args:
            symbol: The stock symbol to query.
            start_time: Start time in format YYYY-MM-DD HH:MM:SS.
            end_time: End time in format YYYY-MM-DD HH:MM:SS.

        Returns:
            Minute price history as a list of dictionaries or a dictionary.
        """
        try:
            result = gm_api.history(
                symbol=symbol, frequency="1m", start_time=start_time, end_time=end_time
            )
            if isinstance(result, pd.DataFrame):
                result = result.to_dict(orient="records")
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_sector_category(
        self, sector_type: Optional[str] = None
    ) -> ApiResponse:
        """Get sector category information.

        Args:
            sector_type: Optional sector type filter.

        Returns:
            Sector category information as a list of dictionaries or a dictionary.
        """
        try:
            params = {}
            if sector_type is not None:
                params["sector_type"] = sector_type

            result = gm_api.stk_get_sector_category(**params)
            if isinstance(result, pd.DataFrame):
                result = result.to_dict(orient="records")
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_sector_constituents(self, category_id: str) -> ApiResponse:
        """Get sector constituents.

        Args:
            category_id: The category ID to query.

        Returns:
            Sector constituents as a list of dictionaries or a dictionary.
        """
        try:
            result = gm_api.stk_get_sector_constituents(category_id)
            if isinstance(result, pd.DataFrame):
                result = result.to_dict(orient="records")
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_symbol_sector(
        self, symbol: str, sector_type: Optional[str] = None
    ) -> ApiResponse:
        """Get sector information for a symbol.

        Args:
            symbol: The stock symbol to query.
            sector_type: Optional sector type filter.

        Returns:
            Symbol sector information as a list of dictionaries or a dictionary.
        """
        try:
            params = {}
            if sector_type is not None:
                params["sector_type"] = sector_type

            result = gm_api.stk_get_symbol_sector(symbol, **params)

            if isinstance(result, pd.DataFrame):
                result = result.to_dict(orient="records")
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_symbols(
        self,
        sec_type1: int,
        sec_type2: int = 0,
        exchanges: Optional[Union[str, List[str]]] = None,
        symbols: Optional[Union[str, List[str]]] = None,
        skip_suspended: bool = True,
        skip_st: bool = True,
        trade_date: str = "",
    ) -> List[Dict[str, Any]]:
        """Get a list of available symbols.

        Args:
            sec_type1: Primary security type (integer code).
            sec_type2: Secondary security type (integer code), default is 0 for all.
            exchanges: Optional exchange(s) to filter (string or list).
            symbols: Optional symbol(s) to filter (string or list).
            skip_suspended: Whether to skip suspended securities.
            skip_st: Whether to skip ST securities.
            trade_date: Optional trade date in format YYYY-MM-DD.

        Returns:
            List of symbols as dictionaries.
        """
        try:
            # Handle the case where exchanges or symbols is None
            exch_param = exchanges if exchanges is not None else None
            sym_param = symbols if symbols is not None else None

            result = await self.run_in_thread(
                gm_api.get_symbols,
                sec_type1=sec_type1,
                sec_type2=sec_type2,
                exchanges=exch_param,
                symbols=sym_param,
                skip_suspended=skip_suspended,
                skip_st=skip_st,
                trade_date=trade_date,
            )
            # Convert DataFrame to dict if result is DataFrame
            if isinstance(result, pd.DataFrame):
                return result.to_dict("records")
            return cast(List[Dict[str, Any]], result)
        except Exception as e:
            logger.error(f"Error getting symbols: {str(e)}")
            return []

    async def get_symbol_infos(self, symbols: List[str]) -> List[Dict[str, Any]]:
        """
        Get detailed information for specified symbols.

        Args:
            symbols: List of symbols to query.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries with detailed symbol information.
        """
        try:
            result = await self.run_in_thread(
                gm_api.get_symbol_infos,
                sec_type1=1,  # Default to stocks
                symbols=symbols,
            )
            # Convert DataFrame to dict if result is DataFrame
            if isinstance(result, pd.DataFrame):
                return cast(List[Dict[str, Any]], result.to_dict("records"))
            return cast(List[Dict[str, Any]], result)
        except Exception as e:
            logger.error(f"Error getting symbol infos: {str(e)}")
            return []

    async def run_strategy(self, code: str) -> Dict[str, Any]:
        """Run a trading strategy.

        Args:
            code: The Python code for the strategy.

        Returns:
            Strategy execution result as a dictionary.
        """
        try:
            # Preprocess the strategy code
            processed_code = self._preprocess_strategy_code(code)

            # Add UTF-8 encoding declaration at the beginning of the file
            processed_code = "# -*- coding: utf-8 -*-\n" + processed_code

            # Create a temporary file to write the strategy code in the configured directory
            tmp_file = self.strategy_path / f"strategy_{self.strategy_id}.py"
            with open(tmp_file, "w", encoding="utf-8") as f:
                f.write(processed_code)

            # Execute the strategy code in a subprocess
            process = subprocess.run(
                ["python", str(tmp_file)], capture_output=True, text=True, check=False
            )

            # Clean up the temporary file
            # if tmp_file.exists():
            #     tmp_file.unlink()

            # Check if the process was successful
            if process.returncode == 0:
                return {
                    "strategy_id": self.strategy_id,
                    "success": True,
                    "output": process.stdout,
                    "error": process.stderr,
                }
            else:
                return {
                    "strategy_id": self.strategy_id,
                    "success": False,
                    "output": process.stdout,
                    "error": process.stderr,
                    "code": processed_code,
                    "returncode": process.returncode,
                }
        except Exception as e:
            return {
                "strategy_id": self.strategy_id,
                "success": False,
                "output": "",
                "error": str(e),
                "code": code,
                "returncode": -1,
            }


# Create a singleton instance of the core API
gm_api_core = GMAPICore()
