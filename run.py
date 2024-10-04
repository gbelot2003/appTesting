from app import FlaskApp
from extensions import db

flask_app = FlaskApp()
app = flask_app.get_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)