from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class CustomerAccountForm(FlaskForm):
    first_name = StringField('First Name', validators=[Length(min=1, max=100)])
    last_name = StringField('Last Name', validators=[])

class SellerAccountForm(FlaskForm):

