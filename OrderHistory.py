from flask import Flask,render_template
from flaskext.mysql import MySQL
import sys

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'cmpt354'


mysql = MySQL() 
mysql.init_app(app)
#Add parameter to check what user is accessing the page to only fetch their records
@app.route("/Orders")
def Orders():
    cursor = mysql.get_db().cursor()
    cursor.execute('''SELECT first_name, last_name,orderid,product_name,cost,order_Time,payment_method_used  FROM store_order, customer,product WHERE customer.id = store_order.customerid AND store_order.cost = product.price''')
    retVal = cursor.fetchall()
    cursor.close()
    return render_template('OrderHistory.html',orders = retVal)


if __name__ == "__main__":
    app.run(debug = True)

