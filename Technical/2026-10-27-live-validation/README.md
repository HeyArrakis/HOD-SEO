# Live validation record — 2026-10-27 (post-developer fixes)

Read-only re-check of `https://houseofdiams.com` after the developer reported the on-page/QA batch complete. Report: [`../../DEVELOPER-HANDOFF/04-IMPLEMENTATION-VERIFICATION-2026-10-27.md`](../../DEVELOPER-HANDOFF/04-IMPLEMENTATION-VERIFICATION-2026-10-27.md).

| File | Content |
|---|---|
| `sitemap_2026-10-27.xml` | Live sitemap (248 URLs, apex host) |
| `crawl_2026-10-27.json` | 274 responses (all sitemap URLs + probes) |
| `crawl_log_2026-10-27.txt` | Status line per URL |
| `spec_comparison_2026-10-27.json` | Live title/meta/H1 vs `On-page SEO/01-ON-PAGE-SEO-MASTER.csv`, per row |
| `targeted_probes_2026-10-27.json` | Empty listings, trust/claim text, Education hubs, the ten blogs vs packages, nav labels, llms.txt, PDP name vs H1, internal links |
| `_scripts/` | `crawl_validate.py <outdir> <date>`, `verify_spec.py <crawl> <out>`, `probe_2026-10-27.py <crawl> <out>`, older `probe2.py` |

Browser retests (QA bugs, cart/checkout text, homepage rendered text) were done in the built-in browser on 2026-10-27; results are recorded in the report (§5). Method limits: one vantage point (India), desktop width, no payment step, no CWV measurement. The 2026-10-24 and 2026-10-09 snapshots are unchanged.
