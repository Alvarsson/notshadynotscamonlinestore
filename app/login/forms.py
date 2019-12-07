from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from app.login.user import User
from flask_login import current_user

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    mail = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Register')


    def validate_username(self, username):
        user = User.get_user(username=username.data)
        if user is not None:
            raise ValidationError('Username already taken')

    def validate_mail(self, mail):
        if User.get_user(mail=mail.data) is not None:
            raise ValidationError('E-mail already taken')

class EditUserForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    mail = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[])
    submit = SubmitField('Submit')

    def validate_mail(self, mail):
        if User.get_user(mail=mail.data) is not None and mail.data != current_user.mail:
            raise ValidationError('E-mail already taken')


