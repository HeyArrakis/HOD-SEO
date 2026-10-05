# House of Diams — Stage 1: Current Site Inventory

Date: 2026-09-17
Source: `https://www.houseofdiams.com/sitemap.xml` (public sitemap) + direct browser crawl of the live site. No DataForSEO (paid) calls were used in this stage, per project rules.

## Method

1. Fetched the live sitemap.xml (198 URLs) and saved it unedited to [`site/raw_sitemap.xml`](raw_sitemap.xml).
2. Classified every URL by page type from its path.
3. Individually crawled (rendered page, extracted `<title>`, `<h1>`, canonical link, meta robots, meta description) all 18 core/utility/category pages, all 10 blog articles, the 1 education article, and 8 representative product pages spanning the main product families plus known edge cases (a CMS "copy" variant, a paired numeric-ID variant, and the visible test product).
4. The remaining ~161 product pages were **not** individually crawled for title/H1/canonical — that is not practical by hand at this volume and isn't needed to complete this stage's deliverable. Their rows in `01_site_inventory.csv` carry a URL-slug-derived topic and are flagged `"not individually audited — sample-based"`. The 8 sampled PDPs all showed a consistent template (self-referencing canonical, populated title/H1, descriptive meta description), so the working assumption is that the template is consistent site-wide — this should be spot-checked again once real crawl tooling (e.g. Screaming Frog) is available, not re-derived by hand.

## No local datasets duplicated

This is the first data-gathering stage of the project. `progress.md` confirmed no prior stage had produced data yet, and `site/`, `dataforseo/`, `serp/`, `competitors/`, `clusters/`, `architecture/`, `content-strategy/`, and `exports/` were all empty before this stage. Nothing here duplicates an existing dataset.

## Deliverables produced this stage

- [`01_site_inventory.csv`](01_site_inventory.csv) — full technical inventory, all 198 sitemap URLs
- [`01_existing_content_inventory.csv`](01_existing_content_inventory.csv) — the current Education hub + its 1 live article (existing SEO asset, not a future-strategy assumption)
- [`01_existing_blog_inventory.csv`](01_existing_blog_inventory.csv) — the current Blog hub + its 10 live articles (existing SEO asset, not a future-strategy assumption)
- [`raw_sitemap.xml`](raw_sitemap.xml) — unedited raw sitemap pull

## Site structure summary

198 URLs total in the sitemap, breaking down as:

| page_type | count | notes |
|---|---|---|
| product (`/shop/*`) | 169 | Individual product detail pages (PDPs) |
| blog-article (`/blog/*`) | 10 | Current journal/blog content |
| commercial-category (`/t-bar`, `/fine-jewellery`, `/engagement-rings`, `/wedding-bands`, `/hiphop`) | 5 | Live category/collection pages |
| utility (`/faq`, `/shipping`, `/returns`, `/privacy-policy`, `/terms`) | 5 | Policy/support pages |
| commercial-listing (`/shop`, `/collection`) | 2 | Full-catalog and filtered-catalog listing views |
| commercial-brand (`/about`, `/contact`) | 2 | Brand story and contact |
| commercial-home (`/`) | 1 | Homepage |
| service-bespoke (`/bespoke`) | 1 | Custom/bespoke commissioning |
| blog-hub (`/blog`) | 1 | Blog index |
| education-hub (`/education`) | 1 | Education index |
| education-article (`/education/*`) | 1 | Current education content |

No `/wedding-bands`, `/engagement-rings`, `/fine-jewellery`, or `/t-bar` products all funnel from `/shop` as the apparent parent in nav, though the sitemap does not encode a parent relationship explicitly — parent_url in the CSV is inferred from URL structure and observed nav, not from a sitemap hierarchy (flat XML sitemaps don't carry one).

No dedicated commercial category pages exist yet for **earrings**, **necklaces/pendants**, or **bracelets** even though these are the majority of live product inventory (see next section) — all of those products currently sit only under `/shop` and `/collection` with no dedicated category URL. This is a gap to weigh once keyword demand and SERP evidence are in (per project rule: do not create a category page just because a keyword has volume — but also don't rule one out before evidence is reviewed, since three of the four biggest product groupings currently have zero dedicated category URL).

## Product catalog composition (from 169 PDP slugs)

Rough grouping by slug keywords (approximate, since not every PDP was individually audited):

- **Engagement rings / bridal sets / eternity bands / solitaires** — the largest group, roughly half of all PDPs (`engagement-ring`, `bridal-set`, `solitaire`, `eternity-band`, `halo`, etc.)
- **Earrings** (studs, hoops, huggies, drops) — second-largest group
- **Necklaces / pendants** (including t-bar pendants and charms)
- **Bracelets** (tennis bracelets, link bracelets)

## Key findings / issues to flag (not to fix — research only)

1. **`/collection` is indexable but empty.** Live render shows "0 pieces" / "No pieces match your filters" with no products. This is a filtered/browse view with a self-referencing canonical, currently thin/empty content that would offer nothing to a crawler landing on it today.
2. **`/hiphop` is a placeholder category with a visible test artifact.** The rendered page shows "Coming Soon" and a nav/filter item literally labeled **"TEST SUBCAT"** — a dev/QA leftover visible on the live, indexed page.
3. **A dedicated test product is live and indexable:** `/shop/fine-jewellery-test-product` — generic title ("Fine Jewellery Test Product"), placeholder meta description ("Stud Earrings · White Gold - House of Diams"), no real content. Flagged in the CSV as a candidate for removal/noindex ahead of relaunch (no action taken — website safety rule).
4. **Carat/size variants are modeled as separate, CMS-generated URLs, not variant selectors.** E.g. `milgrain-bezel-round-diamond-necklace-1788000835747` (1.00 ct) and `milgrain-bezel-round-diamond-necklace-1788000835747-copy-baae7d47cd58` (1.50 ct) are two distinct, correctly self-canonicalized, non-duplicate PDPs — but the second URL carries an internal CMS copy-ID rather than a clean slug. The same pattern repeats for at least 2 other product families (`floating-four-prong-diamond-necklace-*`, `emerald-horizon-diamond-pendant-*`, and a non-"copy" numeric-ID pair `round-baguette-three-stone-ring-*` / `round-diamond-split-bail-solitaire-pendant-*`). This is a URL-hygiene/architecture question for later stages (whether carat variants should live on one URL with a size selector, or on separate URLs with clean slugs) — flagged, not decided here.
5. **Category pages (`/t-bar`, `/fine-jewellery`, `/engagement-rings`, `/wedding-bands`) all carry an identical, auto-generated meta description template**: "Browse {Category} from the live catalog." — thin, non-differentiated boilerplate rather than written copy.
6. **Several pages render substantial content but have no `<h1>` tag at all**: `/about`, `/faq`, `/hiphop`. `/about` in particular has a full brand-story narrative (workshop process, founders, milestones, values) with no H1 anchoring it.
7. **Blog/Education topical overlap already exists.** The one live Education article ("GIA vs IGI: What Your Lab-Grown Diamond Report Actually Tells You") covers essentially the same certification-comparison subject as the live Blog article "IGI Certification for Lab-Grown Diamonds: What It Means" — same core topic, two different URLs/sections, no evident cross-canonical. This is exactly the kind of existing-content conflict stage 13 (existing-content decisions) needs to resolve with real keyword/SERP evidence — not resolved here.
8. **Internal overlap within the 10 blog articles themselves**: "How to Choose a Lab-Grown Diamond: The Complete Buyer's Guide," "The 4Cs of Lab-Grown Diamonds Explained," and "How to Choose a Lab-Grown Diamond Engagement Ring Online" all cover substantially the same buying-guide ground (4Cs, certification, shape, common mistakes) from slightly different angles. Whether that's 3 pages of cannibalization or legitimate intent segmentation should be settled with SERP validation, not assumed now.
9. **No `robots` meta tag was found on any crawled page** (value `null` throughout) — nothing observed is currently blocked from indexing at the meta-tag level. This was not checked at the HTTP-header or robots.txt level, and robots.txt itself was out of scope for this stage (research only, and modifying it is explicitly prohibited regardless).

None of the above were changed. This is a research record only, per the website-safety rule in `CLAUDE.md`.

## Explicit reminder for later stages

Per `CLAUDE.md`: the 10 current blog articles and the 1 current education article are **existing SEO assets to evaluate**, not the final blog/education strategy. Nothing in this inventory should be read as a recommendation to keep, cut, or expand any of this content — that comes later, from keyword demand + intent + SERP evidence + competitor gaps (stages 2–9), then a deliberate existing-content decision (stage 13) and future blog/education strategy (stages 14–15).

## Stopping point

Per instructions, work stops here. Next stage is keyword universe seeding — before any paid DataForSEO call, the US location/English language identifiers must be verified via the DataForSEO locations/languages endpoint (per `CLAUDE.md` — never hard-coded from memory).
