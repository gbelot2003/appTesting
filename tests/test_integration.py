# test/test_integration.py
import pytest
from flask import Flask
from unittest.mock import patch
from app.services.openai_service import OpenAIService
from app.routes.routes import bp  # Import the blueprint

# Create a Flask app instance for testing
@pytest.fixture
def client():
    # Initialize the Flask app
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(bp)  # Register the blueprint

    # Use the Flask test client
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test the index route of the Flask app."""
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"message": "Hello, World!"}

def test_api_message_route(client):
    """Test the /api/message route of the Flask app."""
    # Use patch to mock the OpenAIService.handle_request method
    with patch.object(OpenAIService, 'handle_request') as mock_handle_request:
        # Mock return value for the handle_request method
        mock_handle_request.return_value = {"status": "success", "response": "Respuesta simulada"}

        # Prepare the payload and headers
        payload = {
            "message": "Este es un mensaje de prueba"
        }
        headers = {
            'Content-Type': 'application/json'
        }

        # Use the Flask test client to send POST request to /api/message
        response = client.post('/api/message', json=payload, headers=headers)

        # Validate the response
        assert response.status_code == 200
        assert response.json["status"] == "success"
        assert "response" in response.json
        assert response.json["response"] == "Respuesta simulada"

        # Verify that the mock was called with the correct argument
        mock_handle_request.assert_called_once_with("Este es un mensaje de prueba")
