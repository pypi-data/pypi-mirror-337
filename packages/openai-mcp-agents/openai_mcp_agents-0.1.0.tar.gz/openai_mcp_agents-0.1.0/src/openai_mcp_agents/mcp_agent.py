from __future__ import annotations

import logging
from contextlib import AsyncExitStack
from types import TracebackType
from typing import Any, Dict, List, Literal, Optional, TypedDict, Union

from agents import Agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client

from .tools import load_mcp_tools

# Configure logging
logger = logging.getLogger(__name__)

# 默认值
DEFAULT_ENCODING = "utf-8"
DEFAULT_ENCODING_ERROR_HANDLER = "strict"

DEFAULT_HTTP_TIMEOUT = 5
DEFAULT_SSE_READ_TIMEOUT = 60 * 5


class StdioConnection(TypedDict):
    transport: Literal["stdio"]

    command: str
    """要运行以启动服务器的可执行文件。"""

    args: List[str]
    """传递给可执行文件的命令行参数。"""

    env: Optional[Dict[str, str]]
    """生成进程时使用的环境。"""

    encoding: str
    """向服务器发送/接收消息时使用的文本编码。"""

    encoding_error_handler: Literal["strict", "ignore", "replace"]
    """
    文本编码错误处理程序。

    有关可能值的解释，请参阅 https://docs.python.org/3/library/codecs.html#codec-base-classes
    """


class SSEConnection(TypedDict):
    transport: Literal["sse"]

    url: str
    """要连接的 SSE 端点的 URL。"""

    headers: Optional[Dict[str, Any]]
    """发送到 SSE 端点的 HTTP 头"""

    timeout: float
    """HTTP 超时时间"""

    sse_read_timeout: float
    """SSE 读取超时时间"""


class McpAgent(Agent):
    """
    Agent implementation using MCP protocol.
    
    McpAgent inherits from Agent class and connects to the server via MCP protocol
    to obtain and use tools.
    
    支持两种连接方式：
    1. Stdio 连接：通过标准输入/输出与本地进程通信
    2. SSE 连接：通过 Server-Sent Events 与远程服务器通信
    
    This class supports the async context manager protocol (async with), which
    automatically initializes the agent on entry and cleans up resources on exit.
    """

    def __init__(
        self,
        mcp_server: Optional[Union[StdioServerParameters, StdioConnection, SSEConnection]] = None,
        **kwargs,
    ):
        """
        Initialize McpAgent.
        
        Args:
            mcp_server: MCP protocol configuration，可以是以下类型之一：
                - StdioServerParameters: 用于 stdio 连接的参数对象
                - StdioConnection: 用于 stdio 连接的配置字典
                - SSEConnection: 用于 SSE 连接的配置字典
            **kwargs: Other parameters passed to parent class
        """
        self.mcp_server = mcp_server
        self.session: Optional[ClientSession] = None
        self.exit_stack = None

        super().__init__(
            tools=[],
            **kwargs,
        )

    # 删除 _connection_client 方法，直接在 connect 方法中处理

    async def connect(self):
        """
        Initialize connection to MCP server and get available tools.
        
        Raises:
            RuntimeError: If an error occurs during initialization
            ValueError: If configuration parameters are invalid
        """
        from contextlib import AsyncExitStack

        try:
            self.exit_stack = AsyncExitStack()

            # 根据不同类型的连接参数创建相应的连接
            if isinstance(self.mcp_server, StdioServerParameters):
                # 直接使用 StdioServerParameters
                logger.debug(f"Initializing MCP stdio connection with params: {self.mcp_server}")
                transport = await self.exit_stack.enter_async_context(stdio_client(self.mcp_server))
                read, write = transport

            # 检查是否是字典并包含 transport 字段
            elif isinstance(self.mcp_server, dict) and self.mcp_server.get("transport") == "stdio":
                # 从 StdioConnection 创建 StdioServerParameters
                if "command" not in self.mcp_server or "args" not in self.mcp_server:
                    raise ValueError("stdio 连接需要 'command' 和 'args' 参数")

                server_params = StdioServerParameters(
                    command=self.mcp_server["command"],
                    args=self.mcp_server["args"],
                    env=self.mcp_server.get("env"),
                    encoding=self.mcp_server.get("encoding", DEFAULT_ENCODING),
                    encoding_error_handler=self.mcp_server.get(
                        "encoding_error_handler", DEFAULT_ENCODING_ERROR_HANDLER
                    ),
                )
                logger.debug(f"Initializing MCP stdio connection with params: {server_params}")
                transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
                read, write = transport

            elif isinstance(self.mcp_server, dict) and self.mcp_server.get("transport") == "sse":
                # 创建 SSE 连接
                if "url" not in self.mcp_server:
                    raise ValueError("sse 连接需要 'url' 参数")

                url = self.mcp_server["url"]
                headers = self.mcp_server.get("headers")
                timeout = self.mcp_server.get("timeout", DEFAULT_HTTP_TIMEOUT)
                sse_read_timeout = self.mcp_server.get("sse_read_timeout", DEFAULT_SSE_READ_TIMEOUT)

                logger.debug(f"Initializing MCP SSE connection with URL: {url}")
                transport = await self.exit_stack.enter_async_context(
                    sse_client(url, headers, timeout, sse_read_timeout)
                )
                read, write = transport

            else:
                raise ValueError(f"不支持的连接类型或配置: {self.mcp_server}")

            # 创建并初始化会话
            self.session = await self.exit_stack.enter_async_context(ClientSession(read, write))
            await self.session.initialize()
            logger.info("MCP session initialized successfully")

            # Get available tools and convert to Agent tool format
            await self._update_tools()
        except Exception as e:
            # Ensure resources are cleaned up if initialization fails
            if self.exit_stack:
                await self.exit_stack.aclose()
                self.exit_stack = None
                self.session = None
            logger.error(f"Failed to initialize MCP agent: {e}")
            raise RuntimeError(f"Failed to initialize MCP agent: {e}") from e

    async def disconnect(self):
        """
        Clean up resources and close connection to MCP server.
        This method should be called after using McpAgent.
        """
        if self.exit_stack:
            try:
                await self.exit_stack.aclose()
                logger.info("MCP resources cleaned up successfully")
            except Exception as e:
                logger.error(f"Error during MCP resource cleanup: {e}")
            finally:
                self.exit_stack = None
                self.session = None

    async def __aenter__(self) -> McpAgent:
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    async def _update_tools(self):
        """
        从MCP服务器获取工具并更新Agent的tools属性。
        
        异常:
            RuntimeError: 如果MCP会话未初始化
        """
        if not self.session:
            raise RuntimeError("MCP会话未初始化。请先调用initialize()。")

        try:
            agent_tools = await load_mcp_tools(self.session)
            self.tools = agent_tools
            return agent_tools
        except Exception as e:
            logger.error(f"更新工具失败: {e}")
            raise RuntimeError(f"更新工具失败: {e}") from e


class MultiServerMCPClient(Agent):
    """
    客户端，用于连接多个 MCP 服务器并从中加载工具。
    
    支持两种连接方式：
    1. Stdio 连接：通过标准输入/输出与本地进程通信
    2. SSE 连接：通过 Server-Sent Events 与远程服务器通信
    
    该类支持异步上下文管理器协议（async with），可以自动初始化连接和清理资源。
    继承自 Agent 类，将每个 MCP 服务器创建为 McpAgent 实例，并将这些实例放入 self.handoffs 中。
    复用 McpAgent 的逻辑处理连接和工具加载。
    """

    def __init__(
        self,
        connections: Optional[Dict[str, Union[StdioConnection, SSEConnection]]] = None,
        name: str = "MultiServerMCPClient",
        **kwargs
    ) -> None:
        """
        使用 MCP 服务器连接初始化 MultiServerMCPClient。

        Args:
            connections: 将服务器名称映射到连接配置的字典。
                每个配置可以是 StdioConnection 或 SSEConnection。
                如果为 None，则不建立初始连接。
            name: Agent 的名称
            **kwargs: 传递给 Agent 父类的其他参数

        示例:

            ```python
            async with MultiServerMCPClient(
                {
                    "math": {
                        "command": "python",
                        # 确保更新为 math_server.py 文件的完整绝对路径
                        "args": ["/path/to/math_server.py"],
                        "transport": "stdio",
                    },
                    "weather": {
                        # 确保在端口 8000 上启动天气服务器
                        "url": "http://localhost:8000/sse",
                        "transport": "sse",
                    }
                }
            ) as client:
                all_tools = client.get_tools()
                ...
            ```
        """
        # 初始化 Agent 父类
        super().__init__(name=name, tools=[], **kwargs)

        self.connections = connections
        self.mcp_agents: Dict[str, McpAgent] = {}

    async def _create_mcp_agent_for_connection(
        self, server_name: str, connection: Union[StdioConnection, SSEConnection]
    ) -> McpAgent:
        """
        为给定的连接创建 McpAgent 实例。

        Args:
            server_name: 服务器名称
            connection: 连接配置，可以是 StdioConnection 或 SSEConnection
            
        Returns:
            创建的 McpAgent 实例
            
        Raises:
            ValueError: 如果连接配置无效
        """
        # 验证连接配置
        # TypedDict 不支持 isinstance 检查，所以我们通过检查字典的键来验证
        transport = connection.get("transport")
        if not transport or transport not in ["stdio", "sse"]:
            raise ValueError(f"不支持的传输类型: {transport}。必须是 'stdio' 或 'sse'")

        # 验证必要的字段
        if transport == "stdio" and ("command" not in connection or "args" not in connection):
            raise ValueError("stdio 连接需要 'command' 和 'args' 参数")

        if transport == "sse" and "url" not in connection:
            raise ValueError("sse 连接需要 'url' 参数")

        # 创建 McpAgent 实例
        mcp_agent = McpAgent(
            name=server_name,
            mcp_server=connection
        )

        # 将 McpAgent 添加到字典中
        self.mcp_agents[server_name] = mcp_agent
        return mcp_agent

    async def connect_to_server(self, server_name: str) -> McpAgent:
        """
        使用 self.connections 中的配置连接到 MCP 服务器。

        创建一个 McpAgent 实例并连接到服务器。

        Args:
            server_name: 标识此服务器连接的名称，必须存在于 self.connections 中

        Returns:
            创建并连接的 McpAgent 实例

        Raises:
            ValueError: 如果服务器名称不存在于 self.connections 中
            ValueError: 如果连接配置不完整或无效
        """
        # 检查服务器名称是否存在于 self.connections 中
        if not self.connections or server_name not in self.connections:
            raise ValueError(f"服务器名称 '{server_name}' 不存在于 connections 配置中")

        # 获取连接配置
        connection_config = self.connections[server_name]

        # 创建 McpAgent 实例
        mcp_agent = await self._create_mcp_agent_for_connection(server_name, connection_config)

        # 连接到服务器
        await mcp_agent.connect()

        # 将 McpAgent 添加到 handoffs 中
        if mcp_agent not in self.handoffs:
            self.handoffs.append(mcp_agent)

        return mcp_agent

    def get_tools(self) -> List[Any]:
        """获取所有已连接服务器的所有工具列表。"""
        # 更新 Agent 父类的 tools 属性
        all_tools: List[Any] = []
        for mcp_agent in self.mcp_agents.values():
            all_tools.extend(mcp_agent.tools)
        self.tools = all_tools
        return all_tools

    def get_mcp_agent(self, server_name: str) -> McpAgent:
        """获取特定服务器的 McpAgent 实例。
        
        Args:
            server_name: 服务器名称
            
        Returns:
            对应服务器的 McpAgent 实例
            
        Raises:
            ValueError: 如果找不到指定的服务器
        """
        if server_name not in self.mcp_agents:
            raise ValueError(f"未找到服务器 {server_name} 的 McpAgent 实例")
        return self.mcp_agents[server_name]

    async def __aenter__(self) -> "MultiServerMCPClient":
        try:
            # 清空 handoffs 列表，以防重复添加
            self.handoffs = []
            self.mcp_agents = {}

            # 连接到所有服务器
            if self.connections:
                for server_name in self.connections:
                    # 使用新的简化版 connect_to_server 方法
                    await self.connect_to_server(server_name)

            # 更新工具列表
            self.get_tools()
            return self
        except Exception:
            # 出现异常时清理资源
            await self.disconnect()
            raise

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        # 清理所有资源
        await self.disconnect()

        # 清空 handoffs 和 mcp_agents
        self.handoffs = []
        self.mcp_agents = {}

    async def disconnect(self) -> None:
        # 清理 McpAgent 的资源
        for server_name in list(self.mcp_agents.keys()):
            try:
                mcp_agent = self.mcp_agents.pop(server_name, None)
                if mcp_agent is not None:
                    # 直接清理 McpAgent 的内部资源，而不是调用其 disconnect 方法
                    await mcp_agent.disconnect()
                    print(f"  已清理 {server_name} 服务器的资源")
            except Exception as e:
                print(f"  清理 {server_name} 服务器资源时出错: {e}")
        
        print("资源清理完成")
