# File path: app/extractors/address_extractor.py

import re
import logging

class DireccionExtractor:
    def __init__(self):
        # Definir patrones para direcciones comunes, extendiendo para capturar ciudad, estado, y país.
        self.patrones_direccion = [
            r"(?:mi dirección es|la dirección es|vivo en|resido en|puedes encontrarme en|me encuentro en|la ubicación es|mi ubicación es|mi dirección actual es|mi nueva dirección es|actualiza mi dirección a|cambia mi dirección a|la dirección actual es)\s+([\w\s\d,]+(?:, [\w\s]+){0,3})",  
            # El patrón permite hasta 3 segmentos adicionales separados por comas (ciudad, estado, país)
        ]

    def extraer_direccion(self, texto):
        texto = texto.lower()  # Convertir el texto a minúsculas para coincidencias insensibles a mayúsculas/minúsculas
        for patron in self.patrones_direccion:
            resultado = re.findall(patron, texto)
            if resultado:
                logging.debug(f"Dirección encontrada con el patrón: {patron}")
                return resultado[0].strip().capitalize()  # Capitaliza y limpia la dirección encontrada
        return None  # Retorna None si no encuentra una dirección
