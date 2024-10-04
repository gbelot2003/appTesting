# File path: app/__init__.py

from flask import Flask
from extensions import db

def create_app():
    app = Flask(__name__)
    
    # Configuración de la aplicación
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True
    
    # Inicializar extensiones
    db.init_app(app)
    
    # Importar vistas y modelos
    with app.app_context():
        #import app.views
        import app.models
        db.create_all()  # Crear las tablas necesarias
    
    return app
