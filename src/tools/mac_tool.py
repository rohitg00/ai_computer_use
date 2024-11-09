import asyncio
import base64
import os
from pathlib import Path
from typing import Literal, cast
from uuid import uuid4

import pyautogui
from anthropic.types.beta import BetaToolComputerUse20241022Param

from ..config import TEMP_DIR, MAX_SCALING_TARGETS
from .base import BaseAnthropicTool, ToolError, ToolResult
from .mac_safety import SafetyChecker

class MacTool(BaseAnthropicTool):
    """Tool for controlling macOS with safety checks"""

    name: Literal["mac"] = "mac"
    api_type: Literal["computer_20241022"] = "computer_20241022"

    def __init__(self):
        super().__init__()
        self.safety = SafetyChecker()
        pyautogui.FAILSAFE = True  # Enable failsafe

    async def __call__(
        self,
        *,
        action: Literal[
            "click",
            "type",
            "key",
            "screenshot",
            "move",
            "get_position",
        ],
        text: str | None = None,
        position: tuple[int, int] | None = None,
        **kwargs
    ) -> ToolResult:
        try:
            # Add position validation
            if position is not None:
                is_safe, reason = self.safety.is_safe_click(*position)
                if not is_safe:
                    return ToolResult(error=f"Unsafe click position: {reason}")

            # Add text validation
            if text is not None:
                is_safe, reason = self.safety.is_safe_type(text)
                if not is_safe:
                    return ToolResult(error=f"Unsafe text input: {reason}")

            # Execute action with retries
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    return await self._execute_action(action, text, position)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    await asyncio.sleep(1)

        except Exception as e:
            return ToolResult(error=f"Action failed: {str(e)}")

    async def _execute_action(
        self,
        action: str,
        text: str | None,
        position: tuple[int, int] | None
    ) -> ToolResult:
        """Execute the requested action"""
        try:
            if action == "screenshot":
                return await self._take_screenshot()
            
            if action in ("click", "move"):
                if not position:
                    raise ToolError("Position required for mouse actions")
                x, y = self._scale_coordinates(*position)
                
                if action == "click":
                    pyautogui.click(x, y)
                else:
                    pyautogui.moveTo(x, y)
                    
                return await self._take_screenshot()

            if action in ("type", "key"):
                if not text:
                    raise ToolError("Text required for keyboard actions")
                    
                if action == "type":
                    pyautogui.write(text)
                else:
                    pyautogui.press(text)
                    
                return await self._take_screenshot()

            raise ToolError(f"Unknown action: {action}")

        except Exception as e:
            return ToolResult(error=str(e))

    def to_params(self) -> BetaToolComputerUse20241022Param:
        return {
            "type": self.api_type,
            "name": self.name,
            "display_width_px": self.width,
            "display_height_px": self.height,
            "display_number": None
        }

    async def _take_screenshot(self) -> ToolResult:
        """Take and save screenshot"""
        path = TEMP_DIR / f"screenshot_{uuid4().hex}.png"
        
        try:
            pyautogui.screenshot(str(path))
            await asyncio.sleep(self._screenshot_delay)
            
            if self._scaling_enabled:
                # Scale screenshot to target resolution
                target = MAX_SCALING_TARGETS["WXGA"]
                img = pyautogui.screenshot()
                img = img.resize((target["width"], target["height"]))
                img.save(path)

            return ToolResult(
                base64_image=base64.b64encode(path.read_bytes()).decode()
            )
        except Exception as e:
            return ToolResult(error=f"Screenshot failed: {e}")

    def _scale_coordinates(self, x: int, y: int) -> tuple[int, int]:
        """Scale coordinates between actual and target resolution"""
        if not self._scaling_enabled:
            return x, y

        target = MAX_SCALING_TARGETS["WXGA"]
        scale_x = self.width / target["width"] 
        scale_y = self.height / target["height"]

        return round(x * scale_x), round(y * scale_y) 