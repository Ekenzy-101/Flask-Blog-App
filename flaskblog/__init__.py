from datetime import datetime
from flask import Flask, render_template, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sassutils.wsgi import SassMiddleware
from flaskblog.forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "38a9b7992e3710d8b125d2eee83a2913"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.wsgi_app = SassMiddleware(app.wsgi_app, {
    'flaskblog': ('static/sass', 'static/css', '/static/css')
})
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    fullname = db.Column(db.String(40), unique=True,
                         default="Unknown Member", nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    image_file = db.Column(
        db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(
        db.String(20), nullable=False, default="default-post.jpg")
    category = db.Column(db.String(40), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}', '{self.category}')"


@app.route("/")
def home():
    return render_template("home.html", title="Home")


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account Created For {form.username.data}", category="success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f"Successfully Logged In", category="success")
        return redirect(url_for("home"))
    return render_template("login.html", title="Login", form=form)
