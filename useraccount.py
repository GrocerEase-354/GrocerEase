from flask import Flask, render_template, url_for, flash, redirect, request
from useraccountforms import CustomerAccountForm, SellerAccountForm
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_HOST'] = '10.0.2.2'
app.config['MYSQL_DB'] = 'cmpt354'
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
@app.route('/account', methods=['GET', 'POST'])
def account():
    form = CustomerAccountForm()

    if form.validate_on_submit():
        db_connection = mysql.connection
        db_cursor = db_connection.cursor()
        
        for field in form:
            if field.name != 'submit' and field.name != 'csrf_token' and field.data != None and field.data != '':
                if field.name == 'first_name' or field.name == 'last_name':
                    db_cursor.execute('''
                                            UPDATE customer
                                            SET {} = %s
                                            WHERE id = 'H123'
                                      '''.format(field.name) ,
                                      (field.data,))
                else:
                    db_cursor.execute('''
                                            UPDATE user
                                            SET {} = %s
                                            WHERE userid = 'H123'
                                      '''.format(field.name) ,
                                      (field.data,))

                db_connection.commit()
                flash(f'Changes saved!', 'success')
    return render_template('account.html', title='Account', form=form)

if __name__ == '__main__':
    app.run(debug=True)
        







