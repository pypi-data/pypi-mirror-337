from typing import Annotated

from mcp.shared.exceptions import McpError
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    ErrorData,
    GetPromptResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    TextContent,
    Tool,
    INVALID_PARAMS,
)
from pydantic import BaseModel, Field, AnyUrl


async def fetch_prefixed_url(url: str) -> str:
    """Prefix URL with r.jina.ai and fetch the resulting content.

    Args:
        url: Original URL to prefix and fetch

    Returns:
        Content from the URL
    """
    import httpx
    prefixed_url = f"https://r.jina.ai/{url}"
    headers = {
        "Accept": "text/event-stream",
        "X-Engine": "browser",
        "X-Remove-Selector": "header",
        "X-Respond-With": "readerlm-v2",
        "X-Return-Format": "markdown"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(prefixed_url, headers=headers)
        response.raise_for_status()
        return response.text

def prefix_jina_url(url: str) -> str:
    """Add r.jina.ai prefix to URL (without fetching).

    Args:
        url: Original URL to prefix

    Returns:
        read URL content 
    """
    return f"https://r.jina.ai/{url}"


class JinaReader(BaseModel):
    """Parameters for Jina Reader URL prefixing and content fetching."""

    url: Annotated[AnyUrl, Field(description="URL to prefix with r.jina.ai")]


async def serve() -> None:
    """Run the Jina Reader MCP server."""
    server = Server("mcp-jina-reader")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="jina_reader",
                description="read a URL with r.jina.ai to make it more LLM-friendly",
                inputSchema=JinaReader.model_json_schema(),
            )
        ]

    @server.list_prompts()
    async def list_prompts() -> list[Prompt]:
        return [
            Prompt(
                name="jina_reader",
                description="read URL content with r.jina.ai",
                arguments=[
                    PromptArgument(
                        name="url", description="URL to read", required=True
                    )
                ],
            )
        ]

    @server.call_tool()
    async def call_tool(name, arguments: dict) -> list[TextContent]:
        try:
            args = JinaReader(**arguments)
        except ValueError as e:
            raise McpError(ErrorData(code=INVALID_PARAMS, message=str(e)))

        url = str(args.url)
        if not url:
            raise McpError(ErrorData(code=INVALID_PARAMS, message="URL is required"))

        content = await fetch_prefixed_url(url)
        return [
            TextContent(
                type="text", text=f"Content from prefixed URL: {content}"
            )
        ]

    @server.get_prompt()
    async def get_prompt(name: str, arguments: dict | None) -> GetPromptResult:
        if not arguments or "url" not in arguments:
            raise McpError(ErrorData(code=INVALID_PARAMS, message="URL is required"))

        url = arguments["url"]
        content = await fetch_prefixed_url(url)
        return GetPromptResult(
            description=f"Content from URL{url}",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text", text=f"Content from URL: {content}"
                    ),
                )
            ],
        )

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)