from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError, URL, Optional
from flaskblog.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[
        InputRequired(), Length(min=3, max=20,)])
    fullname = StringField("Fullname", validators=[
        InputRequired(), Length(min=6, max=40,)])
    email = StringField("Email", validators=[
                        InputRequired(), Email()])
    password = PasswordField("Password", validators=[
        InputRequired(), Length(min=6, max=50)])
    confirm_password = PasswordField("Confirm Password",
                                    validators=[InputRequired(), Length(min=6, max=50), EqualTo("password")])
    submit = SubmitField("SIGN UP")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "Username already exists. Please choose another one")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email is  taken. Please choose another one")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[
                        InputRequired(), Email()])
    password = PasswordField("Password", validators=[
        InputRequired(), Length(min=6, max=50)])
    remember = BooleanField("Remember Me")
    submit = SubmitField("LOG IN")


class UpdateAccountForm(FlaskForm):
    fullname = StringField("Fullname", validators=[
        InputRequired(), Length(min=6, max=40)])
    username = StringField("Username", validators=[
                            InputRequired(), Length(min=3, max=20)])
    job_title = StringField("Job Title")
    facebook_link = StringField(
        "Facebook Link", validators=[Optional(), URL()])
    linkedin_link = StringField(
        "LinkedIn Link", validators=[Optional(), URL()])
    instagram_link = StringField(
        "Instagram Link", validators=[Optional(), URL()])
    twitter_link = StringField("Twitter Link", validators=[Optional(), URL()])
    location = StringField("Location")
    bio = TextAreaField("Bio")
    picture = FileField("Update Profile Picture", validators=[
                        FileAllowed(["jpg", "jpeg", "jfif", "png"])])
    submit = SubmitField("UPDATE INFO")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "Username already exists. Please choose another one")

    # def validate_fullname(self, fullname):
    #     if fullname.data != current_user.fullname:
    #         user = User.query.filter_by(fullname=fullname.data).first()
    #         if user:
    #             raise ValidationError(
    #                 "Email is  taken. Please choose another one")


class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    submit = SubmitField("Send Password Reset Email")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.strip()).first()
        if user is None:
            raise ValidationError(
                "There is no account with that email. You must register first")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[
        InputRequired(), Length(min=6, max=50)])
    confirm_password = PasswordField("Confirm Password",
                                    validators=[InputRequired(), Length(min=6, max=50), EqualTo("password")])
    submit = SubmitField("Change Password")
