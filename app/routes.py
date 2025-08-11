# app/routes.py
from flask import Blueprint, render_template, session, redirect, url_for

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("home.html")

@main.route("/login", methods=["GET","POST"])
def login():
    return render_template("login.html")

@main.route("/register", methods=["GET","POST"])
def register():
    return render_template("register.html")

@main.route("/forum")
def forum():
    return render_template("forum.html")

@main.route("/issues")
def issues():
    if not session.get("user_id"):
        return redirect(url_for("main.login"))
    return render_template("issues.html")

@main.route("/logout", methods=["POST","GET"])
def logout():
    session.clear()
    return redirect(url_for("main.home"))
