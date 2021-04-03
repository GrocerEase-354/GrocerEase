from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint
from flask_mysqldb import MySQL
from flask_login import login_required, current_user
from . import mysql
from datetime import date

main = Blueprint('main', __name__)

@main.route("/")
def home():
    cursor = mysql.connection.cursor()
    # get the first user
    cursor.execute('''SELECT * FROM customer;''')
    users = cursor.fetchall()
    user = users[0]
    session['user'] = user
    session['orderID'] = 999
    cursor.close()
    return render_template("index.html", user=current_user)

@main.route("/shopping_cart", methods=["GET", "POST"])
@login_required
def shopping_cart():
    cursor = mysql.connection.cursor()

    user = current_user

    # get the items in the cart
    cursor.execute(f'''SELECT P.product_name, PSC.quantity, P.price, P.price*PSC.quantity AS total_price
                       FROM product_in_shopping_cart AS PSC, product AS P 
                       WHERE customerid="{user.userid}" AND PSC.productid = P.productid;''')
    products = cursor.fetchall()
    cursor.close()

    # get the subtotal
    subtotal = sum([int(products[-1]*100) for products in products])/100
    session['subtotal'] = subtotal
    print(user)
    print(products)
    if request.method == "POST":
        if "sc" in request.form:
            return redirect(url_for(".home"))
        elif "checkout" in request.form:
            if len(products) == 0:
                flash("No products ordered!")
                return redirect(url_for(".shopping_cart"))
            else:
                return redirect(url_for(".checkout"))
        for p in products:
            #print(f"delete_{p[0]}")
            if f"delete_{p[0]}" in request.form:
                cursor = mysql.connection.cursor()
                cursor.execute(f'''DELETE FROM product_in_shopping_cart
                                   WHERE customerid="{user.userid}" AND productid IN (
                                       SELECT productid
                                       FROM product
                                       WHERE product_name="{p[0]}");''')
                mysql.connection.commit()
                cursor.close()
                print(f"deleting {p[0]}")
                return redirect(url_for(".redirect_on_delete"))

    cursor = mysql.connection.cursor() 
    # get the items in the cart
    cursor.execute(f'''SELECT P.product_name, PSC.quantity, P.price, P.price*PSC.quantity AS total_price
                       FROM product_in_shopping_cart AS PSC, product AS P 
                       WHERE customerid="{user.userid}" AND PSC.productid = P.productid;''')
    products = cursor.fetchall()
    cursor.close()

    return render_template("shopping_cart.html", items=products, subtotal=subtotal, user=current_user)

@main.route("/redirect")
@login_required
def redirect_on_delete():
    return redirect(url_for(".shopping_cart"))

@main.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout(): 
    cursor = mysql.connection.cursor()

    user = current_user

    # get the subtotal
    subtotal = session['subtotal']

    if request.method == "POST":
        if "confirm" in request.form:
            ts = date.today()

            cursor = mysql.connection.cursor()

            cursor.execute(f"""SELECT orderid FROM store_order GROUP BY orderid ORDER BY orderid DESC""")

            orderID = cursor.fetchall()[0][0]+1

            subtotal = session['subtotal']

            print(orderID)

            cursor.execute(f"""INSERT INTO store_order (`customerid`, `orderid`, `cost`, `order_time`, `payment_method_used`)
                            VALUES ('{user.userid}', {orderID}, {subtotal*1.12}, '{ts}', '{user.payment_method}')""")
            mysql.connection.commit()

            cursor.execute(f"""DELETE FROM product_in_shopping_cart
                               WHERE customerid='{user.userid}'""")
            mysql.connection.commit()
            return redirect(url_for(".order_confirmed"))
            
        elif "cancel" in request.form:
            return redirect(url_for(".shopping_cart"))

    return render_template("checkout.html", user=current_user, subtotal=subtotal, user_dict={
        "Name": current_user.fname + " " + current_user.lname,
        "Email": current_user.email,
        "House Number": current_user.house_number,
        "Street Name": current_user.street_name,
        "Postal Code": current_user.postal_code,
        "Province": current_user.province,
        "City": current_user.city,
        "Payment Method": current_user.payment_method
    })

@main.route("/order_confirmed", methods=["GET", "POST"])
@login_required
def order_confirmed():
    # TODO: Fix orderID incrementing
    ts = date.today()

    orderID = session['orderID']

    if request.method == "POST":
        if "home" in request.form:
            return redirect(url_for(".home"))

    return render_template("order_confirmed.html", orderID=orderID, timestamp=ts, user=current_user)

@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html", name=current_user.fname+" "+current_user.lname, user=current_user)

@main.route("/logged_out")
def logged_out():
    return render_template("logged_out.html", user=current_user)