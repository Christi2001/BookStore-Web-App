# models.py

from typing import overload
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from app import db

# many-to-many association
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    bookId = db.Column(db.Integer, db.ForeignKey('book.id'))
    user = db.relationship('User', back_populates='books')
    book = db.relationship('Book', back_populates='users')

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    books = db.relationship('Order', back_populates='user')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    author = db.Column(db.String(300), nullable=False)
    photo = db.Column(db.String(500)) # .jpg
    category = db.Column(db.String(200))
    stock = db.Column(db.Integer)
    price = db.Column(db.Float, nullable=False)
    users = db.relationship('Order', back_populates='book')
