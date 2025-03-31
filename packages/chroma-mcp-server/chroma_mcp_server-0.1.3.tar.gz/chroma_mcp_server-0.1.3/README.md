# Chroma MCP Server

A Model Context Protocol (MCP) server integration for [Chroma](https://www.trychroma.com/), the open-source embedding database.

## Overview

The Chroma MCP Server allows you to connect AI applications with Chroma through the Model Context Protocol. This enables AI models to:

- Store and retrieve embeddings
- Perform semantic search on vector data
- Manage collections of embeddings
- Support RAG (Retrieval Augmented Generation) workflows

## Installation

### Basic Installation

```bash
pip install chroma-mcp-server
```

### Full Installation (with embedding models)

```bash
pip install chroma-mcp-server[full]
```

## Usage

### Starting the server

```bash
# Using the command-line executable
chroma-mcp-server

# Or using the Python module
python -m chroma_mcp.server
```

Or use the provided scripts during development:

```bash
# For development environment
./develop.sh

# To build the package
./build.sh

# To publish to PyPI
./publish.sh
```

### Configuration

The server can be configured with command-line options or environment variables:

#### Command-line Options

```bash
chroma-mcp-server --client-type persistent --data-dir ./my_data
```

#### Environment Variables

```bash
export CHROMA_CLIENT_TYPE=persistent
export CHROMA_DATA_DIR=./my_data
chroma-mcp-server
```

#### Available Configuration Options

- `--client-type`: Type of Chroma client (`ephemeral`, `persistent`, `http`, `cloud`)
- `--data-dir`: Path to data directory for persistent client
- `--log-dir`: Path to log directory
- `--host`: Host address for HTTP client
- `--port`: Port for HTTP client
- `--ssl`: Whether to use SSL for HTTP client
- `--tenant`: Tenant ID for Cloud client
- `--database`: Database name for Cloud client
- `--api-key`: API key for Cloud client
- `--cpu-execution-provider`: Force CPU execution provider for embedding functions (`auto`, `true`, `false`)

### Cursor Integration

To use with Cursor, add the following to your `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "chroma": {
      "command": "chroma-mcp-server",
      "args": [],
      "env": {
        "CHROMA_CLIENT_TYPE": "persistent",
        "CHROMA_DATA_DIR": "/path/to/data/dir",
        "CHROMA_LOG_DIR": "/path/to/logs/dir",
        "LOG_LEVEL": "INFO",
        "MCP_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Smithery Integration

This MCP server is compatible with [Smithery](https://smithery.ai/). See the `smithery.yaml` file for configuration details.

## Development

This project uses [Hatch](https://hatch.pypa.io/) for development and package management.

### Setting Up Development Environment

```bash
# Install Hatch globally
pip install hatch

# Create and activate a development environment
hatch shell
```

### Running Tests

```bash
# Run all tests
hatch run python -m pytest

# Run with coverage
hatch run python -m pytest --cov=chroma_mcp

# Using the test script (with coverage)
./test.sh
```

### Building the Package

```bash
# Build both wheel and sdist
hatch build

# Or use the script
./build.sh
```

## Dependencies

The package has optimized dependencies organized into groups:

- **Core**: Required for basic functionality (`python-dotenv`, `pydantic`, `fastapi`, `chromadb`, etc.)
- **Full**: Optional for extended functionality (`sentence-transformers`, `onnxruntime`, etc.)
- **Dev**: Only needed for development and testing

## License

MIT (see [LICENSE.md](LICENSE.md))
