"""Small WSGI application; local server is for development only."""
import hmac
import json
import os
import threading
from pathlib import Path
from wsgiref.simple_server import make_server
from .core import Budget, Providers, ResearchError, research

STATIC = Path(__file__).parent / 'static'
LOCK = threading.Lock()


def app(environ, start_response):
    def respond(status, data, mime='application/json'):
        body = json.dumps(data).encode() if mime == 'application/json' else data
        start_response(status, [('Content-Type', mime + '; charset=utf-8'),
            ('Content-Length', str(len(body))), ('Cache-Control', 'no-store'),
            ('X-Content-Type-Options', 'nosniff'), ('Referrer-Policy', 'no-referrer'),
            ('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")])
        return [body]
    path = environ.get('PATH_INFO', '/')
    method = environ.get('REQUEST_METHOD', 'GET')
    if method == 'GET' and path == '/health':
        return respond('200 OK', {'status': 'ok', 'research_ready': Providers().configured() and os.getenv('ENABLE_LIVE_RESEARCH') == 'true' and len(os.getenv('APP_ACCESS_TOKEN', '')) >= 24})
    assets = {'/': ('index.html', 'text/html'), '/app.js': ('app.js', 'text/javascript'), '/style.css': ('style.css', 'text/css')}
    if method == 'GET' and path in assets:
        filename, mime = assets[path]
        return respond('200 OK', (STATIC / filename).read_bytes(), mime)
    if method != 'POST' or path != '/api/research':
        return respond('404 Not Found', {'error': 'Not found.'})
    token = os.getenv('APP_ACCESS_TOKEN', '')
    if len(token) < 24 or not hmac.compare_digest(environ.get('HTTP_AUTHORIZATION', '').encode('utf-8'), ('Bearer ' + token).encode('utf-8')):
        return respond('401 Unauthorized', {'error': 'A valid research access code is required.'})
    origin = environ.get('HTTP_ORIGIN')
    if origin and origin != os.getenv('APP_ORIGIN', 'http://127.0.0.1:8000'):
        return respond('403 Forbidden', {'error': 'Origin is not allowed.'})
    if os.getenv('ENABLE_LIVE_RESEARCH') != 'true':
        return respond('503 Service Unavailable', {'error': 'Live research is disabled pending provider and budget authorization.'})
    if environ.get('CONTENT_TYPE', '').split(';')[0] != 'application/json':
        return respond('415 Unsupported Media Type', {'error': 'JSON is required.'})
    try:
        length = int(environ.get('CONTENT_LENGTH', '0'))
        if not 1 <= length <= 8192:
            raise ValueError()
        payload = json.loads(environ['wsgi.input'].read(length))
        if not isinstance(payload, dict):
            raise ValueError()
    except (ValueError, TypeError):
        return respond('400 Bad Request', {'error': 'Invalid request body.'})
    if not LOCK.acquire(blocking=False):
        return respond('429 Too Many Requests', {'error': 'Research is already running. Please wait.'})
    try:
        limit = int(os.getenv('DAILY_RUN_LIMIT', '10'))
        if not 1 <= limit <= 100:
            raise ResearchError('Server research limit must be between 1 and 100.')
        budget = Budget(os.getenv('QUOTA_DB', 'quota.sqlite3'), limit)
        report = research(payload.get('question'), Providers(), budget)
        return respond('200 OK', report)
    except ResearchError as exc:
        return respond('422 Unprocessable Entity', {'error': str(exc)})
    except Exception:
        return respond('500 Internal Server Error', {'error': 'Research could not finish. No automatic retry was made.'})
    finally:
        LOCK.release()


def main():
    # Never log request URLs, tokens, questions or retrieved content.
    from wsgiref.simple_server import WSGIRequestHandler
    class QuietHandler(WSGIRequestHandler):
        def log_message(self, *args):
            pass
    with make_server('127.0.0.1', 8000, app, handler_class=QuietHandler) as server:
        print('EvidencePilot development server: http://127.0.0.1:8000', flush=True)
        server.serve_forever()

if __name__ == '__main__':
    main()
