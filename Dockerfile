# Use Python 3.13 with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Install git and system dependencies needed by Chromium
RUN apt-get update && apt-get install -y \
    git \
    libglib2.0-0 \
    libnspr4 \
    libnss3 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libxkbcommon0 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy pyproject.toml and uv.lock for dependency installation
COPY ./pyproject.toml ./uv.lock ./

# Hatch requires the README.md to build the project
COPY ./README.md .

# Install dependencies using uv
RUN uv sync --frozen --no-install-project

# Install playwright browser
RUN python -m pip install playwright && python -m playwright install chromium

# Copy the travelhax0r package
COPY travelhax0r/ ./travelhax0r/

# Expose port 8080 for the MCP server
EXPOSE 8080

# Set entrypoint to run the MCP server
ENTRYPOINT ["uv", "run", "python", "travelhax0r/mcp_server.py"]

# Default CMD is the transport type (stdio)
CMD ["stdio"]
