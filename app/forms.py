from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from flask_wtf import Form
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Required, Length, Email, Regexp, EqualTo
from flask_pagedown.fields import PageDownField
import pymongo 


class LoginForm(Form):
    """Login form to access writing and settings pages"""

    email = StringField('email', validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired()])


class RegisterationForm(Form):
  username = StringField('User Name', validators=[DataRequired()])
  
  password = PasswordField('Password', validators=[
        Required(), EqualTo('password2', message='password is not equal to the confirmation.')])

  password2 = PasswordField('Confirmation Password', validators=[Required()])

  email = StringField('Email', validators=[Required(), Length(1, 64),
                                          Email()])

  about_me = TextAreaField('Self - Introduction')
  #about_me = TextAreaField('Self - Introduction')

  submit = SubmitField('submit') 

class EditProfileForm(Form):
    username = StringField('User Name', validators=[DataRequired()])
    about_me = TextAreaField('Self Introduction')
    submit = SubmitField('submit')

class PostForm(Form):
    body = PageDownField('Say somthing.', validators=[Required()])
    submit = SubmitField('Post')


class testForm(Form):
    submit = SubmitField('submit') 