import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flaskblog import mail
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
    msg = Message('Password Reset Request',
                  sender='amhq@dot.ca.gov',
                  recipients=[user.email])
    msg.body = '''To reset your password, visit the following link:{}
    '''.format(url_for('reset_token', token=token, _external=True))
    mail.send(msg)

def save_file(file, folder):
    # create a random file name
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file.filename)
    file_fn = random_hex + f_ext
    print(file_fn)
    file_path = os.path.join(current_app.root_path, folder, file_fn)
    file.save(file_path)
    return file_path