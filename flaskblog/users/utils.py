import os
import secrets
import boto3
import logging
from botocore.exceptions import ClientError
from flask import url_for
from flask_mail import Message
from flaskblog import mail
from flask import Flask, current_app
from os import environ

s3_client = boto3.client(
    "s3",
    region_name=environ.get("AWS_REGION"),
    aws_access_key_id=environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=environ.get("AWS_SECRET_ACCESS_KEY")
)    

def get_filename(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    
    return picture_fn


def upload_file_to_s3(form_picture, bucket_name, acl="public-read", prefix="profile-pics/"):

    try:
        file_name = get_filename(form_picture)
        prefixed_filename = prefix + file_name
        s3_client.upload_fileobj(
            form_picture,
            bucket_name,
            prefixed_filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": form_picture.content_type
            })
    except ClientError as e:
        logging.error(e)
        return False
    return "{}{}".format(current_app.config["AWS_LOCATION"], prefixed_filename)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request",
                    sender="noreply@demo.com", recipients=[user.email])
    msg.body = f"""We heard that you lost your password. Sorry about that!
But don't worry! You can use the following link to reset your password:

{url_for("users.reset_token", token=token, _external=True)}

If you don't use the link within 3 hours, it will expire. To get a new password reset link, visit:

{url_for("users.reset_request", _external=True)}

If you did not make this request then simply ignore this email and no changes
will be made.

Thanks
Kenzy
"""
    mail.send(msg)
