from flask import Flask
from app.routes import Router
from flask_cors import CORS


def create_app():
	app = Flask(__name__.split('.')[0])

	CORS(app)
	Router(app)

	return app
