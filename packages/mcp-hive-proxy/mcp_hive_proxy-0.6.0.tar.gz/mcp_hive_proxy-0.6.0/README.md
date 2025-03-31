# MCP Hive Proxy

A command-line interface for interacting with MCP servers. This package provides a standalone implementation that doesn't depend on the external `mcp` package.

## Features

- Connect to any MCP server using the SSE protocol
- Ask questions to MCP servers with automatic tool detection
- Manage server configurations with an easy-to-use CLI
- Support for servers with predefined questions
- Automatic question matching for servers that require specific questions
- Store server configurations in ~/.config/mcp_cli/config.json
- Import/export server configurations

## Installation

You can install the package directly from PyPI:

```bash
pip install mcp-hive-proxy
```

Or build and install the package from source:

```bash
cd /path/to/mcp-hive-proxy
pip install build
python -m build
pip install dist/mcp_hive_proxy-0.6.0-py3-none-any.whl
```

## Usage

### Ask a question to an MCP server

```bash
# Ask a question to the default server
mcp-hive-proxy ask "What is the weather today?"

# Ask a question to a specific server
mcp-hive-proxy ask "What is the weather today?" --server trilogy-mcp

# Ask a question to a custom URL
mcp-hive-proxy ask "What is the weather today?" --url https://mcp-server.example.com/sse

# List available predefined questions for a server
mcp-hive-proxy ask --list-questions --server trilogy-mcp
```

### Manage server configurations

```bash
# List all configured servers
mcp-hive-proxy servers list

# Add a new server
mcp-hive-proxy servers add my-server https://mcp-server.example.com/sse

# Remove a server
mcp-hive-proxy servers remove my-server

# Set the default server
mcp-hive-proxy servers set-default trilogy-mcp

# Export server configurations
mcp-hive-proxy servers export --file servers.json

# Import server configurations
mcp-hive-proxy servers import servers.json
```

## Configuration

The package stores server configurations in `~/.config/mcp_cli/config.json`. This file is created automatically with default servers when you first run the tool.

## Windsurf Integration

To use mcp-hive-proxy with Windsurf, configure mcp_config.json with "command" and "args" properties instead of "url":

```json
{
  "servers": {
    "my-server": {
      "command": "python3.12 -m mcp_cli.cli",
      "args": ["https://mcp-server.example.com/sse"]
    }
  }
}
```

This allows Windsurf to spawn mcp-hive-proxy processes to handle SSE connections. Each server requires a separate mcp-hive-proxy instance as one instance can only connect to one endpoint.

## Requirements

- Python 3.8 or higher
- httpx
- httpx-sse
- anyio
- pydantic
- pydantic-settings
