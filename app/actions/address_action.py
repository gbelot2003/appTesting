# File path: app/actions/address_action.py

from app.extractors.lat_long_extractor import LatLongExtractor
from app.extractors.address_extractor import DireccionExtractor
from app.repos.contact_repo import ContactRepo
from app.models import Address
import logging

class AddressAction:
    def __init__(self, contacto, prompt):
        self.contacto = contacto
        self.prompt = prompt
        self.lat_long_extractor = LatLongExtractor()  # Inicializa el extractor de latitud y longitud

    def process_address(self):
        """
        Procesa y clasifica la dirección extraída según el tipo y la actualiza en la base de datos.
        """
        message = None
        logging.info("Iniciando AddressAction con prompt: %s", self.prompt)

        # Extraer todas las direcciones usando el extractor
        direcciones_extraidas = DireccionExtractor().extraer_todas_las_direcciones(self.prompt)
        logging.info("Direcciones extraídas: %s", direcciones_extraidas)

        if not direcciones_extraidas:
            return {"role": "system", "content": "No se pudo encontrar ninguna dirección en el texto proporcionado."}

        # Seleccionar la primera dirección encontrada para este ejemplo
        direccion_principal = direcciones_extraidas[0].lower()

        # Determinar el tipo de dirección (pickup, delivery o principal)
        tipo_direccion = self.determinar_tipo_direccion()
        
        # Si es una dirección de recogida, extraer latitud y longitud
        if tipo_direccion == "pickup":
            latitud, longitud = self.lat_long_extractor.obtener_lat_long(direccion_principal)
            nueva_direccion = Address(
                contact_id=self.contacto.id, type=tipo_direccion, address_line=direccion_principal,
                latitude=latitud, longitude=longitud, is_primary=False
            )
            ContactRepo().agregar_direccion(nueva_direccion)
            message = {"role": "assistant", "content": f"Se ha registrado la dirección de recogida: {direccion_principal} con latitud: {latitud} y longitud: {longitud}."}
        else:
            # Direcciones de entrega o principales no necesitan latitud y longitud
            nueva_direccion = Address(contact_id=self.contacto.id, type=tipo_direccion, address_line=direccion_principal, is_primary=False)
            ContactRepo().agregar_direccion(nueva_direccion)
            message = {"role": "assistant", "content": f"Se ha registrado la dirección de {tipo_direccion}: {direccion_principal}."}

        # Si se detectan múltiples direcciones, agregarlas al mensaje
        if len(direcciones_extraidas) > 1:
            message["content"] += f" Se detectaron múltiples direcciones: {', '.join(direcciones_extraidas).lower()}."

        return message

    def determinar_tipo_direccion(self):
        """
        Determina el tipo de dirección según el contenido del prompt.
        """
        if "recogida" in self.prompt.lower() or "pickup" in self.prompt.lower():
            return "pickup"
        elif "entrega" in self.prompt.lower() or "delivery" in self.prompt.lower():
            return "delivery"
        elif "principal" in self.prompt.lower():
            return "principal"
        else:
            return "other"  # Tipo genérico si no se especifica
