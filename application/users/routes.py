import readtime
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import func

from application import db, bcrypt
from application.models import User, Post, Tag, Comment
from application.posts.utils import listToString
from application.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm)
from application.users.utils import save_picture, truncate_html

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()

    subquery = db.session.query(Comment.post_id, func.count(Comment.post_id).label('count'))\
        .group_by(Comment.post_id)\
        .subquery()

    results = db.session.query(Post, subquery.c.count)\
        .filter_by(author=user)\
        .outerjoin(subquery, subquery.c.post_id == Post.id)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)

    for result in results.items:
        reading_time = readtime.of_html(result[0].content)
        result[0].reading_time = reading_time
        result[0].truncated_content = truncate_html(result[0].content, 500)
        tags = listToString(Tag.query.filter_by(post_id=result[0].id).all()).split(",")
        result[0].tags_list = tags

    return render_template('user_posts.html', results=results, user=user, reading_time=reading_time, tags=tags)
