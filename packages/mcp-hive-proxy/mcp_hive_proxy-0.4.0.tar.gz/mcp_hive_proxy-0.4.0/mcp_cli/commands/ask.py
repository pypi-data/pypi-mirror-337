"""
Implementation of the 'ask' command for MCP CLI
"""
import asyncio
import json
from typing import Optional, Dict, Any

from mcp.client.sse import sse_client
from mcp import ClientSession

from mcp_cli.config import get_server_url


async def ask_mcp(server_url: str, question: str, tool_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Ask a question to an MCP server and return the response.
    
    Args:
        server_url: The URL of the MCP server
        question: The question to ask
        tool_name: Optional specific tool to use (if None, will try to auto-detect)
    
    Returns:
        The response from the MCP server
    """
    async with sse_client(server_url) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # If no tool name provided, try to find an appropriate one
            if not tool_name:
                tools = await session.list_tools()
                
                # Look for tools that might handle questions or chat
                for tool in tools.tools:
                    if any(keyword in tool.name.lower() for keyword in 
                           ['question', 'ask', 'chat', 'complete', 'tweet']):
                        tool_name = tool.name
                        break
                
                if not tool_name and tools.tools:
                    # Just use the first tool if we couldn't find a better match
                    tool_name = tools.tools[0].name
            
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


def ask_command(question: str, server: Optional[str] = None, url: Optional[str] = None) -> None:
    """
    CLI command to ask a question to an MCP server.
    
    Args:
        question: The question to ask
        server: The name of the server to use (from config)
        url: The URL of the server to use (overrides server)
    """
    try:
        # Determine the server URL
        server_url = url if url else get_server_url(server)
        
        print(f"Connecting to {server_url}...")
        response = asyncio.run(ask_mcp(server_url, question))
        
        # Pretty print the response
        print(json.dumps(response, indent=2))
        
    except Exception as e:
        print(f"Error: {str(e)}")
