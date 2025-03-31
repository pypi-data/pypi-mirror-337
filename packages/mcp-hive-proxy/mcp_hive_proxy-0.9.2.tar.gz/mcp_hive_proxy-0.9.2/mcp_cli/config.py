"""
Configuration management for MCP CLI

This module handles all configuration-related functionality for the MCP CLI,
including loading and saving configurations, managing server entries, and
synchronizing with Windsurf and Cursor configurations.
"""
import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

# Configuration paths
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

# Windsurf integration paths
WINDSURF_CONFIG_PATH = os.path.expanduser("~/.codeium/windsurf/mcp_config.json")
WINDSURF_MEMORY_PATH = os.path.expanduser("~/.codeium/windsurf/memories")


def ensure_config_dir() -> None:
    """
    Ensure the configuration directory exists.
    
    Creates the directory structure for the MCP CLI configuration
    if it doesn't already exist.
    """
    config_dir = os.path.dirname(DEFAULT_CONFIG_PATH)
    os.makedirs(config_dir, exist_ok=True)


def load_config() -> Dict[str, Any]:
    """
    Load the configuration file.
    
    Returns:
        Dict[str, Any]: The loaded configuration as a dictionary
        
    If the configuration file doesn't exist, it creates a default one.
    """
    ensure_config_dir()
    
    if not os.path.exists(DEFAULT_CONFIG_PATH):
        # Create default config file
        with open(DEFAULT_CONFIG_PATH, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        print(f"Created default configuration at {DEFAULT_CONFIG_PATH}")
        return DEFAULT_CONFIG
    
    try:
        with open(DEFAULT_CONFIG_PATH, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Config file at {DEFAULT_CONFIG_PATH} is invalid JSON. Using default config.")
        return DEFAULT_CONFIG


def save_config(config: Dict[str, Any]) -> None:
    """
    Save the configuration file.
    
    Args:
        config: The configuration to save
    """
    ensure_config_dir()
    with open(DEFAULT_CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)


def get_server_url(server_name: Optional[str] = None) -> Optional[str]:
    """
    Get the URL for a server by name.
    
    Args:
        server_name: The name of the server to get the URL for.
                    If None, returns the URL for the default server.
    
    Returns:
        Optional[str]: The URL of the server, or None if not found
    """
    config = load_config()
    servers = config.get("servers", {})
    
    if not server_name:
        # Use default server
        default_server = config.get("default_server")
        if default_server and default_server in servers:
            return servers[default_server]
        elif servers:
            # If no default server is set but servers exist, use the first one
            return next(iter(servers.values()))
        return None
    
    return servers.get(server_name)


def list_servers() -> Dict[str, str]:
    """
    List all configured servers.
    
    Returns:
        Dict[str, str]: A dictionary of server names to URLs
    """
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
    
    # Ensure servers key exists
    if "servers" not in config:
        config["servers"] = {}
    
    # Add or update the server
    config["servers"][name] = url
    
    # If this is the first server, set it as default
    if len(config["servers"]) == 1:
        config["default_server"] = name
    
    # Save the updated config
    save_config(config)
    
    # Sync with Windsurf and/or Cursor if requested
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
    servers = config.get("servers", {})
    
    # Check if the server exists
    if name not in servers:
        print(f"Error: Server '{name}' not found in configuration")
        return
    
    # Remove the server
    del servers[name]
    
    # If the default server was removed, update it
    if config.get("default_server") == name:
        if servers:
            # Set the first remaining server as default
            config["default_server"] = next(iter(servers.keys()))
        else:
            # No servers left, remove default_server key
            if "default_server" in config:
                del config["default_server"]
    
    # Save the updated config
    save_config(config)
    
    # Sync with Windsurf and/or Cursor if requested
    if sync_windsurf:
        sync_with_windsurf()
    
    if sync_cursor:
        sync_with_cursor()


def set_default_server(name: str) -> None:
    """
    Set the default server.
    
    Args:
        name: The name of the server to set as default
    """
    config = load_config()
    servers = config.get("servers", {})
    
    # Check if the server exists
    if name not in servers:
        print(f"Error: Server '{name}' not found in configuration")
        return
    
    # Set the default server
    config["default_server"] = name
    
    # Save the updated config
    save_config(config)


def sync_with_windsurf() -> None:
    """
    Sync the MCP CLI configuration with Windsurf's MCP config.
    
    This function:
    1. Creates the Windsurf config directory if it doesn't exist
    2. Loads the current MCP CLI server configurations
    3. Updates the Windsurf MCP config to use these servers
    4. Formats each server entry to use the mcp_proxy module
    5. Creates a memory instructing Windsurf to use the proxy
    """
    # Create Windsurf config directory if it doesn't exist
    windsurf_dir = os.path.dirname(WINDSURF_CONFIG_PATH)
    os.makedirs(windsurf_dir, exist_ok=True)
    
    # Load MCP CLI config
    mcp_cli_config = load_config()
    servers = mcp_cli_config.get("servers", {})
    
    # Load existing Windsurf config if it exists
    windsurf_config = {"servers": {}}
    if os.path.exists(WINDSURF_CONFIG_PATH):
        try:
            with open(WINDSURF_CONFIG_PATH, 'r') as f:
                windsurf_config = json.load(f)
        except json.JSONDecodeError:
            print(f"Error: Windsurf config file at {WINDSURF_CONFIG_PATH} is invalid JSON. Creating new one.")
    
    # Ensure servers key exists
    if "servers" not in windsurf_config:
        windsurf_config["servers"] = {}
    
    # Replace existing servers with the current MCP CLI servers
    # This ensures deleted servers are also removed from Windsurf config
    windsurf_config["servers"] = {}
    
    # Update Windsurf config with MCP CLI servers
    for name, url in servers.items():
        windsurf_config["servers"][name] = {
            "command": "python3.12 -m mcp_proxy",
            "args": [url]
        }
    
    # Save updated Windsurf config
    with open(WINDSURF_CONFIG_PATH, 'w') as f:
        json.dump(windsurf_config, f, indent=2)
    
    print(f"Synchronized with Windsurf MCP config at {WINDSURF_CONFIG_PATH}")
    
    # Create or update memory about using the proxy
    create_proxy_memory()


def create_proxy_memory() -> None:
    """
    Create or update a memory about using the MCP proxy.
    
    This function creates a memory in Windsurf's memory store that instructs
    the AI assistant to use the MCP Hive Proxy for all MCP server interactions.
    This ensures that the intelligent question matching and parameter handling
    features are leveraged consistently.
    """
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
    """
    Sync the MCP CLI configuration with Cursor's MCP config.
    
    Note: This is a placeholder for future implementation.
    Currently, Cursor integration is not fully implemented.
    """
    print("Cursor integration not yet implemented")


def delete_all_servers(sync_windsurf: bool = False, sync_cursor: bool = False) -> None:
    """
    Delete all servers from the configuration.
    
    Args:
        sync_windsurf: Whether to sync with Windsurf's MCP config
        sync_cursor: Whether to sync with Cursor's MCP config
    
    This function removes all server configurations and the default server setting.
    If sync_windsurf is True, it also updates the Windsurf configuration to remove
    all servers.
    """
    config = load_config()
    
    # Clear the servers dictionary
    config["servers"] = {}
    
    # Remove default server setting
    if "default_server" in config:
        del config["default_server"]
    
    # Save the updated config
    save_config(config)
    
    # Sync with Windsurf and/or Cursor if requested
    if sync_windsurf:
        sync_with_windsurf()
    
    if sync_cursor:
        sync_with_cursor()
