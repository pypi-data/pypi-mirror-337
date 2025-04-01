"""
Server management commands for MCP CLI.
"""
import argparse
import json
import os
from pathlib import Path
from typing import Dict, Optional

CONFIG_DIR = os.path.expanduser("~/.config/mcp_cli")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


def ensure_config_dir():
    """Ensure the config directory exists."""
    os.makedirs(CONFIG_DIR, exist_ok=True)


def load_config() -> Dict:
    """Load the configuration from the config file."""
    ensure_config_dir()
    if not os.path.exists(CONFIG_FILE):
        return {"servers": {}, "default_server": None}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def save_config(config: Dict):
    """Save the configuration to the config file."""
    ensure_config_dir()
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def add_server_command(args):
    """Add a server to the configuration."""
    config = load_config()
    config["servers"][args.name] = args.url
    if args.default or not config["default_server"]:
        config["default_server"] = args.name
    save_config(config)
    print(f"Server '{args.name}' added successfully.")


def remove_server_command(args):
    """Remove a server from the configuration."""
    config = load_config()
    if args.name in config["servers"]:
        del config["servers"][args.name]
        if config["default_server"] == args.name:
            config["default_server"] = next(iter(config["servers"]), None)
        save_config(config)
        print(f"Server '{args.name}' removed successfully.")
    else:
        print(f"Server '{args.name}' not found.")


def list_servers_command(args):
    """List all servers in the configuration."""
    config = load_config()
    print("Configured MCP Servers:")
    print("----------------------")
    if not config["servers"]:
        print("No servers configured.")
        return
    for name, url in config["servers"].items():
        default_marker = " (default)" if name == config["default_server"] else ""
        print(f"{name}{default_marker}: {url}")


def set_default_command(args):
    """Set the default server."""
    config = load_config()
    if args.name in config["servers"]:
        config["default_server"] = args.name
        save_config(config)
        print(f"Default server set to '{args.name}'.")
    else:
        print(f"Server '{args.name}' not found.")


def import_servers_command(args):
    """Import servers from a JSON file."""
    if not os.path.exists(args.file):
        print(f"File '{args.file}' not found.")
        return
    try:
        with open(args.file, "r") as f:
            imported = json.load(f)
        config = load_config()
        for name, url in imported.get("servers", {}).items():
            config["servers"][name] = url
        if "default_server" in imported and imported["default_server"] in config["servers"]:
            config["default_server"] = imported["default_server"]
        save_config(config)
        print(f"Servers imported successfully from '{args.file}'.")
    except json.JSONDecodeError:
        print(f"Error: '{args.file}' is not a valid JSON file.")


def export_servers_command(args):
    """Export servers to a JSON file."""
    config = load_config()
    with open(args.file, "w") as f:
        json.dump(config, f, indent=2)
    print(f"Servers exported successfully to '{args.file}'.")


def get_server_url(server_name: Optional[str] = None) -> Optional[str]:
    """Get the URL for a server."""
    config = load_config()
    if not server_name:
        server_name = config["default_server"]
    if not server_name or server_name not in config["servers"]:
        return None
    return config["servers"][server_name]


def setup_servers_parser(servers_parser):
    """Set up the servers command parser."""
    servers_subparsers = servers_parser.add_subparsers(
        dest="servers_command", help="Servers command to run"
    )
    servers_subparsers.required = True

    # Add server command
    add_parser = servers_subparsers.add_parser("add", help="Add a new MCP server")
    add_parser.add_argument("name", help="Name of the server")
    add_parser.add_argument("url", help="URL of the server")
    add_parser.add_argument(
        "--default", action="store_true", help="Set as the default server"
    )
    add_parser.set_defaults(func=add_server_command)

    # Remove server command
    remove_parser = servers_subparsers.add_parser(
        "remove", help="Remove an MCP server"
    )
    remove_parser.add_argument("name", help="Name of the server to remove")
    remove_parser.set_defaults(func=remove_server_command)

    # List servers command
    list_parser = servers_subparsers.add_parser(
        "list", help="List all configured MCP servers"
    )
    list_parser.set_defaults(func=list_servers_command)

    # Set default server command
    default_parser = servers_subparsers.add_parser(
        "default", help="Set the default MCP server"
    )
    default_parser.add_argument("name", help="Name of the server to set as default")
    default_parser.set_defaults(func=set_default_command)

    # Import servers command
    import_parser = servers_subparsers.add_parser(
        "import", help="Import MCP servers from a JSON file"
    )
    import_parser.add_argument("file", help="Path to the JSON file to import from")
    import_parser.set_defaults(func=import_servers_command)

    # Export servers command
    export_parser = servers_subparsers.add_parser(
        "export", help="Export MCP servers to a JSON file"
    )
    export_parser.add_argument("file", help="Path to the JSON file to export to")
    export_parser.set_defaults(func=export_servers_command)
