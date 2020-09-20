import asyncio
from requests_futures.sessions import FuturesSession
import base64 as b64
import zlib

REMOTE = 'http://172.28.54.188:8000'

def init_session():
    session = FuturesSession()
    resp = session.post(f'{REMOTE}/login', data={'username': 'todo_bot_loadtest'}).result()
    csrf_token = resp.text.split('name="csrf" value="')[1].split('"')[0]
    return session, csrf_token

def test_connection(session, csrf, server):
    return session.post(f'{REMOTE}/api/submit', data={
        'url': server,
        'csrf': csrf
    })

def do_test(session, csrf, server, size=8):
    connections = [test_connection(session, csrf, server) for _ in range(size)]
    return [c.result() for c in connections]

if __name__ == '__main__':
    import sys

    size = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    sess, csrf = init_session()
    resp = do_test(sess, csrf, 'http://example.com', size=size)
    print(resp, [r.elapsed for r in resp])