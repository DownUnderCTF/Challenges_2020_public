from os import environ, path
from datetime import timedelta


class Config:
    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + '/db/templatedb.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
