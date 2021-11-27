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


from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
