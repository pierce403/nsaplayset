# NSA Playset

A static, source-backed security research catalog built with Zola. Source: [pierce403/nsaplayset](https://github.com/pierce403/nsaplayset). Live at [nsaplayset.org](https://nsaplayset.org) on Cloudflare Pages. No backend, database, runtime npm dependencies, external fonts, or runtime API calls. Wrangler is a pinned development dependency for Cloudflare preview and deployment.

## Local development

Use Zola **0.21.0** (pinned in `.zola-version`). On Linux x86_64:

```sh
bash scripts/install-zola.sh
.tools/zola serve
```

On other systems install that version from Zola's official releases, then run `zola serve`. `config.toml` is the configuration filename supported by the pinned version.

## Build and verify

```sh
bash scripts/build.sh
```

The build installs the pinned Zola if needed, generates `public/`, and checks local links, redirects, and JavaScript syntax. Requires Linux x86_64, Bash, curl, tar, Python 3.11+, and Node.js 22+. Generated output is ignored by Git. To view the output, run `python3 -m http.server --directory public 8000` and open http://localhost:8000. Local Python serving does not apply Cloudflare `_redirects` or `_headers`; those are validated structurally by the checker and take effect on Cloudflare.

## Cloudflare Pages

Pages project `nsaplayset` is connected to `pierce403/nsaplayset`. Pushes to `main` automatically build and deploy with:

| Setting | Value |
| --- | --- |
| Production branch | `main` |
| Framework preset | None (custom build) |
| Build command | `bash scripts/build.sh` |
| Build output | `public` |
| Root directory | Repository root |

The installer pins both the version and SHA-256 of the release archive used during validation. Update both together for upgrades. The checked-in `wrangler.jsonc` declares the Pages project name and output directory. This is a Pages configuration; do not use `wrangler deploy` (the Workers command).

Production builds keep `https://nsaplayset.org` as their base URL. Non-`main` Cloudflare branches use `CF_PAGES_URL`, so project links and canonical URLs stay on the preview. Preview output also disallows crawling and adds `X-Robots-Tag: noindex`. The same build and checks run in GitHub Actions for both modes. See [Cloudflare’s Zola guide](https://developers.cloudflare.com/pages/framework-guides/deploy-a-zola-site/).

Both `nsaplayset.org` and `www.nsaplayset.org` are attached in Cloudflare with HTTPS. The active Cloudflare Redirect Rule `Redirect www to nsaplayset.org` matches `http.host eq "www.nsaplayset.org"`, redirects with 301 to `concat("https://nsaplayset.org", http.request.uri.path)`, and preserves the query string. HTTP also redirects to HTTPS. These account-level settings are managed in the Cloudflare dashboard, not by the repository. Production canonical URLs and the sitemap use `https://nsaplayset.org`.

The generated `_redirects` handles historical extensionless paths and aliases. The top-level `404.html` ensures genuine unknown URLs remain 404s rather than an SPA homepage fallback. Verify response codes and host redirects after deployment; a static build cannot validate Cloudflare account configuration.

No credentials or deployment secrets are required in this repo. GitHub Actions builds and checks the output, but does not publish it. Cloudflare builds from Git through the existing **Connect to Git** integration. Keep this integration for automatic releases.

### Local Cloudflare preview

```sh
npm ci
npm run preview
```

Open the URL printed by Wrangler. Unlike the Python server, this applies Cloudflare redirects and headers and exercises the custom 404. Wrangler requires Node.js 22+. In another terminal, run `python3 scripts/check-http.py http://127.0.0.1:8788` (adjust the port to match Wrangler). After deployment, run the same check against `https://nsaplayset.org`.

### Manual deployment to the connected Pages project

For an exceptional manual release to the existing Pages project `nsaplayset`, authenticate to the intended Cloudflare account with `npx wrangler login`, then run `npm run deploy`. Prefer the normal Git integration for releases. Never commit API tokens.

## Add or edit a project

Copy an existing file under `content/projects/`. Set `title`, `description`, `weight`, and a root-level `path` such as `twilightvegetable`. Keep the `extra` metadata used by `templates/project.html`: number, category, interface, code, year, credits, and sources. Filter categories are generated from the project metadata.

Write the body in Markdown. Link to primary sources, credit original work, and distinguish historical claims from current tested status. The homepage is generated from all project pages automatically; search runs locally in the browser and all entries remain readable without JavaScript.

## Legacy URL recovery

`docs/legacy-urls.csv` records path provenance. `static/_redirects` is the routing source of truth. Do not infer original paths merely by lowercasing project names. HALIBUTDUGOUT and ALLOYVIPER are new routes for historically documented projects.

The catalog contains the fourteen projects in the original navigation plus HALIBUTDUGOUT and ALLOYVIPER. The original site wordmark and pencil illustration, plus 11 project photographs and diagrams, have been recovered. Image origins, credits, dimensions, and hashes are recorded in `docs/site-graphics.json` and `docs/project-graphics.json`. Four original PDFs are served at their historical mirror paths, with provenance and byte hashes in `docs/downloads.json`.

The requirements headings and Open Problems research list were recovered from the old site; requirements explanations are concise summaries. Original contributor names and project summaries have linked provenance. No license for third-party hardware, code, or media is implied; upstream licenses apply. A license for the new site code has intentionally not been selected on the owner's behalf.

## Inbound-link audit

The [audit report](docs/LINK_AUDIT.md) records Wikipedia, its Playset references, their immediate related sources, and the old-site navigation. `docs/inbound-links.json` preserves observed URLs, archived/printed URLs, source availability, and 114 bounded first-party checks. The build checks that these paths still exist and that restored PDF hashes match their sources.

After deployment, verify host redirects, status codes, destination titles, PDF responses, and fragments:

```sh
python3 scripts/check-inbound-links.py --output tmp/link-audit/live.json
```

This checks only the recorded first-party URLs. It does not crawl third-party sites or run periodically.

## Contributing code

Clone `https://github.com/pierce403/nsaplayset.git`, edit the Markdown or templates, and run the checks above. Do not commit `public/` or `.tools/`.
