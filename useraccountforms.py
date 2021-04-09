from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SubmitField, BooleanField, TextField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, Email, EqualTo, Optional

class CustomerNameForm(FlaskForm):
    first_name = StringField('First Name', validators=[Length(min=1, max=100), Optional()])
    last_name = StringField('Last Name', validators=[Length(min=1, max=100), Optional()])
    submit = SubmitField('Save Changes')

class SellerCompanyNameForm(FlaskForm):
    company_name = StringField('Company Name', validators=[Length(min=1, max=100), Optional()])
    submit = SubmitField('Save Changes')

class PasswordForm(FlaskForm):
    user_password = PasswordField('Password', validators=[Length(min=1, max=100), Optional()])
    confirm_user_password = PasswordField('Confirm Password', validators=[Length(min=1, max=100), EqualTo('user_password'), Optional()])
    submit = SubmitField('Save Changes')

class EmailForm(FlaskForm):
    email = StringField('Email', validators=[Email(), Optional()])
    submit = SubmitField('Save Changes')

class AddressForm(FlaskForm):
    house_number = IntegerField('House Number', validators=[NumberRange(min=0), Optional()])
    street_name = StringField('Street Name', validators=[Length(min=1, max=100), Optional()])
    city = StringField('City', validators=[Length(min=1, max=100), Optional()])
    province = SelectField(u'Province', 
                           choices=[(''), ('AB'), ('BC'), ('MB'), ('NB'), ('NL'), ('NT'), ('NS'), ('NU'), ('ON'), ('PE'), ('QC'), ('SK'), ('YT')], 
                           validators=[Optional()])
    postal_code = StringField('Postal Code', validators=[Length(min=1, max=20), Optional()])
    submit = SubmitField('Save Changes')

class PaymentMethodForm(FlaskForm):
    delete_payment_method = StringField('Payment Methods')
    add_payment_method = SelectField(u'Add Payment Method', choices=[(''), ('Credit Card'), ('Debit Card'), ('PayPal')], validators=[Optional()])
    submit = SubmitField('Add')



