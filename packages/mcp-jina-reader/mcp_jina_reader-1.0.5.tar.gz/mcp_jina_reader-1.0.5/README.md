# mcp-jina-reader MCP server

A standard MCP server that converts URLs into LLM-friendly inputs using Jina AI's API


### Tools

The server implements one tool:
- reader: Use Jina URL reader to process URLs and return LLM-friendly output
  - Requires "url" as a mandatory string parameter
  - Returns processed URL content


## Quickstart

### Install

#### Claude Desktop

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

<details>
  <summary>Development/Unpublished Servers Configuration</summary>
  ```
  "mcpServers": {
    "mcp-jina-reader": {
      "command": "uv",
      "args": [
        "--directory",
        "your-dir",
        "run",
        "mcp-jina-reader"
      ]
    }
  }
  ```
</details>

<details>
  <summary>Published Servers Configuration</summary>
  ```
  "mcpServers": {
    "mcp-jina-reader": {
      "command": "uvx",
      "args": [
        "mcp-jina-reader"
      ]
    }
  }
  ```
</details>

## Development

### Building and Publishing

To prepare the package for distribution:

1. Sync dependencies and update lockfile:
```bash
uv sync
```

2. Build package distributions:
```bash
uv build
```

This will create source and wheel distributions in the `dist/` directory.

3. Publish to PyPI:
```bash
uv publish
```

Note: You'll need to set PyPI credentials via environment variables or command flags:
- Token: `--token` or `UV_PUBLISH_TOKEN`
- Or username/password: `--username`/`UV_PUBLISH_USERNAME` and `--password`/`UV_PUBLISH_PASSWORD`

### Debugging

Since MCP servers run over stdio, debugging can be challenging. For the best debugging
experience, we strongly recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).


You can launch the MCP Inspector via [`npm`](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) with this command:

```bash
npx @modelcontextprotocol/inspector uv --directory yourdir run mcp-jina-reader
```


Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.