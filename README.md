# TravelHax0r MCP Server Setup

This document explains how to set up and use the TravelHax0r MCP server for flight search functionality with ChatGPT.

## Overview

The TravelHax0r MCP server provides a single tool called `search_flights` that allows you to search for flights using the fast_flights library. It wraps the `get_flights_from_filter` function with a user-friendly interface.

## Prerequisites

- Python 3.8+
- The `fastmcp` and `fast_flights` packages installed
- Access to the TravelHax0r project

## Installation

1. Ensure you have the required dependencies:
   ```bash
   uv sync
   ```

2. The MCP server is located at `src/travelhax0r/mcp_server.py`

## Configuration for ChatGPT

To use this MCP server with ChatGPT, you need to configure it in your MCP settings. The settings file is typically located at:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### Adding the Server Configuration

Add the following configuration to your `mcpServers` object in the settings file:

```json
{
  "mcpServers": {
    "travelhax0r-flights": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/your/travelhax0r", "python", "src/travelhax0r/mcp_server.py"],
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

**Important**: Replace `/path/to/your/travelhax0r/` with the actual path to your TravelHax0r project directory.
