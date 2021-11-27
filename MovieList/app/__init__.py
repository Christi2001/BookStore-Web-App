# __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = LoginManager()
# login_manager.login_view = 'auth.login'
# login_manager.init_app(app) # not working ?????

migrate = Migrate(app, db)

from app import views, models
