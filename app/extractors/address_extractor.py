# File path: app/extractors/address_extractor.py

import re
import logging

class DireccionExtractor:
    def __init__(self):
        # Modificar los patrones para capturar direcciones completas con componentes opcionales como estado y país
        self.patrones_direccion = [
            # Patrón extendido para capturar dirección completa con ciudad, estado y país opcionales
            r"(\d+\s[\w\s]+,\s*[\w\s]+(?:,\s*[\w\s]+){0,3})",  # 14350 Culebra Rd, San Antonio, TX 78253, United States
            # Patrón para capturar dirección con número de calle y nombre de calle
            r"(\d+\s[\w\s]+,\s*[\w\s]+)",  # 1234 Calle Principal, Springfield
            # Patrón para capturar dirección con número de calle solamente
            r"(\d+\s[\w\s]+)"  # 1234 Calle Principal
        ]

    def extraer_direccion(self, texto):
        """
        Extrae la primera dirección que coincida en el texto dado.
        Retorna None si no encuentra una dirección válida.
        """
        texto = texto.lower()  # Convertir a minúsculas para coincidencias insensibles a mayúsculas/minúsculas
        for patron in self.patrones_direccion:
            resultado = re.findall(patron, texto)
            if resultado:
                logging.debug(f"Dirección encontrada con el patrón: {patron}")
                return resultado[0].strip().capitalize()  # Limpiar y capitalizar la dirección encontrada
        return None

    def extraer_todas_las_direcciones(self, texto):
        """
        Extrae todas las direcciones que coincidan en el texto dado.
        Retorna una lista de direcciones o una lista vacía si no encuentra ninguna.
        """
        texto = texto.lower()  # Convertir a minúsculas para coincidencias insensibles a mayúsculas/minúsculas
        direcciones = []
        for patron in self.patrones_direccion:
            resultado = re.findall(patron, texto)
            if resultado:
                logging.debug(f"Direcciones encontradas con el patrón: {patron}: {resultado}")
                direcciones.extend([direccion.strip().capitalize() for direccion in resultado])
        return direcciones if direcciones else []
