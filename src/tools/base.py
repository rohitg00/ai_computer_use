from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, fields, replace
from typing import Any, Optional

from anthropic.types.beta import BetaToolUnionParam

@dataclass(frozen=True)
class ToolResult:
    """Result from tool execution"""
    output: Optional[str] = None
    error: Optional[str] = None 
    base64_image: Optional[str] = None
    system: Optional[str] = None

    def __bool__(self):
        return any(getattr(self, field.name) for field in fields(self))

    def replace(self, **kwargs):
        return replace(self, **kwargs)

class ToolError(Exception):
    """Tool execution error"""
    def __init__(self, message: str):
        self.message = message

class BaseAnthropicTool(metaclass=ABCMeta):
    """Base class for Anthropic tools"""
    
    @abstractmethod
    async def __call__(self, **kwargs) -> Any:
        """Execute the tool"""
        pass

    @abstractmethod
    def to_params(self) -> BetaToolUnionParam:
        """Convert tool to API parameters"""
        pass 