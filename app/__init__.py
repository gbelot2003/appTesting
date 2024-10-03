from flask import Flask

from app.routes import routes

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    app.register_blueprint(routes.bp)

    return app