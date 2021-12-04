# forms.py

from werkzeug.utils import validate_arguments
from flask_wtf import Form
from wtforms import TextField
from wtforms import SelectField
from wtforms.fields.html5 import EmailField
from wtforms import IntegerField
from wtforms import DecimalField
from wtforms import StringField
from wtforms import PasswordField
from wtforms.validators import DataRequired, EqualTo
from app.models import Category

class SignupForm(Form):
    name = TextField('name', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    password_hash = PasswordField('password_hash', validators=[DataRequired(), EqualTo('password_hash2')])
    password_hash2 = PasswordField('password_hash2', validators=[DataRequired()])

class LoginForm(Form):
    email = EmailField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class ChangePasswordForm(Form):
    old_password = PasswordField('old_password', validators=[DataRequired()])
    new_password_hash = PasswordField('new_password_hash', validators=[DataRequired(), EqualTo('new_password_hash2')])
    new_password_hash2 = PasswordField('new_password_hash2', validators=[DataRequired()])

class BookForm(Form):
    title = TextField('title', validators=[DataRequired()])
    author = TextField('author', validators=[DataRequired()])
    photo = StringField('photo', validators=[DataRequired()])
    cats = Category.query.all()
    category_names = []
    for cat in cats:
        category_names.append(cat.name)
    category = SelectField('category', choices=category_names, validators=[DataRequired()])
    stock = IntegerField('stock', validators=[DataRequired()])
    price = DecimalField('price', validators=[DataRequired()])

class BasketForm(Form):
    id = IntegerField('id', validators=[DataRequired()])
    action = TextField('title', validators=[DataRequired()])

class CategoryForm(Form):
    id = IntegerField('id', validators=[DataRequired()])

class SearchForm(Form):
    title = TextField('title', validators=[DataRequired()])
