from flask import render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, current_user
from app.login import login_bp as bp
from app.login.user import User
from app.login.forms import LoginForm, RegisterForm

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

@bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    username=form.username.data,
                    mail=form.mail.data,
                    address=form.address.data)
        user.set_password(form.password.data)
        user.commit()
        flash("Du är nu registrerad")
        return redirect(url_for('login.login'))
    return render_template('register.html', form=form)

