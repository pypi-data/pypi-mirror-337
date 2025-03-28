"""
Main CLI entry point for the MCP CLI
"""
import argparse
import sys

from .commands import ask, servers


def create_parser() -> argparse.ArgumentParser:
    """
    Create the argument parser for the CLI.
    
    Returns:
        The configured argument parser
    """
    parser = argparse.ArgumentParser(
        description="Command-line interface for interacting with MCP servers"
    )
    
    # Create subparsers for commands
    subparsers = parser.add_subparsers(
        title="commands",
        dest="command",
        help="Command to run"
    )
    
    # Add command parsers
    ask.add_parser(subparsers)
    servers.add_parser(subparsers)
    
    return parser


def main() -> None:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not hasattr(args, 'func'):
        parser.print_help()
        sys.exit(1)
    
    # Call the handler function for the selected command
    args.func(args)


if __name__ == "__main__":
    main()
