"""System preferences and permissions management"""

import subprocess
from typing import Dict, List, Optional

class SystemTool:
    """Manage system settings and permissions"""
    
    @staticmethod
    def check_permissions() -> Dict[str, bool]:
        """Check required system permissions"""
        return {
            "accessibility": SystemTool._check_accessibility(),
            "screen_recording": SystemTool._check_screen_recording(),
            "automation": SystemTool._check_automation()
        }
    
    @staticmethod
    def _check_accessibility() -> bool:
        """Check accessibility permissions"""
        try:
            result = subprocess.run(
                ["tccutil", "check", "com.apple.accessibility"],
                capture_output=True,
                text=True
            )
            return "granted" in result.stdout.lower()
        except:
            return False
            
    @staticmethod
    def _check_screen_recording() -> bool:
        """Check screen recording permissions"""
        try:
            result = subprocess.run(
                ["tccutil", "check", "com.apple.screencapture"],
                capture_output=True,
                text=True
            )
            return "granted" in result.stdout.lower()
        except:
            return False
            
    @staticmethod
    def _check_automation() -> bool:
        """Check automation permissions"""
        try:
            result = subprocess.run(
                ["tccutil", "check", "com.apple.automation"],
                capture_output=True,
                text=True
            )
            return "granted" in result.stdout.lower()
        except:
            return False
            
    @staticmethod
    def request_permissions() -> List[str]:
        """Request missing permissions"""
        missing = []
        permissions = SystemTool.check_permissions()
        
        for perm, granted in permissions.items():
            if not granted:
                missing.append(perm)
                SystemTool._request_permission(perm)
                
        return missing
        
    @staticmethod
    def _request_permission(permission: str):
        """Show system dialog to request permission"""
        dialogs = {
            "accessibility": [
                "osascript",
                "-e",
                'tell application "System Preferences" to activate',
                "-e",
                'tell application "System Preferences" to reveal anchor "Privacy_Accessibility" of pane id "com.apple.preference.security"'
            ],
            "screen_recording": [
                "osascript",
                "-e",
                'tell application "System Preferences" to activate',
                "-e",
                'tell application "System Preferences" to reveal anchor "Privacy_ScreenCapture" of pane id "com.apple.preference.security"'
            ],
            "automation": [
                "osascript",
                "-e",
                'tell application "System Preferences" to activate',
                "-e",
                'tell application "System Preferences" to reveal anchor "Privacy_Automation" of pane id "com.apple.preference.security"'
            ]
        }
        
        if cmd := dialogs.get(permission):
            subprocess.run(cmd) 