from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from . import mysql
from flask_login import login_user, logout_user, login_required
from .user import User, create_user

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

#@auth.route('/logout')
#def logout():
#    return render_template('Logout')

@auth.route('/signup', methods=['POST'])
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
    cursor.execute(f"""SELECT * FROM user WHERE userid='{username}'""")
    user = cursor.fetchall()

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash("Username is already in use")
        return redirect(url_for('auth.signup'))
    
    print(request.form)
    print(username, fname, lname, password, email, house_number, street_name, postal_code, province, city, payment_method)

    user_obj = User(
        userid=username,
        password=generate_password_hash(password, method='sha256'),
        house_number=house_number,
        street_name=street_name,
        postal_code=postal_code,
        province=province,
        city=city,
        email=email,
        fname=fname,
        lname=lname,
        payment_method=payment_method
    )

    #session['user'] = user_obj

    # add user to DB
    cursor.execute(f"""INSERT INTO user (`userid`, `user_password`, `house_number`, `street_name`, `postal_code`, `province`, `city`, `email`)
                       VALUES('{username}', '{generate_password_hash(password, method='sha256')}', '{house_number}', '{street_name}', '{postal_code}', '{province}', '{city}', '{email}')""")
    # add customer to DB
    cursor.execute(f"""INSERT INTO customer (id, first_name, last_name)
                       VALUES('{username}', '{fname}', '{lname}')""")
    cursor.execute(f"""INSERT INTO customer_payment_method (customerid, payment_method)
                       VALUES('{username}', '{payment_method}')""")
    mysql.connection.commit()
    cursor.close()

    # code to validate and add user to database goes here
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    cursor = mysql.connection.cursor()
    # see if user is in DB
    cursor.execute(f"""SELECT * FROM user WHERE userid='{username}'""")
    user = cursor.fetchall()
    cursor.close()
    print(user)
    if not user or (not check_password_hash(user[0][1], password) and user[0][1] != password): # if a user is found, we want to redirect back to signup page so user can try again
        flash("Username/Password is invalid")
        return redirect(url_for('auth.login'))
    user2 = create_user(user[0][0])
    print("Jello")
    login_user(user2, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.logged_out"))