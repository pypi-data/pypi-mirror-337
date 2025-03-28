"""
Configuration management for the MCP CLI
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


# Default configuration directory
CONFIG_DIR = os.path.expanduser("~/.config/mcp_cli")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


def ensure_config_dir() -> None:
    """Ensure the configuration directory exists."""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR, exist_ok=True)


def load_config() -> Dict[str, Any]:
    """
    Load the configuration from the config file.
    
    Returns:
        The configuration as a dictionary
    """
    ensure_config_dir()
    
    if not os.path.exists(CONFIG_FILE):
        # Create default config
        default_config = {
            "servers": {},
            "default_server": None
        }
        save_config(default_config)
        return default_config
    
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: Config file {CONFIG_FILE} is corrupted. Creating a new one.")
        default_config = {
            "servers": {},
            "default_server": None
        }
        save_config(default_config)
        return default_config


def save_config(config: Dict[str, Any]) -> None:
    """
    Save the configuration to the config file.
    
    Args:
        config: The configuration to save
    """
    ensure_config_dir()
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def get_server_url(config: Dict[str, Any], server_name: Optional[str] = None) -> Optional[str]:
    """
    Get the URL for a server by name.
    
    Args:
        config: The configuration dictionary
        server_name: The name of the server to get the URL for
    
    Returns:
        The URL of the server, or None if not found
    """
    if not server_name:
        # Use default server
        server_name = config.get("default_server")
        if not server_name:
            return None
    
    servers = config.get("servers", {})
    return servers.get(server_name)
