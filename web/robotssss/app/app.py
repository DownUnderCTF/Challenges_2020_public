from page import create_app
from flask import session
from werkzeug.middleware.proxy_fix import ProxyFix
from database import *
import os

#app = Flask(__name__)

app = create_app()
app.secret_key = "app.jinja_env.globals['getFile'] = getFile(fileName)"
app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
    init_db(r"templatedb.db")
    #app.run(debug=False)
