# File path: tests/test_address_extractor.py

import pytest
from app.extractors.address_extractor import DireccionExtractor

def test_direccion_extractor():
    extractor = DireccionExtractor()

    # Probar varios ejemplos de direcciones con más detalles
    ejemplos = [
        ("Mi dirección es 1234 Calle Principal, Springfield", "1234 calle principal, springfield"),
        ("Vivo en 5678 Calle Secundaria, Ciudad", "5678 calle secundaria, ciudad"),
        ("Resido en 91011 Avenida Tercera, Estado", "91011 avenida tercera, estado"),
        ("Puedes encontrarme en 1213 Calle Cuarta, San Antonio, Texas, Estados Unidos", "1213 calle cuarta, san antonio, texas, estados unidos"),
    ]

    for texto, direccion_esperada in ejemplos:
        direccion_extraida = extractor.extraer_direccion(texto)
        assert direccion_extraida.lower() == direccion_esperada  # Comparar en minúsculas
