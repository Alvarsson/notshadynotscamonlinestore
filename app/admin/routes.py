from flask import render_template, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from flask_login.config import EXEMPT_METHODS
from functools import wraps
from app.admin import admin_bp as bp
from app import db
from app.admin.forms import AddCategoryForm, RemoveCategoryForm, EditCategoryForm
from app.admin.articleForms import ArticleForm,RemoveArticleForm


artiklar = ["edward", "albin", "axel", "blabla", "hejhej"]

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.config.get('LOGIN_DISABLED'):
            return func(*args, **kwargs)
        elif not (current_user.is_authenticated and current_user.admin):
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view

#Helperfunktion -- Skönt för att kunna debugga -- Ta bort i när vi går live
@bp.route("/userinfo")
def user_info():
    if current_user.is_authenticated:
        return str(current_user)
    return "Not logged in"

@bp.route("/admin")
@admin_required
def admin():
    return render_template("admin/overview.html", artiklar=artiklar)


@bp.route("/admin/editArticle/<int:article_number>", methods=['POST', 'GET'])
def adminEditArticle(article_number):

    editArticle=ArticleForm(article_number)

    if editArticle.validate_on_submit() and editArticle.submitArticle.data:

        cur = db.connection.cursor()
        print(editArticle.name.data)

        #editID = str(editArticle.article_number) tycker inte det är en bra ide att låta folk göra detta. exempel hoppa till 100 när count är 23 osv
        newName = str(editArticle.name.data)
        newStock = str(editArticle.stock.data)
        newPrice = str(editArticle.price.data)

        newPicture = str(editArticle.url.data)
        ###########################glöm inte kategori. problem med att nuvarande inte visas när man skriver .data delen...
        cur.execute("UPDATE articles SET article_name= " + "'" + newName + "'" +", stock_quantity=" +  newStock + ", price=" + newPrice + ",picture_url='" + newPicture  +  "' WHERE article_number= " + str(article_number) +";")
        #cur.execute("UPDATE articles SET article_name= " + "'" + newName + "' WHERE article_number= " + str(article_number) +";")

        #cur.execute("""UPDATE articles SET article_name = "TallTall", stock_quantity= 123, price= 124, picture_url= "texas.com"  WHERE article_number=2;""")

        newDescription = str(editArticle.description.data)
        if newDescription != "":
            #upsert, så infoga ny rad om ingen finns, annars uppdatera googla det
            cur.execute("INSERT INTO article_description (description_id,art_description) VALUES ( " + str(article_number) + ",'" + newDescription+ "') ON DUPLICATE KEY UPDATE art_description ='" + newDescription + "';")
            print("Uppdaterar eller infogar nya data i description tabellen")

        db.connection.commit()
        cur.close()
        return redirect(url_for('admin.adminArticles'))

    return render_template("admin/editArticle.html",editArticleForm = editArticle, articleNumber = article_number)



@bp.route("/admin/articles", methods=['POST', 'GET'])
def adminArticles():

    cur = db.connection.cursor()

    #Article list in adminview
    cur.execute("SELECT article_number,stock_quantity,category_name,article_name,price FROM articles INNER JOIN categories ON articles.category=categories.category_id;")
    articlesArray = []
    for article in cur.fetchall():
        articlesArray.append(article)

    addArticle = ArticleForm()
    removeArticle = RemoveArticleForm()


    if addArticle.validate_on_submit() and addArticle.submitArticle.data:
        #print(str(addArticle.category.data))
        print("Adding article")
        #det här kan ju såklart tas bort, men sql queriet blir något lättare att läsa och pilla i.
        chooseCat = str(addArticle.category.data)
        articleName = str(addArticle.name.data)
        stockAmount = str(addArticle.stock.data)
        price = str(addArticle.price.data)
        url = str(addArticle.url.data)
        desc = str(addArticle.description.data)

        cur.execute("INSERT INTO articles (article_name, category, price, stock_quantity, picture_url) VALUES ('" + articleName + "','" + chooseCat +
                     "', '" + price+ "' ,  '" + stockAmount + "'   ,'" + url + "');")
        if desc != "":
            cur.execute("INSERT INTO article_description (art_description, description_id ) VALUES ('" + desc +
             "', (SELECT article_number FROM articles WHERE article_name='" + articleName + "'));")
        db.connection.commit()
        cur.close()
        return redirect(url_for('admin.adminArticles'))


    if removeArticle.validate_on_submit() and removeArticle.submitRemoveArticle.data:
        articleToRemove = str(removeArticle.article.data)
        cur.execute("DELETE FROM articles WHERE article_number=" + articleToRemove + ";")
        print("removed article")
        db.connection.commit()
        cur.close()
        return redirect(url_for('admin.adminArticles'))

    # elif request.form['submit'] == 'remove':
    #     removeArticle = request.form['removefield']
    #     cur.execute("DELETE FROM articles WHERE article_number=" + removeArticle + ";")
    #     db.connection.commit()
    #     cur.close()
    #     return redirect(url_for('admin.adminArticles'))

    return render_template("admin/articlesv2.html", addArticleForm = addArticle, articles=articlesArray,removeArticleForm=removeArticle)

@bp.route("/admin/categories", methods=['POST', 'GET'])
def adminCategories():

    # Fetchar data från nuvarande kategoritabell och skriver ut på sidan
    cur = db.connection.cursor()
    cur.execute("SELECT category_name, category_id FROM categories ORDER BY category_id ASC;")
    categoryArray = []
    for i in cur.fetchall():
        categoryArray.append(i)

    addCategory = AddCategoryForm()
    removeCategory = RemoveCategoryForm()
    editCategory = EditCategoryForm()

    if addCategory.validate_on_submit() and addCategory.submitAdd.data:
        newCategory = addCategory.name.data
        newCategory = "('" + str(newCategory) + "')"
        cur.execute("INSERT INTO categories (category_name) VALUES" + newCategory + ";")
        db.connection.commit()
        cur.close()
        return redirect(url_for('admin.adminCategories'))


    if removeCategory.validate_on_submit() and removeCategory.submitRemove.data:
        print("remoive")
        deleteCat = removeCategory.category_id.data
        cur.execute("DELETE FROM categories WHERE category_id=" + str(deleteCat))
        db.connection.commit()
        cur.close()
        return redirect(url_for('admin.adminCategories'))

    if editCategory.validate_on_submit() and editCategory.submitEdit.data:
        catID = str(editCategory.category_id.data)
        newName = str(editCategory.new_name.data)

        cur.execute("UPDATE categories SET category_name ='" + newName + "' WHERE category_id = " + catID +";")
        db.connection.commit()
        cur.close()
        return redirect(url_for('admin.adminCategories'))


    return render_template("admin/categoriesv2.html", categories=categoryArray, addCategoryForm=addCategory, removeCategoryForm=removeCategory,
     editCategoryForm=editCategory)


@bp.route("/admin/users", methods=['POST', 'GET'])
def adminUsers():
    cur = db.connection.cursor()
    cur.execute(
        "SELECT customer_id, first_name, last_name, user_name FROM users ORDER BY customer_id ASC;")
    userArray = []
    for user in cur.fetchall():
        userArray.append(user)

    if request.method == 'POST':
        if request.form['submit'] == 'removeuser':
            userID = request.form['userfield']
            cur.execute("DELETE FROM users WHERE customer_id=" + userID + ";")
            db.connection.commit()
            cur.close()
            return redirect(url_for('admin.adminUsers'))
    return render_template("admin/users.html", users=userArray)


# @bp.route("/admin/articles", methods=['POST', 'GET'])
# def adminArticles():
#     cur = db.connection.cursor()
#     cur.execute("SELECT category_name, category_id FROM categories")
#     categoryArray = []
#     for cat in cur.fetchall():
#         categoryArray.append(cat)

#     cur.execute(
#         "SELECT article_number, article_name, stock_quantity, price FROM articles")
#     articlesArray = []
#     for art in cur.fetchall():
#         articlesArray.append(art)

#     if request.method == 'POST':
#         # Submit för att lägga till artiklar
#         if request.form['submit'] == 'addarticle':
#             chooseCat = "('" + request.form['chooseCategory'] + "')"
#             articleName = "('" + request.form['article'] + "')"
#             stockAmount = request.form['stock']
#             price = request.form['price']
#             url = "('" + request.form['url'] + "')"
#             desc = request.form['description']

#             cur.execute("INSERT INTO articles (article_name, category, price, stock_quantity, picture_url) VALUES (" + articleName +
#                         ",(SELECT category_id FROM categories WHERE category_name=" + chooseCat + ")," + price + "," + stockAmount + "," + url + ");")
#             if desc != "":
#                 desc = "('" + request.form['description'] + "')"
#                 cur.execute("INSERT INTO article_description (description, description_number ) VALUES (" +
#                             desc + ", (SELECT article_number FROM articles WHERE article_name=" + articleName + "));")
#             db.connection.commit()
#             cur.close()
#             return redirect(url_for('admin.adminArticles'))
#         # Ta bort artikel
#         elif request.form['submit'] == 'remove':
#             removeArticle = request.form['removefield']
#             cur.execute(
#                 "DELETE FROM articles WHERE article_number=" + removeArticle + ";")
#             db.connection.commit()
#             cur.close()
#             return redirect(url_for('admin.adminArticles'))
#         # Ändra artikelinformation
#         elif request.form['submit'] == 'edit':
#             editID = request.form['editfield']
#             newName = "('" + request.form['newname'] + "')"
#             newStock = request.form['newstock']
#             newPrice = request.form['newprice']
#             newDescription = request.form['newdescription']
#             cur.execute("UPDATE articles SET article_name=" + newName + ", stock_quantity=" +
#                         newStock + ", price=" + newPrice + " WHERE article_number= " + editID + ";")
#             if newDescription != "":
#                 newDescription = "('" + request.form['newdescription'] + "')"
#                 cur.execute("UPDATE article_description SET description=" +
#                             newDescription + " WHERE description_number= " + editID + ";")
#             db.connection.commit()
#             cur.close()
#             return redirect(url_for('admin.adminArticles'))

#     return render_template("admin/articles.html", categories=categoryArray, articles=articlesArray
