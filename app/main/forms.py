from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired



class AddToCartForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField("Add to cart")
    
class CartForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField("Change")
    
    def __init__(self,quantity):
        super(CartForm, self).__init__() 
        self.quantity.data = quantity



    