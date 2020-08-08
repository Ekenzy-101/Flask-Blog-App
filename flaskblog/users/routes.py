from flask import Blueprint, redirect, render_template, request, url_for, abort, flash
from flaskblog import db, bcrypt, mail
from flaskblog.models import User, Post
from flaskblog.users.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm, UpdateAccountForm
from flaskblog.users.utils import save_profile_pic, send_reset_email
from flask_login import current_user, login_user, logout_user, login_required

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user = User(username=form.username.data, fullname=form.fullname.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created! You are now able to Log In",
              category="success")
        return redirect(url_for("users.login"))
    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash(f"Successfully Logged In", category="success")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash(f"Login Unsuccessful. Please check email and password",
                  category="danger")
    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_profile_pic(form.picture.data)
            current_user.image_file = picture_file.strip()
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
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.fullname.data = current_user.fullname
        form.facebook_link.data = current_user.facebook_link
        form.linkedin_link.data = current_user.linkedin_link
        form.twitter_link.data = current_user.twitter_link
        form.instagram_link.data = current_user.instagram_link
        form.job_title.data = current_user.job_title
        form.bio.data = current_user.bio
        form.location.data = current_user.location
    image_file = url_for(
        "static", filename="profile-pics/" + current_user.image_file)
    return render_template("account.html", title="Account", form=form, image_file=image_file)


@users.route("/users/<username>")
def get_user(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.updated_at.desc())\
        .paginate(page, 4, False)
    next_url = url_for("users.get_user", username=username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for("users.get_user", username=username, page=posts.next_num) \
        if posts.has_prev else None
    if getattr(current_user, "image_file", "") == "":
        return render_template("user.html", title=user.username, user=user, posts=posts,
                                len=len, next_url=next_url, prev_url=prev_url)

    image_file = url_for(
        "static", filename="profile-pics/" + current_user.image_file)
    return render_template("user.html", title=user.username, len=len, image_file=image_file, user=user, posts=posts, prev_url=prev_url, next_url=next_url)




@users.route("/reset-password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip()).first()
        send_reset_email(user)
        flash("""Check your email for a link to reset your password. If it doesn't appear within a
few minutes, check your spam folder""", category="info")
        return redirect(url_for("users.login"))
    return render_template("reset-request.html", title="Reset Password", form=form)


@users.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("It looks like you clicked on an invalid password reset link. Please try again", category="danger")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data.strip()).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        flash(f"Your password has been updated! You are now able to Log In",
                category="success")
        return redirect(url_for("users.login"))
    return render_template("reset-token.html", title="Reset Password", user=user, form=form)
