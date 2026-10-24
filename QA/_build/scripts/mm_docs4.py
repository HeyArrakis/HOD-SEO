import sys; sys.path.insert(0, ".")
from mm_docs import *


def isY(r, col):
    return r[col] == "Y"


def doc05():
    A_ = []
    A = A_.append
    A("# 05 — On-Page Optimization Backlog (input to the NEXT SEO phase)")
    A(f"\nGenerated {TODAY}. Everything below is a **recommendation** drawn from the master map (`01-…csv`); no page has been edited. Titles/metas are drafts that must be fact-checked (HOD claims such as certification, shipping and warranty are unconfirmed) and re-validated after the commercial keyword decision (D-19). The site template appends ` | House of Diams` to titles; recommended titles below are the *rendered* length where marked. US spelling is used in drafts; the jewelry/jewellery label decision is open (Stage 12 D-15).\n")
    A("**Timing key:** **A** prepare now · **B** apply after AWS · **C** verify after AWS. Priorities are from the CSV.\n")
    live_opt = [r for r in live if isY(r, "Flag: Metadata Opp")]
    # ---------------------------------------------------------- 1 titles
    A("## 1. Title optimization\n")
    A(f"{len(live_opt)} live pages have a title/meta opportunity. Pattern issues: homepage has no brand; {boiler_meta} category/subcategory pages use `X | Parent | House of Diams` with typos inherited from slugs ('Solitare', 'Anniversay', lower-case 'chain & Link', 'T- BAR'); {len(pdp_long)} PDP titles exceed 60 characters; article titles are 55–75 characters with the brand suffix.\n")
    A(table(["ID", "Page", "Current title", "Recommended title (draft)", "Pri."], [[r["Row ID"].replace("SUB:", ""), rid_url(r), short(r["Current SEO Title"], 80), short(r["Recommended SEO Title"], 100), r["Priority"]] for r in live_opt if not r["Recommended SEO Title"].startswith(("No change", "—", "(remove"))]))
    A("\n**Planned pages (title direction only — finalise when the article is written):**\n")
    A(table(["ID", "Calendar date", "Title direction"], [[r["Row ID"], (re.search(r"calendar date (\S+)", r["Status"]) or [None, "—"])[1] if re.search(r"calendar date (\S+)", r["Status"]) else "—", short(r["Recommended SEO Title"], 110)] for r in planned]))
    # ---------------------------------------------------------- 2 meta
    A("\n## 2. Meta description optimization\n")
    A(f"{boiler_meta} non-PDP pages carry boilerplate metas ('Browse X in Y.', 'from the live catalog'); 54 non-PDP metas are under 70 characters; {len(pdp_plc)} PDPs have placeholder metas. Article metas are the first lines of the article body (long; truncated in SERPs). Target: answer-first, ≤155 characters, only confirmed claims.\n")
    A(table(["ID", "Page", "Current meta", "Recommended meta (draft)"], [[r["Row ID"].replace("SUB:", ""), rid_url(r), short(r["Current Meta Description"], 90), short(r["Recommended Meta Description"], 170)] for r in live_opt if not r["Recommended Meta Description"].startswith(("—", "Template"))]))
    A("\nPDPs: replace the 6 placeholder metas and the duplicated metas first (list in `06-PDP-AUDIT-APPENDIX.csv`, column *Flags*). Planned articles: meta descriptions are written with the article (10 already approved in `blogs/bc-*/seo-metadata.md`).\n")
    # ---------------------------------------------------------- 3 H1
    A("## 3. H1 optimization\n")
    A("All 256 sitemap pages have exactly one H1. Opportunities are wording, not presence: hub H1s 'Explore <Category>' (generic), the homepage tagline H1, the FAQ H1 ('How May We Help You?'), the blog hub H1 ('Stories…') vs its title ('Blog'), and slug-typo H1s ('Solitare').\n")
    h1 = [r for r in live if isY(r, "Flag: H1 Opp") and not r["Recommended H1"].startswith(("—", "Keep"))]
    A(table(["ID", "Page", "Current H1", "Recommended H1 (draft)"], [[r["Row ID"].replace("SUB:", ""), rid_url(r), short(r["Current H1"], 60), short(r["Recommended H1"], 110)] for r in h1]))
    # ---------------------------------------------------------- 4 content
    A("\n## 4. Content expansion\n")
    ce = [r for r in live if r["Recommended Action"] in ("OPTIMIZE", "EXPAND") and r["Row Group"] in ("CORE LIVE", "HUBS", "COMMERCIAL CATEGORY", "EXISTING ARTICLES (Education-owned)", "PRODUCT PAGES")]
    A(table(["ID", "Page", "Content / section changes", "Pri."], [[r["Row ID"], rid_url(r), short(r["Recommended Content/Section Changes"], 420), r["Priority"]] for r in ce]))
    A("\n**Subcategories (40 rows):** populated pages need 80–150 words of unique intro + a link to the Education owner; empty pages need a noindex/populate decision first (see CSV). **Planned pages** follow the Stage 19 briefs (`19_content_briefs.csv`) — 20 new Education pages, 4 without a brief.\n")
    # ---------------------------------------------------------- 5 entity
    A("## 5. Entity clarification\n")
    ent = [r for r in rows if r["Entity Clarity Needed?"].startswith("YES") and r["Row Group"] in LIVE_G]
    A(table(["ID", "Page", "Entities", "Clarification needed"], [[r["Row ID"].replace("SUB:", ""), rid_url(r), short(r["Important Entities"], 120), short(r["Entity Clarity Needed?"], 160)] for r in ent]))
    A("\n**Site-wide entity facts to make consistent (source of truth needed from HOD):** brand description; founders' names and roles ('Akshar Korat, co-founder' on About vs 'Krish Babriya, Co-founder' bylines); locations (Surat workshop, New York office at 36 W 44th St); contact email (info@ vs Admin@ on /returns); phone (+91 only); certification lab(s) (IGI vs GIA); warranty, shipping and returns terms; whether HOD sells natural diamonds (Stage 12: unknown).\n")
    # ---------------------------------------------------------- 6 links
    A("## 6. Internal linking\n")
    A("### 6a. Live pages missing Stage 16 REQUIRED outgoing links to live targets (initial HTML, any position incl. global nav)\n")
    gaps = []
    for r in live:
        pid = r["Registry/Calendar ID"]
        if pid not in L.links_req or not r["URL"].startswith(BASE):
            continue
        path = path_of(r["URL"])
        c = cr(path)
        if not c or "internal_links" not in c:
            continue
        miss, ok = H.missing_required_out(pid, c["internal_links"], path)
        if miss:
            gaps.append([pid, path, ", ".join(H.disp(x) for x in miss)])
    A(table(["Page ID", "Page", "Missing REQUIRED outgoing links (live targets)"], gaps))
    A("\n### 6b. Template / global-link items\n")
    for x in [
        "Header mega-menu links to filter-parameter URLs (`/engagement-rings?shape=…`, `?metal=…`) — they are `noindex, follow` + canonical to the parent, which is correct; keep that behaviour on AWS. Consider whether crawlable parameter links in the nav dilute internal-link signals (decision for engineering).",
        "Header/footer 'Contact' points to `/contact` (307 → modal). Update link targets if a real contact page is chosen.",
        "Header nav exposes empty subcategories (tennis necklace, initials, tennis earrings, personalized & charm, For Him, Hip Hop) — remove from nav or populate (D-13).",
        "Education hub lists 1 of 11 Education-owned articles; blog hub lists all 10 blog articles — align with Stage 14 hub structure.",
        "Add breadcrumb component to articles (BreadcrumbList + visible breadcrumb): 'Journal › Post' / 'Education › Hub › Page'.",
    ]:
        A(f"- {x}")
    A("\n### 6c. Links that must ship with each planned page (Stage 16 `LINKING_REQUIREMENT_AT_LAUNCH`)\n")
    rq = []
    for r in planned:
        pid = r["Registry/Calendar ID"]
        lr = L.links_req.get(pid)
        if lr:
            rq.append([pid, len(H.parse_ids(lr["incoming_required"])), len(H.parse_ids(lr["outgoing_required"])), short(lr["launch_linking_requirement"], 110)])
    A(table(["Page", "REQUIRED in", "REQUIRED out", "Requirement"], rq))
    A("\nBlog posts: every post needs hub ↔ post links and the Education owners named in its calendar `internal_link_targets` (recorded in each CSV row, *Recommended Internal Links OUT*). Anchor guidance per target is in `architecture/16_anchor_strategy.csv` (descriptive anchors; exact-match at most once per page; never bare head terms).\n")
    # ---------------------------------------------------------- 7 schema
    A("## 7. Schema\n")
    A("Principle: mark up only what the page visibly shows. Google does not require special schema for AI features; FAQ rich results were deprecated 2026-05-08 (VERIFICATION_AUDIT_2026-10-04) — don't invest in FAQPage/HowTo; QAPage is invalid for site-authored FAQs.\n")
    A(table(["Page type", "Current (live crawl)", "Recommended", "Timing"], [
        ["Sitewide", "Organization + ContactPoint + PostalAddress (Surat IN, New York US) on every page", "Keep; add `sameAs` (Instagram, Pinterest), `@id`; founder/foundingDate only when confirmed; verify logo spec; keep one telephone/email policy", "B / C"],
        ["Homepage", "Organization only", "Optional WebSite; no Product/FAQ", "B"],
        ["Category / subcategory / shop", "BreadcrumbList + Organization; **FAQPage on 35 pages (boilerplate repeated)**", "BreadcrumbList; retire boilerplate FAQPage (no feature) or make it category-specific and visible", "B"],
        ["PDP (184)", "Product + Offer + Brand + BreadcrumbList; images on Supabase/R2 hosts; no ratings", "Keep; complete material/size/stone attributes; add shipping/return details only when policies are final; update image URLs after AWS; never add fake reviews", "B / C"],
        ["Articles (blog + education)", "BlogPosting + Person author + ImageObject + WebPage; no BreadcrumbList", "Add BreadcrumbList; one author policy (Organization or a real named expert); keep ISO dates; no FAQPage/HowTo", "B"],
        ["About / Contact", "Organization only", "AboutPage / ContactPage optional; BreadcrumbList", "B"],
        ["FAQ / Returns", "FAQPage (on /returns attached to non-FAQ body)", "WebPage + BreadcrumbList; MerchantReturnPolicy once terms are final", "B"],
        ["Bespoke", "Organization only", "BreadcrumbList; Service optional (no Google feature)", "B"],
    ]))
    A("\nValidation list (after AWS, with Rich Results Test + Schema.org validator): home, 1 category, 1 subcategory, 3 PDPs (different categories), 2 articles, /faq, /returns, /about.\n")
    # ---------------------------------------------------------- 8 images
    A("## 8. Image / alt text\n")
    tot_img = sum(r.get("img_count", 0) for r in crawl.values() if r["url"] in sitemap_urls and "/shop/" not in r["url"] and "img_count" in r)
    tot_no = sum(r.get("img_no_alt", 0) for r in crawl.values() if r["url"] in sitemap_urls and "/shop/" not in r["url"] and "img_count" in r)
    ptot = sum(r.get("img_count", 0) for r in crawl.values() if r["url"] in sitemap_urls and "/shop/" in r["url"] and "img_count" in r)
    pno = sum(r.get("img_no_alt", 0) for r in crawl.values() if r["url"] in sitemap_urls and "/shop/" in r["url"] and "img_count" in r)
    A(f"- Initial HTML contains {tot_img:,} `<img>` tags on non-PDP pages ({tot_no:,} without alt) and {ptot:,} on PDPs ({pno:,} without alt). Counts include UI icons and lazy-loaded gallery images, so treat as a **flag to audit the rendered DOM**, not a defect count.\n- Rules: product images = `<name>, <view>`; hub/hero images = what the picture shows; no keyword stuffing; decorative icons `alt=\"\"`. Articles: descriptive alt per diagram/chart (Stage 19 visuals); real HOD photography for craft/bespoke posts (image-requirements.md in each draft package).\n- AWS: image URLs in Product/BlogPosting schema, OG tags and `/llms.txt` currently point at Supabase storage and `*.r2.dev` hosts; plan stable CDN URLs and redirects for already-indexed images.\n")
    # ---------------------------------------------------------- 9 AEO
    A("## 9. AEO (answer engine / answer-first)\n")
    A("Use existing PAA/AIO research; answer first, then explain; map questions into headings or answer blocks — no FAQ padding.\n")
    aeo = [r for r in live if isY(r, "Flag: AEO Opp")]
    A(table(["ID", "Page", "Questions to answer (from Stage 17/18 / PAA)", "Coverage"], [[r["Row ID"], rid_url(r), short(r["Primary Questions to Answer"], 190), short(r["PAA/Question Coverage Needed?"], 110)] for r in aeo]))
    A(f"\n**Planned pages ({len(planned)}):** each CSV row lists the questions and the answer-first format hint; AI Overview appears on most calendar SERPs (round-2/final-consolidation research). Priority AEO pages by demand: ring size chart (165,000), diamond shapes (60,500), diamond cut (60,500), diamond clarity chart (33,100), 10 year anniversary gift (33,100), how to tell if a diamond is real (18,100).\n")
    # ---------------------------------------------------------- 10 GEO
    A("## 10. GEO / entity & trust signals\n")
    A("Treated as part of SEO (Google: no separate algorithm): make content understandable, retrievable and attributable.\n")
    geo = [r for r in live if isY(r, "Flag: GEO/Entity Opp")]
    A(table(["ID", "Page", "Opportunity"], [[r["Row ID"], rid_url(r), short(r["GEO/AI Search Opportunity"], 230)] for r in geo]))
    A("\n**Site-level GEO actions:**\n")
    for x in ["Keep `/llms.txt` accurate (it lists ~50 of 184 products and `/collection`, which is empty) — regenerate after AWS; it is optional and not a ranking factor.",
              "Robots.txt already allows major AI crawlers (GPTBot, OAI-SearchBot, ChatGPT-User, Google-Extended, ClaudeBot, Claude-SearchBot, PerplexityBot) — decide intentionally whether to keep that allowance.",
              "One factual source of truth for brand facts (see §5); mirror it in About, FAQ, Organization schema and llms.txt.",
              "Attribution: byline policy + 'last updated' dates on Education pages; cite GIA/IGI and other primary sources; show reviewer credentials only if real.",
              "Do not state unconfirmed HOD facts (bespoke timing is 'typically 2–3 weeks to make + ~6–9 days delivery, ~3–4 weeks, stone-dependent'; never a guarantee)."]:
        A(f"- {x}")
    A("\n## 11. Hand-off\n")
    A("Filter the CSV for `Priority` + `AWS Class` to build the sprint: **A** items can be started now (drafts, decisions, redirect map, briefs); **B** items wait for the AWS build; **C** items form the post-migration QA checklist. Columns `Recommended SEO Title`, `Recommended Meta Description`, `Recommended H1`, `Recommended Schema`, `Recommended Internal Links IN/OUT` are the copy-ready inputs.\n")
    open(OUT + "05-ON-PAGE-OPTIMIZATION-BACKLOG.md", "w").write("\n".join(A_))


doc05()
print("05 done")
