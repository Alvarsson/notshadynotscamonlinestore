from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired

from app import db

class ArticleForm(FlaskForm):
    name = StringField('Article name', validators=[DataRequired()])
    category = SelectField('Category ID', validators=[DataRequired()], coerce=int)
    stock = IntegerField('Stock', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    url = StringField('URL')
    description = StringField('Description')
    submitArticle = SubmitField("Add Article")

 
    def __init__(self,article_number=None):
        super(ArticleForm, self).__init__() 
        cur = db.connection.cursor()
        cur.execute("SELECT category_id,name FROM categories")
        categoryArray = []
        for cat in cur.fetchall():
            categoryArray.append(cat)

        self.category.choices = categoryArray

        if article_number != None and self.name.data == None: #för att stoppa att skriva över form input från user... 
            self.addPlaceholders(article_number)


    ########################################## EDWARD SAY ME, WHY NOT 2 CONSTRUCTORS I LOSE MIND #########################################
    #behöver nog inte ens vara static. eller? 
    #@staticmethod
    def addPlaceholders(self,article_number): #vi vill bara göra detta med ett artikel nummer så none behövs ej
        #print("om du kommit in i edit specific article delen, så påbörjar en annorlunda articleform")
        cur = db.connection.cursor()

        cur.execute("""SELECT article_id,stock,category_id,articles.name,price,url,text FROM articles
         left JOIN categories ON articles.category_id=categories.category_id 
         left join description on articles.article_id=description.description_id 
         where article_id=""" + str(article_number) + ";")
        
        query = cur.fetchone()
        db.connection.commit()
        cur.close()
        print(query)

        #editArticle=ArticleForm()

        self.name.data = query[3]
        self.category.data = query[2] 
        self.stock.data = query[1]
        self.price.data = query[4]
        self.url.data = query[5] if query[5] != None else ""
        self.description.data = query[6] if query[6] != None else ""

        #return editArticle


class RemoveArticleForm(FlaskForm):
    article = IntegerField('Article ID')
    submitRemoveArticle = SubmitField("Remove")


# class EditArticleForm(FlaskForm):
#     name = StringField('Article name', validators=[DataRequired()])
#     category = SelectField('Category ID', validators=[DataRequired()], coerce=int)
#     stock = IntegerField('Stock', validators=[DataRequired()])
#     price = IntegerField('Price', validators=[DataRequired()])
#     url = StringField('URL')
#     description = StringField('Description')
#     submitAddArticle = SubmitField("Add Article")



