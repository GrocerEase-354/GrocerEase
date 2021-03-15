from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'cmpt354'




mysql = MySQL(app)

@app.route("/")
def defaultFunction():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM category''')
    retVal = cursor.fetchall()
    cursor.close()

    return f"<h1>Category</h1><p>{str(retVal)}</p>"


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
