from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SubmitField, BooleanField, TextField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, Email, EqualTo, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=1, max=20)])
    password = PasswordField('Password', validators=[Length(min=1, max=100)])

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=1, max=20)])
    first_name = StringField('First Name', validators=[Length(min=1, max=100)])
    last_name = StringField('Last Name', validators=[Length(min=1, max=100)])
    password = PasswordField('Password', validators=[Length(min=1, max=100)])
    confirm_password = PasswordField('Confirm Password', validators=[Length(min=1, max=100), EqualTo('password')])
    house_number = IntegerField('House Number', validators=[NumberRange(min=0)])
    street_name = StringField('Street Name', validators=[Length(min=1, max=100)])
    city = StringField('City', validators=[Length(min=1, max=100)])
    province = SelectField("Province", choices=[('BC', 'British Columbia'), ('AB', 'Alberta'), ('MN', 'Manitoba')])
    postal_code = StringField('Postal Code', validators=[Length(min=1, max=20)])
    email = StringField('Email', validators=[Email()])
    payment_method = SelectField('Payment Method', choices=[('Credit Card', 'Credit Card'), ('Debit Card', 'Debit Card'), ('PayPal', 'PayPal')])
    submit = SubmitField('Sign up')