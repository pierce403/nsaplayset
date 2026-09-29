# Validation — 2026-09-29

- Built successfully with the official Zola 0.21.0 Linux x86_64 release binary.
- 14 generated HTML documents, including a genuine 404 page.
- Seven documented project entries, five editorial pages, and the catalog homepage.
- All generated local links, asset references, fragments, 20 redirects, and recorded legacy routes pass `scripts/check-site.py`.
- `node --check static/catalog.js` passes.
- Filtering logic exercised against metadata parsed from the generated homepage: query-string initialization, combined search/category, empty state, reset, case-insensitive search, URL-escaped input, and category-only results all pass. This used a DOM harness, not a browser.
- Live desktop homepage rendering was inspected in Brave. Search for `twilight` returned one project, and Clear filters restored all seven. Mobile layout and comprehensive accessibility review remain unverified.
- Cloudflare Pages local runtime (Wrangler 4.143.1): all 20 redirect statuses and destinations, homepage/project/assets responses, security headers, and unknown-path HTTP 404 passed `scripts/check-http.py`.
- Production and preview builds pass the same site checks. Preview project links use the preview origin; preview robots.txt and X-Robots-Tag block indexing. Production output was rebuilt afterward.
- Pinned Wrangler dependencies installed with `npm ci`; npm audit reported zero vulnerabilities.
- External source availability and historical hardware compatibility are not validated by the local checks.

## Production launch

- Initial Git deployment: commit `89a8bf0be865d889245940a937cc39741b8ed8d9`, Pages deployment `05f45704-096d-458f-b12e-ed4f5f42aaa3`.
- Pages project `nsaplayset` is connected to `pierce403/nsaplayset`, production branch `main`, with automatic deployments enabled.
- Public `https://nsaplayset.org` and `https://nsaplayset.pages.dev` pass `scripts/check-http.py`: all 20 redirect statuses and destinations, representative HTML/assets, security headers, and genuine HTTP 404.
- Apex and www HTTPS certificates validate. HTTP apex, HTTP www, and HTTPS www return 301 to HTTPS apex while preserving `/twilightvegetable/?check=redirect%20test&x=1`.
- Public homepage, `site.css`, and `catalog.js` match local production output byte-for-byte by SHA-256.
- The HTTP checker identifies itself with a project User-Agent because Cloudflare rejects Python's default User-Agent with error 1010. No Cloudflare security controls were disabled.

## Remaining editorial work

Recover missing original assets as available. They are not required for the site build, but the historical archive remains incomplete without them. External source availability and historical hardware compatibility are outside these deployment checks.

## Original graphics and pencil aesthetic

- Recovered two original site graphics from the public homepage mirror and 11 original project images from upstream sources. Every asset has a local path, source URL, dimensions, credit, and SHA-256 in `docs/site-graphics.json` or `docs/project-graphics.json`.
- The logo and homepage drawing retain their original bytes. Selected original hardware photos appear as small catalog previews and all 11 project images appear in credited project galleries. No generated replacement graphics were used.
- The original `/customLogo.gif` and `/hackrf-kid.png` paths redirect to the locally hosted images; the original logo's data is PNG despite its historical `.gif` name. There are now 22 declared redirects.
- White paper, graphite rules, serif headings, and simpler catalog rows replace the previous block design. Source photos and board drawings retain their colors.
- Checked the homepage and project gallery at a 390-pixel mobile viewport and the homepage at 1280 pixels. No horizontal overflow; search, combined-filter empty state, and reset work. Images remain legible when a browser dark-theme override is applied.
- Source PDFs were inspected to verify image extraction. One photograph required rendering its PDF image bounds to preserve the source colors; that exception is documented in its provenance entry.

## Original copy restoration

- Removed the added slogans, illustration caption, contribution banner, and repeated editorial paragraphs from project pages.
- Reused the original homepage mission and project descriptions from the GBPPR mirror; HALIBUTDUGOUT and ALLOYVIPER descriptions come from the author's overview. Restored the original requirements headings and Open Problems category/item list.
- Preserved image credits and source links. Added the missing original credits for Loki (Nick Jacobsen) and Miles Crabill.
- Production build and generated-link checks pass for all 14 HTML pages and 22 redirects. Inspected the revised homepage at mobile and desktop widths.

## Wikipedia backlink recovery

- Audited 34 bounded source documents; recorded exact, printed, and archived URLs in `docs/inbound-links.json`. Five external sources were unavailable (three 404s, one connection reset, one TLS hostname mismatch).
- Restored nine missing project pages and four original PDF files. All fourteen projects from the original navigation are now present, alongside HALIBUTDUGOUT and ALLOYVIPER.
- Build checks pass for 23 HTML documents and 28 redirects. The build also verifies every inbound route and SHA-256 hashes of the recovered PDFs.
- Local Pages HTTP checks pass for all 28 redirects, existing pages/assets, security headers, and real 404s. Browser checks confirmed the restored PORCUPINEMASQUERADE page and Active Radio Injection filter (2 of 16 projects).
- `scripts/check-inbound-links.py` provides 114 public checks for exact destinations, host/protocol variants, content types, titles, query preservation, and fragments. Initial live failures are documented in `docs/LINK_AUDIT.md`; rerun after deployment for current results.
