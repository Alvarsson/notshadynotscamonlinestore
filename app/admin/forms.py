from flask_wtf import FlaskForm
from wtforms import StringField, SelectField,PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired

    
class AddCategoryForm(FlaskForm):
    name = StringField('Category name', validators=[DataRequired()])
    submitAdd = SubmitField("Add")

class RemoveCategoryForm(FlaskForm):
    category_id = IntegerField('Category ID', validators=[DataRequired()])
    submitRemove = SubmitField("Remove")

class EditCategoryForm(FlaskForm):
    new_name = StringField('Category name', validators=[DataRequired()])
    category_id = IntegerField('Category ID', validators=[DataRequired()])
    submitEdit = SubmitField("Edit")
    


