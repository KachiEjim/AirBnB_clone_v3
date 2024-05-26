#!/usr/bin/python3
"""File doc"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS  # to enable CORS
import os


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})  # Create a CORS instance


app.register_blueprint(app_views)


@app.errorhandler(404)
def page_not_found(error):
    """Handles error 404 file not found"""

    return jsonify({'error': 'Not found'}), 404


@app.teardown_appcontext
def teardown_db(exception):
    """
    A method to handle @app.teardown_appcontext
    that calls storage.close()
    """
    storage.close()


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
