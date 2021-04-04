from flask import Flask, render_template, request, session, url_for, redirect
from flask_mysqldb import MySQL
import sys
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *



app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'cmpt354'

mysql = MySQL(app)

topbar = Navbar(View("Home", "home"))

nav = Nav()
nav.register_element('topbar', topbar)
nav.init_app(app)

# creating the nav bar for categories, though first we need the categories
'''extcursor = mysql.connection.cursor()
extcursor.execute("SELECT category_name FROM category")
extretVal = cursor.fetchall()
extcursor.close()'''





@app.route("/category/<selected_category>", methods=['GET', 'POST'])
def goToCategory(selected_category):
    actualSelectedCategory = selected_category.lower()
    if (actualSelectedCategory == "all"):
        actualSelectedCategory = "%"
    cursor = mysql.connection.cursor()
    productsToSelect = "product_name, price, sellerid, product_description, category_name, best_before_date"
    # preventing SQL injection from URL
    cursor.execute(f"SELECT { productsToSelect } FROM product WHERE LOWER(category_name) LIKE %(parameterInput)s", {'parameterInput': actualSelectedCategory})
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
        return render_template("category.jinja2", selected_category=selected_category, retVal=retVal)


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

    
    return render_template('home.jinja2', retVal = retVal)

@app.before_first_request
def initNavBar():

    topbar.items.append(View("All", "goToCategory", selected_category = "All"))

    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT category_name FROM category''')
    retVal = cursor.fetchall()
    cursor.close()
    #topbar.items.append(View("Hello", "home"))
    
    for i in retVal:
        j = ''.join(i)  # to get the string
        topbar.items.append(View(j, "goToCategory", selected_category = j))
    

    

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)