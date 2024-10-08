# test_update_address_action.py

import pytest
from unittest.mock import patch, MagicMock
from app.actions.update_address_action import UpdateAddressAction
from app.repos.contact_repo import ContactRepo
from app.models.contact_model import Contact
from extensions import db
from flask import Flask
from app.routes.routes import bp


@pytest.fixture
def client():
    """Fixture para configurar el cliente de pruebas de Flask."""
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Registrar el blueprint y configurar la base de datos
    app.register_blueprint(bp)
    db.init_app(app)

    # Crear las tablas en la base de datos
    with app.app_context():
        db.create_all()

    # Crear un cliente de pruebas
    with app.test_client() as client:
        yield client

    # Limpiar la base de datos
    with app.app_context():
        db.drop_all()


@pytest.fixture
def contacto_existente(client):
    """Fixture para crear un contacto en la base de datos antes del test."""
    with client.application.app_context():
        nuevo_contacto = Contact(
            nombre="Carlos", telefono="+14155551234", direccion="Calle Falsa 123"
        )
        db.session.add(nuevo_contacto)
        db.session.commit()
        db.session.refresh(nuevo_contacto)

    yield nuevo_contacto


def test_update_address_success(contacto_existente, client):
    """Test para verificar que se actualiza la dirección correctamente."""
    # Mock del extractor de direcciones
    with patch("app.actions.update_address_action.DireccionExtractor") as MockDireccionExtractor:
        mock_extractor = MockDireccionExtractor.return_value
        mock_extractor.extraer_direccion.return_value = "1234 Calle Principal, Ciudad"

        # Mock del repositorio de contactos usando el path correcto con patch.object
        with patch.object(ContactRepo, 'obtener_contacto_por_telefono', return_value=contacto_existente) as mock_obtener_contacto:
            with patch.object(ContactRepo, 'actualizar_contacto', return_value=contacto_existente) as mock_actualizar_contacto:

                # Asegurar contexto de aplicación para la prueba
                with client.application.app_context():
                    # Crear la acción con datos de prueba
                    action = UpdateAddressAction(
                        telefono="+14155551234",
                        texto="Quiero cambiar mi dirección a 1234 Calle Principal, Ciudad",
                    )

                    # Imprimir información del mock antes de ejecutar
                    print(f"Mock obtener_contacto_por_telefono antes de ejecutar: {mock_obtener_contacto.mock_calls}")

                    # Ejecutar la acción dentro del contexto de la aplicación
                    resultado = action.ejecutar()

                    # Verificar que la dirección fue extraída y se actualizó correctamente
                    mock_extractor.extraer_direccion.assert_called_once_with(
                        "Quiero cambiar mi dirección a 1234 Calle Principal, Ciudad"
                    )
                    mock_obtener_contacto.assert_called_once_with("+14155551234")
                    mock_actualizar_contacto.assert_called_once_with(
                        contacto_existente.id, direccion="1234 Calle Principal, Ciudad"
                    )

                    # Verificar el resultado final de la ejecución
                    assert resultado["status"] == "success"
                    assert (
                        resultado["message"]
                        == "Dirección actualizada a: 1234 Calle Principal, Ciudad"
                    )


def test_update_address_contact_not_found(client):
    """Test para verificar que UpdateAddressAction devuelve error cuando no se encuentra el contacto."""
    # Mock del extractor de direcciones usando el path correcto
    with patch("app.actions.update_address_action.DireccionExtractor") as MockDireccionExtractor:
        mock_extractor = MockDireccionExtractor.return_value
        mock_extractor.extraer_direccion.return_value = "1234 Calle Principal, Ciudad"

        # Mock del repositorio de contactos usando el path correcto con patch.object
        with patch.object(ContactRepo, 'obtener_contacto_por_telefono', return_value=None) as mock_obtener_contacto:
            with patch.object(ContactRepo, 'actualizar_contacto') as mock_actualizar_contacto:

                # Asegurar contexto de aplicación para la prueba
                with client.application.app_context():
                    # Crear la acción con datos de prueba
                    action = UpdateAddressAction(
                        telefono="+14155551234",
                        texto="Quiero cambiar mi dirección a 1234 Calle Principal, San Antonio",
                    )

                    # Imprimir información del mock antes de ejecutar
                    print(f"Mock obtener_contacto_por_telefono antes de ejecutar: {mock_obtener_contacto.mock_calls}")

                    # Ejecutar la acción dentro del contexto de la aplicación
                    resultado = action.ejecutar()

                    # Verificar que se devolvió el mensaje de error apropiado
                    assert resultado["status"] == "error"
                    assert (
                        resultado["message"]
                        == "No se encontró el contacto con el teléfono +14155551234"
                    )

                    # Verificar que el método obtener_contacto_por_telefono fue llamado correctamente
                    mock_obtener_contacto.assert_called_once_with("+14155551234")

def test_update_address_invalid_address():
    # Mock del extractor de direcciones para que no encuentre ninguna dirección válida
    with patch(
        "app.actions.update_address_action.DireccionExtractor"
    ) as MockDireccionExtractor:
        mock_extractor = MockDireccionExtractor.return_value
        mock_extractor.extraer_direccion.return_value = (
            None  # No se encontró ninguna dirección
        )

        # Crear la acción con datos de prueba
        action = UpdateAddressAction(
            telefono="+14155551234", texto="No hay dirección en este mensaje"
        )
        resultado = action.ejecutar()

        # Verificar que se devolvió el mensaje de error apropiado
        assert resultado["status"] == "error"
        assert (
            resultado["message"]
            == "No se pudo extraer una dirección válida del texto proporcionado."
        )