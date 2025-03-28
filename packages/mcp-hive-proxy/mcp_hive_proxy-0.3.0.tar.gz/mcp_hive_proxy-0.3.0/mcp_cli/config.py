"""
Configuration management for MCP CLI
"""
import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

DEFAULT_CONFIG_PATH = os.path.expanduser("~/.config/mcp_cli/config.json")
DEFAULT_CONFIG = {
    "servers": {
        "xoactivities": "https://mcp-server.ti.trilogy.com/5b46ff14/sse",
        "team-mcp": "https://mcp-server.ti.trilogy.com/83d6abf7/sse",
        "tweet-finder-mcp": "https://mcp-server.ti.trilogy.com/86c89e81/sse",
        "memory-store": "https://mcp-server.ti.trilogy.com/f6a5f1e1/sse"
    },
    "default_server": "tweet-finder-mcp"
}

WINDSURF_CONFIG_PATH = os.path.expanduser("~/.codeium/windsurf/mcp_config.json")
WINDSURF_MEMORY_PATH = os.path.expanduser("~/.codeium/windsurf/memories")


def ensure_config_dir() -> None:
    """Ensure the config directory exists."""
    config_dir = os.path.dirname(DEFAULT_CONFIG_PATH)
    os.makedirs(config_dir, exist_ok=True)


def load_config() -> Dict[str, Any]:
    """Load the configuration file."""
    ensure_config_dir()
    
    if not os.path.exists(DEFAULT_CONFIG_PATH):
        # Create default config if it doesn't exist
        with open(DEFAULT_CONFIG_PATH, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        return DEFAULT_CONFIG
    
    try:
        with open(DEFAULT_CONFIG_PATH, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Config file at {DEFAULT_CONFIG_PATH} is invalid JSON. Using defaults.")
        return DEFAULT_CONFIG


def save_config(config: Dict[str, Any]) -> None:
    """Save the configuration file."""
    ensure_config_dir()
    
    with open(DEFAULT_CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)


def get_server_url(server_name: Optional[str] = None) -> str:
    """Get the URL for a server by name."""
    config = load_config()
    
    if not server_name:
        server_name = config.get("default_server", "tweet-finder-mcp")
    
    servers = config.get("servers", {})
    if server_name not in servers:
        raise ValueError(f"Server '{server_name}' not found in configuration.")
    
    return servers[server_name]


def list_servers() -> Dict[str, str]:
    """List all configured servers."""
    config = load_config()
    return config.get("servers", {})


def add_server(name: str, url: str, sync_windsurf: bool = False, sync_cursor: bool = False) -> None:
    """
    Add a new server to the configuration.
    
    Args:
        name: The name of the server
        url: The URL of the server
        sync_windsurf: Whether to sync with Windsurf's MCP config
        sync_cursor: Whether to sync with Cursor's MCP config
    """
    config = load_config()
    
    if "servers" not in config:
        config["servers"] = {}
    
    config["servers"][name] = url
    save_config(config)
    
    if sync_windsurf:
        sync_with_windsurf()
    
    if sync_cursor:
        sync_with_cursor()


def remove_server(name: str, sync_windsurf: bool = False, sync_cursor: bool = False) -> None:
    """
    Remove a server from the configuration.
    
    Args:
        name: The name of the server to remove
        sync_windsurf: Whether to sync with Windsurf's MCP config
        sync_cursor: Whether to sync with Cursor's MCP config
    """
    config = load_config()
    
    if "servers" not in config or name not in config["servers"]:
        raise ValueError(f"Server '{name}' not found in configuration.")
    
    del config["servers"][name]
    save_config(config)
    
    if sync_windsurf:
        sync_with_windsurf()
    
    if sync_cursor:
        sync_with_cursor()


def set_default_server(name: str) -> None:
    """Set the default server."""
    config = load_config()
    
    if "servers" not in config or name not in config["servers"]:
        raise ValueError(f"Server '{name}' not found in configuration.")
    
    config["default_server"] = name
    save_config(config)


def sync_with_windsurf() -> None:
    """Sync the MCP CLI configuration with Windsurf's MCP config."""
    # Create Windsurf config directory if it doesn't exist
    windsurf_dir = os.path.dirname(WINDSURF_CONFIG_PATH)
    os.makedirs(windsurf_dir, exist_ok=True)
    
    # Load MCP CLI config
    mcp_cli_config = load_config()
    servers = mcp_cli_config.get("servers", {})
    
    # Load existing Windsurf config if it exists
    windsurf_config = {"mcpServers": {}}
    if os.path.exists(WINDSURF_CONFIG_PATH):
        try:
            with open(WINDSURF_CONFIG_PATH, 'r') as f:
                windsurf_config = json.load(f)
        except json.JSONDecodeError:
            print(f"Error: Windsurf config file at {WINDSURF_CONFIG_PATH} is invalid JSON. Creating new one.")
    
    # Update Windsurf config with MCP CLI servers
    for name, url in servers.items():
        windsurf_config["mcpServers"][name] = {
            "command": "/bin/bash",
            "args": ["-c", f"mcp-hive-proxy ask \"$QUESTION\" --server {name}"]
        }
    
    # Save updated Windsurf config
    with open(WINDSURF_CONFIG_PATH, 'w') as f:
        json.dump(windsurf_config, f, indent=2)
    
    print(f"Synchronized with Windsurf MCP config at {WINDSURF_CONFIG_PATH}")
    
    # Create or update memory about using the proxy
    create_proxy_memory()


def create_proxy_memory() -> None:
    """Create or update a memory about using the MCP proxy."""
    # Ensure the memories directory exists
    os.makedirs(WINDSURF_MEMORY_PATH, exist_ok=True)
    
    # Define the memory content
    memory_content = {
        "id": "mcp-proxy-usage",
        "title": "Always use MCP Hive Proxy for MCP servers",
        "content": "When MCP tools or servers are detected, always use the mcp-hive-proxy CLI tool to interact with them, as it provides intelligent question matching and better parameter handling. This ensures consistent behavior and leverages the enhanced functionality.",
        "tags": ["mcp", "proxy", "tool_usage"],
        "corpusNames": ["global"],
        "createdAt": "2025-03-28T00:00:00Z",
        "updatedAt": "2025-03-28T00:00:00Z"
    }
    
    # Check if the memory already exists
    memory_exists = False
    for filename in os.listdir(WINDSURF_MEMORY_PATH):
        if filename.endswith(".json"):
            try:
                with open(os.path.join(WINDSURF_MEMORY_PATH, filename), 'r') as f:
                    memory = json.load(f)
                    if memory.get("id") == "mcp-proxy-usage":
                        memory_exists = True
                        # Update existing memory
                        with open(os.path.join(WINDSURF_MEMORY_PATH, filename), 'w') as f:
                            json.dump(memory_content, f, indent=2)
                        print(f"Updated existing memory about MCP proxy usage")
                        break
            except (json.JSONDecodeError, IOError):
                continue
    
    # Create new memory if it doesn't exist
    if not memory_exists:
        memory_file = os.path.join(WINDSURF_MEMORY_PATH, "mcp-proxy-usage.json")
        with open(memory_file, 'w') as f:
            json.dump(memory_content, f, indent=2)
        print(f"Created new memory about MCP proxy usage at {memory_file}")


def sync_with_cursor() -> None:
    """Sync the MCP CLI configuration with Cursor's MCP config."""
    # This is a placeholder for future implementation
    # Cursor integration would be similar to Windsurf integration
    print("Cursor synchronization is not yet implemented")
