# TravelHax0r MCP Server

Flight search MCP server using the fast_flights library.

## Quick Start

```bash
# Install dependencies
uv sync

# Run the server
uv run python travelhax0r/mcp_server.py
```

## Docker

```bash
# Using Docker Compose
docker-compose up --build

# Or build and run directly
docker build -t travelhax0r-mcp .
docker run -p 8080:8080 travelhax0r-mcp
```

## MCP Configuration

Add to your MCP settings file (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "travelhax0r-flights": {
      "command": "/usr/local/bin/docker-compose",
      "args": [
        "-f",
        "/path/to/travelhax0r/docker-compose.yml",
        "run",
        "--rm",
        "travelhax0r-mcp"
      ]
    }
  }
}
```
