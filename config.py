import os
from dotenv import load_dotenv

load_dotenv(".env")
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "standard_pass"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['gustavo.fonseca@outlook.pt']
    DATABASE_NAME = os.environ.get("DATABASE_NAME")
    AZURE_SERVER_NAME = os.environ.get("AZURE_SERVER_NAME")
    DB_LOGIN = os.environ.get("DB_LOGIN")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    SCORING_URI = os.environ.get("SCORING_URI")
    ENDPOINT_KEY = os.environ.get("ENDPOINT_KEY")
