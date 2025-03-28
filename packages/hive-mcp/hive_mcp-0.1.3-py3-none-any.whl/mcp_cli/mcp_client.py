"""
Simplified MCP client implementation without requiring the mcp package
"""
import asyncio
import json
from typing import Dict, Any, Optional, List, Tuple, AsyncGenerator

import httpx
from httpx_sse import aconnect_sse


class SimpleMCPClient:
    """A simplified MCP client that connects to an MCP server via SSE."""

    def __init__(self, server_url: str):
        """
        Initialize the MCP client.
        
        Args:
            server_url: The URL of the MCP server to connect to
        """
        self.server_url = server_url
        self.session_id = None
        self.client = None
        self.sse_client = None
        self.tools = []
    
    async def __aenter__(self):
        """Enter the async context."""
        self.client = httpx.AsyncClient()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit the async context."""
        if self.client:
            await self.client.aclose()
    
    async def connect(self) -> None:
        """Connect to the MCP server."""
        print(f"Connecting to {self.server_url}...")
        try:
            # Fix: Use the context manager properly
            self.sse_client = aconnect_sse(self.client, "GET", self.server_url)
            # Don't await here, we'll await when we use it
            print("Connection established")
        except Exception as e:
            print(f"Error connecting to server: {str(e)}")
            raise
    
    async def initialize_session(self) -> None:
        """Initialize a session with the MCP server."""
        if not self.sse_client:
            await self.connect()
        
        # Send initialize message
        init_message = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {},
            "id": 1
        }
        
        try:
            await self._send_message(init_message)
            
            # Wait for response
            async with self.sse_client as event_source:
                async for event in event_source.aiter_sse():
                    if event.event == "message":
                        try:
                            response = json.loads(event.data)
                            if response.get("id") == 1:
                                self.session_id = response.get("result", {}).get("sessionId")
                                print("Session initialized")
                                break
                        except json.JSONDecodeError:
                            print(f"Error parsing response: {event.data}")
        except Exception as e:
            print(f"Error initializing session: {str(e)}")
            raise
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """
        List the available tools on the MCP server.
        
        Returns:
            A list of tool definitions
        """
        if not self.session_id:
            await self.initialize_session()
        
        # Send list tools message
        list_tools_message = {
            "jsonrpc": "2.0",
            "method": "listTools",
            "params": {},
            "id": 2
        }
        
        try:
            await self._send_message(list_tools_message)
            
            # Wait for response
            async with self.sse_client as event_source:
                async for event in event_source.aiter_sse():
                    if event.event == "message":
                        try:
                            response = json.loads(event.data)
                            if response.get("id") == 2:
                                self.tools = response.get("result", {}).get("tools", [])
                                print(f"Available tools: {[tool.get('name') for tool in self.tools]}")
                                return self.tools
                        except json.JSONDecodeError:
                            print(f"Error parsing response: {event.data}")
        except Exception as e:
            print(f"Error listing tools: {str(e)}")
            raise
        
        return []
    
    async def call_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a tool on the MCP server.
        
        Args:
            tool_name: The name of the tool to call
            params: The parameters to pass to the tool
        
        Returns:
            The response from the tool
        """
        if not self.session_id:
            await self.initialize_session()
        
        if not self.tools:
            await self.list_tools()
        
        # Send call tool message
        call_tool_message = {
            "jsonrpc": "2.0",
            "method": "callTool",
            "params": {
                "name": tool_name,
                "input": params
            },
            "id": 3
        }
        
        try:
            await self._send_message(call_tool_message)
            
            # Wait for response
            result = {}
            async with self.sse_client as event_source:
                async for event in event_source.aiter_sse():
                    if event.event == "message":
                        try:
                            response = json.loads(event.data)
                            if response.get("id") == 3:
                                result = response.get("result", {})
                                if "content" in result:
                                    for content in result["content"]:
                                        if content.get("type") == "text":
                                            try:
                                                return json.loads(content.get("text", "{}"))
                                            except json.JSONDecodeError:
                                                return {"response": content.get("text", "")}
                                break
                        except json.JSONDecodeError:
                            print(f"Error parsing response: {event.data}")
        except Exception as e:
            print(f"Error calling tool: {str(e)}")
            raise
        
        return result
    
    async def _send_message(self, message: Dict[str, Any]) -> None:
        """
        Send a message to the MCP server.
        
        Args:
            message: The message to send
        """
        if self.session_id and "params" in message:
            message["params"]["sessionId"] = self.session_id
        
        try:
            response = await self.client.post(
                self.server_url,
                json=message,
                headers={"Content-Type": "application/json"},
                timeout=30.0  # Add a reasonable timeout
            )
            response.raise_for_status()  # Raise an exception for 4XX/5XX responses
        except Exception as e:
            print(f"Error sending message to server: {str(e)}")
            raise


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
    try:
        async with SimpleMCPClient(server_url) as client:
            try:
                await client.connect()
                await client.initialize_session()
                
                # If no tool name provided, try to find an appropriate one
                if not tool_name:
                    tools = await client.list_tools()
                    
                    # Look for tools that might handle questions or chat
                    for tool in tools:
                        if any(keyword in tool.get("name", "").lower() for keyword in 
                              ['question', 'ask', 'chat', 'complete', 'tweet']):
                            tool_name = tool.get("name")
                            break
                    
                    if not tool_name and tools:
                        # Just use the first tool if we couldn't find a better match
                        tool_name = tools[0].get("name")
                
                if not tool_name:
                    return {"error": "No suitable tools found on this MCP server"}
                
                print(f"Auto-selected tool: {tool_name}")
                
                # Determine the parameter name based on the tool's schema
                param_name = "question"  # Default
                for tool in client.tools:
                    if tool.get("name") == tool_name and "inputSchema" in tool and "properties" in tool["inputSchema"]:
                        properties = tool["inputSchema"]["properties"]
                        for prop in ['question', 'prompt', 'input', 'text', 'message']:
                            if prop in properties:
                                param_name = prop
                                break
                
                print(f"Asking question using {tool_name} with parameter {param_name}...")
                result = await client.call_tool(tool_name, {param_name: question})
                
                return result
            except Exception as e:
                print(f"Error: {str(e)}")
                return {"error": str(e)}
    except Exception as e:
        print(f"Error connecting to MCP server: {str(e)}")
        return {"error": str(e)}
