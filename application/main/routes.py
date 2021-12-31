import readtime
from flask import render_template, request, Blueprint
from sqlalchemy import func, desc

from application.models import Post, Comment, Tag
from application import db
from application.posts.utils import listToString
from application.users.utils import truncate_html

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    subquery = db.session.query(Comment.post_id, func.count(Comment.post_id).label('count')).group_by(Comment.post_id).subquery()
    results = db.session.query(Post, subquery.c.count).outerjoin(subquery, subquery.c.post_id == Post.id).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)

    for result in results.items:
        reading_time = readtime.of_html(result[0].content)
        result[0].reading_time = reading_time
        result[0].truncated_content = truncate_html(result[0].content, 500)
        tags = listToString(Tag.query.filter_by(post_id=result[0].id).all()).split(",")

        result[0].tags_list = tags

    most_viewed_post = Post.query.order_by(Post.views.desc()).first()
    most_popular_tags = db.session.query(Tag.content, func.count(Tag.content).label('count')).group_by(Tag.content).order_by(desc('count')).limit(3).all()

    return render_template('home.html', results=results, most_viewed_post=most_viewed_post, most_popular_tags=most_popular_tags)


@main.route("/about")
def about():
    return render_template('about.html', title='About')
