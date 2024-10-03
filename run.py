from app import FlaskApp

flask_app = FlaskApp()
app = flask_app.get_app()

if __name__ == '__main__':
    app.run(debug=True)