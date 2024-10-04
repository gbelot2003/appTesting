# app/extractors/address_extractor.py

import re
import logging

class DireccionExtractor:
    def __init__(self):
        # Definir patrones para direcciones comunes
        self.patrones_direccion = [
            r"mi dirección es\s+([\w\s\d,]+)",  # "Mi dirección es 1234 Calle Principal, Ciudad"
            r"la dirección es\s+([\w\s\d,]+)",  # "La dirección es 1234 Calle Principal, Ciudad"
            r"vivo en\s+([\w\s\d,]+)",  # "Vivo en 1234 Calle Principal, Ciudad"
            r"resido en\s+([\w\s\d,]+)",  # "Resido en 1234 Calle Principal, Ciudad"
            r"puedes encontrarme en\s+([\w\s\d,]+)",  # "Puedes encontrarme en 1234 Calle Principal, Ciudad"
            r"me encuentro en\s+([\w\s\d,]+)",  # "Me encuentro en 1234 Calle Principal, Ciudad"
            r"la ubicación es\s+([\w\s\d,]+)",  # "La ubicación es 1234 Calle Principal, Ciudad"
            r"mi ubicación es\s+([\w\s\d,]+)",  # "Mi ubicación es 1234 Calle Principal, Ciudad"
            r"mi dirección actual es\s+([\w\s\d,]+)",  # "Mi dirección actual es 1234 Calle Principal, Ciudad"
            r"mi nueva dirección es\s+([\w\s\d,]+)",  # "Mi nueva dirección es 1234 Calle Principal, Ciudad"
            r"actualiza mi dirección a\s+([\w\s\d,]+)",  # "Actualiza mi dirección a 1234 Calle Principal, Ciudad"
            r"cambia mi dirección a\s+([\w\s\d,]+)",  # "Cambia mi dirección a 1234 Calle Principal, Ciudad"
            r"la dirección actual es\s+([\w\s\d,]+)",  # "La dirección actual es 1234 Calle Principal, Ciudad"
        ]

    def extraer_direccion(self, texto):
        texto = texto.lower()  # Convertir el texto a minúsculas para coincidencias insensibles a mayúsculas/minúsculas
        for patron in self.patrones_direccion:
            resultado = re.findall(patron, texto)
            if resultado:
                logging.debug(f"Dirección encontrada con el patrón: {patron}")
                return resultado[0].strip().capitalize()  # Capitaliza y limpia la dirección encontrada
        return None  # Retorna None si no encuentra una dirección
