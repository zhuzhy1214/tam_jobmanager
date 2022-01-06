import os
import secrets
from PIL import Image
from flask import url_for, current_app
from jobmanager import mail
from flask_mail import Message


def save_picture(form_picture):
    # create a random file name
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request for Job Manager',
                  sender='hq_am_jobmanager@dot.ca.gov',
                  recipients=[user.email])
    msg.body = '''Hi there, \n
    You are receiving this email because someone submitted a request to reset password on HQ TAM Job Manager Site. 
    Please ignore this email if you did not initiate the request. \n
    To reset your password, please click the following link:\n
    {}
    '''.format(url_for('users.reset_token', token=token, _external=True))


    mail.send(msg)

