"""State management for tools and connections"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

class DeviceStatus(Enum):
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    ERROR = "error"

@dataclass
class DeviceState:
    """Track device connection state"""
    status: DeviceStatus
    last_action: datetime
    error: Optional[str] = None
    
    @property
    def is_active(self) -> bool:
        """Check if device is actively connected"""
        return self.status == DeviceStatus.CONNECTED

class StateManager:
    """Manage global application state"""
    
    def __init__(self):
        self.mac_state = DeviceState(
            status=DeviceStatus.DISCONNECTED,
            last_action=datetime.now()
        )
        self.ios_state = DeviceState(
            status=DeviceStatus.DISCONNECTED,
            last_action=datetime.now()
        )
        
    def update_mac_state(self, status: DeviceStatus, error: Optional[str] = None):
        """Update Mac device state"""
        self.mac_state = DeviceState(
            status=status,
            last_action=datetime.now(),
            error=error
        )
        
    def update_ios_state(self, status: DeviceStatus, error: Optional[str] = None):
        """Update iOS device state"""
        self.ios_state = DeviceState(
            status=status,
            last_action=datetime.now(),
            error=error
        ) 