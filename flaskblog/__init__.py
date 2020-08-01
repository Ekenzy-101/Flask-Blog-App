from flask import Flask, render_template, redirect
from sassutils.wsgi import SassMiddleware

app = Flask(__name__)
app.wsgi_app = SassMiddleware(app.wsgi_app, {
    'package': ('static/sass', 'static/css', '/static/css')
})


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")
