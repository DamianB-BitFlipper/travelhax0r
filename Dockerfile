# Use Python 3.13 with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Install git for git dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy pyproject.toml and uv.lock for dependency installation
COPY pyproject.toml uv.lock ./

COPY README .

# Install dependencies using uv
RUN uv sync --frozen --no-install-project

# Copy the travelhax0r package
COPY travelhax0r/ ./travelhax0r/

# Expose port 8080 for the MCP server
EXPOSE 8080

# Run the MCP server
CMD ["uv", "run", "python", "travelhax0r/mcp_server.py"]
