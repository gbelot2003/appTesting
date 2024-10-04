# File path: app/services/action_handler_service.py

from app.actions.conversation_history_action import ConversationHistoryAction
from app.actions.name_action import NameAction
from app.actions.address_action import AddressAction
from app.actions.verify_contact_action import VerifyContactAction
import logging

class ActionHandleService:
    def __init__(self, user_id, prompt):
        self.user_id = user_id
        self.prompt = prompt
        self.messages = []

    def handle_actions(self):
        logging.info("Iniciando handle_actions con prompt: %s", self.prompt)

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

        # Verificar si el usuario desea actualizar explícitamente su dirección
        if "actualizar dirección" in self.prompt.lower() or "quiero actualizar mi dirección" in self.prompt.lower():
            logging.info("Se detectó una solicitud explícita de actualización de dirección.")
            address_action = AddressAction(contacto, self.prompt)
            address_message = address_action.process_address()
            if address_message:
                self.messages.append(address_message)
        else:
            # Manejar la dirección normalmente
            address_action = AddressAction(contacto, self.prompt)
            address_message = address_action.process_address()
            if address_message:
                self.messages.append(address_message)

        return self.messages
