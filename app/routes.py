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



@main.route("/issues")
def issues():
    if not session.get("user_id"):
        return redirect(url_for("main.login"))
    user_id = session.get("user_id")
    tag = request.args.get("tag")
    tags = model.get_tags_for_user(user_id)
    if tag:
        issues = model.get_issues_by_tag_for_user(user_id, tag)
    else:
        issues = model.get_issues(user_id)
    if not issues:
        return render_template("issues.html", error="No issues found.", tags=tags)
    return render_template("issues.html", issues=issues, tags=tags, selected_tag=tag)

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

@main.route("/issue/<int:issue_id>")
def issue_detail(issue_id):
    issue = model.get_issue_by_id(issue_id)
    comments = model.get_comments(issue_id)
    viewer_id = session.get("user_id")
    is_owner = bool(issue and viewer_id == issue[4])
    return render_template("issue_detail.html", issue=issue, comments=comments,is_owner=is_owner)

ALLOWED_TAGS = ["bug", "feature", "ui", "backend", "security", "docs", "helpwanted"]# needs extending do when sai is fine i guess
MAX_TAGS = 3

@main.route("/post", methods=["GET", "POST"])
def post_issue():
    if not session.get("user_id"):
        return redirect(url_for("main.login"))

    if request.method == "POST":
        user_id = session["user_id"]
        title   = request.form["title"].strip()
        content = request.form["content"].strip()
        selected = request.form.getlist("tags")

        # cap set to 3 for now change if you want bot
        tags = []
        for t in selected:
            t_norm = t.strip().lower()
            if t_norm in ALLOWED_TAGS and t_norm not in tags:
                tags.append(t_norm)
            if len(tags) == MAX_TAGS:
                break

        model.create_issue(user_id, title, content, tags)
        return redirect(url_for("main.issues"))

    return render_template("post.html", allowed_tags=ALLOWED_TAGS, max_tags=MAX_TAGS)

@main.route("/forum")
def forum():
    if not session.get("user_id"):
        return redirect(url_for("main.login"))
    q   = (request.args.get("q") or "").strip()
    tag = request.args.get("tag")

    tags = model.get_all_tags_global()#add a list here fine for now i guess

    if q:
        issues = model.search_recent_issues_global(q, limit=10)
    elif tag:
        issues = model.idkwhattoname(tag, 10)  # returns (issue_id, title, content, created_at)
    else:
        issues = model.get_global_issues(limit=10)

    if not issues:
        return render_template("issues.html",
                               error="No issues yet.",
                               tags=tags,
                               selected_tag=tag,
                               mode="forum",
                               q=q)

    return render_template("issues.html",
                           issues=issues,
                           tags=tags,
                           selected_tag=tag,
                           mode="forum",
                           q=q)

@main.route("/issue/<int:issue_id>/comment", methods=["POST"])
def add_comment_route(issue_id):
    if not session.get("user_id"):
        return redirect(url_for("main.login"))

    issue = model.get_issue_by_id(issue_id)
    if not issue:
        return redirect(url_for("main.forum")) 

    # double checking i  guess review karo
    if session["user_id"] == issue[4]:
        return redirect(url_for("main.issue_detail", issue_id=issue_id))

    content = (request.form.get("content") or "").strip()
    if content:
        model.add_comment(issue_id, session["user_id"], content)

    return redirect(url_for("main.issue_detail", issue_id=issue_id))
    
    

    

