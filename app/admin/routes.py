from flask import render_template, redirect, url_for, request
from app.admin import admin_bp as bp
from app import db

artiklar = ["edward", "albin", "axel", "blabla", "hejhej"]

@bp.route("/admin")
def admin():
    return render_template("admin/overview.html", artiklar = artiklar)

@bp.route("/admin/articles")
def adminArticles():
    return render_template("admin/articles.html", artiklar = artiklar)

@bp.route("/admin/categories", methods=['POST', 'GET'])
def adminCategories():
    
    #Fetchar data från nuvarande kategoritabell och skriver ut på sidan
    cur = db.connection.cursor()
    cur.execute('''SELECT category_name, unique_id FROM categories''')
    categoryArray = []
    for i in cur.fetchall():
        categoryArray.append(i)
    
    #Skickar data mot tabell kategorier beroende på vilken submitknapp
    if request.method == 'POST':
        #Submit för att lägga till kategori
        if request.form['submit'] == 'addCategory':
            newCategory = request.form['categoryfield']
            newCategory = "('" + str(newCategory) + "')"
            cur.execute('''INSERT INTO categories (category_name) VALUES'''+ newCategory + ";")
            db.connection.commit()
            cur.close()
            return redirect(url_for('admin.adminCategories'))
        #Submit för att ta bort kategori
        elif request.form['submit'] == 'remove':
            deleteCat = request.form['removefield']
            cur.execute('''DELETE FROM categories WHERE unique_id=''' + deleteCat)
            db.connection.commit()
            cur.close()
            return redirect(url_for('admin.adminCategories'))
        #Submit för att ändra namn på kategori
        elif request.form['submit'] == 'edit':
            catID = request.form['editfield']
            newName = "('" + request.form['newname'] + "')"
            cur.execute("UPDATE categories SET category_name =" + newName + " WHERE unique_id = " + str(catID))
            db.connection.commit()
            cur.close()
            return redirect(url_for('admin.adminCategories'))
    return render_template("admin/categories.html", categories = categoryArray)

@bp.route("/admin/users")
def adminUsers():
    return render_template("admin/articles.html", artiklar = artiklar)

