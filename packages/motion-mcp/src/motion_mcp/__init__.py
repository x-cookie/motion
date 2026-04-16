"""MCP server for Motion.

This package provides a Model Context Protocol (MCP) server that enables
Claude Desktop and other MCP-compatible AI clients to interact with Motion.
"""

from importlib.metadata import version

try:
    __version__ = version("motion-mcp")
except Exception:
    __version__ = "unknown"
