from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail 
from sassutils.wsgi import SassMiddleware
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "38a9b7992e3710d8b125d2eee83a2913"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.wsgi_app = SassMiddleware(app.wsgi_app, {
    'flaskblog': ('static/sass', 'static/css', '/static/css')
})
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info" 
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.environ.get("USERNAME") 
app.config["MAIL_PASSWORD"] = os.environ.get("PASSWORD")
mail = Mail(app)

from flaskblog import routes