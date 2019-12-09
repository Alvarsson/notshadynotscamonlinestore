from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired



class AddToCartForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField("Add to cart")
    
    def __init__(self):
        super(AddToCartForm, self).__init__() 
        self.quantity.data = 1

