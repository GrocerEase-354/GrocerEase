from flask import Flask
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"] = 'root'
app.config["MYSQL_DB"] = 'project354'

@app.route("/")
def test():
    return "<h1>In test</h1>"

mysql = MySQL(app)

#home page
@app.route("/home")
def home():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM user''')
    rv = cur.fetchall()
    return f"<h1>Hello</h1><p>{str(rv)}</p>"

#register page

@app.route("/register")
def about():
    return "<h1>Registration</h1>"

#enable debugging
if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=5000)
