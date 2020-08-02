from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(), Length(min=3, max=20,)])
    fullname = StringField("Fullname", validators=[
        DataRequired(), Length(min=3, max=40,)])
    email = StringField("Email", validators=[
                        DataRequired(), Email()])
    password = PasswordField("Password", validators=[
        DataRequired(), Length(min=6, max=50)])
    confirm_password = PasswordField("Confirm Password",
                                     validators=[DataRequired(), Length(min=6, max=50), EqualTo("password")])
    submit = SubmitField("SIGN UP")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already exists. Please choose another one")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email is  taken. Please choose another one")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[
                        DataRequired(), Email(message="Invalid Email Address")])
    password = PasswordField("Password", validators=[
        DataRequired(), Length(min=6, max=50)])
    remember = BooleanField("Remember Me")
    submit = SubmitField("LOGIN")
