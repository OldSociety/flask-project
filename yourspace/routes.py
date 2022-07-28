from flask import redirect, render_template, url_for, flash, request, abort
from yourspace import app, db, bcrypt
from yourspace.forms import RegistrationForm, LoginForm, PostForm, MessageForm
from yourspace.models import User, Post
from datetime import datetime
from flask_login import login_user, logout_user, current_user, login_required

# Left Side Navbar
@app.route('/', methods=['GET', 'POST'])
def home():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    form = PostForm()
    if form.validate_on_submit():
        post = Post(content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(f'Your post has been created.', 'success')
        return redirect(url_for('home'))
    return render_template('home.html', form=form, posts=posts)

@app.route('/about', methods=['GET', 'POST'])
def about():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    form = PostForm()
    if form.validate_on_submit():
        post = Post(content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(f'Your post has been created.', 'success')
        return redirect(url_for('home'))
    return render_template('about.html', title='About', form=form, posts=posts)

# Right Side Navbar - Registration and Login
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Take users string password and hash for security
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Create user from Registration Data
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # Add user to database
        db.session.add(user)
        db.session.commit()
        # Success Message
        return redirect(url_for('login')) #url_for uses "home" name of function
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    # authenticate user
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        # check if username exists in database. If not, return none.
        user = User.query.filter_by(username=form.username.data).first()
        # check form password against unhashed password in database
        if user and bcrypt.check_password_hash(user.password, form.password.data): 
            login_user(user, remember=form.remember.data)
            # send user to page they were trying to reach using request arguments
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login unsuccessful. Please check username and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    form = PostForm()
    return render_template('account.html', title='account', form=form)

# Posting - Update/Delete
# @app.route('/<int:post_id>/update', methods=['Get', 'POST'])
# def update_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     if post.author != current_user:
#         abort(403)
#     form = PostForm()
#     if form.validate_on_submit():
#         post.content = form.content.data
#         post.is_edited = True
#         db.session.commit()
#         return redirect(url_for('home'))
#     elif request.method == 'GET':
#         form.content.data = post.content
#     return redirect(url_for('home'))


# Posting - Delete
@app.route('/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(f'Your post has been deleted.', 'danger')
    return redirect(url_for('home'))

