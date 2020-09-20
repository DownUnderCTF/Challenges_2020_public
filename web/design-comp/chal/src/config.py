import os
import sys
import secrets

REDIS_HOST    = os.environ.get('REDIS_HOST',  'localhost')
SECRET_KEY    = os.environ.get('SECRET_KEY',  secrets.token_urlsafe(32))
ADMIN_TOKEN   = os.environ.get('ADMIN_TOKEN', secrets.token_urlsafe(32))
ADMIN_API     = os.environ.get('XSSBOT_API', 'http://xssbot/visit')
ADMIN_TIMEOUT = int(os.environ.get('XSSBOT_TIMEOUT', 30000))
EXTERNAL_HOST = os.environ.get('EXTERNAL_HOST', None)
FLAG          = open('/flag').read().strip() if os.path.isfile('/flag') else None

RECAPTCHA_ENABLED    = os.environ.get('RECAPTCHA_ENABLED',    '1') == '1'
RECAPTCHA_SITE_KEY   = os.environ.get('RECAPTCHA_SITE_KEY',   None)
RECAPTCHA_SECRET_KEY = os.environ.get('RECAPTCHA_SECRET_KEY', None)

INTERNAL_TOKEN = os.environ.get('INTERNAL_TOKEN', None)

if EXTERNAL_HOST is None:
    print(
        '[DANGER] No external host explicitly specified. Trusting Host Header.',
        file=sys.stderr
    )

if FLAG is None:
    print(
        '[WARNING] No /flag file found. Defaulting to a random string',
        file=sys.stderr
    )
    FLAG = 'FLAG{' + secrets.token_hex(16) + '}'

if RECAPTCHA_ENABLED:
    if RECAPTCHA_SECRET_KEY is None:
        print(
            '[WARNING] Recaptcha was enabled but no secret key was specified. Turning captcha off',
            file=sys.stderr
        )
        RECAPTCHA_ENABLED = False
    if RECAPTCHA_SITE_KEY is None:
        print(
            '[WARNING] Recaptcha was enabled but no site key was specified. Turning captcha off',
            file=sys.stderr
        )
        RECAPTCHA_ENABLED = False
