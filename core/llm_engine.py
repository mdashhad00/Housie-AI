"""
Housie AI — Local LLM Engine (Qwen2.5 1.5B Q4_K_M via llama.cpp)
Optimized for 4 GB RAM machines (~1.1 GB memory footprint).
Translates user voice & text instructions into safe, structured tool calls.
"""

import os
import json
import urllib.request
import threading
from typing import List, Dict, Any, Optional, Callable
from .tools import TOOL_SCHEMAS, validate_tool_call
from .planner import Planner

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
MODEL_FILENAME = "qwen2.5-1.5b-instruct-q4_k_m.gguf"
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILENAME)
MODEL_URL = "https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf"

SYSTEM_PROMPT = """You are the computer-control planning engine for Housie AI.
Given a user command, your ONLY job is to select the correct sequence of tools to accomplish the task.
Output MUST be a JSON array of tool calls matching the available schemas. Do NOT output Markdown code fences or extra conversational text.

Available Tools:
""" + json.dumps(TOOL_SCHEMAS, indent=2) + """

Example user: "Open Chrome and search YouTube for Minecraft"
Output:
[
  {"tool": "open_app", "args": {"name": "Chrome"}},
  {"tool": "open_url", "args": {"url": "https://www.youtube.com/results?search_query=Minecraft"}}
]

Example user: "Text on WhatsApp to 9876543210: Hey I'll be home soon"
Output:
[
  {"tool": "whatsapp_send", "args": {"phone": "9876543210", "message": "Hey I'll be home soon", "auto_send": true}}
]
"""

class LLMEngine:
    _instance: Optional['LLMEngine'] = None
    _lock = threading.Lock()

    def __init__(self):
        self.model = None
        self.model_status = "idle"  # idle | downloading | ready | error
        self.download_progress = 0
        self.download_error = None
        self._init_local_model()

    @classmethod
    def get_instance(cls) -> 'LLMEngine':
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    def _init_local_model(self):
        if os.path.exists(MODEL_PATH):
            try:
                from llama_cpp import Llama
                # 4 GB RAM optimization: n_ctx=2048, n_threads=4, n_gpu_layers=0 for CPU
                self.model = Llama(
                    model_path=MODEL_PATH,
                    n_ctx=2048,
                    n_threads=max(1, os.cpu_count() or 4),
                    verbose=False
                )
                self.model_status = "ready"
            except ImportError:
                self.model_status = "needs_llama_cpp"
            except Exception as e:
                self.model_status = "error"
                self.download_error = str(e)
        else:
            self.model_status = "not_downloaded"

    def download_model(self, progress_callback: Optional[Callable[[int], None]] = None) -> bool:
        if self.model_status in ["downloading", "ready"]:
            return True

        def _do_download():
            self.model_status = "downloading"
            self.download_progress = 0
            os.makedirs(MODEL_DIR, exist_ok=True)

            temp_path = MODEL_PATH + ".tmp"
            try:
                def _report(block_num, block_size, total_size):
                    if total_size > 0:
                        pct = int(min(100, (block_num * block_size / total_size) * 100))
                        self.download_progress = pct
                        if progress_callback:
                            progress_callback(pct)

                urllib.request.urlretrieve(MODEL_URL, temp_path, reporthook=_report)
                if os.path.exists(temp_path):
                    if os.path.exists(MODEL_PATH):
                        os.remove(MODEL_PATH)
                    os.rename(temp_path, MODEL_PATH)

                self._init_local_model()
            except Exception as e:
                self.model_status = "error"
                self.download_error = str(e)
                if os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except:
                        pass

        thread = threading.Thread(target=_do_download, daemon=True)
        thread.start()
        return True

    def generate_tool_plan(self, user_query: str) -> List[Dict[str, Any]]:
        """
        Generates a validated list of tool calls using Qwen2.5 1.5B LLM,
        or falls back to high-speed deterministic semantic planner.
        """
        # If Qwen 1.5B is loaded, query the model
        if self.model and self.model_status == "ready":
            try:
                prompt = f"<|im_start|>system\n{SYSTEM_PROMPT}<|im_end|>\n<|im_start|>user\n{user_query}<|im_end|>\n<|im_start|>assistant\n"
                output = self.model(
                    prompt,
                    max_tokens=256,
                    stop=["<|im_end|>", "\n\n"],
                    temperature=0.1
                )
                raw_text = output["choices"][0]["text"].strip()
                # Parse JSON array
                raw_json = re.search(r'\[\s*\{.*?\}\s*\]', raw_text, re.DOTALL)
                if raw_json:
                    parsed = json.loads(raw_json.group(0))
                    validated = []
                    for item in parsed:
                        if "tool" in item:
                            t_name = item["tool"]
                            t_args = item.get("args", {})
                            val_args = validate_tool_call(t_name, t_args)
                            validated.append({"tool": t_name, "args": val_args})
                    if validated:
                        return validated
            except Exception as e:
                # LLM parse error, fallback smoothly
                pass

        # Deterministic instant planner fallback
        return Planner.plan_from_text(user_query)
