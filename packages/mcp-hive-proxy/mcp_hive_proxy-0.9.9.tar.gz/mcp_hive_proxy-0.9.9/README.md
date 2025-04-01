# MCP Hive Proxy

A powerful command-line interface for interacting with MCP (Model Context Protocol) servers using the SSE protocol. This tool serves as a smart proxy between users and MCP servers, providing intelligent question matching, server management, and seamless integration with AI assistants like Windsurf.

## Key Features

- **Intelligent Question Matching**: Automatically finds the best predefined question on servers that require specific formats
- **Server Management**: Easily add, remove, list, and configure MCP servers
- **Windsurf/Cursor Integration**: Seamlessly connects your AI assistants to MCP servers
- **Parameter Handling**: Automatically detects and handles required parameters for specialized MCP servers
- **Configuration Import/Export**: Share server configurations between environments
- **Standalone Mode**: Can be used as a standalone script without installation

## Installation

```bash
# From PyPI (recommended)
pip install mcp-hive-proxy

# From source
git clone https://github.com/trilogy-group/mcp-hive-proxy.git
cd mcp-hive-proxy
pip install -e .
```

After installation, the `mcp-hive-proxy` command will be available in your terminal.

## Quick Start

```bash
# Ask a question to the default MCP server
mcp-hive-proxy ask "What is the latest news about AI?"

# Add a new server
mcp-hive-proxy servers add my-server https://mcp-server.example.com/sse

# List all configured servers
mcp-hive-proxy servers list
```

## Detailed Usage Guide

### Asking Questions

The `ask` command allows you to query any MCP server:

```bash
# Ask using the default server
mcp-hive-proxy ask "What is the weather today?"

# Ask using a specific server by name
mcp-hive-proxy ask "What tools are being used in this team room?" --server team-mcp

# Ask using a specific server by URL
mcp-hive-proxy ask "How can I improve my code?" --url https://mcp-server.example.com/sse

# List available questions for servers with predefined questions
mcp-hive-proxy ask --server team-mcp --list-questions
```

### Managing Servers

The `servers` command provides comprehensive server management:

```bash
# List all configured servers
mcp-hive-proxy servers list

# Add a new server
mcp-hive-proxy servers add my-server https://mcp-server.example.com/sse

# Add a server and sync with Windsurf
mcp-hive-proxy servers add my-server https://mcp-server.example.com/sse --sync-windsurf

# Remove a server
mcp-hive-proxy servers remove my-server

# Remove a server and sync with Windsurf
mcp-hive-proxy servers remove my-server --sync-windsurf

# Delete all servers (with confirmation prompt)
mcp-hive-proxy servers delete-all

# Delete all servers (skip confirmation)
mcp-hive-proxy servers delete-all --yes

# Set the default server
mcp-hive-proxy servers set-default tweet-finder-mcp

# Export server configuration
mcp-hive-proxy servers export --file servers.json

# Import server configuration
mcp-hive-proxy servers import servers.json
```

## Intelligent Question Matching

MCP Hive Proxy includes a smart question matching system for servers that require specific question formats:

1. **Auto-detection**: Automatically identifies servers with list/answer patterns
2. **Smart Matching**: Finds the best matching predefined question based on your query
3. **Parameter Handling**: Manages required parameters like s3_key, start_date, etc.
4. **Suggestions**: Provides helpful suggestions when your query doesn't match exactly

Example workflow:

```bash
# List available questions
mcp-hive-proxy ask --server team-mcp --list-questions

# Ask a question - the proxy will find the best matching predefined question
mcp-hive-proxy ask --server team-mcp "What tools are my team using?"
```

## Windsurf Integration

MCP Hive Proxy integrates seamlessly with Windsurf, allowing your AI assistant to leverage all the intelligent features:

```bash
# Add a server and sync with Windsurf
mcp-hive-proxy servers add my-server https://mcp-server.example.com/sse --sync-windsurf
```

When syncing with Windsurf, the proxy:

1. Updates the Windsurf MCP configuration file (`~/.codeium/windsurf/mcp_config.json`)
2. Configures each server with the proper format:
   ```json
   {
     "servers": {
       "my-server": {
         "command": "python3.12 -m mcp_proxy",
         "args": ["https://mcp-server.example.com/sse"]
       }
     }
   }
   ```
3. Ensures that Windsurf can spawn separate mcp-proxy processes for each server

This integration allows Windsurf to benefit from the intelligent question matching and parameter handling features of MCP Hive Proxy.

## Configuration

MCP Hive Proxy stores its configuration in `~/.config/mcp_cli/config.json`. This file contains:

- A list of configured servers with their URLs
- The default server to use when none is specified

Example configuration:

```json
{
  "servers": {
    "tweet-finder-mcp": "https://mcp-server.example.com/86c89e81/sse",
    "team-mcp": "https://mcp-server.example.com/83d6abf7/sse"
  },
  "default_server": "tweet-finder-mcp"
}
```

## Standalone Script

For environments where installation is not possible, you can use the standalone script:

```bash
# Make it executable
chmod +x mcp_cli_standalone.py

# Run it directly
./mcp_cli_standalone.py ask "What are the latest AI trends?"
```

## Advanced Usage

### Working with Specialized MCP Servers

Some MCP servers require specific question formats or parameters. MCP Hive Proxy handles this automatically:

1. First, it attempts to list available questions from the server
2. Then it matches your query to the best available question
3. If parameters are required, it extracts them from your query or uses defaults

### Troubleshooting

If you encounter issues:

1. Check your server configuration with `mcp-hive-proxy servers list`
2. Verify the server URL is correct and accessible
3. For servers with predefined questions, use `--list-questions` to see available options
4. Check the Windsurf configuration at `~/.codeium/windsurf/mcp_config.json`

## Requirements

- Python 3.9 or higher
- `mcp` package (installed automatically as a dependency)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The MCP team for creating the Model Context Protocol
- The Windsurf team for their AI assistant integration
- All contributors to this project
