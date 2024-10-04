# File path: tests/test_address_extractor.py

import pytest
from app.extractors.address_extractor import DireccionExtractor

def test_direccion_extractor():
    extractor = DireccionExtractor()

    # Probar varios ejemplos de direcciones con y sin etiquetas
    ejemplos = [
        ("Mi dirección es 1234 Calle Principal, Springfield", "1234 calle principal, springfield"),
        ("Vivo en 5678 Calle Secundaria, Ciudad", "5678 calle secundaria, ciudad"),
        ("Resido en 91011 Avenida Tercera, Estado", "91011 avenida tercera, estado"),
        ("Puedes encontrarme en 1213 Calle Cuarta, San Antonio, Texas, Estados Unidos", "1213 calle cuarta, san antonio, texas, estados unidos"),
        ("14350 Culebra Rd, San Antonio, TX 78253, United States", "14350 culebra rd, san antonio, tx 78253, united states"),  # Caso sin etiqueta
        ("Ubicación: 1600 Pennsylvania Ave NW, Washington, DC 20500, United States", "1600 pennsylvania ave nw, washington, dc 20500, united states"),  # Caso con ubicación
        ("1234 Calle Principal", "1234 calle principal"),  # Dirección simple
        ("No contiene dirección", None),  # Caso donde no hay dirección
    ]

    for texto, direccion_esperada in ejemplos:
        direccion_extraida = extractor.extraer_direccion(texto)
        # Comparar en minúsculas para asegurar igualdad y evitar problemas de capitalización
        assert (direccion_extraida.lower() if direccion_extraida else direccion_extraida) == (direccion_esperada.lower() if direccion_esperada else direccion_esperada)
