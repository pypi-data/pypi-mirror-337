"""
Main CLI entry point for MCP CLI
"""
import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

from mcp_cli.sse_client import sse_client, ClientSession
from mcp_cli.config import (
    list_servers,
    add_server,
    remove_server,
    set_default_server,
    get_server_url,
    export_servers_command,
    import_servers_command
)


async def find_best_matching_question(available_questions, user_question):
    """
    Find the best matching predefined question for a user's input.
    
    Args:
        available_questions: List of available predefined questions
        user_question: The question asked by the user
    
    Returns:
        Tuple of (best_match, match_ratio)
    """
    if not available_questions:
        return "", 0.0
        
    # Use difflib to find the closest match
    import difflib
    matches = difflib.get_close_matches(user_question, available_questions, n=1, cutoff=0.0)
    if not matches:
        return "", 0.0
        
    best_match = matches[0]
    match_ratio = difflib.SequenceMatcher(None, user_question.lower(), best_match.lower()).ratio()
    return best_match, match_ratio


async def ask_mcp(server_url: str, question: str, list_questions: bool = False) -> Dict[str, Any]:
    """
    Ask a question to an MCP server and return the response.
    
    Args:
        server_url: The URL of the MCP server
        question: The question to ask
        list_questions: If True, explicitly request available questions
    
    Returns:
        The response from the MCP server
    """
    print(f"Connecting to {server_url}...")
    
    async with sse_client(server_url) as (read, write):
        print("Connection established")
        
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("Session initialized")
            
            # Get available tools
            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")
            
            # Check if this server has list_questions and answer_question tools
            has_list_questions_tool = any(tool.name.lower() == "list_questions" for tool in tools.tools)
            has_answer_question_tool = any(tool.name.lower() == "answer_question" for tool in tools.tools)
            has_team_question_tools = any("team_question" in tool.name.lower() for tool in tools.tools)
            
            # If we have both list and answer tools, this is a server with predefined questions
            is_predefined_questions_server = (has_list_questions_tool and has_answer_question_tool) or has_team_question_tools
            
            # If user explicitly wants to list questions or we detect a predefined questions server
            if list_questions or (is_predefined_questions_server and not question):
                # Find the appropriate tool for listing questions
                list_tool = next((tool.name for tool in tools.tools if tool.name.lower() == "list_questions"), None)
                if not list_tool and has_team_question_tools:
                    list_tool = next((tool.name for tool in tools.tools if "list" in tool.name.lower() and "team" in tool.name.lower()), None)
                
                if list_tool:
                    # Get the list of available questions
                    result = await session.call_tool(list_tool, {})
                    if result.content:
                        for content in result.content:
                            if content.type == 'text':
                                try:
                                    questions_data = json.loads(content.text)
                                    # If explicitly asked to list questions, return them
                                    if list_questions:
                                        return questions_data
                                    
                                    # Otherwise, try to find the best matching question
                                    if "questions" in questions_data:
                                        available_questions = list(questions_data["questions"].keys())
                                        best_match, match_ratio = await find_best_matching_question(available_questions, question)
                                        
                                        # If we have a good match, use the answer_question tool with the matched question
                                        if match_ratio > 0.7:  # 70% similarity threshold
                                            answer_tool = next((tool.name for tool in tools.tools if tool.name.lower() == "answer_question"), None)
                                            if not answer_tool and has_team_question_tools:
                                                answer_tool = next((tool.name for tool in tools.tools if "answer" in tool.name.lower() and "team" in tool.name.lower()), None)
                                            
                                            if answer_tool:
                                                print(f"Using matched question: '{best_match}'")
                                                result = await session.call_tool(answer_tool, {"question": best_match})
                                                for content in result.content:
                                                    if content.type == 'text':
                                                        try:
                                                            return json.loads(content.text)
                                                        except json.JSONDecodeError:
                                                            return {"response": content.text}
                                        else:
                                            # No good match, suggest the closest question
                                            questions_data["suggestion"] = f"Your question didn't match any predefined questions. Did you mean: '{best_match}'?"
                                            return questions_data
                                except json.JSONDecodeError:
                                    pass
            
            # If no tool name provided, try to find an appropriate one
            tool_name = None
            # Look for tools that might handle questions or chat
            for tool in tools.tools:
                if any(keyword in tool.name.lower() for keyword in 
                       ['question', 'ask', 'chat', 'complete', 'tweet']):
                    tool_name = tool.name
                    print(f"Auto-selected tool: {tool_name}")
                    break
            
            if not tool_name and tools.tools:
                # Just use the first tool if we couldn't find a better match
                tool_name = tools.tools[0].name
                print(f"Defaulting to first available tool: {tool_name}")
            
            if not tool_name:
                return {"error": "No suitable tools found on this MCP server"}
            
            # Determine the parameter name based on the tool's schema
            param_name = "question"  # Default
            for tool in tools.tools:
                if tool.name == tool_name and tool.inputSchema and 'properties' in tool.inputSchema:
                    properties = tool.inputSchema['properties']
                    for prop in ['question', 'prompt', 'input', 'text', 'message']:
                        if prop in properties:
                            param_name = prop
                            break
            
            print(f"Asking question using {tool_name} with parameter {param_name}...")
            
            result = await session.call_tool(tool_name, {param_name: question})
            
            # Process the response
            if result.content:
                for content in result.content:
                    if content.type == 'text':
                        try:
                            # Try to parse as JSON for better formatting
                            return json.loads(content.text)
                        except json.JSONDecodeError:
                            # Not JSON, use as is
                            return {"response": content.text}
            
            return {"error": "No response content"}


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


def ask_command(question: str, server: Optional[str] = None, url: Optional[str] = None, list_questions: bool = False) -> None:
    """
    CLI command to ask a question to an MCP server.
    
    Args:
        question: The question to ask
        server: The name of the server to use (from config)
        url: The URL of the server to use (overrides server)
        list_questions: If True, explicitly request available questions
    """
    try:
        # Determine the server URL
        server_url = url if url else get_server_url(server)
        
        print(f"Connecting to {server_url}...")
        response = asyncio.run(ask_mcp(server_url, question, list_questions=list_questions))
        
        # Pretty print the response
        print(json.dumps(response, indent=2))
        
    except Exception as e:
        print(f"Error: {str(e)}")


def list_servers_command() -> None:
    """List all configured servers."""
    servers = list_servers()
    
    print("Configured MCP Servers:")
    print("----------------------")
    
    if not servers:
        print("No servers configured.")
        return
    
    default_server = None
    try:
        default_server = get_server_url(None)
    except:
        pass
    
    for name, url in servers.items():
        default_marker = " (default)" if url == default_server else ""
        print(f"{name}{default_marker}: {url}")


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
            add_server(parsed_args.name, parsed_args.url)
            print(f"Server '{parsed_args.name}' added successfully.")
        elif parsed_args.servers_command == "remove":
            remove_server(parsed_args.name)
            print(f"Server '{parsed_args.name}' removed successfully.")
        elif parsed_args.servers_command == "set-default":
            set_default_server(parsed_args.name)
            print(f"Server '{parsed_args.name}' set as default.")
        elif parsed_args.servers_command == "export":
            export_servers_command(parsed_args.file)
        elif parsed_args.servers_command == "import":
            import_servers_command(parsed_args.file)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
