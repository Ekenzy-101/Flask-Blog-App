from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail 
from flaskblog.config import Config
from sassutils.wsgi import SassMiddleware

# Globally accessible libraries
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info" 
mail = Mail()


def create_app(config_class=Config):
    """Initialize the core application"""
    app = Flask(__name__)
    app.config.from_object(Config)
    app.wsgi_app = SassMiddleware(app.wsgi_app, {
        'flaskblog': ('static/sass', 'static/css', '/static/css')
    })
    
    # Initialize plugins
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    with app.app_context():
        # Include our routes
        from flaskblog.main.routes import main
        from flaskblog.posts.routes import posts
        from flaskblog.users.routes import users
        from flaskblog.errors.handlers import errors

        # Register Blueprints
        app.register_blueprint(errors)
        app.register_blueprint(main)
        app.register_blueprint(posts)
        app.register_blueprint(users)

        return app