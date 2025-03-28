import asyncio
import requests
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
import mcp.server.stdio


server = Server("mcp-jina-reader")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        types.Tool(
            name="reader",
            description="use Jina URL reader to read a URL and return the llm frendly output",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {"type": "string"}
                },
                "required": ["url"],
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    Tools can modify server state and notify clients of changes.
    """
    if name != "reader":
        raise ValueError(f"Unknown tool: {name}")

    if not arguments:
        raise ValueError("Missing arguments")

    url = arguments.get("url")

    if not url:
        raise ValueError("Missing url")

    content = call_jina_url_reader(url)

    return [
        types.TextContent(
            type="text",
            text=f"url content: {content}",
        )
    ]

        
def call_jina_url_reader(url: str):
    read_url = f"https://r.jina.ai/{url}"
    headers = {
        "Accept": "text/event-stream",
        "X-Engine": "browser",
        # "X-Remove-Selector": "header,
        "X-Respond-With": "readerlm-v2",
        "X-Return-Format": "markdown"
    }

    response = requests.get(read_url, headers=headers, timeout=60000)
    
    return response.text
    


async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-jina-reader",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
            raise_exceptions=True
        )