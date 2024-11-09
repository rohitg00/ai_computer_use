from enum import StrEnum
from pathlib import Path
from typing import TypedDict

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class APIProvider(StrEnum):
    ANTHROPIC = "anthropic"
    BEDROCK = "bedrock"
    VERTEX = "vertex"

class Resolution(TypedDict):
    width: int
    height: int

PROVIDER_TO_MODEL = {
    APIProvider.ANTHROPIC: "claude-3-5-sonnet-20241022",
    APIProvider.BEDROCK: "anthropic.claude-3-5-sonnet-20241022-v2:0",
    APIProvider.VERTEX: "claude-3-5-sonnet-v2@20241022",
}

# Screen resolution targets
MAX_SCALING_TARGETS = {
    "XGA": Resolution(width=1024, height=768),  # 4:3
    "WXGA": Resolution(width=1280, height=800),  # 16:10
    "FWXGA": Resolution(width=1366, height=768),  # ~16:9
}

# Configuration
CONFIG = {
    "api_key": os.getenv("ANTHROPIC_API_KEY"),
    "api_provider": os.getenv("API_PROVIDER", "anthropic"),
    "screen_width": int(os.getenv("SCREEN_WIDTH", "1280")),
    "screen_height": int(os.getenv("SCREEN_HEIGHT", "800")),
    "ios_device_id": os.getenv("IOS_DEVICE_ID"),
}

# Paths
ROOT_DIR = Path(__file__).parent.parent
TEMP_DIR = ROOT_DIR / "temp"
TEMP_DIR.mkdir(exist_ok=True) 