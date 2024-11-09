"""Context managers for device operations"""

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

from ..tools.device_manager import DeviceManager
from ..utils.state import DeviceStatus
from .logging import setup_logging

logger = setup_logging()

@asynccontextmanager
async def device_operation(
    device_manager: DeviceManager,
    device_type: str,
    timeout: Optional[float] = None
) -> AsyncGenerator[bool, None]:
    """Context manager for safe device operations"""
    try:
        # Ensure device is ready
        if not await device_manager.ensure_device_ready(device_type):
            logger.error(f"Failed to prepare {device_type} device")
            yield False
            return
            
        # Set timeout if specified
        if timeout:
            try:
                async with asyncio.timeout(timeout):
                    yield True
            except asyncio.TimeoutError:
                logger.error(f"Operation timed out after {timeout}s")
                if device_type == "mac":
                    device_manager.state.update_mac_state(
                        DeviceStatus.ERROR,
                        "Operation timed out"
                    )
                else:
                    device_manager.state.update_ios_state(
                        DeviceStatus.ERROR,
                        "Operation timed out"
                    )
                yield False
        else:
            yield True
            
    except Exception as e:
        logger.error(f"Device operation failed: {str(e)}")
        if device_type == "mac":
            device_manager.state.update_mac_state(DeviceStatus.ERROR, str(e))
        else:
            device_manager.state.update_ios_state(DeviceStatus.ERROR, str(e))
        yield False
        
    finally:
        # Cleanup if needed
        if device_type == "ios":
            device_manager.cleanup() 