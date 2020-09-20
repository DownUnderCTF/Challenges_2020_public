from page import database
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property


class Users(database.Model):
    __tablename__ = 'users'

    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.Text, nullable=False)
    email = database.Column(database.Text, nullable=False)
    password = database.Column(database.Text, nullable=False)
    urole = database.Column(database.Text, nullable=False)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    @property
    def get_urole(self):
        return str(self.urole)

    def __init__(self, username, email, password, urole):
        self.username = username
        self.email = email
        self.password = password
        self.urole = urole

    def __repr__(self):
        returnStr = str('Account name: %s\n') % (self.username)
        return returnStr
'''
class Admin(database.Model):
    __tablename__ = "admin"

    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.Text, nullable=False)
    email = database.Column(database.Text, nullable=False)
    password = database.Column(database.Text, nullable=False)
    bio = database.Column(database.Text, nullable=False)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_admin(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def get_id(self):
        return str(self.id)

    def __init__(self, username, email, password, bio):
        self.username = username
        self.email = email
        self.password = password
        self.bio = bio

    def __repr__(self):
        returnStr = str('Account name: %s\n') % (self.username)
        return returnStr
'''

class Blog(database.Model):
    __tablename__ = "blog"

    id = database.Column(database.Integer, primary_key=True)
    author = database.Column(database.Text, nullable=False)
    title = database.Column(database.Text, nullable=False)
    content = database.Column(database.Text, nullable=False)

    def __init__(self, author, title, content):
        self.author = author
        self.title = title
        self.content = content

from page.util.login_manager import *
