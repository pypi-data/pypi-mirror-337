#!/usr/bin/env python3
"""
测试 McpAgent 类的基本功能
"""

import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from openai_mcp_agents.mcp_agent import McpAgent, StdioConnection, SSEConnection


@pytest.fixture
def mock_session():
    """创建模拟的 ClientSession"""
    session = AsyncMock()
    session.initialize = AsyncMock()
    session.list_tools = AsyncMock(return_value=MagicMock(tools=[]))
    return session


@pytest.mark.asyncio
async def test_mcp_agent_context_manager(mock_session):
    """测试 McpAgent 的异步上下文管理器功能"""
    with patch('openai_mcp_agents.mcp_agent.ClientSession', return_value=mock_session):
        with patch('openai_mcp_agents.mcp_agent.stdio_client') as mock_stdio:
            # 设置模拟的 stdio_client
            mock_transport = (AsyncMock(), AsyncMock())
            mock_stdio.return_value.__aenter__.return_value = mock_transport
            
            # 使用异步上下文管理器
            async with McpAgent(
                name="Test Agent",
                instructions="Test instructions",
                mcp_server={
                    "transport": "stdio",
                    "command": "test_command",
                    "args": ["--test"],
                    "encoding": "utf-8",
                    "encoding_error_handler": "strict"
                }
            ) as agent:
                # 验证连接是否已建立
                assert agent.session is not None
                assert mock_session.initialize.called
                assert mock_session.list_tools.called
            
            # 验证退出上下文管理器后是否已断开连接
            assert agent.session is None
            assert agent.exit_stack is None


@pytest.mark.asyncio
async def test_mcp_agent_manual_connection(mock_session):
    """测试 McpAgent 的手动连接和断开功能"""
    with patch('openai_mcp_agents.mcp_agent.ClientSession', return_value=mock_session):
        with patch('openai_mcp_agents.mcp_agent.stdio_client') as mock_stdio:
            # 设置模拟的 stdio_client
            mock_transport = (AsyncMock(), AsyncMock())
            mock_stdio.return_value.__aenter__.return_value = mock_transport
            
            # 创建 McpAgent 实例
            agent = McpAgent(
                name="Test Agent",
                instructions="Test instructions",
                mcp_server={
                    "transport": "stdio",
                    "command": "test_command",
                    "args": ["--test"],
                    "encoding": "utf-8",
                    "encoding_error_handler": "strict"
                }
            )
            
            # 手动连接
            await agent.connect()
            
            # 验证连接是否已建立
            assert agent.session is not None
            assert mock_session.initialize.called
            assert mock_session.list_tools.called
            
            # 手动断开连接
            await agent.disconnect()
            
            # 验证是否已断开连接
            assert agent.session is None
            assert agent.exit_stack is None


@pytest.mark.asyncio
async def test_mcp_agent_invalid_connection():
    """测试 McpAgent 无效连接配置的情况"""
    # 测试无效的连接类型
    agent = McpAgent(
        name="Test Agent",
        instructions="Test instructions",
        mcp_server={"invalid": "config"}
    )
    
    with pytest.raises(ValueError):
        await agent.connect()
    
    # 测试缺少必要参数的 stdio 连接
    agent = McpAgent(
        name="Test Agent",
        instructions="Test instructions",
        mcp_server={"transport": "stdio"}
    )
    
    with pytest.raises(ValueError):
        await agent.connect()
    
    # 测试缺少必要参数的 sse 连接
    agent = McpAgent(
        name="Test Agent",
        instructions="Test instructions",
        mcp_server={"transport": "sse"}
    )
    
    with pytest.raises(ValueError):
        await agent.connect()
