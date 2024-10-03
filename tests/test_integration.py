import pytest
import requests
import json
import os

BASE_URL = "http://127.0.0.1:5000"

def test_index_route():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

def test_api_message_route():
    payload = {
        "message": "Este es un mensaje de prueba"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(f"{BASE_URL}/api/message", data=json.dumps(payload), headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "response" in response.json()