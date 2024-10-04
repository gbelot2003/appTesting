# File path: tests/test_address_action.py

import pytest
from unittest.mock import patch, MagicMock
from app.actions.address_action import AddressAction
from app.extractors.address_extractor import DireccionExtractor
from app.repos.contact_repo import ContactRepo

# Mock del Contacto y de los métodos del repositorio para simular el comportamiento
class MockContact:
    def __init__(self, id, direccion=None):
        self.id = id
        self.direccion = direccion

@pytest.fixture
def contacto_sin_direccion():
    return MockContact(id=2, direccion=None)

def test_address_action_con_direccion_preexistente():
    """Probar que se usa la dirección ya registrada en lugar de extraer una nueva."""
    contacto = MockContact(id=1, direccion="1234 Calle Principal, Ciudad")
    action = AddressAction(contacto, "El usuario quiere actualizar su dirección a 5678 Calle Secundaria, Ciudad.")
    message = action.process_address()
    assert message["content"] == "El usuario ya tiene una dirección registrada: 1234 calle principal, ciudad."

def test_address_action_sin_direccion_exito(contacto_sin_direccion, mocker):
    """Probar que se extrae la dirección correctamente del prompt cuando no hay dirección previa."""
    prompt = "Vivo en 5678 Calle Secundaria, Ciudad"
    mocker.patch.object(DireccionExtractor, 'extraer_todas_las_direcciones', return_value=["5678 calle secundaria, ciudad"])
    mocker.patch.object(ContactRepo, 'actualizar_contacto')

    action = AddressAction(contacto_sin_direccion, prompt)
    message = action.process_address()

    ContactRepo.actualizar_contacto.assert_called_once_with(2, direccion="5678 calle secundaria, ciudad")
    assert message["content"] == "La dirección del usuario es: 5678 calle secundaria, ciudad."

def test_address_action_direcciones_internacionales(contacto_sin_direccion, mocker):
    """Probar direcciones internacionales con diferentes formatos."""
    prompt = "La dirección es 10 Downing St, Westminster, London SW1A 2AA, United Kingdom."
    mocker.patch.object(DireccionExtractor, 'extraer_todas_las_direcciones', return_value=["10 downing st, westminster, london sw1a 2aa, united kingdom"])
    mocker.patch.object(ContactRepo, 'actualizar_contacto')

    action = AddressAction(contacto_sin_direccion, prompt)
    message = action.process_address()

    ContactRepo.actualizar_contacto.assert_called_once_with(2, direccion="10 downing st, westminster, london sw1a 2aa, united kingdom")
    assert message["content"] == "La dirección del usuario es: 10 downing st, westminster, london sw1a 2aa, united kingdom."

def test_address_action_multiple_direcciones(contacto_sin_direccion, mocker):
    """Probar que se detectan múltiples direcciones y se usa la primera."""
    prompt = "Mis direcciones son 1234 Calle Principal, Ciudad y 5678 Calle Secundaria, Ciudad."
    mocker.patch.object(DireccionExtractor, 'extraer_todas_las_direcciones', return_value=["1234 calle principal, ciudad", "5678 calle secundaria, ciudad"])
    mocker.patch.object(ContactRepo, 'actualizar_contacto')

    action = AddressAction(contacto_sin_direccion, prompt)
    message = action.process_address()

    ContactRepo.actualizar_contacto.assert_called_once_with(2, direccion="1234 calle principal, ciudad")
    assert message["content"] == "La dirección del usuario es: 1234 calle principal, ciudad. Se detectaron múltiples direcciones: 1234 calle principal, ciudad, 5678 calle secundaria, ciudad."

def test_address_action_direccion_incompleta(contacto_sin_direccion, mocker):
    """Probar que se detecta dirección incluso si está incompleta."""
    prompt = "La dirección es 5678 Calle Secundaria"
    mocker.patch.object(DireccionExtractor, 'extraer_todas_las_direcciones', return_value=["5678 calle secundaria"])
    mocker.patch.object(ContactRepo, 'actualizar_contacto')

    action = AddressAction(contacto_sin_direccion, prompt)
    message = action.process_address()

    ContactRepo.actualizar_contacto.assert_called_once_with(2, direccion="5678 calle secundaria")
    assert message["content"] == "La dirección del usuario es: 5678 calle secundaria."

def test_address_action_sin_direccion_fallo(contacto_sin_direccion, mocker):
    """Probar que se maneja correctamente cuando no se encuentra ninguna dirección."""
    prompt = "No hay dirección en este texto."
    mocker.patch.object(DireccionExtractor, 'extraer_todas_las_direcciones', return_value=[])

    action = AddressAction(contacto_sin_direccion, prompt)
    message = action.process_address()

    assert message["content"] == "No se pudo encontrar la dirección. Pregunte al usuario su dirección para mejor servicio."
