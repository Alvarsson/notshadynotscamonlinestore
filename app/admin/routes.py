from flask import render_template, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from flask_login.config import EXEMPT_METHODS
from functools import wraps
from app.admin import admin_bp as bp
from app import db
from app.admin.forms import AddCategoryForm, RemoveCategoryForm, EditCategoryForm
from app.admin.articleForms import ArticleForm,RemoveArticleForm
import re



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


@bp.route("/admin")
@admin_required
def admin():
    return render_template("admin/overview.html")


@bp.route("/admin/editArticle/<int:article_number>", methods=['POST', 'GET'])
@admin_required
def adminEditArticle(article_number):

    editArticle=ArticleForm(article_number)

    if editArticle.validate_on_submit() and editArticle.submitArticle.data:

        cur = db.connection.cursor()
        print(editArticle.name.data)

        cur.execute('''UPDATE articles SET
                    name = %s,
                    category_id = %s,
                    stock = %s,
                    price = %s,
                    url = %s
                    WHERE article_id = %s;''',
                    (editArticle.name.data,
                    int(editArticle.category.data),
                    int(editArticle.stock.data),
                    int(editArticle.price.data),
                    editArticle.url.data,
                    int(article_number)))

        if editArticle.description.data != "":
            cur.execute('''INSERT INTO description
                        (description_id, text)
                        VALUES
                        (%s, %s)
                        ON DUPLICATE KEY UPDATE
                        text = %s''',
                        (article_number,
                            editArticle.description.data,
                            editArticle.description.data))

        db.connection.commit()
        cur.close()
        return redirect(url_for('admin.adminArticles'))

    return render_template("admin/editArticle.html",
            editArticleForm = editArticle,
            articleNumber = article_number)



@bp.route("/admin/articles", methods=['POST', 'GET'])
@admin_required
def adminArticles():

    cur = db.connection.cursor()

    #Article list in adminview
    cur.execute('''SELECT article_id,
                            stock,
                            categories.name,
                            articles.name,
                            price
                FROM articles INNER JOIN categories ON 
                articles.category_id = categories.category_id''')
    articlesArray = []
    for article in cur.fetchall():
        articlesArray.append(article)

    addArticle = ArticleForm()
    removeArticle = RemoveArticleForm()


    if addArticle.validate_on_submit() and addArticle.submitArticle.data:
        cur.execute('''INSERT INTO articles
                    (name, category_id, price, stock, url)
                    VALUES
                    (%s, %s, %s, %s, %s)''',
                    (addArticle.name.data,
                        addArticle.category.data,
                        addArticle.price.data,
                        addArticle.stock.data,
                        addArticle.url.data))

        if addArticle.description.data != "":
            cur.execute('''INSERT INTO description
                        (text, description_id)
                        VALUES
                        (%s, (SELECT article_id FROM articles
                                WHERE name = %s))''',
                        (addArticle.description.data,
                            addArticle.name.data))
        db.connection.commit()
        cur.close()
        return redirect(url_for('admin.adminArticles'))


    if removeArticle.validate_on_submit() and removeArticle.submitRemoveArticle.data:
        articleToRemove = str(removeArticle.article.data)

        
        x = re.search("([0-9]+)-([0-9]+)", articleToRemove)
        if x:
            x = re.split("-", articleToRemove)
            x.sort()
            for i in range(int(x[0]),int(x[1])+1):
                cur.execute("DELETE FROM articles WHERE article_id = %s",(i,))
        else:
            cur.execute("DELETE FROM articles WHERE article_id= %s", (articleToRemove,))

        db.connection.commit()
        cur.close()
        return redirect(url_for('admin.adminArticles'))
    return render_template("admin/articlesv2.html",
            addArticleForm = addArticle,
            articles=articlesArray,removeArticleForm=removeArticle)

@bp.route("/admin/categories", methods=['POST', 'GET'])
@admin_required
def adminCategories():

    # Fetchar data från nuvarande kategoritabell och skriver ut på sidan
    cur = db.connection.cursor()
    cur.execute("SELECT name, category_id FROM categories ORDER BY category_id ASC;")
    categoryArray = []
    for i in cur.fetchall():
        categoryArray.append(i)

    addCategory = AddCategoryForm()
    removeCategory = RemoveCategoryForm()
    editCategory = EditCategoryForm()

    if addCategory.validate_on_submit() and addCategory.submitAdd.data:
        #newCategory = addCategory.name.data
        #newCategory = "('" + str(newCategory) + "')"
        cur.execute("INSERT INTO categories (name) VALUES (%s)", (addCategory.name.data,))
        db.connection.commit()
        cur.close()
        return redirect(url_for('admin.adminCategories'))

    if removeCategory.validate_on_submit() and removeCategory.submitRemove.data:
        cur.execute("DELETE FROM categories WHERE category_id= %s", (removeCategory.category_id.data,))
        db.connection.commit()
        cur.close()
        return redirect(url_for('admin.adminCategories'))

    if editCategory.validate_on_submit() and editCategory.submitEdit.data:
        cur.execute('''UPDATE categories SET name = %s
                        WHERE category_id = %s''',
                        (editCategory.new_name.data,
                         editCategory.category_id.data))
        db.connection.commit()
        cur.close()
        return redirect(url_for('admin.adminCategories'))
    return render_template("admin/categoriesv2.html",
            categories = categoryArray,
            addCategoryForm = addCategory,
            removeCategoryForm = removeCategory,
            editCategoryForm = editCategory)



@bp.route("/admin/orders", methods=['POST', 'GET'])
@admin_required
def adminOrders():
    # Fetchar data från nuvarande kategoritabell och skriver ut på sidan
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM orders ORDER BY order_id ASC;")
    ordersArray = []
    for i in cur.fetchall():
        ordersArray.append(i)

    

   
    return render_template("admin/orders.html",
            orders = ordersArray)



@bp.route("/admin/users", methods=['POST', 'GET'])
@admin_required
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
            cur.execute("DELETE FROM users WHERE customer_id= %s", (userID,))
            db.connection.commit()
            cur.close()
            return redirect(url_for('admin.adminUsers'))
    return render_template("admin/users.html", users=userArray)

@bp.route("/admin/order/cancel/<int:order_id>", methods=['GET','POST'])
@admin_required
def cancel_order(order_id):
    cur = db.connection.cursor()
    cur.execute("DELETE FROM orders WHERE order_id= %s", (order_id,)) 
    db.connection.commit()
    cur.close()
    return redirect(url_for('admin.adminOrders'))