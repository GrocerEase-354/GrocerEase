from flask import Flask, render_template, redirect, url_for, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
from flask_login import login_user, logout_user, login_required, LoginManager, current_user, UserMixin
from user import User, create_user
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from datetime import date
from useraccountforms import CustomerNameForm, SellerCompanyNameForm, PasswordForm, EmailForm, AddressForm, PaymentMethodForm
from login_signup_forms import LoginForm, SignupForm
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SubmitField, BooleanField, TextField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, Email, EqualTo, Optional
import MySQLdb

app = Flask(__name__)

bootstrap = Bootstrap(app)

app.config['MYSQL_HOST'] = '10.0.2.2'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'cmpt354'
app.config['SECRET_KEY'] = 'test'

mysql = MySQL(app)

topbar = Navbar(View("Home", "home"))

nav = Nav()
nav.register_element('topbar', topbar)
nav.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    cursor = mysql.connection.cursor()
    # see if user is in DB
    cursor.execute(
        f"""SELECT `user_password`, `house_number`, `street_name`, `postal_code`, `province`, `city`, `email` 
        FROM user 
        WHERE userid=%(user_id)s""", {'user_id': user_id})
    user = cursor.fetchall()[0]
    pw, hn, sn, pc, pv, c, em = user[0], user[1], user[2], user[3], user[4], user[5], user[6]
    cursor.execute(
        f"""SELECT first_name, last_name 
        FROM customer
        WHERE id=%(user_id)s""", {'user_id': user_id})
    name = cursor.fetchall()[0]
    fn, ln = name[0], name[1]
    cursor.execute(
        f"""SELECT payment_method
        FROM customer_payment_method
        WHERE customerid=%(user_id)s""", {'user_id': user_id})
    pm = cursor.fetchall()

    cursor.close()
    return User(
        userid=user_id,
        password=pw,
        house_number=hn,
        street_name=sn,
        postal_code=pc,
        province=pv,
        city=c,
        email=em,
        fname=fn,
        lname=ln,
        payment_methods=pm
    )


@app.route('/login')
def login():
    login_form = LoginForm()
    return render_template('login.jinja2', form=login_form)

@app.route('/signup')
def signup():
    return render_template('signup.jinja2')

#@auth.route('/logout')
#def logout():
#    return render_template('Logout')

@app.route('/signup', methods=['POST'])
def signup_post():
    username = request.form.get('username')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    password = request.form.get('password')
    email = request.form.get('email')
    house_number = request.form.get('house_number')
    street_name = request.form.get('street_name')
    postal_code = request.form.get('postal_code')
    province = request.form.get('province')
    city = request.form.get('city')
    payment_method = request.form.get('payment_method')

    cursor = mysql.connection.cursor()
    # see if user is in DB
    cursor.execute(f"""SELECT * FROM user WHERE userid=%(username)s""", {'username': username})
    user = cursor.fetchall()

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash("Username is already in use")
        return redirect(url_for('signup'))
    
    print(request.form)
    print(username, fname, lname, password, email, house_number, street_name, postal_code, province, city, payment_method)

    #session['user'] = user_obj
    try:
        if len(password) < 1 or len(password) > 100:
            flash("Password must be between 1 and 100 characters long!")
            raise MySQLdb.OperationalError

        # parameterizing to avoid an SQL injection

        # add user to DB
        cursor.execute(f"""INSERT INTO user (`userid`, `user_password`, `house_number`, `street_name`, `postal_code`, `province`, `city`, `email`)
                        VALUES(%(username)s, %(password)s, %(house_number)s, %(street_name)s, %(postal_code)s, %(province)s, %(city)s, %(email)s)"""
                        , {'username': username, 'password': generate_password_hash(password, method='sha256'), 'house_number': house_number,
                        'street_name': street_name, 'postal_code': postal_code, 'province': province, 'city': city, 'email': email})
        # add customer to DB
        cursor.execute(f"""INSERT INTO customer (id, first_name, last_name)
                        VALUES(%(username)s, %(fname)s, %(lname)s)""",
                        {'username': username, 'fname': fname, 'lname': lname})
        cursor.execute(f"""INSERT INTO customer_payment_method (customerid, payment_method)
                        VALUES(%(username)s, %(payment_method)s)""",
                        {'username': username, 'payment_method': payment_method})
        # add cart to DB
        cursor.execute(f"""INSERT INTO shopping_cart (customerid)
                           VALUES(%(username)s)""",
                           {'username': username})
        mysql.connection.commit()

    except MySQLdb.OperationalError as e:
        print(' '.join([e2.strip(" )\"\'(") for e2 in str(e).split(',')][1:]))
        flash(' '.join([e2.strip(" )\"\'(") for e2 in str(e).split(',')][1:]))
        return render_template("signup.jinja2", username=username,
                                            house_number=house_number,
                                            street_name=street_name,
                                            postal_code=postal_code,
                                            city=city,
                                            email=email,
                                            fname=fname,
                                            lname=lname)

    except MySQLdb._exceptions.DataError as e:
        e = ' '.join([e2.strip(" )\"\'(") for e2 in str(e).split(',')][1:])
        e = ' '.join(e[e.find("'")+1:e.find("'", e.find("'")+1)].split("_"))
        flash(e.capitalize() + " must be between 1 and 100 characters!")
        return render_template("signup.jinja2", username=username,
                                            house_number=house_number,
                                            street_name=street_name,
                                            postal_code=postal_code,
                                            city=city,
                                            email=email,
                                            fname=fname,
                                            lname=lname) 

    cursor.close()

    # code to validate and add user to database goes here
    return redirect(url_for('login'))

@app.route('/login', methods=['POST'])
def login_post():
    login_form = LoginForm()
    if login_form.validate_on_submit(): 
        username = ""
        password = ""
        for field in login_form:
            if field.name != 'submit' and field.name != 'csrf_token' and field.data != None and field.data != '':
                if field.name == 'username':
                    username = field.data
                elif field.name == 'password':
                    password = field.data
        remember = True if request.form.get('remember') else False

        cursor = mysql.connection.cursor()
        # see if user is in DB, parameterize input to avoid sql injection
        cursor.execute(f"""SELECT * FROM user WHERE userid=%(username)s""", {'username': username})
        user = cursor.fetchall()
        cursor.close()
        print(user)
        if not user or (not check_password_hash(user[0][1], password)): # if a user is found, we want to redirect back to signup page so user can try again
            flash("Username/Password is invalid")
            return redirect(url_for('login'))
        user2 = create_user(user[0][0])
        print("Jello")
        login_user(user2, remember=remember)
        return redirect(url_for('home'))

    return render_template('login.jinja2', form=login_form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("logged_out"))

@app.route("/")
def home():
    return render_template("index.jinja2", user=current_user if current_user.is_authenticated else None)

@app.route("/shopping_cart", methods=["GET", "POST"])
@login_required
def shopping_cart():
    cursor = mysql.connection.cursor()

    user = current_user

    # get the items in the cart
    cursor.execute(f'''SELECT P.product_name, P.productid, PSC.quantity, P.price, P.price*PSC.quantity AS total_price
                       FROM product_in_shopping_cart AS PSC, product AS P 
                       WHERE customerid=%(userid)s AND PSC.productid = P.productid;''', {'userid': user.userid})
    products = cursor.fetchall()
    cursor.close()

    # get the subtotal
    subtotal = sum([int(products[-1]*100) for products in products])/100
    session['subtotal'] = subtotal
    print(user)
    print(products)
    if request.method == "POST":
        if "sc" in request.form:
            return redirect(url_for("home"))
        elif "checkout" in request.form:
            if len(products) == 0:
                flash("No products ordered!")
                return redirect(url_for("shopping_cart"))
            else:
                return redirect(url_for("checkout"))
        for p in products:
            #print(f"delete_{p[0]}")
            if f"delete_{p[1]}" in request.form:
                cursor = mysql.connection.cursor()
                cursor.execute(f'''DELETE FROM product_in_shopping_cart
                                   WHERE customerid=%(userid)s AND productid = %(pid)s;''', {'userid': user.userid, 'pid': p[1]})
                mysql.connection.commit()
                cursor.close()
                print(f"deleting {p[1]}")
                return redirect(url_for("redirect_on_delete"))


    cursor = mysql.connection.cursor() 

    #calculating healthy choice
    cursor.execute(f''' SELECT COUNT(*) 
                        FROM customer A 
                        WHERE A.id = %(userid)s AND A.id IN (
                            SELECT B.id 
                            FROM customer B
                            WHERE NOT EXISTS (
                                SELECT category_name FROM category
                                WHERE category_name NOT IN (SELECT product.category_name 
                                                            FROM product_in_shopping_cart, product 
                                                            WHERE product_in_shopping_cart.productid = product.productid AND product_in_shopping_cart.customerid = B.id)))
                    ''', {'userid': user.userid})
    isHealthyChoice = cursor.fetchone()[0]
    print(isHealthyChoice)
    cursor.close()

    return render_template("shopping_cart.jinja2", items=products, subtotal=subtotal, user=current_user, isHealthyChoice=isHealthyChoice)


@app.route("/redirect")
@login_required
def redirect_on_delete():
    return redirect(url_for("shopping_cart"))

@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout(): 
    cursor = mysql.connection.cursor()
    user = current_user

    # get the subtotal
    subtotal = session['subtotal']

    if request.method == "POST":
        if "confirm" in request.form:
            payment_method = request.form.get('payment_method')
            if payment_method != "":
                ts = date.today()

                cursor = mysql.connection.cursor()
                       
                subtotal = session['subtotal']

                cursor.execute(f"""INSERT INTO store_order (`customerid`, `cost`, `order_time`, `payment_method_used`)
                                VALUES (%(user_id)s, {subtotal*1.12}, '{ts}', '{payment_method}')""", {'user_id': current_user.userid})
                mysql.connection.commit()

                cursor.execute(f"""DELETE FROM product_in_shopping_cart
                                WHERE customerid=%(user_id)s""", {'user_id': current_user.userid})
                mysql.connection.commit()
                return redirect(url_for("order_confirmed"))
            
        elif "cancel" in request.form:
            return redirect(url_for("shopping_cart"))

    return render_template("checkout.jinja2", user=current_user, subtotal=subtotal, payment_methods = current_user.payment_methods, user_dict={
        "Name": current_user.fname + " " + current_user.lname,
        "Email": current_user.email,
        "House Number": current_user.house_number,
        "Street Name": current_user.street_name,
        "Postal Code": current_user.postal_code,
        "Province": current_user.province,
        "City": current_user.city,
    })

@app.route("/order_confirmed", methods=["GET", "POST"])
@login_required
def order_confirmed():
    # TODO: Fix orderID incrementing
    ts = date.today()

    cursor = mysql.connection.cursor()
    cursor.execute(f"""SELECT MAX(orderid)
                    FROM store_order
                    WHERE customerid=%(current_user_userid)s""", {'current_user_userid': current_user.userid}) 
    orderID = cursor.fetchall()[0][0]

    if request.method == "POST":
        if "home" in request.form:
            return redirect(url_for("home"))

    return render_template("order_confirmed.jinja2", orderID=orderID, timestamp=ts, user=current_user)

@app.route("/logged_out")
def logged_out():
    return render_template("logged_out.jinja2", user=current_user)

@app.route("/categories", methods=['GET', 'POST'])
def categories():
    if request.method == "POST":
        if "submitbutton" in request.form:
            return redirect(url_for("home"))
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT category_name, COUNT(*) FROM product GROUP BY category_name")
    retVal = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM product")
    total = cursor.fetchall()
    cursor.close()
    return render_template("overview.jinja2", retVal = retVal, total = total)

@app.route("/category/<selected_category>", methods=['GET', 'POST'])
@login_required
def goToCategory(selected_category):
    actualSelectedCategory = selected_category.lower()
    if (actualSelectedCategory == "all"):
        actualSelectedCategory = "%"
    cursor = mysql.connection.cursor()
    productsToSelect = "product_name, price, sellerid, product_description, category_name, best_before_date, productid"
    # preventing SQL injection from URL
    cursor.execute(f"SELECT { productsToSelect } FROM product WHERE LOWER(category_name) LIKE %(parameterInput)s", {'parameterInput': actualSelectedCategory})
    retVal = cursor.fetchall()
    cursor.close()

    if (request.method == "POST"):
        if (request.form['submitbutton'] == "home"):
            return redirect(url_for("home"))
        else:
            cursor2 = mysql.connection.cursor()
            cursor2.execute(f"SELECT cartid FROM shopping_cart WHERE customerid = %(current_user_userid)s", {'current_user_userid': current_user.userid})
            cartid = cursor2.fetchall()[0][0]

            #checkexist = f"SELECT productid, customerid, cartid FROM product_in_shopping_cart WHERE productid='{request.form['submitbutton']}' AND customerid='{ current_user.userid }' AND cartid = '{ cartid }' "
            cursor2.execute(f"SELECT productid, customerid, cartid FROM product_in_shopping_cart WHERE productid='{request.form['submitbutton']}' AND customerid=%(current_user_userid)s AND cartid = '{ cartid }' ",
                            {'current_user_userid': current_user.userid})
            checkexistret = cursor2.fetchall()
            if (checkexistret):
                #updatebyone = f'''UPDATE product_in_shopping_cart SET quantity = quantity + 1 
                #            WHERE product_in_shopping_cart.productid IN (
                #            SELECT * FROM (SELECT B.productid FROM product_in_shopping_cart A 
                #            INNER JOIN product_in_shopping_cart B ON A.productid = B.productid WHERE A.productid = {request.form['submitbutton']} 
                #            AND A.customerid = '{ current_user.userid }' AND A.cartid = { cartid }) as temp)'''
                cursor2.execute(f'''UPDATE product_in_shopping_cart SET quantity = quantity + 1 
                            WHERE product_in_shopping_cart.productid IN (
                            SELECT * FROM (SELECT B.productid FROM product_in_shopping_cart A 
                            INNER JOIN product_in_shopping_cart B ON A.productid = B.productid WHERE A.productid = {request.form['submitbutton']} 
                            AND A.customerid = %(current_user_userid)s AND A.cartid = { cartid }) as temp)''',
                            {'current_user_userid': current_user.userid})
                mysql.connection.commit()
            else:
                #commitmsg = f"INSERT INTO product_in_shopping_cart VALUES({request.form['submitbutton']}, '{ current_user.userid }', { cartid }, 1)"
                cursor2.execute(f"INSERT INTO product_in_shopping_cart VALUES({request.form['submitbutton']}, %(current_user_userid)s, { cartid }, 1)",
                                {'current_user_userid': current_user.userid})
                mysql.connection.commit()
            
            cursor2.close()

            
            return redirect(url_for("goToCategory", selected_category = selected_category))
    else:      
        return render_template("category.jinja2", selected_category=selected_category, retVal=retVal)

@app.route("/orders")
@login_required
def orders():
    cursor = mysql.connection.cursor()
    cursor.execute(f"""SELECT first_name, last_name,orderid,cost,order_Time,payment_method_used  
                        FROM store_order, customer
                        WHERE customer.id = store_order.customerid AND store_order.customerid = %(current_user_userid)s""", {'current_user_userid': current_user.userid})
    retVal = cursor.fetchall()
    cursor.execute(f""" SELECT COUNT(*)
                        FROM store_order
                        WHERE store_order.customerid = %(current_user_userid)s""", {'current_user_userid': current_user.userid})
                        
    numOrders = cursor.fetchone()
    cursor.close()
    return render_template('orderHistory.jinja2', orders = retVal, Ordercount = numOrders)

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if request.method == "POST":
        if request.form['submitbutton'] == "name":
            return redirect(url_for("name"))
        elif request.form['submitbutton'] == "password":
            return redirect(url_for("password"))
        elif request.form['submitbutton'] == "email":
            return redirect(url_for("email"))
        elif request.form['submitbutton'] == "address":
            return redirect(url_for("address"))
        elif request.form['submitbutton'] == "payment_methods":
            return redirect(url_for("payment_methods"))
        elif request.form['submitbutton'] == "home":
            return redirect(url_for("home"))
        elif request.form['submitbutton'] == "delete_account":
            return redirect(url_for("delete_account"))

    house_number = str(current_user.house_number)
    return render_template('account.jinja2', user = current_user, house_number = house_number, payment_methods = current_user.payment_methods)
    
@app.route('/name', methods=['GET', 'POST'])
@login_required
def name():
    form = CustomerNameForm()

    if form.validate_on_submit():
        db_connection = mysql.connection
        db_cursor = db_connection.cursor()
        
        if form.first_name.data != None and form.first_name.data != '':
            db_cursor.execute(f'''
                                    UPDATE customer 
                                    SET first_name = %(form_first_name_data)s 
                                    WHERE id = %(current_user_userid)s
                               ''', {'current_user_userid': current_user.userid, 'form_first_name_data': form.first_name.data})
        
        if form.last_name.data != None and form.last_name.data != '':
            db_cursor.execute(f'''
                                    UPDATE customer 
                                    SET last_name = %(form_last_name_data)s 
                                    WHERE id = %(current_user_userid)s
                               ''', {'current_user_userid': current_user.userid, 'form_last_name_data': form.last_name.data})

        db_connection.commit()
        db_cursor.close()
        flash("Changes saved!")
        return redirect(url_for("account"))

    return render_template('name.jinja2', form = form)

@app.route('/password', methods=['GET', 'POST'])
@login_required
def password():
    form = PasswordForm()

    if form.validate_on_submit():
        db_connection = mysql.connection
        db_cursor = db_connection.cursor()
        
        if form.user_password.data != None and form.user_password.data != '' and form.user_password.data == form.confirm_user_password.data:
            hashedpw = generate_password_hash(form.user_password.data, method='sha256')
            db_cursor.execute(f'''
                                    UPDATE user 
                                    SET user_password = "{hashedpw}"
                                    WHERE userid = %(current_user_userid)s
                               ''', {'current_user_userid': current_user.userid})

        db_connection.commit()
        db_cursor.close()
        flash("Changes saved!")
        return redirect(url_for("account"))

    return render_template('password.jinja2', form = form)

@app.route('/email', methods=['GET', 'POST'])
@login_required
def email():
    form = EmailForm()

    if form.validate_on_submit():
        db_connection = mysql.connection
        db_cursor = db_connection.cursor()
        
        if form.email.data != None and form.email.data != '':
            db_cursor.execute(f'''
                                    UPDATE user 
                                    SET email = %(form_email_data)s
                                    WHERE userid = %(current_user_userid)s
                               ''', {'form_email_data': form.email.data, 'current_user_userid': current_user.userid})

            db_connection.commit()
            db_cursor.close()
        flash("Changes saved!")
        return redirect(url_for("account"))

    return render_template('email.jinja2', form = form)

@app.route('/address', methods=['GET', 'POST'])
@login_required
def address():
    form = AddressForm()

    if form.validate_on_submit():
        db_connection = mysql.connection
        db_cursor = db_connection.cursor()

        for field in form:
            if field.name != 'submit' and field.name != 'csrf_token' and field.data != None and field.data != '':
                db_cursor.execute(f'''
                                        UPDATE user
                                        SET {field.name} = %(field_data)s
                                        WHERE userid = %(userid)s
                                  ''', {'field_data': field.data, 'userid': current_user.userid})

        db_connection.commit()
        db_cursor.close()
        flash("Changes saved!")
        return redirect(url_for("account"))

    return render_template('address.jinja2', form = form)

@app.route('/payment_methods', methods=['GET', 'POST'])
@login_required
def payment_methods():
    form = PaymentMethodForm()
    
    # get the current user's payment methods
    db_connection = mysql.connection
    db_cursor = db_connection.cursor()
    payment_methods = current_user.payment_methods

    # the user adds a payment method
    if form.validate_on_submit():
        if form.add_payment_method.data != None and form.add_payment_method.data != 'Choose a payment method':
            db_cursor.execute(f'''
                                    INSERT IGNORE INTO customer_payment_method
                                    VALUES (%(current_user_userid)s, "{form.add_payment_method.data}")
                               ''', {'current_user_userid': current_user.userid})

        db_connection.commit()
        db_cursor.close()
        flash("Changes saved!")
        return redirect(url_for("account"))
    
    # the user deletes a payment method
    elif request.method == "POST":
        for method in payment_methods:
            if f"delete_{method[0]}" in request.form and len(payment_methods) > 1:
                db_connection = mysql.connection
                db_cursor = db_connection.cursor()

                db_cursor.execute(f''' 
                                        DELETE FROM customer_payment_method
                                        WHERE customerid = %(current_user_userid)s AND payment_method = "{method[0]}"
                                   ''', {'current_user_userid': current_user.userid})

                db_connection.commit()
                db_cursor.close()
                return redirect(url_for("payment_methods"))

    db_cursor.close()
    return render_template('payment_method.jinja2', form = form, payment_methods = current_user.payment_methods)

@app.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
    if request.method == "POST":
        if request.form['submitbutton'] == "delete_account":
            current_user_id = current_user.userid
            logout_user()
            db_connection = mysql.connection
            db_cursor = db_connection.cursor()

            db_cursor.execute(f'''
                                    DELETE FROM user
                                    WHERE userid = %(parameterId)s
                               ''', {'parameterId': current_user_id})

            db_connection.commit()
            db_cursor.close()
            return redirect(url_for("account_deleted"))
        elif request.form['submitbutton'] == "back_to_account":
            return redirect(url_for("account"))

    return render_template('delete_account.jinja2')

@app.route("/account_deleted")
def account_deleted():
    return render_template("account_deleted.jinja2", user=current_user)

@app.before_request
def initNavBar():
    topbar = Navbar(View("Home", "home"))
    nav.register_element('topbar', topbar)

    if (not current_user.is_authenticated):
        topbar.items.append(View("Login", "login"))
        topbar.items.append(View("Sign Up", "signup"))
    else:
        cursor = mysql.connection.cursor()
        cursor.execute(f"""SELECT SUM(quantity) AS total_items FROM product_in_shopping_cart WHERE customerid=%(current_user_userid)s""", {'current_user_userid': current_user.userid})
        shopping_cart_items_count = cursor.fetchall()[0][0]

        cursor.execute('''SELECT category_name FROM category''')
        retVal = cursor.fetchall()
        cursor.close()
        #topbar.items.append(View("Hello", "home"))
        items = []
        items.append(View("Overview", "categories"))
        items.append(View("All", "goToCategory", selected_category = "All"))
        for i in retVal:
            j = ''.join(i)  # to get the string
            items.append(View(j, "goToCategory", selected_category = j))
        topbar.items.append(Subgroup("Categories", *items))

        topbar.items.append(View(f"Shopping Cart{'' if not shopping_cart_items_count or int(shopping_cart_items_count) <= 0 else f' ({shopping_cart_items_count})'}", "shopping_cart"))
        topbar.items.append(View("Order History", "orders"))


        topbar.items.append(Text("Logged in as " + current_user.userid))
        topbar.items.append(View("Logout", "logout"))
        topbar.items.append(View("My Account", "account"))
    
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
