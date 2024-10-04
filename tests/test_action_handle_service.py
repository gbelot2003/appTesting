# File path: tests/test_action_handle_service.py

import pytest
from unittest.mock import patch, MagicMock
from app.services.action_handler_service import ActionHandleService
from app.repos.contact_repo import ContactRepo

@pytest.fixture
def mock_contact():
    """Mock para un contacto básico."""
    contact = MagicMock()
    contact.id = 1
    contact.nombre = "Juan Pérez"
    contact.direccion = None  # El contacto no tiene una dirección inicial
    return contact

def test_handle_actions_actualizar_direccion(mock_contact, mocker):
    """Probar que se actualiza la dirección en la base de datos correctamente."""
    
    # Mockear VerifyContactAction para que devuelva un contacto simulado
    mock_verify_contact = mocker.patch('app.actions.verify_contact_action.VerifyContactAction.verificar_contacto', return_value=mock_contact)

    # Mockear NameAction para simular el mensaje generado
    mock_name_action = mocker.patch('app.actions.name_action.NameAction.process_name', return_value={"role": "assistant", "content": "El usuario se llama Juan Pérez."})

    # Mockear ConversationHistoryAction para simular el historial de chat
    mock_conversation_action = mocker.patch('app.actions.conversation_history_action.ConversationHistoryAction.compilar_conversacion', return_value=[
        {"role": "user", "content": "Hola, ¿puedes actualizar mi dirección?"},
        {"role": "assistant", "content": "Claro, ¿cuál es la nueva dirección?"}
    ])

    # Mockear `DireccionExtractor` para simular la extracción de la dirección
    mock_direccion_extractor = mocker.patch('app.extractors.address_extractor.DireccionExtractor.extraer_todas_las_direcciones', return_value=["5678 calle secundaria, ciudad"])

    # Mockear el método `actualizar_contacto` de `ContactRepo` para verificar que se llama correctamente
    mock_update_contact = mocker.patch.object(ContactRepo, 'actualizar_contacto')

    # Instanciar ActionHandleService con user_id y prompt
    user_id = "123-456-7890"
    prompt = "La nueva dirección es 5678 Calle Secundaria, Ciudad."
    action_service = ActionHandleService(user_id, prompt)

    # Ejecutar handle_actions
    messages = action_service.handle_actions()

    # Verificar que las acciones secundarias fueron llamadas
    mock_verify_contact.assert_called_once_with(user_id)
    mock_name_action.assert_called_once()
    mock_conversation_action.assert_called_once_with(user_id)

    # Verificar que `DireccionExtractor.extraer_todas_las_direcciones` fue llamado
    mock_direccion_extractor.assert_called_once()

    # Verificar que ContactRepo.actualizar_contacto fue llamado con el ID del contacto y la nueva dirección
    mock_update_contact.assert_called_once_with(mock_contact.id, direccion="5678 calle secundaria, ciudad")

    # Verificar que los mensajes generados se almacenan correctamente
    assert len(messages) == 4
    assert messages[0]["content"] == "El usuario se llama Juan Pérez."
    assert messages[1]["content"] == "Hola, ¿puedes actualizar mi dirección?"
    assert messages[2]["content"] == "Claro, ¿cuál es la nueva dirección?"
    assert messages[3]["content"] == "La dirección del usuario es: 5678 calle secundaria, ciudad."
