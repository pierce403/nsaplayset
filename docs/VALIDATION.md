# Validation — 2026-09-29

- Built successfully with the official Zola 0.21.0 Linux x86_64 release binary.
- 14 generated HTML documents, including a genuine 404 page.
- Seven documented project entries, five editorial pages, and the catalog homepage.
- All generated local links, asset references, fragments, 20 redirects, and recorded legacy routes pass `scripts/check-site.py`.
- `node --check static/catalog.js` passes.
- Filtering logic exercised against metadata parsed from the generated homepage: query-string initialization, combined search/category, empty state, reset, case-insensitive search, URL-escaped input, and category-only results all pass. This used a DOM harness, not a browser.
- No browser rendering or interaction QA was available in this environment. Responsive CSS and keyboard/accessibility affordances are implemented, but desktop/mobile visual review remains a pre-launch check.
- Cloudflare Pages local runtime (Wrangler 4.143.1): all 20 redirect statuses and destinations, homepage/project/assets responses, security headers, and unknown-path HTTP 404 passed `scripts/check-http.py`. Browser CSP enforcement, public hosting, DNS, and TLS remain unverified.
- Production and preview builds pass the same site checks. Preview project links use the preview origin; preview robots.txt and X-Robots-Tag block indexing. Production output was rebuilt afterward.
- Pinned Wrangler dependencies installed with `npm ci`; npm audit reported zero vulnerabilities.
- External source availability and historical hardware compatibility are not validated by the local checks.

## Before launch

1. Review the site in a desktop and mobile browser, including filter controls, project pages, and an unknown URL.
2. Commit and push the prepared source to the configured GitHub repository.
3. Connect Cloudflare Pages as described in README.md and configure both domain variants.
4. Run `python3 scripts/check-http.py https://nsaplayset.org` against production, then separately verify HTTP-to-HTTPS and www-to-apex redirects preserve path and query string.
5. Recover missing original assets as available. They are not required for the site build, but the historical archive remains incomplete without them.
