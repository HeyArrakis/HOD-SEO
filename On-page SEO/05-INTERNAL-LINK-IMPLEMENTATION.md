# 05 — Internal Link Implementation

Generated 2026-10-10. **Specification only; no link was added or removed.** Operational file: `05-INTERNAL-LINK-IMPLEMENTATION.csv` (624 link specifications). Every URL is real: live pages use their live path; planned pages show their proposed/fixed path or `URL PENDING`; conditional pages show `NO URL`. No URL was invented.

## 1. Sources and method

1. **Stage 16** `16_internal_link_map.csv` (390 relationships) resolved to URLs via the Step 1 map, with anchors from `16_anchor_strategy.csv` (including the *avoid* lists).
2. **Stage 19** `19_internal_link_requirements.csv` for placement context on the 27 briefed pages.
3. **Final calendar** `internal_link_targets` for the 33 planned Blog posts (206 calendar-derived rows) plus 28 Step 2A additions created by the resolutions.
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

* Link specifications: **624** (Stage 16 resolved: 390 · calendar-derived: 206 · Step 2A additions: 28). Step 2 priority: HIGH 98 · MEDIUM 286 · LOW 240 (REQUIRED→HIGH; RECOMMENDED→MEDIUM; CONDITIONAL/OPTIONAL→LOW; template-level nav/breadcrumb/footer rows are capped at MEDIUM and implemented once in the template).
* Destination status: LIVE (200) 340; PLANNED 154; CONDITIONAL 40; LIVE 37; GROUP 25; TEMPLATE 25; LIVE URL BUT NOT 200 3.
* **Links whose destination ownership is not settled after Step 2A: 8** (flagged `DESTINATION OWNERSHIP NOT SETTLED` — destination is HELD (ambiguous head) or NOT BUILT; the link is still correct as architecture). Destinations: COM-LG-HUB (7); COM-FJ-RINGS (1).

## 4. REQUIRED links missing from live pages today (initial HTML) — fix first

| Source | Source URL | Destination | Destination URL | Anchor | Placement |
|---|---|---|---|---|---|
| EDU-ROOT | /education | EDU-4C-00 | /blog/the-4cs-of-lab-grown-diamonds-explained-cut-colour-clarity-and-c | Diamond Quality (4Cs) | Stage 14 hierarchy: EDU-ROOT is the parent of EDU-4C-00; hub topic list. |
| EDU-ROOT | /education | EDU-SHP-00 | /blog/the-best-lab-grown-diamond-shapes-for-engagement-rings-house-of- | Diamond Shapes | Stage 14 hierarchy: EDU-ROOT is the parent of EDU-SHP-00; hub topic list. |
| EDU-ROOT | /education | EDU-CERT-00 | /blog/igi-certification-for-lab-grown-diamonds-what-it-means-house-of- | Certification & Grading Reports | Stage 14 hierarchy: EDU-ROOT is the parent of EDU-CERT-00; hub topic list. |
| EDU-CERT-00 | /blog/igi-certification-for-lab-grown-diamonds-what-it-means-house-of- | EDU-CERT-01 | /education/lab-grown-diamond-certification-explained-gia-vs-igi-house- | GIA vs IGI compared | On source brief EDU-CERT-00:S03 — Who issues diamond reports: the main labs |
| EDU-CERT-01 | /education/lab-grown-diamond-certification-explained-gia-vs-igi-house- | EDU-CERT-00 | /blog/igi-certification-for-lab-grown-diamonds-what-it-means-house-of- | Certification & Grading Reports | Stage 14 hierarchy breadcrumb (EDU-CERT-01 -> EDU-CERT-00). |
| COM-ER | /engagement-rings | COM-PDP-OVAL-FLORAL | /shop/oval-floral-diamond-ring | Oval Marquise Diamond Engagement Ring | Ranking PDP stays in the engagement-ring grid while live. |
| COM-ER | /engagement-rings | EDU-SHP-00 | /blog/the-best-lab-grown-diamond-shapes-for-engagement-rings-house-of- | compare diamond shapes | On COM-ER (no Stage 19 brief for the source page): Shape is the first engagement-ring dec… |
| COM-ER | /engagement-rings | EDU-4C-00 | /blog/the-4cs-of-lab-grown-diamonds-explained-cut-colour-clarity-and-c | how diamonds are graded (the 4Cs) | On COM-ER (no Stage 19 brief for the source page): Buyers compare grades; category copy l… |
| COM-ER | /engagement-rings | EDU-RJG-02 | /blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-hous | work out your ring size | On COM-ER (no Stage 19 brief for the source page): Sizing is needed for every ring purcha… |
| COM-ER-SIDESTONE | /engagement-rings/by-design/side-stone-rings | COM-PDP-OVAL-FLORAL | /shop/oval-floral-diamond-ring | Oval Marquise Diamond Engagement Ring | The ranking PDP is a side-stone design (Stage 10 title). |
| COM-WB | /wedding-bands | EDU-RJG-02 | /blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-hous | measure your band size | On COM-WB (no Stage 19 brief for the source page): Sizing is needed for every band. |
| COM-SHOP | /shop | COM-PDP-OVAL-FLORAL | /shop/oval-floral-diamond-ring | Oval Marquise Diamond Engagement Ring | All-products grid. |
| COM-PDP-OVAL-FLORAL | /shop/oval-floral-diamond-ring | EDU-RJG-02 | /blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-hous | Find your ring size | COM-PDP-OVAL-FLORAL:S03 — Guides for this ring |
| EDU-LG-10 | /blog/how-to-choose-a-lab-grown-diamond-the-complete-buyer-s-guide | EDU-4C-00 | /blog/the-4cs-of-lab-grown-diamonds-explained-cut-colour-clarity-and-c | the 4Cs of diamond quality | On source brief EDU-LG-10:S03 — Prioritizing the 4Cs for a lab-grown diamond |
| EDU-LG-10 | /blog/how-to-choose-a-lab-grown-diamond-the-complete-buyer-s-guide | EDU-CERT-00 | /blog/igi-certification-for-lab-grown-diamonds-what-it-means-house-of- | why certification matters | On source brief EDU-LG-10:S04 — Insist on a grading report |
| SUP-FAQ | /faq | EDU-LG-01 | /blog/are-lab-grown-diamonds-real-a-complete-buyer-s-guide | more on whether lab-grown diamonds are real | On SUP-FAQ (no Stage 19 brief for the source page): D14-30: legitimacy -> EDU-LG-01. |
| SUP-FAQ | /faq | EDU-LG-02 | /blog/lab-grown-vs-natural-diamonds-the-honest-comparison-house-of-dia | our full lab-grown vs natural comparison | On SUP-FAQ (no Stage 19 brief for the source page): D14-30: lab vs natural -> EDU-LG-02 (… |
| SUP-FAQ | /faq | EDU-CERT-00 | /blog/igi-certification-for-lab-grown-diamonds-what-it-means-house-of- | how diamond certification works | On SUP-FAQ (no Stage 19 brief for the source page): D14-30: certification -> EDU-CERT-00. |
| SUP-FAQ | /faq | EDU-RJG-02 | /blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-hous | how to measure your ring size | On SUP-FAQ (no Stage 19 brief for the source page): D14-30: resizing -> EDU-RJG-02 for th… |

## 5. REQUIRED links that must ship with each new Education page (launch blockers)

| Page | REQUIRED incoming | REQUIRED outgoing | Rule |
|---|---|---|---|
| EDU-LG-00 | 10 | 9 | LINKING_REQUIREMENT_AT_LAUNCH: 10 REQUIRED incoming and 9 RE |
| EDU-LG-05 | 3 | 2 | LINKING_REQUIREMENT_AT_LAUNCH: 3 REQUIRED incoming and 2 REQ |
| EDU-LG-07 | 1 | 1 | LINKING_REQUIREMENT_AT_LAUNCH: 1 REQUIRED incoming and 1 REQ |
| EDU-LG-08 | 1 | 1 | LINKING_REQUIREMENT_AT_LAUNCH: 1 REQUIRED incoming and 1 REQ |
| EDU-LG-09 | 1 | 1 | LINKING_REQUIREMENT_AT_LAUNCH: 1 REQUIRED incoming and 1 REQ |
| EDU-NAT-00 | 2 | 2 | LINKING_REQUIREMENT_AT_LAUNCH: 2 REQUIRED incoming and 2 REQ |
| EDU-4C-01 | 3 | 3 | LINKING_REQUIREMENT_AT_LAUNCH: 3 REQUIRED incoming and 3 REQ |
| EDU-4C-02 | 2 | 2 | LINKING_REQUIREMENT_AT_LAUNCH: 2 REQUIRED incoming and 2 REQ |
| EDU-4C-03 | 2 | 2 | LINKING_REQUIREMENT_AT_LAUNCH: 2 REQUIRED incoming and 2 REQ |
| EDU-4C-05 | 1 | 1 | LINKING_REQUIREMENT_AT_LAUNCH: 1 REQUIRED incoming and 1 REQ |
| EDU-4C-06 | 2 | 2 | LINKING_REQUIREMENT_AT_LAUNCH: 2 REQUIRED incoming and 2 REQ |
| EDU-4C-07 | 1 | 1 | LINKING_REQUIREMENT_AT_LAUNCH: 1 REQUIRED incoming and 1 REQ |
| EDU-MET-00 | 2 | 2 | LINKING_REQUIREMENT_AT_LAUNCH: 2 REQUIRED incoming and 2 REQ |
| EDU-RJG-01 | 1 | 3 | LINKING_REQUIREMENT_AT_LAUNCH: 1 REQUIRED incoming and 3 REQ |
| EDU-GEN-01 | 1 | 1 | LINKING_REQUIREMENT_AT_LAUNCH: 1 REQUIRED incoming and 1 REQ |
| EDU-RJG-03 | 0 | 0 | IF_ACTIVATED: publish with its CONDITIONAL rows (parent hub  |

## 6. Link specifications by relationship (REQUIRED/RECOMMENDED, selected; full list in the CSV)

### Commercial → Education
| Link | Source | Source URL | Dest | Destination URL | Anchor | Purpose | S16 | Step 2 | Ownership flag |
|---|---|---|---|---|---|---|---|---|---|
| L2-111 | COM-ER | /engagement-rings | EDU-SHP-00 | /blog/the-best-lab-grown-diamond-shapes-for-engagement-rings-house-of- | compare diamond shapes | Shape is the first engagement-ring decision; the Shapes pillar includ… | REQUIRED | HIGH |  |
| L2-112 | COM-ER | /engagement-rings | EDU-4C-00 | /blog/the-4cs-of-lab-grown-diamonds-explained-cut-colour-clarity-and-c | how diamonds are graded (the 4Cs) | Buyers compare grades; category copy links rather than re-explains (S… | REQUIRED | HIGH |  |
| L2-113 | COM-ER | /engagement-rings | EDU-RJG-02 | /blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-hous | work out your ring size | Sizing is needed for every ring purchase (Stage 14 N-RJG-02). | REQUIRED | HIGH |  |
| L2-128 | COM-WB | /wedding-bands | EDU-RJG-02 | /blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-hous | measure your band size | Sizing is needed for every band. | REQUIRED | HIGH |  |
| L2-114 | COM-ER | /engagement-rings | EDU-LG-02 | /blog/lab-grown-vs-natural-diamonds-the-honest-comparison-house-of-dia | how lab-grown and natural diamonds compare | Protected ranking URL; origin is a common pre-purchase question. | RECOMMENDED | MEDIUM |  |
| L2-121 | COM-ER-SIDESTONE | /engagement-rings/by-design/side-stone-rings | EDU-RJG-01 | URL PENDING (slug not decided) — Ring settings guide | how different ring settings hold side stones | Settings guide explains styles; the subcategory keeps the shopping qu… | RECOMMENDED | MEDIUM |  |
| L2-151 | COM-FJ-EARRINGS | /fine-jewellery/earrings | EDU-MET-00 | URL PENDING (slug not decided) — Jewelry metals guide (Metals hub pill | which metals suit sensitive ears | EDU-MET-00 owns hypoallergenic-metal questions (Stage 15). | RECOMMENDED | MEDIUM |  |
| L2-129 | COM-WB | /wedding-bands | EDU-MET-01 | /blog/14k-vs-18k-gold-for-diamond-jewellery-which-is-better-house-of-d | 14k or 18k gold for your band? | Protected ranking URL; the validated band keywords are metal question… | RECOMMENDED | MEDIUM |  |

### Education → Commercial (decision-point exits)
| Link | Source | Source URL | Dest | Destination URL | Anchor | Purpose | S16 | Step 2 | Ownership flag |
|---|---|---|---|---|---|---|---|---|---|
| L2-247 | EDU-LG-10 | /blog/how-to-choose-a-lab-grown-diamond-the-complete-buyer-s-guide | COM-ER | /engagement-rings | shop engagement rings | Buying guide -> category at the decision point (Stage 13 §9). | REQUIRED | HIGH |  |
| L2-285 | EDU-MET-01 | /blog/14k-vs-18k-gold-for-diamond-jewellery-which-is-better-house-of-d | COM-ER | /engagement-rings | see engagement ring designs | Existing H1 frames the choice for an engagement ring (Stage 10). | REQUIRED | HIGH |  |
| L2-289 | EDU-RJG-01 | URL PENDING (slug not decided) — Ring settings guide | COM-ER-SIDESTONE | /engagement-rings/by-design/side-stone-rings | side-stone engagement rings | Protected ranking URL: the side-stone section hands the shopping quer… | REQUIRED | HIGH |  |
| L2-290 | EDU-RJG-01 | URL PENDING (slug not decided) — Ring settings guide | COM-ER | /engagement-rings | engagement rings by setting style | Decision-point exit. | REQUIRED | HIGH |  |
| L2-295 | EDU-RJG-02 | /blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-hous | COM-ER | /engagement-rings | shop engagement rings in your size | Tool/guide -> category (D14-23). | REQUIRED | HIGH |  |
| L2-272 | EDU-SHP-00 | /blog/the-best-lab-grown-diamond-shapes-for-engagement-rings-house-of- | COM-ER | /engagement-rings | explore engagement ring designs | Pillar includes engagement-ring shape choice (D14-17). | REQUIRED | HIGH |  |
| L2-256 | EDU-4C-00 | /blog/the-4cs-of-lab-grown-diamonds-explained-cut-colour-clarity-and-c | COM-ER | /engagement-rings | explore engagement rings | Decision-point exit (H1 of existing article is a choosing guide). | RECOMMENDED | MEDIUM |  |
| L2-196 | EDU-LG-00 | /education/lab-grown-diamonds | COM-ER | /engagement-rings | browse our engagement rings | Decision-point exit while no commercial Lab-Grown hub exists. | RECOMMENDED | MEDIUM |  |

### Education hub ↔ child / cross-hub
| Link | Source | Source URL | Dest | Destination URL | Anchor | Purpose | S16 | Step 2 | Ownership flag |
|---|---|---|---|---|---|---|---|---|---|
| L2-312 | BLOG-CRAFT | Blog category: Craft (posts under /blog) | BLOG-HUB | /blog | Blog | Blog breadcrumb. | REQUIRED | MEDIUM |  |
| L2-316 | BLOG-GIFTS | Blog category: Gifts & Occasions (posts under /blog) | BLOG-HUB | /blog | Blog | Blog breadcrumb. | REQUIRED | MEDIUM |  |
| L2-311 | BLOG-HUB | /blog | BLOG-CRAFT | Blog category: Craft (posts under /blog) | (post title) | Blog hub lists posts chronologically (Stage 13 §5). | REQUIRED | HIGH |  |
| L2-313 | BLOG-HUB | /blog | BLOG-STYLE | Blog category: Style & Trends (posts under /blog) | (post title) | Blog hub lists posts chronologically (Stage 13 §5). | REQUIRED | HIGH |  |
| L2-315 | BLOG-HUB | /blog | BLOG-GIFTS | Blog category: Gifts & Occasions (posts under /blog) | (post title) | Blog hub lists posts chronologically (Stage 13 §5). | REQUIRED | HIGH |  |
| L2-317 | BLOG-HUB | /blog | BLOG-LAUNCH | Blog category: Collections & Launches (posts under /blog) | (post title) | Blog hub lists posts chronologically (Stage 13 §5). | REQUIRED | HIGH |  |
| L2-321 | BLOG-HUB | /blog | BLOG-INDUSTRY | Blog category: Industry Notes (posts under /blog) | (post title) | Blog hub lists posts chronologically (Stage 13 §5). | REQUIRED | HIGH |  |
| L2-323 | BLOG-HUB | /blog | EXIST-BLOG-ER-ONLINE | /blog/how-to-choose-a-lab-grown-diamond-engagement-ring-online-house-o | (article title) | Current and only path: the Blog hub listing (Stage 10). Its Education… | REQUIRED | HIGH |  |
| L2-322 | BLOG-INDUSTRY | Blog category: Industry Notes (posts under /blog) | BLOG-HUB | /blog | Blog | Blog breadcrumb. | REQUIRED | MEDIUM |  |
| L2-318 | BLOG-LAUNCH | Blog category: Collections & Launches (posts under /blog) | BLOG-HUB | /blog | Blog | Blog breadcrumb. | REQUIRED | MEDIUM |  |

### Blog → Education / Category (Stage 16 template rows) — per-post targets are in the CSV (`L2-Bxxx`)
| Link | Source | Source URL | Dest | Destination URL | Anchor | Purpose | S16 | Step 2 | Ownership flag |
|---|---|---|---|---|---|---|---|---|---|
| L2-334 | BLOG-CRAFT | Blog category: Craft (posts under /blog) | COM-BESPOKE | /bespoke | commission your own piece | Stage 13 §12: Bespoke is the natural commercial link for craft conten… | REQUIRED | HIGH |  |
| L2-347 | BLOG-GIFTS | Blog category: Gifts & Occasions (posts under /blog) | COM-FJ-EARRINGS | /fine-jewellery/earrings | earrings to give | Stage 13 §12: gift guides link to categories rather than long product… | REQUIRED | HIGH |  |
| L2-348 | BLOG-GIFTS | Blog category: Gifts & Occasions (posts under /blog) | COM-FJ-NECKLACES | /fine-jewellery/necklaces | necklaces and pendants | Stage 13 §12: gift guides link to categories rather than long product… | REQUIRED | HIGH |  |
| L2-349 | BLOG-GIFTS | Blog category: Gifts & Occasions (posts under /blog) | COM-FJ-BRACELETS | /fine-jewellery/bracelet | bracelets for every occasion | Stage 13 §12: gift guides link to categories rather than long product… | REQUIRED | HIGH |  |
| L2-362 | BLOG-INDUSTRY | Blog category: Industry Notes (posts under /blog) | EDU-LG-00 | /education/lab-grown-diamonds | what lab-grown diamonds are | Evergreen concept owner (Stage 13 framework). | REQUIRED | HIGH |  |
| L2-363 | BLOG-INDUSTRY | Blog category: Industry Notes (posts under /blog) | EDU-LG-05 | URL PENDING (slug not decided) — Lab-grown diamond price, value & resa | how lab-grown diamond value works | Dated price commentary is Blog; evergreen value principles are EDU-LG… | REQUIRED | HIGH |  |
| L2-354 | BLOG-LAUNCH | Blog category: Collections & Launches (posts under /blog) | COM-FJ | /fine-jewellery | the full fine jewelry collection | A launch post never replaces the category page (Stage 13 rule 7). | REQUIRED | HIGH |  |
| L2-355 | BLOG-LAUNCH | Blog category: Collections & Launches (posts under /blog) | COM-ER | /engagement-rings | the engagement ring collection | Required when the launch is bridal. | REQUIRED | HIGH |  |

### Commercial hub → subcategory (structural)
| Link | Source | Source URL | Dest | Destination URL | Anchor | Purpose | S16 | Step 2 | Ownership flag |
|---|---|---|---|---|---|---|---|---|---|
| L2-107 | COM-ER | /engagement-rings | COM-ER-SIDESTONE | /engagement-rings/by-design/side-stone-rings | Side-stone engagement rings | Stage 12 D-03: confirmed L2 style; its query SERP is CATEGORY (Stage … | REQUIRED | HIGH |  |
| L2-134 | COM-FJ | /fine-jewellery | COM-FJ-EARRINGS | /fine-jewellery/earrings | Earrings | Stage 12 D-02: L2 under the umbrella. | REQUIRED | HIGH |  |
| L2-139 | COM-FJ | /fine-jewellery | COM-FJ-NECKLACES | /fine-jewellery/necklaces | Necklaces & Pendants | Stage 12 D-02: L2 under the umbrella. | REQUIRED | HIGH |  |
| L2-144 | COM-FJ | /fine-jewellery | COM-FJ-BRACELETS | /fine-jewellery/bracelet | Bracelets | Stage 12 D-02: L2 under the umbrella. | REQUIRED | HIGH |  |
| L2-162 | COM-SHOP | /shop | COM-ER | /engagement-rings | Engagement Rings | Shop-by-category entry points. | RECOMMENDED | MEDIUM |  |
| L2-163 | COM-SHOP | /shop | COM-WB | /wedding-bands | Wedding Bands | Shop-by-category entry points. | RECOMMENDED | MEDIUM |  |
| L2-164 | COM-SHOP | /shop | COM-FJ | /fine-jewellery | Fine Jewelry | Shop-by-category entry points. | RECOMMENDED | MEDIUM |  |

### Subcategory ↔ parent hub, category → product, product → category/Education
| Link | Source | Source URL | Dest | Destination URL | Anchor | Purpose | S16 | Step 2 | Ownership flag |
|---|---|---|---|---|---|---|---|---|---|
| L2-109 | COM-ER | /engagement-rings | COM-PDP | /shop/<product-slug> (184 PDPs) | (product name in grid) | Product grid. | REQUIRED | HIGH |  |
| L2-110 | COM-ER | /engagement-rings | COM-PDP-OVAL-FLORAL | /shop/oval-floral-diamond-ring | Oval Marquise Diamond Engagement Ring | Ranking PDP stays in the engagement-ring grid while live. | REQUIRED | HIGH |  |
| L2-119 | COM-ER-SIDESTONE | /engagement-rings/by-design/side-stone-rings | COM-PDP | /shop/<product-slug> (184 PDPs) | (product name in grid) | Product grid. | REQUIRED | HIGH |  |
| L2-120 | COM-ER-SIDESTONE | /engagement-rings/by-design/side-stone-rings | COM-PDP-OVAL-FLORAL | /shop/oval-floral-diamond-ring | Oval Marquise Diamond Engagement Ring | The ranking PDP is a side-stone design (Stage 10 title). | REQUIRED | HIGH |  |
| L2-146 | COM-FJ-BRACELETS | /fine-jewellery/bracelet | COM-PDP | /shop/<product-slug> (184 PDPs) | (product name in grid) | Product grid. | REQUIRED | HIGH |  |
| L2-136 | COM-FJ-EARRINGS | /fine-jewellery/earrings | COM-PDP | /shop/<product-slug> (184 PDPs) | (product name in grid) | Product grid. | REQUIRED | HIGH |  |
| L2-141 | COM-FJ-NECKLACES | /fine-jewellery/necklaces | COM-PDP | /shop/<product-slug> (184 PDPs) | (product name in grid) | Product grid. | REQUIRED | HIGH |  |
| L2-175 | COM-PDP | /shop/<product-slug> (184 PDPs) | COM-ER | /engagement-rings | Engagement Rings | Breadcrumb to the primary category (engagement-ring PDPs). | REQUIRED | MEDIUM |  |
| L2-176 | COM-PDP | /shop/<product-slug> (184 PDPs) | COM-WB | /wedding-bands | Wedding Bands | Breadcrumb to the primary category (band PDPs). | REQUIRED | MEDIUM |  |
| L2-177 | COM-PDP | /shop/<product-slug> (184 PDPs) | COM-FJ-EARRINGS | /fine-jewellery/earrings | Earrings | Breadcrumb to the primary category (earring PDPs). | REQUIRED | MEDIUM |  |

### FAQ and supporting pages → Bespoke / owners
| Link | Source | Source URL | Dest | Destination URL | Anchor | Purpose | S16 | Step 2 | Ownership flag |
|---|---|---|---|---|---|---|---|---|---|
| L2-099 | NAV-HOME | / | COM-ER | /engagement-rings | House of Diams engagement rings | Stage 12 D-18: the homepage hands the engagement-ring subject to its … | REQUIRED | HIGH |  |
| L2-368 | SUP-FAQ | /faq | EDU-LG-01 | /blog/are-lab-grown-diamonds-real-a-complete-buyer-s-guide | more on whether lab-grown diamonds are real | D14-30: legitimacy -> EDU-LG-01. | REQUIRED | HIGH |  |
| L2-369 | SUP-FAQ | /faq | EDU-LG-02 | /blog/lab-grown-vs-natural-diamonds-the-honest-comparison-house-of-dia | our full lab-grown vs natural comparison | D14-30: lab vs natural -> EDU-LG-02 (protected ranking URL). | REQUIRED | HIGH |  |
| L2-370 | SUP-FAQ | /faq | EDU-CERT-00 | /blog/igi-certification-for-lab-grown-diamonds-what-it-means-house-of- | how diamond certification works | D14-30: certification -> EDU-CERT-00. | REQUIRED | HIGH |  |
| L2-372 | SUP-FAQ | /faq | EDU-RJG-02 | /blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-hous | how to measure your ring size | D14-30: resizing -> EDU-RJG-02 for the general explanation. | REQUIRED | HIGH |  |
| L2-374 | SUP-FAQ | /faq | SUP-POLICIES | /shipping and /returns | shipping and returns policies | Service answers. | REQUIRED | HIGH |  |
| L2-375 | SUP-FAQ | /faq | BRAND-CONTACT | /contact | contact us | Service answers. | REQUIRED | HIGH |  |
| L2-116 | COM-ER | /engagement-rings | COM-BESPOKE | /bespoke | create a custom engagement ring | Bespoke is the commercial alternative for shoppers who do not find a … | RECOMMENDED | MEDIUM |  |
| L2-188 | COM-PDP | /shop/<product-slug> (184 PDPs) | COM-BESPOKE | /bespoke | Commission a bespoke piece | Alternative path for custom requests. | OPTIONAL | LOW |  |
| L2-100 | NAV-HOME | / | COM-FJ | /fine-jewellery | Earrings, necklaces and bracelets | Second product family. | RECOMMENDED | MEDIUM |  |
| L2-101 | NAV-HOME | / | COM-WB | /wedding-bands | Wedding bands | Product family. | RECOMMENDED | MEDIUM |  |
| L2-102 | NAV-HOME | / | COM-BESPOKE | /bespoke | Design a bespoke piece | Service entry. | RECOMMENDED | MEDIUM |  |

### Step 2A additions (links created by the resolutions: re-homed/new Education pages, canonicalized pages)

| Link | Source | Source URL | Dest | Destination URL | Anchor | Purpose | S16 | Step 2 | Ownership flag |
|---|---|---|---|---|---|---|---|---|---|
| L2A-001 | EDU-ROOT | /education | EDU-WB-TYPES | URL PENDING (slug not decided) — Types of wedding rings: wedding band  | types of wedding rings, explained | Education index lists the re-homed style catalog (OD-04). | n/a (Step 2A addition) | MEDIUM |  |
| L2A-002 | EDU-ROOT | /education | EDU-WB-GUIDE | URL PENDING (slug not decided) — How to choose a wedding band (planned | how to choose a wedding band | Education index lists the buying guide. | n/a (Step 2A addition) | MEDIUM |  |
| L2A-003 | EDU-ROOT | /education | EDU-RJG-BR | URL PENDING (slug not decided) — Bracelet size chart (planned Educatio | bracelet size chart | Sizing reference listed under Ring & Jewelry Guides. | n/a (Step 2A addition) | MEDIUM |  |
| L2A-004 | EDU-ROOT | /education | EDU-RJG-NL | URL PENDING (slug not decided) — Necklace length chart (planned Educat | necklace length chart | Sizing reference listed under Ring & Jewelry Guides. | n/a (Step 2A addition) | MEDIUM |  |
| L2A-005 | EDU-WB-TYPES | URL PENDING (slug not decided) — Types of wedding rings: wedding band  | EDU-WB-GUIDE | URL PENDING (slug not decided) — How to choose a wedding band (planned | how to choose a wedding band | Boundary: styles here, buying decision there; ship together. | n/a (Step 2A addition) | HIGH |  |
| L2A-006 | EDU-WB-GUIDE | URL PENDING (slug not decided) — How to choose a wedding band (planned | EDU-WB-TYPES | URL PENDING (slug not decided) — Types of wedding rings: wedding band  | the main wedding band styles | Boundary link; ship together. | n/a (Step 2A addition) | HIGH |  |
| L2A-007 | EDU-WB-TYPES | URL PENDING (slug not decided) — Types of wedding rings: wedding band  | COM-WB | /wedding-bands | browse diamond wedding bands | Decision-point exit (Stage 16 §3.1). | n/a (Step 2A addition) | MEDIUM |  |
| L2A-008 | EDU-WB-TYPES | URL PENDING (slug not decided) — Types of wedding rings: wedding band  | SUB:/wedding-bands/for-her/eternity | /wedding-bands/for-her/eternity | eternity bands | One-home for eternity commercial intent (OD-16). | n/a (Step 2A addition) | LOW |  |
| L2A-009 | EDU-WB-GUIDE | URL PENDING (slug not decided) — How to choose a wedding band (planned | COM-WB | /wedding-bands | browse diamond wedding bands | Decision-point exit. | n/a (Step 2A addition) | MEDIUM |  |
| L2A-010 | COM-WB | /wedding-bands | EDU-WB-GUIDE | URL PENDING (slug not decided) — How to choose a wedding band (planned | how to choose a wedding band | Category copy: one sentence + link; counts toward the ≤5 Education li… | n/a (Step 2A addition) | MEDIUM |  |
| L2A-011 | BC-037 | /blog/<slug generated from Article Title> — Engagement ring vs wedding | EDU-WB-TYPES | URL PENDING (slug not decided) — Types of wedding rings: wedding band  | the types of wedding rings | Blog posts link to the single Education owner. | n/a (Step 2A addition) | MEDIUM |  |
| L2A-012 | BC-007 | /blog/how-to-wear-an-engagement-ring-and-wedding-band | EDU-WB-TYPES | URL PENDING (slug not decided) — Types of wedding rings: wedding band  | wedding band styles | Blog posts link to the single Education owner. | n/a (Step 2A addition) | MEDIUM |  |
| L2A-013 | BC-022 | /blog/<slug generated from Article Title> — How to stack rings: engage | EDU-WB-TYPES | URL PENDING (slug not decided) — Types of wedding rings: wedding band  | wedding band styles | Blog posts link to the single Education owner. | n/a (Step 2A addition) | MEDIUM |  |
| L2A-014 | BC-023 | /blog/<slug generated from Article Title> — Eternity ring meaning: whe | EDU-WB-TYPES | URL PENDING (slug not decided) — Types of wedding rings: wedding band  | eternity and other band styles | Eternity meaning stays Blog; styles live in Education. | n/a (Step 2A addition) | LOW |  |
| L2A-015 | EDU-RJG-BR | URL PENDING (slug not decided) — Bracelet size chart (planned Educatio | COM-FJ-BRACELETS | /fine-jewellery/bracelet | browse diamond bracelets | Decision-point exit. | n/a (Step 2A addition) | MEDIUM |  |
| L2A-016 | EDU-RJG-BR | URL PENDING (slug not decided) — Bracelet size chart (planned Educatio | SUB:/fine-jewellery/bracelet/tennis | /fine-jewellery/bracelet/tennis | tennis bracelets | Sizing page for tennis bracelets (calendar title). | n/a (Step 2A addition) | MEDIUM |  |
| L2A-017 | COM-FJ-BRACELETS | /fine-jewellery/bracelet | EDU-RJG-BR | URL PENDING (slug not decided) — Bracelet size chart (planned Educatio | how to measure your wrist | Category intro link. | n/a (Step 2A addition) | MEDIUM |  |
| L2A-018 | SUB:/fine-jewellery/bracelet/tennis | /fine-jewellery/bracelet/tennis | EDU-RJG-BR | URL PENDING (slug not decided) — Bracelet size chart (planned Educatio | bracelet size chart | Subcategory intro link. | n/a (Step 2A addition) | MEDIUM |  |
| L2A-019 | EDU-RJG-NL | URL PENDING (slug not decided) — Necklace length chart (planned Educat | COM-FJ-NECKLACES | /fine-jewellery/necklaces | browse diamond necklaces and pendants | Decision-point exit. | n/a (Step 2A addition) | MEDIUM |  |
| L2A-020 | COM-FJ-NECKLACES | /fine-jewellery/necklaces | EDU-RJG-NL | URL PENDING (slug not decided) — Necklace length chart (planned Educat | necklace length chart | Category intro link. | n/a (Step 2A addition) | MEDIUM |  |
| L2A-021 | BC-006 | /blog/necklace-layering-how-to-layer-necklaces | EDU-RJG-NL | URL PENDING (slug not decided) — Necklace length chart (planned Educat | necklace length chart | Layering = styling (Blog); lengths = sizing reference (Education). | n/a (Step 2A addition) | MEDIUM |  |
| L2A-022 | EDU-INS | URL PENDING (slug not decided) — Engagement ring insurance (planned Ed | BC-024 | /blog/<slug generated from Article Title> — How much should an engagem | how much an engagement ring costs | Cost PAA is owned by BC-024. | n/a (Step 2A addition) | LOW |  |
| L2A-023 | EDU-INS | URL PENDING (slug not decided) — Engagement ring insurance (planned Ed | COM-ER | /engagement-rings | browse engagement rings | Single optional exit; no HOD insurance/appraisal service claim (F-E5). | n/a (Step 2A addition) | LOW |  |
| L2A-024 | EDU-RJG-03 | NO URL (conditional) — Jewelry care & everyday wear | EDU-RJG-02 | /blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-hous | ring size guide | Related ring guide. | n/a (Step 2A addition) | LOW |  |
| L2A-025 | EDU-RJG-03 | NO URL (conditional) — Jewelry care & everyday wear | COM-ER | /engagement-rings | browse engagement rings | Single optional exit; no cleaning-service claim (F-E5). | n/a (Step 2A addition) | LOW |  |
| L2A-026 | EDU-ROOT | /education | EXIST-BLOG-ER-ONLINE | /blog/how-to-choose-a-lab-grown-diamond-engagement-ring-online-house-o | buying a lab-grown engagement ring online | OD-13: transitional listing; article retained unchanged. | n/a (Step 2A addition) | LOW |  |
| L2A-027 | SUB:/wedding-bands/for-her | /wedding-bands/for-her | COM-WB | /wedding-bands | wedding bands | Canonical target; breadcrumb parent. | n/a (Step 2A addition) | HIGH |  |
| L2A-028 | COM-ER-STYLES-GROUP | /engagement-rings/by-design | COM-ER | /engagement-rings | engagement rings | Canonical target (OD-06). | n/a (Step 2A addition) | HIGH |  |

## 7. Template-level items (implement once, Class B)

* **Header menu** links filter-parameter URLs (`?shape=…`, `?metal=…`): they are `noindex, follow` + canonical to the parent — keep that behavior on AWS; whether crawlable parameter links belong in the menu is an engineering decision.
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
