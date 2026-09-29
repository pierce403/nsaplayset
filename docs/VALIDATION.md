# Validation — 2026-09-29

- Built successfully with the official Zola 0.21.0 Linux x86_64 release binary.
- 14 generated HTML documents, including a genuine 404 page.
- Seven documented project entries, five editorial pages, and the catalog homepage.
- All generated local links, asset references, fragments, 20 redirects, and recorded legacy routes pass `scripts/check-site.py`.
- `node --check static/catalog.js` passes.
- Filtering logic exercised against metadata parsed from the generated homepage: query-string initialization, combined search/category, empty state, reset, case-insensitive search, URL-escaped input, and category-only results all pass. This used a DOM harness, not a browser.
- No browser rendering or interaction QA was available in this environment. Responsive CSS and keyboard/accessibility affordances are implemented, but desktop/mobile visual review remains a pre-launch check.
- Cloudflare host configuration, actual HTTP status codes, CSP enforcement, and deployment have not been tested because nothing has been deployed.
- External source availability and historical hardware compatibility are not validated by the local checks.

## Before launch

1. Review the site in a desktop and mobile browser, including filter controls, project pages, and an unknown URL.
2. Create the GitHub repository and push the source.
3. Connect Cloudflare Pages as described in README.md and configure both domain variants.
4. Confirm the known legacy URLs resolve to their project pages, missing documents receive the documented 302, and unknown URLs return 404.
5. Recover missing original assets as available. They are not required for the site build, but the historical archive remains incomplete without them.
