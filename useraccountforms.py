from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SubmitField, BooleanField, TextField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, Email, EqualTo, Optional

class CustomerAccountForm(FlaskForm):
    first_name = StringField('First Name', validators=[Length(min=1, max=100), Optional()])
    last_name = StringField('Last Name', validators=[Length(min=1, max=100), Optional()])
    user_password = PasswordField('Password', validators=[Length(min=1, max=100), Optional()])
    confirm_user_password = PasswordField('Confirm Password', validators=[Length(min=1, max=100), EqualTo('password'), Optional()])
    house_number = IntegerField('House Number', validators=[NumberRange(min=0), Optional()])
    street_name = StringField('Street Name', validators=[Length(min=1, max=100), Optional()])
    city = StringField('City', validators=[Length(min=1, max=100), Optional()])
    province = StringField('Province', validators=[Length(min=1, max=100), Optional()])
    postal_code = StringField('Postal Code', validators=[Length(min=1, max=20), Optional()])
    email = StringField('Email', validators=[Email(), Optional()])
    submit = SubmitField('Save Changes')

class SellerAccountForm(FlaskForm):
    company_name = StringField('Company Name', validators=[Length(min=1, max=100), Optional()])
    user_password = PasswordField('Password', validators=[Length(min=1, max=100), Optional()])
    confirm_user_password = PasswordField('Confirm Password', validators=[Length(min=1, max=100), EqualTo('password'), Optional()])
    house_number = IntegerField('House Number', validators=[NumberRange(min=0), Optional()])
    street_name = StringField('Street Name', validators=[Length(min=1, max=100), Optional()])
    city = StringField('City', validators=[Length(min=1, max=100), Optional()])
    province = StringField('Province', validators=[Length(min=1, max=100), Optional()])
    postal_code = StringField('Postal Code', validators=[Length(min=1, max=20), Optional()])
    email = StringField('Email', validators=[Email(), Optional()])
    submit = SubmitField('Save Changes')

