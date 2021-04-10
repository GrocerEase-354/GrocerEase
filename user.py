from flask_login import UserMixin
from flask_mysqldb import MySQL

mysql = MySQL()

class User(UserMixin):
    def __init__(
        self,
        userid,
        password,
        house_number,
        street_name,
        postal_code,
        province,
        city,
        email,
        fname,
        lname,
        payment_methods):

        self.userid = userid
        self.password = password
        self.house_number = house_number
        self.street_name = street_name
        self.postal_code = postal_code
        self.province = province
        self.city = city
        self.email = email
        self.fname = fname
        self.lname = lname
        self.payment_methods = payment_methods

    def to_tuple(self):
        return (
            self.userid, 
            self.password, 
            self.house_number,
            self.street_name,
            self.postal_code,
            self.province,
            self.city,
            self.email,
            self.fname,
            self.lname,
            self.payment_methods)

    def to_dict(self):
        return self.__dict__

    def get_id(self):
        return self.userid

def create_user(user_id):
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
    print("here")
    name = cursor.fetchall()[0]
    fn, ln = name[0], name[1]
    cursor.execute(
        f"""SELECT payment_method
        FROM customer_payment_method
        WHERE customerid='{user_id}'""")
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