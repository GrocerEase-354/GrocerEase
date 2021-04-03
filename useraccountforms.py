from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SubmitField, BooleanField, TextField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, Email, EqualTo

class CustomerAccountForm(FlaskForm):
    first_name = StringField('First Name', validators=[Length(min=1, max=100)])
    last_name = StringField('Last Name', validators=[Length(min=1, max=100)])
    password = PasswordField('Password', validators=[Length(min=1, max=100)])
    confirm_password = PasswordField('Confirm Password', validators=[Length(min=1, max=100), EqualTo('password')])
    house_number = IntegerField('House Number', validators=[NumberRange(min=0)])
    street_name = StringField('Street Name', validators=[Length(min=1, max=100)])
    city = StringField('City', validators=[Length(min=1, max=100)])
    province = StringField('Province', validators=[Length(min=1, max=100)])
    postal_code = StringField('Postal Code', validators=[Length(min=1, max=20)])
    country = StringField('Country', validators=[Length(min=1, max=100)])
    email = StringField('Email', validators=[Email()])
    submit = SubmitField('Save Changes')

class SellerAccountForm(FlaskForm):
    company = StringField('Company Name', validators=[Length(min=1, max=100)])
    password = PasswordField('Password', validators=[Length(min=1, max=100)])
    confirm_password = PasswordField('Confirm Password', validators=[Length(min=1, max=100), EqualTo('password')])
    house_number = IntegerField('House Number', validators=[NumberRange(min=0)])
    street_name = StringField('Street Name', validators=[Length(min=1, max=100)])
    city = StringField('City', validators=[Length(min=1, max=100)])
    province = StringField('Province', validators=[Length(min=1, max=100)])
    postal_code = StringField('Postal Code', validators=[Length(min=1, max=20)])
    country = StringField('Country', validators=[Length(min=1, max=100)])
    email = StringField('Email', validators=[Email()])
    submit = SubmitField('Save Changes')

