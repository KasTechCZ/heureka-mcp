# Heureka MCP

**Heureka MCP** (Model Context Protocol) service for integration with Heureka. This service allows AI assistants (such as Claude or ChatGPT) to search for products and offers on Heureka.

The service exposes tools for:
- Searching products
- Searching offers

## Requirements

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (package and environment manager)

## Installation and Setup

1.  **Clone the repository** and navigate to the project folder.

2.  **Set up environment variables**:
    Create a `.env` file by copying the example:
    ```bash
    cp .env.example .env
    ```
    Edit `.env` and fill in:
    - `GRAPHQL_URL`: URL of your GraphQL gateway (e.g., `https://api.heureka.cz/graphql`)

3.  **Install dependencies**:
    ```bash
    uv sync
    ```

## Usage

The service can be run locally using `uv`. The MCP server communicates via standard input/output (stdio) or SSE.

### Local Execution (Stdio)
```bash
uv run main.py
```

### Local Execution (SSE)
```bash
uv run main.py --sse
```

## Configuration for Claude Desktop

To connect with the **Claude Desktop** application (macOS/Windows), you need to modify the configuration file.

1.  Open the configuration file:
    - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
    - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2.  Add the configuration for `heureka-mcp`:

    ```json
    {
      "mcpServers": {
        "heureka-mcp": {
          "command": "/usr/local/bin/uv",
          "args": [
            "run",
            "--directory",
            "/absolute/path/to/heureka-mcp",
            "main.py"
          ],
          "env": {
            "GRAPHQL_URL": "https://api.heureka.cz/graphql"
          }
        }
      }
    }
    ```
    *Ensure that the path to `uv` (here `/usr/local/bin/uv`) and to the project matches your system.*

## Configuration for ChatGPT

To use with **ChatGPT** (using MCP via SSE transport):

1.  **Start the Server in SSE Mode**:
    Run the following command to start the MCP server listening for SSE connections:
    ```bash
    uv run main.py --sse
    ```
    The server will start on `http://localhost:8000` (default).

2.  **Configure ChatGPT**:
    In your MCP-enabled ChatGPT client configuration, add a new server:
    - **Type**: SSE
    - **URL**: `http://localhost:8000/sse`
