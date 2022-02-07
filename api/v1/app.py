#!/usr/bin/python3
"""[summary]
"""
from os import getenv
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def page_not_found(e):
    """Handler for 404 errors that returns a JSON-formatted
       404 status code response
    """
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown(self):
    """Method that calls storage.close()"""
    storage.close()


if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')
    if HBNB_API_HOST is None:
        HBNB_API_HOST = '0.0.0.0'
    if HBNB_API_PORT is None:
        HBNB_API_PORT = '5000'
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, debug=True, threaded=True)
