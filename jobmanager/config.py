import os


class Config:
    SECRET_KEY = '8c46b963a8a8b4782352e4f5f7364a541bbdec21'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.dot.ca.gov'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    INPUTFILE_FOLDER = '/data/input'
    OUTPUTFILE_FOLDER = '/data/output'
    JWT_SECRET_KEY = "super-secret"


