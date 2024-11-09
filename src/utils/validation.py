"""Configuration validation"""

import os
from typing import Dict, List, Optional

from ..config import CONFIG, APIProvider

class ConfigurationError(Exception):
    """Configuration validation error"""
    pass

def validate_config() -> Optional[List[str]]:
    """Validate configuration settings"""
    errors = []
    
    # Check API configuration
    if not CONFIG["api_key"]:
        errors.append("ANTHROPIC_API_KEY is required")
        
    if CONFIG["api_provider"] not in [e.value for e in APIProvider]:
        errors.append(f"Invalid API_PROVIDER: {CONFIG['api_provider']}")
        
    # Check screen dimensions
    try:
        width = int(CONFIG["screen_width"])
        height = int(CONFIG["screen_height"])
        if width <= 0 or height <= 0:
            errors.append("Screen dimensions must be positive integers")
    except ValueError:
        errors.append("Invalid screen dimensions")
        
    # Check iOS configuration if device ID provided
    if CONFIG["ios_device_id"]:
        if not os.path.exists("/usr/local/bin/appium"):
            errors.append("Appium not found. Install with: npm install -g appium")
            
        try:
            import appium
        except ImportError:
            errors.append("Appium Python client not installed")
            
    return errors if errors else None 