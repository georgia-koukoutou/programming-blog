from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired


class CommentForm(FlaskForm):
    content = TextAreaField("Content", validators=[InputRequired()])
    submit = SubmitField("Post")



