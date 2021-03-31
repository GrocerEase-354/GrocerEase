from flask import Flask, render_template, request, session, url_for, redirect
from flask_mysqldb import MySQL
import sys

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'cmpt354'

mysql = MySQL(app)

@app.route("/category/<selected_category>", methods=['GET', 'POST'])
def goToCategory(selected_category):
    actualSelectedCategory = selected_category.lower()
    if (actualSelectedCategory == "all"):
        actualSelectedCategory = "%"
    cursor = mysql.connection.cursor()
    productsToSelect = "product_name, price, sellerid, product_description, category_name, best_before_date"
    cursor.execute(f'''SELECT {productsToSelect} FROM product WHERE LOWER(category_name) LIKE "{actualSelectedCategory}";''')
    retVal = cursor.fetchall()
    cursor.close()
    table = []
    '''for i in retVal:
        temp = []
        #print(i, file=sys.stderr)
        for j in i:
            #print(j)
            '''

    if (request.method == "POST"):
        if (request.form['submitbutton'] == "home"):
            return redirect(url_for("home"))
    else:      
        return render_template("category.html", selected_category=selected_category, retVal=retVal)


@app.route("/", methods=['GET', 'POST'])
def home():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT category_name FROM category''')
    retVal = cursor.fetchall()
    cursor.close()
    if request.method == "POST":
        #print("In POST", file=sys.stderr)
        # for all button clicks, we are running go to category. We can potentially change this by changing the request form name
        return redirect(url_for("goToCategory", selected_category = request.form['submitbutton']))
        #print(request.form.get('submitbutton'))
        '''for i in retVal:
            for j in i:
                if (request.form['submitbutton'] == str(j)):
                    return redirect(url_for("goToCategory", selected_category = str(j)))'''

    
    return render_template('home.html', retVal = retVal)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)