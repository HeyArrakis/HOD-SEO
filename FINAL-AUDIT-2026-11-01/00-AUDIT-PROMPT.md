# Final SEO, performance and AI-visibility audit — House of Diams (prompt)

*Refined from the owner's request of 2026-11-01. This is the brief the audit follows. The two outputs are `report.md` (scores) and `changes.md` (every fix, for the developer).*

## Role

Act as three people at once:

- **A principal SEO strategist** for luxury e-commerce, covering technical, on-page, content, local, off-page and AI search (Google AI Overviews and AI Mode, ChatGPT, Perplexity, Gemini).
- **A site architect** who knows how keyword ownership, information architecture, internal links and structured data fit together.
- **A senior web-performance and full-stack engineer** for Next.js App Router on AWS (CloudFront, nginx, EC2, RDS, S3), who can read the storefront and admin code and give exact file-level fixes.

Work like an auditor: every finding needs evidence (URL, file and line, screenshot, or tool output), an impact, a fix and a "done when" check. Never guess.

## Site and context

- Site: **https://houseofdiams.com** (apex is canonical; `www` 301s). Market: United States, US English. Luxury lab-grown diamond jewelry, bespoke, and a Surat (India) workshop with a USA presence.
- Code (read-only, cloned 2026-11-01):
  - `storefront/` = `House-of-diams/aws-houseofdiams-storefront`
  - `admin/` = `House-of-diams-admin-`
  - Merging to `main` deploys production.
- Admin CMS: `manage.houseofdiams.com`.
- The project's own sources of truth (CLAUDE.md §3), which the audit must check the live site against:
  - Keyword ownership: Stage 15, plus `On-page SEO/10-COMMERCIAL-KEYWORD-ASSIGNMENTS.csv`.
  - On-page specs: `On-page SEO/01`, `03`–`07`.
  - Internal links: `On-page SEO/05-INTERNAL-LINK-IMPLEMENTATION.csv`.
  - Content architecture: Stage 12/14.
  - Blog calendar and the 10 blog packages.
  - Content briefs and boundaries: Stage 19.
  - SERP, PAA and AIO research: Stages 8, 17, 18, 18.5.
  - Clusters: Stage 11.
  - Competitor gap: Stage 9.
  - Backlink plan: `Off-page SEO/`.
  - Confirmed business facts: `confirmed_business_facts.md`, including the 2026-11-01 answers.
  - Open developer items: `DEVELOPER-HANDOFF/05`.

## Rules

1. **Read-only on the live site and the tools.** Use GET requests only. Submit no forms, buy nothing, change no settings in GSC, GA4, Ahrefs, Merchant Center or the Business Profile, and run no paid DataForSEO calls. Cart tests use the built-in browser and the bag is emptied afterwards.
2. **Only confirmed facts.** Any claim on the site that the facts file does not support is a finding.
3. **Specs first.** If the live site differs from an approved spec, report it as a defect. Re-decide nothing that is already decided; flag real conflicts instead.
4. **Google facts as the project established them.** FAQ rich results are gone; `llms.txt` is not a Google signal; field Core Web Vitals (CrUX) count, lab scores are diagnostics; there are no guaranteed rankings or AI citations.
5. **Never skip an area.** If something can't be checked (no access, no data), say so, mark it "not measured", and say what is needed.
6. Plain language in the outputs. Each fix is a concrete instruction with a file, field or setting.

## Scope (all of it)

1. **Technical SEO**
   - Status codes for every sitemap URL plus probes; redirects, chains and loops.
   - Canonicals, `noindex` / `X-Robots-Tag`, `robots.txt` (including AI bots), XML sitemap (coverage, `lastmod`, no non-200 or non-canonical URLs), `llms.txt` / `llms-full.txt`.
   - Pagination and faceted URLs, hreflang/currency handling for Googlebot, HTTPS/HSTS, security headers, caching, JS rendering, 404 handling, media host, orphan pages, crawl depth.
2. **Performance**
   - Lighthouse lab on every template (mobile and desktop).
   - PageSpeed Insights field data (CrUX: LCP, INP, CLS) for the origin and key URLs.
   - Page weight, images, video, fonts, JS and CSS, TTFB, caching.
3. **On-page SEO**
   - On every page: title, meta description, H1 and heading outline, length limits, duplicates, keyword-owner match against the spec, image alt, Open Graph and Twitter tags, URL hygiene, content depth, thin or duplicate pages.
4. **Content and keyword strategy**
   - Each owner keyword is on its owner page; no cannibalization.
   - The 10 blog packages are live and correct; Education pages; calendar items due or overdue.
   - Search intent and SERP fit; PAA and AIO coverage of the top topics.
   - E-E-A-T: author and entity, sources, trust pages; freshness.
5. **Internal linking and architecture**
   - The 52 specified links; breadcrumbs; navigation and footer; hub ↔ spoke links; anchor quality; links to empty or noindex pages.
6. **Structured data**
   - On every template: Organization, WebSite, BreadcrumbList, Product/Offer/merchant fields (price, availability, shipping, returns, images, GTIN or brand), ItemList, BlogPosting/Article, FAQPage only on `/faq`.
   - Validity, consistency with visible text, and facts.
7. **AI search visibility (GEO/AEO)**
   - AI crawler access, `llms.txt` quality, entity consistency (name, founders, address, sameAs), answer-first content, quotable facts and statistics.
   - Brand SERP and knowledge panel; whether the brand shows in AI answers where measurable.
8. **Local SEO and entity**
   - Google Business Profile (exists? category, NAP, hours, photos, reviews).
   - NAP consistency on the site, in schema and on social profiles; citations; the USA presence without an address.
9. **Off-page**
   - Ahrefs: DR, referring domains, backlinks, anchors, toxic or spam links, lost links, competitors.
   - Status of the backlink plan; brand mentions.
10. **Measurement**
    - Google Search Console: performance, indexing, sitemaps, CWV, enhancements (merchant listings, product snippets, breadcrumbs), manual actions, links, the www vs apex property.
    - GA4 and GTM: tags firing, consent mode v2, ecommerce events, conversions, data quality.
    - Merchant Center: feed, approvals and disapprovals, free listings, shipping and returns settings.
    - Bing Webmaster Tools and IndexNow (exists?).
11. **UX, accessibility, trust and QA**
    - Lighthouse accessibility, best practices and agentic scores.
    - Console errors, broken links and images, forms (not submitted), cart and checkout up to payment (not paid).
    - Wording that contradicts the facts, policy pages, cookie consent.
    - Admin errors that affect SEO (missing fields, wrong slugs, uploads).

## Scoring (report.md)

Each area gets a score out of 100. The **total SEO score** is the weighted average. Weights follow what most moves organic and AI visibility for an e-commerce site:

| Area | Weight |
|---|---|
| Technical SEO (crawl, index, canonicals, sitemaps, robots, redirects, rendering) | 18 % |
| Performance and Core Web Vitals | 12 % |
| On-page SEO (titles, metas, headings, keyword fit, images) | 14 % |
| Content quality and keyword strategy (ownership, intent, depth, E-E-A-T, blogs, education) | 14 % |
| Internal linking and site architecture | 8 % |
| Structured data and rich results (including Merchant fields) | 8 % |
| AI search visibility (GEO/AEO) | 7 % |
| Off-page and backlinks | 7 % |
| Local SEO and entity (GBP, NAP, citations) | 4 % |
| Measurement and tracking (GSC, GA4/GTM, Merchant Center) | 4 % |
| UX, accessibility, trust and QA | 4 % |

**Platform scorecards** (each out of 100, reported separately, not part of the weighted total):
- Google Search Console health
- GA4 tracking
- Merchant Center
- Ahrefs site health and authority
- Lighthouse (lab) and PageSpeed (field)
- AI readiness

Each score shows how it was worked out. Search results (clicks, impressions, positions) are reported as KPIs with a baseline, because they lag the fixes.

## changes.md (the developer hand-over)

One file listing every fix found anywhere in the project. It supersedes `DEVELOPER-HANDOFF/05`.

- **Grouping:** by owner.
  - A: storefront code
  - B: admin code
  - C: server, AWS and infrastructure
  - D: tracking and tool configuration (GTM, GA4, GSC, Merchant Center, Bing)
  - E: CMS content in the admin (Claude can make these with the owner's OK)
  - F: owner decisions and facts still needed
- **Each item:** ID, priority (P0 now, P1 next, P2 later), page or file, what is wrong (with evidence), the exact fix, and a "done when" check.
- **Order:** P0 first. A short checklist goes at the top.
