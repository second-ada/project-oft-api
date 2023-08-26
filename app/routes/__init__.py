from flask import Flask
from app.routes import api


class Router:

    def __init__(self, app: Flask):
        app.register_blueprint(api.bp)
