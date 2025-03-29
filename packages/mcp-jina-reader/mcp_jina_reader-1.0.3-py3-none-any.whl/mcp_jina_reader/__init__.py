import sys
from . import server


def main():
    """Main entry point for the package."""
    print("Starting jina reader MCP server...", file=sys.stderr)
    server.run(transport="stdio")


# Optionally expose other important items at package level
__all__ = ["main", "server"]