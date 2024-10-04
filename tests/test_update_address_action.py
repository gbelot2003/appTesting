# tests/test_update_address_action.py
import pytest
from unittest.mock import patch, MagicMock
from app.actions.update_address_action import UpdateAddressAction
from app.repos.contact_repo import ContactRepo
from app.models.contact_model import Contact

@pytest.fixture
def contacto_existente():
    # Crear un contacto simulado
    return Contact(id=1, nombre="Carlos", telefono="+14155551234", direccion="Calle Falsa 123")

def test_update_address_success(contacto_existente):
    # Mock del extractor de direcciones
    with patch('app.actions.update_address_action.DireccionExtractor') as MockDireccionExtractor:
        mock_extractor = MockDireccionExtractor.return_value
        mock_extractor.extraer_direccion.return_value = "1234 Calle Principal, Ciudad"

        # Mock del repositorio de contactos
        with patch('app.actions.update_address_action.ContactRepo') as MockContactRepo:
            # Configurar el mock para que devuelva el contacto existente
            mock_repo = MockContactRepo.return_value
            mock_repo.obtener_contacto_por_telefono.return_value = contacto_existente
            mock_repo.actualizar_contacto.return_value = contacto_existente

            # Crear la acción con datos de prueba
            action = UpdateAddressAction(telefono="+14155551234", texto="Quiero cambiar mi dirección a 1234 Calle Principal, Ciudad")
            resultado = action.ejecutar()

            # Verificar que la dirección fue extraída y se actualizó correctamente
            mock_extractor.extraer_direccion.assert_called_once_with("Quiero cambiar mi dirección a 1234 Calle Principal, Ciudad")
            mock_repo.obtener_contacto_por_telefono.assert_called_once_with("+14155551234")
            mock_repo.actualizar_contacto.assert_called_once_with(contacto_existente.id, direccion="1234 Calle Principal, Ciudad")

            # Verificar el resultado final de la ejecución
            assert resultado["status"] == "success"
            assert resultado["message"] == "Dirección actualizada a: 1234 Calle Principal, Ciudad"

def test_update_address_contact_not_found():
    # Mock del extractor de direcciones
    with patch('app.actions.update_address_action.DireccionExtractor') as MockDireccionExtractor:
        mock_extractor = MockDireccionExtractor.return_value
        mock_extractor.extraer_direccion.return_value = "1234 Calle Principal, Ciudad"

        # Mock del repositorio de contactos para que no devuelva ningún contacto
        with patch('app.actions.update_address_action.ContactRepo') as MockContactRepo:
            mock_repo = MockContactRepo()
            
            # Asegurarse de que el mock devuelve None al buscar por teléfono
            mock_repo.obtener_contacto_por_telefono.return_value = None

            # Crear la acción con datos de prueba
            action = UpdateAddressAction(telefono="+14155551234", texto="Quiero cambiar mi dirección a 1234 Calle Principal, Ciudad")
            resultado = action.ejecutar()

            # Verificar que se devolvió el mensaje de error apropiado
            assert resultado["status"] == "error"
            assert resultado["message"] == "No se encontró el contacto con el teléfono +14155551234"

            # Verificar que el método obtener_contacto_por_telefono fue llamado correctamente
            mock_repo.obtener_contacto_por_telefono.assert_called_once_with("+14155551234")

def test_update_address_invalid_address():
    # Mock del extractor de direcciones para que no encuentre ninguna dirección válida
    with patch('app.actions.update_address_action.DireccionExtractor') as MockDireccionExtractor:
        mock_extractor = MockDireccionExtractor.return_value
        mock_extractor.extraer_direccion.return_value = None  # No se encontró ninguna dirección

        # Crear la acción con datos de prueba
        action = UpdateAddressAction(telefono="+14155551234", texto="No hay dirección en este mensaje")
        resultado = action.ejecutar()

        # Verificar que se devolvió el mensaje de error apropiado
        assert resultado["status"] == "error"
        assert resultado["message"] == "No se pudo extraer una dirección válida del texto proporcionado."
