import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class OpenAIService:

    def __init__(self):
        pass

    def handle_request(self, prompt):
        print(f"Usuario: {prompt}")

        try:
            # Definir el prompt del usuario
            messages = []

            # Agregar el mensaje actual del usuario
            messages.append({"role": "user", "content": prompt})
            
            # Enviar los mensajes a la API de OpenAI
            response = client.chat.completions.create(
                model="gpt-3.5-turbo", messages=messages, max_tokens=100, temperature=0.2
            )

            # Obtener la respuesta generada por el modelo
            respuesta_modelo = response.choices[0].message.content.strip()

            # Imprimir la respuesta generada por el modelo
            print(f"GPT: {respuesta_modelo}")

            return {"status": "success", "response": respuesta_modelo}
        except Exception as e:
            return {"status": "error", "response": str(e)}