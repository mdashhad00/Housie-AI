"""
Housie AI — Android Device Controller Adapter
Implements app launching, text input, and automation on Android devices
using Android Intents (am start), Termux API, and ADB shell input.
"""

import os
import subprocess
import time
from typing import Dict, Any, Optional
from .base import BaseController

class AndroidController(BaseController):
    def __init__(self):
        super().__init__("android")

    def _run_shell(self, cmd_list) -> str:
        try:
            return subprocess.check_output(cmd_list, stderr=subprocess.STDOUT, text=True).strip()
        except Exception as e:
            return f"Error: {e}"

    def open_app(self, name: str, args: str = "") -> str:
        clean = name.lower().strip()
        pkg_map = {
            "chrome": "com.android.chrome",
            "whatsapp": "com.whatsapp",
            "youtube": "com.google.android.youtube",
            "camera": "com.android.camera",
            "settings": "com.android.settings",
            "calculator": "com.google.android.calculator",
            "maps": "com.google.android.apps.maps",
            "spotify": "com.spotify.music",
            "instagram": "com.instagram.android"
        }

        pkg = pkg_map.get(clean)
        if pkg:
            # 1. Try monkey launch
            out = self._run_shell(["monkey", "-p", pkg, "-c", "android.intent.category.LAUNCHER", "1"])
            if "Events injected" in out:
                return f"Launched Android app: {pkg}"

        # 2. Try am start intent
        out = self._run_shell(["am", "start", "-n", f"{clean}/.MainActivity"])
        return f"Dispatched Android intent for: {name}"

    def type_text(self, text: str, press_enter: bool = False) -> str:
        safe_text = text.replace(" ", "%s")
        self._run_shell(["input", "text", safe_text])
        if press_enter:
            self._run_shell(["input", "keyevent", "66"])  # KEYCODE_ENTER = 66
        return f"Injected text on Android: '{text}'"

    def press_key(self, key: str, modifiers: Optional[list] = None) -> str:
        key_map = {
            "enter": "66",
            "return": "66",
            "back": "4",
            "home": "3",
            "menu": "82",
            "tab": "61",
            "space": "62",
            "volume_up": "24",
            "volume_down": "25",
            "power": "26",
            "camera": "27"
        }
        code = key_map.get(key.lower().strip(), "66")
        self._run_shell(["input", "keyevent", code])
        return f"Injected Android keyevent {code} ({key})"

    def click(self, x: Optional[int] = None, y: Optional[int] = None, button: str = "left", clicks: int = 1) -> str:
        target_x = x if x is not None else 540
        target_y = y if y is not None else 960
        for _ in range(clicks):
            self._run_shell(["input", "tap", str(target_x), str(target_y)])
            time.sleep(0.08)
        return f"Tapped on Android screen at ({target_x}, {target_y})"

    def move_mouse(self, x: int, y: int) -> str:
        # Hover/pointer on Android
        return f"Pointer position set on Android: ({x}, {y})"

    def scroll(self, amount: int, direction: str = "down") -> str:
        # Android swipe (x1 y1 x2 y2 duration)
        if direction == "down":
            self._run_shell(["input", "swipe", "500", "1500", "500", "500", "300"])
        else:
            self._run_shell(["input", "swipe", "500", "500", "500", "1500", "300"])
        return f"Performed Android swipe {direction}"

    def take_screenshot(self, filename: Optional[str] = None) -> str:
        fname = filename or f"android_shot_{int(time.time())}.png"
        target_path = f"/sdcard/{fname}"
        self._run_shell(["screencap", "-p", target_path])
        return f"Captured Android screen to {target_path}"

    def get_active_window(self) -> Dict[str, Any]:
        out = self._run_shell(["dumpsys", "window", "windows"])
        for line in out.splitlines():
            if "mCurrentFocus" in line:
                return {"title": line.strip()}
        return {"title": "Android Foreground Activity"}

    def whatsapp_send(self, phone: str, message: str, auto_send: bool = True) -> str:
        import urllib.parse
        clean_phone = "".join(c for c in phone if c.isdigit())
        encoded = urllib.parse.quote(message)
        uri = f"https://api.whatsapp.com/send?phone={clean_phone}&text={encoded}"
        self._run_shell(["am", "start", "-a", "android.intent.action.VIEW", "-d", uri])
        if auto_send:
            time.sleep(2.0)
            self._run_shell(["input", "keyevent", "66"])
        return f"Dispatched Android WhatsApp Intent for {phone}"
