"""
SSE client implementation for connecting to MCP servers
"""
import asyncio
import json
from typing import Any, Dict, List, Optional, Tuple, Callable, AsyncGenerator
import httpx
from httpx_sse import aconnect_sse, SSEError


class ToolSchema:
    """Schema for a tool in the MCP protocol"""
    def __init__(self, name: str, description: str, input_schema: Optional[Dict[str, Any]] = None):
        self.name = name
        self.description = description
        self.input_schema = input_schema


class ToolsList:
    """List of tools available on an MCP server"""
    def __init__(self, tools: List[ToolSchema]):
        self.tools = tools


class ContentItem:
    """Content item in an MCP response"""
    def __init__(self, content_type: str, text: str):
        self.type = content_type
        self.text = text


class ToolResult:
    """Result from calling a tool on an MCP server"""
    def __init__(self, content: List[ContentItem]):
        self.content = content


async def sse_client(url: str) -> Tuple[
    Callable[[], AsyncGenerator[Dict[str, Any], None]],
    Callable[[Dict[str, Any]], None]
]:
    """
    Create an SSE client connection to an MCP server.

    Args:
        url: The URL of the MCP server

    Returns:
        A tuple of (read, write) functions for communicating with the server
    """
    client = httpx.AsyncClient()
    request_id = 0
    write_queue = asyncio.Queue()
    read_queue = asyncio.Queue()

    async def reader() -> AsyncGenerator[Dict[str, Any], None]:
        """Read messages from the server"""
        while True:
            item = await read_queue.get()
            yield item
            read_queue.task_done()

    async def writer(data: Dict[str, Any]) -> None:
        """Write messages to the server"""
        await write_queue.put(data)

    async def connection_task():
        """Maintain the connection to the server"""
        nonlocal request_id

        try:
            async with aconnect_sse(client, "POST", url, json={}) as event_source:
                # Start a task to handle the write queue
                asyncio.create_task(handle_writes(client, url))

                async for event in event_source.aiter_sse():
                    if event.event == "message":
                        try:
                            data = json.loads(event.data)
                            await read_queue.put(data)
                        except json.JSONDecodeError as e:
                            print(f"Failed to parse SSE message: {event.data} - {e}")
                        except Exception as e:
                            print(f"Failed to parse SSE message: {event.data} - {e}")

        except SSEError as e:
            print(f"SSE connection error: {e}")
        except httpx.HTTPError as e:
            print(f"HTTP connection error: {e}")
        except ConnectionResetError as e:
            print(f"Connection reset error: {e}")
        except asyncio.CancelledError as e:
            print(f"Connection cancelled: {e}")
        except Exception as e:
            print(f"Connection error: {e}")
        finally:
            await client.aclose()

    async def handle_writes(client, url):
        """Handle writing messages to the server"""
        nonlocal request_id

        while True:
            data = await write_queue.get()
            request_id += 1

            try:
                data["requestId"] = str(request_id)
                await client.post(url, json=data)
            except httpx.HTTPError as e:
                print(f"Error sending message: {e}")
            except ConnectionResetError as e:
                print(f"Error sending message: {e}")
            except asyncio.CancelledError as e:
                print(f"Error sending message: {e}")
            except Exception as e:
                print(f"Error sending message: {e}")
            finally:
                write_queue.task_done()

    # Start the connection task
    asyncio.create_task(connection_task())

    return reader, writer


class ClientSession:
    """Session for interacting with an MCP server"""
    def __init__(self, read_fn, write_fn):
        self.read = read_fn
        self.write = write_fn
        self.reader = None

    async def __aenter__(self):
        self.reader = self.read()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.reader = None

    async def initialize(self):
        """Initialize the session"""
        await self.write({"type": "initialize"})
        async for message in self.reader:
            if message.get("type") == "initialize":
                return

    async def list_tools(self) -> ToolsList:
        """List the tools available on the server"""
        await self.write({"type": "listTools"})
        async for message in self.reader:
            if message.get("type") == "listTools":
                tools = []
                for tool in message.get("tools", []):
                    tools.append(ToolSchema(
                        name=tool.get("name", ""),
                        description=tool.get("description", ""),
                        input_schema=tool.get("inputSchema")
                    ))
                return ToolsList(tools)

    async def call_tool(self, tool_name: str, parameters: Dict[str, Any]) -> ToolResult:
        """
        Call a tool on the server

        Args:
            tool_name: The name of the tool to call
            parameters: The parameters to pass to the tool

        Returns:
            The result from the tool
        """
        await self.write({
            "type": "callTool",
            "name": tool_name,
            "parameters": parameters
        })

        content_items = []
        async for message in self.reader:
            if message.get("type") == "content":
                content_type = message.get("contentType", "text")
                content_text = message.get("content", "")
                content_items.append(ContentItem(content_type, content_text))
            elif message.get("type") == "toolResult":
                break

        return ToolResult(content_items)
