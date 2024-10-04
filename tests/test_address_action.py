# File path: tests/test_address_action.py

import pytest
from unittest.mock import MagicMock, patch
from app.actions.address_action import AddressAction
from app.repos.contact_repo import ContactRepo
from app.extractors.address_extractor import DireccionExtractor

# Mock del Contacto y de los métodos del repositorio para simular el comportamiento
class MockContact:
    def __init__(self, id, direccion=None):
        self.id = id
        self.direccion = direccion

@pytest.fixture
def contacto_sin_direccion():
    return MockContact(id=2, direccion=None)

@pytest.fixture
def db_session():
    return MagicMock()

def test_address_action_sin_direccion_exito(contacto_sin_direccion, mocker, db_session):
    """Probar que se extrae la dirección correctamente del prompt cuando no hay dirección previa."""
    prompt = "Vivo en 5678 Calle Secundaria, Ciudad"
    
    # Mockear la extracción de direcciones
    mocker.patch.object(DireccionExtractor, 'extraer_todas_las_direcciones', return_value=["5678 calle secundaria, ciudad"])
    
    # Mockear ContactRepo.actualizar_contacto y verificar que se llame correctamente
    mock_update_contact = mocker.patch('app.repos.contact_repo.ContactRepo.actualizar_contacto')

    action = AddressAction(contacto_sin_direccion, prompt, db_session)
    message = action.process_address()

    # Verificar que ContactRepo.actualizar_contacto fue llamado con los parámetros correctos
    mock_update_contact.assert_called_once_with(db_session, 2, direccion="5678 calle secundaria, ciudad")
    assert message["content"] == "La dirección del usuario es: 5678 calle secundaria, ciudad."
