# File path: app/extractors/address_extractor.py

import re
import logging

class DireccionExtractor:
    def __init__(self):
        # Definir patrón extendido para capturar múltiples direcciones separadas por comas
        self.patron_direcciones = r"[a-zA-Z0-9\s]+(?:,\s*[a-zA-Z0-9\s]+)+"

    def extraer_direccion(self, texto):
        """
        Extrae la primera dirección que coincida en el texto dado.
        Retorna None si no encuentra una dirección válida.
        """
        texto = texto.lower()  # Convertir a minúsculas para coincidencias insensibles a mayúsculas/minúsculas
        resultado = re.findall(self.patron_direcciones, texto)
        if resultado:
            logging.debug(f"Dirección encontrada: {resultado[0]}")
            return resultado[0].strip().capitalize()
        return None

    def extraer_todas_las_direcciones(self, texto):
        """
        Extrae todas las direcciones que coincidan en el texto dado.
        Retorna una lista de direcciones o una lista vacía si no encuentra ninguna.
        """
        texto = texto.lower()  # Convertir a minúsculas para coincidencias insensibles a mayúsculas/minúsculas
        direcciones = re.findall(self.patron_direcciones, texto)
        logging.debug(f"Direcciones encontradas: {direcciones}")
        return [direccion.strip().capitalize() for direccion in direcciones] if direcciones else []
