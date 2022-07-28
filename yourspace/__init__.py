from flask import Flask
from flask_login import LoginManager, LoginManager
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = 'f4c942ccae311bf497904370dacd6c0c'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #suppress modification error
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(basedir, "posts.db")
bcrypt = Bcrypt(app) # encrypt/decrypt hashpasswords
login_manager = LoginManager(app)
login_manager.login_view = 'login' #login route
login_manager.login_message_category = 'info' #Bootstrap color for login messages
db = SQLAlchemy(app)
admin = Admin(app)


# prevent circular calls by placing this below
from yourspace import routes