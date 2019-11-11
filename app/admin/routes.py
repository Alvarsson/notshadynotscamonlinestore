from flask import render_template
from app.admin import admin_bp as bp

@bp.route("/admin")
def admin():
    return render_template("adminview.html", artiklar = artiklar)
