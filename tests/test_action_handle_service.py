# File path: tests/test_action_handle_service.py

import logging
import pytest
from unittest.mock import MagicMock
from app.services.action_handler_service import ActionHandleService
from app.repos.contact_repo import ContactRepo

@pytest.fixture
def mock_contact():
    """Mock para un contacto básico."""
    contact = MagicMock()
    contact.id = 1
    contact.nombre = "Juan Pérez"
    return contact

@pytest.fixture
def db_session():
    """Mock para la sesión de base de datos."""
    return MagicMock()

# File path: tests/test_action_handle_service.py

def test_handle_actions_actualizar_direccion_explicitamente(mock_contact, mocker, caplog, db_session):
    """Probar que se actualiza la dirección cuando el usuario lo solicita explícitamente."""
    caplog.set_level(logging.INFO)  # Habilitar captura de logs

    # Instanciar ActionHandleService con db_session
    user_id = "123-456-7890"
    prompt = "Quiero actualizar mi dirección a 5678 Calle Secundaria, Ciudad."
    action_service = ActionHandleService(user_id, prompt, db_session)  # Asegúrate de pasar db_session aquí

    # Mockear VerifyContactAction para que devuelva un contacto simulado
    mocker.patch('app.actions.verify_contact_action.VerifyContactAction.verificar_contacto', return_value=mock_contact)

    # Mockear NameAction para simular el mensaje generado
    mocker.patch('app.actions.name_action.NameAction.process_name', return_value={"role": "assistant", "content": "El usuario se llama Juan Pérez."})

    # Mockear ConversationHistoryAction para simular el historial de chat
    mocker.patch('app.actions.conversation_history_action.ConversationHistoryAction.compilar_conversacion', return_value=[
        {"role": "user", "content": "Hola, ¿puedes actualizar mi dirección?"},
        {"role": "assistant", "content": "Claro, ¿cuál es la nueva dirección?"}
    ])

    # Mockear `DireccionExtractor` para simular la extracción de la nueva dirección
    mocker.patch('app.extractors.address_extractor.DireccionExtractor.extraer_todas_las_direcciones', return_value=["5678 calle secundaria, ciudad"])

    # Asegúrate de que el mock esté usando la ruta completa del método `ContactRepo.actualizar_contacto`
    mock_update_contact = mocker.patch('app.repos.contact_repo.ContactRepo.actualizar_contacto')

    # Ejecutar handle_actions
    messages = action_service.handle_actions()

    # Verificar que se actualizó la dirección correctamente
    mock_update_contact.assert_called_once_with(db_session, mock_contact.id, direccion="5678 calle secundaria, ciudad")
    assert messages[-1]["content"] == "Se ha registrado la dirección de delivery: 5678 calle secundaria, ciudad."