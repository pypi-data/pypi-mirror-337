# MCP CLI

A command-line interface for interacting with MCP (Model Context Protocol) servers.

## Features

- **Ask questions** to any MCP server directly from the command line
- **Manage server configurations** with easy add, remove, and list operations
- **Set default servers** for quick access
- **Import and export** server configurations

## Installation

```bash
# From the source directory
pip install -e .

# Or once published
pip install mcp-cli
```

## Usage

### Asking Questions

```bash
# Ask a question to the default server
mcp-cli ask "What is the best AI tool for coding?"

# Ask a question to a specific server by name
mcp-cli ask --server team-mcp "What tools are being used in this team room?"

# Ask a question to a specific server by URL
mcp-cli ask --url https://mcp-server.example.com/sse "What is the weather today?"
```

### Managing Servers

```bash
# List all configured servers
mcp-cli servers list

# Add a new server
mcp-cli servers add my-server https://mcp-server.example.com/sse

# Remove a server
mcp-cli servers remove my-server

# Set the default server
mcp-cli servers set-default tweet-finder-mcp

# Export server configuration
mcp-cli servers export --file servers.json

# Import server configuration
mcp-cli servers import servers.json
```

## Configuration

The CLI stores its configuration in `~/.config/mcp_cli/config.json`. This file is created automatically when you first run the CLI, and it contains:

- A list of configured servers with their URLs
- The default server to use when none is specified

## Requirements

- Python 3.9 or higher
- `mcp` package (installed automatically as a dependency)

## License

MIT
