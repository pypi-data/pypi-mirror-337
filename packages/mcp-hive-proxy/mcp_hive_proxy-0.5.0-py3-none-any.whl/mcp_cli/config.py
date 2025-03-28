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


def add_server(name: str, url: str) -> None:
    """Add a new server to the configuration."""
    config = load_config()
    
    if "servers" not in config:
        config["servers"] = {}
    
    config["servers"][name] = url
    save_config(config)


def remove_server(name: str) -> None:
    """Remove a server from the configuration."""
    config = load_config()
    
    if "servers" not in config or name not in config["servers"]:
        raise ValueError(f"Server '{name}' not found in configuration.")
    
    del config["servers"][name]
    save_config(config)


def set_default_server(name: str) -> None:
    """Set the default server."""
    config = load_config()
    
    if "servers" not in config or name not in config["servers"]:
        raise ValueError(f"Server '{name}' not found in configuration.")
    
    config["default_server"] = name
    save_config(config)
