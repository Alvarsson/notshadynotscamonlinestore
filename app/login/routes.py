from flask import render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, current_user
from app.login import login_bp as bp
from app.login.user import User
from app.login.forms import LoginForm

@bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.get_user(username=login_form.username.data)
        if not user or not user.check_password(login_form.password.data):
            flash("User does not exist or password is wrong.")
            return redirect(url_for("login.login"))
        login_user(user)
        return redirect("login")
    return render_template("login.html", form=login_form)

@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))
