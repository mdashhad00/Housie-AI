"""
Housie AI — Linux Computer Controller Adapter
Implements keyboard, mouse, app, and desktop automation on Linux (X11 & Wayland).
Uses xdotool / ydotool and PyAutoGUI with xdg-open.
"""

import os
import subprocess
import time
from typing import Dict, Any, Optional
from .base import BaseController

class LinuxController(BaseController):
    def __init__(self):
        super().__init__("linux")
        self.has_pyautogui = False
        try:
            import pyautogui
            self.pyautogui = pyautogui
            self.has_pyautogui = True
        except ImportError:
            self.pyautogui = None

    def open_app(self, name: str, args: str = "") -> str:
        clean = name.lower().strip()
        app_map = {
            "chrome": "google-chrome",
            "firefox": "firefox",
            "terminal": "x-terminal-emulator",
            "calculator": "gnome-calculator",
            "code": "code",
            "vscode": "code",
            "files": "nautilus",
            "whatsapp": "whatsapp-for-linux"
        }
        cmd = app_map.get(clean, clean)
        try:
            full_cmd = f"{cmd} {args}".strip()
            subprocess.Popen(full_cmd, shell=True)
            return f"Launched Linux application: {cmd}"
        except Exception as e:
            try:
                subprocess.Popen(["xdg-open", cmd])
                return f"Opened via xdg-open: {cmd}"
            except Exception as e2:
                raise RuntimeError(f"Failed to open '{name}' on Linux: {e2}")

    def type_text(self, text: str, press_enter: bool = False) -> str:
        if self.has_pyautogui:
            self.pyautogui.write(text, interval=0.01)
            if press_enter:
                self.pyautogui.press('enter')
            return f"Typed {len(text)} characters on Linux"
        else:
            try:
                subprocess.run(["xdotool", "type", "--delay", "10", text], check=True)
                if press_enter:
                    subprocess.run(["xdotool", "key", "Return"], check=True)
                return "Typed text via xdotool"
            except:
                return "Text input requires xdotool or pyautogui on Linux"

    def press_key(self, key: str, modifiers: Optional[list] = None) -> str:
        k = key.strip()
        mods = [m.lower().strip() for m in (modifiers or [])]
        if self.has_pyautogui:
            if mods:
                self.pyautogui.hotkey(*mods, k)
            else:
                self.pyautogui.press(k)
            return f"Pressed key {k}"
        else:
            try:
                combo = "+".join(mods + [k]) if mods else k
                subprocess.run(["xdotool", "key", combo], check=True)
                return f"Pressed {combo} via xdotool"
            except:
                return f"Key press requires xdotool on Linux"

    def click(self, x: Optional[int] = None, y: Optional[int] = None, button: str = "left", clicks: int = 1) -> str:
        btn_num = "1" if button == "left" else "3" if button == "right" else "2"
        if self.has_pyautogui:
            if x is not None and y is not None:
                self.pyautogui.click(x=x, y=y, clicks=clicks, button=button)
            else:
                self.pyautogui.click(clicks=clicks, button=button)
            return f"{button} clicked on Linux"
        else:
            try:
                if x is not None and y is not None:
                    subprocess.run(["xdotool", "mousemove", str(x), str(y)], check=True)
                for _ in range(clicks):
                    subprocess.run(["xdotool", "click", btn_num], check=True)
                return f"Clicked via xdotool ({button})"
            except:
                return "Mouse click requires xdotool on Linux"

    def move_mouse(self, x: int, y: int) -> str:
        if self.has_pyautogui:
            self.pyautogui.moveTo(x, y, duration=0.2)
            return f"Moved cursor to ({x}, {y})"
        else:
            try:
                subprocess.run(["xdotool", "mousemove", str(x), str(y)], check=True)
                return f"Moved cursor via xdotool to ({x}, {y})"
            except:
                return "Cursor movement requires xdotool on Linux"

    def scroll(self, amount: int, direction: str = "down") -> str:
        # Button 4 is scroll up, Button 5 is scroll down
        btn = "5" if direction == "down" else "4"
        if self.has_pyautogui:
            delta = -amount if direction == "down" else amount
            self.pyautogui.scroll(delta)
            return f"Scrolled {direction} on Linux"
        else:
            try:
                repeat = max(1, amount // 100)
                subprocess.run(["xdotool", "click", "--repeat", str(repeat), btn], check=True)
                return f"Scrolled {direction} via xdotool"
            except:
                return "Scroll requires xdotool on Linux"

    def take_screenshot(self, filename: Optional[str] = None) -> str:
        shots_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "screenshots")
        os.makedirs(shots_dir, exist_ok=True)
        fname = filename or f"screenshot_{int(time.time())}.png"
        target_path = os.path.join(shots_dir, fname)

        for cmd in [["scrot", target_path], ["import", "-window", "root", target_path], ["gnome-screenshot", "-f", target_path]]:
            try:
                subprocess.run(cmd, check=True)
                return f"Screenshot saved: {target_path}"
            except:
                continue
        if self.has_pyautogui:
            shot = self.pyautogui.screenshot()
            shot.save(target_path)
            return f"Screenshot saved: {target_path}"
        return "Screenshot tool (scrot or gnome-screenshot) not found"

    def get_active_window(self) -> Dict[str, Any]:
        try:
            out = subprocess.check_output(["xdotool", "getactivewindow", "getwindowname"], text=True).strip()
            return {"title": out or "Desktop"}
        except:
            return {"title": "Linux Active Window"}
