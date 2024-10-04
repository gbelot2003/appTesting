# tests/test_update_address_action.py
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
    # Crear un contacto de prueba
    with client.application.app_context():
        nuevo_contacto = Contact(
            nombre="Carlos", telefono="+14155551234", direccion="Calle Falsa 123"
        )
        db.session.add(nuevo_contacto)
        db.session.commit()
        db.session.refresh(nuevo_contacto)  # Refrescar la instancia dentro de la sesión

    yield nuevo_contacto

def test_verificar_contacto_existente(contacto_existente, client):
    """Test para verificar que el contacto fue creado correctamente en la base de datos."""
    with client.application.app_context():
        # Intentar obtener el contacto por su número de teléfono
        contacto = ContactRepo.obtener_contacto_por_telefono(
            contacto_existente.telefono
        )

        # Verificar que el contacto fue encontrado y tiene los atributos esperados
        assert (
            contacto is not None
        ), "El contacto no fue encontrado en la base de datos."
        assert (
            contacto.nombre == "Carlos"
        ), f"Se esperaba el nombre 'Carlos', pero se encontró: {contacto.nombre}"
        assert (
            contacto.telefono == "+14155551234"
        ), f"Se esperaba el teléfono '+14155551234', pero se encontró: {contacto.telefono}"
        assert (
            contacto.direccion == "Calle Falsa 123"
        ), f"Se esperaba la dirección 'Calle Falsa 123', pero se encontró: {contacto.direccion}"

def test_update_address_success(contacto_existente, client):
    """Test para verificar que se actualiza la dirección correctamente."""
    # Mock del extractor de direcciones
    with patch(
        "app.actions.update_address_action.DireccionExtractor"
    ) as MockDireccionExtractor:
        mock_extractor = MockDireccionExtractor.return_value
        mock_extractor.extraer_direccion.return_value = "1234 Calle Principal, Ciudad"

        # Mock del repositorio de contactos usando el path correcto
        with patch("app.repos.contact_repo.ContactRepo") as MockContactRepo:
            # Configurar el mock para que devuelva el contacto existente
            mock_repo = MockContactRepo.return_value
            mock_repo.obtener_contacto_por_telefono.return_value = contacto_existente
            mock_repo.actualizar_contacto.return_value = contacto_existente

            # Asegurar contexto de aplicación para la prueba
            with client.application.app_context():
                # Crear la acción con datos de prueba
                action = UpdateAddressAction(
                    telefono="+14155551234",
                    texto="Quiero cambiar mi dirección a 1234 Calle Principal, Ciudad",
                )

                # Ejecutar la acción dentro del contexto de la aplicación
                resultado = action.ejecutar()

                # Verificar que la dirección fue extraída y se actualizó correctamente
                mock_extractor.extraer_direccion.assert_called_once_with(
                    "Quiero cambiar mi dirección a 1234 Calle Principal, Ciudad"
                )
                mock_repo.obtener_contacto_por_telefono.assert_called_once_with(
                    "+14155551234"
                )
                mock_repo.actualizar_contacto.assert_called_once_with(
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
    with patch(
        "app.actions.update_address_action.DireccionExtractor"
    ) as MockDireccionExtractor:
        mock_extractor = MockDireccionExtractor.return_value
        mock_extractor.extraer_direccion.return_value = "1234 Calle Principal, Ciudad"

        # Mock del repositorio de contactos usando el path correcto
        with patch(
            "app.repos.contact_repo.ContactRepo", autospec=True
        ) as MockContactRepo:
            mock_repo_instance = MockContactRepo.return_value

            # Configurar el mock para que devuelva None al buscar un contacto por teléfono.
            mock_repo_instance.obtener_contacto_por_telefono.return_value = None

            # Asegurar contexto de aplicación para la prueba
            with client.application.app_context():
                # Crear la acción con datos de prueba
                action = UpdateAddressAction(
                    telefono="+14155551234",
                    texto="Quiero cambiar mi dirección a 1234 Calle Principal, Ciudad",
                )

                # Ejecutar la acción dentro del contexto de la aplicación
                resultado = action.ejecutar()

                # Verificar que se devolvió el mensaje de error apropiado
                assert resultado["status"] == "error"
                assert (
                    resultado["message"]
                    == "No se encontró el contacto con el teléfono +14155551234"
                )

                # Verificar que el método obtener_contacto_por_telefono fue llamado correctamente
                mock_repo_instance.obtener_contacto_por_telefono.assert_called_once_with(
                    "+14155551234"
                )

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