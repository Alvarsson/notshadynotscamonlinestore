from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class AddArticleForm(FlaskForm):

    #hoicess = [(34, '1'), (31, '22'), (1, 'Barrträd'), (24, 'Eduardo'), (5, 'Gamer-träd'), (2, 'Lövträd'), (33, 'NUDÅ!?'), (3, 'Små träd'), (4, 'Stora träd'), (7, 'Träd från kända serier'), (6, 'Wannabee-träd'), (39, 'aa'), (44, 'aaa232'),
                #(32, 'aaaa'), (38, 'aaaaaaaaaaaaaaaaa'), (27, 'aaakkkiiariir'), (28, 'ddd'), (18, 'hejsan'), (30, 'kkakaaka'), (46, 'naaaa'), (48, 'nu då!?'), (41, 'okidoke'), (42, 'okieo'), (49, 'rrrr'), (47, 's'), (19, 'tjosan'), (29, 'tysk')]

    name = StringField('Article name', validators=[DataRequired()])
    category = SelectField('Category ID', validators=[DataRequired()], coerce=int)
    stock = IntegerField('Stock', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    url = StringField('URL')
    description = StringField('Description')
    submitAddArticle = SubmitField("Add Article")

