from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from flask_wtf import Form
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Required, Length, Email, Regexp, EqualTo
import pymongo 


class LoginForm(Form):
    """Login form to access writing and settings pages"""

    username = StringField('Username', validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired()])


class RegisterationForm(Form):
  username = StringField('User Name', validators=[DataRequired()])
  
  password = PasswordField('Password', validators=[
        Required(), EqualTo('password2', message='password is not equal to the confirmation.')])

  password2 = PasswordField('Confirmation Password', validators=[Required()])

  email = StringField('Email', validators=[Required(), Length(1, 64),
                                          Email()])
  #about_me = TextAreaField('Self - Introduction')

  submit = SubmitField('submit') 