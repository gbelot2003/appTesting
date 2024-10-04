# File path: tests/test_address_action.py

import pytest
from app.actions.address_action import AddressAction
from app.repos.contact_repo import ContactRepo
from app.extractors.address_extractor import DireccionExtractor

# Mock del Contacto y de los métodos del repositorio para simular el comportamiento
class MockContact:
    def __init__(self, id, direccion=None):
        self.id = id
        self.direccion = direccion

@pytest.fixture
def contacto_con_direccion():
    return MockContact(id=1, direccion="1234 Calle Principal, Ciudad")

@pytest.fixture
def contacto_sin_direccion():
    return MockContact(id=2, direccion=None)

def test_address_action_con_direccion(contacto_con_direccion):
    prompt = "El usuario vive en 5678 Calle Secundaria, Ciudad"
    action = AddressAction(contacto_con_direccion, prompt)
    message = action.process_address()
    assert message["role"] == "assistant"
    # Convertir ambas direcciones a minúsculas para una comparación insensible a mayúsculas/minúsculas
    assert message["content"].lower() == "el usuario ya tiene una dirección registrada: 1234 calle principal, ciudad.".lower()

def test_address_action_sin_direccion_exito(contacto_sin_direccion, mocker):
    prompt = "El usuario vive en 5678 Calle Secundaria, Ciudad"
    mocker.patch.object(DireccionExtractor, 'extraer_todas_las_direcciones', return_value=["5678 calle secundaria, ciudad"])
    mocker.patch.object(ContactRepo, 'actualizar_contacto')

    action = AddressAction(contacto_sin_direccion, prompt)
    message = action.process_address()

    # Verificar que se actualizó la dirección y se generó el mensaje correcto
    ContactRepo.actualizar_contacto.assert_called_once_with(2, direccion="5678 calle secundaria, ciudad")
    assert message["role"] == "assistant"
    assert message["content"] == "La dirección del usuario es: 5678 calle secundaria, ciudad."

def test_address_action_multiples_direcciones(contacto_sin_direccion, mocker):
    prompt = "El usuario vive en 5678 Calle Secundaria, Ciudad y 91011 Avenida Tercera, Estado"
    mocker.patch.object(DireccionExtractor, 'extraer_todas_las_direcciones', return_value=["5678 calle secundaria, ciudad", "91011 avenida tercera, estado"])
    mocker.patch.object(ContactRepo, 'actualizar_contacto')

    action = AddressAction(contacto_sin_direccion, prompt)
    message = action.process_address()

    # Verificar que se actualizó la dirección y se generó el mensaje correcto
    ContactRepo.actualizar_contacto.assert_called_once_with(2, direccion="5678 calle secundaria, ciudad")
    assert message["role"] == "assistant"
    assert message["content"] == "La dirección del usuario es: 5678 calle secundaria, ciudad. Se detectaron múltiples direcciones: 5678 calle secundaria, ciudad, 91011 avenida tercera, estado."

def test_address_action_sin_direccion_fallo(contacto_sin_direccion, mocker):
    prompt = "No hay dirección en el texto."
    mocker.patch.object(DireccionExtractor, 'extraer_todas_las_direcciones', return_value=[])

    action = AddressAction(contacto_sin_direccion, prompt)
    message = action.process_address()

    # Verificar que no se actualizó la dirección y se generó un mensaje de error
    assert message["role"] == "system"
    assert message["content"] == "No se pudo encontrar la dirección. Pregunte al usuario su dirección para mejor servicio."
