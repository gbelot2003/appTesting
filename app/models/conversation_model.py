# src/models/conversacion_model.py
from extensions import db

class Conversation(db.Model):
    __tablename__ = 'conversations'

    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.String(50), nullable=False)  # Identificador único del usuario o sesión
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())