from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from application import db
from application.models import Comment, Post
from application.comments.forms import CommentForm

comments = Blueprint('comments', __name__)


@comments.route("/post/<int:post_id>/comments", methods=['GET', 'POST'])
@login_required
def new_comment(post_id):
    form = CommentForm()
    if request.method == 'POST':
        print(form.is_submitted(), form.validate())
        if form.validate_on_submit():
            comment = Comment(content=form.content.data, author=current_user, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            flash('Your comment has been added!', 'success')
        else:
            flash('Your comment has not been added!', 'error')
            return redirect(url_for('posts.post', post_id=post_id))

    return redirect(url_for('posts.post', post_id=post_id))
