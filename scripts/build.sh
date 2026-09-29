#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

version="$(cat .zola-version)"
if [[ ! -x .tools/zola ]] || [[ "$(.tools/zola --version)" != "zola $version" ]]; then
  bash scripts/install-zola.sh
fi

base_url="https://nsaplayset.org"
preview=false
if [[ -n "${CF_PAGES_BRANCH:-}" && "${CF_PAGES_BRANCH}" != main ]]; then
  : "${CF_PAGES_URL:?Cloudflare preview builds require CF_PAGES_URL}"
  base_url="$CF_PAGES_URL"
  preview=true
fi
.tools/zola build --base-url "$base_url"
if [[ "$preview" == true ]]; then
  printf 'User-agent: *\nDisallow: /\n' > public/robots.txt
  printf '\n/*\n  X-Robots-Tag: noindex\n' >> public/_headers
fi
python3 scripts/check-site.py --base-url "$base_url"
node --check static/catalog.js
