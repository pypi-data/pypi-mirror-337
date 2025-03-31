# MCP Standalone

A standalone implementation of the MCP client without external dependencies. This package provides a command-line interface for interacting with MCP servers, with no dependency on the external `mcp` package.

## Features

- Connect to any MCP server using the SSE protocol
- Ask questions to MCP servers with automatic tool detection
- Manage server configurations with an easy-to-use CLI
- Support for servers with predefined questions
- Automatic question matching for servers that require specific questions

## Installation

You can install the package directly from the source:

```bash
cd /path/to/mcp-standalone
pip install -e .
```

Or build and install the package:

```bash
cd /path/to/mcp-standalone
pip install build
python -m build
pip install dist/mcp_standalone-0.1.0-py3-none-any.whl
```

## Usage

### Ask a question to an MCP server

```bash
# Ask a question to the default server
mcp-standalone ask "What is the weather today?"

# Ask a question to a specific server
mcp-standalone ask "What is the weather today?" --server trilogy-mcp

# Ask a question to a custom URL
mcp-standalone ask "What is the weather today?" --url https://mcp-server.example.com/sse

# List available predefined questions for a server
mcp-standalone ask --list-questions --server trilogy-mcp
```

### Manage server configurations

```bash
# List all configured servers
mcp-standalone servers list

# Add a new server
mcp-standalone servers add my-server https://mcp-server.example.com/sse

# Remove a server
mcp-standalone servers remove my-server

# Set the default server
mcp-standalone servers set-default trilogy-mcp

# Export server configurations
mcp-standalone servers export --file servers.json

# Import server configurations
mcp-standalone servers import servers.json
```

## Configuration

The package stores server configurations in `~/.config/mcp_standalone/config.json`. This file is created automatically with default servers when you first run the tool.

## Requirements

- Python 3.8 or higher
- httpx
- httpx-sse
- anyio
- pydantic
- pydantic-settings
