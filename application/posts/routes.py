import json

import readtime
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from sqlalchemy import func

from application import db
from application.models import Post, Comment, User, Vote, Tag
from application.posts.forms import PostForm
from application.comments.forms import CommentForm
from application.posts.utils import listToString, stringToTagList
from application.users.utils import truncate_html

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        tag_list = stringToTagList(form.tags.data)
        print(tag_list)
        post = Post(title=form.title.data, content=form.content.data, author=current_user, tags=tag_list)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    user = current_user
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    comment = Comment.query.filter_by(post_id=post_id).all()
    comment_count = Comment.query.filter_by(post_id=post.id).count()
    reading_time = readtime.of_html(post.content)

    post.views += 1
    db.session.commit()

    post_likes = Vote.query.filter_by(status=1, post_id=post_id).count()
    post_dislikes = Vote.query.filter_by(status=0, post_id=post_id).count()

    tags = listToString(Tag.query.filter_by(post_id=post_id).all()).split(",")

    if current_user.is_authenticated:
        vote = Vote.query.filter_by(user_id=user.id, post_id=post_id).first()
        return render_template('post.html', vote=vote, title=post.title, post=post, form=form, comment=comment, comment_count=comment_count, reading_time=reading_time, post_likes=post_likes, post_dislikes=post_dislikes, tags=tags)
    else:
        return render_template('post.html', title=post.title, post=post, form=form, comment=comment, comment_count=comment_count, reading_time=reading_time, post_likes=post_likes, post_dislikes=post_dislikes, tags=tags)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        # delete existing post's tags
        Tag.query.filter(Tag.post_id == post_id).delete()
        post.title = form.title.data
        post.content = form.content.data
        # add any tags from form
        post.tags = stringToTagList(form.tags.data)
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        tag_list = post.tags
        tags = listToString(tag_list)
        form.title.data = post.title
        form.content.data = post.content
        form.tags.data = tags
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


@posts.route("/post/<int:post_id>/vote", methods=['POST'])
@login_required
def vote_post(post_id):

    bodyJson = request.get_data()
    body = json.loads(bodyJson)
    response = body['status']
    user = current_user
    exists = Vote.query.filter_by(user_id=user.id, post_id=post_id).first()

    if exists is None:
        new_vote = Vote(status=response, user_id=user.id, post_id=post_id)
        db.session.add(new_vote)
        db.session.commit()
    else:
        if exists.status is True:
            if response is True:
                vote = Vote.query.filter_by(user_id=user.id, post_id=post_id).first()
                db.session.delete(vote)
                db.session.commit()
            else:
                vote = Vote.query.filter_by(user_id=user.id, post_id=post_id).first()
                new_vote = Vote(status=response, user_id=user.id, post_id=post_id)
                db.session.delete(vote)
                db.session.add(new_vote)
                db.session.commit()
        else:
            if response is True:
                vote = Vote.query.filter_by(user_id=user.id, post_id=post_id).first()
                new_vote = Vote(status=response, user_id=user.id, post_id=post_id)
                db.session.delete(vote)
                db.session.add(new_vote)
                db.session.commit()
            else:
                vote = Vote.query.filter_by(user_id=user.id, post_id=post_id).first()
                db.session.delete(vote)
                db.session.commit()

    return {"message": "OK"}, 200


@posts.route("/post/tag/<content>")
def tagged_posts(content):

    page = request.args.get('page', 1, type=int)

    subquery = db.session.query(Comment.post_id, func.count(Comment.post_id).label('count')).group_by(
        Comment.post_id).subquery()
    results = db.session.query(Post, subquery.c.count).outerjoin(subquery, subquery.c.post_id == Post.id).join(
        Tag).filter(Tag.content == content).order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)

    for result in results.items:
        reading_time = readtime.of_html(result[0].content)
        result[0].reading_time = reading_time
        result[0].truncated_content = truncate_html(result[0].content, 500)
        tags = listToString(Tag.query.filter_by(post_id=result[0].id).all()).split(",")
        result[0].tags_list = tags


    return render_template('tagged_posts.html', results=results, reading_time=reading_time, tags=tags)


@posts.route("/post/<int:post_id>/counters")
def count_votes(post_id):

    post_likes = Vote.query.filter_by(status=1, post_id=post_id).count()
    post_dislikes = Vote.query.filter_by(status=0, post_id=post_id).count()

    return {"likes": post_likes, "dislikes": post_dislikes}, 200
