# 12 — Engineering Inputs (AWS migration)

Short intake for the developers. **None of these block the On-Page SEO specification**; each blocks only the implementation step shown. Until answered, every Class B action stays post-migration and is listed as awaiting engineering input. Source decisions: `10-DECISIONS-RESOLUTION-LOG.md`.

| ID | Question | Why it matters | Blocked / affected actions |
|---|---|---|---|
| E-01 | Cut-over date and content-freeze/DB-sync window? | Dating every Class B item; whether copy fixes can go earlier | All B rows; publishing of the 9 publish-ready packaged posts (BC-001 is held for F-A1) |
| E-02 | Where are page titles, meta descriptions, H1s, category names and article bodies edited — Supabase-backed CMS or in code — and does that store move to AWS? | Who applies metadata/copy and how | All metadata/copy rows |
| E-03 | Will every current URL stay identical on AWS (incl. /by-design/ paths, /blog, /education, /shop/<slug>)? | Whether the redirect map needs extra rows | Redirect map R-01…R-09; Stage 13 transitional URLs |
| E-04 | Who owns/implements the redirect map; can 1:1 301s preserve query strings and avoid chains? | R-01…R-09 delivery | Redirect rows |
| E-05 | Can sitemap.xml and robots/meta-robots be set per page (exclude empty/test pages; noindex,follow; add lastmod)? Can empty categories be auto-excluded at 0 products? | Index-control rule for 18 pages | /collection + 17 subcategories; group page C-01 |
| E-06 | Does the listing template support self-referencing canonical on ?page=N and 'Page N' in title/H1 (shop, engagement-rings, blog)? | Pagination spec | /shop, /engagement-rings, /blog |
| E-07 | Can article templates output BreadcrumbList, an Organization author, and a visible breadcrumb (Blog › Post; Education › Hub › Page)? | Article schema + byline policy | All articles (11 live + planned) |
| E-08 | Can the boilerplate FAQPage (35 pages) be removed and the FAQ block made category-specific or optional? | Schema clean-up | Category/subcategory/shop pages; /returns |
| E-09 | PDP data model: how are variants/metals represented (default variant price)? Can JSON-LD name/sku/breadcrumb be aligned with the visible page? Image host/URL plan after the Supabase/R2 move? | PDP schema + image URLs | 184 PDPs; Product/OG image fields |
| E-10 | How is USD pricing/schema guaranteed for US users and Googlebot when currency cookies are IP-based? | Offer currency | PDP Offer schema |
| E-11 | What replaces the current no-store HTML caching (CDN/cache policy)? | CWV/TTFB baseline comparison | Sitewide Class C |
| E-12 | Can a real /contact page be added and /?contact=open canonicalized to it? Can header/footer Contact link to it? | OD-09 implementation | /contact; nav |
| E-13 | Can internal links be repointed: PDP breadcrumbs 'By Design' → /engagement-rings; header menu empty children removed; Education index listing the transitional articles? | Group-page canonical and nav clean-up | C-01; header menu; /education |

## Defaults we will assume if there is no answer

* Titles/metas/H1s/category names are edited in the CMS or product data; URLs stay identical; redirects are applied at the edge or application layer with query strings preserved.
* Sitemap and robots generators are re-implemented and can exclude individual URLs.
* Listing pagination keeps `?page=N` with a self-referencing canonical (page-number titles only if the template supports them).
