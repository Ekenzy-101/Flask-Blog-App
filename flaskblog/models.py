from flaskblog import db, login_manager
from flask_login import UserMixin
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID
import uuid

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(str(user_id))

def generate_uuid():
    return str(uuid.uuid4())

class User(db.Model, UserMixin):
    id = db.Column(db.String(50), primary_key=True, default=generate_uuid)
    username = db.Column(db.String(20), unique=True, nullable=False)
    fullname = db.Column(db.String(40), default="Unknown Member", nullable=False)
    job_title = db.Column(db.String(200), default="", nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    image_file = db.Column(
        db.String(20), nullable=False, default="default.jpg")
    facebook_link = db.Column(db.String(150), default="",  nullable=False)
    linkedin_link = db.Column(db.String(150), default="", nullable=False)
    instagram_link = db.Column(db.String(150), default="", nullable=False)
    twitter_link = db.Column(db.String(150), default="" ,nullable=False)
    location =  db.Column(db.String(200), default="", nullable=False)
    bio = db.Column(db.Text, default="", nullable=False)
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, 
    default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    title = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, 
    default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(
        db.String(20), nullable=False, default="default-post.jpg")
    category = db.Column(db.String(40), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.created_at}', '{self.category}')"