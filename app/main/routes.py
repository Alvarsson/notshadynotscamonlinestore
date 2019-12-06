from flask import render_template,url_for
from app.main import main_bp as bp
from app import db


 #Static test input
artiklar = [["Tall",3,239],["Ek",13,2329],["Lönn",31,2139]]
artiklar = [["edward",'Username:'],["albin", 'First name:'], ["axel", 'Sur name:'], ["blabla", 'Email:'], ["hejhej", 'Adress:']]
testy = ['Username', 'First name', 'Sur name', 'Email', 'Adress', 'Password']
#kategorier = ["Barrträd", "Lövträd", "Små träd","Stora träd","Gamer-träd","Wannabee-träd","Träd från kända serier"]


@bp.route("/")
def home():
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM categories ORDER BY category_name")

    categories = []
    for i in cur.fetchall():
        category = (int(i[0]),i[1])
        categories.append(category)
    print(categories)
    return render_template("index.html", ArrayMedTräd = categories)


@bp.route("/category/<int:category_id>")
def category(category_id):
    cur = db.connection.cursor()
    cur.execute("SELECT article_number,picture_url,article_name,price,category_name FROM articles INNER JOIN categories ON articles.category=categories.category_id WHERE categories.category_id=" + str(category_id)) # Can't wait for that sweet, sweet SQL Injection right here.
    
    result = list()
    images = list()

    for i in cur.fetchall():
        
        #i[1]=url_for('static', filename='img/user.svg')  if i[1] == '' else i[1]
        result.append(i)
    

    return render_template("kategori.html", artiklar = result,title=result[0][4],images = images)


@bp.route("/article/<int:article_number>")
def article(article_number):
    cur = db.connection.cursor()
    cur.execute("SELECT article_number,picture_url,article_name,price FROM articles WHERE article_number = " + str(article_number)) # Can't wait for that sweet, sweet SQL Injection right here.

    result = cur.fetchone()

    return render_template("article.html", artiklar = result,picture=result[1])


@bp.route("/user")
def user():
    #Få in inlogginformation om användare här!
    cur = db.connection.cursor()
    cur.execute("SELECT user_name, first_name, last_name, mail, adress FROM users WHERE customer_id="+ str(2))
    userResult = []
    for i in cur.fetchall():
        userResult.append(i)
    

    return render_template("user.html", testy = testy, userResult = userResult)

@bp.route("/user/cart")
def cart():
    
    return render_template("user.html", artiklar = artiklar)



