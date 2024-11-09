"""Cleanup utilities"""

import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from ..config import TEMP_DIR

class CleanupManager:
    """Manage temporary files and resources"""
    
    def __init__(self, max_age: Optional[timedelta] = None):
        self.max_age = max_age or timedelta(hours=1)
        
    def cleanup_temp_files(self):
        """Remove old temporary files"""
        now = datetime.now()
        
        for file in TEMP_DIR.glob("*"):
            if not file.is_file():
                continue
                
            # Check file age
            mtime = datetime.fromtimestamp(file.stat().st_mtime)
            if now - mtime > self.max_age:
                try:
                    file.unlink()
                except OSError:
                    pass
                    
    def cleanup_all(self):
        """Perform full cleanup"""
        # Remove temp directory
        try:
            shutil.rmtree(TEMP_DIR)
            TEMP_DIR.mkdir(exist_ok=True)
        except OSError:
            pass
            
        # Kill any lingering processes
        self._cleanup_processes()
        
    def _cleanup_processes(self):
        """Kill related processes"""
        processes = [
            "appium",
            "WebDriverAgent",
        ]
        
        for proc in processes:
            try:
                os.system(f"pkill -f {proc}")
            except:
                pass 