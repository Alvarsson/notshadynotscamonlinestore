from flask import render_template
from app.main import main_bp as bp
from app import db


 #Static test input
artiklar = [["Tall",3,239],["Ek",13,2329],["Lönn",31,2139]]
artiklar = ["edward", "albin", "axel", "blabla", "hejhej"]
#kategorier = ["Barrträd", "Lövträd", "Små träd","Stora träd","Gamer-träd","Wannabee-träd","Träd från kända serier"]


@bp.route("/test")
def testsite():

    return render_template("article.html", artiklar = artiklar)


@bp.route("/")
def home():
    cur = db.connection.cursor()
    cur.execute('''SELECT category_name FROM categories''')
    treeArray = []
    for i in cur.fetchall():
        treeArray.append(i[0])
    return render_template("index.html", ArrayMedTräd = treeArray)


@bp.route("/login")
def login():
    return render_template("login.html")


@bp.route("/admin")
def admin():
    return render_template("adminview.html", artiklar = artiklar)


@bp.route("/kategori")
def kategori():
    return render_template("kategori.html", artiklar = artiklar)


@bp.route("/article")
def article():
    return render_template("article.html", artiklar = artiklar)


@bp.route("/user")
def user():
    return render_template("user.html", artiklar = artiklar)



