from flask import Flask, render_template
import test.py

app = Flask(__name__)

kategorier = ["Barrträd", "Lövträd", "Små träd","Stora träd","Gamer-träd","Wannabee-träd","Träd från kända serier"]

@app.route("/test")
def testsite():
    return render_template("index.html", ArrayMedTräd = kategorier)
    
@app.route("/")
def home():
    return render_template("index.html", ArrayMedTräd = kategorier)


@app.route("/login")
def login():
    return render_template("login.html")

artiklar = [["Tall",3,239],["Ek",13,2329],["Lönn",31,2139]]
@app.route("/admin")
def kategori():

    return render_template("adminview.html", artiklar = artiklar)

artiklar = ["edward", "albin", "axel", "blabla", "hejhej"]
@app.route("/kategori")
def kategori():
    return render_template("kategori.html", artiklar = artiklar)

@app.route("/article")
def article():
    return render_template("article.html", artiklar = artiklar)

@app.route("/user")
def user():
    return render_template("user.html", artiklar = artiklar)

if __name__ == "__main__":
    app.run(debug=True)


