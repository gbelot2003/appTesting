# File path: app/actions/address_action.py

from app.extractors.address_extractor import DireccionExtractor
from app.repos.contact_repo import ContactRepo
import logging

class AddressAction:
    def __init__(self, contacto, prompt):
        self.contacto = contacto
        self.prompt = prompt

    def process_address(self):
        message = None
        logging.info("Iniciando AddressAction con prompt: %s", self.prompt)

        try:
            # Si el contacto ya tiene una dirección, usarla en la conversación
            if self.contacto.direccion:
                direccion_formateada = self.contacto.direccion.lower()
                message = {"role": "assistant", "content": f"El usuario ya tiene una dirección registrada: {direccion_formateada}."}
                logging.info("El contacto ya tiene una dirección registrada: %s", direccion_formateada)
            else:
                # Extraer todas las direcciones usando el extractor
                logging.info("Intentando extraer direcciones del prompt...")
                direcciones_extraidas = DireccionExtractor().extraer_todas_las_direcciones(self.prompt)
                logging.info("Direcciones extraídas: %s", direcciones_extraidas)

                if direcciones_extraidas:
                    # Seleccionar la primera dirección encontrada
                    direccion_principal = direcciones_extraidas[0].lower()
                    # Actualizar la dirección del contacto en la base de datos
                    ContactRepo().actualizar_contacto(self.contacto.id, direccion=direccion_principal)
                    message = {"role": "assistant", "content": f"La dirección del usuario es: {direccion_principal}."}
                    if len(direcciones_extraidas) > 1:
                        message["content"] += f" Se detectaron múltiples direcciones: {', '.join(direcciones_extraidas).lower()}."
                else:
                    message = {"role": "system", "content": "No se pudo encontrar la dirección. Pregunte al usuario su dirección para mejor servicio."}
        except Exception as e:
            logging.error(f"Error al actualizar la dirección: {str(e)}")
            message = {"role": "system", "content": "No se pudo actualizar la dirección en la base de datos debido a un error interno."}

        return message
