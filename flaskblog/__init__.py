from flask import Flask, render_template, redirect, flash, url_for
from sassutils.wsgi import SassMiddleware
from flaskblog.forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "38a9b7992e3710d8b125d2eee83a2913"
app.wsgi_app = SassMiddleware(app.wsgi_app, {
    'flaskblog': ('static/sass', 'static/css', '/static/css')
})


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
