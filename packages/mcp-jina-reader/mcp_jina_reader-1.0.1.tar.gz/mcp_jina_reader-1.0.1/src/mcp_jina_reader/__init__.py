from .server import serve


def main():
    """MCP Fetch Server - Use Jina URL reader to process URLs and return LLM-friendly output"""
    import asyncio

    asyncio.run(serve())


if __name__ == "__main__":
    main()
