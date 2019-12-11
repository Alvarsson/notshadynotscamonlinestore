from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField, IntegerField, TextAreaField
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

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField("Submit comment/rating")
    rating = SelectField('Rating:', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),('5', '5')])

class PurchaseCartForm(FlaskForm):
    submit = SubmitField("Commit and Order")





    