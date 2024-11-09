import asyncio
import base64
from typing import Literal
from uuid import uuid4

from appium import webdriver
from anthropic.types.beta import BetaToolComputerUse20241022Param

from ..config import TEMP_DIR
from .base import BaseAnthropicTool, ToolError, ToolResult

class IOSTool(BaseAnthropicTool):
    """Tool for controlling iOS devices"""
    
    name: Literal["ios"] = "ios"
    api_type: Literal["computer_20241022"] = "computer_20241022"

    def __init__(self):
        self.driver = None
        self._screenshot_delay = 0.5

    async def __call__(
        self,
        *,
        action: Literal[
            "tap",
            "type", 
            "screenshot",
            "swipe",
            "launch_app",
            "close_app"
        ],
        text: str | None = None,
        position: tuple[int, int] | None = None,
        app_id: str | None = None,
        **kwargs
    ) -> ToolResult:
        try:
            if not self.driver:
                await self._init_driver()

            if action == "screenshot":
                return await self._take_screenshot()

            if action in ("tap", "swipe"):
                if not position:
                    raise ToolError("Position required for touch actions")
                    
                if action == "tap":
                    self.driver.tap([position])
                else:
                    # Implement swipe
                    pass
                    
                return await self._take_screenshot()

            if action == "type":
                if not text:
                    raise ToolError("Text required for keyboard actions")
                self.driver.keyboard.send_keys(text)
                return await self._take_screenshot()

            if action in ("launch_app", "close_app"):
                if not app_id:
                    raise ToolError("App ID required")
                    
                if action == "launch_app":
                    self.driver.activate_app(app_id)
                else:
                    self.driver.terminate_app(app_id)
                    
                return await self._take_screenshot()

            raise ToolError(f"Unknown action: {action}")

        except Exception as e:
            return ToolResult(error=str(e))

    def to_params(self) -> BetaToolComputerUse20241022Param:
        return {
            "type": self.api_type,
            "name": self.name,
            "display_width_px": 0,  # Set based on device
            "display_height_px": 0,  # Set based on device
            "display_number": None
        }

    async def _init_driver(self):
        """Initialize Appium driver"""
        caps = {
            'platformName': 'iOS',
            'automationName': 'XCUITest',
            'deviceName': 'iPhone Simulator',
            # Add more capabilities as needed
        }
        
        self.driver = webdriver.Remote(
            'http://localhost:4723/wd/hub',
            caps
        )

    async def _take_screenshot(self) -> ToolResult:
        """Take and save device screenshot"""
        path = TEMP_DIR / f"ios_screenshot_{uuid4().hex}.png"
        
        try:
            self.driver.get_screenshot_as_file(str(path))
            await asyncio.sleep(self._screenshot_delay)
            
            return ToolResult(
                base64_image=base64.b64encode(path.read_bytes()).decode()
            )
        except Exception as e:
            return ToolResult(error=f"Screenshot failed: {e}") 