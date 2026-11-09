"""Small source guard; complements, does not replace, external secret/SAST scans."""
import ast
from pathlib import Path
root=Path(__file__).resolve().parents[1]
for p in root.rglob('*.py'):
    if '.venv' not in p.parts: ast.parse(p.read_text(), filename=str(p))
js=(root/'evidencepilot/static/app.js').read_text()
for forbidden in ('innerHTML', 'eval(', 'localStorage', 'sessionStorage'):
    assert forbidden not in js, forbidden
assert not list(root.glob('.env')),'Do not package secrets'
assert not list(root.glob('*.sqlite3')),'Do not package operational databases'
print('Syntax and narrow source guards passed. External security scans remain required.')
