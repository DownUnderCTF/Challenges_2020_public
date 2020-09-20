import flask
from flask_recaptcha import ReCaptcha
import redis
import urllib.parse
import uuid
import secrets

import config
import admin
from decorators import logged_in, is_admin, plain_resp

app = flask.Flask(__name__)
db = redis.Redis(config.REDIS_HOST)

app.config['SECRET_KEY'] = config.SECRET_KEY
app.config.update({
    'RECAPTCHA_ENABLED': config.RECAPTCHA_ENABLED,
    'RECAPTCHA_SITE_KEY': config.RECAPTCHA_SITE_KEY,
    'RECAPTCHA_SECRET_KEY': config.RECAPTCHA_SECRET_KEY
})
app.config.update({
    'SESSION_COOKIE_SECURE': True,
    'SESSION_COOKIE_HTTPONLY': True,
    'SESSION_COOKIE_SAMESITE': 'None'
})

recaptcha = ReCaptcha(app=app)

def session_login(username, is_admin=False):
    flask.session['loggedin'] = True
    flask.session['username'] = username
    flask.session['id']       = str(uuid.uuid4())
    flask.session['csrf']     = secrets.token_hex(12)
    flask.session['admin']    = is_admin

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/login', methods=["POST", "GET"])
def login():
    if 'loggedin' in flask.session and flask.session['loggedin']:
        return flask.redirect(flask.url_for('me'))

    err_msg = ''
    if flask.request.method == 'POST':
        username = flask.request.form.get('username', '')
        if len(username) > 0:
            session_login(username)
            return flask.redirect(flask.url_for('me'))
        else:
            err_msg = 'Username must be specified'
    return flask.render_template('login.html', msg=err_msg)

@app.route('/logout')
def logout():
    flask.session.clear()
    return flask.redirect('/')

@app.route('/me')
@logged_in(redir=True)
def me():
    score = None
    if db.exists(flask.session['id']):
        score = int(db.get(flask.session['id']).decode())

    return flask.render_template(
        'me.html',
        username=flask.session['username'],
        score=score,
        flag=config.FLAG if score == 10 else '',
        userid=flask.session['id'],
        csrf=flask.session['csrf']
    )

@app.route('/playground/<uid>')
@logged_in(redir=True)
def playground(uid):
    return flask.render_template(
        'playground.html',
        csrf=flask.session['csrf']
    )

@app.route('/editor')
@logged_in(redir=True)
def editor():
    return flask.render_template('editor.html')

@app.route('/api/submit', methods=['post'])
@logged_in(redir=False)
@plain_resp
def submit():
    if flask.request.headers.get('X-Internal', '') != config.INTERNAL_TOKEN:
        if not recaptcha.verify():
            return 'Invalid Captcha', 403

    csrf_form = flask.request.form.get('csrf', '')
    csrf_cookie = flask.session['csrf']
    if len(csrf_form) == 0 or len(csrf_cookie) == 0 or csrf_cookie != csrf_form:
        return 'Invalid CSRF token', 403

    url = flask.request.form.get('url', '')
    if len(url) == 0:
        return 'URL must be specified', 400

    parsed = urllib.parse.urlparse(url)
    if not all([parsed.scheme, parsed.netloc]):
        return 'Invalid URL', 400

    host = config.EXTERNAL_HOST if config.EXTERNAL_HOST is not None else flask.request.headers['Host']
    resp = admin.visit(url, flask.session['id'], host)
    if resp:
        return 'A judge will look at your submission shortly', 200
    else:
        return 'A Unknown Error occurred when trying to invoke the XSS bot', 500

@app.route('/admin/login')
def admin_login():
    if flask.request.args.get('token', '') != config.ADMIN_TOKEN:
        return flask.abort(404)

    session_login('admin', is_admin=True)

    return flask.redirect('/')

@app.route('/admin/rate', methods=['POST', 'GET'])
@logged_in(redir=False)
@is_admin
def rate_submission():
    if flask.request.method == 'GET':
        if flask.request.args.get('token', '') != config.ADMIN_TOKEN:
            return flask.abort(405)

        user_id = flask.request.args.get('user', '')
        if len(user_id) == 0:
            return 'No user id specified', 400, {'Content-Type': 'text/plain'}

        return flask.render_template(
            'rate.html',
            csrf=flask.session['csrf'],
            user_id=user_id
        )

    csrf_form   = flask.request.form.get('csrf', '')
    csrf_cookie = flask.session['csrf']
    user_id     = flask.request.form.get('user', '')
    score       = flask.request.form.get('score', '')

    if len(csrf_form) == 0 or len(csrf_cookie) == 0 or csrf_cookie != csrf_form:
        return 'Invalid CSRF token', 403, {'Content-Type': 'text/plain'}

    if len(user_id) == 0 or len(score) == 0:
        return 'Requires user id and score', 400, {'Content-Type': 'text/plain'}

    try: uuid.UUID(hex=user_id)
    except ValueError:
        return 'Invalid user id', 400, {'Content-Type': 'text/plain'}

    try: int(score)
    except ValueError:
        return 'Score must be an integer', 400, {'Content-Type': 'text/plain'}

    if int(score) < 0 or int(score) > 10:
        return 'Score must be in [0, 10]', 400, {'Content-Type': 'text/plain'}

    existing = -1
    if db.exists(user_id):
        existing = int(db.get(user_id).decode())
    db.set(user_id, str(max(int(score), existing)))

    return 'Success', 200, {'Content-Type': 'text/plain'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
