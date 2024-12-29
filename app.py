from flask import Flask
from db.database import create_table_if_not_exists
from routes.transcript_routes import transcript_blueprint

def create_app():
    app = Flask(__name__)

    # Initialize DB if needed
    create_table_if_not_exists()

    # Register Blueprints
    app.register_blueprint(transcript_blueprint, url_prefix="/")

    return app

if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run(host='0.0.0.0', port=5000, debug=True)
