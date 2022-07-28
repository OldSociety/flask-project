from flask import abort
from yourspace import db, login_manager, admin
from sqlalchemy.orm import validates
from flask_login import UserMixin
from flask_login.utils import current_user
from datetime import datetime
from flask_admin.contrib.sqla import ModelView


# Reload returning user from user id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# UserMixin provides implimentation of authentication, activity, anonymity and unique id for Flask-Login
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True) #One to Many Relationship with Post table
    is_admin = db.Column(db.Boolean, unique=False, default=False)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    @validates('content')
    def validates_username(self, key, value):
        if self.content and self.content != value:  # Field already exists
            raise ValueError('Content cannot be modified.')
        return value
    
    def __repr__(self):
        return f"Post('{self.content}', '{self.date_posted}')"
    
class MyAdminView(ModelView):
    def is_accessible(self):
        if current_user.is_anonymous:
            return abort(404)
        elif current_user.is_admin == True or current_user.username == 'administrator':
            return current_user.is_authenticated
        else:
            return abort(404)
    def not_auth(self):
        return abort(404)

admin.add_view(MyAdminView(User, db.session))
admin.add_view(MyAdminView(Post, db.session))
