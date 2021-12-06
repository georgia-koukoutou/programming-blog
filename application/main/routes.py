from flask import render_template, request, Blueprint
from sqlalchemy import func

from application.models import Post, Comment
from application import db

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    subquery = db.session.query(Comment.post_id, func.count(Comment.post_id).label('count')).group_by(Comment.post_id).subquery()
    results = db.session.query(Post, subquery.c.count).outerjoin(subquery, subquery.c.post_id == Post.id).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)

    most_viewed_post = Post.query.order_by(Post.views.desc()).first()

    return render_template('home.html', results=results, most_viewed_post=most_viewed_post)


@main.route("/about")
def about():
    return render_template('about.html', title='About')
