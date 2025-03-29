import sys
from mcp_jina_reader.server import server


def main():
    # Start the MCP server
    print("Starting jina reader MCP server...", file=sys.stderr)
    server.run(transport="stdio")


if __name__ == "__main__":
    main()