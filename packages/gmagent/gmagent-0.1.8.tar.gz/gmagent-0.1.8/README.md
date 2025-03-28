# GM Trading Agent API

A service that provides both REST API and MCP (Model Context Protocol) interfaces to interact with the GM trading API. This project helps investors create and manage their trading strategies while providing helpful tools through a modern FastAPI service.

## Features

- **Market Data**
  - Current Price: Get real-time price data for any symbol
  - Historical Data: Access daily and minute-level historical price data
  - Sector Information: Get sector categories, constituents, and symbol sector information
- **Trading Tools**
  - Strategy Execution: Run custom Python trading strategies
  - Symbol Information: Get detailed information about trading symbols
  - Market Categories: Access market sector and industry classifications
- **Dual Interface**
  - REST API: Standard HTTP endpoints for web and application clients
  - MCP Server: Model Context Protocol server for AI agent integration

## Architecture

The application has a modular architecture with:

1. **Core API Layer**: Shared implementation of all API functionality
2. **FastAPI Server**: REST API server for web and application clients
3. **MCP Server**: Model Context Protocol server for AI agents like Claude

You can run either the FastAPI server or the MCP server independently, as they both use the same underlying core API implementation.

## Installation

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) for dependency management (recommended)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd gmagent
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install the package with dependencies:
```bash
# Using uv (recommended)
uv pip install -e .

# Using pip
pip install -e .
```

## Configuration

Create a `.env` file in the project root with your GM API credentials:

```env
GM_TOKEN=your_gm_token
GM_SERV_ADDR=your_gm_server_address
```

Optional environment variables:
```env
PROJECT_NAME=GM Trading Agent
API_V1_STR=/api/v1
```

## Usage

### Running the Server

The `gmagent` command-line tool supports both FastAPI and MCP servers:

```bash
# Run FastAPI server (default)
gmagent

# Run FastAPI server with custom host/port
gmagent --host 127.0.0.1 --port 9000

# Run FastAPI server with auto-reload for development
gmagent --reload

# Run MCP server
gmagent --server mcp
```

### REST API Endpoints

The FastAPI server provides the following endpoints:

#### Market Data

```http
# Current Price
GET /api/v1/current_price?symbol={symbol}

# Daily History
GET /api/v1/daily_history?symbol={symbol}&start_date={YYYY-MM-DD}&end_date={YYYY-MM-DD}

# Minute History
GET /api/v1/minute_history?symbol={symbol}&start_time={YYYY-MM-DD HH:MM:SS}&end_time={YYYY-MM-DD HH:MM:SS}
```

#### Market Structure

```http
# Sector Categories
GET /api/v1/sector/category?sector_type={sector_type}

# Sector Constituents
GET /api/v1/sector/constituents?category_id={category_id}

# Symbol Sector
GET /api/v1/symbol/sector?symbol={symbol}&sector_type={sector_type}
```

#### Symbol Information

```http
# List Symbols
GET /api/v1/symbols?sec_type1={type1}&sec_type2={type2}&exchanges={exchanges}&symbols={symbols}

# Symbol Details
GET /api/v1/symbol_infos?symbols={symbol1,symbol2,...}
```

#### Strategy Execution

```http
# Run Strategy
POST /api/v1/strategy/run
Content-Type: application/json

{
    "code": "your_python_code_here"
}
```

### MCP Tools

When running as an MCP server, the following tools are available to AI agents:

- `get_current_time()`: Get server time with timezone information
- `get_current_price(symbol)`: Get real-time price data
- `get_daily_history(symbol, start_date, end_date)`: Get daily historical data
- `get_minute_history(symbol, start_time, end_time)`: Get minute-level data
- `get_sector_category(sector_type)`: Get sector classifications
- `get_sector_constituents(category_id)`: Get sector members
- `get_symbol_sector(symbol)`: Get symbol's sector information
- `get_symbols(sec_type1, ...)`: List available symbols
- `get_symbol_infos(symbols)`: Get detailed symbol information
- `run_strategy(code)`: Execute trading strategies

## Development

### Project Structure

```
gmagent/
├── src/
│   └── gmagent/
│       ├── app/
│       │   ├── api/
│       │   │   └── core.py      # Core API implementation
│       │   ├── models/          # Data models
│       │   ├── services/        # Business logic
│       │   ├── config.py        # Configuration
│       │   ├── fastapi_server.py # FastAPI implementation
│       │   └── mcp_server.py    # MCP server implementation
│       └── __init__.py          # Entry point
├── tests/                       # Test suite
├── pyproject.toml              # Project metadata and dependencies
├── README.md                   # This file
└── .env                        # Environment configuration
```

### Testing

Run the test suite:

```bash
pytest
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

[Your License Here]

## Acknowledgments

- [GM API](https://www.myquant.cn/) - Trading API provider
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [MCP](https://github.com/lhenault/mcp) - Model Context Protocol implementation

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


## Knowledgebase for LLM

docs/gmapi.md    完整的掘金api定义
docs/策略示例.md  策略示例

## Cherry Studio

MCP server support