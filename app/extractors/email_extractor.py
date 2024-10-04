# File path: app/extractors/email_extractor.py

import re
import logging

class EmailExtractor:
    def __init__(self):
        # Patrón básico para capturar direcciones de correo electrónico
        self.patron_email = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    def extraer_email(self, texto):
        """
        Extrae el primer correo electrónico que coincide en el texto dado.
        Retorna None si no encuentra un correo válido.
        """
        texto = texto.lower()  # Convertir a minúsculas para coincidencias insensibles a mayúsculas/minúsculas
        resultado = re.findall(self.patron_email, texto)
        if resultado:
            logging.debug(f"Correo encontrado: {resultado[0]}")
            return resultado[0]  # Retornar el primer correo encontrado
        return None  # Retorna None si no encuentra un correo
