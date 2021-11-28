# forms.py

from flask_wtf import Form
from wtforms import TextField
from wtforms.fields.html5 import EmailField
# from wtforms import IntegerField
# from wtforms import StringField
from wtforms import PasswordField
from wtforms.validators import DataRequired, EqualTo, Length

class SignupForm(Form):
    name = TextField('name', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    password_hash = PasswordField('password_hash', validators=[DataRequired(), EqualTo('password_hash2')])
    password_hash2 = PasswordField('password_hash2', validators=[DataRequired()])


class LoginForm(Form):
    email = EmailField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
