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
    setup_servers_parser
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
    setup_servers_parser(servers_parser)
    
    return parser


def main(args: Optional[List[str]] = None) -> int:
    """Run the CLI with the given arguments."""
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    if not hasattr(parsed_args, "command"):
        parser.print_help()
        return 1
    
    try:
        if parsed_args.command == "ask":
            return ask_command(
                question=parsed_args.question,
                server=parsed_args.server,
                url=parsed_args.url,
                tool=parsed_args.tool,
                list_questions=parsed_args.list_questions,
                verbose=parsed_args.verbose
            )
        elif parsed_args.command == "servers":
            if not hasattr(parsed_args, "servers_command"):
                parser.parse_args(["servers", "--help"])
                return 1
                
            if parsed_args.servers_command == "list":
                list_servers_command(parsed_args)
            elif parsed_args.servers_command == "add":
                add_server_command(parsed_args)
            elif parsed_args.servers_command == "remove":
                remove_server_command(parsed_args)
            elif parsed_args.servers_command == "default":
                set_default_command(parsed_args)
            elif parsed_args.servers_command == "export":
                export_servers_command(parsed_args)
            elif parsed_args.servers_command == "import":
                import_servers_command(parsed_args)
            return 0
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 130
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
