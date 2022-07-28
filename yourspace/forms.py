from flask_wtf import FlaskForm
from yourspace.models import User
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField


# New User Registration
class RegistrationForm(FlaskForm):
    #validate length and DataRequired = not-nullable, regexp for alphanumeric
    username = StringField('Username', validators=[DataRequired(), Length(min=7, max=20), Regexp('^[\w-]+$', message='Alphanumeric characters only (excluding underscore and dash).')]) 
    email  = StringField('Email', validators=[DataRequired(), Email()])
    password  = PasswordField('Password', validators=[DataRequired(), Length(min=7, max=20)])
    confirm_password  = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=7, max=20), EqualTo('password')])
    submit = SubmitField('Register')
    
    # Errorhandling for duplicate usernames
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username unavailable.')
        
        # Errorhandling for duplicate emails
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email.')
    
# Returning User Login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=7, max=20)])
    password  = PasswordField('Password', validators=[DataRequired(), Length(min=7, max=20)])
    remember = BooleanField('Remember Me?')
    submit = SubmitField('Login')
    
# Posting
class PostForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
    
# Contact Message
class MessageForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired(),Length(max=500)])
