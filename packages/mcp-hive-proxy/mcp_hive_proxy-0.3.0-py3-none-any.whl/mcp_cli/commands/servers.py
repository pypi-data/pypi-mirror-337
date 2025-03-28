"""
Implementation of the 'servers' command for MCP CLI
"""
from typing import Optional
import json

from mcp_cli.config import (
    list_servers,
    add_server,
    remove_server,
    set_default_server,
    load_config,
    sync_with_windsurf,
    sync_with_cursor
)


def list_servers_command() -> None:
    """List all configured servers."""
    servers = list_servers()
    config = load_config()
    default_server = config.get("default_server")
    
    print("Configured MCP Servers:")
    print("----------------------")
    
    if not servers:
        print("No servers configured.")
        return
    
    for name, url in servers.items():
        default_marker = " (default)" if name == default_server else ""
        print(f"{name}{default_marker}: {url}")


def add_server_command(name: str, url: str, sync_windsurf: bool = False, sync_cursor: bool = False) -> None:
    """
    Add a new server to the configuration.
    
    Args:
        name: The name of the server
        url: The URL of the server
        sync_windsurf: Whether to sync with Windsurf's MCP config
        sync_cursor: Whether to sync with Cursor's MCP config
    """
    try:
        add_server(name, url, sync_windsurf=sync_windsurf, sync_cursor=sync_cursor)
        print(f"Server '{name}' added successfully.")
    except Exception as e:
        print(f"Error adding server: {str(e)}")


def remove_server_command(name: str, sync_windsurf: bool = False, sync_cursor: bool = False) -> None:
    """
    Remove a server from the configuration.
    
    Args:
        name: The name of the server to remove
        sync_windsurf: Whether to sync with Windsurf's MCP config
        sync_cursor: Whether to sync with Cursor's MCP config
    """
    try:
        remove_server(name, sync_windsurf=sync_windsurf, sync_cursor=sync_cursor)
        print(f"Server '{name}' removed successfully.")
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Error removing server: {str(e)}")


def set_default_command(name: str) -> None:
    """Set the default server."""
    try:
        set_default_server(name)
        print(f"Default server set to '{name}'.")
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Error setting default server: {str(e)}")


def export_servers_command(file_path: Optional[str] = None) -> None:
    """Export servers configuration to a file."""
    servers = list_servers()
    config = load_config()
    
    export_data = {
        "servers": servers,
        "default_server": config.get("default_server")
    }
    
    if file_path:
        try:
            with open(file_path, 'w') as f:
                json.dump(export_data, f, indent=2)
            print(f"Servers exported to {file_path}")
        except Exception as e:
            print(f"Error exporting servers: {str(e)}")
    else:
        # Print to stdout
        print(json.dumps(export_data, indent=2))


def import_servers_command(file_path: str, sync_windsurf: bool = False, sync_cursor: bool = False) -> None:
    """
    Import servers configuration from a file.
    
    Args:
        file_path: Path to the file to import from
        sync_windsurf: Whether to sync with Windsurf's MCP config
        sync_cursor: Whether to sync with Cursor's MCP config
    """
    try:
        with open(file_path, 'r') as f:
            import_data = json.load(f)
        
        if not isinstance(import_data, dict):
            print("Error: Invalid import file format.")
            return
        
        servers = import_data.get("servers", {})
        if not servers:
            print("Error: No servers found in import file.")
            return
        
        default_server = import_data.get("default_server")
        
        # Add each server
        for name, url in servers.items():
            try:
                add_server(name, url)
                print(f"Server '{name}' imported successfully.")
            except Exception as e:
                print(f"Error importing server '{name}': {str(e)}")
        
        # Set default server if specified
        if default_server:
            try:
                set_default_server(default_server)
                print(f"Default server set to '{default_server}'.")
            except Exception as e:
                print(f"Error setting default server: {str(e)}")
        
        # Sync with Windsurf and/or Cursor if requested
        if sync_windsurf:
            sync_with_windsurf()
        
        if sync_cursor:
            sync_with_cursor()
            
    except json.JSONDecodeError:
        print(f"Error: File '{file_path}' is not valid JSON.")
    except Exception as e:
        print(f"Error importing servers: {str(e)}")
