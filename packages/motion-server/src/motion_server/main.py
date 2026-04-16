"""Main entry point for Motion API server."""

import argparse
import sys

from motion_server import __version__


def main() -> None:
    """Start the Motion API server."""
    parser = argparse.ArgumentParser(
        description="Motion API Server - REST API for task management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  motion-server                        # Start server on default host:port
  motion-server --host 0.0.0.0         # Listen on all interfaces
  motion-server --port 3000            # Use custom port
  motion-server --reload               # Enable auto-reload for dev

The API will be available at:
  - Root: http://{host}:{port}/
  - Docs: http://{host}:{port}/docs
  - Health: http://{host}:{port}/health
        """,
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"motion-server {__version__}",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind (default: 8000)",
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development",
    )
    args = parser.parse_args()

    try:
        import uvicorn
    except ImportError:
        print(
            "Error: uvicorn is not installed. Install it with: pip install motion-server",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Starting Motion API server on {args.host}:{args.port}")
    print(f"API documentation: http://{args.host}:{args.port}/docs")
    print(f"Health check: http://{args.host}:{args.port}/health")
    print()

    uvicorn.run(
        "motion_server.api.app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info",
    )


if __name__ == "__main__":
    main()
