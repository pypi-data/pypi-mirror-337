"""Tests for API endpoints."""

from typing import TYPE_CHECKING, Dict, Any
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, ANY
import pandas as pd

if TYPE_CHECKING:
    from _pytest.fixtures import FixtureRequest
    from pytest_mock import MockerFixture


def test_get_current_price(test_client: TestClient, mocker: "MockerFixture") -> None:
    """Test current price endpoint.

    Args:
        test_client: FastAPI test client.
        mocker: Pytest mocker fixture.
    """
    # Mock GM API response
    mock_response = {"symbol": "SH000001", "price": 3000.0}
    mocker.patch("app.api.core.gm_api.current", return_value=mock_response)

    response = test_client.get("/api/v1/current_price?symbol=SH000001")
    assert response.status_code == 200
    assert response.json() == mock_response


def test_get_daily_history(test_client: TestClient, mocker: "MockerFixture") -> None:
    """Test daily history endpoint.

    Args:
        test_client: FastAPI test client.
        mocker: Pytest mocker fixture.
    """
    # Mock GM API response
    mock_response = [
        {"date": "2024-03-25", "close": 3000.0},
        {"date": "2024-03-26", "close": 3100.0},
    ]
    mocker.patch("app.api.core.gm_api.history", return_value=mock_response)

    response = test_client.get(
        "/api/v1/daily_history",
        params={
            "symbol": "SH000001",
            "start_date": "2024-03-25",
            "end_date": "2024-03-26",
        },
    )
    assert response.status_code == 200
    assert response.json() == mock_response


def test_get_minute_history(test_client: TestClient, mocker: "MockerFixture") -> None:
    """Test minute history endpoint.

    Args:
        test_client: FastAPI test client.
        mocker: Pytest mocker fixture.
    """
    # Mock GM API response
    mock_response = [
        {"time": "2024-03-25 09:30:00", "close": 3000.0},
        {"time": "2024-03-25 09:31:00", "close": 3001.0},
    ]
    mocker.patch("app.api.core.gm_api.history", return_value=mock_response)

    response = test_client.get(
        "/api/v1/minute_history",
        params={
            "symbol": "SH000001",
            "start_time": "2024-03-25 09:30:00",
            "end_time": "2024-03-25 09:31:00",
        },
    )
    assert response.status_code == 200
    assert response.json() == mock_response


def test_get_sector_category(test_client: TestClient, mocker: "MockerFixture") -> None:
    """Test sector category endpoint.

    Args:
        test_client: FastAPI test client.
        mocker: Pytest mocker fixture.
    """
    # Test with list response
    mock_list_response = [
        {"category_id": "S001", "name": "Industry"},
        {"category_id": "S002", "name": "Region"},
    ]
    mock_stk_get_sector_category_list = mocker.patch(
        "app.api.core.gm_api.stk_get_sector_category", return_value=mock_list_response
    )

    # Test without sector_type parameter
    response = test_client.get("/api/v1/sector/category")
    assert response.status_code == 200
    assert response.json() == mock_list_response
    mock_stk_get_sector_category_list.assert_called_with()

    # Test with sector_type parameter
    response = test_client.get("/api/v1/sector/category?sector_type=1001")
    assert response.status_code == 200
    assert response.json() == mock_list_response
    mock_stk_get_sector_category_list.assert_called_with(sector_type="1001")

    # Test with DataFrame response
    mock_df = pd.DataFrame(
        {"category_id": ["S001", "S002"], "name": ["Industry", "Region"]}
    )
    mock_records = mock_df.to_dict(orient="records")
    mock_stk_get_sector_category_df = mocker.patch(
        "app.api.core.gm_api.stk_get_sector_category", return_value=mock_df
    )

    # Test with DataFrame result
    response = test_client.get("/api/v1/sector/category")
    assert response.status_code == 200
    assert response.json() == mock_records
    mock_stk_get_sector_category_df.assert_called_with()


def test_get_sector_constituents(
    test_client: TestClient, mocker: "MockerFixture"
) -> None:
    """Test sector constituents endpoint.

    Args:
        test_client: FastAPI test client.
        mocker: Pytest mocker fixture.
    """
    # Mock GM API response with DataFrame
    mock_df = pd.DataFrame(
        {
            "symbol": ["SH600000", "SZ000001"],
            "name": ["Stock1", "Stock2"],
            "weight": [0.05, 0.03],
        }
    )
    mock_records = mock_df.to_dict(orient="records")
    mocker.patch(
        "app.api.core.gm_api.stk_get_sector_constituents", return_value=mock_df
    )

    response = test_client.get("/api/v1/sector/constituents?category_id=S001")
    assert response.status_code == 200
    assert response.json() == mock_records


def test_get_symbol_sector(test_client: TestClient, mocker: "MockerFixture") -> None:
    """Test symbol sector endpoint.

    Args:
        test_client: FastAPI test client.
        mocker: Pytest mocker fixture.
    """
    # Mock GM API response with DataFrame
    mock_df = pd.DataFrame(
        {"sector_id": ["S001", "S002"], "sector_name": ["Industry1", "Industry2"]}
    )
    mock_records = mock_df.to_dict(orient="records")
    mock_stk_get_symbol_sector = mocker.patch(
        "app.api.core.gm_api.stk_get_symbol_sector", return_value=mock_df
    )

    # Test without sector_type parameter
    response = test_client.get("/api/v1/symbol/sector?symbol=SHSE.600000")
    assert response.status_code == 200
    assert response.json() == mock_records
    mock_stk_get_symbol_sector.assert_called_with("SHSE.600000")

    # Test with sector_type parameter
    response = test_client.get(
        "/api/v1/symbol/sector?symbol=SHSE.600000&sector_type=1003"
    )
    assert response.status_code == 200
    assert response.json() == mock_records
    mock_stk_get_symbol_sector.assert_called_with("SHSE.600000", sector_type="1003")


def test_run_strategy(test_client: TestClient, mocker: "MockerFixture") -> None:
    """Test strategy execution endpoint.

    Args:
        test_client: FastClient: FastAPI test client.
        mocker: Pytest mocker fixture.
    """
    # Mock subprocess.run for success case
    mock_result_success = MagicMock()
    mock_result_success.stdout = "Strategy output"
    mock_result_success.stderr = ""
    mock_result_success.returncode = 0

    # Mock subprocess.run for failure case
    mock_result_failure = MagicMock()
    mock_result_failure.stdout = ""
    mock_result_failure.stderr = "NameError: name 'printf' is not defined"
    mock_result_failure.returncode = 1

    # Create a mock that returns different results based on input
    mock_run = mocker.patch("app.api.core.subprocess.run")

    # Test successful strategy execution
    mock_run.return_value = mock_result_success

    strategy_code_success = """
    from gm.api import *
    set_token("your token")
    print("Strategy running...")
    """

    response = test_client.post(
        "/api/v1/strategy/run",
        json={"code": strategy_code_success},
    )

    assert response.status_code == 200
    result = response.json()
    assert "strategy_id" in result
    assert result["success"] is True
    assert result["output"] == "Strategy output"
    assert result["error"] == ""

    # Test failed strategy execution
    mock_run.return_value = mock_result_failure

    strategy_code_failure = """
    from gm.api import *
    set_token("your token")
    printf("This will fail")
    """

    response = test_client.post(
        "/api/v1/strategy/run",
        json={"code": strategy_code_failure},
    )

    assert response.status_code == 200  # Still returns 200 even with execution error
    result = response.json()
    assert "strategy_id" in result
    assert result["success"] is False
    assert "returncode" in result
    assert result["returncode"] == 1
    assert "NameError" in result["error"]
    assert "code" in result  # Should include the strategy code for debugging


def test_error_handling(test_client: TestClient, mocker: "MockerFixture") -> None:
    """Test error handling for all endpoints.

    Args:
        test_client: FastAPI test client.
        mocker: Pytest mocker fixture.
    """
    # Mock API errors
    mocker.patch("app.api.core.gm_api.current", side_effect=Exception("API Error"))
    mocker.patch("app.api.core.gm_api.history", side_effect=Exception("API Error"))
    mocker.patch(
        "app.api.core.gm_api.stk_get_sector_category",
        side_effect=Exception("API Error"),
    )
    mocker.patch(
        "app.api.core.gm_api.stk_get_sector_constituents",
        side_effect=Exception("API Error"),
    )
    mocker.patch(
        "app.api.core.gm_api.stk_get_symbol_sector", side_effect=Exception("API Error")
    )

    # Test current price endpoint error
    response = test_client.get("/api/v1/current_price?symbol=SH000001")
    assert response.status_code == 500
    assert "API Error" in response.json()["detail"]

    # Test daily history endpoint error
    response = test_client.get(
        "/api/v1/daily_history",
        params={
            "symbol": "SH000001",
            "start_date": "2024-03-25",
            "end_date": "2024-03-26",
        },
    )
    assert response.status_code == 500
    assert "API Error" in response.json()["detail"]

    # Test minute history endpoint error
    response = test_client.get(
        "/api/v1/minute_history",
        params={
            "symbol": "SH000001",
            "start_time": "2024-03-25 09:30:00",
            "end_time": "2024-03-25 09:31:00",
        },
    )
    assert response.status_code == 500
    assert "API Error" in response.json()["detail"]

    # Test sector category endpoint error
    response = test_client.get("/api/v1/sector/category")
    assert response.status_code == 500
    assert "API Error" in response.json()["detail"]

    # Test sector constituents endpoint error
    response = test_client.get("/api/v1/sector/constituents?category_id=S001")
    assert response.status_code == 500
    assert "API Error" in response.json()["detail"]

    # Test symbol sector endpoint error
    response = test_client.get("/api/v1/symbol/sector?symbol=SHSE.600000")
    assert response.status_code == 500
    assert "API Error" in response.json()["detail"]
