from flask import Flask
from config import Config
from extensions import db

class FlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config.from_object(Config)

        self.register_extensions()
        self.register_blueprints()

    def register_extensions(self):
        db.init_app(self.app)

    def register_blueprints(self):
        from app.routes.routes import bp  # Asegúrate de que 'bp' esté importado correctamente
        self.app.register_blueprint(bp)

    def get_app(self):
        return self.app