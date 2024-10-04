# File path: tests/test_action_handle_service.py

import pytest
from unittest.mock import patch, MagicMock
from app.services.action_handler_service import ActionHandleService

@pytest.fixture
def mock_contact():
    """Mock para un contacto básico."""
    contact = MagicMock()
    contact.nombre = "Juan Pérez"
    contact.direccion = "1234 Calle Principal, Springfield"
    contact.telefono = "123-456-7890"
    return contact

def test_handle_actions(mock_contact, mocker):
    """Prueba unitaria para ActionHandleService.handle_actions."""
    
    # Mockear VerifyContactAction para que devuelva un contacto simulado
    mock_verify_contact = mocker.patch('app.actions.verify_contact_action.VerifyContactAction.verificar_contacto', return_value=mock_contact)

    # Mockear NameAction para simular el mensaje generado
    mock_name_action = mocker.patch('app.actions.name_action.NameAction.process_name', return_value={"role": "assistant", "content": "El usuario se llama Juan Pérez."})

    # Mockear ConversationHistoryAction para simular el historial de chat
    mock_conversation_action = mocker.patch('app.actions.conversation_history_action.ConversationHistoryAction.compilar_conversacion', return_value=[
        {"role": "user", "content": "Hola, ¿puedes actualizar mi dirección?"},
        {"role": "assistant", "content": "Claro, ¿cuál es la nueva dirección?"}
    ])

    # Mockear AddressAction para verificar la actualización de la dirección y el mensaje generado
    mock_address_action = mocker.patch('app.actions.address_action.AddressAction.process_address', return_value={"role": "assistant", "content": "La dirección del usuario es: 5678 calle secundaria, ciudad."})

    # Instanciar ActionHandleService con user_id y prompt
    user_id = "123-456-7890"
    prompt = "La nueva dirección es 5678 Calle Secundaria, Ciudad."
    action_service = ActionHandleService(user_id, prompt)

    # Ejecutar handle_actions
    messages = action_service.handle_actions()

    # Verificar que las acciones secundarias fueron llamadas
    mock_verify_contact.assert_called_once_with(user_id)  # Utilizar el mock retornado en lugar de la clase directamente
    mock_name_action.assert_called_once()
    mock_conversation_action.assert_called_once_with(user_id)
    mock_address_action.assert_called_once()

    # Verificar que los mensajes generados se almacenan correctamente
    assert len(messages) == 4
    assert messages[0]["content"] == "El usuario se llama Juan Pérez."
    assert messages[1]["content"] == "Hola, ¿puedes actualizar mi dirección?"
    assert messages[2]["content"] == "Claro, ¿cuál es la nueva dirección?"
    assert messages[3]["content"] == "La dirección del usuario es: 5678 calle secundaria, ciudad."
