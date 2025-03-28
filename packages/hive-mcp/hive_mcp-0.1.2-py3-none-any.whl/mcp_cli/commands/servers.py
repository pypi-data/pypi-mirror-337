"""
Commands for managing MCP server configurations
"""
import argparse
import sys
from typing import Dict, Any

from ..config import load_config, save_config, get_server_url


def add_parser(subparsers):
    """Add the servers command parser to the subparsers."""
    parser = subparsers.add_parser(
        "servers", help="Manage MCP server configurations"
    )
    
    # Create subcommands for the servers command
    server_subparsers = parser.add_subparsers(
        title="server commands",
        help="Commands for managing MCP servers"
    )
    
    # List servers
    list_parser = server_subparsers.add_parser(
        "list", help="List configured servers"
    )
    list_parser.set_defaults(func=handle_list)
    
    # Add server
    add_parser = server_subparsers.add_parser(
        "add", help="Add a new server configuration"
    )
    add_parser.add_argument(
        "name", help="Name for the server"
    )
    add_parser.add_argument(
        "url", help="URL of the server"
    )
    add_parser.set_defaults(func=handle_add)
    
    # Remove server
    remove_parser = server_subparsers.add_parser(
        "remove", help="Remove a server configuration"
    )
    remove_parser.add_argument(
        "name", help="Name of the server to remove"
    )
    remove_parser.set_defaults(func=handle_remove)
    
    # Set default server
    default_parser = server_subparsers.add_parser(
        "default", help="Set the default server"
    )
    default_parser.add_argument(
        "name", help="Name of the server to set as default"
    )
    default_parser.set_defaults(func=handle_default)


def handle_list(args: argparse.Namespace) -> None:
    """
    Handle the servers list command.
    
    Args:
        args: Command line arguments
    """
    config = load_config()
    
    print("Configured MCP Servers:")
    print("======================")
    
    if "servers" not in config or not config["servers"]:
        print("No servers configured.")
        return
    
    default_server = config.get("default_server")
    
    for name, url in config["servers"].items():
        if name == default_server:
            print(f"* {name}: {url} (default)")
        else:
            print(f"  {name}: {url}")


def handle_add(args: argparse.Namespace) -> None:
    """
    Handle the servers add command.
    
    Args:
        args: Command line arguments
    """
    config = load_config()
    
    if "servers" not in config:
        config["servers"] = {}
    
    config["servers"][args.name] = args.url
    
    # If this is the first server, set it as default
    if len(config["servers"]) == 1:
        config["default_server"] = args.name
        print(f"Added server '{args.name}' and set as default.")
    else:
        print(f"Added server '{args.name}'.")
    
    save_config(config)


def handle_remove(args: argparse.Namespace) -> None:
    """
    Handle the servers remove command.
    
    Args:
        args: Command line arguments
    """
    config = load_config()
    
    if "servers" not in config or args.name not in config["servers"]:
        print(f"Error: Server '{args.name}' not found.")
        sys.exit(1)
    
    del config["servers"][args.name]
    
    # If we removed the default server, update the default
    if config.get("default_server") == args.name:
        if config["servers"]:
            # Set the first server as default
            config["default_server"] = next(iter(config["servers"]))
            print(f"Removed server '{args.name}' and set '{config['default_server']}' as default.")
        else:
            # No servers left
            config.pop("default_server", None)
            print(f"Removed server '{args.name}' (was default). No servers left.")
    else:
        print(f"Removed server '{args.name}'.")
    
    save_config(config)


def handle_default(args: argparse.Namespace) -> None:
    """
    Handle the servers default command.
    
    Args:
        args: Command line arguments
    """
    config = load_config()
    
    if "servers" not in config or args.name not in config["servers"]:
        print(f"Error: Server '{args.name}' not found.")
        sys.exit(1)
    
    config["default_server"] = args.name
    print(f"Set '{args.name}' as the default server.")
    
    save_config(config)
