import pytest
from flask import Flask
from unittest.mock import patch
from app.services.openai_service import OpenAIService
from app.routes.routes import bp  # Import the blueprint
from app.repos.contact_repo import ContactRepo
from app.models.contact_model import Contact
from extensions import db

# Create a Flask app instance for testing
@pytest.fixture
def client():
    # Initialize the Flask app
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory SQLite for testing
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.register_blueprint(bp)  # Register the blueprint

    # Initialize the database
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Use the Flask test client
    with app.test_client() as client:
        yield client

    # Clean up the database after the test
    with app.app_context():
        db.drop_all()

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
            "message": "Mi nombre es Juan",
            "from_number": "+14155551234"
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
        mock_handle_request.assert_called_once_with("Mi nombre es Juan", "+14155551234")

        # Verify that the contact was created in the database
        contacto = ContactRepo.obtener_contacto_por_telefono("+14155551234")
        assert contacto.nombre == "Juan"
        assert contacto is not None
