from flask import render_template, url_for, flash, redirect, request, Flask, abort
from app.main import main_bp as bp
from app import db
from app.login.forms import EditUserForm
from flask_login import login_user, logout_user, current_user, login_required
from app.login.user import User
from app.main.forms import AddToCartForm, CartForm, CommentForm, PurchaseCartForm

 #Static test input
artiklar = [["Tall",3,239],["Ek",13,2329],["Lönn",31,2139]]
#artiklar = [["edward",'Username:'],["albin", 'First name:'], ["axel", 'Sur name:'], ["blabla", 'Email:'], ["hejhej", 'Adress:']]
testy = ['Username', 'First name', 'Sur name', 'Email', 'Adress', 'Password']
#kategorier = ["Barrträd", "Lövträd", "Små träd","Stora träd","Gamer-träd","Wannabee-träd","Träd från kända serier"]

@bp.app_errorhandler(404)
def invalid_route(e):
    return render_template("404error.html", title="404"), 404



@bp.route("/")
def home():
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM categories INNER JOIN articles ON categories.category_id = articles.category_id GROUP BY categories.name")

    categories = []
    for i in cur.fetchall():
        category = (int(i[0]),i[1])
        categories.append(category)
    print(categories)
    return render_template("index.html", ArrayMedTräd = categories)


@bp.route("/category/<int:category_id>")
def category(category_id):
    cur = db.connection.cursor()
    cur.execute("SELECT article_id,url,articles.name,price,categories.name FROM articles INNER JOIN categories ON articles.category_id=categories.category_id WHERE categories.category_id=" + str(category_id)) # Can't wait for that sweet, sweet SQL Injection right here.

    result = list()
    images = list()

    for i in cur.fetchall():

        #i[1]=url_for('static', filename='img/user.svg')  if i[1] == '' else i[1]
        result.append(i)


    return render_template("kategori.html", artiklar = result,title=result[0][4],images = images)


@bp.route("/article/<int:article_number>", methods=['GET', 'POST'])
def article(article_number):
    cur = db.connection.cursor()

    cur.execute("SELECT article_id, url, name, category_id, price FROM articles WHERE article_id = " + str(article_number)) # Can't wait for that sweet, sweet SQL Injection right here.
    result = cur.fetchone()

    cur.execute("SELECT comments.comment, users.user_name, comments.timestamp, comments.rating FROM comments INNER JOIN users ON comments.customer_id = users.customer_id WHERE comments.article_id ="+ str(article_number))

    allComments = list()
    for i in cur.fetchall():
        allComments.append(i)
    #print(allComments)
    addToCart = AddToCartForm()
    commentForm = CommentForm()

    if commentForm.validate_on_submit() and commentForm.comment.data:
        if current_user.is_authenticated != True:
            return redirect(url_for("login.login"))

        customer_id = current_user.id

        cur.execute("INSERT INTO comments (article_id, rating, comment, timestamp, customer_id) VALUES ("+
                                         str(article_number)+
                                         ", "+ str(commentForm.rating.data) +
                                         ", '"+ str(commentForm.comment.data) +
                                         "', NOW()," + str(customer_id) +
                                         ");")
        db.connection.commit()
        cur.close()
        return redirect(url_for("main.article",article_number=article_number))

    if addToCart.validate_on_submit() and addToCart.quantity.data:


        #cur = db.connection.cursor()
        customer_id = current_user.id
        print(current_user.id)

        cur.execute("INSERT IGNORE INTO cart (customer_id) VALUES ("+str(customer_id)+");") # SKAPA CART OM EJ FINNS, kasnke bör göra detta på ett annat ställe för "efficiency"

        #Funkar för att vi sätter en unique key som kopplar article_id med cart_id <3
        cur.execute("INSERT INTO cart_items (article_id, cart_id, quantity) VALUES ("+
                    str(result[0]) +", (SELECT cart_id FROM cart WHERE customer_id = "+ str(customer_id) +"), "
                    + str(addToCart.quantity.data) +") ON DUPLICATE KEY UPDATE QUANTITY="+ str(addToCart.quantity.data) +";")

        db.connection.commit()
        cur.close()
        #print(cur.fetchone())
        return redirect(url_for("main.category",category_id=result[3]))

    else:
        addToCart.quantity.data = 1

    return render_template("article.html", artiklar = result,kommentarer=allComments,picture=result[1],addToCartForm = addToCart, commentForm = commentForm)

@bp.route("/userdebug")
def user_debug():
    return str(current_user)

#man kan nå någon annans order nu...
@bp.route("/order/<int:order_id>", methods=['GET', 'POST'])
@login_required
def order(order_id):
    cur = db.connection.cursor()
    cur.execute('''SELECT articles.name,order_items.quantity,order_items.price , order_items.quantity*order_items.price
                FROM order_items inner join articles on articles.article_id=order_items.article_id 
                WHERE order_id=%s''', (order_id, ))
    res = cur.fetchall()           

    cur.execute('''SELECT SUM(quantity*price) from order_items where order_id=%s''', (order_id, ))

    totalPrice = cur.fetchone()[0]
    
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

    cur.execute("SELECT articles.name,cart_items.quantity,articles.price,articles.article_id,cart_items.cart_items_id " +
                "FROM cart_items inner join articles on articles.article_id=cart_items.article_id "+
                "WHERE cart_id=(SELECT cart_id FROM cart WHERE customer_id = "+str(customer_id) + "); ")
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


    return render_template("user_cart.html", artiklar = result,totalPrice = totalPrice)



@bp.route("/user/cart/remove/<int:article_number>", methods=['GET','POST'])
@login_required
def remove_item(article_number):
    print("yoloss remove")
    cur = db.connection.cursor()
    cur.execute("DELETE FROM cart_items WHERE cart_items_id=" + str(article_number)) # Can't wait for that sweet, sweet SQL Injection right here.

    db.connection.commit()
    cur.close()

    return redirect(url_for('main.cart'))


@bp.route("/user/cartToOrder", methods=['GET','POST'])
@login_required
def cart_to_order():

    cur = db.connection.cursor()
    cur.execute("INSERT INTO orders (user_id) VALUES (" + str(current_user.id) + ");")

    cur.execute("INSERT INTO order_items (order_id, article_id, quantity, price) " +
        "SELECT LAST_INSERT_ID(), cart_items.article_id, cart_items.quantity, articles.price " +
        "FROM cart_items LEFT JOIN articles " +
        "ON cart_items.article_id = articles.article_id " +
        "WHERE cart_id = (SELECT cart_id FROM cart WHERE customer_id ="+ str(current_user.id) +");")

    cur.execute("DELETE FROM cart WHERE " +
        "cart_id = (SELECT cart_id FROM cart WHERE customer_id ="+ str(current_user.id) +");")

    cur.connection.commit()
    cur.close()

    print("slut")
    return redirect(url_for('main.user'))



