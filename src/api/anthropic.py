"""Anthropic API integration"""

import asyncio
from datetime import datetime
from typing import Any, Callable, Optional

from anthropic import Anthropic, AnthropicBedrock, AnthropicVertex
from anthropic.types import (
    MessageParam,
    MessageStreamEvent,
)

from ..config import CONFIG, PROVIDER_TO_MODEL, APIProvider
from ..tools import ToolCollection, ToolResult

SYSTEM_PROMPT = f"""You are an AI assistant with the ability to control Mac and iOS devices.

Available tools:
- mac: Control macOS through mouse, keyboard and screenshots
- ios: Control iOS devices through touch, typing and app management

Current date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Guidelines:
1. Always verify actions before executing them
2. Take screenshots to confirm results
3. Handle errors gracefully
4. Never access sensitive data or credentials
5. Chain multiple actions when efficient
"""

class AnthropicClient:
    """Client for Anthropic API interaction"""

    def __init__(
        self,
        tools: ToolCollection,
        on_content: Optional[Callable[[str], None]] = None,
        on_tool_result: Optional[Callable[[ToolResult], None]] = None,
    ):
        self.tools = tools
        self.on_content = on_content
        self.on_tool_result = on_tool_result
        self.messages: list[MessageParam] = []
        
        # Initialize client based on provider
        provider = CONFIG["api_provider"]
        if provider == APIProvider.ANTHROPIC:
            self.client = Anthropic(api_key=CONFIG["api_key"])
        elif provider == APIProvider.BEDROCK:
            self.client = AnthropicBedrock()
        elif provider == APIProvider.VERTEX:
            self.client = AnthropicVertex()
        else:
            raise ValueError(f"Invalid API provider: {provider}")

    async def send_message(self, message: str) -> None:
        """Send message to Claude and handle response"""
        self.messages.append({"role": "user", "content": message})

        # Stream response from Claude
        stream = await self.client.messages.create(
            model=PROVIDER_TO_MODEL[CONFIG["api_provider"]],
            max_tokens=4096,
            messages=self.messages,
            system=SYSTEM_PROMPT,
            tools=self.tools.to_params(),
            stream=True,
        )

        current_text = ""
        async for event in stream:
            if isinstance(event, MessageStreamEvent):
                if event.type == "content_block_delta":
                    current_text += event.delta.text
                    if self.on_content:
                        self.on_content(current_text)
                        
                elif event.type == "tool_use":
                    # Execute tool
                    result = await self.tools.run(
                        name=event.tool_name,
                        tool_input=event.parameters
                    )
                    
                    if self.on_tool_result:
                        self.on_tool_result(result)

                    # Add tool result to messages
                    self.messages.append({
                        "role": "tool",
                        "content": {
                            "output": result.output,
                            "error": result.error,
                            "image": result.base64_image
                        }
                    })

        # Add final response to message history
        if current_text:
            self.messages.append({
                "role": "assistant",
                "content": current_text
            }) 