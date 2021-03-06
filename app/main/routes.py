from flask import render_template, url_for, flash, redirect, request, Flask, abort, jsonify
from app.main import main_bp as bp
from app import db
from app.login.forms import EditUserForm
from flask_login import login_user, logout_user, current_user, login_required
from app.login.user import User
from app.main.forms import AddToCartForm, CartForm, CommentForm, PurchaseCartForm
import requests
from app.main.utils import *

@bp.app_errorhandler(404)
def invalid_route(e):
    return render_template("404error.html", title="404"), 404


@bp.route("/search", methods=['POST'])
def search():
    if request.method == "POST" and request.form['search_string'] != '':
        req = request.form['search_string']
        cur = db.connection.cursor()
        cur.execute('''SELECT article_id, name FROM articles
                WHERE MATCH(name) AGAINST(%s IN BOOLEAN MODE)''', (req+'*',))
        res = cur.fetchall()
        print(res)
        return jsonify(data=res)
    return jsonify(data=[])

@bp.route("/")
def home():
    cur = db.connection.cursor()
    cur.execute('''SELECT categories.category_id, categories.name FROM categories INNER JOIN articles
                    ON categories.category_id = articles.category_id
                    GROUP BY categories.name, categories.category_id''')
    categories = []
    for i in cur.fetchall():
        category = (int(i[0]),i[1])
        categories.append(category)
    return render_template("index.html", ArrayMedTräd = categories)


@bp.route("/category/<int:category_id>")
def category(category_id):
    cur = db.connection.cursor()
    cur.execute('''SELECT article_id, url, articles.name, price, categories.name
                FROM articles INNER JOIN categories
                ON articles.category_id=categories.category_id
                WHERE categories.category_id = %s''',
                (category_id,))


    result = list()
    images = list()

    for i in cur.fetchall():
        article_information = list(i)
        article_information[1] = is_url_image(article_information[1]) # Validates and sets default urls for articles.
        result.append(article_information)
    return render_template("kategori.html", artiklar = result,title=result[0][4],images = images)


@bp.route("/article/<int:article_number>", methods=['GET', 'POST'])
def article(article_number):
    cur = db.connection.cursor()
    #get data from artikel table
    cur.execute('''SELECT article_id, url, name, category_id, price, stock
                FROM articles WHERE article_id = %s''', (article_number,))
    result = cur.fetchone() 
    
    #get data from comment table
    cur.execute('''SELECT comments.comment,
                        users.user_name,
                        comments.timestamp,
                        comments.rating
                        FROM comments INNER JOIN users
                        ON comments.customer_id = users.customer_id 
                        WHERE comments.article_id = %s''',
                        (article_number,))
    allComments = list()
    for i in cur.fetchall():
        allComments.append(i)
    allComments.reverse()

    #calc average rating
    average = 0
    loop = 0
    for i in allComments:
        average = average + i[3]
        loop += 1
    try:
        average = average/loop
    except:
        average = 0


    #get data from description table
    cur.execute("""SELECT text FROM `description` WHERE description_id =
                %s""", (article_number,))

    desc = cur.fetchall()

    addToCart = AddToCartForm()
    commentForm = CommentForm()

    #Functionality for user adding comment on article
    if commentForm.validate_on_submit() and commentForm.comment.data:
        if current_user.is_authenticated != True:
            return redirect(url_for("login.login"))

        cur.execute('''INSERT INTO comments
                    (article_id, rating, comment, timestamp, customer_id)
                    VALUES (%s, %s, %s, NOW(), %s)''',
                    (article_number,
                    commentForm.rating.data,
                    commentForm.comment.data,
                    current_user.id))
        db.connection.commit()
        cur.close()
        return redirect(url_for("main.article",article_number=article_number))

    #functionality for adding article to user cart
    if addToCart.validate_on_submit() and addToCart.quantity.data>0:

        if addToCart.quantity.data > result[5]:
            flash('You cant order that many stuffs','danger')
            return render_template("article.html", artiklar = result,
                    kommentarer = allComments,picture=is_url_image(result[1]),
                    addToCartForm = addToCart,
                    commentForm = commentForm,
                    desc = desc,
                    average = average)

        customer_id = current_user.id
        cur.execute("INSERT IGNORE INTO cart (customer_id) VALUES (%s)",(customer_id,)) # SKAPA CART OM EJ FINNS, kasnke bör göra detta på ett annat ställe för "efficiency"

        #Funkar för att vi sätter en unique key som kopplar article_id med cart_id <3
        cur.execute('''INSERT INTO cart_items (article_id, cart_id, quantity)
                    VALUES (%s, (SELECT cart_id FROM cart WHERE customer_id = %s), %s)
                    ON DUPLICATE KEY UPDATE quantity = %s''',
                    (result[0], customer_id, addToCart.quantity.data, 
                        addToCart.quantity.data))

        db.connection.commit()
        cur.close()
        flash('You now have ' + str(addToCart.quantity.data) + ' ' + str(result[2]) + ' in your shopping cart.','success')

        return redirect(url_for("main.category",category_id=result[3]))

    else:
        addToCart.quantity.data = 1
    return render_template("article.html", artiklar = result,kommentarer=allComments,picture=is_url_image(result[1]) ,addToCartForm = addToCart, commentForm = commentForm, desc = desc, average = average)

@bp.route("/userdebug")
def user_debug():
    return str(current_user)

@bp.route("/order/<int:order_id>", methods=['GET', 'POST'])
@login_required
def order(order_id):
    cur = db.connection.cursor()

    cur.execute('''SELECT articles.name,order_items.quantity,order_items.price,order_items.quantity*order_items.price
                FROM order_items inner join articles on articles.article_id=order_items.article_id
                inner join orders on orders.order_id=order_items.order_id
                WHERE orders.order_id=%s and orders.user_id=%s;''', (order_id,current_user.id, ))

    res = cur.fetchall()

    cur.execute('''SELECT SUM(order_items.quantity*order_items.price) FROM
            order_items inner join orders ON orders.order_id = order_items.order_id
            WHERE order_items.order_id = %s and orders.user_id = %s''', (order_id,current_user.id, ))

    output = cur.fetchone()[0]

    totalPrice = 0 if output==None else output

    return render_template("user_order.html", orders = res,order_id=order_id,totalPrice=totalPrice)

@bp.route("/user")
@login_required
def user():
    cur = db.connection.cursor()
    cur.execute('''SELECT order_items.order_id, SUM(price*quantity)
                FROM order_items LEFT JOIN orders
                ON order_items.order_id = orders.order_id
                WHERE orders.user_id = %s
                GROUP BY order_id ORDER BY order_id DESC;''', (current_user.id, ))
    res = cur.fetchall()

    return render_template("user.html", orders = res)

@bp.route("/user/edit", methods=['GET', 'POST'])
@login_required
def edit_user():
    form = EditUserForm()
    if request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.address.data = current_user.address
        form.mail.data = current_user.mail
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    username=current_user.username,
                    password=current_user.password,
                    mail=form.mail.data,
                    address=form.address.data)
        if not form.password.data == '':
            user.set_password(form.password.data)
        user.commit()
        return redirect(url_for('main.user'))
    return render_template('user_edit.html', form=form)


@bp.route("/user/cart", methods=['GET', 'POST'])
@login_required
def cart():

    cur = db.connection.cursor()

    customer_id = current_user.id

    cur.execute('''SELECT articles.name,
                    cart_items.quantity,
                    articles.price,
                    articles.article_id,
                    cart_items.cart_items_id 
                    FROM cart_items INNER JOIN articles
                    ON articles.article_id = cart_items.article_id
                    WHERE cart_id = (SELECT cart_id FROM cart
                                    WHERE customer_id = %s)''', (customer_id,))
    #a = list()
    #[a.append(list(item)) for item in cur.fetchall()] #gör om allt till list of lists

    #Skapar ny order, lägger in alla cart_items i order_items med rätt värden. Tar bort cart.
    totalPrice = 0
    result = cur.fetchall()
    for item in result:
        #item.append(CartForm(item[1]))

        totalPrice += item[1] * item[2]
    db.connection.commit()
    cur.close()
    return render_template("user_cart.html", artiklar = result, totalPrice = totalPrice)



@bp.route("/user/cart/remove/<int:article_number>", methods=['GET','POST'])
@login_required
def remove_item(article_number):
    cur = db.connection.cursor()
    cur.execute("DELETE FROM cart_items WHERE cart_items_id= %s", (article_number,)) 
    db.connection.commit()
    cur.close()
    return redirect(url_for('main.cart'))


@bp.route("/user/cartToOrder", methods=['GET','POST'])
@login_required
def cart_to_order():

    cur = db.connection.cursor()


    #check if we can sell the amount of stuff the user wants.
    cur.execute('''SELECT articles.article_id,cart_items.quantity,articles.stock 
            FROM cart_items left join articles 
            on articles.article_id=cart_items.article_id 
            where cart_id=(select cart_id from cart where customer_id=%s)''', (current_user.id,))

    for row in cur.fetchall():
        if row[1] > row[2]:
            flash('One or more items in your shopping cart cant be processed. Out of stock!','danger')
            return redirect(url_for('main.cart'))
        
    print("check passed, now lets fix the amounts!")

    #updates the article stock.
    cur.execute('''UPDATE articles join cart_items 
            ON articles.article_id = cart_items.article_id 
            SET articles.stock = articles.stock-cart_items.quantity 
            WHERE cart_id=(select cart_id from cart where customer_id=%s)''', (current_user.id,))


    cur.execute("INSERT INTO orders (user_id) VALUES (%s)",(current_user.id,))

    cur.execute('''INSERT INTO order_items (order_id, article_id, quantity, price)
            SELECT LAST_INSERT_ID(),
            cart_items.article_id,
            cart_items.quantity,
            articles.price
            FROM cart_items LEFT JOIN articles
            ON cart_items.article_id = articles.article_id
            WHERE cart_id = (SELECT cart_id FROM cart WHERE customer_id = %s)''',
            (current_user.id,))

    cur.execute("SELECT cart_id FROM cart WHERE customer_id = %s", (current_user.id,))
    usrCartID = cur.fetchone()
    if usrCartID != None:
        cur.execute("DELETE FROM cart WHERE cart_id = %s", (usrCartID[0],))
    

    cur.connection.commit()
    cur.close()

    return redirect(url_for('main.user'))



