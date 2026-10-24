# -*- coding: utf-8 -*-
"""Docs 05, 06, 07."""
import collections, re
from s2_docs_a import mdt, short, esc, TODAY, pth
from s2_load import LINKREQ, CRAWL, PDP


def doc05(rows, L):
    pc = collections.Counter(l["Step 2 Priority"] for l in L)
    ds = collections.Counter(l["Destination Status"].split(" —")[0].split(" /")[0] for l in L)
    miss = [l for l in L if l["Present In Live HTML?"].startswith("NOT FOUND") and l["Stage 16 Priority"] == "REQUIRED"]
    flagged = [l for l in L if l["Destination Ownership Flag"]]
    flag_dest = collections.Counter(l["Destination ID"] for l in flagged)

    def pick(rel, n=8, prios=("REQUIRED", "RECOMMENDED")):
        out = [l for l in L if l["Relationship"] in rel and l["Stage 16 Priority"] in prios and l["Origin"].startswith("Stage 16")]
        out.sort(key=lambda l: (0 if l["Stage 16 Priority"] == "REQUIRED" else 1, l["Source ID"]))
        return out[:n]

    def lrow(l):
        return [l["Link ID"], l["Source ID"], l["Source URL"][:70], l["Destination ID"], l["Destination URL"][:70], l["Recommended Anchor"][:60], short(l["Purpose"], 70), l["Stage 16 Priority"], l["Step 2 Priority"],
                short(l["Destination Ownership Flag"], 45)]

    lh = ["Link", "Source", "Source URL", "Dest", "Destination URL", "Anchor", "Purpose", "S16", "Step 2", "Ownership flag"]
    req = []
    for r in rows:
        if r["Row Group"] == "PLANNED EDUCATION":
            q = [x for x in LINKREQ if x["page_id"] == r["Row ID"]]
            if q:
                x = q[0]
                req.append([r["Row ID"], x["incoming_required"].split(":")[0], x["outgoing_required"].split(":")[0], x["launch_linking_requirement"][:60]])
    p = """# 05 — Internal Link Implementation

Generated %s. **Specification only; no link was added or removed.** Operational file: `05-INTERNAL-LINK-IMPLEMENTATION.csv` (%d link specifications). Every URL is real: live pages use their live path; planned pages show their proposed/fixed path or `URL PENDING`; conditional pages show `NO URL`. No URL was invented.

## 1. Sources and method

1. **Stage 16** `16_internal_link_map.csv` (390 relationships) resolved to URLs via the Step 1 map, with anchors from `16_anchor_strategy.csv` (including the *avoid* lists).
2. **Stage 19** `19_internal_link_requirements.csv` for placement context on the 27 briefed pages.
3. **Final calendar** `internal_link_targets` for the 33 planned Blog posts (%d calendar-derived rows) plus %d Step 2A additions created by the resolutions.
4. **Live check:** for live→live links the initial HTML of the 2026-10-09 crawl was searched for the destination path (any position, **including global navigation**), so "PRESENT" can be satisfied by the menu; contextual links may still be absent.
5. Stage 16's record of the side-stone page uses the stale `/by-desgin/` URL — the specification uses the live `/by-design/` URL and flags it (`OD-06`).

## 2. Rules applied (from `16_linking_rules.md`)

| Rule | Source |
|---|---|
| Education links to commerce only at a decision point; commerce links to Education only when the buyer needs an explanation (short sentence + link, no re-explaining) | §3 / Stage 12 D-06 |
| Category/subcategory ≤5 contextual Education links + 1 Bespoke CTA; PDP ≤3 Education links as template UI labels; Education article ≤10 contextual outgoing links, 1–3 commercial exits; FAQ one link per answer to the named owner | §9 |
| Default to descriptive / natural-language anchors; exact match at most once per target (4 allowed, all from the lab-grown pillar); never an anchor that equals a keyword owned by another page; no target gets the same contextual anchor from more than two sources | §6 |
| The bare anchors "lab grown diamonds" / "lab diamonds" belong only to the (conditional) commercial Lab-Grown hub; until it exists the Education pillar's commercial exit is "browse our engagement rings" | §3.3 |
| Link style subcategories directly, never the `/by-desgin/` (or `/by-design/`) grouping page | §5 / P-DEPTH |
| Never remove the Blog-hub listing of an Education-owned article before its Education path exists | §4 |
| A planned page launches only with its REQUIRED incoming and outgoing links (`LAUNCH_BLOCKER_IF_MISSING`); certification pages ship together | §8, §3.5 |
| Do not cross cut-grade and shape anchors (D14-02); no shape-filter URLs as link targets | §9 |

## 3. Counts

* Link specifications: **%d** (Stage 16 resolved: %d · calendar-derived: %d · Step 2A additions: %d). Step 2 priority: HIGH %d · MEDIUM %d · LOW %d (REQUIRED→HIGH; RECOMMENDED→MEDIUM; CONDITIONAL/OPTIONAL→LOW; template-level nav/breadcrumb/footer rows are capped at MEDIUM and implemented once in the template).
* Destination status: %s.
* **Links whose destination ownership is not settled after Step 2A: %d** (flagged `DESTINATION OWNERSHIP NOT SETTLED` — destination is HELD (ambiguous head) or NOT BUILT; the link is still correct as architecture). Destinations: %s.

## 4. REQUIRED links missing from live pages today (initial HTML) — fix first

%s

## 5. REQUIRED links that must ship with each new Education page (launch blockers)

%s

## 6. Link specifications by relationship (REQUIRED/RECOMMENDED, selected; full list in the CSV)

### Commercial → Education
%s

### Education → Commercial (decision-point exits)
%s

### Education hub ↔ child / cross-hub
%s

### Blog → Education / Category (Stage 16 template rows) — per-post targets are in the CSV (`L2-Bxxx`)
%s

### Commercial hub → subcategory (structural)
%s

### Subcategory ↔ parent hub, category → product, product → category/Education
%s

### FAQ and supporting pages → Bespoke / owners
%s

### Step 2A additions (links created by the resolutions: re-homed/new Education pages, canonicalised pages)

%s

## 7. Template-level items (implement once, Class B)

* **Header menu** links filter-parameter URLs (`?shape=…`, `?metal=…`): they are `noindex, follow` + canonical to the parent — keep that behaviour on AWS; whether crawlable parameter links belong in the menu is an engineering decision.
* **Header/footer "Contact"** points to `/contact` (307 → modal): the real /contact page is adopted (`OD-09`); the link stays and gains a real destination when the page ships.
* **Header nav exposes empty subcategories** (tennis necklace, initials, tennis earrings, personalized & charm, For Him, Hip Hop): remove from the nav until populated (`OD-07` adopted; E-13).
* **Breadcrumbs:** add visible breadcrumbs + BreadcrumbList to articles (`Blog › Post`, `Education › Hub › Page`; the public section name is "Blog", OD-12) and align PDP BreadcrumbList with the visible path.
* **Education index** (`/education`) lists 1 article; per Stage 16 §8 it must list the Education-owned articles whose parent hub does not yet exist (LG-01/02/03/10, MET-01, RJG-02, CERT-01 + 4C-00, SHP-00, CERT-00) until each hub launches.
* **PDP template UI labels** to Education (ring size guide, grading explanations) are NAVIGATIONAL, ≤3 per PDP.

## 8. Anchor guidance in practice

| Do | Don't |
|---|---|
| "browse our engagement rings" (Education pillar → category) | "lab-grown diamonds" to the pillar or to a category (head term reserved) |
| "how CVD and HPHT diamonds are grown" (descriptive) | the same exact phrase repeated from many sources |
| "find your ring size" / "ring size chart" (guide) | "click here"/"read more" for important links |
| Category/child name ("side-stone engagement rings") | Per-shape filter URLs as targets from the shapes guide |
| "GIA vs IGI" only from the certification pillar to EDU-CERT-01 | "GIA vs IGI" anchors to any other page |

## 9. Validation (Class C, after AWS)

Crawl the rendered HTML and confirm every REQUIRED row: link present, anchor matches the specification, no nofollow, no redirect hop, destination 200 and self-canonical; confirm no new orphan; confirm the by-desgin 301 and nav changes.
""" % (TODAY, len(L), len([l for l in L if l["Origin"].startswith("STEP 2 —")]), len([l for l in L if l["Origin"].startswith("STEP 2A")]),
       len(L), len([l for l in L if l["Origin"].startswith("Stage 16")]), len([l for l in L if l["Origin"].startswith("STEP 2 —")]), len([l for l in L if l["Origin"].startswith("STEP 2A")]),
       pc["HIGH"], pc["MEDIUM"], pc["LOW"], "; ".join("%s %d" % (k, v) for k, v in ds.most_common()),
       len(flagged), "; ".join("%s (%d)" % (k, v) for k, v in flag_dest.most_common(8)),
       mdt(["Source", "Source URL", "Destination", "Destination URL", "Anchor", "Placement"], [[l["Source ID"], l["Source URL"][:70], l["Destination ID"], l["Destination URL"][:70], l["Recommended Anchor"][:60], short(l["Placement / Context"], 90)] for l in miss]),
       mdt(["Page", "REQUIRED incoming", "REQUIRED outgoing", "Rule"], req),
       mdt(lh, [lrow(l) for l in pick({"CATEGORY_TO_EDUCATION"})]),
       mdt(lh, [lrow(l) for l in pick({"EDUCATION_TO_CATEGORY"})]),
       mdt(lh, [lrow(l) for l in pick({"HUB_TO_CHILD", "CHILD_TO_HUB", "EDUCATION_CROSS_HUB"}, 10)]),
       mdt(lh, [lrow(l) for l in pick({"BLOG_TO_EDUCATION", "BLOG_TO_CATEGORY", "EDUCATION_TO_BLOG"}, 8, ("REQUIRED", "RECOMMENDED", "OPTIONAL", "CONDITIONAL"))]),
       mdt(lh, [lrow(l) for l in pick({"CATEGORY_TO_SUBCATEGORY"}, 8)]),
       mdt(lh, [lrow(l) for l in pick({"PRODUCT_TO_CATEGORY", "CATEGORY_TO_PRODUCT", "PRODUCT_TO_EDUCATION"}, 10)]),
       mdt(lh, [lrow(l) for l in pick({"FAQ_TO_EDUCATION", "FAQ_TO_SUPPORT", "SERVICE_TO_BLOG", "CATEGORY_TO_SERVICE", "PRODUCT_TO_SERVICE", "HOME_TO_CATEGORY"}, 12, ("REQUIRED", "RECOMMENDED", "OPTIONAL"))]),
       mdt(lh, [lrow(l) for l in L if l["Origin"].startswith("STEP 2A")]))
    return p


def doc06(rows):
    imgstats = []
    for path in ["/", "/engagement-rings", "/fine-jewellery/earrings", "/shop/oval-floral-diamond-ring", "/bespoke"]:
        c = CRAWL.get(path)
        if c:
            imgstats.append([path, c["img_count"], c["img_no_alt"]])
    aeo = [r for r in rows if r["AEO Opportunity"].startswith("HIGH") and r["Row Group"] in ("EXISTING ARTICLES (Education-owned)", "PLANNED EDUCATION", "CORE LIVE", "PLANNED BLOG")]
    aeo_rows = [[r["Row ID"], short(r["Primary Questions"].split("|")[0].split("?")[0] + "?", 90), short(r["AEO Opportunity"], 120), r["Status"]] for r in aeo[:34]]
    p = """# 06 — Schema, AEO, GEO/Entity & Image Spec

Generated %s. **Specification only. Template/schema/image-host changes are Class B (wait for AWS); validation is Class C.** Principles: mark up only what the page visibly shows; Google needs no special markup for AI features; FAQ rich results were discontinued (2026-05) — **FAQPage is not recommended anywhere**, HowTo has no feature, QAPage is invalid for site-authored Q&A; no ratings/reviews markup without genuine reviews; nothing here guarantees AI Overview or AI-answer visibility.

## 1. Schema — CURRENT / RECOMMENDED / WHY / DEPENDENCY / VALIDATION

%s

### Organization specification (sitewide)

| Property | Recommended | Status |
|---|---|---|
| `@type`, `name`, `url`, `logo` | Organization "House of Diams", https://www.houseofdiams.com, logo meeting Google's guidelines | Present — verify logo spec |
| `@id` | Stable `https://www.houseofdiams.com/#organization` reused by WebSite/AboutPage/Product `brand`/`publisher` | ADD |
| `contactPoint` | ONE email + telephone pair HOD designates as public (today info@ site-wide vs Admin@ on /returns; +91 phone only) | HOD INPUT REQUIRED (F-C2) |
| `address` | Surat (IN) and New York (US) as currently published | VERIFY with HOD |
| `sameAs` | Only profiles HOD confirms (Instagram linked on-page; Pinterest VERIFY) | ADD after confirmation |
| `founder`, `foundingDate` | Only after names/roles/year are confirmed | HOD INPUT REQUIRED (F-C1) |
| `hasMerchantReturnPolicy`, shipping | Only after /returns and /shipping facts are final | HOD INPUT REQUIRED (F-A1, F-A2) |

## 2. Product / PDP schema

See `07-PDP-ON-PAGE-SEO.md` §7 (name = visible H1; sku = visible SKU; one default-variant material/price; BreadcrumbList = visible path; no reviews; shipping/returns only when final; image URLs after the AWS host change).

## 3. AEO — answer-first specification

**Pattern for every informational page:** question (H1/H2 phrased as the user asks) → **direct answer in 1–2 sentences** → explanation → evidence/context (dated, sourced) → details (table/list/steps *only* where the content is genuinely tabular or sequential) → next action (link). Do **not** add FAQ blocks for their own sake; map the PAA questions the research found into headings or answer blocks; keep one owner per question (Stage 18 ownership), and link rather than repeat.

**Where AEO work matters most (from the research: AI Overview present on the calendar SERP):** ring size chart (165,000), diamond shapes (60,500), diamond cut (60,500), diamond clarity chart (33,100), 10-year anniversary gift (33,100), how to tell if a diamond is real (18,100) — all Education/Blog pages still to be written or refreshed (primary keywords now ratified, OD-03).

%s

**Commercial pages:** AEO is LOW — a one/two-sentence category definition above the grid and links to the Education owners; the questions stay on Education pages. **Policy pages:** AEO is about *accuracy* — shipping/returns answers are quoted by AI systems, so they must match the policy exactly (F-B1).

## 4. GEO / entity / trust

Treated as part of SEO (Google has no separate algorithm): make the brand and its facts understandable, consistent and attributable.

| Entity / fact | Today | Needed | Pages that must agree |
|---|---|---|---|
| Brand description (what House of Diams is and sells) | Different on Home / About / FAQ / /returns | One approved description | Home, About, FAQ, Organization schema, /llms.txt |
| Locations (Surat workshop, New York office) | /about and schema; /returns calls Surat "Headquarters & Workshop" | Confirmed list | About, Contact, schema, footer |
| Founders / roles / year | 'Akshar korat co founder'; bylines 'Krish Babriya, Co-founder'; 2014 vs 'half a century' | Confirmed names, roles, year | About, bylines, Person schema |
| Contact details | info@ / Admin@; +91 only | One public set | footer, About, Contact, FAQ, schema |
| Certification stance | 'IGI Certified', 'IGI / GIA', per-product 'IGI certified GH / VVS' | Which labs, which products, report available? | Home, Bespoke, PDP, FAQ, EDU-CERT pages |
| Shipping / returns / warranty | Contradictory or placeholder | Final policies | Header badge, Home, PDP, FAQ, policy pages |
| Authorship of articles | 'House of Diams Jewellery Team', 'HOD Team', 'Krish Babriya, Co-founder' | ADOPTED (OD-11): 'House of Diams' organization byline; a named person only where identity, role and credentials are verified; visible byline and schema must match | All articles, schema |
| Sources | Few external citations | Cite GIA/IGI/standards bodies for factual claims; visible 'last updated' | Education pages |

**Site-level GEO actions:** keep `/llms.txt` accurate and regenerated after AWS (it lists ~50 of 184 products and the empty `/collection`; it is optional and not a ranking factor); keep the robots.txt AI-crawler allowances only as a deliberate decision; one fact source mirrored in About/FAQ/schema/llms.txt; never state an unconfirmed HOD fact (bespoke timing = typically 2–3 weeks + ~6–9 days delivery, ~3–4 weeks, stone-dependent, never a guarantee).

## 5. Image & alt-text SEO

| Image class | Needed? | Rule |
|---|---|---|
| Product gallery images | Audit rendered DOM; alt where missing | `<product name>, <view>` (e.g. "Oval Marquise Diamond Engagement Ring, side view"); first image is primary; no keyword stuffing; don't invent visual facts (stone origin/certification) |
| Category/hub hero & tiles | Yes | Describe what the image shows or the category it links to; decorative flourishes `alt=""` |
| Product cards in grids | Yes | Product name + one key attribute |
| Article diagrams, charts, tables-as-images | Yes (Education/Blog) | Describe the information, not "chart"; keep real data in HTML tables |
| Craft/bespoke/workshop photography | Yes | Real HOD photos only, descriptive alt; no stock images implying HOD work |
| UI icons, badges | Decorative | `alt=""` (they inflate the missing-alt counts) |
| Open Graph / schema `image` | Yes | Absolute, stable URLs; must resolve after AWS |

Observed (initial HTML, includes icons/lazy images — treat as a **flag to audit the rendered DOM**, not a defect count): %s. **Do not rename image files. Do not change the image hosts before AWS.** After AWS: keep old Supabase/R2 URLs resolving or 301 (Google Images), update Product/BlogPosting `image`, OG tags and `/llms.txt`.

## 6. Validation checklist (Class C, after AWS)

Rich Results Test + Schema.org validator on: home, 1 category, 1 subcategory, 3 PDPs (different categories), 2 articles, /faq, /returns, /about, /bespoke. Check: no FAQPage outside /faq (if kept at all), BreadcrumbList on articles/PDP matches visible path, Product `name`/`sku`/`price`/`priceCurrency: USD` correct for a US/Googlebot request (geo/currency cookies are set from IP), `image` URLs 200, one Organization `@id`, author consistent. Search Console: confirm the "Search generative AI" setting is not excluding the property (GSC access currently unavailable → VERIFY).
""" % (TODAY,
       mdt(["Page type", "CURRENT (live crawl 2026-10-09)", "RECOMMENDED", "WHY", "IMPLEMENTATION DEPENDENCY", "VALIDATION NEEDED"], [
           ["Sitewide", "Organization + ContactPoint + PostalAddress (Surat IN, New York US)", "Keep; add @id; one email/phone; confirmed sameAs; founder/foundingDate only when confirmed", "Single entity signal across AI/search surfaces", "Class B template; OD-08 facts", "Org @id resolves; contact data = visible contact data"],
           ["Homepage", "Organization only", "Optional WebSite (name only). No Product/FAQ", "Clarifies site entity; no feature to chase", "Class B", "WebSite name matches brand"],
           ["Category / subcategory / shop", "BreadcrumbList + Organization; **FAQPage on 35 pages (boilerplate repeated)**", "BreadcrumbList only; retire boilerplate FAQPage; optional visible category-specific Q&A WITHOUT FAQPage markup", "FAQ rich results discontinued; duplicated Q&A across pages is noise", "Class B template", "No FAQPage left on listing pages; breadcrumbs valid"],
           ["PDP (184)", "Product + Offer + Brand + BreadcrumbList; no ratings; images on Supabase / R2 hosts", "Keep Product/Offer; name = H1; sku = visible SKU; default-variant material/price; BreadcrumbList = visible path; shipping/returns details only when final; image URLs updated after AWS; never fake reviews", "Prevents mismatches between markup and visible content", "Class B/C; OD-08; OD-14", "Rich Results Test on 3 PDPs; currency USD for US"],
           ["Articles (Blog + Education)", "BlogPosting + `Person` author (names vary) + ImageObject; dates ISO on live articles; no BreadcrumbList", "BlogPosting/Article + BreadcrumbList; author = Organization or a real named expert (OD-11); ISO dates; **no FAQPage/HowTo**", "Consistent attribution; navigation context", "Class B template (CMS has no schema field); OD-11", "2 articles incl. one CMS-generated post (package notes claim non-ISO dates — VERIFY)"],
           ["/about", "Organization only", "AboutPage + Organization @id; Person only for confirmed founders", "Primary entity page", "Class B; OD-08", "Person names match visible page"],
           ["/contact (if built)", "n/a (modal)", "ContactPage + Organization", "NAP consistency", "Class B; OD-09", "Contact data identical sitewide"],
           ["/faq", "FAQPage", "WebPage + BreadcrumbList; FAQPage on /faq alone is harmless but earns no rich result — do not extend", "Visible Q&A page is the only legitimate FAQPage context", "Class B", "Visible Q&A = markup Q&A"],
           ["/returns, /shipping", "FAQPage on /returns attached to a non-FAQ body; none on /shipping", "WebPage + BreadcrumbList; MerchantReturnPolicy / OfferShippingDetails when terms are final", "Remove mismatched markup; add policy structure only with facts", "Class B; OD-08", "Policy markup = visible policy"],
           ["/bespoke", "Organization only", "BreadcrumbList; Service optional (no Google feature)", "Low value; keep simple", "Class B", "—"],
           ["Hubs (/blog, /education)", "Organization only", "CollectionPage/Blog optional + BreadcrumbList", "Context only", "Class B", "—"]]),
       mdt(["Row", "Lead question", "AEO opportunity", "Status"], aeo_rows),
       "; ".join("%s: %s imgs / %s without alt" % tuple(x) for x in imgstats))
    return p


def doc07(rows, P):
    pdp = [x for x in PDP]
    t60 = sum(1 for x in pdp if "title>60" in x["Flags"])
    cats = collections.Counter(x["Schema category"] for x in pdp)
    ex = [
        ["Adeline 2 CTW Round Diamond Solitaire Stud Earrings (68 rendered)", "Round Solitaire Diamond Stud Earrings, 2 ct (≈44 pre-suffix)"],
        ["Alternating Pear Lab-Grown Diamond Eternity Ring (53)", "KEEP — already ≤60 rendered"],
        ["Milgrain Bezel Round Lab-Grown Diamond Necklace 1.00 Carat (>60)", "Round Milgrain Bezel Diamond Necklace, 1.00 ct"],
        ["Oval Marquise Side-Stone Engagement Ring", "2.5 ct Oval Marquise Diamond Engagement Ring"],
    ]
    p = """# 07 — PDP On-Page SEO

Generated %s. Companion: `07-PDP-PRIORITY-ACTIONS.csv` (%d PDPs needing special treatment). **The 184 product pages are governed by templates and rules; they are not rewritten one by one.** Product URLs never change in this package.

## 1. Evidence (QA/06 + live re-read 2026-10-09)

* %d PDPs (categories: %s). All 200, self-canonical, USD in schema (US/IP behaviour to verify), 178 priced for 10K Yellow Gold, 5 for 10K White Gold, 1 for '18K Gold Vermil'.
* Titles = `<Product name> | House of Diams`; **%d exceed 60 rendered characters**; 2 products share one title; 6 have placeholder-style metas ("Stud Earrings · 10K White Gold - House of Diams"); 3 metas exceed 160 characters; 10 PDPs have numeric-ID / `-copy-` slugs (carat variants as separate URLs).
* Product descriptions are substantive (shape, carat, setting, closure, dimensions, SKU, 'Best for') — but also contain **unverified claims**: "IGI certified GH / VVS diamonds", a shipping block ("Worldwide insured shipping is complimentary…", "In-stock pieces usually ship within 2-3 business days") and a "Care & Warranty" block. Header badges say "Complimentary Insured Shipping / 15-Day Returns". None of these is a confirmed HOD fact (F-B1).

## 2. Title template (pre-suffix; the template adds ` | House of Diams`)

`[{Total carat} ct ]{Shape} [Lab-Grown ]Diamond {Product type}[, {distinguishing feature}]` — order of priority when space is short: **shape + product type > carat > distinguishing feature > origin word > metal**. Target ≤~43 characters pre-suffix (≤60 rendered; a display guideline).

* Use the **product record** for every word (shape, carat, type, stone type). Do not add 'Lab-Grown' unless the record's Stone Type says so (the spec table does show 'Lab Grown Diamond').
* **Keep the existing name** when it is already descriptive and short; do not rename for its own sake. Collection names alone ("Adeline", "Elyra") never stand as the title.
* Titles must be unique: where two products would collide, add the true differentiator (bail style, setting, carat).

%s

## 3. Meta-description template

`{Product type} with {shape/stone description} ({carat} total) in {setting/metal note}. {One factual differentiator}. {Metal availability as shown on the page}.` ≤~155 characters. Built from the description and spec table only. **Never** include certification, shipping, returns, warranty or "free". Replace the six placeholder metas first (drafts in the CSV); trim the three >160 character metas at a sentence boundary.

## 4. H1 and description rules

* H1 = the visible product name (unchanged). It must equal the schema `name` (see §7).
* Description first sentence: product type, stone shape, carat, setting, metal. Then design details. Avoid cloning descriptions across carat variants (near-duplicate risk — vary the carat/size facts that genuinely differ).
* Specs table kept (shape, total carat, center stone, setting, closure, dimensions, SKU, style, best for). State the stone type per product from the record.
* Certification: show a lab and report number **only where a report exists for that piece**; no blanket "IGI certified" (F-B1).
* Shipping/returns/warranty sections: replace the per-PDP copy with a short summary linking to /shipping and /returns once those are final.

## 5. Variants and near-duplicates

* IA D-11: one URL per product, variants on the page. Ten PDPs are separate URLs for carat variants (e.g. 1 CT vs 2 CT east-west emerald pendant; milgrain bezel necklace 1.00 vs 1.50; 2.62 vs 3.62 ct three-stone ring; two round solitaire pendants). **ADOPTED (OD-14): keep these URLs; do not merge, delete or redirect them without a supported consolidation plan and GSC/URL evidence.** Keep each self-canonical with carat in title/meta so each is unique; review after cut-over with GSC data (G-01).
* Metal choices (10K/14K × yellow/white/rose) are on-page options, not URLs.
* Duplicate-risk pairs: Aurelia vs Elyra round solitaire pendants (same title; differ by bail style).

## 6. Image / alt text

Gallery alt = `<product name>, <view>`; primary image first; product video poster alt; card images = name + one attribute; decorative icons `alt=""`. Do not rename files or change hosts before AWS; after AWS keep old image URLs resolvable and update schema `image`, OG tags and `/llms.txt`.

## 7. Product / Offer schema — CURRENT / RECOMMENDED / WHY / DEPENDENCY / VALIDATION

%s

## 8. Internal-link rules for PDPs

* Breadcrumb: Home › Category › Subcategory › Product (visible and schema identical); PDP URLs stay flat.
* ≤3 Education links as **template UI labels** ("Find your ring size", "What do these diamond grades mean?") — NAVIGATIONAL, not keyword strings (Stage 16 §5). Ring PDPs must link the ring-size guide (REQUIRED for the ranking PDP).
* Related-products module links PDP → other PDPs only; a product never links to itself.
* Bespoke CTA where the product is customisable — only if HOD confirms product-level customisation (Stage 16 §6.5: unconfirmed).
* Link to /shipping and /returns once final.

## 9. Priority PDPs (see CSV)

%s

## 10. Sequencing

1. **Now (Class A):** approve templates; fact-check the six placeholder-meta drafts and the two title differentiators against the product records; list the full set of titles >60 rendered characters for template-based rewrite.
2. **After AWS (Class B):** apply title/meta templates in the CMS/product data; fix schema name/sku/material/breadcrumb; replace per-PDP shipping/warranty copy; update image URLs.
3. **After AWS (Class C):** re-crawl all 184 PDPs: title uniqueness, length distribution, schema validity, canonical, 200s, USD for a US request.
""" % (TODAY, len(P), len(pdp), ", ".join("%s %d" % kv for kv in cats.most_common()), t60,
       mdt(["Current (rendered)", "Template result (illustrative — fact-check vs product record)"], ex),
       mdt(["Property", "CURRENT", "RECOMMENDED", "WHY", "DEPENDENCY", "VALIDATION"], [
           ["name", "Internal name ('Oval Floral Diamond Ring') ≠ visible H1 on the checked PDP", "= visible H1", "Mismatched names confuse shopping surfaces", "Class B (product data/template)", "Name equals H1 on 3 PDPs"],
           ["sku", "UUID in JSON-LD; visible SKU (e.g. RG038993) differs", "= visible SKU", "Stable merchant identifier", "Class B", "sku equals visible SKU"],
           ["description", "Present", "= visible description (no unverified claims)", "Consistency", "OD-08", "—"],
           ["material / offers.price", "Six metals listed; one price (default variant)", "Default variant material with its price, or ProductGroup/variants if variant URLs/params exist", "Price must describe what is listed", "Class B; engineering decision", "Rich Results Test"],
           ["BreadcrumbList", "Home › Shop › Product (visible: Home / Engagement Rings / By Design)", "Home › Category › Subcategory › Product = visible", "Markup must match the page", "Class B", "Breadcrumb equals visible path"],
           ["image", "Supabase / Cloudflare R2 URLs", "Stable post-AWS URLs; all gallery images", "Hosts change with AWS", "Class B; keep old URLs resolving", "Image URLs 200"],
           ["Offer.priceCurrency / availability", "USD (crawl from IN also showed USD in schema; cookies were IN/INR)", "USD for US/Googlebot; availability accurate", "Currency by IP risk", "Engineering confirm", "Request from a US IP"],
           ["shippingDetails / hasMerchantReturnPolicy", "Absent", "Add only when policies are final", "Avoid unconfirmed promises in markup", "OD-08; Class B", "Matches visible policy"],
           ["aggregateRating / review", "Absent", "Do not add without genuine, displayed reviews", "Guideline compliance", "—", "—"]]),
       mdt(["PDP", "Issues", "Priority", "Action"], [[x["URL"].replace("/shop/", "")[:48], short(x["Issues (QA/06 flags)"], 70), x["Priority"], short(x["Action"], 90)] for x in P]))
    return p
