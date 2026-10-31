# Live validation — 2026-10-31 (after the developer's last release)

Read-only check after the developer reported his final fixes; his contract has ended. A new build is live (8 of 22 homepage JS chunks are new compared with 30 Oct). Result: `DEVELOPER-HANDOFF/05-…` was rewritten to list only the remaining items.

| File | Content |
|---|---|
| `sitemap_2026-10-31.xml`, `crawl_2026-10-31.json` | 246 sitemap URLs + probes (crawl now starts from the apex host, because `www` 301s) |
| `spec_comparison_2026-10-31.json`, `targeted_probes_2026-10-31.json` | Title/meta/H1 vs `On-page SEO/01`; blogs, labels, `llms.txt`, PDP name vs H1, internal links (unchanged from 30 Oct) |
| `deep_scan_2026-10-31.json` | Sitewide visible text claims, OG tags, schema fields per page |
| `lighthouse/*.json` | Lighthouse 13.6, 11 templates × mobile/desktop |
| `_scripts/` | Same scripts as 30 Oct; `crawl_validate.py` BASE switched to `https://houseofdiams.com` |

**Fixed since 30 Oct (developer):**
- `https://www` → apex 301.
- CloudFront Hit on `/_next/static`.
- `<lastmod>` on 246/246 sitemap URLs.
- New York address removed (schema + panel); Organization address complete.
- Footer socials fixed.
- `og:image` on all pages.
- Promo page `noindex`.
- `/contact` shows contact details.
- Ring size not pre-selected.
- Cart "1 item" / "Shape: Round".
- Flag img a11y fixed: A11y 96–100, Agentic 3/3 everywhere except the PDP.

**Still open:** see `DEVELOPER-HANDOFF/05-…` Parts C and D. Browser tests used the built-in browser for the bag (the owner's Chrome bag was not touched); the test bag was emptied.
