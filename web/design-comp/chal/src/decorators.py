import flask

def logged_in(redir=False):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            if 'loggedin' not in flask.session or not flask.session['loggedin']:
                if redir:
                    return flask.redirect(flask.url_for('login'))
                else:
                    return flask.jsonify({
                        'error': 'UNAUTHORIZED',
                        'detail': 'You must be logged in'
                    }), 401
            else:
                return fn(*args, **kwargs)
        wrapper.__name__ = fn.__name__
        return wrapper
    return decorator

def is_admin(fn):
    def wrapper():
        if 'admin' not in flask.session or not flask.session['admin']:
            return flask.jsonify({
                'error': 'UNAUTHORIZED',
                'detail': 'Only admins can access this route'
            }), 401
        return fn()
    wrapper.__name__ = fn.__name__
    return wrapper

def plain_resp(fn):
    def wrapper():
        # Pretty much a big hack
        resp, status = fn()
        return resp, status, {'Content-Type': 'text/plain'}

    wrapper.__name__ == fn.__name__
    return wrapper