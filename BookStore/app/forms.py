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
from app.models import Genre

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
    genres = Genre.query.all()
    genre_choices = []
    for g in genres:
        genre_choices.append(g.name)
    # ['Action and Adventure', 'Anthology', 'Classic', 'Comic and Graphic Novel',
    #                 'Crime and Detective', 'Drama', 'Fable', 'Fairy Tale', 'Fan-Fiction',
    #                 'Fantasy', 'Historical Fiction', 'Horror', 'Humor', 'Legend', 'Magical Realism', 
    #                 'Mystery', 'Mythology', 'Realistic Fiction', 'Romance', 'Satire', 
    #                 'Science Fiction (Sci-Fi)', 'Short Story', 'Suspense/Thriller',
    #                 'Biography/Autobiography', 'Essay', 'Memoir', 'Narrative Nonfiction',
    #                 'Periodicals', 'Reference Books', 'Self-help Book', 'Speech', 'Textbook', 'Poetry']
    genre = SelectField('genre', choices=genre_choices, validators=[DataRequired()])
    stock = IntegerField('stock', validators=[DataRequired()])
    price = DecimalField('price', validators=[DataRequired()])

class BasketForm(Form):
    id = IntegerField('id', validators=[DataRequired()])
    action = TextField('title', validators=[DataRequired()])

class SearchForm(Form):
    title = TextField('title', validators=[DataRequired()])
