
from datetime import datetime
import time
import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flaskblog import mail
from flask_mail import Message


# def utc2local_offset():
#     epoch = time.mktime(utc.timetuple())
#     offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
#     return offset


def save_file(file, folder):
    # create a random file name
    random_hex = secrets.token_hex(4)
    f_n, f_ext = os.path.splitext(file.filename)
    file_name = '{}_{}{}'.format(f_n, random_hex, f_ext)
    file_path = os.path.join(folder, file_name)
    file.save(file_path)
    return file_name

