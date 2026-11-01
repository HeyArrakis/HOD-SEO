# Live validation — 2026-11-01 (final SEO audit)

Read-only checks for the final audit (`FINAL-AUDIT-2026-11-01/report.md` and `changes.md`).

| File | Content |
|---|---|
| `sitemap_2026-11-01.xml`, `crawl_2026-11-01.json` | 246 sitemap URLs + 20 probes |
| `spec_comparison_2026-11-01.json` | Title/meta/H1 vs `On-page SEO/01` |
| `targeted_probes_2026-11-01.json` | Empty pages, claims, hubs, 10 blogs vs packages, llms.txt, 52 links |
| `deep_scan_2026-11-01.json` | Visible text, OG tags, schema per page |
| `full_audit_2026-11-01.json` | Status codes, titles/metas/H1 lengths and duplicates, canonicals, images, word counts, schema by template, inlinks, orphans, links to uncrawled pages, TTFB, HTML size, cache headers |
| `lighthouse/*.json` | Lighthouse 13.6, 14 templates × mobile/desktop |
| `platforms_2026-11-01.md` | GSC, GA4, GTM, Ahrefs, Merchant Center, Business Profile snapshot (baseline) |
| `_scripts/` | Previous scripts + `full_audit.py`; `probe_live.py` now reads this folder's sitemap; `run_lighthouse.sh` has 14 templates |

PageSpeed Insights API: daily quota exhausted on 1 Nov, so no field data (GSC Core Web Vitals also "No data").
