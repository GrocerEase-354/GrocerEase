from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import sys

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'cmpt354'




mysql = MySQL(app)

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM category''')
    retVal = cursor.fetchall()
    cursor.close()
    print("Hello", file=sys.stderr)
    clickValue = "None"
    if request.method == "POST":
        print("In POST", file=sys.stderr)
        #print(request.form.get('submitbutton'))
        for i in retVal:
            for j in i:
                if (request.form['submitbutton'] == str(j)):
                    clickValue = str(j)
                    print(j, file=sys.stderr)
                    return render_template('home.html', homeRetVal = [str(retVal), retVal, clickValue])
    
    return render_template('home.html', homeRetVal = [str(retVal), retVal, clickValue])

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
