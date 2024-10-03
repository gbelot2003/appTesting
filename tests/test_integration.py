import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

def test_index_route():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}