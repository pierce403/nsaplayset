#!/usr/bin/env python3
"""Check generated local links, fragments, assets and every declared redirect.

No network requests. Run after `zola build` with Python 3.11+.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote, urljoin
import csv
import argparse
import hashlib
import json
import tomllib

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--base-url', default='https://nsaplayset.org')
base_url = parser.parse_args().base_url.rstrip('/')
local_hosts = {'nsaplayset.org', 'www.nsaplayset.org', urlsplit(base_url).netloc}

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
errors = []

class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.ids = set()
        self.feed(text)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if key in attrs:
                self.links.append(attrs[key])

def resolve(path):
    path = unquote(path).lstrip('/')
    target = PUBLIC / path
    for candidate in (target, target / 'index.html', PUBLIC / (path + '.html')):
        if candidate.is_file():
            return candidate
    return None

redirects = {}
for line in (PUBLIC / '_redirects').read_text().splitlines():
    if not line.strip() or line.lstrip().startswith('#'):
        continue
    source, destination, status = line.split()
    assert source not in redirects, f'Duplicate redirect: {source}'
    assert status in ('301', '302'), f'Unexpected redirect status: {status}'
    redirects[source] = destination

documents = {path: Document(path.read_text()) for path in PUBLIC.rglob('*.html')}

def check_url(url, origin):
    parts = urlsplit(url)
    if parts.scheme and parts.scheme not in ('http', 'https'):
        return
    if parts.netloc and parts.netloc not in local_hosts:
        return
    path = parts.path or '/'
    fragment = parts.fragment
    visited = set()
    while path in redirects:
        if path in visited:
            errors.append(f'{origin}: redirect loop at {path}')
            return
        visited.add(path)
        destination = urlsplit(redirects[path])
        path = destination.path
        fragment = destination.fragment or fragment
    target = resolve(path)
    if not target:
        errors.append(f'{origin}: missing {path}')
    elif fragment and target in documents and unquote(fragment) not in documents[target].ids:
        errors.append(f'{origin}: missing fragment {path}#{fragment}')

assert PUBLIC.is_dir(), 'Run zola build first'
assert (PUBLIC / '404.html').is_file(), 'Cloudflare needs a real top-level 404.html'
for path, doc in documents.items():
    route = '/' + path.relative_to(PUBLIC).as_posix()
    for link in doc.links:
        check_url(urljoin(base_url + route, link), route)
for source in redirects:
    check_url(source, '_redirects')
with (ROOT / 'docs/legacy-urls.csv').open() as file:
    for row in csv.DictReader(file):
        check_url(row['path'], 'legacy-urls.csv')
for item in json.loads((ROOT / 'docs/inbound-links.json').read_text())['checks']:
    check_url(item['url'], 'inbound-links.json')
for item in json.loads((ROOT / 'docs/downloads.json').read_text()):
    target = resolve(item['path'])
    if not target:
        errors.append(f"downloads.json: missing {item['path']}")
        continue
    data = target.read_bytes()
    if len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
        errors.append(f"downloads.json: changed original bytes at {item['path']}")

resource_groups = {'video': 'videos', 'code': 'code-schematics', 'hardware': 'components', 'training': 'training'}
resources = json.loads((ROOT / 'docs/resources.json').read_text())['items']
for item in resources:
    if item['kind'] not in resource_groups or urlsplit(item['url']).scheme != 'https':
        errors.append(f"resources.json: invalid resource {item['url']}")
        continue
    for project in item['projects']:
        source = ROOT / ('content/about.md' if project == 'about' else f'content/projects/{project}.md')
        metadata = tomllib.loads(source.read_text().split('+++', 2)[1])
        fields = {key: item[key] for key in ('kind', 'label', 'url', 'note') if key in item}
        if fields not in metadata.get('extra', {}).get('resources', []):
            errors.append(f"resources.json: metadata differs for {project}: {item['url']}")
        target = resolve(f'/{project}/')
        if target not in documents or item['url'] not in documents[target].links:
            errors.append(f"resources.json: missing rendered link on {project}: {item['url']}")
        elif resource_groups[item['kind']] not in documents[target].ids:
            errors.append(f"resources.json: missing resource heading on {project}: {item['kind']}")
if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {len(documents)} HTML pages, {len(redirects)} redirects, {len(resources)} resources, local assets, fragments and legacy routes')
