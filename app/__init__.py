# app/__init__.py
from flask import Flask
from dotenv import load_dotenv
import os, pymysql

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev_secret")
    # import and register blueprint after app is created
    from .routes import main
    app.register_blueprint(main)

    return app
