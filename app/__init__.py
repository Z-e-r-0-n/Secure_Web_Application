from flask import Flask
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Secret key for sessions
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev_secret")

# DB connection
db = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", "root"),
    database=os.getenv("DB_NAME", "secure_issue_tracker")
)

from app import routes
