# File path: app/actions/address_action.py

from app.extractors.address_extractor import DireccionExtractor
from app.extractors.lat_long_extractor import LatLongExtractor
from app.models.address_model import Address
from app.repos.contact_repo import ContactRepo


class AddressAction:
    def __init__(self, contacto, prompt, db_session):
        self.contacto = contacto
        self.prompt = prompt
        self.db_session = db_session  # Sesión de base de datos
        self.contact_repo = ContactRepo  # Usar la clase ContactRepo directamente
        self.lat_long_extractor = LatLongExtractor()

    def process_address(self):
        # Asegúrate de que `self.contact_repo.actualizar_contacto` esté llamándose con `db_session`
        if self.contacto.direccion:
            direccion_formateada = self.contacto.direccion.lower()
            return {"role": "assistant", "content": f"El usuario ya tiene una dirección registrada: {direccion_formateada}."}

        direcciones_extraidas = DireccionExtractor().extraer_todas_las_direcciones(self.prompt)
        if not direcciones_extraidas:
            return {"role": "system", "content": "No se pudo encontrar ninguna dirección en el texto proporcionado."}

        direccion_principal = direcciones_extraidas[0].lower()
        tipo_direccion = self.determinar_tipo_direccion()

        if tipo_direccion == "pickup":
            latitud, longitud = self.lat_long_extractor.obtener_lat_long(direccion_principal)
            nueva_direccion = Address(contact_id=self.contacto.id, type=tipo_direccion, address_line=direccion_principal, latitude=latitud, longitude=longitud, is_primary=False)
            self.contact_repo.agregar_direccion(self.db_session, nueva_direccion)
        else:
            nueva_direccion = Address(contact_id=self.contacto.id, type=tipo_direccion, address_line=direccion_principal, is_primary=False)
            self.contact_repo.agregar_direccion(self.db_session, nueva_direccion)
