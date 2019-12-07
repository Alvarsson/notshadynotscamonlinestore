from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from app.login.user import User

class EditUserForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    mail = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[])
    submit = SubmitField('Register')

    def validate_mail(self, mail):
        if User.get_user(mail=mail.data) is not None:
            raise ValidationError('E-mail already taken')

