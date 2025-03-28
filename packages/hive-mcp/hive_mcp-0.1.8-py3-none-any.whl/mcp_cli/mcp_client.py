"""
Simplified MCP client implementation without requiring the mcp package
"""
import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Tuple, AsyncGenerator
from urllib.parse import urljoin

import httpx
from httpx_sse import aconnect_sse

logger = logging.getLogger(__name__)

class SimpleMCPClient:
    """A simplified client for interacting with MCP servers."""
    
    def __init__(self, server_url: str):
        """
        Initialize the client with a server URL.
        
        Args:
            server_url: The URL of the MCP server
        """
        self.server_url = server_url
        self.client = httpx.AsyncClient()
        self.session_id = None
        self.tools = []
        self.endpoint_url = None
        self.request_id = 0
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    async def close(self):
        """Close the client connection."""
        if self.client:
            await self.client.aclose()
    
    def _get_next_request_id(self) -> int:
        """Get the next request ID."""
        self.request_id += 1
        return self.request_id
    
    async def connect(self):
        """Connect to the MCP server and get the endpoint URL."""
        print(f"Connecting to {self.server_url}...")
        
        try:
            # First establish SSE connection to get the endpoint URL
            async with httpx.AsyncClient() as client:
                async with aconnect_sse(client, "GET", self.server_url, timeout=30.0) as event_source:
                    print("SSE connection established")
                    
                    # Wait for the endpoint event
                    async for event in event_source.aiter_sse():
                        if event.event == "endpoint":
                            # Get the endpoint URL from the event data
                            self.endpoint_url = urljoin(self.server_url, event.data)
                            print(f"Received endpoint URL: {self.endpoint_url}")
                            break
            
            # Now initialize the session with the endpoint URL
            await self.initialize_session()
                
        except Exception as e:
            print(f"Error connecting to server: {str(e)}")
            raise
    
    async def initialize_session(self):
        """Initialize a session with the MCP server."""
        if not self.endpoint_url:
            raise ValueError("No endpoint URL available. Call connect() first.")
        
        # Send initialize message
        init_message = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "protocolVersion": "0.1.0",
                "capabilities": {
                    "sampling": {},
                    "roots": {"listChanged": True}
                },
                "clientInfo": {
                    "name": "hive-mcp",
                    "version": "0.1.8"
                }
            },
            "id": self._get_next_request_id()
        }
        
        try:
            response = await self.client.post(
                self.endpoint_url,
                json=init_message,
                headers={"Content-Type": "application/json"},
                timeout=30.0
            )
            response.raise_for_status()
            
            # Process the response
            response_data = response.json()
            if "result" in response_data:
                self.session_id = response_data.get("result", {}).get("sessionId")
                print(f"Session initialized with ID: {self.session_id}")
                
                # Send initialized notification
                await self._send_notification("notifications/initialized", {})
            elif "error" in response_data:
                error = response_data.get("error", {})
                raise Exception(f"Error initializing session: {error.get('message', 'Unknown error')}")
                
        except Exception as e:
            print(f"Error initializing session: {str(e)}")
            raise
    
    async def _send_notification(self, method: str, params: Dict[str, Any]) -> None:
        """
        Send a notification to the MCP server.
        
        Args:
            method: The notification method
            params: The notification parameters
        """
        notification = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }
        
        try:
            response = await self.client.post(
                self.endpoint_url,
                json=notification,
                headers={"Content-Type": "application/json"},
                timeout=30.0
            )
            response.raise_for_status()
        except Exception as e:
            print(f"Error sending notification: {str(e)}")
            raise
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """
        List the available tools on the MCP server.
        
        Returns:
            A list of tool definitions
        """
        if not self.session_id:
            await self.connect()
        
        # Send list tools message
        list_tools_message = {
            "jsonrpc": "2.0",
            "method": "tools/list",
            "params": {
                "sessionId": self.session_id
            },
            "id": self._get_next_request_id()
        }
        
        try:
            response = await self.client.post(
                self.endpoint_url,
                json=list_tools_message,
                headers={"Content-Type": "application/json"},
                timeout=30.0
            )
            response.raise_for_status()
            
            response_data = response.json()
            if "result" in response_data:
                self.tools = response_data.get("result", {}).get("tools", [])
                print(f"Available tools: {[tool.get('name') for tool in self.tools]}")
                return self.tools
            elif "error" in response_data:
                error = response_data.get("error", {})
                raise Exception(f"Error listing tools: {error.get('message', 'Unknown error')}")
                
        except Exception as e:
            print(f"Error listing tools: {str(e)}")
            raise
        
        return []
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a tool on the MCP server.
        
        Args:
            tool_name: The name of the tool to call
            arguments: The arguments to pass to the tool
        
        Returns:
            The response from the tool
        """
        if not self.session_id:
            await self.connect()
        
        if not self.tools:
            await self.list_tools()
        
        # Send call tool message
        call_tool_message = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "sessionId": self.session_id,
                "name": tool_name,
                "arguments": arguments
            },
            "id": self._get_next_request_id()
        }
        
        try:
            response = await self.client.post(
                self.endpoint_url,
                json=call_tool_message,
                headers={"Content-Type": "application/json"},
                timeout=30.0
            )
            response.raise_for_status()
            
            response_data = response.json()
            if "result" in response_data:
                result = response_data.get("result", {})
                if "content" in result:
                    for content in result["content"]:
                        if content.get("type") == "text":
                            try:
                                return json.loads(content.get("text", "{}"))
                            except json.JSONDecodeError:
                                return {"response": content.get("text", "")}
                return result
            elif "error" in response_data:
                error = response_data.get("error", {})
                raise Exception(f"Error calling tool: {error.get('message', 'Unknown error')}")
                
        except Exception as e:
            print(f"Error calling tool: {str(e)}")
            raise
        
        return {}


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
