"""
End-to-end Flask API tests for Computer Control Layer
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

def test_api_control_preview():
    print("Testing /api/control in preview mode (execute=False)...")
    client = app.test_client()

    res = client.post('/api/control', json={
        "message": "Open Chrome and search YouTube for Minecraft",
        "execute": False
    })

    assert res.status_code == 200, f"Status code: {res.status_code}"
    data = res.get_json()
    assert data["success"] is True
    assert "platform" in data
    assert len(data["plan"]) >= 1
    print(f"[PASS] Planned {len(data['plan'])} action(s) for query.")
    for idx, step in enumerate(data["plan"]):
        print(f"       Step {idx+1}: {step['tool']} -> {step['args']}")

def test_api_models_endpoint():
    print("\nTesting /api/control/models endpoint...")
    client = app.test_client()
    res = client.get('/api/control/models')
    assert res.status_code == 200
    data = res.get_json()
    print(f"[PASS] Model status: {data['status']}, Target RAM: {data['ram_target']}")

def test_api_control_whatsapp():
    print("\nTesting /api/control for WhatsApp intent...")
    client = app.test_client()
    res = client.post('/api/control', json={
        "message": "Text on WhatsApp to 9876543210: Hello this is automated test",
        "execute": False
    })
    assert res.status_code == 200
    data = res.get_json()
    assert len(data["plan"]) == 1
    assert data["plan"][0]["tool"] == "whatsapp_send"
    print(f"[PASS] WhatsApp tool planned: {data['plan'][0]['args']['phone']}")

if __name__ == "__main__":
    test_api_control_preview()
    test_api_models_endpoint()
    test_api_control_whatsapp()
    print("\nALL API CONTROL TESTS PASSED SUCCESSFULLY!")
