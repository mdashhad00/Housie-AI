"""
Housie AI — Computer Controller Factory
Auto-detects the host operating system and instantiates the matching platform adapter:
- Windows (Win32 / PyAutoGUI)
- macOS (AppleScript / PyAutoGUI)
- Linux (xdotool / PyAutoGUI)
- Android (Android Intents / Termux API / ADB)
"""

import sys
import os
from typing import Optional
from .base import BaseController
from .windows import WindowsController
from .macos import MacOSController
from .linux import LinuxController
from .android import AndroidController

_controller_instance: Optional[BaseController] = None

def get_controller() -> BaseController:
    """
    Returns the singleton controller instance matching the host OS.
    """
    global _controller_instance
    if _controller_instance is not None:
        return _controller_instance

    # Check for Android / Termux environment
    if os.path.exists("/system/build.prop") or "ANDROID_ROOT" in os.environ or "TERMUX_VERSION" in os.environ:
        _controller_instance = AndroidController()
    elif sys.platform.startswith("win"):
        _controller_instance = WindowsController()
    elif sys.platform == "darwin":
        _controller_instance = MacOSController()
    elif sys.platform.startswith("linux"):
        _controller_instance = LinuxController()
    else:
        # Generic fallback
        _controller_instance = WindowsController()

    return _controller_instance
