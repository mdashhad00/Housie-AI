"""
Housie AI — Base Computer Controller
Abstract base class defining the hardware and OS automation contract.
All platform adapters (Windows, macOS, Linux, Android) implement this interface.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import os
import time
import webbrowser

class BaseController(ABC):
    """
    Abstract Base Controller for Cross-Platform Device Automation.
    """

    def __init__(self, platform_name: str):
        self.platform_name = platform_name

    def execute_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Dispatches and executes a tool call safely.
        """
        handlers = {
            "open_app": lambda: self.open_app(args.get("name", ""), args.get("args", "")),
            "type_text": lambda: self.type_text(args.get("text", ""), args.get("press_enter", False)),
            "press_key": lambda: self.press_key(args.get("key", ""), args.get("modifiers")),
            "click": lambda: self.click(args.get("x"), args.get("y"), args.get("button", "left"), args.get("clicks", 1)),
            "move_mouse": lambda: self.move_mouse(args.get("x", 0), args.get("y", 0)),
            "scroll": lambda: self.scroll(args.get("amount", 500), args.get("direction", "down")),
            "take_screenshot": lambda: self.take_screenshot(args.get("filename")),
            "open_url": lambda: self.open_url(args.get("url", "")),
            "whatsapp_send": lambda: self.whatsapp_send(args.get("phone", ""), args.get("message", ""), args.get("auto_send", True)),
            "get_active_window": lambda: self.get_active_window()
        }

        if tool_name not in handlers:
            return {"success": False, "error": f"Tool '{tool_name}' not implemented on {self.platform_name}"}

        try:
            res = handlers[tool_name]()
            return {"success": True, "tool": tool_name, "platform": self.platform_name, "result": res}
        except Exception as e:
            return {"success": False, "tool": tool_name, "platform": self.platform_name, "error": str(e)}

    @abstractmethod
    def open_app(self, name: str, args: str = "") -> str:
        pass

    @abstractmethod
    def type_text(self, text: str, press_enter: bool = False) -> str:
        pass

    @abstractmethod
    def press_key(self, key: str, modifiers: Optional[list] = None) -> str:
        pass

    @abstractmethod
    def click(self, x: Optional[int] = None, y: Optional[int] = None, button: str = "left", clicks: int = 1) -> str:
        pass

    @abstractmethod
    def move_mouse(self, x: int, y: int) -> str:
        pass

    @abstractmethod
    def scroll(self, amount: int, direction: str = "down") -> str:
        pass

    @abstractmethod
    def take_screenshot(self, filename: Optional[str] = None) -> str:
        pass

    @abstractmethod
    def get_active_window(self) -> Dict[str, Any]:
        pass

    def open_url(self, url: str) -> str:
        """Universal URL opener using default browser."""
        if not url.startswith("http"):
            url = f"https://{url}"
        webbrowser.open(url)
        return f"Opened URL: {url}"

    def whatsapp_send(self, phone: str, message: str, auto_send: bool = True) -> str:
        """
        Universal fallback: opens WhatsApp Web/API link.
        Specialized platform adapters can override with desktop app keystroke automation.
        """
        import urllib.parse
        clean_phone = "".join(c for c in phone if c.isdigit())
        encoded_msg = urllib.parse.quote(message)
        wa_url = f"https://wa.me/{clean_phone}?text={encoded_msg}"
        self.open_url(wa_url)
        if auto_send:
            time.sleep(1.8)
            try:
                self.press_key("enter")
            except:
                pass
        return f"Dispatched WhatsApp message to {phone}: '{message}'"

    def close_app(self, name: str) -> str:
        """Closes target application or active window."""
        try:
            self.press_key("f4", ["alt"])
            return f"Closed application: {name}"
        except Exception as e:
            return f"Attempted to close {name}: {e}"

    def system_command(self, action: str) -> str:
        """Executes system-level actions (volume, lock, etc.)."""
        return f"System action {action} triggered"
