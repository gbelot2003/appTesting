from app.repos.contact_repo import ContactRepo
from app.extractors.address_extractor import DireccionExtractor

class UpdateAddressAction:
    def __init__(self, telefono, texto):
        self.telefono = telefono
        self.texto = texto

    def ejecutar(self):
        # Extraer la dirección del texto utilizando el extractor de direcciones
        direccion_extractor = DireccionExtractor()
        nueva_direccion = direccion_extractor.extraer_direccion(self.texto)

        if not nueva_direccion:
            return {"status": "error", "message": "No se pudo extraer una dirección válida del texto proporcionado."}

        # Buscar el contacto por teléfono
        contacto = ContactRepo.obtener_contacto_por_telefono(self.telefono)
        if not contacto:
            return {"status": "error", "message": f"No se encontró el contacto con el teléfono {self.telefono}"}
        
        # Actualizar la dirección del contacto
        contacto.direccion = nueva_direccion
        ContactRepo.actualizar_contacto(contacto.id, direccion=nueva_direccion)
        
        return {"status": "success", "message": f"Dirección actualizada a: {nueva_direccion}"}