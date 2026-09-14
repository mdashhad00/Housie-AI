"""
Housie AI — macOS Computer Controller Adapter
Implements keyboard, mouse, app, and accessibility automation on macOS.
Uses osascript (AppleScript) and PyAutoGUI.
"""

import os
import subprocess
import time
from typing import Dict, Any, Optional
from .base import BaseController

class MacOSController(BaseController):
    def __init__(self):
        super().__init__("macos")
        self.has_pyautogui = False
        try:
            import pyautogui
            self.pyautogui = pyautogui
            self.has_pyautogui = True
        except ImportError:
            self.pyautogui = None

    def open_app(self, name: str, args: str = "") -> str:
        clean = name.strip()
        app_map = {
            "chrome": "Google Chrome",
            "safari": "Safari",
            "vscode": "Visual Studio Code",
            "code": "Visual Studio Code",
            "terminal": "Terminal",
            "iterm": "iTerm",
            "notes": "Notes",
            "calculator": "Calculator",
            "spotify": "Spotify",
            "whatsapp": "WhatsApp",
            "finder": "Finder"
        }
        target = app_map.get(clean.lower(), clean)
        try:
            if args:
                subprocess.Popen(["open", "-a", target, "--args", args])
            else:
                subprocess.Popen(["open", "-a", target])
            return f"Launched macOS Application: {target}"
        except Exception as e:
            raise RuntimeError(f"Failed to open '{name}' on macOS: {e}")

    def type_text(self, text: str, press_enter: bool = False) -> str:
        if self.has_pyautogui:
            self.pyautogui.write(text, interval=0.01)
            if press_enter:
                self.pyautogui.press('return')
            return f"Typed {len(text)} characters on macOS"
        else:
            safe = text.replace('\\', '\\\\').replace('"', '\\"')
            script = f'tell application "System Events" to keystroke "{safe}"'
            if press_enter:
                script += '\ntell application "System Events" to key code 36'
            subprocess.run(["osascript", "-e", script], check=True)
            return f"Typed text via AppleScript"

    def press_key(self, key: str, modifiers: Optional[list] = None) -> str:
        k = key.lower().strip()
        mods = [m.lower().strip() for m in (modifiers or [])]

        if self.has_pyautogui:
            if mods:
                self.pyautogui.hotkey(*mods, k)
            else:
                self.pyautogui.press(k)
            return f"Pressed key {k}"
        else:
            mod_clauses = []
            for m in mods:
                if m in ["command", "cmd"]: mod_clauses.append("command down")
                elif m == "shift": mod_clauses.append("shift down")
                elif m in ["option", "alt"]: mod_clauses.append("option down")
                elif m in ["control", "ctrl"]: mod_clauses.append("control down")
            using_clause = f" using {{{', '.join(mod_clauses)}}}" if mod_clauses else ""
            script = f'tell application "System Events" to keystroke "{k}"{using_clause}'
            subprocess.run(["osascript", "-e", script], check=True)
            return f"Pressed key {k} via AppleScript"

    def click(self, x: Optional[int] = None, y: Optional[int] = None, button: str = "left", clicks: int = 1) -> str:
        if self.has_pyautogui:
            if x is not None and y is not None:
                self.pyautogui.click(x=x, y=y, clicks=clicks, button=button)
            else:
                self.pyautogui.click(clicks=clicks, button=button)
            return f"{button} click performed on macOS"
        return "Click simulation requires pyautogui on macOS"

    def move_mouse(self, x: int, y: int) -> str:
        if self.has_pyautogui:
            self.pyautogui.moveTo(x, y, duration=0.2)
            return f"Moved cursor to ({x}, {y})"
        return "Mouse movement requires pyautogui on macOS"

    def scroll(self, amount: int, direction: str = "down") -> str:
        delta = -amount if direction == "down" else amount
        if self.has_pyautogui:
            self.pyautogui.scroll(delta)
            return f"Scrolled {direction} on macOS"
        return "Scroll requires pyautogui on macOS"

    def take_screenshot(self, filename: Optional[str] = None) -> str:
        shots_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "screenshots")
        os.makedirs(shots_dir, exist_ok=True)
        fname = filename or f"screenshot_{int(time.time())}.png"
        target_path = os.path.join(shots_dir, fname)
        subprocess.run(["screencapture", "-x", target_path], check=True)
        return f"Screenshot captured: {target_path}"

    def get_active_window(self) -> Dict[str, Any]:
        try:
            script = 'tell application "System Events" to get name of first process whose frontmost is true'
            res = subprocess.check_output(["osascript", "-e", script], text=True).strip()
            return {"title": res or "Desktop"}
        except:
            return {"title": "macOS Active Window"}
