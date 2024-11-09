"""Custom error types"""

class APIError(Exception):
    """Base API error"""
    pass

class ToolExecutionError(Exception):
    """Error during tool execution"""
    pass

class ConnectionError(Exception):
    """Connection/network error"""
    pass

class AuthenticationError(Exception):
    """Authentication failed"""
    pass 