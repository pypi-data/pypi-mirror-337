"""Main entry point for the application."""

import argparse
import os
import uvicorn
from app.mcp_server import create_mcp_server


def main() -> None:
    """Run either the FastAPI server or the MCP server based on command line arguments."""
    parser = argparse.ArgumentParser(description="GM Trading API Server")
    parser.add_argument(
        "--server",
        type=str,
        choices=["fastapi", "mcp"],
        default="fastapi",
        help="Server type to run (fastapi or mcp)",
    )
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host to bind the server to (FastAPI only)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Port to bind the server to (default: 8000 for FastAPI)",
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development (FastAPI only)",
    )
    args = parser.parse_args()

    if args.server == "fastapi":
        port = args.port or 8000
        print(
            f"Starting FastAPI server on {args.host}:{port} with reload={'enabled' if args.reload else 'disabled'}"
        )
        uvicorn.run(
            "app.fastapi_server:app",
            host=args.host,
            port=port,
            reload=args.reload,
        )
    else:  # args.server == "mcp"
        print("Starting MCP server")

        # Create and run the MCP server
        mcp_server = create_mcp_server()

        try:
            # Run the MCP server - no host/port needed as it uses MCP protocol
            mcp_server.run()
        except KeyboardInterrupt:
            print("MCP server stopped by user")
        except Exception as e:
            print(f"Error starting MCP server: {e}")


if __name__ == "__main__":
    main()
