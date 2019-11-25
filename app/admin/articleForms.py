from flask_wtf import FlaskForm
from wtforms import StringField, SelectField,PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class AddArticleForm(FlaskForm):
    name = StringField('Article name', validators=[DataRequired()])
    category = SelectField('Category ID', validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    url = StringField('URL')
    description = StringField('Description')
    submitAddArticle = SubmitField("Add Article")
    