from flask import Blueprint, jsonify, request
from app.services.openai_service import OpenAIService

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return jsonify({"message": "Hello, World!"})

@bp.route('/api/message', methods=['POST'])
def simulate_twilio():
    data = request.json
    message_body = data.get('message', 'Este es un mensaje simulado desde Twilio')

    response = OpenAIService().handle_request(message_body)

    return jsonify(response)