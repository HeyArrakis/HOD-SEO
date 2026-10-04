# House of Diams — US SEO Research Project

## What this is

A research project to build the complete US search keyword universe for House of Diams (luxury diamond jewellery ecommerce) and turn it into a validated site architecture, keyword-to-URL map, and content strategy — ahead of a full website rebuild.

This is research, not implementation. Nothing here edits the live site, its repo, its CMS, or its technical SEO configuration (robots.txt, sitemap.xml, redirects, metadata). See [CLAUDE.md](CLAUDE.md) for the full rules this project operates under.

## Why this exists

The website is being rebuilt and the current blog/education content is not treated as the final editorial plan — it's existing SEO assets to be evaluated (retain / rewrite / merge / redirect / retire) once real keyword, intent, and SERP evidence is in hand. The objective is maximum useful search coverage with a clean architecture, not maximum URL count.

## Workflow

```
keyword universe
  → keyword metrics
  → search intent
  → SERP validation
  → competitor gaps
  → semantic clusters
  → page opportunities
  → site architecture
  → keyword-to-URL map
  → education strategy
  → future blog strategy
  → internal linking strategy
  → content briefs
```

Outputs are numbered sequentially (01_... through 16_...) so the pipeline stays traceable end to end — see CLAUDE.md for the exact file list.

## Folder structure

- `site/` — current site inventory/crawl data (existing pages, current blog/education content as-is)
- `dataforseo/raw/` — raw API responses (untouched)
- `dataforseo/processed/` — cleaned datasets derived from raw
- `dataforseo/metrics/` — keyword metrics outputs
- `serp/raw/` — raw SERP pulls
- `serp/analysis/` — SERP intent/feature analysis
- `competitors/raw/` — raw competitor data pulls
- `competitors/analysis/` — competitor gap analysis
- `clusters/` — semantic keyword clustering outputs
- `architecture/` — information architecture and keyword-to-URL mapping
- `content-strategy/` — blog strategy, education strategy, internal linking, content briefs
- `exports/` — final deliverables for sharing

## Tracking files

- [progress.md](progress.md) — stage-by-stage status, outputs, endpoints used, actual cost, next stage
- [cost-log.csv](cost-log.csv) — every DataForSEO call: endpoint, market, request count, estimated vs. actual cost
- [decision-log.md](decision-log.md) — key research decisions and the reasoning behind them (e.g. page-type calls, URL preservation calls, cluster boundaries)

## Market settings

Location: United States. Language: English. Confirmed against DataForSEO's locations/languages endpoint before the first paid call (not hard-coded from memory).

**Confirmed 2026-09-17 (Stage 2):**
- US location name: `United States` — location_code: **2840**
- English language name: `English` — language_code: **en**
- Google organic keyword/SERP data confirmed available for US + English (1,258,076,829 keywords / 190,345,375 SERPs indexed for this location+language pair in DataForSEO Labs), alongside Bing and Amazon sources for the same pair.
- DataForSEO MCP connection: PASS. Account balance at time of check: **$50.56** (of $51.00 total deposited).

## Credentials

DataForSEO credentials live only in Claude Desktop's MCP configuration — never in this repo.

## Status

Workspace initialized. Keyword research has not started yet. See [progress.md](progress.md) for current stage.
