# Hive MCP

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
pip install hive-mcp
```

## Usage

### Asking Questions

```bash
# Ask a question to the default server
hive-mcp ask "What is the best AI tool for coding?"

# Ask a question to a specific server by name
hive-mcp ask --server team-mcp "What tools are being used in this team room?"

# Ask a question to a specific server by URL
hive-mcp ask --url https://mcp-server.example.com/sse "What is the weather today?"
```

### Managing Servers

```bash
# List all configured servers
hive-mcp servers list

# Add a new server
hive-mcp servers add my-server https://mcp-server.example.com/sse

# Remove a server
hive-mcp servers remove my-server

# Set the default server
hive-mcp servers set-default tweet-finder-mcp

# Export server configuration
hive-mcp servers export --file servers.json

# Import server configuration
hive-mcp servers import servers.json
```

## Configuration

The CLI stores its configuration in `~/.config/hive_mcp/config.json`. This file is created automatically when you first run the CLI, and it contains:

- A list of configured servers with their URLs
- The default server to use when none is specified

## Requirements

- Python 3.9 or higher
- `hive-mcp` package (installed automatically as a dependency)

## License

MIT
