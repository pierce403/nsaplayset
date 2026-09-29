#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
version="$(cat .zola-version)"
if [[ "$(uname -s)" != Linux || "$(uname -m)" != x86_64 ]]; then
  echo 'This helper installs the pinned Linux x86_64 binary. Install Zola for your platform from https://www.getzola.org/documentation/getting-started/installation/' >&2
  exit 1
fi
mkdir -p .tools
archive="$(mktemp)"
trap 'rm -f "$archive"' EXIT
curl --fail --location --silent --show-error --retry 2 \
  "https://github.com/getzola/zola/releases/download/v${version}/zola-v${version}-x86_64-unknown-linux-gnu.tar.gz" -o "$archive"
printf '%s  %s\n' '5c37a8f706567d6cad3f0dbc0eaebe3b9591cc301bd67089e5ddc0d0401732d6' "$archive" | sha256sum --check
tar --no-same-owner -xzf "$archive" -C .tools zola
.tools/zola --version
