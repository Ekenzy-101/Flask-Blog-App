from os import environ
from dotenv import load_dotenv, find_dotenv

# Load Environmental Variables
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(dotenv_path=ENV_FILE)


class Config:
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
<<<<<<< HEAD
    MAIL_USERNAME = environ.get("EMAIL_USER") 
    MAIL_PASSWORD = environ.get("EMAIL_PASS")
    SECRET_KEY = environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    AWS_ACCESS_KEY_ID = environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_BUCKET_NAME = environ.get("AWS_BUCKET_NAME")
    AWS_REGION = environ.get("AWS_REGION")
    AWS_LOCATION = "https://{}.s3.{}.amazonaws.com/".format(
        environ.get("AWS_BUCKET_NAME"), environ.get("AWS_REGION"))
=======
    MAIL_USERNAME = os.environ.get("EMAIL_USER") 
    MAIL_PASSWORD = os.environ.get("EMAIL_PASS")
    SECRET_KEY = os.environ.get("SECRET_KEY") or "38a9b7992e3710d8b125d2eee83a2913"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_BUCKET_NAME = os.environ.get("AWS_BUCKET_NAME")
    AWS_REGION = os.environ.get("AWS_REGION")
    AWS_LOCATION = "https://{}.s3.{}.amazonaws.com/".format(AWS_BUCKET_NAME, AWS_REGION)
>>>>>>> 1c638d1c8bb1ae46e9251c8391cd96abff56974a
