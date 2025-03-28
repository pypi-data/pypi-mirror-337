# GM Trading Agent API

A service that provides both REST API and MCP (Model Context Protocol) interfaces to interact with the GM trading API.

## Features

- Current Price: Get the current price of a symbol
- Daily History: Get daily price history of a symbol
- Minute History: Get minute price history of a symbol
- Sector Information: Get sector categories, constituents, and symbol sector
- Strategy Execution: Run trading strategies with Python code

## Architecture

The application has a modular architecture with:

1. **Core API Layer**: Shared implementation of all API functionality
2. **FastAPI Server**: REST API server for web and application clients
3. **MCP Server**: Model Context Protocol server for AI agents like Claude

You can run either the FastAPI server or the MCP server independently, as they both use the same underlying core API implementation.

## Installation

Clone the repository and install the dependencies:

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
```

## Configuration

The application uses a centralized configuration system based on Pydantic Settings. Create a `.env` file in the root directory with the following environment variables:

```
GM_TOKEN=your_gm_token
GM_SERV_ADDR=http://127.0.0.1:8080
```

All settings are defined in `app/config.py` and used throughout the application.

## Usage

### Starting the server

You can run either the FastAPI server or the MCP server:

```bash
# Run the FastAPI server (default)
python main.py

# Run the MCP server
python main.py --server mcp

# Specify host and port (FastAPI only)
python main.py --host 127.0.0.1 --port 9000
```

### REST API Endpoints

When running the FastAPI server, the following endpoints are available:

#### Current Price

```
GET /api/v1/current_price?symbol={symbol}
```

- `symbol`: Stock symbol (e.g., SHSE.000001)

Response:
```json
{
  "price": 10.5,
  "volume": 1000
}
```

#### Daily History

```
GET /api/v1/daily_history?symbol={symbol}&start_date={start_date}&end_date={end_date}
```

- `symbol`: Stock symbol (e.g., SHSE.000001)
- `start_date`: Start date in format YYYY-MM-DD
- `end_date`: End date in format YYYY-MM-DD

Response:
```json
[
  {
    "date": "2023-01-01",
    "open": 10.0,
    "high": 11.0,
    "low": 9.5,
    "close": 10.5,
    "volume": 1000
  }
]
```

#### Minute History

```
GET /api/v1/minute_history?symbol={symbol}&start_time={start_time}&end_time={end_time}
```

- `symbol`: Stock symbol (e.g., SHSE.000001)
- `start_time`: Start time in format YYYY-MM-DD HH:MM:SS
- `end_time`: End time in format YYYY-MM-DD HH:MM:SS

Response:
```json
[
  {
    "time": "2023-01-01 09:30:00",
    "open": 10.0,
    "high": 10.1,
    "low": 9.9,
    "close": 10.0,
    "volume": 100
  }
]
```

#### Sector Category

```
GET /api/v1/sector/category?sector_type={sector_type}
```

- `sector_type`: (Optional) Sector type filter
  - 1001: 市场类
  - 1002: 地域类
  - 1003: 概念类

Response:
```json
[
  {
    "category_id": "S001",
    "name": "Industry"
  }
]
```

#### Sector Constituents

```
GET /api/v1/sector/constituents?category_id={category_id}
```

- `category_id`: Sector category ID

Response:
```json
[
  {
    "symbol": "SHSE.000001",
    "name": "Company Name"
  }
]
```

#### Symbol Sector

```
GET /api/v1/symbol/sector?symbol={symbol}
```

- `symbol`: Stock symbol (e.g., SHSE.000001)

Response:
```json
[
  {
    "category_id": "S001",
    "category_name": "Industry"
  }
]
```

#### Strategy Execution

```
POST /api/v1/strategy/run
```

Request body:
```json
{
  "code": "print('Hello, World!')"
}
```

Response for successful execution:
```json
{
  "strategy_id": "unique_id",
  "success": true,
  "output": "Hello, World!",
  "error": ""
}
```

Response for failed execution:
```json
{
  "strategy_id": "unique_id",
  "success": false,
  "error": "Traceback (most recent call last):\n  File \"<string>\", line 1, in <module>\nNameError: name 'printf' is not defined",
  "output": "",
  "code": "printf('Hello, World!')",
  "returncode": 1
}
```

### MCP Server

The Model Context Protocol (MCP) server provides AI agents (like Claude) with access to trading functionality via the Model Context Protocol.

### Running the MCP Server

To run the MCP server:

```bash
python main.py --server mcp
```

Or directly:

```bash
python -m app.mcp_server
```

### MCP Tools

The MCP server exposes the following tools:

- `get_current_time` - Get the current server time
- `get_current_price` - Get current price for a symbol
- `get_daily_history` - Get daily price history for a symbol
- `get_minute_history` - Get minute price history for a symbol
- `get_sector_category` - Get sector category information
- `get_sector_constituents` - Get sector constituents
- `get_symbol_sector` - Get sector information for a symbol
- `run_strategy` - Run a trading strategy

### Testing with MCP CLI Tools

For interactive testing, use the `mcp` command-line tools:

```bash
# Run the server in development mode with inspector
mcp dev app/mcp_server.py
```

### Using with Claude

To use with Claude for Desktop or API:

1. Run the MCP server
2. Connect Claude to the MCP server through the Claude interface

### References

- [Model Context Protocol Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [FastMCP](https://github.com/jlowin/fastmcp)

## API Documentation

Visit `/docs` or `/redoc` when running the FastAPI server to access the interactive API documentation.

## Development

The project follows modern Python best practices:
- Type hints for all functions and classes
- Comprehensive docstrings
- FastAPI best practices
- Error handling and logging
- CORS enabled for development

## Test with Dify Cloud

Run as an API server to work with Dify.
- ngrok to rproxy api
- export openapi schema to Dify to integrate with customized tools
- add the missing "server" section.

## Build and release as executables

uv add --dev nuitka
uv run python -m nuitka --standalone main.py

## Knowledgebase for LLM

docs/gmapi.md    完整的掘金api定义
docs/策略示例.md  策略示例

## Cherry Studio

MCP server support