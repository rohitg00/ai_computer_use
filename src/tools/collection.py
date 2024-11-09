"""Collection of tools for device control"""

from typing import Any

from anthropic.types.beta import BetaToolUnionParam

from .base import BaseAnthropicTool, ToolError, ToolResult
from .mac_tool import MacTool
from .ios_tool import IOSTool

class ToolCollection:
    """Collection of control tools"""

    def __init__(self):
        self.tools = [
            MacTool(),
            IOSTool(),
        ]
        self.tool_map = {tool.to_params()["name"]: tool for tool in self.tools}

    def to_params(self) -> list[BetaToolUnionParam]:
        """Get API parameters for all tools"""
        return [tool.to_params() for tool in self.tools]

    async def run(self, *, name: str, tool_input: dict[str, Any]) -> ToolResult:
        """Execute a tool by name"""
        tool = self.tool_map.get(name)
        if not tool:
            return ToolResult(error=f"Invalid tool: {name}")

        try:
            return await tool(**tool_input)
        except ToolError as e:
            return ToolResult(error=e.message) 