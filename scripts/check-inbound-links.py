#!/usr/bin/env python3
"""Check the bounded set of public inbound links recorded in the audit.

Run after deployment: python3 scripts/check-inbound-links.py
Use --output tmp/link-audit/live.json to save redirect chains and results.
Only requests nsaplayset.org and www.nsaplayset.org; never crawls other sites.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit, unquote
from urllib.request import HTTPRedirectHandler, Request, build_opener

ROOT = Path(__file__).resolve().parents[1]
HOSTS = {'nsaplayset.org', 'www.nsaplayset.org'}
USER_AGENT = 'NSAPlayset-LinkAudit/1.0 (+https://github.com/pierce403/nsaplayset)'


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args):
        return None


class Page(HTMLParser):
    def __init__(self, body):
        super().__init__()
        self.ids = set()
        self.title = ''
        self.in_title = False
        self.feed(body.decode('utf-8', errors='replace'))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        if tag == 'title':
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def check(item):
    result = {'url': item['url'], 'chain': [], 'ok': False}
    current = item['url']
    fragment = urlsplit(current).fragment
    opener = build_opener(NoRedirect)
    try:
        for _ in range(8):
            parts = urlsplit(current)
            if parts.scheme not in {'http', 'https'} or parts.hostname not in HOSTS:
                raise ValueError('redirect leaves the audited first-party hosts')
            request = Request(current, headers={'User-Agent': USER_AGENT})
            try:
                response = opener.open(request, timeout=20)
            except HTTPError as error:
                response = error
            with response:
                status = response.code
                location = response.headers.get('Location')
                result['chain'].append({'url': current, 'status': status, **({'location': location} if location else {})})
                if status in {301, 302, 303, 307, 308} and location:
                    current = urljoin(current, location)
                    fragment = urlsplit(current).fragment or fragment
                    continue
                body = response.read(512_000 if item['kind'] == 'html' else 1024)
                content_type = response.headers.get('Content-Type', '')
            result['final_url'] = current
            if status != 200:
                raise ValueError(f'HTTP {status}')
            if (parts.scheme, parts.hostname, parts.path or '/') != ('https', 'nsaplayset.org', item['expected_path']):
                raise ValueError(f'unexpected destination: {current}')
            if parts.query != urlsplit(item['url']).query:
                raise ValueError('query string was lost or changed')
            if item['kind'] == 'pdf':
                if 'application/pdf' not in content_type or not body.startswith(b'%PDF-'):
                    raise ValueError('expected a PDF, received different content')
            else:
                page = Page(body)
                result['title'] = page.title
                if 'text/html' not in content_type or page.title != item['title']:
                    raise ValueError(f'wrong page title: {page.title!r}')
                if fragment and unquote(fragment) not in page.ids:
                    raise ValueError(f'missing fragment: {fragment}')
            result['ok'] = True
            return result
        raise ValueError('too many redirects')
    except (ValueError, URLError, TimeoutError, OSError) as error:
        result['error'] = str(error)
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'docs/inbound-links.json').read_text())
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(check, manifest['checks']))
    report = {'checked_at': datetime.now(timezone.utc).isoformat(), 'checks': results}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + '\n')
    failures = [result for result in results if not result['ok']]
    for result in failures:
        print(f"FAIL: {result['url']}: {result['error']}")
    print(f"{'FAIL' if failures else 'PASS'}: {len(results) - len(failures)}/{len(results)} inbound links, canonical destinations, content types, titles, and fragments")
    return bool(failures)


if __name__ == '__main__':
    raise SystemExit(main())
