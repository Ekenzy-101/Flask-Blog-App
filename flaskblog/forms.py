from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


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


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[
                        DataRequired(), Email(message="Invalid Email Address")])
    password = PasswordField("Password", validators=[
        DataRequired(), Length(min=6, max=50)])
    remember = BooleanField("Remember Me")
    submit = SubmitField("LOGIN")
