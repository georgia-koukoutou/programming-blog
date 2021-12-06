from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    # content = TextAreaField("Content", validators=[DataRequired()])
    content = HiddenField("Content", validators=[DataRequired()], id="post_content")
    submit = SubmitField("Post")



