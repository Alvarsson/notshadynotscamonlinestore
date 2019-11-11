from flask import render_template
from app.login import login_bp as bp

@bp.route("/login")
def login():
    return render_template("login.html")

