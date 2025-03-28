from __future__ import annotations

import json
import logging
from typing import Any, List, Tuple, Optional, Union

from agents.tool import FunctionTool
from mcp import Tool as McpTool
from mcp.types import CallToolResult, TextContent, ImageContent, EmbeddedResource

# Type alias for non-text content
NonTextContent = Union[ImageContent, EmbeddedResource]

# Configure logging
logger = logging.getLogger(__name__)


def _convert_call_tool_result(call_tool_result: CallToolResult) -> Tuple[Union[str, List[str]], Optional[List[NonTextContent]]]:
    text_contents: List[TextContent] = []
    non_text_contents: List[NonTextContent] = []

    # Separate text and non-text content
    for content in call_tool_result.content:
        if isinstance(content, TextContent):
            text_contents.append(content)
        else:
            non_text_contents.append(content)

    # Extract text from text content
    tool_content: Union[str, List[str]] = [content.text for content in text_contents]
    if len(text_contents) == 1:
        tool_content = tool_content[0]

    # Handle error case
    if call_tool_result.isError:
        error_msg = tool_content if isinstance(tool_content, str) else "\n".join(tool_content) if tool_content else "Unknown error"
        logger.error(f"Tool call error: {error_msg}")
        raise RuntimeError(error_msg)

    return tool_content, non_text_contents or None


def _convert_mcp_tool_schema(mcp_tool: McpTool):
    params_schema = {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False
    }

    if not hasattr(mcp_tool, 'inputSchema') or not mcp_tool.inputSchema:
        return params_schema

    input_schema = mcp_tool.inputSchema

    if 'type' in input_schema:
        params_schema['type'] = input_schema['type']

    if 'description' in input_schema:
        params_schema['description'] = input_schema['description']

    property_names = []
    if 'properties' in input_schema and isinstance(input_schema['properties'], dict):
        for prop_name, prop_schema in input_schema['properties'].items():
            property_names.append(prop_name)
            simplified_prop = {}
            if 'type' in prop_schema:
                simplified_prop['type'] = prop_schema['type']
            else:
                simplified_prop['type'] = 'string'

            if 'description' in prop_schema:
                simplified_prop['description'] = prop_schema['description']

            if simplified_prop.get('type') == 'array' and 'items' in prop_schema:
                if isinstance(prop_schema['items'], dict) and 'type' in prop_schema['items']:
                    simplified_prop['items'] = {
                        'type': prop_schema['items']['type']
                    }
                else:
                    simplified_prop['items'] = {'type': 'string'}

            params_schema['properties'][prop_name] = simplified_prop

    params_schema['required'] = property_names

    return params_schema


def convert_mcp_tool_to_agent_tool(mcp_tool: McpTool, session) -> FunctionTool:
    async def on_invoke_tool(run_context: Any, params_str: str) -> str:
        if not session:
            error_msg = "MCP session not initialized. Please call connect() first."
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        # Parse parameters
        try:
            params = json.loads(params_str)
        except json.JSONDecodeError as e:
            error_msg = f"Error parsing parameters for tool '{mcp_tool.name}': {e}"
            logger.error(error_msg)
            return error_msg

        # Call MCP tool
        try:
            result = await session.call_tool(mcp_tool.name, params)
            text_content, _ = _convert_call_tool_result(result)
            return text_content if isinstance(text_content, str) else "\n".join(text_content)
        except Exception as e:
            error_message = f"Error calling MCP tool '{mcp_tool.name}': {str(e)}"
            logger.error(error_message)
            return error_message

    return FunctionTool(
        name=mcp_tool.name,
        description=mcp_tool.description or "",
        params_json_schema=_convert_mcp_tool_schema(mcp_tool),
        on_invoke_tool=on_invoke_tool
    )


async def load_mcp_tools(session) -> List[FunctionTool]:
    response = await session.list_tools()
    return [convert_mcp_tool_to_agent_tool(tool, session) for tool in response.tools]
