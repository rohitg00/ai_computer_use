"""Safety checks for Mac automation"""

import pyautogui
from typing import Tuple

class SafetyChecker:
    """Validates automation actions for safety"""
    
    # Sensitive UI elements that should not be clicked
    SENSITIVE_REGIONS = [
        # Add coordinates of sensitive UI areas
    ]
    
    @staticmethod
    def is_safe_click(x: int, y: int) -> Tuple[bool, str]:
        """Check if clicking at coordinates is safe"""
        # Check screen bounds
        screen_width, screen_height = pyautogui.size()
        if x < 0 or x > screen_width or y < 0 or y > screen_height:
            return False, "Coordinates out of screen bounds"
            
        # Check sensitive regions
        for region in SafetyChecker.SENSITIVE_REGIONS:
            if point_in_region((x, y), region):
                return False, "Cannot click in sensitive UI region"
                
        return True, ""

    @staticmethod
    def is_safe_type(text: str) -> Tuple[bool, str]:
        """Check if text input is safe"""
        # Prevent dangerous commands
        dangerous_patterns = [
            "sudo",
            "rm -rf",
            "mkfs",
            "dd",
            ">",
            "|",
        ]
        
        for pattern in dangerous_patterns:
            if pattern in text.lower():
                return False, f"Dangerous pattern detected: {pattern}"
                
        return True, ""

def point_in_region(point: Tuple[int, int], region: Tuple[int, int, int, int]) -> bool:
    """Check if point is inside region"""
    x, y = point
    rx, ry, rw, rh = region
    return rx <= x <= rx + rw and ry <= y <= ry + rh 