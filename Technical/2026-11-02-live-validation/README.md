# Live validation — 2026-11-02 (after merging `sonder-hod-seo`)

Read-only checks after storefront `2c8071f` and admin `3666e0e` went live. Results are in `FINAL-AUDIT-2026-11-01/changes.md`, "Live check, 2 Nov".

| File | Content |
|---|---|
| `sitemap_2026-11-02.xml`, `crawl_2026-11-02.json` | 246 sitemap URLs + 20 probes |
| `deep_scan_2026-11-02.json`, `full_audit_2026-11-02.json`, `spec_comparison_2026-11-02.json` | Same scans as 1 Nov |
| `branch_items_2026-11-02.json` | `_scripts/check_branch_items.py`: sitewide text, product schema, redirects, 410s, llms.txt, article links |
| `lighthouse/` | 14 templates × mobile/desktop; ran while the text scan was still running for part of the time |
| `lighthouse_quiet/`, `lighthouse_quiet2/` | Repeat runs with nothing else running |

The Lighthouse performance numbers from this date are not reliable as a baseline: see the note in `changes.md`.
