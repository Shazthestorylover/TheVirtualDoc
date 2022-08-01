import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    """Base Config Object"""
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', './uploads')
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'Password123')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', './uploads')
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Som3$ec5etK*y')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # This is just here to suppress a warning from SQLAlchemy as it will soon be removed