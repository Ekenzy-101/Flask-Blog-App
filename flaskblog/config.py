import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv("EMAIL_USER") 
    MAIL_PASSWORD = os.getenv("EMAIL_PASS")
    SECRET_KEY = os.getenv("SECRET_KEY") or "38a9b7992e3710d8b125d2eee83a2913"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or "sqlite:///site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
