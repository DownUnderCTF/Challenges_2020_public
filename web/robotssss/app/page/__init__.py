from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from page import database
import os

# this is used for login and sessions
login_manager = LoginManager()
database = SQLAlchemy()
migrate = Migrate()
DATABASE = '../templatedb.db'
app = Flask(__name__, instance_relative_config=False)

def create_app():
    #app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    app.config.from_object(__name__)
    # this is used for linking helper objects with current Flask apps
    login_manager.init_app(app)
    database.init_app(app)
    migrate.init_app(app, database)

    with app.app_context():
        from page.user.views import user
        from page.admin.views import admin
        app.register_blueprint(user)
        app.register_blueprint(admin)
        database.create_all()

        return app

# This function is used to read files of our container
def getFile(f):
    with open(f) as fil3:
        return fil3.read()

app.jinja_env.globals['getFile'] = getFile
