"""
Main CLI entry point for MCP CLI
"""
import argparse
import sys
from typing import List, Optional

from mcp_cli.commands.ask import ask_command
from mcp_cli.commands.servers import (
    list_servers_command,
    add_server_command,
    remove_server_command,
    set_default_command,
    export_servers_command,
    import_servers_command
)


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        description="MCP CLI - A command-line interface for interacting with MCP servers"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Ask command
    ask_parser = subparsers.add_parser("ask", help="Ask a question to an MCP server")
    ask_parser.add_argument("question", help="The question to ask")
    server_group = ask_parser.add_mutually_exclusive_group()
    server_group.add_argument("--server", "-s", help="The name of the server to use (from config)")
    server_group.add_argument("--url", "-u", help="The URL of the server to use (overrides server)")
    ask_parser.add_argument("--list-questions", action="store_true", help="List available predefined questions for servers that support them")
    
    # Servers command
    servers_parser = subparsers.add_parser("servers", help="Manage MCP server configurations")
    servers_subparsers = servers_parser.add_subparsers(dest="servers_command", help="Servers command to run")
    
    # List servers
    list_parser = servers_subparsers.add_parser("list", help="List all configured servers")
    
    # Add server
    add_parser = servers_subparsers.add_parser("add", help="Add a new server to the configuration")
    add_parser.add_argument("name", help="The name of the server")
    add_parser.add_argument("url", help="The URL of the server")
    add_parser.add_argument("--sync-windsurf", action="store_true", help="Sync with Windsurf's MCP configuration")
    add_parser.add_argument("--sync-cursor", action="store_true", help="Sync with Cursor's MCP configuration")
    
    # Remove server
    remove_parser = servers_subparsers.add_parser("remove", help="Remove a server from the configuration")
    remove_parser.add_argument("name", help="The name of the server to remove")
    remove_parser.add_argument("--sync-windsurf", action="store_true", help="Sync with Windsurf's MCP configuration")
    remove_parser.add_argument("--sync-cursor", action="store_true", help="Sync with Cursor's MCP configuration")
    
    # Set default server
    default_parser = servers_subparsers.add_parser("set-default", help="Set the default server")
    default_parser.add_argument("name", help="The name of the server to set as default")
    
    # Export servers
    export_parser = servers_subparsers.add_parser("export", help="Export servers configuration")
    export_parser.add_argument("--file", "-f", help="File to export to (if not specified, prints to stdout)")
    
    # Import servers
    import_parser = servers_subparsers.add_parser("import", help="Import servers configuration")
    import_parser.add_argument("file", help="File to import from")
    import_parser.add_argument("--sync-windsurf", action="store_true", help="Sync with Windsurf's MCP configuration after import")
    import_parser.add_argument("--sync-cursor", action="store_true", help="Sync with Cursor's MCP configuration after import")
    
    # Sync command
    sync_parser = servers_subparsers.add_parser("sync", help="Synchronize server configurations with other tools")
    sync_parser.add_argument("--windsurf", action="store_true", help="Sync with Windsurf's MCP configuration")
    sync_parser.add_argument("--cursor", action="store_true", help="Sync with Cursor's MCP configuration")
    
    return parser


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    if not parsed_args.command:
        parser.print_help()
        return 1
    
    if parsed_args.command == "ask":
        ask_command(
            question=parsed_args.question,
            server=parsed_args.server,
            url=parsed_args.url,
            list_questions=parsed_args.list_questions
        )
    elif parsed_args.command == "servers":
        if not parsed_args.servers_command:
            # Default to list if no subcommand specified
            list_servers_command()
        elif parsed_args.servers_command == "list":
            list_servers_command()
        elif parsed_args.servers_command == "add":
            add_server_command(
                parsed_args.name, 
                parsed_args.url,
                sync_windsurf=parsed_args.sync_windsurf,
                sync_cursor=parsed_args.sync_cursor
            )
        elif parsed_args.servers_command == "remove":
            remove_server_command(
                parsed_args.name,
                sync_windsurf=parsed_args.sync_windsurf,
                sync_cursor=parsed_args.sync_cursor
            )
        elif parsed_args.servers_command == "set-default":
            set_default_command(parsed_args.name)
        elif parsed_args.servers_command == "export":
            export_servers_command(parsed_args.file)
        elif parsed_args.servers_command == "import":
            import_servers_command(
                parsed_args.file,
                sync_windsurf=parsed_args.sync_windsurf,
                sync_cursor=parsed_args.sync_cursor
            )
        elif parsed_args.servers_command == "sync":
            if parsed_args.windsurf:
                from mcp_cli.config import sync_with_windsurf
                sync_with_windsurf()
            if parsed_args.cursor:
                from mcp_cli.config import sync_with_cursor
                sync_with_cursor()
            if not (parsed_args.windsurf or parsed_args.cursor):
                print("Error: Please specify at least one sync target (--windsurf or --cursor)")
                return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
