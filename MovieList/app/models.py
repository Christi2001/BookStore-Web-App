# # models.py

# from werkzeug.security import check_password_hash, generate_password_hash
# from flask_login import UserMixin
# from app import db

# watchedMovie = db.Table('watchedMovie', db.Model.metadata,
#     db.Column('id', db.Integer, primary_key=True),
#     db.Column('userId', db.Integer, db.ForeignKey('user.id')),
#     db.Column('movieId', db.Integer, db.ForeignKey('movie.id')),
#     db.Column('userRating', db.Integer)
# )

# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(300), nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password_hash = db.Column(db.String(128), nullable=False)
#     movies = db.relationship('Movie', secondary=watchedMovie, backref='user')

#     @property
#     def password(self):
#         raise AttributeError('password is not a readable attribute!')
    
#     @password.setter
#     def password(self, password):
#         self.password_hash = generate_password_hash(password)
    
#     def verify_password(self, password):
#         return check_password_hash(self.password_hash, password)

# class Movie(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     photo = db.Column(db.String(500))
#     title = db.Column(db.String(300), nullable=False)
#     year = db.Column(db.Integer)
#     description = db.Column(db.String(2000))
#     users = db.relationship('User', secondary=watchedMovie, backref='movie')

from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
