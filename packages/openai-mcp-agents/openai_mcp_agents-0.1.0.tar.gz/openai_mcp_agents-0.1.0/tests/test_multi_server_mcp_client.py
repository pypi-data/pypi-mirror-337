#!/usr/bin/env python3
"""
测试 MultiServerMCPClient 类的基本功能
"""

import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from openai_mcp_agents.mcp_agent import MultiServerMCPClient, McpAgent, StdioConnection, SSEConnection


@pytest.fixture
def mock_mcp_agent():
    """创建模拟的 McpAgent"""
    agent = AsyncMock()
    agent.tools = [MagicMock(), MagicMock()]
    agent.connect = AsyncMock()
    agent.disconnect = AsyncMock()
    return agent


@pytest.mark.asyncio
async def test_multi_server_mcp_client_context_manager(mock_mcp_agent):
    """测试 MultiServerMCPClient 的异步上下文管理器功能"""
    with patch('openai_mcp_agents.mcp_agent.McpAgent', return_value=mock_mcp_agent):
        # 设置连接配置
        connections = {
            "filesystem": {
                "transport": "stdio",
                "command": "test_command",
                "args": ["--test"],
                "encoding": "utf-8",
                "encoding_error_handler": "strict"
            },
            "git": {
                "transport": "sse",
                "url": "http://localhost:8000/sse",
                "headers": None,
                "timeout": 5,
                "sse_read_timeout": 300
            }
        }
        
        # 使用异步上下文管理器
        async with MultiServerMCPClient(
            name="Test Multi-Server Client",
            instructions="Test instructions",
            connections=connections
        ) as client:
            # 验证是否已创建 McpAgent 实例
            assert len(client.mcp_agents) == 2
            assert "filesystem" in client.mcp_agents
            assert "git" in client.mcp_agents
            
            # 验证是否已连接
            assert mock_mcp_agent.connect.call_count == 2
            
            # 测试获取工具
            tools = client.get_tools()
            assert len(tools) == 4  # 每个服务器有 2 个工具
        
        # 验证退出上下文管理器后是否已断开连接
        assert mock_mcp_agent.disconnect.call_count == 2


@pytest.mark.asyncio
async def test_multi_server_mcp_client_manual_connection(mock_mcp_agent):
    """测试 MultiServerMCPClient 的手动连接和断开功能"""
    with patch('openai_mcp_agents.mcp_agent.McpAgent', return_value=mock_mcp_agent):
        # 设置连接配置
        connections = {
            "filesystem": {
                "transport": "stdio",
                "command": "test_command",
                "args": ["--test"],
                "encoding": "utf-8",
                "encoding_error_handler": "strict"
            },
            "git": {
                "transport": "sse",
                "url": "http://localhost:8000/sse",
                "headers": None,
                "timeout": 5,
                "sse_read_timeout": 300
            }
        }
        
        # 创建 MultiServerMCPClient 实例
        client = MultiServerMCPClient(
            name="Test Multi-Server Client",
            instructions="Test instructions",
            connections=connections
        )
        
        # 手动连接到特定服务器
        await client.connect_to_server("filesystem")
        
        # 验证是否已连接到指定服务器
        assert "filesystem" in client.mcp_agents
        assert mock_mcp_agent.connect.called
        
        # 测试获取特定服务器的 McpAgent 实例
        agent = client.get_mcp_agent("filesystem")
        assert agent is not None
        
        # 测试获取不存在的服务器
        with pytest.raises(ValueError):
            client.get_mcp_agent("nonexistent")
        
        # 手动断开连接
        await client.disconnect()
        
        # 验证是否已断开连接
        assert mock_mcp_agent.disconnect.called


@pytest.mark.asyncio
async def test_multi_server_mcp_client_invalid_connection():
    """测试 MultiServerMCPClient 无效连接配置的情况"""
    # 设置连接配置
    connections = {
        "invalid": {
            "invalid": "config"
        }
    }
    
    # 创建 MultiServerMCPClient 实例
    client = MultiServerMCPClient(
        name="Test Multi-Server Client",
        instructions="Test instructions",
        connections=connections
    )
    
    # 测试连接到无效服务器
    with pytest.raises(ValueError):
        await client.connect_to_server("invalid")
