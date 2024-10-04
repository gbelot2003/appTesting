# File path: src/actions/address_action.py

from app.extractors.address_extractor import DireccionExtractor
from app.repos.contact_repo import ContactRepo
import logging

class AddressAction:
    def __init__(self, contacto, prompt):
        self.contacto = contacto
        self.prompt = prompt

    def process_address(self):
        message = None

        # Si el contacto ya tiene una dirección, usarla en la conversación
        if self.contacto.direccion:
            # Convertir la dirección a minúsculas para asegurar consistencia
            direccion_formateada = self.contacto.direccion.lower()
            message = {"role": "assistant", "content": f"El usuario ya tiene una dirección registrada: {direccion_formateada}."}
        else:
            # Extraer todas las direcciones usando el extractor
            direcciones_extraidas = DireccionExtractor().extraer_todas_las_direcciones(self.prompt)
            if direcciones_extraidas:
                # Seleccionar la primera dirección encontrada para este ejemplo
                direccion_principal = direcciones_extraidas[0].lower()  # Convertir a minúsculas
                # Actualizar la dirección del contacto en la base de datos
                ContactRepo().actualizar_contacto(self.contacto.id, direccion=direccion_principal)
                
                message = {"role": "assistant", "content": f"La dirección del usuario es: {direccion_principal}."}
                
                # Si se detectan múltiples direcciones, generar un mensaje adicional
                if len(direcciones_extraidas) > 1:
                    message["content"] += f" Se detectaron múltiples direcciones: {', '.join(direcciones_extraidas).lower()}."
            else:
                # Si no se encuentra dirección, indicar que se pregunte al usuario
                message = {"role": "system", "content": "No se pudo encontrar la dirección. Pregunte al usuario su dirección para mejor servicio."}

        return message
