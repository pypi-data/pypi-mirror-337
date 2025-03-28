# MCP Hive Proxy

A command-line interface for interacting with MCP (Model Context Protocol) servers using the SSE protocol.

## Features

- **Ask questions** to any MCP server directly from the command line
- **Intelligent question matching** for servers with predefined questions
- **Automatic parameter handling** for specialized MCP servers
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
mcp-hive-proxy ask "What is the best AI tool for coding?"

# Ask a question to a specific server by name
mcp-hive-proxy ask --server team-mcp "What tools are being used in this team room?"

# Ask a question to a specific server by URL
mcp-hive-proxy ask --url https://mcp-server.example.com/sse "What is the weather today?"

# List available questions for servers with predefined questions
mcp-hive-proxy ask --server team-mcp --list-questions
```

### Managing Servers

```bash
# List all configured servers
mcp-hive-proxy servers list

# Add a new server
mcp-hive-proxy servers add my-server https://mcp-server.example.com/sse

# Remove a server
mcp-hive-proxy servers remove my-server

# Set the default server
mcp-hive-proxy servers set-default tweet-finder-mcp

# Export server configuration
mcp-hive-proxy servers export --file servers.json

# Import server configuration
mcp-hive-proxy servers import servers.json
```

## Intelligent Question Matching

Some MCP servers have a predefined set of questions they can answer. The CLI automatically:

1. Detects servers with list/answer patterns
2. Finds the best matching question based on your query
3. Handles required parameters (like s3_key, start_date, end_date)
4. Shows available questions when using the `--list-questions` flag

Example:
```bash
# List available questions on a server
mcp-hive-proxy ask --server team-mcp --list-questions

# Ask a question - the CLI will find the best matching predefined question
mcp-hive-proxy ask --server team-mcp "What tools are my team using?"
```

## Standalone Script

The repository also includes a standalone script `mcp_cli_standalone.py` that can be run directly without installing the package:

```bash
# Make it executable
chmod +x mcp_cli_standalone.py

# Run it directly
./mcp_cli_standalone.py ask "What are the latest AI trends?"

# Or copy it to a location in your PATH
cp mcp_cli_standalone.py ~/bin/mcp-hive-proxy
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
