# File path: tests/test_email_extractor.py

import pytest
from app.extractors.email_extractor import EmailExtractor

def test_email_extractor():
    extractor = EmailExtractor()

    # Probar varios ejemplos de correos electrónicos
    ejemplos = [
        ("Mi correo es usuario@example.com", "usuario@example.com"),
        ("Puedes contactarme en otro.email@sub.dominio.org", "otro.email@sub.dominio.org"),
        ("Escribeme a: nombre.apellido@empresa.co", "nombre.apellido@empresa.co"),
        ("Mi nuevo email es user123@mail-server.net", "user123@mail-server.net"),
        ("Contacta a soporte en support+filter@company.com", "support+filter@company.com"),
        ("gerardo@dominio.com", "gerardo@dominio.com"),
        ("No hay correo aquí", None),  # Caso donde no hay correo electrónico
    ]

    for texto, email_esperado in ejemplos:
        email_extraido = extractor.extraer_email(texto)
        assert email_extraido == email_esperado  # Comparar el correo extraído con el esperado
