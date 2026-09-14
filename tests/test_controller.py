"""
Unit tests for Housie AI Computer Control & Planning Layer
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.tools import TOOL_SCHEMAS, validate_tool_call
from core.planner import Planner
from controller.factory import get_controller

def test_tool_validation():
    print("Testing tool validation...")
    # Test valid open_app
    v = validate_tool_call("open_app", {"name": "Chrome"})
    assert v["name"] == "Chrome"

    # Test missing required field
    try:
        validate_tool_call("open_app", {})
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

    # Test valid click
    v_click = validate_tool_call("click", {"x": "100", "y": "200", "button": "left", "clicks": "2"})
    assert v_click["x"] == 100
    assert v_click["y"] == 200
    assert v_click["clicks"] == 2

    print("[PASS] Tool validation passed!")

def test_planner():
    print("Testing planner intent recognition...")
    # 1. Multi-step Chrome + YouTube
    plan1 = Planner.plan_from_text("Open Chrome and search YouTube for Minecraft")
    assert len(plan1) >= 1
    assert any("youtube" in p.get("explanation", "").lower() or p["tool"] == "open_url" for p in plan1)

    # 2. WhatsApp
    plan2 = Planner.plan_from_text("Text on WhatsApp to 9876543210: Hello world")
    assert len(plan2) == 1
    assert plan2[0]["tool"] == "whatsapp_send"
    assert "9876543210" in plan2[0]["args"]["phone"]
    assert "Hello world" in plan2[0]["args"]["message"]

    # 3. Screenshot
    plan3 = Planner.plan_from_text("Take a screenshot")
    assert len(plan3) == 1
    assert plan3[0]["tool"] == "take_screenshot"

    # 4. Scroll
    plan4 = Planner.plan_from_text("Scroll down by 600")
    assert len(plan4) == 1
    assert plan4[0]["tool"] == "scroll"
    assert plan4[0]["args"]["direction"] == "down"
    assert plan4[0]["args"]["amount"] == 600

    print("[PASS] Planner tests passed!")

def test_controller_factory():
    print("Testing controller factory...")
    ctrl = get_controller()
    assert ctrl is not None
    print(f"[PASS] Controller initialized for platform: {ctrl.platform_name}")

if __name__ == "__main__":
    test_tool_validation()
    test_planner()
    test_controller_factory()
    print("\nALL TESTS PASSED SUCCESSFULLY!")
