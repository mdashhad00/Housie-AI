"""
Housie AI — Computer Control Tool Definitions
Defines the controlled set of actions the small local LLM (Qwen2.5 1.5B) can invoke.
The AI model outputs structured JSON tool calls that are strictly validated before execution.
"""

from typing import Dict, Any, List

TOOL_SCHEMAS: List[Dict[str, Any]] = [
    {
        "name": "open_app",
        "description": "Opens or focuses a native desktop application, browser, or system tool by name.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the application, e.g., 'Chrome', 'WhatsApp', 'Notepad', 'Calculator', 'Spotify', 'Terminal', 'VS Code'."
                },
                "args": {
                    "type": "string",
                    "description": "Optional command-line arguments or target URL (e.g., website link for browsers)."
                }
            },
            "required": ["name"]
        }
    },
    {
        "name": "type_text",
        "description": "Types text into the currently active window or input field, optionally pressing Enter.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The exact string of text to type."
                },
                "press_enter": {
                    "type": "boolean",
                    "description": "Whether to press the Enter/Return key after typing (default: false)."
                }
            },
            "required": ["text"]
        }
    },
    {
        "name": "press_key",
        "description": "Simulates pressing a single key or key combination (e.g., 'enter', 'tab', 'escape', 'ctrl+c', 'ctrl+v', 'alt+f4', 'space').",
        "parameters": {
            "type": "object",
            "properties": {
                "key": {
                    "type": "string",
                    "description": "The primary key name (e.g. 'enter', 'tab', 'backspace', 'up', 'down', 'f5')."
                },
                "modifiers": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional modifier keys such as ['ctrl'], ['alt'], ['shift'], ['meta']."
                }
            },
            "required": ["key"]
        }
    },
    {
        "name": "click",
        "description": "Clicks the mouse at specified coordinates or current cursor location.",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {
                    "type": "integer",
                    "description": "X coordinate on screen (optional, defaults to current position)."
                },
                "y": {
                    "type": "integer",
                    "description": "Y coordinate on screen (optional, defaults to current position)."
                },
                "button": {
                    "type": "string",
                    "enum": ["left", "right", "middle"],
                    "description": "Mouse button to click (default: 'left')."
                },
                "clicks": {
                    "type": "integer",
                    "description": "Number of clicks: 1 for single click, 2 for double click (default: 1)."
                }
            }
        }
    },
    {
        "name": "move_mouse",
        "description": "Moves the mouse cursor smoothly to target coordinates.",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {"type": "integer", "description": "Target X screen coordinate."},
                "y": {"type": "integer", "description": "Target Y screen coordinate."}
            },
            "required": ["x", "y"]
        }
    },
    {
        "name": "scroll",
        "description": "Scrolls the active window vertically or horizontally.",
        "parameters": {
            "type": "object",
            "properties": {
                "amount": {
                    "type": "integer",
                    "description": "Scroll distance in units/clicks. Positive for down/right, negative for up/left."
                },
                "direction": {
                    "type": "string",
                    "enum": ["up", "down", "left", "right"],
                    "description": "Direction to scroll (default: 'down')."
                }
            },
            "required": ["amount"]
        }
    },
    {
        "name": "take_screenshot",
        "description": "Captures the current desktop screen and saves it as an image file.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "Optional custom filename to save the screenshot."
                }
            }
        }
    },
    {
        "name": "open_url",
        "description": "Opens a web link or URL in the system default web browser.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL to open, e.g., 'https://youtube.com', 'https://google.com'."
                }
            },
            "required": ["url"]
        }
    },
    {
        "name": "whatsapp_send",
        "description": "Sends or stages a WhatsApp text message to a specific contact number.",
        "parameters": {
            "type": "object",
            "properties": {
                "phone": {
                    "type": "string",
                    "description": "The recipient's phone number with country code, e.g., '+919876543210'."
                },
                "message": {
                    "type": "string",
                    "description": "The message body to send."
                },
                "auto_send": {
                    "type": "boolean",
                    "description": "Whether to auto-press Enter to send (default: true)."
                }
            },
            "required": ["phone", "message"]
        }
    },
    {
        "name": "get_active_window",
        "description": "Returns the title and process name of the currently focused window on the device.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "close_app",
        "description": "Closes an active application or window by name or closes the active window.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the application, e.g. 'Notepad', 'Chrome', 'Calculator', or 'current'."
                }
            },
            "required": ["name"]
        }
    },
    {
        "name": "system_command",
        "description": "Performs system-level actions like volume control, mute, lock screen, or minimize windows.",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["volume_up", "volume_down", "volume_mute", "lock_screen", "minimize_all", "show_desktop"],
                    "description": "The system action to execute."
                }
            },
            "required": ["action"]
        }
    }
]

def validate_tool_call(tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates tool name and arguments against schemas.
    Returns sanitized arguments dict or raises ValueError.
    """
    schema = next((s for s in TOOL_SCHEMAS if s["name"] == tool_name), None)
    if not schema:
        raise ValueError(f"Unknown tool: '{tool_name}'")

    props = schema["parameters"].get("properties", {})
    required = schema["parameters"].get("required", [])

    for req in required:
        if req not in args or args[req] is None or (isinstance(args[req], str) and not args[req].strip()):
            raise ValueError(f"Missing required parameter '{req}' for tool '{tool_name}'")

    sanitized = {}
    for k, v in args.items():
        if k in props:
            expected_type = props[k].get("type")
            if expected_type == "integer" and v is not None:
                try:
                    sanitized[k] = int(v)
                except (ValueError, TypeError):
                    raise ValueError(f"Parameter '{k}' must be an integer, got {v}")
            elif expected_type == "boolean" and v is not None:
                sanitized[k] = bool(v)
            elif expected_type == "string" and v is not None:
                sanitized[k] = str(v)
            else:
                sanitized[k] = v

    return sanitized
