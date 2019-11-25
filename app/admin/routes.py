from flask import render_template, redirect, url_for, request
from app.admin import admin_bp as bp
from app import db
from app.admin.forms import AddCategoryForm, RemoveCategoryForm, EditCategoryForm
from app.admin.articleForms import AddArticleForm


artiklar = ["edward", "albin", "axel", "blabla", "hejhej"]


@bp.route("/admin")
def admin():
    return render_template("admin/overview.html", artiklar=artiklar)


@bp.route("/admin/articles", methods=['POST', 'GET'])
def adminArticles():
    cur = db.connection.cursor()
    cur.execute("SELECT  category_id,category_name FROM categories")
    categoryArray = []
    for cat in cur.fetchall():
        categoryArray.append(cat)

    cur.execute(
        "SELECT article_number, article_name, stock_quantity, price FROM articles")
    articlesArray = []
    for art in cur.fetchall():
        articlesArray.append(art)
        
    #print(categoryArray)
    
    
    addArticle = AddArticleForm()
    addArticle.category.choices = categoryArray #fill dropdown with categories
    
    
    if addArticle.validate_on_submit() and addArticle.submitAddArticle.data:
        
        print("adding a new article")
        chooseCat = "('" + addArticle.category.data + "')"
        articleName = "('" + addArticle.name.data + "')"
        stockAmount = addArticle.stock.data
        price = addArticle.price.data
        url = "('" + addArticle.url.data + "')"
        desc = addArticle.description.data

        cur.execute("INSERT INTO articles (article_name, category, price, stock_quantity, picture_url) VALUES (" + articleName +
                    ",(SELECT category_id FROM categories WHERE category_name=" + chooseCat + ")," + price + "," + stockAmount + "," + url + ");")
        if desc != "":
            desc = "('" + request.form['description'] + "')"
            cur.execute("INSERT INTO article_description (description, description_number ) VALUES (" +
                        desc + ", (SELECT article_number FROM articles WHERE article_name=" + articleName + "));")
        db.connection.commit()
        cur.close()
        return redirect(url_for('admin.adminArticles'))
   

    return render_template("admin/articlesv2.html", addArticleForm = addArticle, articles=articlesArray)


@bp.route("/admin/categories", methods=['POST', 'GET'])
def adminCategories():

    # Fetchar data från nuvarande kategoritabell och skriver ut på sidan
    cur = db.connection.cursor()
    cur.execute(
        '''SELECT category_name, category_id FROM categories ORDER BY category_id ASC;''')
    categoryArray = []
    for i in cur.fetchall():
        categoryArray.append(i)
        
    addCategory = AddCategoryForm()
    removeCategory = RemoveCategoryForm()
    editCategory = EditCategoryForm()

    
    if addCategory.validate_on_submit() and addCategory.submitAdd.data:
        print("adding a new category")
        newCategory = addCategory.name.data
        newCategory = "('" + str(newCategory) + "')"
        cur.execute(
            '''INSERT INTO categories (category_name) VALUES''' + newCategory + ";")
        db.connection.commit()
        cur.close()
        return redirect(url_for('admin.adminCategories'))

    
    elif removeCategory.validate_on_submit() and removeCategory.submitRemove.data:
        print("removing")
        
        deleteCat = removeCategory.category_id.data
        cur.execute(
            '''DELETE FROM categories WHERE category_id=''' + str(deleteCat))
        db.connection.commit()
        cur.close()
        return redirect(url_for('admin.adminCategories'))
    
    elif editCategory.validate_on_submit() and editCategory.submitEdit.data:
        print("editing")

        catID = str(editCategory.category_id.data)
        newName = str(editCategory.new_name.data)
        
        cur.execute("UPDATE categories SET category_name ='" + newName + "' WHERE category_id = " + catID +";")
        #UPDATE categories SET category_name ='Abbe' WHERE category_id = 16;
        
        db.connection.commit()
        cur.close()
        return redirect(url_for('admin.adminCategories'))


    return render_template("admin/categoriesv2.html", categories=categoryArray, addCategoryForm=addCategory, removeCategoryForm=removeCategory, editCategoryForm=editCategory)


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

#     return render_template("admin/articles.html", categories=categoryArray, articles=articlesArray)