# Wikipedia inbound-link audit — 2026-09-29

Started with [ANT catalog](https://en.wikipedia.org/wiki/ANT_catalog), revision 1374882568. Scope: its Playset citations and external links, immediately related Playset articles/talk pages, and the original site's navigation. No unrelated recursive crawl.

## Findings and repairs

- Wikipedia has two live homepage links, both `http://www.nsaplayset.org/`, plus two copies of the same Wayback homepage link. The live links redirect to HTTPS at the apex.
- Vice links directly to `/porcupinemasquerade`, which returned 404. ZDNet links to `/openproblems`, `/twilightvegetable`, and `/project-requirements`; Ars and Ossmann's blog link to the homepage.
- The Wayback homepage was accessible and confirmed 19 original URLs, including all fourteen projects. Nine missing project pages have been restored from the mirror and primary sources, with slashless URL redirects. Existing project pages and the two additional catalog entries remain.
- Toorcamp slide 87 prints the ANT catalog PDF URL. Three existing PDF routes previously redirected to a missing-download note; they now serve recovered original bytes. The CHUCKWAGON presentation was also recovered. `docs/downloads.json` records all four files, source URLs, sizes, and SHA-256 hashes.
- Two referenced slide decks contain image pages rather than clickable links. Printed URLs were checked separately from HTML hrefs. Pages are recorded in the manifest.

## Coverage

`docs/inbound-links.json` records 34 source documents, exact backlinks, archived original URLs, and printed slide URLs. Its 114 public checks cover the recorded destinations, HTTP/HTTPS and apex/www variants, slashless paths, one query/fragment regression case, and legacy `index.html`. They reject soft 404s, incorrect page titles, PDF URLs that return HTML, missing fragments, and redirects off the first-party hosts.

The initial 112-check snapshot had 50 failures covering nine missing project pages and four PDF destinations; variants of the same destination count as separate checks. The final inventory additionally includes the two printed/archived HTTP PDF URLs. The build validates all restored routes and original PDF hashes. Run `python3 scripts/check-inbound-links.py --output tmp/link-audit/live.json` against production after deployment.

## Third-party limitations

These destinations are outside nsaplayset.org and were not modified:

| Source | Observed result |
| --- | --- |
| `haxpo.nl/hitb2014ams-michael-ossmann/` | 404 |
| `haxpo.nl/wp-content/uploads/2014/01/D1T1-The-NSA-Playset.pdf` | 404 |
| `toorcamp.toorcon.net/talks/#34` | 404 |
| DEF CON 22 speaker page | Connection reset; not verified |
| Wireless Village speaker page | Redirected hostname has a TLS certificate mismatch; not verified |

The four mirror-local `.tgz` downloads returned 200 at the mirror; they were not found as first-party backlinks and were not republished. One is about 38 MB. No claim is made that archived hardware/software still works, or that every external link on the web was checked. No Wikipedia or publisher pages were edited.
