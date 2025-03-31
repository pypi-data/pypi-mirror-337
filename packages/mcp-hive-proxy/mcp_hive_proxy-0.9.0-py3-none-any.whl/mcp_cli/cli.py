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
    import_servers_command,
    delete_all_servers_command
)


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        description="""MCP Hive Proxy - A command-line interface for interacting with MCP servers
        
This tool provides:
- Intelligent question matching for MCP servers with predefined questions
- Server configuration management with easy add, remove, and list operations
- Windsurf/Cursor integration for AI assistant compatibility
- Automatic parameter handling for specialized MCP servers
- Import/export functionality for server configurations

For full documentation, visit: https://github.com/trilogy-group/mcp-hive-proxy
""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Ask command
    ask_parser = subparsers.add_parser("ask", help="Ask a question to an MCP server", 
                                      description="Ask questions to any MCP server with intelligent question matching")
    ask_parser.add_argument("question", help="The question to ask")
    server_group = ask_parser.add_mutually_exclusive_group()
    server_group.add_argument("--server", "-s", help="The name of the server to use (from config)")
    server_group.add_argument("--url", "-u", help="The URL of the server to use (overrides server)")
    ask_parser.add_argument("--list-questions", action="store_true", help="List available predefined questions for servers that support them")
    
    # Servers command
    servers_parser = subparsers.add_parser("servers", help="Manage MCP server configurations",
                                          description="Add, remove, list, and manage MCP server configurations")
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
    
    # Delete all servers
    delete_all_parser = servers_subparsers.add_parser("delete-all", help="Delete ALL server configurations",
                                                    description="Delete all configured MCP servers. Use with caution!")
    delete_all_parser.add_argument("--sync-windsurf", action="store_true", help="Sync with Windsurf's MCP configuration")
    delete_all_parser.add_argument("--sync-cursor", action="store_true", help="Sync with Cursor's MCP configuration")
    delete_all_parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation prompt")
    
    # Set default server
    default_parser = servers_subparsers.add_parser("set-default", help="Set the default server")
    default_parser.add_argument("name", help="The name of the server to set as default")
    
    # Export servers
    export_parser = servers_subparsers.add_parser("export", help="Export server configurations to a file")
    export_parser.add_argument("--file", "-f", help="The file to export to (defaults to stdout)")
    
    # Import servers
    import_parser = servers_subparsers.add_parser("import", help="Import server configurations from a file")
    import_parser.add_argument("file", help="The file to import from")
    import_parser.add_argument("--sync-windsurf", action="store_true", help="Sync with Windsurf's MCP configuration")
    import_parser.add_argument("--sync-cursor", action="store_true", help="Sync with Cursor's MCP configuration")
    
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
        return 0
    
    if parsed_args.command == "servers":
        if not parsed_args.servers_command:
            # Default to list if no subcommand provided
            list_servers_command()
            return 0
        
        if parsed_args.servers_command == "list":
            list_servers_command()
        elif parsed_args.servers_command == "add":
            add_server_command(
                name=parsed_args.name,
                url=parsed_args.url,
                sync_windsurf=parsed_args.sync_windsurf,
                sync_cursor=parsed_args.sync_cursor
            )
        elif parsed_args.servers_command == "remove":
            remove_server_command(
                name=parsed_args.name,
                sync_windsurf=parsed_args.sync_windsurf,
                sync_cursor=parsed_args.sync_cursor
            )
        elif parsed_args.servers_command == "delete-all":
            delete_all_servers_command(
                sync_windsurf=parsed_args.sync_windsurf,
                sync_cursor=parsed_args.sync_cursor,
                confirm=parsed_args.yes
            )
        elif parsed_args.servers_command == "set-default":
            set_default_command(name=parsed_args.name)
        elif parsed_args.servers_command == "export":
            export_servers_command(file_path=parsed_args.file)
        elif parsed_args.servers_command == "import":
            import_servers_command(
                file_path=parsed_args.file,
                sync_windsurf=parsed_args.sync_windsurf,
                sync_cursor=parsed_args.sync_cursor
            )
        else:
            print(f"Unknown servers command: {parsed_args.servers_command}")
            return 1
        
        return 0
    
    print(f"Unknown command: {parsed_args.command}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
