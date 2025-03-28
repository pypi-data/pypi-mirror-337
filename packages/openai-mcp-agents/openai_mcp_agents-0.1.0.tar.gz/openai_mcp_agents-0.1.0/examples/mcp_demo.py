#!/usr/bin/env python3
"""
Example of using McpAgent to interact with Filesystem MCP Server
This example demonstrates how to use McpAgent to connect to Filesystem MCP Server and directly call tools

Two usage methods:
1. Using async context manager (async with)
2. Manually calling connect() and disconnect() methods
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import Any

from mcp import StdioServerParameters

# Add project root directory to Python path
project_root = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, project_root)  # Use insert(0, ...) to ensure our path has priority

# Use absolute import paths
from openai_mcp_agents.mcp_agent import McpAgent
# Use absolute import paths
from agents import Runner, RunConfig, AgentHooks, RunContextWrapper, Agent, Tool


class CustomAgentHooks(AgentHooks):
    def __init__(self, display_name: str):
        self.event_counter = 0
        self.display_name = display_name

    async def on_start(self, context: RunContextWrapper, agent: Agent) -> None:
        self.event_counter += 1
        print(f"### ({self.display_name}) {self.event_counter}: Agent {agent.name} started")

    async def on_end(self, context: RunContextWrapper, agent: Agent, output: Any) -> None:
        self.event_counter += 1
        print(
            f"### ({self.display_name}) {self.event_counter}: Agent {agent.name} ended with output {output}"
        )

    async def on_handoff(self, context: RunContextWrapper, agent: Agent, source: Agent) -> None:
        self.event_counter += 1
        print(
            f"### ({self.display_name}) {self.event_counter}: Agent {source.name} handed off to {agent.name}"
        )

    async def on_tool_start(self, context: RunContextWrapper, agent: Agent, tool: Tool) -> None:
        self.event_counter += 1
        print(
            f"### ({self.display_name}) {self.event_counter}: Agent {agent.name} started tool {tool.name}"
        )

    async def on_tool_end(
        self, context: RunContextWrapper, agent: Agent, tool: Tool, result: str
    ) -> None:
        self.event_counter += 1
        print(
            f"### ({self.display_name}) {self.event_counter}: Agent {agent.name} ended tool {tool.name} with result {result}"
        )


async def filesystem_agent(temp_dir: Path):
    """Demonstrate McpAgent using async context manager (async with)
    
    Args:
        temp_dir: Test directory
        
    Returns:
        Execution result
    """
    # Configure MCP server
    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", str(temp_dir)],
    )

    # Using async context manager (async with)
    async with McpAgent(
        name="Filesystem Assistant - Method 1",
        instructions="You are a filesystem assistant",
        mcp_server=server_params,
        model="gpt-4o",
        hooks=CustomAgentHooks("Filesystem")
    ) as agent:
        # Run agent for interaction
        print("\nRunning Agent (using async with)...")
        result = await Runner.run(
            agent,
            input=f"Please list all files in the {temp_dir} directory.",
            context={},
            run_config=RunConfig(tracing_disabled=True)
        )
        # Output result
        print(f"\nResult: {result.final_output}")
        return result


async def git_agent():
    """Demonstrate McpAgent by manually calling connect() and disconnect() methods
    
    Args:
        temp_dir: Test directory
        
    Returns:
        Execution result
    """

    git_dir = "/Users/madroid/develop/workspace/openai-mcp-agents"
    

    # fetch
    server_params = StdioServerParameters(
        command="uvx",
        args=["mcp-server-git", "--repository", str(git_dir)],
    )

    # Manually calling connect() and disconnect() methods
    agent = McpAgent(
        name="Git Assistant",
        instructions="You are a git assistant",
        mcp_server=server_params,
        model="gpt-4o",
        hooks=CustomAgentHooks("Git Assistant")
    )

    try:
        # Manual connection
        await agent.connect()

        # Run agent for interaction
        print("\nRunning Agent (manual connect/disconnect)...")
        result = await Runner.run(
            agent,
            input=f"当前仓库({git_dir})的提交记录是怎样的？",
            context={},
            run_config=RunConfig(tracing_disabled=True)
        )
        # Output result
        print(f"\nResult: {result.final_output}")
        return result
    finally:
        # Ensure disconnection after completion, even if an exception occurs
        await agent.disconnect()


async def main():
    """Main function, runs McpAgent example"""
    print("Starting McpAgent Filesystem example...")

    # Set up MCP configuration
    # Create test directory
    temp_dir = Path("/Users/madroid/Desktop/mcp_test_dir")
    os.makedirs(temp_dir, exist_ok=True)

    # Create a test file for subsequent operations
    test_file_path = temp_dir / "test_file.txt"
    with open(test_file_path, "w") as f:
        f.write("This is a test file for demonstrating interaction between McpAgent and Filesystem MCP Server.")

    try:
        # Demonstrate method 1: Using async context manager
        await filesystem_agent(temp_dir)

        # Demonstrate method 2: Manually calling connect() and disconnect()
        await git_agent()


    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
