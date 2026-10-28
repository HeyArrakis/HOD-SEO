# Live validation record — 2026-10-29 (pre-delivery audit)

Read-only audit of `https://houseofdiams.com`. Report: [`../../DEVELOPER-HANDOFF/05-FINAL-PRE-DELIVERY-MASTER-FIX-LIST-2026-10-29.md`](../../DEVELOPER-HANDOFF/05-FINAL-PRE-DELIVERY-MASTER-FIX-LIST-2026-10-29.md).

| File | Content |
|---|---|
| `sitemap_2026-10-29.xml` | Live sitemap (246 URLs; the test article, test product, `/collection`, round-rings and `/engagement-rings/by-design` are gone vs 10-28) |
| `crawl_2026-10-29.json`, `crawl_run.log` | All sitemap URLs + fixed probes (`_scripts/crawl_validate.py`) |
| `spec_comparison_2026-10-29.json` | Live title/meta/H1 vs `On-page SEO/01` |
| `targeted_probes_2026-10-29.json` | Empties, claims, hubs, 10 blogs, labels, llms.txt, PDP name vs H1, internal links (`_scripts/probe_live.py`) |
| `deep_scan_2026-10-29.json` | Visible-text claims/typos, OG/Twitter, image alt, schema fields (Product/Offer, BlogPosting), internal-link targets (`_scripts/deep_scan.py`) |
| `lighthouse/*.json`, `lighthouse/run.log` | Lighthouse 13.6.0 (incl. Agentic Browsing) on 11 templates, mobile + desktop (`_scripts/run_lighthouse.sh <lighthouse-bin> <outdir>`) |

Also checked live on 29 Oct (not saved as files): browser QA (cart, search, mobile menu, contact form, consent/GA4 dataLayer); Ahrefs Site Audit for both projects; Search Console (indexing, sitemaps, merchant listings, performance by page); GA4 (stream, events). Findings are in the report.

Next re-check: copy `_scripts/` to a new dated folder and change the sitemap path in `probe_live.py`.
