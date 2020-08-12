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
    MAIL_USERNAME = environ.get("EMAIL_USER") 
    MAIL_PASSWORD = environ.get("EMAIL_PASS")
    SECRET_KEY = environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    AWS_ACCESS_KEY_ID = environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_BUCKET_NAME = environ.get("AWS_BUCKET_NAME")
    AWS_REGION = environ.get("AWS_REGION")
    AWS_LOCATION = "https://{}.s3.{}.amazonaws.com/".format(
        environ.get("AWS_BUCKET_NAME"), environ.get("AWS_REGION"))
