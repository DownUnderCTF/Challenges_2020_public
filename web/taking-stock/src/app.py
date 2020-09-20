import os
import flask
import sklearn as skl
import joblib
import werkzeug
import uuid
import secrets

app = flask.Flask(__name__)
app.config['UPLOAD_ROOT'] = '/tmp'
app.config['MODEL_ROOT'] = './models'
app.config['MAX_CONTENT_LENGTH'] = 128 * 1024
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_urlsafe(32))

ALLOWED_EXTENSIONS = set(['png'])

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def plain(msg, code):
    return msg, code, {'Content-Type': 'text/plain'}

def get_user_img_path():
    return os.path.join(app.config['UPLOAD_ROOT'], f'{flask.session["id"]}.png')

@app.errorhandler(413)
def too_large(e):
    return plain(
        f'Entity too large. Please make sure your files are < {app.config["MAX_CONTENT_LENGTH"]}B',
        413
    )

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/me')
def me():
    if 'id' not in flask.session:
        return plain(
            'Must be logged in',
            401
        )
    return flask.render_template('me.html', username=flask.session['username'])

@app.route('/login', methods=["GET", "POST"])
def register():
    if flask.request.method == 'GET':
        return flask.render_template('login.html')
    else:
        if 'username' not in flask.request.form or len(flask.request.form['username']) == 0:
            return plain(
                'A username must be specified',
                400
            )
        flask.session['id'] = str(uuid.uuid4())
        flask.session['username'] = flask.request.form['username']
        return flask.redirect('/')

@app.route('/logout')
def logout():
    if 'id' in flask.session:
        uid = flask.session['id']
        img_path = get_user_img_path()
        if os.path.isfile(img_path):
            os.unlink(img_path)
        flask.session.clear()
    return flask.redirect('/')

@app.route('/predict', methods=["POST"])
def predict():
    model = flask.request.form.get('stock', 'GOOGL')
    prices = flask.request.form.get('prices', None) 
    if prices is None:
        return plain(
            f'Price history must be specified',
            400
        )

    try:
        prices = [[float(p)] for p in prices.split(',')]
    except ValueError:
        return plain(
            f'Invalid prices',
            400
        )
    
    if len(prices) < 1:
        return plain(
            f'',
            400
        )

    model = os.path.join(app.config['MODEL_ROOT'], model)
    try:
        model = joblib.load(model)
    except Exception as e:
        return plain(
            f'Failed to load {model}',
            500
        )
    
    try:
        res = model.predict(prices)
    except Exception as e:
        return plain(
            f'Failed to make prediction',
            500
        )

    return flask.jsonify(list(res))

@app.route('/profile-picture', methods=["POST"])
def upload():
    if 'id' not in flask.session:
        return plain(
            'Must be logged in',
            401
        )

    if 'img' not in flask.request.files:
        return plain(
            'No image found',
            400
        )
    img = flask.request.files['img']
    if img.filename == '':
        return plain(
            'No image found',
            400
        )
    
    img_path = get_user_img_path()
    if img and allowed_file(img.filename):
        try:
            img.save(img_path)
        except:
            return plain(
                f'Failed to upload image to {img_path}',
                500
            )
        return flask.redirect('/me')
    else:
        return plain(
            f'Invalid file: file must be a png',
            400
        )

@app.route('/profile-picture/<uid>')
def profilepic(uid):
    try:
        uuid.UUID(hex=uid)
    except ValueError:
        return plain(
            'Invalid User ID',
            400
        )

    prof_img = get_user_img_path()
    if os.path.isfile(prof_img):
        return flask.send_file(prof_img)
    else:
        return plain(
            f'No such file {prof_img}',
            404
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
