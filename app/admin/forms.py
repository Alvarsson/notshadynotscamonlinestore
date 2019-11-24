from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class AddCategoryForm(FlaskForm):
    name = StringField('Category name', validators=[DataRequired()])
    submit = SubmitField("Add")

class RemoveCategoryForm(FlaskForm):
    category_id = IntegerField('Category ID', validators=[DataRequired()])
    submit = SubmitField("Remove")

class EditCategoryForm(FlaskForm):
    name = StringField('Email', validators=[DataRequired()])
    category_id = IntegerField('Category ID', validators=[DataRequired()])
    submit = SubmitField("Edit")