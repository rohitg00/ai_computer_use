"""iOS device connection management"""

import asyncio
import atexit
import subprocess
from typing import Optional

from appium import webdriver
from appium.webdriver.webdriver import WebDriver

from ..config import CONFIG

class IOSConnectionManager:
    """Manages Appium server and device connections"""
    
    def __init__(self):
        self.driver: Optional[WebDriver] = None
        self.appium_process: Optional[subprocess.Popen] = None
        self._setup_cleanup()

    def _setup_cleanup(self):
        """Ensure cleanup on exit"""
        atexit.register(self.cleanup)

    async def ensure_appium_running(self):
        """Start Appium server if not running"""
        if self.appium_process is None:
            try:
                self.appium_process = subprocess.Popen(
                    ["appium"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                # Wait for server to start
                await asyncio.sleep(5)
            except Exception as e:
                raise ConnectionError(f"Failed to start Appium: {e}")

    async def connect_device(self) -> WebDriver:
        """Connect to iOS device/simulator"""
        await self.ensure_appium_running()
        
        capabilities = {
            'platformName': 'iOS',
            'automationName': 'XCUITest',
            'deviceName': 'iPhone Simulator',
        }

        if device_id := CONFIG["ios_device_id"]:
            capabilities['udid'] = device_id

        try:
            self.driver = webdriver.Remote(
                'http://localhost:4723/wd/hub',
                capabilities
            )
            return self.driver
        except Exception as e:
            raise ConnectionError(f"Failed to connect to iOS device: {e}")

    def cleanup(self):
        """Clean up connections"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None

        if self.appium_process:
            try:
                self.appium_process.terminate()
            except:
                pass
            self.appium_process = None 