# models.py

from typing import overload
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from app import db

# many-to-many association with additional columns
class Association(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    movieId = db.Column(db.Integer, db.ForeignKey('movie.id'))
    rating = db.Column(db.Integer, default=-1)
    watched = db.Column(db.Boolean, default=False)
    user = db.relationship('User', back_populates='movies')
    movie = db.relationship('Movie', back_populates='users')

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    movies = db.relationship('Association', back_populates='user')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    photo = db.Column(db.String(500)) # .jpg
    year = db.Column(db.Integer)
    description = db.Column(db.String(2000))
    users = db.relationship('Association', back_populates='movie')
