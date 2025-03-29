import httpx
import sys
from mcp.server.fastmcp import FastMCP

server = FastMCP("mcp-jina-reader")


@server.tool(description="Read a webpage and return the LLM-friendly content.")
async def mcp_jina_reader(url: str) -> str:
    prefixed_url = f"https://r.jina.ai/{url}"
    print(f'recept url {prefixed_url}', file=sys.stderr)
    headers = {
        # "Accept": "text/event-stream",
        "X-Engine": "browser",
        "X-Remove-Selector": "header",
        "X-Md-Link-Style": "discarded"
        # "X-Respond-With": "readerlm-v2",
        # "X-Return-Format": "markdown"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(prefixed_url, headers=headers)
        response.raise_for_status()
        return response.text
    
if __name__ == "__main__":
    server.run(transport='stdio')
    
