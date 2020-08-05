import secrets
import os
from PIL import Image
from flask import render_template, flash, redirect, url_for, request, abort
from flaskblog.models import User, Post
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
def home():
    posts = Post.query.all()
    if getattr(current_user, "image_file", "") == "":
        return render_template("home.html", title="Home", posts=posts)
    else:
        image_file = url_for("static", filename="profile-pics/" + current_user.image_file )
        return render_template("home.html", title="Home",  image_file=image_file, posts=posts)


@app.route("/about")
def about():
    if getattr(current_user, "image_file", "") == "":
        return render_template("about.html", title="About")
    else:
        image_file = url_for("static", filename="profile-pics/" + current_user.image_file)
        return render_template("about.html", title="About", image_file=image_file)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, fullname=form.fullname.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created! You are now able to Log In", category="success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash(f"Successfully Logged In", category="success")
            return  redirect(next_page) if next_page else  redirect(url_for("home"))
        else:
            flash(f"Login Unsuccessful. Please check email and password", category="danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

def save_profile_pic(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile-pics", picture_fn)

    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_profile_pic(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data.strip()
        current_user.fullname = form.fullname.data.strip()
        current_user.facebook_link = form.facebook_link.data.strip()
        current_user.linkedin_link = form.linkedin_link.data.strip()
        current_user.instagram_link = form.instagram_link.data.strip()
        current_user.twitter_link = form.twitter_link.data.strip()
        current_user.location = form.location.data.strip()
        current_user.bio = form.bio.data.strip()
        current_user.job_title = form.job_title.data.strip()
        db.session.commit()
        flash("Your account has been updated", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.fullname.data = current_user.fullname
        form.facebook_link.data = current_user.facebook_link
        form.linkedin_link.data = current_user.linkedin_link
        form.instagram_link.data = current_user.instagram_link
        form.job_title.data = current_user.job_title
        form.bio.data = current_user.bio
        form.location.data = current_user.location 
    image_file = url_for("static", filename="profile-pics/" + current_user.image_file)
    return render_template("account.html", title="Account", form=form, image_file=image_file)

def save_post_pic(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/post-pics", picture_fn)

    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        pic_file = save_post_pic(form.image_file.data)
        value = dict(form.category.choices).get(form.category.data)
        post = Post(title=form.title.data.strip(), content=form.content.data.strip(), 
        category=value, author=current_user, image_file=pic_file)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created successfully!", category="success")
        return redirect(url_for("home"))
    image_file = url_for("static", filename="profile-pics/" + current_user.image_file)
    return render_template("create-post.html", title="New Post",
    form=form, image_file=image_file, legend="New Post")


@app.route("/posts/<id>")
def get_post(id):
    post = Post.query.get_or_404(id)
    image_file = url_for("static", filename="profile-pics/" + current_user.image_file)
    return render_template("post.html", title=post.title, post=post, image_file=image_file)


@app.route("/posts/<id>/update", methods=["GET", "POST"])
@login_required
def update_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data.strip()
        post.content = form.content.data.strip()
        post.category = dict(form.category.choices).get(form.category.data)
        post.image_file = save_post_pic(form.image_file.data)
        db.session.commit()
        flash("Your post has been updated successfully!", category="success")
        return redirect(url_for("get_post", id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
        form.category.data = post.category
        form.image_file.data = post.image_file
    return render_template("create-post.html", title="Update Post",
    form=form, legend="Update Post")


@app.route("/posts/<id>/delete", methods=["POST"])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted successfully!", category="success")
    return redirect(url_for("home"))
