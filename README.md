# NSA Playset

A static, source-backed security research catalog built with Zola. Source: [pierce403/nsaplayset](https://github.com/pierce403/nsaplayset). Prepared for Cloudflare Pages. No backend, database, npm dependencies, external fonts, analytics, or runtime API calls.

## Local development

Use Zola **0.21.0** (pinned in `.zola-version`). On Linux x86_64:

```sh
bash scripts/install-zola.sh
.tools/zola serve
```

On other systems install that version from Zola's official releases, then run `zola serve`. `config.toml` is the configuration filename supported by the pinned version.

## Build and verify

```sh
.tools/zola build
python3 scripts/check-site.py
node --check static/catalog.js
```

Output is `public/`. The delivery ZIP includes a prebuilt copy for review, but generated output is ignored by Git. To view that copy without installing Zola, run `python3 -m http.server --directory public 8000` and open http://localhost:8000. Local Python serving does not apply Cloudflare `_redirects` or `_headers`; those are validated structurally by the checker and take effect on Cloudflare.

## Cloudflare Pages

Connect `pierce403/nsaplayset` with:

| Setting | Value |
| --- | --- |
| Production branch | `main` |
| Build command | `bash scripts/install-zola.sh && .tools/zola build` |
| Build output | `public` |
| Root directory | Repository root |

The installer pins both the version and SHA-256 of the release archive used during validation. Update both together for upgrades. A compatible preinstalled Zola can instead use `zola build`.

Set up `nsaplayset.org` and `www.nsaplayset.org` in Cloudflare, including certificates for both. Use a Cloudflare Redirect Rule from `www` to the apex domain that preserves path and query string; also enable HTTP-to-HTTPS redirection. These account-level changes are **not applied** by this repository. Production canonical URLs and the sitemap use `https://nsaplayset.org`.

The generated `_redirects` handles historical extensionless paths and temporary missing-asset routes. The top-level `404.html` ensures genuine unknown URLs remain 404s rather than an SPA homepage fallback. Verify response codes and host redirects after deployment; a static build cannot validate Cloudflare account configuration.

No credentials or deployment secrets are required in this repo. GitHub Actions builds and checks the output, but does not publish it. Cloudflare deployment is configured separately.

## Add or edit a project

Copy an existing file under `content/projects/`. Set `title`, `description`, `weight`, and a root-level `path` such as `twilightvegetable`. Keep the `extra` metadata used by `templates/project.html`: number, category, interface, code, year, credits, and sources. Supported filter categories are the four original categories in `templates/index.html`.

Write the body in Markdown. Link to primary sources, credit original work, and distinguish historical claims from current tested status. The homepage is generated from all project pages automatically; search runs locally in the browser and all entries remain readable without JavaScript.

## Legacy URL recovery

`docs/legacy-urls.csv` records path provenance. `static/_redirects` is the routing source of truth. Do not infer original paths merely by lowercasing project names. HALIBUTDUGOUT and ALLOYVIPER are new routes for historically documented projects.

Recovery remains partial: seven project records are included; additional project names are listed on Open Problems without invented specifications. Original photos and downloadable assets have not been recovered. Three known download paths temporarily redirect to the archive explanation with **302**, not to unrelated replacement documents. Restore exact files under `static/` and remove the matching redirect when recovered.

The project requirements and open-problems pages are new editorial guidance, not recovered copies. Original contributor names and project summaries have linked provenance. No license for third-party hardware, code, or media is implied; upstream licenses apply. A license for the new site code has intentionally not been selected on the owner's behalf.

## Contributing code

Clone `https://github.com/pierce403/nsaplayset.git`, edit the Markdown or templates, and run the checks above. Do not commit `public/` or `.tools/`.
