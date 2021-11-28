# models.py

# from flask_login import UserMixin
# from . import db

# watchedMovie = db.Table('watchedMovie', db.Model.metadata,
#     db.Column('userId', db.Integer, db.ForeignKey('user.userId')),
#     db.Column('movieId', db.Integer, db.ForeignKey('movie.movieId')),
#     db.Column('userRating', db.Integer)
# )

# class User(UserMixin, db.Model):
#     userId = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
#     email = db.Column(db.String(100), index=True, unique=True)
#     password = db.Column(db.String(100), index=True)
#     name = db.Column(db.String(300), index=True)
#     movies = db.relationship('Movie', secondary=watchedMovie)

# class Movie(db.Model):
#     movieId = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(300), index=True, nullable=False)
#     year = db.Column(db.Integer, index=True)
#     description = db.Column(db.String(2000), index=True)
#     users = db.relationship('User', secondary=watchedMovie, overlaps="movies")


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
