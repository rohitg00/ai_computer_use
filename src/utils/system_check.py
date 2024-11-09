"""System compatibility and requirements check"""

import os
import shutil
import subprocess
from typing import List, Tuple

def check_system_requirements() -> List[Tuple[str, bool, str]]:
    """Check all system requirements"""
    results = []
    
    # Check Python version
    import sys
    python_version = sys.version_info >= (3, 12)
    results.append((
        "Python 3.12+",
        python_version,
        "Install Python 3.12 or later"
    ))
    
    # Check Homebrew
    homebrew = shutil.which("brew") is not None
    results.append((
        "Homebrew",
        homebrew,
        "Install Homebrew: /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    ))
    
    # Check cliclick
    cliclick = shutil.which("cliclick") is not None
    results.append((
        "cliclick",
        cliclick,
        "Install cliclick: brew install cliclick"
    ))
    
    # Check Node.js (for Appium)
    node = shutil.which("node") is not None
    results.append((
        "Node.js",
        node,
        "Install Node.js: brew install node"
    ))
    
    # Check Appium if iOS support needed
    if os.getenv("IOS_DEVICE_ID"):
        appium = shutil.which("appium") is not None
        results.append((
            "Appium",
            appium,
            "Install Appium: npm install -g appium"
        ))
        
        # Check Xcode
        xcode = subprocess.run(
            ["xcode-select", "-p"],
            capture_output=True
        ).returncode == 0
        results.append((
            "Xcode",
            xcode,
            "Install Xcode from the App Store"
        ))
    
    return results

def print_system_status():
    """Print system requirements status"""
    print("System Requirements Check:")
    print("-" * 50)
    
    results = check_system_requirements()
    all_passed = True
    
    for requirement, passed, fix in results:
        status = "✅" if passed else "❌"
        print(f"{status} {requirement}")
        if not passed:
            print(f"   Fix: {fix}")
            all_passed = False
    
    print("-" * 50)
    if all_passed:
        print("All system requirements met! ✨")
    else:
        print("Please fix the issues above before continuing.")
    
    return all_passed 