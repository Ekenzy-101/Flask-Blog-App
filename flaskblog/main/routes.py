from flask import Blueprint, redirect, render_template, request, url_for
from flaskblog.models import Post
from flask_login import current_user

main = Blueprint("main", __name__)


@main.route("/")
def home():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(
        Post.updated_at.desc()).paginate(page, 4, False)
    next_url = url_for("main.home", page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for("main.home", page=posts.next_num) \
        if posts.has_prev else None
    if getattr(current_user, "image_file", "") == "":
        return render_template("home.html", title="Home", posts=posts, next_url=next_url, prev_url=prev_url)
    
    image_file = url_for(
        "static", filename="profile-pics/" + current_user.image_file)
    return render_template("home.html", title="Home",  image_file=image_file, posts=posts, next_url=next_url, prev_url=prev_url)


@main.route("/about")
def about():
    if getattr(current_user, "image_file", "") == "":
        return render_template("about.html", title="About")
    
    image_file = url_for(
        "static", filename="profile-pics/" + current_user.image_file)
    return render_template("about.html", title="About", image_file=image_file)
