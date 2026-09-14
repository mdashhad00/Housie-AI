"""
Housie AI — Windows Computer Controller Adapter
Implements mouse, keyboard, app, and window control for Microsoft Windows.
Uses PyAutoGUI when installed, with native Win32 / PowerShell fallback.
"""

import os
import sys
import subprocess
import time
from typing import Dict, Any, Optional
from .base import BaseController

class WindowsController(BaseController):
    def __init__(self):
        super().__init__("windows")
        self.has_pyautogui = False
        try:
            import pyautogui
            pyautogui.FAILSAFE = True
            self.pyautogui = pyautogui
            self.has_pyautogui = True
        except ImportError:
            self.pyautogui = None

    def open_app(self, name: str, args: str = "") -> str:
        clean_name = name.lower().strip()
        app_map = {
            "chrome": "chrome",
            "google chrome": "chrome",
            "edge": "msedge",
            "microsoft edge": "msedge",
            "firefox": "firefox",
            "brave": "brave",
            "opera": "opera",
            "notepad": "notepad",
            "calculator": "calc",
            "calc": "calc",
            "camera": "microsoft.windows.camera:",
            "webcam": "microsoft.windows.camera:",
            "photos": "ms-photos:",
            "paint": "mspaint",
            "mspaint": "mspaint",
            "snipping tool": "snippingtool",
            "snippingtool": "snippingtool",
            "spotify": "spotify:",
            "whatsapp": "whatsapp:",
            "discord": "discord:",
            "telegram": "telegram:",
            "zoom": "zoommtg:",
            "code": "code",
            "vs code": "code",
            "vscode": "code",
            "visual studio code": "code",
            "terminal": "wt",
            "windows terminal": "wt",
            "powershell": "powershell",
            "cmd": "cmd",
            "command prompt": "cmd",
            "explorer": "explorer",
            "file explorer": "explorer",
            "files": "explorer",
            "downloads": "shell:Downloads",
            "documents": "shell:Personal",
            "settings": "ms-settings:",
            "task manager": "taskmgr",
            "taskmgr": "taskmgr",
            "control panel": "control",
            "word": "winword",
            "excel": "excel",
            "powerpoint": "powerpnt",
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "gmail": "https://mail.google.com",
            "maps": "https://maps.google.com",
            "github": "https://github.com",
            "chatgpt": "https://chatgpt.com",
            "netflix": "https://www.netflix.com"
        }

        target = app_map.get(clean_name, clean_name)
        try:
            if target.endswith(":") or target.startswith("http") or target.startswith("shell:"):
                os.startfile(target)
                return f"Launched Windows application: {name} ({target})"
            else:
                cmd = f"start {target} {args}".strip()
                subprocess.Popen(cmd, shell=True)
                return f"Launched Windows application: {name} ({target})"
        except Exception as e:
            try:
                subprocess.Popen(f"start {target}", shell=True)
                return f"Started {target} via Windows Shell"
            except Exception as e2:
                raise RuntimeError(f"Failed to open '{name}': {e2}")

    def close_app(self, name: str) -> str:
        clean_name = name.lower().strip()
        proc_map = {
            "notepad": "notepad.exe",
            "chrome": "chrome.exe",
            "edge": "msedge.exe",
            "calc": "CalculatorApp.exe",
            "calculator": "CalculatorApp.exe",
            "paint": "mspaint.exe",
            "code": "Code.exe",
            "spotify": "Spotify.exe",
            "whatsapp": "WhatsApp.exe",
            "terminal": "WindowsTerminal.exe",
            "cmd": "cmd.exe"
        }

        if clean_name in ["current", "active", "this", "window", "tab"]:
            self.press_key("f4", ["alt"])
            return "Closed active window (Alt+F4)"

        proc = proc_map.get(clean_name)
        if proc:
            try:
                subprocess.run(f"taskkill /IM {proc} /F", shell=True, check=False)
                return f"Terminated {proc} successfully"
            except:
                pass
        self.press_key("f4", ["alt"])
        return f"Sent close command to {name}"

    def system_command(self, action: str) -> str:
        act = action.lower().strip()
        if act == "volume_up":
            ps_cmd = '$w = New-Object -ComObject WScript.Shell; 1..5 | ForEach-Object { $w.SendKeys([char]175) }'
            subprocess.run(["powershell", "-Command", ps_cmd], check=False)
            return "Volume increased 🔊"
        elif act == "volume_down":
            ps_cmd = '$w = New-Object -ComObject WScript.Shell; 1..5 | ForEach-Object { $w.SendKeys([char]174) }'
            subprocess.run(["powershell", "-Command", ps_cmd], check=False)
            return "Volume decreased 🔉"
        elif act == "volume_mute":
            ps_cmd = '$w = New-Object -ComObject WScript.Shell; $w.SendKeys([char]173)'
            subprocess.run(["powershell", "-Command", ps_cmd], check=False)
            return "Volume toggled/muted 🔇"
        elif act == "lock_screen":
            subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True, check=False)
            return "Workstation locked 🔒"
        elif act in ["minimize_all", "show_desktop"]:
            ps_cmd = '(New-Object -ComObject Shell.Application).MinimizeAll()'
            subprocess.run(["powershell", "-Command", ps_cmd], check=False)
            return "All windows minimized 🖥️"
        return f"Executed system command: {action}"

    def type_text(self, text: str, press_enter: bool = False) -> str:
        if self.has_pyautogui:
            self.pyautogui.write(text, interval=0.01)
            if press_enter:
                self.pyautogui.press('enter')
            return f"Typed {len(text)} characters{' + Enter' if press_enter else ''}"
        else:
            # Fallback: PowerShell WScript.Shell SendKeys
            safe_text = text.replace('"', '""').replace('`', '``')
            ps_cmd = f'$wshell = New-Object -ComObject WScript.Shell; $wshell.SendKeys("{safe_text}")'
            if press_enter:
                ps_cmd += '; $wshell.SendKeys("{ENTER}")'
            subprocess.run(["powershell", "-Command", ps_cmd], check=True)
            return f"Typed text via PowerShell SendKeys"

    def press_key(self, key: str, modifiers: Optional[list] = None) -> str:
        k = key.lower().strip()
        mods = [m.lower().strip() for m in (modifiers or [])]

        if self.has_pyautogui:
            if mods:
                self.pyautogui.hotkey(*mods, k)
                return f"Pressed hotkey: {'+'.join(mods)}+{k}"
            else:
                self.pyautogui.press(k)
                return f"Pressed key: {k}"
        else:
            # PowerShell fallback
            key_code = f"{{{k.upper()}}}" if len(k) > 1 else k
            mod_prefix = ""
            if "ctrl" in mods: mod_prefix += "^"
            if "shift" in mods: mod_prefix += "+"
            if "alt" in mods: mod_prefix += "%"
            send_str = f"{mod_prefix}{key_code}"
            ps_cmd = f'$wshell = New-Object -ComObject WScript.Shell; $wshell.SendKeys("{send_str}")'
            subprocess.run(["powershell", "-Command", ps_cmd], check=True)
            return f"Pressed {send_str} via PowerShell"

    def click(self, x: Optional[int] = None, y: Optional[int] = None, button: str = "left", clicks: int = 1) -> str:
        if self.has_pyautogui:
            if x is not None and y is not None:
                self.pyautogui.click(x=x, y=y, clicks=clicks, button=button)
                return f"{button.capitalize()} clicked at ({x}, {y}) {clicks} time(s)"
            else:
                self.pyautogui.click(clicks=clicks, button=button)
                return f"{button.capitalize()} clicked at current position {clicks} time(s)"
        else:
            import ctypes
            # Win32 mouse_event
            if x is not None and y is not None:
                self.move_mouse(x, y)
            flags = 0x02 | 0x04 if button == "left" else 0x08 | 0x10  # DOWN | UP
            for _ in range(clicks):
                ctypes.windll.user32.mouse_event(flags, 0, 0, 0, 0)
                time.sleep(0.05)
            return f"Win32 {button} click performed"

    def move_mouse(self, x: int, y: int) -> str:
        if self.has_pyautogui:
            self.pyautogui.moveTo(x, y, duration=0.2)
            return f"Moved cursor to ({x}, {y})"
        else:
            import ctypes
            ctypes.windll.user32.SetCursorPos(int(x), int(y))
            return f"Set cursor position to ({x}, {y})"

    def scroll(self, amount: int, direction: str = "down") -> str:
        delta = -amount if direction == "down" else amount
        if self.has_pyautogui:
            self.pyautogui.scroll(delta)
            return f"Scrolled {direction} by {amount}"
        else:
            import ctypes
            # MOUSEEVENTF_WHEEL = 0x0800
            ctypes.windll.user32.mouse_event(0x0800, 0, 0, int(delta), 0)
            return f"Scrolled {direction} via Win32 mouse wheel"

    def take_screenshot(self, filename: Optional[str] = None) -> str:
        shots_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "screenshots")
        os.makedirs(shots_dir, exist_ok=True)
        fname = filename or f"screenshot_{int(time.time())}.png"
        target_path = os.path.join(shots_dir, fname)

        if self.has_pyautogui:
            shot = self.pyautogui.screenshot()
            shot.save(target_path)
            return f"Screenshot saved to: {target_path}"
        else:
            ps_cmd = f"""
            Add-Type -AssemblyName System.Windows.Forms,System.Drawing
            $screen = [System.Windows.Forms.Screen]::PrimaryScreen
            $bitmap = New-Object System.Drawing.Bitmap $screen.Bounds.Width, $screen.Bounds.Height
            $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
            $graphics.CopyFromScreen($screen.Bounds.X, $screen.Bounds.Y, 0, 0, $bitmap.Size)
            $bitmap.Save('{target_path}')
            $graphics.Dispose()
            $bitmap.Dispose()
            """
            subprocess.run(["powershell", "-Command", ps_cmd], check=True)
            return f"Screenshot saved to: {target_path}"

    def get_active_window(self) -> Dict[str, Any]:
        try:
            import ctypes
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
            return {"hwnd": hwnd, "title": buff.value or "Desktop"}
        except:
            return {"hwnd": 0, "title": "Windows Active Window"}
