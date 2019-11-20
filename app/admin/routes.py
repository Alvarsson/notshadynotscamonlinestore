from flask import render_template, redirect, url_for, request
from app.admin import admin_bp as bp
from app import db
#categoryArray = [("edward",'1'),("albin",'2')]

artiklar = ["edward", "albin", "axel", "blabla", "hejhej"]

@bp.route("/admin")
def admin():
    return render_template("admin/overview.html", artiklar = artiklar)

@bp.route("/admin/articles")
def adminArticles():
    return render_template("admin/articles.html", artiklar = artiklar)

@bp.route("/admin/categories", methods=['POST', 'GET'])
def adminCategories():
    
    cur = db.connection.cursor()
    cur.execute('''SELECT category_name, unique_id FROM categories''')
    categoryArray = []
    for i in cur.fetchall():
        categoryArray.append(i)
    
    if request.method == 'POST':
        print("hejhå")
        if request.form['submit'] == 'addCategory':

            #cur = db.connection.cursor()
            newCategory = request.form['categoryfield']
            newCategory = "('" + str(newCategory) + "')"
            print(newCategory)
            #addCatCur = db.connection.cursor()
            cur.execute('''INSERT INTO categories (category_name) VALUES'''+ newCategory + ";")
            db.connection.commit()
            cur.close()
            return redirect(url_for('admin.adminCategories'))
    return render_template("admin/categories.html", categories = categoryArray)

@bp.route("/admin/users")
def adminUsers():
    return render_template("admin/articles.html", artiklar = artiklar)

