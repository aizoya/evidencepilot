"""Opt-in real HTTP verification. No fake client. Saves PRIVATE synthetic-question evidence."""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from urllib.request import Request, build_opener, HTTPRedirectHandler


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def main():
    if os.getenv('ENABLE_LIVE_RESEARCH') != 'true' or not os.getenv('APP_ACCESS_TOKEN'):
        sys.exit('Blocked: authorize and configure live research in the server and verification environment first.')
    question = 'What are the current eligibility and submission requirements for the ODSC Nebius research agent hackathon in 2026?'
    url = os.getenv('VERIFY_ORIGIN', 'http://127.0.0.1:8000').rstrip('/')
    if not (url == 'http://127.0.0.1:8000' or url.startswith('https://')):
        sys.exit('Verification requires localhost or HTTPS.')
    req = Request(url+'/api/research', data=json.dumps({'question':question}).encode(), headers={
        'Content-Type':'application/json', 'Authorization':'Bearer '+os.environ['APP_ACCESS_TOKEN']})
    with build_opener(NoRedirect).open(req, timeout=300) as response:
        report=json.load(response)
    root=Path('evidence/private'); root.mkdir(parents=True, exist_ok=True, mode=0o700)
    raw=json.dumps(report, indent=2).encode()
    artifact=root/(report['run_id']+'.json'); artifact.write_bytes(raw); artifact.chmod(0o600)
    try: sha=subprocess.check_output(['git','rev-parse','HEAD'], stderr=subprocess.DEVNULL, text=True).strip()
    except subprocess.CalledProcessError: sha='uncommitted'
    manifest={'report_sha256':hashlib.sha256(raw).hexdigest(),'code_sha':sha,
              'run_id':report['run_id'],'status':report['status'],'synthetic_question':True}
    (root/(report['run_id']+'.manifest.json')).write_text(json.dumps(manifest,indent=2))
    providers={u['provider'] for u in report.get('usage',[])}
    supported=any(c['status']=='supported' for c in report.get('claims',[]))
    print(json.dumps(manifest))
    if providers != {'nebius','tavily'} or not supported or report['status']=='failed':
        sys.exit('Live run captured but did not pass end-to-end acceptance. Inspect private evidence.')
    print('Real provider path returned supported findings. Manual citation checking is still required.')

if __name__=='__main__': main()
