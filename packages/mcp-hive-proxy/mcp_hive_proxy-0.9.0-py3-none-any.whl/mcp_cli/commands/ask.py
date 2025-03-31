"""
Implementation of the 'ask' command for MCP CLI
"""
import asyncio
import json
import difflib
from typing import Optional, Dict, Any, List, Tuple

from mcp.client.sse import sse_client
from mcp import ClientSession

from mcp_cli.config import get_server_url


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


async def ask_mcp(server_url: str, question: str, tool_name: Optional[str] = None, list_questions: bool = False) -> Dict[str, Any]:
    """
    Ask a question to an MCP server and return the response.
    
    Args:
        server_url: The URL of the MCP server
        question: The question to ask
        tool_name: Optional specific tool to use (if None, will try to auto-detect)
        list_questions: Whether to just list available questions (if applicable)
    
    Returns:
        The response from the MCP server
    """
    print(f"Connecting to {server_url}...")
    
    async with sse_client(server_url) as (read, write):
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
            
            for tool in tools.tools:
                if 'list' in tool.name.lower() and 'question' in tool.name.lower():
                    list_tool = tool.name
                elif any(keyword in tool.name.lower() for keyword in ['answer', 'ask']) and 'question' in tool.name.lower():
                    answer_tool = tool.name
            
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
                        for tool in tools.tools:
                            if tool.name == answer_tool and tool.inputSchema and 'required' in tool.inputSchema:
                                required_params = tool.inputSchema['required']
                                properties = tool.inputSchema.get('properties', {})
                                
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
            if not tool_name:
                # Look for tools that might handle questions or chat
                for tool in tools.tools:
                    if any(keyword in tool.name.lower() for keyword in 
                           ['question', 'ask', 'chat', 'complete', 'tweet']):
                        tool_name = tool.name
                        break
                
                if not tool_name and tools.tools:
                    # Just use the first tool if we couldn't find a better match
                    tool_name = tools.tools[0].name
                
                print(f"Auto-selected tool: {tool_name}")
            
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
            params = {param_name: question}
            print(f"Parameters: {params}")
            result = await session.call_tool(tool_name, params)
            
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


def ask_command(question: str, server: Optional[str] = None, url: Optional[str] = None, list_questions: bool = False) -> None:
    """
    CLI command to ask a question to an MCP server.
    
    Args:
        question: The question to ask
        server: The name of the server to use (from config)
        url: The URL of the server to use (overrides server)
        list_questions: Whether to just list available questions (if applicable)
    """
    try:
        # Determine the server URL
        server_url = url if url else get_server_url(server)
        
        response = asyncio.run(ask_mcp(server_url, question, list_questions=list_questions))
        
        # Pretty print the response
        print(json.dumps(response, indent=2))
        
    except KeyError as e:
        print(f"Configuration error: {str(e)}")
    except ConnectionError as e:
        print(f"Connection error: {str(e)}")
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {str(e)}")
    except asyncio.TimeoutError:
        print("Connection timed out. Please check your network connection and try again.")
    except Exception as e:
        print(f"Error: {str(e)}")
