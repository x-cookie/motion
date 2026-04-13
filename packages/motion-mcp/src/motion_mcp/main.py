"""Entry point for the Motion MCP server.

Run with: motion-mcp
Or: python -m motion_mcp.main
"""

import argparse

from motion_mcp import __version__
from motion_mcp.server import create_mcp_server


def main() -> None:
    """Start the MCP server."""
    parser = argparse.ArgumentParser(
        description="Motion MCP Server - Model Context Protocol server for AI integration",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"motion-mcp {__version__}",
    )
    # Parse args (exits on --version)
    parser.parse_args()

    mcp = create_mcp_server()
    mcp.run()


if __name__ == "__main__":
    main()
