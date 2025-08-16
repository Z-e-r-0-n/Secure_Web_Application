# app/routes.py
from flask import Blueprint, render_template, session, redirect, url_for, request
import hashlib
from app import models as model  # adjust import path if needed

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("home.html")

@main.route("/login", methods=["GET","POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username","").strip()
        password = request.form.get("password","")
        pw_hash  = hashlib.sha256(password.encode()).hexdigest()
        if model.check_login(username, pw_hash):
            model.cursor.execute("SELECT user_id FROM users WHERE username=%s LIMIT 1", (username,))
            row = model.cursor.fetchone()
            if row:
                session["user_id"] = row[0]   
                return redirect(url_for("main.home"))
            error = "Login succeeded but user_id not found."
        else:
            error = "Invalid username or password."
    return render_template("login.html", error=error)

@main.route("/register", methods=["GET","POST"])
def register():
    error = None
    if request.method == "POST":
        username   = request.form.get("username","").strip()
        email      = request.form.get("email","").strip()
        first_name = request.form.get("first_name","").strip()
        last_name  = request.form.get("last_name","").strip()
        password   = request.form.get("password","")
        if len(password) < 8 or not any(c.isdigit() for c in password):
            error = "Password must be at least 8 characters and include a number."
        else:
            pw_hash = hashlib.sha256(password.encode()).hexdigest()
            try:
                model.create_user(username, pw_hash, email, first_name, last_name)
                return redirect(url_for("main.login"))
            except Exception:
                error = "Registration failed."
    return render_template("register.html", error=error)

@main.route("/forum")
def forum():
    return render_template("forum.html")

@main.route("/issues")
def issues():
    if not session.get("user_id"):
        return redirect(url_for("main.login"))
    issues=model.get_issues(session.get("user_id"))
    if not issues:
        return render_template("issues.html", error="No issues found.")
    return render_template("issues.html",issues=issues)

@main.route("/logout", methods=["POST","GET"])
def logout():
    session.clear()
    return redirect(url_for("main.home"))

@main.route("/profile")
def profile():
    profile=model.get_profile(session.get("user_id"))
    return render_template("profile.html",username=profile[0], email=profile[1],name=profile[2]+profile[3])

@main.route("/home")
def home_alias():
    return render_template("home.html")

@main.route("/messages")
def messages():
    if not session.get("user_id"):
        return redirect(url_for("main.login"))
    messages = model.get_messages(session.get("user_id"),"fixthis")
    if not messages:
        return render_template("message.html", error="No messages found.")
    user=session.get("user_id")
    return render_template("message.html", messages=messages,user=user)

@main.route("/friends")
def friends():
    if not session.get("user_id"):
        return redirect(url_for("main.login"))
    return redirect(url_for("main.friends"))
    

