#!/usr/bin/env python3
"""
示例：使用 MultiServerMCPClient 连接多个 MCP 服务器

本示例演示如何使用 MultiServerMCPClient 同时连接到多个 MCP 服务器并使用它们的工具。
演示通过手动调用 connect_to_server() 和 disconnect() 方法来连接多个 MCP 服务器。
为了避免异步上下文管理器带来的复杂性和可能的错误，本示例只使用手动连接方式。
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import Dict, Union

# 将项目根目录添加到 Python 路径
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

# 使用绝对导入路径
from openai_mcp_agents.mcp_agent import MultiServerMCPClient, StdioConnection, SSEConnection
from agents import Runner, RunConfig


async def run_multi_mcp_demo(temp_dir: Path, connections: Dict[str, Union[StdioConnection, SSEConnection]]):
    """通过手动调用 connect_to_server() 和 disconnect() 方法演示 MultiServerMCPClient
    
    Args:
        temp_dir: 测试目录
        connections: MCP 服务器连接配置
        
    Returns:
        执行结果
    """
    print("\n使用 MultiServerMCPClient 连接多个 MCP 服务器")

    # 创建 MultiServerMCPClient 实例
    client = MultiServerMCPClient(
        name="Multi-MCP Assistant",
        instructions="你是一个可以访问文件系统和网络的助手",
        model="gpt-4o",
        connections=connections,
    )

    try:
        # 手动连接到文件系统服务器
        await client.connect_to_server("filesystem")

        # 手动连接到 fetch 服务器
        await client.connect_to_server("git")

        # 获取所有可用工具
        tools = client.get_tools()
        print(f"已加载 {len(tools)} 个工具")

        # 列出每个服务器的工具
        for server_name, agent in client.mcp_agents.items():
            print(f"服务器 '{server_name}' 提供了 {len(agent.tools)} 个工具")

        # 运行交互
        print("\n运行 MultiServerMCPClient (手动连接/断开)...")
        result = await Runner.run(
            client,
            input=f"请获取 'https://google.com' 的内容，然后在 {temp_dir} 中创建一个名为 'example_content.txt' 的文件并写入内容。",
            context={},
            run_config=RunConfig(tracing_disabled=True)
        )

        # 输出结果
        print(f"\n结果: {result.final_output}")
        return result
    finally:
        # 确保完成后断开连接，即使发生异常
        await client.disconnect()


async def main():
    """主函数，运行 MultiServerMCPClient 示例"""
    print("启动 MultiServerMCPClient 示例...")

    # 设置 MCP 配置
    # 创建测试目录
    temp_dir = Path("/Users/madroid/Desktop/mcp_test_dir")
    os.makedirs(temp_dir, exist_ok=True)

    # 创建测试文件用于后续操作
    test_file_path = temp_dir / "test_file.txt"
    with open(test_file_path, "w") as f:
        f.write("这是一个测试文件，用于演示 MultiServerMCPClient 与多个 MCP 服务器的交互。")

    try:
        # 配置多个 MCP 服务器连接
        connections = {
            "filesystem": StdioConnection(
                transport="stdio",
                command="npx",
                args=["-y", "@modelcontextprotocol/server-filesystem", str(temp_dir)],
                env=None,
                encoding="utf-8",
                encoding_error_handler="strict"
            ),
            "git": StdioConnection(
                transport="stdio",
                command="uvx",
                args=["mcp-server-git", "--repository", "/Users/madroid/develop/workspace/openai-mcp-agents"],
                env=None,
                encoding="utf-8",
                encoding_error_handler="strict"
            )
        }

        # 运行多 MCP 服务器连接示例
        await run_multi_mcp_demo(temp_dir, connections)

    except Exception as e:
        print(f"发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
