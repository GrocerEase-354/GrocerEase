from flask import Flask, render_template, url_for, flash, redirect, request
from useraccountforms import CustomerAccountForm, SellerAccountForm
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_HOST'] = '10.0.2.2'
app.config['MYSQL_DB'] = 'cmpt354'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
@app.route('/account', methods=['GET', 'POST'])
def account():
    form = CustomerAccountForm()

    if form.validate_on_submit():
        db_connection = mysql.connection
        db_cursor = db_connection.cursor()
        
        for field in form:
            if field.data != None:
                if field.name == 'first_name' or field.name == 'last_name':
                    query = "UPDATE customer SET %s = %s WHERE id = 'H123'"
                elif field.name == 'house_number':
                    query = "UPDATE user SET %s = %d WHERE id = 'H123'"
                else:
                    query = "UPDATE user SET %s = %s WHERE id = 'H123'"
                
                cursor2.execute(f'''SELECT * FROM product WHERE category_name = "{str(j)}"''')
                data = (field.name, field.data)

                db_cursor.execute(query, data)
                db_connection.commit()
                db_cursor.close()

                flash(f'Changes saved!', 'success')
    return render_template('account.html', title='Account', form=form)

if __name__ == '__main__':
    app.run(debug=True)
        







