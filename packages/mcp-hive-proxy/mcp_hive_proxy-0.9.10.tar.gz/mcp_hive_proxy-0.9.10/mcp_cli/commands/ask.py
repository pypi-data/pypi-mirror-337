"""
Implementation of the 'ask' command for MCP CLI
"""
import asyncio
import json
import difflib
import aiohttp
import urllib.parse
from typing import Optional, Dict, Any, List, Tuple, AsyncGenerator

from mcp_cli.config import get_server_url


# Simple SSE client implementation to replace mcp.client.sse
async def sse_client(url: str):
    """
    Create an SSE client for the given URL.
    
    Args:
        url: The URL of the SSE endpoint
        
    Returns:
        A tuple of (read, write) functions for the SSE connection
    """
    class SSEClient:
        def __init__(self, url):
            self.url = url
            self.session = None
            self.response = None
            
        async def __aenter__(self):
            self.session = aiohttp.ClientSession()
            self.response = await self.session.get(self.url)
            return self.read, self.write
            
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            if self.response:
                await self.response.release()
            if self.session:
                await self.session.close()
        
        async def read(self) -> AsyncGenerator[Dict[str, Any], None]:
            """Read events from the SSE stream."""
            buffer = ""
            async for line in self.response.content:
                line = line.decode('utf-8')
                if line.strip() == "":
                    # Empty line, end of event
                    if buffer:
                        event_data = {}
                        for part in buffer.split("\n"):
                            if part.startswith("data: "):
                                try:
                                    event_data = json.loads(part[6:])
                                except json.JSONDecodeError:
                                    event_data = {"data": part[6:]}
                        buffer = ""
                        yield event_data
                else:
                    buffer += line
        
        async def write(self, data: Dict[str, Any]) -> None:
            """Write data to the SSE stream."""
            async with self.session.post(
                urllib.parse.urljoin(self.url, "write"),
                json=data
            ) as response:
                await response.text()
    
    return SSEClient(url)


# Simple client session to replace mcp.ClientSession
class ClientSession:
    def __init__(self, read, write):
        self.read = read
        self.write = write
        self.tools = None
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
    
    async def initialize(self):
        """Initialize the session."""
        await self.write({"type": "initialize"})
        async for event in self.read():
            if event.get("type") == "initialized":
                return
    
    async def list_tools(self):
        """List available tools."""
        await self.write({"type": "list_tools"})
        async for event in self.read():
            if event.get("type") == "tools_listed":
                self.tools = ToolsList(event.get("tools", []))
                return self.tools
    
    async def call_tool(self, tool_name: str, params: Dict[str, Any]):
        """Call a tool with the given parameters."""
        await self.write({
            "type": "call_tool",
            "tool": tool_name,
            "params": params
        })
        
        result = ToolResult()
        async for event in self.read():
            if event.get("type") == "tool_result":
                result.content.append(Content(event.get("content_type", "text"), event.get("content", "")))
            elif event.get("type") == "tool_call_done":
                return result


# Simple classes to replace mcp package classes
class ToolsList:
    def __init__(self, tools):
        self.tools = [Tool(t.get("name", ""), t.get("inputSchema", {})) for t in tools]


class Tool:
    def __init__(self, name, input_schema):
        self.name = name
        self.inputSchema = input_schema


class Content:
    def __init__(self, type, text):
        self.type = type
        self.text = text


class ToolResult:
    def __init__(self):
        self.content = []


def find_best_matching_question(user_question: str, available_questions: List[str]) -> Tuple[str, float]:
    """
    Find the best matching question from a list of available questions.
    
    Args:
        user_question: The question asked by the user
        available_questions: List of available predefined questions
    
    Returns:
        Tuple of (best matching question, match ratio)
    """
    if not available_questions:
        return "", 0.0
    
    # Convert to lowercase for better matching
    user_question_lower = user_question.lower()
    
    # Find the best match using difflib
    matches = [(q, difflib.SequenceMatcher(None, user_question_lower, q.lower()).ratio()) 
               for q in available_questions]
    
    # Sort by match ratio (highest first)
    matches.sort(key=lambda x: x[1], reverse=True)
    
    # Return the best match
    return matches[0]


async def ask_mcp(server_url: str, question: str, tool: Optional[str] = None, list_questions: bool = False) -> Dict[str, Any]:
    """
    Ask a question to an MCP server and return the response.
    
    Args:
        server_url: The URL of the MCP server
        question: The question to ask
        tool: Optional specific tool to use (if None, will try to auto-detect)
        list_questions: Whether to just list available questions (if applicable)
    
    Returns:
        The response from the MCP server
    """
    print(f"Connecting to {server_url}...")
    
    async with sse_client(server_url) as client:
        read, write = client
        async with ClientSession(read, write) as session:
            print("Connection established")
            await session.initialize()
            print("Session initialized")
            
            # Get available tools
            tools = await session.list_tools()
            available_tools = [tool.name for tool in tools.tools]
            print(f"Available tools: {available_tools}")
            
            # Check if this server has both list and answer tools (pattern for predefined questions)
            list_tool = None
            answer_tool = None
            
            for tool_name in tools.tools:
                if 'list' in tool_name.name.lower() and 'question' in tool_name.name.lower():
                    list_tool = tool_name.name
                elif any(keyword in tool_name.name.lower() for keyword in ['answer', 'ask']) and 'question' in tool_name.name.lower():
                    answer_tool = tool_name.name
            
            # If we have both list and answer tools, use them together
            if list_tool and answer_tool:
                # First, get the list of available questions
                print(f"Checking available questions using {list_tool}...")
                list_result = await session.call_tool(list_tool, {})
                
                questions_data = {}
                if list_result.content:
                    for content in list_result.content:
                        if content.type == 'text':
                            try:
                                result_json = json.loads(content.text)
                                if 'questions' in result_json:
                                    questions_data = result_json['questions']
                                    break
                            except json.JSONDecodeError:
                                pass
                
                # If we just want to list questions, return them now
                if list_questions:
                    return {"questions": questions_data}
                
                # Find the best matching question
                if questions_data:
                    available_questions = list(questions_data.keys())
                    best_match, match_ratio = find_best_matching_question(question, available_questions)
                    
                    if match_ratio > 0.6:  # Threshold for a good match
                        print(f"Using best matching question: '{best_match}'")
                        
                        # Get the s3_key if available
                        s3_key = questions_data.get(best_match)
                        if s3_key:
                            print(f"Using s3_key: {s3_key}")
                        
                        # Prepare parameters for the answer tool
                        params = {"question": best_match}
                        
                        # Add s3_key if available
                        if s3_key:
                            params["s3_key"] = s3_key
                        
                        # Check if the tool requires additional parameters
                        for tool_name in tools.tools:
                            if tool_name.name == answer_tool and tool_name.inputSchema and 'required' in tool_name.inputSchema:
                                required_params = tool_name.inputSchema['required']
                                properties = tool_name.inputSchema.get('properties', {})
                                
                                # Add required parameters with default values if they're not already set
                                if 'start_date' in required_params and 'start_date' not in params:
                                    params['start_date'] = '2025-01-01'
                                if 'end_date' in required_params and 'end_date' not in params:
                                    params['end_date'] = '2025-12-31'
                        
                        print(f"Asking question using {answer_tool} with parameter question...")
                        print(f"Parameters: {params}")
                        result = await session.call_tool(answer_tool, params)
                        
                        # Process the response
                        if result.content:
                            for content in result.content:
                                if content.type == 'text':
                                    try:
                                        return json.loads(content.text)
                                    except json.JSONDecodeError:
                                        return {"response": content.text}
                        
                        return {"error": "No response content"}
            
            # If no tool name provided, try to find an appropriate one
            if not tool:
                # Look for tools that might handle questions or chat
                for tool_name in tools.tools:
                    if any(keyword in tool_name.name.lower() for keyword in 
                           ['question', 'ask', 'chat', 'complete', 'tweet']):
                        tool = tool_name.name
                        break
                
                if not tool and tools.tools:
                    # Just use the first tool if we couldn't find a better match
                    tool = tools.tools[0].name
                
                print(f"Auto-selected tool: {tool}")
            
            if not tool:
                return {"error": "No suitable tools found on this MCP server"}
            
            # Determine the parameter name based on the tool's schema
            param_name = "question"  # Default
            for tool_name in tools.tools:
                if tool_name.name == tool and tool_name.inputSchema and 'properties' in tool_name.inputSchema:
                    properties = tool_name.inputSchema['properties']
                    for prop in ['question', 'prompt', 'input', 'text', 'message']:
                        if prop in properties:
                            param_name = prop
                            break
            
            print(f"Asking question using {tool} with parameter {param_name}...")
            params = {param_name: question}
            print(f"Parameters: {params}")
            result = await session.call_tool(tool, params)
            
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


def ask_command(question: str, server: Optional[str] = None, url: Optional[str] = None, 
                list_questions: bool = False, tool: Optional[str] = None, verbose: bool = False):
    """
    CLI command to ask a question to an MCP server.
    
    Args:
        question: The question to ask
        server: The name of the server to use (from config)
        url: The URL of the server to use (overrides server)
        list_questions: Whether to just list available questions (if applicable)
        tool: Optional specific tool to use
        verbose: Whether to show verbose output
    """
    if not url:
        if server:
            url = get_server_url(server)
        else:
            url = get_server_url()
            
    if not url:
        print("Error: No server URL provided and no default server configured.")
        print("Use --url to specify a server URL or configure a default server with 'mcp-hive-proxy servers add'.")
        return 1
        
    try:
        response = asyncio.run(ask_mcp(url, question, tool, list_questions))
        print(response)
        return 0
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
