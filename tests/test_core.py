"""Core functionality tests"""

import asyncio
import pytest
from src.tools.device_manager import DeviceManager
from src.utils.contexts import device_operation
from src.utils.state import DeviceStatus

@pytest.mark.asyncio
async def test_mac_initialization():
    """Test Mac device initialization"""
    device_manager = DeviceManager()
    success = await device_manager.initialize()
    assert success
    assert device_manager.state.mac_state.status == DeviceStatus.CONNECTED

@pytest.mark.asyncio
async def test_device_operation_context():
    """Test device operation context manager"""
    device_manager = DeviceManager()
    
    async with device_operation(device_manager, "mac") as ready:
        assert ready
        assert device_manager.state.mac_state.is_active

@pytest.mark.asyncio
async def test_mac_tool_safety():
    """Test Mac tool safety checks"""
    from src.tools.mac_tool import MacTool
    
    tool = MacTool()
    
    # Test unsafe click
    result = await tool(
        action="click",
        position=(-1, -1)  # Invalid coordinates
    )
    assert result.error and "bounds" in result.error.lower()
    
    # Test unsafe text
    result = await tool(
        action="type",
        text="sudo rm -rf /"  # Dangerous command
    )
    assert result.error and "unsafe" in result.error.lower() 