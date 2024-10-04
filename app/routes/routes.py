from flask import Blueprint, jsonify, request, render_template
from app.services.openai_service import OpenAIService

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template("index.html")
    
  

@bp.route('/api/message', methods=['POST'])
def simulate_twilio():
    data = request.json
    message_body = data.get('message', 'Este es un mensaje simulado desde Twilio')
    from_number = data.get('from_number', '+14155551234')

    response = OpenAIService().handle_request(message_body, from_number)

    return jsonify(response)