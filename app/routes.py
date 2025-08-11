from flask import render_template, request, redirect, url_for, session
from app import app
import app.models as models

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    # TODO: Handle login form
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    # TODO: Handle registration form
    return render_template("register.html")

@app.route("/profile")
def profile():
    # TODO: Show user profile
    return render_template("profile.html")

@app.route("/forum")
def forum():
    # TODO: Show forum posts
    return render_template("forum.html")

@app.route("/issues")
def issues():
    # TODO: Show all issues
    return render_template("issues.html")

@app.route("/logout")
def logout():
    # TODO: Clear session
    return redirect(url_for("home"))
