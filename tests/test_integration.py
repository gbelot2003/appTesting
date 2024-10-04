# File path: tests/test_integration.py

import pytest
from unittest.mock import patch, MagicMock
from flask.testing import FlaskClient
from app.repos.contact_repo import ContactRepo
from app.models.contact_model import Contact
from extensions import db  # Asumiendo que la extensión de db está correctamente configurada
from app import create_app

@pytest.fixture
def client():
    # Crear la app y el cliente para pruebas
    app = create_app()  # Asegúrate de que esta función esté correctamente definida
    app.config['TESTING'] = True

    # Limpiar la base de datos antes de cada prueba
    with app.app_context():
        db.create_all()
    
    # Devolver el cliente de pruebas
    yield app.test_client()

    # Limpiar la base de datos después de cada prueba
    with app.app_context():
        db.session.remove()
        db.drop_all()

def test_api_message_route(client: FlaskClient):
    """Test the /api/message route of the Flask app."""
    with patch.object(ContactRepo, 'obtener_contacto_por_telefono') as mock_obtener_contacto:
        # Simular que no existe el contacto inicialmente
        mock_obtener_contacto.return_value = None

        # Crear un contacto simulado para la prueba
        contacto_mock = MagicMock()
        contacto_mock.telefono = "+14155551234"
        contacto_mock.nombre = "Juan"

        # Preparar el payload y headers
        payload = {
            "message": "Mi nombre es Juan",
            "from_number": "+14155551234"
        }
        headers = {
            'Content-Type': 'application/json'
        }

        # Simular una solicitud POST a la ruta /api/message
        response = client.post('/api/message', json=payload, headers=headers)

        # Verificar que el estado de la respuesta es 200
        assert response.status_code == 200
        assert response.json["status"] == "success"
        assert "response" in response.json

        # Verificar que el mock fue llamado con los argumentos correctos, incluyendo db_session
        mock_obtener_contacto.assert_called_once_with(db.session, "+14155551234")
