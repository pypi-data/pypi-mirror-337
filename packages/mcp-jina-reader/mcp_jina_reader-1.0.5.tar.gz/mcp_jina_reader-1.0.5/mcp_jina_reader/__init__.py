import sys
from mcp_jina_reader.server import mcp_server 
import asyncio


def main():
    """Main entry point for the package."""
    print("Starting jina reader MCP server...", file=sys.stderr)
    asyncio.run(mcp_server.run(transport="stdio"))


# Optionally expose other important items at package level
__all__ = ["main", "server"]