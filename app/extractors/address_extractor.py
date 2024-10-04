# File path: app/extractors/address_extractor.py

import re
import logging

class DireccionExtractor:
    def __init__(self):
        # Modificar el patrón para evitar capturar texto adicional
        # Se añade un patrón para ignorar las palabras iniciales y capturar solo la dirección
        self.patron_direccion = r"(?:mi dirección es|la dirección es|vivo en|resido en|puedes encontrarme en|me encuentro en|la ubicación es|mi ubicación es|mi dirección actual es|mi nueva dirección es|actualiza mi dirección a|cambia mi dirección a|la dirección actual es)\s*([\w\s\d,]+)"

    def extraer_direccion(self, texto):
        """
        Extrae la primera dirección que coincida en el texto dado.
        Retorna None si no encuentra una dirección válida.
        """
        texto = texto.lower()  # Convertir a minúsculas para coincidencias insensibles a mayúsculas/minúsculas
        resultado = re.findall(self.patron_direccion, texto)
        if resultado:
            logging.debug(f"Dirección encontrada: {resultado[0]}")
            return resultado[0].strip().capitalize()  # Limpiar y capitalizar la dirección encontrada
        return None

    def extraer_todas_las_direcciones(self, texto):
        """
        Extrae todas las direcciones que coincidan en el texto dado.
        Retorna una lista de direcciones o una lista vacía si no encuentra ninguna.
        """
        texto = texto.lower()  # Convertir a minúsculas para coincidencias insensibles a mayúsculas/minúsculas
        direcciones = re.findall(self.patron_direccion, texto)
        logging.debug(f"Direcciones encontradas: {direcciones}")
        return [direccion.strip().capitalize() for direccion in direcciones] if direcciones else []
