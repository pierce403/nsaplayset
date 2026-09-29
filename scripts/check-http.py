#!/usr/bin/env python3
"""Check Pages HTTP behavior: python3 scripts/check-http.py https://SITE"""
import sys
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urljoin
from urllib.request import HTTPRedirectHandler, build_opener

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args):
        return None

base = sys.argv[1].rstrip('/')
opener = build_opener(NoRedirect)

def get(path):
    try:
        return opener.open(base + path, timeout=15)
    except HTTPError as error:
        return error

root = Path(__file__).resolve().parents[1]
count = 0
for line in (root / 'static/_redirects').read_text().splitlines():
    if not line.strip() or line.startswith('#'):
        continue
    source, destination, status = line.split()
    with get(source) as response:
        assert response.code == int(status), (source, response.code, status)
        actual = urljoin(base + source, response.headers['Location'])
        assert actual == urljoin(base + '/', destination), (source, actual, destination)
    count += 1
for path in ['/', '/twilightvegetable/', '/site.css', '/catalog.js']:
    with get(path) as response:
        assert response.code == 200, (path, response.code)
        assert response.headers['X-Content-Type-Options'] == 'nosniff'
        assert "default-src 'self'" in response.headers['Content-Security-Policy']
with get('/definitely-not-a-page/') as response:
    assert response.code == 404, response.code
print(f'PASS: {count} HTTP redirects, pages/assets, security headers, and HTTP 404 at {base}')
