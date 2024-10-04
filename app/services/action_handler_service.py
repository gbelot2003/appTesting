# app/services/action_handler_service.py

from app.actions.conversation_history_action import ConversationHistoryAction
from app.actions.name_action import NameAction
from app.actions.update_address_action import UpdateAddressAction
from app.actions.verify_contact_action import VerifyContactAction

class ActionHandleService:
    def __init__(self, user_id, prompt):
        self.user_id = user_id
        self.prompt = prompt
        self.messages = []

    def handle_intent(self, intent, entities):
        if intent == "actualizar_direccion":
            # Obtener el número de teléfono y la nueva dirección de las entidades
            telefono = entities.get("telefono")
            nueva_direccion = entities.get("direccion")
            
            # Ejecutar la acción de actualización de dirección
            action = UpdateAddressAction(telefono, nueva_direccion)
            resultado = action.ejecutar()
            
            return resultado

    def handle_actions(self):
        # Verificar si el usuario tiene un número de teléfono en la base de datos
        contacto = VerifyContactAction().verificar_contacto(self.user_id)

        # Procesar el nombre del contacto
        name_action = NameAction(contacto, self.prompt)
        name_message = name_action.process_name()
        if name_message:
            self.messages.append(name_message)

         # Buscar historial de conversación
        conversation_history_action = ConversationHistoryAction()
        chat_history_messages = conversation_history_action.compilar_conversacion(self.user_id)
        self.messages.extend(chat_history_messages)

        # Llamar al manejador de intentos con el intent `actualizar_direccion`
        self.handle_intent("actualizar_direccion", {"telefono": self.user_id, "direccion": self.prompt})

    
        return self.messages