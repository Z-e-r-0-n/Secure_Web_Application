# app/__init__.py
from flask import Flask
from dotenv import load_dotenv
import os, pymysql

load_dotenv()

def get_conn():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),  # keep this name since you used it
        database=os.getenv("DB_NAME", "secure_issue_tracker"),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev_secret")
    app.config["DB_CONN_FACTORY"] = get_conn

    # import and register blueprint after app is created
    from .routes import main
    app.register_blueprint(main)

    return app
