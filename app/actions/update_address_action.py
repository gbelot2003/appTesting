# app/actions/update_address_action.py
from app.extractors.address_extractor import DireccionExtractor
from app.repos.contact_repo import ContactRepo

class UpdateAddressAction:
    def __init__(self, telefono, texto):
        self.telefono = telefono
        self.texto = texto

    def ejecutar(self):
        # Extraer la dirección del texto utilizando el extractor de direcciones
        direccion_extractor = DireccionExtractor()
        nueva_direccion = direccion_extractor.extraer_direccion(self.texto)
        print(nueva_direccion)

        if not nueva_direccion:
            return {"status": "error", "message": "No se pudo extraer una dirección válida del texto proporcionado."}

        # Buscar el contacto por teléfono
        # Revisa este bloque de código en `UpdateAddressAction`
        contacto = ContactRepo.obtener_contacto_por_telefono(self.telefono)
        if not contacto:
            return {"status": "error", "message": f"No se encontró el contacto con el teléfono {self.telefono}"}

        
        # Actualizar la dirección del contacto
        contacto.direccion = nueva_direccion
        ContactRepo.actualizar_contacto(contacto.id, direccion=nueva_direccion)
        
        return {"status": "success", "message": f"Dirección actualizada a: {nueva_direccion}"}
