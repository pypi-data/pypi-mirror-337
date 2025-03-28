#!/usr/bin/env python3
"""
测试工具转换功能
"""

import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from openai_mcp_agents.tools import (
    convert_mcp_tool_to_agent_tool,
    load_mcp_tools,
    _convert_mcp_tool_schema,
    _convert_call_tool_result,
)
from mcp.types import CallToolResult, TextContent, ImageContent, EmbeddedResource


@pytest.fixture
def mock_mcp_tool():
    """创建模拟的 MCP 工具"""
    tool = MagicMock()
    tool.name = "test_tool"
    tool.description = "Test tool description"
    tool.inputSchema = {
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "description": "First parameter"
            },
            "param2": {
                "type": "number",
                "description": "Second parameter"
            },
            "param3": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "Third parameter"
            }
        }
    }
    return tool


@pytest.fixture
def mock_session():
    """创建模拟的会话"""
    session = AsyncMock()
    session.call_tool = AsyncMock()
    return session


def test_convert_mcp_tool_schema(mock_mcp_tool):
    """测试 MCP 工具模式转换"""
    schema = _convert_mcp_tool_schema(mock_mcp_tool)
    
    # 验证基本结构
    assert schema["type"] == "object"
    assert "properties" in schema
    assert "required" in schema
    
    # 验证属性
    assert "param1" in schema["properties"]
    assert schema["properties"]["param1"]["type"] == "string"
    assert schema["properties"]["param1"]["description"] == "First parameter"
    
    assert "param2" in schema["properties"]
    assert schema["properties"]["param2"]["type"] == "number"
    
    assert "param3" in schema["properties"]
    assert schema["properties"]["param3"]["type"] == "array"
    assert schema["properties"]["param3"]["items"]["type"] == "string"
    
    # 验证必需字段
    assert set(schema["required"]) == {"param1", "param2", "param3"}


def test_convert_mcp_tool_schema_empty():
    """测试没有模式的 MCP 工具转换"""
    tool = MagicMock()
    tool.name = "empty_tool"
    tool.description = "Empty tool"
    tool.inputSchema = None
    
    schema = _convert_mcp_tool_schema(tool)
    
    # 验证默认结构
    assert schema["type"] == "object"
    assert schema["properties"] == {}
    assert schema["required"] == []
    assert schema["additionalProperties"] is False


def test_convert_call_tool_result_text():
    """测试文本结果转换"""
    result = CallToolResult(
        isError=False,
        content=[
            TextContent(text="Test result")
        ]
    )
    
    content, non_text = _convert_call_tool_result(result)
    
    assert content == "Test result"
    assert non_text is None


def test_convert_call_tool_result_multiple_text():
    """测试多个文本结果转换"""
    result = CallToolResult(
        isError=False,
        content=[
            TextContent(text="First line"),
            TextContent(text="Second line")
        ]
    )
    
    content, non_text = _convert_call_tool_result(result)
    
    assert isinstance(content, list)
    assert content == ["First line", "Second line"]
    assert non_text is None


def test_convert_call_tool_result_mixed():
    """测试混合内容结果转换"""
    image_content = ImageContent(
        mediaType="image/png",
        data="base64data"
    )
    
    result = CallToolResult(
        isError=False,
        content=[
            TextContent(text="Text result"),
            image_content
        ]
    )
    
    content, non_text = _convert_call_tool_result(result)
    
    assert content == "Text result"
    assert non_text is not None
    assert len(non_text) == 1
    assert non_text[0] == image_content


def test_convert_call_tool_result_error():
    """测试错误结果转换"""
    result = CallToolResult(
        isError=True,
        content=[
            TextContent(text="Error message")
        ]
    )
    
    with pytest.raises(RuntimeError) as excinfo:
        _convert_call_tool_result(result)
    
    assert "Error message" in str(excinfo.value)


@pytest.mark.asyncio
async def test_convert_mcp_tool_to_agent_tool(mock_mcp_tool, mock_session):
    """测试 MCP 工具转换为 Agent 工具"""
    # 设置模拟会话返回值
    mock_session.call_tool.return_value = CallToolResult(
        isError=False,
        content=[TextContent(text="Tool result")]
    )
    
    # 转换工具
    agent_tool = convert_mcp_tool_to_agent_tool(mock_mcp_tool, mock_session)
    
    # 验证基本属性
    assert agent_tool.name == "test_tool"
    assert agent_tool.description == "Test tool description"
    assert agent_tool.params_json_schema == _convert_mcp_tool_schema(mock_mcp_tool)
    
    # 测试调用工具
    result = await agent_tool.on_invoke_tool(None, json.dumps({"param1": "value1"}))
    
    # 验证调用结果
    assert result == "Tool result"
    mock_session.call_tool.assert_called_once_with("test_tool", {"param1": "value1"})


@pytest.mark.asyncio
async def test_load_mcp_tools(mock_mcp_tool, mock_session):
    """测试加载 MCP 工具"""
    # 设置模拟会话返回值
    mock_session.list_tools.return_value = MagicMock(tools=[mock_mcp_tool])
    
    # 加载工具
    tools = await load_mcp_tools(mock_session)
    
    # 验证结果
    assert len(tools) == 1
    assert tools[0].name == "test_tool"
    assert tools[0].description == "Test tool description"
