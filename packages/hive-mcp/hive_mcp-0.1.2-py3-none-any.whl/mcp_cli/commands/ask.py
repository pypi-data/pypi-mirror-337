"""
Command for asking questions to MCP servers
"""
import argparse
import asyncio
import json
import sys
from typing import Dict, Any, Optional

from ..config import load_config, get_server_url
from ..mcp_client import ask_mcp


def add_parser(subparsers):
    """Add the ask command parser to the subparsers."""
    parser = subparsers.add_parser(
        "ask", help="Ask a question to an MCP server"
    )
    parser.add_argument(
        "question", help="The question to ask"
    )
    parser.add_argument(
        "-s", "--server", help="Server name or URL to use"
    )
    parser.add_argument(
        "-t", "--tool", help="Specific tool to use (optional)"
    )
    parser.set_defaults(func=handle_ask)


def handle_ask(args: argparse.Namespace) -> None:
    """
    Handle the ask command.
    
    Args:
        args: Command line arguments
    """
    # Get the server URL
    config = load_config()
    server_url = None
    
    if args.server:
        # Check if it's a URL or a server name
        if args.server.startswith(("http://", "https://")):
            server_url = args.server
        else:
            server_url = get_server_url(config, args.server)
    else:
        # Use the default server
        default_server = config.get("default_server")
        if default_server:
            server_url = get_server_url(config, default_server)
    
    if not server_url:
        print("Error: No server specified and no default server configured.")
        print("Use 'hive-mcp servers add' to add a server or specify a URL.")
        sys.exit(1)
    
    # Ask the question
    try:
        response = asyncio.run(ask_mcp(server_url, args.question, args.tool))
        
        # Format the response nicely
        if isinstance(response, dict):
            if "error" in response:
                print(f"Error: {response['error']}")
                sys.exit(1)
            elif "response" in response:
                print(response["response"])
            else:
                print(json.dumps(response, indent=2))
        else:
            print(response)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
