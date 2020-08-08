from flask import Blueprint, redirect, render_template, request, url_for, abort, flash
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm, UpdatePostForm 
from flaskblog.posts.utils import save_post_pic
from flask_login import current_user, login_required

posts = Blueprint("posts", __name__)


@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        pic_file = save_post_pic(form.image_file.data).strip()
        value = dict(form.category.choices).get(form.category.data)
        post = Post(title=form.title.data.strip(), content=form.content.data.strip(),
                    category=value, author=current_user, image_file=pic_file)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created successfully!", category="success")
        return redirect(url_for("main.home"))
    
    image_file = url_for("static", filename="profile-pics/" + current_user.image_file)
    return render_template("create-post.html", title="New Post",
                        form=form, image_file=image_file, legend="New Post")


@posts.route("/posts/<id>")
def get_post(id):
    post = Post.query.get_or_404(id)
    if getattr(current_user, "image_file", "") == "":
        return render_template("post.html", title=post.title, post=post)

    image_file = url_for("static", filename="profile-pics/" + current_user.image_file)
    return render_template("post.html", title=post.title, post=post, image_file=image_file)


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
        post.image_file = save_post_pic(form.image_file.data)
        db.session.commit()
        flash("Your post has been updated successfully!", category="success")
        return redirect(url_for("posts.get_post", id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
        form.category.data = post.category
        form.image_file.data = post.image_file
    image_file = url_for(
        "static", filename="profile-pics/" + current_user.image_file)
    return render_template("create-post.html", title="Update Post",
                            form=form, legend="Update Post", image_file=image_file)


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
