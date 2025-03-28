# MCP Hive Proxy

A command-line interface for interacting with MCP (Model Context Protocol) servers using the SSE protocol.

## Features

- **Ask questions** to any MCP server directly from the command line
- **Manage server configurations** with easy add, remove, and list operations
- **Set default servers** for quick access
- **Import and export** server configurations
- **Standalone script** that can be run outside of a virtual environment

## Installation

```bash
# From the source directory
pip install -e .

# Or once published
pip install mcp-hive-proxy
```

## Usage

### Asking Questions

```bash
# Ask a question to the default server
mcp ask "What is the best AI tool for coding?"

# Ask a question to a specific server by name
mcp ask --server team-mcp "What tools are being used in this team room?"

# Ask a question to a specific server by URL
mcp ask --url https://mcp-server.example.com/sse "What is the weather today?"
```

### Managing Servers

```bash
# List all configured servers
mcp servers list

# Add a new server
mcp servers add my-server https://mcp-server.example.com/sse

# Remove a server
mcp servers remove my-server

# Set the default server
mcp servers set-default tweet-finder-mcp

# Export server configuration
mcp servers export --file servers.json

# Import server configuration
mcp servers import servers.json
```

## Standalone Script

The repository also includes a standalone script `mcp_cli_standalone.py` that can be run directly without installing the package:

```bash
# Make it executable
chmod +x mcp_cli_standalone.py

# Run it directly
./mcp_cli_standalone.py ask "What are the latest AI trends?"

# Or copy it to a location in your PATH
cp mcp_cli_standalone.py ~/bin/mcp
```

## Configuration

The CLI stores its configuration in `~/.config/mcp_cli/config.json`. This file is created automatically when you first run the CLI, and it contains:

- A list of configured servers with their URLs
- The default server to use when none is specified

## Requirements

- Python 3.9 or higher
- `mcp` package (installed automatically as a dependency)

## License

MIT
