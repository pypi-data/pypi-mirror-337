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


async def find_best_matching_question(available_questions: List[str], user_question: str) -> Tuple[str, float]:
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
    matches = difflib.get_close_matches(user_question, available_questions, n=1, cutoff=0.0)
    if not matches:
        return "", 0.0
        
    best_match = matches[0]
    match_ratio = difflib.SequenceMatcher(None, user_question.lower(), best_match.lower()).ratio()
    return best_match, match_ratio


async def ask_mcp(server_url: str, question: str, tool_name: Optional[str] = None, list_questions: bool = False) -> Dict[str, Any]:
    """
    Ask a question to an MCP server and return the response.
    
    Args:
        server_url: The URL of the MCP server
        question: The question to ask
        tool_name: Optional specific tool to use (if None, will try to auto-detect)
        list_questions: If True, explicitly request available questions
    
    Returns:
        The response from the MCP server
    """
    async with sse_client(server_url) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Get available tools
            tools = await session.list_tools()
            if not tools.tools:
                return {"error": "No tools available on this MCP server"}
                
            # Check if this server has list_questions and answer_question tools
            has_list_questions_tool = any(tool.name.lower() == "list_questions" for tool in tools.tools)
            has_answer_question_tool = any(tool.name.lower() == "answer_question" for tool in tools.tools)
            has_team_question_tools = any("team_question" in tool.name.lower() for tool in tools.tools)
            
            # If we have both list and answer tools, this is a server with predefined questions
            is_predefined_questions_server = (has_list_questions_tool and has_answer_question_tool) or has_team_question_tools
            
            # If user explicitly wants to list questions or we detect a predefined questions server
            if list_questions or (is_predefined_questions_server and not tool_name):
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
