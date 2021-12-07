# __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging

logging.basicConfig(level=logging.DEBUG, filename='logs.txt', 
format='[%(asctime)s]:%(levelname)s:%(name)s:%(message)s')

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

migrate = Migrate(app, db, render_as_batch=True)

from app import views, models
