from flask import Flask
from flask_mysqldb import MySQL
from flask_login import LoginManager

mysql = MySQL()

def create_app():
    app = Flask(__name__)

    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'root'
    app.config['MYSQL_DB'] = 'onlinegrocery'
    app.config['SECRET_KEY'] = 'test'

    mysql.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .user import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        cursor = mysql.connection.cursor()
        # see if user is in DB
        cursor.execute(
            f"""SELECT `user_password`, `house_number`, `street_name`, `postal_code`, `province`, `city`, `email` 
            FROM user 
            WHERE userid='{user_id}'""")
        user = cursor.fetchall()[0]
        pw, hn, sn, pc, pv, c, em = user[0], user[1], user[2], user[3], user[4], user[5], user[6]
        cursor.execute(
            f"""SELECT first_name, last_name 
            FROM customer
            WHERE id='{user_id}'""")
        name = cursor.fetchall()[0]
        fn, ln = name[0], name[1]
        cursor.execute(
            f"""SELECT payment_method
            FROM customer_payment_method
            WHERE customerid='{user_id}'""")
        pm = cursor.fetchall()[0][0]

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
            payment_method=pm
        )

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app