from flask import Blueprint, redirect, render_template, request, url_for, abort, flash, current_app
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm, UpdatePostForm 
from flaskblog.users.utils import upload_file_to_s3
from flask_login import current_user, login_required
from os import environ

posts = Blueprint("posts", __name__)


@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        pic_file = upload_file_to_s3(form.image_file.data, environ.get("AWS_BUCKET_NAME"), prefix="post-pics/")
        value = dict(form.category.choices).get(form.category.data)
        post = Post(title=form.title.data.strip(), content=form.content.data.strip(),
                    category=value, author=current_user, image_file=pic_file)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created successfully!", category="success")
        return redirect(url_for("main.home"))
    

    return render_template("create-post.html", title="New Post",
                            form=form, image_file=current_user.image_file, legend="New Post")


@posts.route("/posts/<id>")
def get_post(id):
    post = Post.query.get_or_404(id)
    if getattr(current_user, "image_file", "") == "":
        return render_template("post.html", title=post.title, post=post)

    return render_template("post.html", title=post.title, post=post, image_file=current_user.image_file)


@posts.route("/posts/<id>/update", methods=["GET", "POST"])
@login_required
def update_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        abort(403)
    form = UpdatePostForm()
    if form.validate_on_submit():
        post.title = form.title.data.strip()
        post.content = form.content.data.strip()
        post.category = dict(form.category.choices).get(form.category.data)
        post.image_file = upload_file_to_s3(form.image_file.data, environ.get("AWS_BUCKET_NAME"), prefix="post-pics/")
        db.session.commit()
        flash("Your post has been updated successfully!", category="success")
        return redirect(url_for("posts.get_post", id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
        form.category.data = post.category
        form.image_file.data = post.image_file

    return render_template("create-post.html", title="Update Post",
                            form=form, legend="Update Post", image_file=current_user.image_file)


@posts.route("/posts/<id>/delete", methods=["POST"])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted successfully!", category="success")
    return redirect(url_for("main.home"))
