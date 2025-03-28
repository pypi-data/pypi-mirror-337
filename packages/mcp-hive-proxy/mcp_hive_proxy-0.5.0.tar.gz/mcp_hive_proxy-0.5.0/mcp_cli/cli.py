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
    ask_parser.add_argument("--list-questions", "-l", action="store_true", help="List available predefined questions for this server")
    
    # Servers command
    servers_parser = subparsers.add_parser("servers", help="Manage MCP server configurations")
    servers_subparsers = servers_parser.add_subparsers(dest="servers_command", help="Servers command to run")
    
    # List servers
    list_parser = servers_subparsers.add_parser("list", help="List all configured servers")
    
    # Add server
    add_parser = servers_subparsers.add_parser("add", help="Add a new server to the configuration")
    add_parser.add_argument("name", help="The name of the server")
    add_parser.add_argument("url", help="The URL of the server")
    
    # Remove server
    remove_parser = servers_subparsers.add_parser("remove", help="Remove a server from the configuration")
    remove_parser.add_argument("name", help="The name of the server to remove")
    
    # Set default server
    default_parser = servers_subparsers.add_parser("set-default", help="Set the default server")
    default_parser.add_argument("name", help="The name of the server to set as default")
    
    # Export servers
    export_parser = servers_subparsers.add_parser("export", help="Export servers configuration")
    export_parser.add_argument("--file", "-f", help="File to export to (if not specified, prints to stdout)")
    
    # Import servers
    import_parser = servers_subparsers.add_parser("import", help="Import servers configuration")
    import_parser.add_argument("file", help="File to import from")
    
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
            add_server_command(parsed_args.name, parsed_args.url)
        elif parsed_args.servers_command == "remove":
            remove_server_command(parsed_args.name)
        elif parsed_args.servers_command == "set-default":
            set_default_command(parsed_args.name)
        elif parsed_args.servers_command == "export":
            export_servers_command(parsed_args.file)
        elif parsed_args.servers_command == "import":
            import_servers_command(parsed_args.file)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
