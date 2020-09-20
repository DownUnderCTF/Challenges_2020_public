from flask import current_app as app
from itsdangerous import URLSafeTimedSerializer


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    return serializer.dumps(email, salt='SLIGHTSALTED')


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    try:
        email = serializer.loads( \
            token,
            salt='SLIGHTSALTED',
            max_age=expiration)
    except:
        return False

    return email
