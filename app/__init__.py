from flask import Flask
from app.routes.routes import bp  # Asegúrate de que 'bp' esté importado correctamente

class FlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config.from_object('config')

        self.register_blueprints()

    def register_blueprints(self):
        self.app.register_blueprint(bp)

    def get_app(self):
        return self.app