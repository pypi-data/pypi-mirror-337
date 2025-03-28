# OpenAI MCP Agents

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This project is an SDK that integrates [Model Context Protocol (MCP)](https://modelcontextprotocol.io) into OpenAI Agents. It allows you to easily provide MCP server functionality as tools for OpenAI Agents to use.

## Features

- Supports two connection types:
  - Stdio connection: Communicate with local processes via standard input/output
  - SSE connection: Communicate with remote servers via Server-Sent Events
- Supports two usage patterns:
  - Using async context manager (async with) for automatic connection management
  - Manual connection management via connect() and disconnect() methods
- Support for connecting to multiple MCP servers
- Full type hint support
- Detailed example code provided

## Installation

### Using uv (Recommended)

```bash
uv install git+https://github.com/madroidmaq/openai-mcp-agents.git
```

### Using pip

```bash
pip install git+https://github.com/madroidmaq/openai-mcp-agents.git
```

### Development Environment Setup

If you want to contribute to the project, you can set up your development environment as follows:

```bash
# Clone the repository
git clone https://github.com/madroidmaq/openai-mcp-agents.git
cd openai-mcp-agents

# Create a virtual environment and install dependencies using uv
uv venv
source .venv/bin/activate  # On Windows use .venv\Scripts\activate
uv pip install -e .
```

## Usage Examples

### Single Server Connection

```python
from openai_mcp_agents.mcp_agent import McpAgent
from mcp import StdioServerParameters

# Configure MCP server
server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"],
)

# Using async context manager
async with McpAgent(
    name="Filesystem Assistant",
    instructions="You are a filesystem assistant",
    mcp_server=server_params,
    model="gpt-4"
) as agent:
    result = await Runner.run(
        agent,
        input="Please list all files in the directory.",
        context={}
    )
    print(result.final_output)
```

### Multiple Server Connection

```python
from openai_mcp_agents.mcp_agent import MultiServerMCPClient

async with MultiServerMCPClient({
    "math": {
        "command": "python",
        "args": ["/path/to/math_server.py"],
        "transport": "stdio",
    },
    "weather": {
        "url": "http://localhost:8000/sse",
        "transport": "sse",
    }
}) as client:
    all_tools = client.get_tools()
    # Use the tools...
```

## API Documentation

### McpAgent

`McpAgent` class inherits from `Agent` class and is used to connect to a single MCP server.

```python
class McpAgent(Agent):
    def __init__(self,
        mcp_server: Optional[Union[StdioServerParameters, StdioConnection, SSEConnection]] = None,
        **kwargs):
        ...
```

### MultiServerMCPClient

`MultiServerMCPClient` class is used to connect to multiple MCP servers simultaneously.

```python
class MultiServerMCPClient(Agent):
    def __init__(self,
        connections: Optional[Dict[str, Union[StdioConnection, SSEConnection]]] = None,
        name: str = "MultiServerMCPClient",
        **kwargs):
        ...
```

## Contributing

Issues and Pull Requests are welcome!

### Contribution Process

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

This project uses [Black](https://github.com/psf/black) for code formatting and [mypy](http://mypy-lang.org/) for type checking. Please ensure you run these tools before submitting your code.

```bash
black src tests examples
mypy src
```

## License

[Apache License 2.0](LICENSE)

## Support

If you encounter any issues while using this project, please get support through the following channels:

1. Check the [documentation](https://github.com/madroidmaq/openai-mcp-agents/wiki)
2. Submit an [Issue](https://github.com/madroidmaq/openai-mcp-agents/issues)
3. Send an email to madroidmaq@gmail.com
