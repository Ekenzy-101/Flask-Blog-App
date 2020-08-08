from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import InputRequired, ValidationError

class PostForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField("Content", validators=[InputRequired()])
    category = SelectField("Content",
                           choices=[("Politics", "Politics"), ("Science", "Science"), ("Sport", "Sport"), ("Technology", "Technology"),
                                    ("Entertainment", "Entertainment")])
    image_file = FileField("Upload Post Picture",
                           validators=[FileAllowed(["jpg", "jpeg", "jfif", "png"]), FileRequired()])
    submit = SubmitField("CREATE POST")


class UpdatePostForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField("Content", validators=[InputRequired()])
    category = SelectField("Content",
                           choices=[("Politics", "Politics"), ("Science", "Science"), ("Sport", "Sport"), ("Technology", "Technology"),
                                    ("Entertainment", "Entertainment")])
    image_file = FileField("Upload Post Picture",
                           validators=[FileAllowed(["jpg", "jpeg", "jfif", "png"]), FileRequired()])
    submit = SubmitField("UPDATE POST")
