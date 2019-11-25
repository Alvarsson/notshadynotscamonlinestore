from flask import render_template,url_for
from app.main import main_bp as bp
from app import db


 #Static test input
artiklar = [["Tall",3,239],["Ek",13,2329],["Lönn",31,2139]]
artiklar = [["edward",'Username:'],["albin", 'First name:'], ["axel", 'Sur name:'], ["blabla", 'Email:'], ["hejhej", 'Adress:']]
testy = ['Username', 'First name', 'Sur name', 'Email', 'Adress', 'Password']
#kategorier = ["Barrträd", "Lövträd", "Små träd","Stora träd","Gamer-träd","Wannabee-träd","Träd från kända serier"]

@bp.route("/test")
def testsite():

    return render_template("article.html", artiklar = artiklar)


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
    #cur.execute("SELECT * FROM articles WHERE category = " + str(category_id))
    cur.execute("SELECT * FROM articles INNER JOIN categories ON articles.category=categories.category_id WHERE categories.category_id=" + str(category_id)) # Can't wait for that sweet, sweet SQL Injection right here.
    result = list()
    for i in cur.fetchall():
        result.append(i)

    #print(result)

    return render_template("kategori.html", artiklar = result,title=result[0][7])


@bp.route("/article/<int:article_number>")
def article(article_number):
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM articles WHERE article_number = " + str(article_number)) # Can't wait for that sweet, sweet SQL Injection right here.

    return render_template("article.html", artiklar = [i[5] for i in cur.fetchall()])


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



