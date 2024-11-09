"""Device management and coordination"""

import asyncio
from typing import Dict, Optional

from ..utils.state import DeviceStatus, StateManager
from ..utils.logging import setup_logging
from .ios_connection import IOSConnectionManager
from .system_tool import SystemTool

logger = setup_logging()

class DeviceManager:
    """Coordinate device connections and states"""
    
    def __init__(self):
        self.state = StateManager()
        self.ios_connection = IOSConnectionManager()
        self.system_tool = SystemTool()
        
    async def initialize(self):
        """Initialize device connections"""
        # Check system permissions
        permissions = self.system_tool.check_permissions()
        missing_permissions = [p for p, granted in permissions.items() if not granted]
        
        if missing_permissions:
            logger.warning(f"Missing permissions: {missing_permissions}")
            self.system_tool.request_permissions()
            return False
            
        # Initialize Mac state
        try:
            self.state.update_mac_state(DeviceStatus.CONNECTED)
            logger.info("Mac control initialized")
        except Exception as e:
            self.state.update_mac_state(DeviceStatus.ERROR, str(e))
            logger.error(f"Failed to initialize Mac control: {e}")
            return False
            
        # Initialize iOS if configured
        if self.ios_connection.is_configured:
            try:
                self.state.update_ios_state(DeviceStatus.CONNECTING)
                await self.ios_connection.connect_device()
                self.state.update_ios_state(DeviceStatus.CONNECTED)
                logger.info("iOS device connected")
            except Exception as e:
                self.state.update_ios_state(DeviceStatus.ERROR, str(e))
                logger.error(f"Failed to connect iOS device: {e}")
                
        return True
        
    async def ensure_device_ready(self, device_type: str) -> bool:
        """Ensure specific device is ready for use"""
        if device_type == "mac":
            if not self.state.mac_state.is_active:
                try:
                    self.state.update_mac_state(DeviceStatus.CONNECTING)
                    # Re-check permissions and initialize
                    return await self.initialize()
                except Exception as e:
                    self.state.update_mac_state(DeviceStatus.ERROR, str(e))
                    return False
            return True
            
        elif device_type == "ios":
            if not self.state.ios_state.is_active:
                try:
                    self.state.update_ios_state(DeviceStatus.CONNECTING)
                    await self.ios_connection.connect_device()
                    self.state.update_ios_state(DeviceStatus.CONNECTED)
                    return True
                except Exception as e:
                    self.state.update_ios_state(DeviceStatus.ERROR, str(e))
                    return False
            return True
            
        return False
        
    def cleanup(self):
        """Clean up device connections"""
        if self.state.ios_state.is_active:
            self.ios_connection.cleanup()
            self.state.update_ios_state(DeviceStatus.DISCONNECTED) 