# Sterling B2B Integrator/Filegateway MCP Server

A [Model Context Protocol][mcp] (MCP) server that enables AI assistants to interact with Sterling B2B/Filegateway through standardized interfaces.

[mcp]: https://modelcontextprotocol.io

## Features

- [x] Trading Partners
  - [x] List Trading Partners
- [] Filegateway Communities
  - [] List Trading Partners
- [] Discover and explore metrics
  - [] List available metrics
  - [] Get metadata for specific metrics
  - [] View instant query results
- [x] Authentication support
  - [x] Basic auth from environment variables
- [] Docker containerization support
- [] Provide interactive tools for AI assistants


The list of tools is configurable, so you can choose which tools you want to make available to the MCP client.
This is useful if you don't use certain functionality or if you don't want to take up too much of the context window.

## Usage

1. Ensure your Sterling B2Bi/Filegateway server is accessible from the environment where you'll run this MCP server.

2. Ensure your user has permission to access REST API services.

3. Configure the environment variables for your Sterling B2B server, either through a `.env` file or system environment variables:

```env
# Required: Sterling B2Bi/Filegateway configuration
B2BI_URL=http://your-sterling-b2bi-server:5000
B2BI_RESTAPI_URL=http://your-sterling-b2bi-server:5076

# Authentication credentials
B2BI_USERNAME=your_username
B2BI_PASSWORD=your_password
```

3. Add the server configuration to your client configuration file. For example, for Claude Desktop:

```json
{
  "mcpServers": {
    "sterlingb2b": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "B2BI_URL",
        "-e",
        "B2BI_RESTAPI_URL",
        "-e",
        "B2BI_USERNAME", 
        "-e",
        "B2BI_PASSWORD",
        "quay.io/ebasso/sterling-b2b-mcp-server:latest"
      ],
      "env": {
        "B2BI_URL": "<url>",
        "B2BI_RESTAPI_URL": "<url>",
        "B2BI_USERNAME": "<username>",
        "B2BI_PASSWORD": "<password>",
      }
    }
  }
}
```


## Development

Contributions are welcome! Please open an issue or submit a pull request if you have any suggestions or improvements.

This project uses [`uv`](https://github.com/astral-sh/uv) to manage dependencies. Install `uv` following the instructions for your platform:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

You can then create a virtual environment and install the dependencies with:

```bash
uv venv
source .venv/bin/activate  # On Unix/macOS
.venv\Scripts\activate     # On Windows
uv pip install -e .
```

## Project Structure

The project has been organized with a `src` directory structure:

```
sterling-b2b-mcp-server/
├── src/
│   └── sterling_b2b_mcp_server/
│       ├── __init__.py      # Package initialization
│       ├── server.py        # MCP server implementation
│       ├── sterling_b2b.py  # Sterling B2Bi/Filegateway Rest APIs helper
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose configuration
├── .dockerignore            # Docker ignore file
├── pyproject.toml           # Project configuration
└── README.md                # This file
```

### Testing

The project includes a comprehensive test suite that ensures functionality and helps prevent regressions.

Run the tests with pytest:

```bash
# Install development dependencies
uv pip install -e ".[dev]"

# Run the tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=term-missing
```
Tests are organized into:

- Configuration validation tests
- Server functionality tests
- Error handling tests
- Main application tests

When adding new features, please also add corresponding tests.

### Tools

| Tool | Category | Description |
|-------------------------------------| ----- | --- |
| `get_trading_partners`              | Query | List of all Trading Partners in Sterling B2Bi/Filegateway |
| `get_trading_partners_with_details` | Query | List of all Trading Partners with details in Sterling B2Bi/Filegateway |


## License

MIT

---

[mcp]: https://modelcontextprotocol.io