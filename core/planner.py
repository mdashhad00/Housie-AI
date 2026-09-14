"""
Housie AI — Execution Planner & Intent Classifier
Turns spoken/text input into a concrete plan of validated tool calls.
Works with Qwen2.5-1.5B LLM or instant rule-based semantic parser.
"""

import re
from typing import List, Dict, Any
from .tools import validate_tool_call

class PlanStep:
    def __init__(self, tool: str, args: Dict[str, Any], explanation: str = ""):
        self.tool = tool
        self.args = validate_tool_call(tool, args)
        self.explanation = explanation

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tool": self.tool,
            "args": self.args,
            "explanation": self.explanation
        }

class Planner:
    """
    Translates user requests into ordered, executable computer control actions.
    """

    @staticmethod
    def plan_from_text(text: str) -> List[Dict[str, Any]]:
        clean = text.strip()
        steps: List[PlanStep] = []

        # 1. WhatsApp Texting
        wa_match = re.search(
            r'(?:text|message|send|msg|bhejo)\s+(?:on\s+|pe\s+)?whatsapp\s+(?:to\s+|ko\s+)?([0-9+\s\-]{7,16})[:\s]+(.+)',
            clean, re.IGNORECASE
        ) or re.search(
            r'whatsapp\s+(?:pe\s+)?([0-9+\s\-]{7,16})\s+(?:ko\s+)?(?:message|text|bhejo)?[:\s]+(.+)',
            clean, re.IGNORECASE
        )
        if wa_match:
            phone = re.sub(r'[^0-9+]', '', wa_match.group(1))
            msg = wa_match.group(2).strip()
            steps.append(PlanStep("whatsapp_send", {"phone": phone, "message": msg, "auto_send": True}, f"Send WhatsApp message to {phone}"))
            return [s.to_dict() for s in steps]

        # 2. Multi-step: "Open [App/Browser] and search [Query]"
        search_pattern = re.search(
            r'(?:open|launch|kholo)\s+([a-zA-Z0-9\s]+?)\s+and\s+(?:search|look\s+up|play|type)\s+(?:for\s+)?(.+)',
            clean, re.IGNORECASE
        )
        if search_pattern:
            app_raw = search_pattern.group(1).strip()
            query = search_pattern.group(2).strip()

            if re.search(r'youtube|yt', app_raw, re.IGNORECASE):
                yt_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
                steps.append(PlanStep("open_url", {"url": yt_url}, f"Open YouTube search for '{query}'"))
                return [s.to_dict() for s in steps]
            elif re.search(r'google|chrome|edge|firefox|browser', app_raw, re.IGNORECASE):
                g_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                steps.append(PlanStep("open_url", {"url": g_url}, f"Search Google for '{query}'"))
                return [s.to_dict() for s in steps]
            else:
                steps.append(PlanStep("open_app", {"name": app_raw}, f"Open {app_raw}"))
                steps.append(PlanStep("type_text", {"text": query, "press_enter": True}, f"Type '{query}' and press Enter"))
                return [s.to_dict() for s in steps]

        # 3. Open URL
        url_match = re.search(r'(?:open|go\s+to|visit)\s+(https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9\-]+\.(?:com|org|io|net|edu|dev))', clean, re.IGNORECASE)
        if url_match:
            raw_url = url_match.group(1)
            full_url = raw_url if raw_url.startswith("http") else f"https://{raw_url}"
            steps.append(PlanStep("open_url", {"url": full_url}, f"Open website {full_url}"))
            return [s.to_dict() for s in steps]

        # 4. Open Application
        app_match = re.search(r'(?:open|launch|start|run|chalao|kholo)\s+(?:the\s+)?([a-zA-Z0-9\s\.\-_]+?)(?:\s+app|\s+application)?$', clean, re.IGNORECASE)
        if app_match:
            target_app = app_match.group(1).strip()
            # Ignore common non-apps
            if target_app.lower() not in ["camera", "photo", "microphone", "door", "window"]:
                steps.append(PlanStep("open_app", {"name": target_app}, f"Launch application {target_app}"))
                return [s.to_dict() for s in steps]

        # 5. Type text
        type_match = re.search(r'(?:type|write|enter|likho)\s+["\']?(.+?)["\']?(?:\s+and\s+press\s+enter)?$', clean, re.IGNORECASE)
        if type_match:
            text_to_type = type_match.group(1).strip()
            press_enter = bool(re.search(r'press\s+enter|enter\s+dabao', clean, re.IGNORECASE))
            steps.append(PlanStep("type_text", {"text": text_to_type, "press_enter": press_enter}, f"Type '{text_to_type}'"))
            return [s.to_dict() for s in steps]

        # 6. Press key / shortcut
        key_match = re.search(r'(?:press|hit|dabao)\s+([a-zA-Z0-9\+\s]+)', clean, re.IGNORECASE)
        if key_match:
            raw_keys = key_match.group(1).lower().strip()
            if '+' in raw_keys:
                parts = [p.strip() for p in raw_keys.split('+')]
                modifiers = parts[:-1]
                key = parts[-1]
                steps.append(PlanStep("press_key", {"key": key, "modifiers": modifiers}, f"Press shortcut {'+'.join(parts)}"))
                return [s.to_dict() for s in steps]
            else:
                steps.append(PlanStep("press_key", {"key": raw_keys}, f"Press key {raw_keys}"))
                return [s.to_dict() for s in steps]

        # 7. Screenshot
        if re.search(r'screenshot|screen\s+capture|screen\s+grab|screencap', clean, re.IGNORECASE):
            steps.append(PlanStep("take_screenshot", {}, "Capture full screen"))
            return [s.to_dict() for s in steps]

        # 8. Scroll
        scroll_match = re.search(r'scroll\s+(up|down|left|right)(?:\s+by\s+(\d+))?', clean, re.IGNORECASE)
        if scroll_match:
            direction = scroll_match.group(1).lower()
            amount = int(scroll_match.group(2)) if scroll_match.group(2) else 500
            steps.append(PlanStep("scroll", {"amount": amount, "direction": direction}, f"Scroll {direction}"))
            return [s.to_dict() for s in steps]

        # 9. Mouse click
        click_match = re.search(r'(?:click|double\s+click|right\s+click)(?:\s+at\s+(\d+)[,\s]+(\d+))?', clean, re.IGNORECASE)
        if click_match:
            is_double = "double" in clean.lower()
            is_right = "right" in clean.lower()
            button = "right" if is_right else "left"
            clicks = 2 if is_double else 1
            x = int(click_match.group(1)) if click_match.group(1) else None
            y = int(click_match.group(2)) if click_match.group(2) else None
            args = {"button": button, "clicks": clicks}
            if x is not None and y is not None:
                args["x"] = x
                args["y"] = y
            steps.append(PlanStep("click", args, f"{'Double ' if is_double else ''}{button} click"))
            return [s.to_dict() for s in steps]

        return []
