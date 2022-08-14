from wsgiref.validate import validator
from flask import Flask
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError, Regexp, EqualTo
from wtforms import StringField, PasswordField, SubmitField, SelectField
from shop.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Regexp('^[a-zA-Z0-9]{5,20}$',message='Your username should be between 5 and 20 characters long, and can only contain letters and numbers')])
    password = PasswordField('Password', validators=[DataRequired(), Regexp('^[a-zA-Z0-9]{5,20}$',message='Your password should be between 5 and 20 characters long, and can only contain letters and numbers'), EqualTo('confirm_password', message='Passwords do not match. Try again')])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Register')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exists. Please choose a different one')

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class CheckoutForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired()])
    card_no = StringField('Card Number', validators = [DataRequired(), Regexp('^[0-9]{16}$',message='You must enter a 16-digit number')])
    submit = SubmitField('Pay')

class SortGalleryForm(FlaskForm):
    sort_type=SelectField("Sort by",
choices=[("none", "No filter"),("price_high", "High price"),
 ("price_low", "Low price"), ("ecological", "Ecological Impact (low to high)")],
 default="none",
 render_kw={"onchange": "this.form.submit()"})
