# Housie AI & SpeechAssist 🤖🎙️

**Housie AI** is a multi-modal, cross-platform AI assistant combining **Speech Recognition (Whisper)**, **Local LLM Computer Control (Qwen2.5 1.5B via llama.cpp)**, **SymPy Computer Algebra**, and **Multi-OS Native Automation (Windows, macOS, Linux, Android)**.

---

## 🏗️ Architecture: Decoupled Computer Control

The AI model does **not** directly execute arbitrary shell scripts or hold raw OS memory pointers. Instead, user intent is mapped into strictly validated JSON tool calls, which are safely dispatched to platform-specific adapters.

```
YOUR SPEECH / TEXT INPUT
       │ (Voice / STT / Web / Desktop)
       ▼
┌────────────────────────────────────────────────────────┐
│               Local AI Planner Engine                  │
│       Qwen2.5 1.5B Instruct Q4_K_M (~1.1 GB RAM)       │
│    (with zero-latency Regex/Grammar rule fallback)     │
└──────────────────────────┬─────────────────────────────┘
                           │ Tool / Action Decision (Strict JSON)
                           ▼
┌────────────────────────────────────────────────────────┐
│           COMPUTER CONTROL SAFETY GUARD LAYER          │
│  Validates: open_app, type_text, click, press_key,     │
│             scroll, take_screenshot, whatsapp_send     │
└──────────────────────────┬─────────────────────────────┘
                           │ Dispatches safe commands
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
   ┌───────────┐     ┌───────────┐     ┌───────────┐     ┌───────────┐
   │  Windows  │     │   macOS   │     │   Linux   │     │  Android  │
   │ Win32/PS/ │     │ AppleScr/ │     │ xdotool/  │     │ Intents/  │
   │ PyAutoGUI │     │ PyAutoGUI │     │  xdg-open │     │ Termux/ADB│
   └───────────┘     └───────────┘     └───────────┘     └───────────┘
```

---

## 🌟 Key Features

1. **🖥️ Cross-Platform Computer Control:**
   - Control mouse, keyboard, applications, and windows via voice or text.
   - Built-in adapters for **Windows**, **macOS**, **Linux**, and **Android**.
   - Zero-external-dependency fallback: works immediately via standard OS utilities (`os.startfile`, `osascript`, `xdg-open`, `am start`).

2. **🧠 4 GB RAM Optimized Local AI:**
   - Uses `Qwen2.5-1.5B-Instruct-Q4_K_M.gguf` requiring only **~1.1 GB of RAM**.
   - In-browser Whisper WASM speech recognition uses **~75 MB**.
   - Total system footprint stays comfortably under 2.5 GB RAM.

3. **🎙️ SpeechAssist 3D Interface:**
   - 3D glassmorphic SaaS interface with metallic floating microphone and animated glowing sound waves.
   - Live speech transcription, persistent History drawer with search, and full vocal settings modal.

4. **💬 Automated WhatsApp Flow:**
   - Sends messages automatically with pre-filled numbers and text via `https://wa.me/` and desktop/Android intent integrations.

5. **📐 SymPy Math & Science Engine:**
   - Solves calculus, derivatives, integrals, polynomial roots, LCM/GCD, and 30+ science concepts.

---

## 🚀 Quick Start

### 1. Run Python Backend (Recommended)

```bash
# Clone the repository
git clone https://github.com/mdashhad00/Housie-AI.git
cd Housie-AI

# Install core dependencies
pip install flask flask-cors sympy

# (Optional) For direct hardware cursor control and local GGUF model execution:
# pip install pyautogui pillow llama-cpp-python

# Start the Housie AI server
python app.py
```

Open `http://localhost:5000` in your browser!

To launch the 3D Speech Assistance interface directly, navigate to:
`http://localhost:5000/speech-assist/index.html`

---

## 🧪 Running Tests

The test suite validates tool schema enforcement, intent planning, OS controller factory resolution, and API endpoints:

```bash
# Run controller & planner unit tests
python tests/test_controller.py

# Run API endpoint tests (/api/control & /api/control/models)
python tests/test_api_control.py
```

---

## 📁 Repository Structure

```
housie-ai-app/
├── core/
│   ├── tools.py          # Controlled tool schemas & safety validators
│   ├── planner.py        # Intent parser & rule-based execution planner
│   └── llm_engine.py     # Qwen2.5 1.5B llama.cpp loader & downloader
├── controller/
│   ├── base.py           # BaseController abstract class
│   ├── windows.py        # Windows OS automation adapter
│   ├── macos.py          # macOS automation adapter (AppleScript)
│   ├── linux.py          # Linux automation adapter (xdotool / xdg)
│   ├── android.py        # Android automation adapter (Intents / ADB)
│   └── factory.py        # Dynamic OS detection & controller factory
├── speech-assist/
│   └── index.html        # 3D SpeechAssist web interface
├── tests/
│   ├── test_controller.py   # Unit test suite
│   └── test_api_control.py  # Flask API test suite
├── electron/             # Native desktop app wrapper
├── app.py                # Flask server with /api/control endpoints
├── server.js             # Express Node.js alternative backend
└── requirements.txt      # Python dependencies
```
