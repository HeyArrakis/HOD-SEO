# 04 — Keyword → URL Ownership Validation

Generated 2026-10-09. Validates the existing Stage 15 ownership system (and the Stage 12/14/16/19 + final-calendar layers on top of it) against the master map and the live site. **Nothing in the ownership files was changed.** Recommendations at the end are proposals with evidence; they require your decision.

Scope of the check: Stage 15 (`15_keyword_url_map.csv` 1,936 keywords; `15_target_page_registry.csv` 27 targets), `15_cannibalization_check.csv`, final calendar (62 scheduled items), Stage 19 briefs, and the live crawl of 2026-10-09.

## 1. Confirmed ownership (Stage 15 targets vs live)

| Target | Page | Stage 15 status | Registry URL | Live HTTP | Calendar | Verdict |
|---|---|---|---|---|---|---|
| EDU-LG-00 | Lab-grown diamonds explained (Lab-Grown Education hub pil… | PROPOSED | /education/lab-grown-diamonds | n/a | EDU-LG-00 · 2026-10-21 | OWNER CONFIRMED in architecture — page not built |
| EDU-LG-01 | Are lab-grown diamonds real? (authenticity) | EXISTING_MOVE_WHEN_CONDITIONS_MET | /blog/are-lab-grown-diamonds-real-a-complete-buyer-s-guide | 200 | EDU-LG-01 · 2026-12-02 | CONFIRMED — URL live (200, self-canonical) |
| EDU-LG-02 | Lab-grown vs natural diamonds (comparison) | EXISTING_KEEP | /blog/lab-grown-vs-natural-diamonds-the-honest-comparison-house-of-diams | 200 | EDU-LG-02 · 2026-11-25 | CONFIRMED — URL live (200, self-canonical) |
| EDU-LG-03 | CVD vs HPHT (single home for CVD and HPHT) | EXISTING_KEEP | /blog/cvd-vs-hpht-lab-grown-diamonds-what-buyers-should-know-house-of-diams | 200 | EDU-LG-03 · 2027-01-21 | CONFIRMED — URL live (200, self-canonical) |
| EDU-LG-05 | Lab-grown diamond price, value & resale | PROPOSED_PROVISIONAL | URL_PENDING | n/a | EDU-LG-05 · 2026-12-11 | OWNER CONFIRMED — slug undecided (URL_PENDING) |
| EDU-LG-07 | Lab-grown diamond ethics & sustainability | PROPOSED_PROVISIONAL | URL_PENDING | n/a | EDU-LG-07 · 2027-01-25 | OWNER CONFIRMED — slug undecided (URL_PENDING) |
| EDU-LG-08 | Lab-grown diamond appearance & durability | PROPOSED_PROVISIONAL | URL_PENDING | n/a | EDU-LG-08 · 2027-01-19 | OWNER CONFIRMED — slug undecided (URL_PENDING) |
| EDU-LG-09 | Detecting lab-grown diamonds (testers & identification) | PROPOSED_PROVISIONAL | URL_PENDING | n/a | EDU-LG-09 · 2026-11-30 | OWNER CONFIRMED — slug undecided (URL_PENDING) |
| EDU-LG-10 | How to choose a lab-grown diamond (buying guide) | EXISTING_KEEP_MIGRATION_DEFERRED | /blog/how-to-choose-a-lab-grown-diamond-the-complete-buyer-s-guide | 200 | — | CONFIRMED — URL live (200, self-canonical) |
| EDU-NAT-00 | Natural diamonds: formation & origin (Natural Education h… | PROPOSED_PROVISIONAL | URL_PENDING | n/a | EDU-NAT-00 · 2026-12-14 | OWNER CONFIRMED — slug undecided (URL_PENDING) |
| EDU-4C-00 | The 4Cs of diamond quality (4Cs hub pillar, incl. lab-gro… | EXISTING_MOVE_WHEN_CONDITIONS_MET | /blog/the-4cs-of-lab-grown-diamonds-explained-cut-colour-clarity-and-carat-house-of-diams | 200 | EDU-4C-00 · 2026-12-10 | CONFIRMED — URL live (200, self-canonical) |
| EDU-4C-01 | Diamond clarity guide | PROPOSED | /education/diamond-4cs/diamond-clarity | n/a | EDU-4C-01 · 2026-11-11 | OWNER CONFIRMED in architecture — page not built |
| EDU-4C-02 | SI clarity diamonds (SI1, SI2, SI3) | PROPOSED | /education/diamond-4cs/si-clarity-diamonds | n/a | EDU-4C-02 · 2026-12-17 | OWNER CONFIRMED in architecture — page not built |
| EDU-4C-03 | VVS, IF & flawless clarity diamonds | PROPOSED | /education/diamond-4cs/vvs-diamonds | n/a | EDU-4C-03 · 2026-11-20 | OWNER CONFIRMED in architecture — page not built |
| EDU-4C-05 | Diamond color guide (D to Z) | PROPOSED | /education/diamond-4cs/diamond-color | n/a | EDU-4C-05 · 2026-11-16 | OWNER CONFIRMED in architecture — page not built |
| EDU-4C-06 | Diamond cut guide (cut grade, facets, light performance) | PROPOSED | /education/diamond-4cs/diamond-cut | n/a | EDU-4C-06 · 2026-11-17 | OWNER CONFIRMED in architecture — page not built |
| EDU-4C-07 | Diamond carat guide | PROPOSED_PROVISIONAL | URL_PENDING | n/a | EDU-4C-07 · 2026-11-19 | OWNER CONFIRMED — slug undecided (URL_PENDING) |
| EDU-SHP-00 | Diamond shapes guide (Shapes hub pillar, incl. engagement… | EXISTING_MOVE_WHEN_CONDITIONS_MET | /blog/the-best-lab-grown-diamond-shapes-for-engagement-rings-house-of-diams | 200 | EDU-SHP-00 · 2026-11-13 | CONFIRMED — URL live (200, self-canonical) |
| EDU-CERT-00 | Diamond certification explained (Certification hub pillar) | EXISTING_RETARGET_THEN_MOVE | /blog/igi-certification-for-lab-grown-diamonds-what-it-means-house-of-diams | 200 | EDU-CERT-00 · 2026-12-15 | CONFIRMED — URL live (200, self-canonical) |
| EDU-CERT-01 | GIA vs IGI (comparison) | EXISTING_KEEP | /education/lab-grown-diamond-certification-explained-gia-vs-igi-house-of-diams | 200 | — | CONFIRMED — URL live (200, self-canonical) |
| EDU-MET-00 | Jewelry metals guide (Metals hub pillar) | PROPOSED_PROVISIONAL | URL_PENDING | n/a | EDU-MET-00 · 2026-11-24 | OWNER CONFIRMED — slug undecided (URL_PENDING) |
| EDU-MET-01 | 14k vs 18k gold (and 10k) | EXISTING_MOVE_WHEN_CONDITIONS_MET | /blog/14k-vs-18k-gold-for-diamond-jewellery-which-is-better-house-of-diams | 200 | EDU-MET-01 · 2026-11-18 | CONFIRMED — URL live (200, self-canonical) |
| EDU-RJG-01 | Ring settings guide | PROPOSED | URL_PENDING | n/a | EDU-RJG-01 · 2027-01-04 | OWNER CONFIRMED — slug undecided (URL_PENDING) |
| EDU-RJG-02 | Ring size guide (tool embedded by default) | EXISTING_MOVE_WHEN_CONDITIONS_MET | /blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-house-of-diams | 200 | EDU-RJG-02 · 2026-11-12 | CONFIRMED — URL live (200, self-canonical) |
| EDU-GEN-01 | Diamond properties: composition, hardness & durability | PROPOSED_PROVISIONAL | URL_PENDING | n/a | EDU-GEN-01 · 2026-12-18 | OWNER CONFIRMED — slug undecided (URL_PENDING) |
| COM-ER-SIDESTONE | Engagement rings: side-stone (style subcategory) | EXISTING_KEEP | /engagement-rings/by-desgin/side-stone-rings | 404 | — | URL STALE — registry URL returns 404; see conflict C1 |
| COM-PDP-OVAL-FLORAL | Oval floral diamond ring (product page) | EXISTING_KEEP | /shop/oval-floral-diamond-ring | 200 | — | CONFIRMED — URL live (200, self-canonical) |

**Result:** 11 existing owner URLs confirmed live; 1 stale; 15 proposed/pending owners (not built). Stage 15's central claim — no keyword has two HOD owners — holds: `15_cannibalization_check` B-check = 0 duplicate owners, and this map's own check found **0 exact duplicate primary keywords across 147 rows** (the side-stone legacy row deliberately carries no keyword).

## 2. Missing URL ownership

| Gap | Count | Detail |
|---|---|---|
| Commercial hubs/categories with no ratified keyword | 9 | Engagement rings, wedding bands, fine jewellery, earrings, necklaces, bracelets, FJ rings, T-Bar (+ bespoke, below). Stage 15: *'commercial hubs have no keywords because the master database has almost no commercial category queries … a data gap, not a lack of demand'* (D-19; the supplement was never approved). |
| Commercial subcategories with no ratified keyword | 38 | Only `side-stone-rings` has an owner. The other style/type/gender pages are conditional under the D-07 gate (demand + SERP type + inventory + distinctness + one home + business fit + stability). |
| Core commercial pages with no ratified keyword | 1 | /bespoke — the calendar says COM-BESPOKE owns 'custom engagement ring' (40,500) / 'design your own engagement ring' (5,400) but Stage 15 maps neither. |
| Unowned head term, largest in the project | 1 | 'lab grown diamonds' 135,000 (+ 'lab diamonds' 27,100, 'lab created diamonds' 12,100): CL-001, CONDITIONAL_NOT_MAPPED → COM-LG-HUB (not built; business confirmation needed). |
| New Education pages with no Stage 14/15 owner | 4 | Bracelet size chart (EDU-RJG-BR), necklace length chart (EDU-RJG-NL), engagement ring insurance (EDU-INS), wedding-band buying guide (EDU-WB-GUIDE) — calendar status OWNERSHIP_CONFIRMATION. |
| Calendar primaries outside the Stage 15 map | 50 | New research (calendar says 'no Stage 15 owner'); additive, but unratified. 33 Blog posts are Blog-owned by the calendar only. |
| Pages that intentionally own no keyword | 13 | Homepage (brand), /shop, /collection, /about, /contact, /faq, policies, /blog, /education — acceptable and labelled `NO PRIMARY KEYWORD / BRAND / SUPPORTING PAGE`. |

## 3. Possible conflicts (both values shown, nothing resolved)

### 3a. Primary keyword differs between the Stage 19 brief / Stage 17 and the final calendar (same page)

| Page | Stage 17/19 primary | Calendar primary | Note |
|---|---|---|---|
| EDU-MET-01 | is 18k gold or 14k gold better | 14k vs 18k gold (12100/mo) | NOT in the Stage 15 keyword map (new research) |
| EDU-4C-00 | diamond grading scale | 4 cs of diamonds (6600/mo) | NOT in the Stage 15 keyword map (new research) |
| EDU-SHP-00 | diamond shape | diamond shapes (60500/mo) | NOT in the Stage 15 keyword map (new research) |
| EDU-RJG-02 | are mens and womens ring sizes the same | ring size chart (165000/mo) | NOT in the Stage 15 keyword map (new research) |
| EDU-LG-00 | synthetic diamonds | 'what are lab grown diamonds' (12100/mo) | Calendar term not in Stage 15 map |
| EDU-LG-09 | do lab grown diamonds pass a diamond tester | 'how to tell if a diamond is real' (18100/mo) | Calendar term not in Stage 15 map |
| EDU-4C-01 | diamond clarity grading scale | 'diamond clarity chart' (33100/mo) | Calendar term not in Stage 15 map |
| EDU-4C-03 | v v s diamond | 'vvs diamonds' (18100/mo) | Calendar term not in Stage 15 map |
| EDU-4C-05 | color grade diamond | 'diamond color scale' (27100/mo) | Calendar term not in Stage 15 map |
| EDU-4C-06 | diamond cut grade | 'diamond cut' (60500/mo) | Calendar term not in Stage 15 map |
| EDU-4C-07 | is 1 carat diamond good | 'diamond carat size chart' (4400/mo) | Calendar term not in Stage 15 map |
| EDU-MET-00 | types of jewelry metals | 'white gold vs platinum' (8100/mo) | Calendar term not in Stage 15 map |

Both terms point to one page, so this is **not** two pages competing — but the choice changes the title/H1 and which volume the page is judged on. Example: EDU-LG-00 would be 'synthetic diamonds' 2,900 (brief) or 'what are lab grown diamonds' 12,100 (calendar, SERP-validated in Stage 18.5). Stage 15 page ownership is unaffected. **Needs your ratification before the 20 new pages are written.**

### 3b. Calendar items that Stage 14/15 do not cover (ownership confirmation flagged by the calendar itself)

| Calendar ID | Primary | Vol | Proposed owner | Calendar's own risk note |
|---|---|---|---|---|
| EDU-RJG-BR | bracelet size chart | 5400 | NEW Education page under EDU-RJG hub (ownership co | CLEAR - no Stage 15 owner. Boundary with BC-021 (tennis bracelet meaning and wear; owns "tennis bracelet stack" and "how to stack bracelets"); this page owns sizing only. |
| EDU-RJG-NL | necklace length chart | 9900 | NEW Education page under EDU-RJG hub (ownership co | CLEAR - no Stage 15 owner (gap logged in D-BC-14). Boundary with BC-006 necklace layering: layering = styling, this = sizing reference; "necklace layering lengths" (30) stays with BC-006. Two-way lin… |
| EDU-RJG-03 | how to clean diamond ring | 3600 | EDU-RJG-03 (activation recommended) | CLEAR - EDU-RJG-03 is the Stage 14 care owner (conditional); no Blog post targets care (Stage 13). |
| EDU-LG-09 | how to tell if a diamond is real | 18100 | EDU-LG-09 (new primary proposed) | MEDIUM (documented, ownership confirmation recommended) - "how to tell if a diamond is real" is a NEW keyword (not in S15); placed in EDU-LG-09 (testers & identification) as the closest owner. Distin… |
| BLOG-WR-TYPES | types of wedding rings | 12100 | Blog (Style & Trends) | MEDIUM (documented) - two phrasings share 1 of 10 top results (C2), below the R-02 merge threshold, but they express the same need (style catalogue); merged deliberately to avoid two near-duplicate p… |
| EDU-INS | engagement ring insurance | 8100 | NEW Education page under EDU-RJG hub (ownership co | CLEAR - no Stage 15 owner. Income/budget PAA ("how much should I spend if I make $100,000") routes to BC-024. |
| EDU-RJG-01 | types of diamond settings | 720 | EDU-RJG-01 | OWNERSHIP REVIEW CARRIED (S19) - "engagement ring settings" is commercial-led (S18.5 CONFLICT) and is NOT targeted here until the review; style heads (bezel/toi et moi engagement ring) stay with cond… |
| EDU-WB-GUIDE | how to choose a wedding band | 590 | NEW Education page under EDU-RJG hub (ownership co | MEDIUM (documented) - BC-007 owns wearing order and "should engagement ring and wedding band match" (10); BC-022 owns stacks; BLOG-WR-TYPES owns the style catalogue; this page owns the buying decisio… |

### 3c. Commercial ownership claimed in notes but not mapped in Stage 15

| Claim (source) | Reality in Stage 15 / live | Evidence |
|---|---|---|
| COM-BESPOKE owns 'custom engagement ring' 40,500 and 'design your own engagement ring' 5,400 (calendar BC-001) | No Stage 15 mapping; /bespoke is a form-led page | blog_keyword_research.csv: both labelled RESERVED_COMMERCIAL_PAGE |
| COM-WB owns 'matching wedding band' 6,600, curved/contour/enhancer (calendar BLOG-WR-TYPES / EDU-WB-GUIDE) | No Stage 15 mapping; /wedding-bands has 7 products | calendar cannibalization notes |
| Style heads (toi et moi, bezel, east-west, three-stone) reserved for COM-ER style subcategories (calendar BC-031) | Subcategories exist and are populated (bezel 2, three-stone 4, toi-moi 1 products) but are 'conditional' and own no keyword | calendar BC-031 note; live crawl |
| Stage 12 D-05: COM-LG-HUB conditional | Live homepage/ER title and all PDP copy already say lab-grown; 135,000 head unowned | 15_keyword_url_map.csv CL-001 |

### 3d. Live-site changes that make recorded ownership stale

- **COM-ER-SIDESTONE:** registry/ranking-equity/link files all cite `/engagement-rings/by-desgin/side-stone-rings` (est. pos 104, 1 keyword). Live: 404; new URL `/engagement-rings/by-design/side-stone-rings` is 200. *Owner unchanged; URL record stale; 301 missing.*
- **COM-PDP-OVAL-FLORAL:** product renamed 'Oval Marquise Side-Stone Engagement Ring' (slug unchanged); its title now contains the COM-ER-SIDESTONE term 'side-stone' (MEDIUM boundary risk).
- **BRAND-CONTACT:** IA expects an indexable /contact page; live is a 307 to a modal.

## 4. Cannibalization risks

### 4a. Stage 15 'E' pairs (adjacent intents between owners) — carried forward

| Severity | Pair | Boundary rule (Stage 15) |
|---|---|---|
| MEDIUM | EDU-LG-01 ↔ EDU-LG-02 | Authenticity vs comparison: REL-020 max 2 shared URLs, both SERPs COMPARISON-dominant (D14-07). Enforce the boundary in content. Flagged for Stage 16 linking and briefs; no mapping change. |
| MEDIUM | EDU-LG-02 ↔ EDU-LG-05 | Worth-it pros/cons (interim on LG-02) vs price/value/resale: money-worry overlap (D14-10; D14-27). Flagged for Stage 16 linking and briefs; no mapping change. |
| HIGH | EDU-LG-00 ↔ EDU-LG-03 | CL-015 process queries are split between the pillar (general) and CVD vs HPHT (methods). If EDU-LG-04 is ever created, it must not target CVD/HPHT method queries (D14-08). Flagged for Stage 16 linking and briefs; no mapping change. |
| MEDIUM | EDU-4C-00 ↔ EDU-4C-01 | Lab-grown clarity-chart queries (CL-023) sit on the 4Cs pillar while general clarity-scale queries sit on the clarity guide. Separation is INSUFFICIENT_EVIDENCE (D14-15; D14-29 #3). Flagged for Stage 16 linking and briefs; no mapping change. |
| MEDIUM | EDU-CERT-00 ↔ EDU-CERT-01 | General certification vs GIA-vs-IGI: 0 shared URLs (D14-18). Both changes must ship together (Stage 13) or OV-01 persists. Flagged for Stage 16 linking and briefs; no mapping change. |
| MEDIUM | EDU-4C-06 ↔ EDU-SHP-00 | Cut grade vs shape: 'cut' is ambiguous (grade vs shape). Cut-grade queries → EDU-4C-06; shape queries → EDU-SHP-00 (D14-02 SPLIT). Flagged for Stage 16 linking and briefs; no mapping change. |
| MEDIUM | EDU-LG-08 ↔ EDU-LG-01 | 'do lab-grown diamonds look real' is appearance (EDU-LG-08), not authenticity (D14-07). Flagged for Stage 16 linking and briefs; no mapping change. |
| LOW | EDU-LG-09 ↔ EDU-LG-01 | 'do lab grown diamonds test real' wording mixes detection and authenticity; detection owns tester questions (D14-13). Flagged for Stage 16 linking and briefs; no mapping change. |
| MEDIUM | EDU-LG-00 ↔ CL-001 commercial Lab-Grown hub (conditional) | Pillar must not target the head terms; REL-004 DISTINCT_INTENT (D14-05). Flagged for Stage 16 linking and briefs; no mapping change. |
| INSUFFICIENT_EVIDENCE | EDU-LG-10 ↔ EDU-RJG-04 (deferred) | 'should i buy a lab grown diamond engagement ring' sits on the lab-grown buying guide; boundary with the deferred engagement-ring guide is unresolved (OV-06; D-19). Flagged for Stage 16 linking and briefs; no mapping change. |
| LOW | EDU-4C-02 ↔ EDU-4C-01 | SI SERP shares 0 URLs with the clarity scale (D14-14). Flagged for Stage 16 linking and briefs; no mapping change. |
| LOW | EDU-4C-03 ↔ EDU-4C-01 | VVS SERP shares 1 URL with the clarity scale (D14-14). Flagged for Stage 16 linking and briefs; no mapping change. |

Stage 15 conclusion: *no actual cannibalization is demonstrated; the pairs are boundaries to enforce in content (Stage 19) and linking (Stage 16)*. The highest, **EDU-LG-00 ↔ EDU-LG-03 (HIGH)**, concerns process queries (CL-015); EDU-LG-04 must never target CVD/HPHT method terms.

### 4b. New risks found by mapping live + calendar pages together — CANNIBALIZATION REVIEW REQUIRED

| Pages | Risk | Why | Suggested handling (not applied) |
|---|---|---|---|
| Homepage ↔ /engagement-rings ↔ COM-LG-HUB | MEDIUM | Homepage title 'Lab-Grown Diamond Engagement Rings & Fine Jewellery' (Stage 10 OV-13) covers the category subject and the unowned lab-grown head. | Brand-led homepage title; decide COM-LG-HUB; keep category subject on /engagement-rings. |
| /engagement-rings ↔ /engagement-rings/by-design | HIGH | Identical grid (61 pieces on both), same boilerplate FAQ, both indexable, self-canonical and in the sitemap. | Decide canonical/redirect/unique-index; do not merge automatically. |
| /wedding-bands/for-her/eternity ↔ /fine-jewellery/rings/eternity-rings | MEDIUM | Same subject, two homes; one is empty. 'eternity ring/band' (12,100/9,900) labelled informational by DFS. | One-home decision (P-ONE-HOME); SERP check before assigning. |
| /fine-jewellery/bracelet ↔ /fine-jewellery/bracelet/tennis ↔ BC-021 | MEDIUM | 'tennis bracelet' 135,000 commercial head vs hub vs child; BC-021 'what is a tennis bracelet' 3,600 informational. | Child owns the commercial head; BC-021 stays informational (documented boundary). |
| Earrings hub ↔ stud/hoop/drop children ↔ BC-025 | MEDIUM | 'diamond stud earrings' 49,500 vs hub 'diamond earrings' 74,000; BC-025 'different types of earrings' 1,600. | Stage 15 CL-125 REVIEW: assign stud head to the stud child; hub keeps broad term. |
| /t-bar ↔ /fine-jewellery/necklaces/pendant-necklace | MEDIUM | Stage 10 OV-16; 4 vs 3 products. | D-14 decision: curated collection vs subtype. |
| /faq ↔ Education owners (EDU-LG-01/02/03, EDU-4C-00) | MEDIUM | FAQ answers lab-grown vs natural, CVD/HPHT, 4Cs in full. | One-line answer + link (D-18, D14-30). |
| /bespoke ↔ BC-001 (and BC-024) | LOW–MEDIUM | Informational timeline post vs commercial 'custom engagement ring' heads. | Boundary already documented; keep heads on /bespoke. |
| /shop/oval-floral-diamond-ring ↔ /engagement-rings/by-design/side-stone-rings | MEDIUM | PDP title now says 'Side-Stone'. | Keep 'oval'/'marquise' as lead terms in the PDP. |
| IGI certification article ↔ GIA-vs-IGI article (OV-01) | MEDIUM | Both live, one topic (CLEAR_OVERLAP in Stage 10). | Retarget/ship both changes together (Stage 13). |
| BC-036 ↔ BC-038 ↔ BC-039 ↔ BC-007 (finger/hand/order posts) | LOW–MEDIUM | Adjacent SERPs share 2 URLs ('what finger does a wedding ring go on' vs 'what hand does engagement ring go on'). | Calendar boundary notes assign each question; keep exact wording separate. |
| BC-004 ↔ BC-008 ↔ BC-009 ↔ BC-035 ↔ BC-018 (gift series) | LOW–MEDIUM | SERPs of BC-008/BC-009 share 2 URLs; hub vs recipient posts. | Series rule: hub owns generic holiday gifts; recipient posts keep recipient primaries. |
| BLOG-WR-TYPES ↔ EDU-WB-GUIDE ↔ BC-037 ↔ BC-007 ↔ BC-022 | MEDIUM | Wedding-band topics split across Blog and Education; 1 of 10 results shared. | Confirm Blog-vs-Education ownership (flagged). |

### 4c. Automated checks on this map

- Exact duplicate primary keywords across rows: **0**.
- A row's primary keyword appearing as another row's secondary keyword: **0**.
- Calendar secondaries that map to a *different* Stage 15 target than the calendar item's own page: **0** (checked all 62 items; matches the calendar's own 'PASS' notes).
- SERP overlap ≥2 shared top-10 URLs (calendar round-2): 'how to layer necklaces' / 'necklace layering' (4 — already merged into BC-006); 'ring finger meaning' / 'what do rings on each finger mean' (3 — one post, BC-038); 'jewelry gifts for girlfriend' / 'wife' (2 — kept separate, series rule); 'what finger does a wedding ring go on' / 'what hand does engagement ring go on' (2 — split BC-036/BC-007 by question).

## 5. Orphan keyword clusters (keywords with no live or planned owner)

| Cluster | Name | Unowned kws | Σ volume | Top keyword | Dispositions | Nearest home today |
|---|---|---|---|---|---|---|
| CL-001 | Lab-Grown Diamonds: General & Head Terms | 27 | 314,020 | diamond growing lab (135,000) | CONDITIONAL 27 | COM-LG-HUB (not built) — business decision |
| CL-090 | Moissanite: General & Head Terms | 13 | 205,620 | moissanite (201,000) | DEFERRED 13 | EDU-GEM-03 (deferred) |
| UNCLUSTERED_REVIEW |  | 154 | 94,840 | diamond stone (18,100) | REVIEW_REQUIRED 154 | Needs human triage (brand/dual meaning) |
| CL-006 | Lab-Grown Diamonds by Carat Weight | 6 | 19,940 | 2 ct lab created diamond (6,600) | DEFERRED 6 | Loose-stone pages (deferred; are loose stones sold?) |
| CL-105 | Coloured Gemstone Rings & Jewellery (Tanzan… | 11 | 19,840 | tanzanite rings (12,100) | EXCLUDE_COMMERCIAL 11 | — |
| CL-061 | Asscher Cut Diamonds | 4 | 19,650 | asscher cut diamond (18,100) | DEFERRED 4 | — |
| CL-070 | Natural Diamonds: General & Head Terms | 5 | 19,060 | natural diamonds (18,100) | DEFERRED 5 | Natural commercial hub (deferred) |
| CL-065 | Types of Diamonds (General Overview) | 7 | 16,870 | diamond types (6,600) | CONDITIONAL 7 | EDU-GEN-02 (conditional; 'types of diamonds' sense unresolved) |
| CL-102 | Lab-Created Gemstones (General & Other Ston… | 18 | 15,450 | lab created gemstones (3,600) | DEFERRED 18 | — |
| CL-071 | Rough & Raw Diamonds | 8 | 15,250 | raw diamond (9,900) | EXCLUDE_COMMERCIAL 5, DEFERRED 3 | — |
| CL-103 | Natural Gemstones & Stones (Opal, Jade, Pea… | 15 | 14,760 | natural pearls (3,600) | DEFERRED 15 | — |
| CL-100 | Sapphire: Natural, Lab-Created & White Sapp… | 14 | 13,740 | lab grown sapphire (3,600) | DEFERRED 14 | — |
| CL-095 | Diamond Simulants & Alternatives | 16 | 12,910 | simulated diamond (4,400) | CONDITIONAL 16 | EDU-GEM-00 (conditional) |
| CL-094 | Cubic Zirconia vs Diamond & Lab-Grown Diamo… | 12 | 10,840 | cubic zirconia vs diamond (3,600) | CONDITIONAL 12 | — |
| CL-123 | Mixed Metal Rings | 2 | 8,800 | mixed metal ring (4,400) | DEFERRED 2 | `/fine-jewellery/rings` (FJ rings, DEFER) |
| CL-051 | Fancy-Colored Diamonds (Black, Red, Pink, G… | 15 | 8,480 | are black diamonds real (1,600) | CONDITIONAL 15 | — |
| CL-104 | Morganite Rings & Jewellery | 4 | 8,390 | morganite rings (8,100) | EXCLUDE_COMMERCIAL 4 | — |
| CL-093 | Do Moissanite Pass a Diamond Tester? | 9 | 6,120 | do moissanite pass diamond tester (1,900) | DEFERRED 9 | — |

Totals (Stage 15): CONDITIONAL_NOT_MAPPED 140 kws / 379,760 vol; DEFERRED_NOT_MAPPED 127 kws / 336,560 vol; REVIEW_REQUIRED 156 kws / 94,960 vol; EXCLUDE_COMMERCIAL 59 kws / 48,690 vol. Volumes are DataForSEO Labs monthly US searches and overlap across variants — treat as magnitude, not additive traffic.

## 6. Pages without clear keyword ownership

| Row group | Rows without an owner or with only candidates |
|---|---|
| COMMERCIAL SUBCATEGORY | 39 |
| CONDITIONAL EDUCATION | 13 |
| CORE LIVE | 11 |
| COMMERCIAL CATEGORY | 9 |
| LEGACY / REDIRECT | 5 |
| HUBS | 2 |
| PRODUCT PAGES | 1 |
| EXISTING ARTICLES (Education-owned) | 1 |
| CONDITIONAL COMMERCIAL | 1 |

Every mapped page states either a keyword owner, `NO RATIFIED PRIMARY (D-19 …)` with candidate evidence, or `NO PRIMARY KEYWORD / BRAND / SUPPORTING PAGE`. Pages with *no* such statement: **0** (checked programmatically).

## 7. Keywords on inappropriate page types

**7a. Transactional/navigational labels inside Education owners — 36 keywords** (DataForSEO intent labels, none SERP-validated). Largest: 'cvd diamond' 3,600 → EDU-LG-03; 'gia lab diamonds' 2,400 → EDU-CERT-00; 'diamond inclusions' 1,900 → EDU-4C-01; 'diamond pipes' 1,300 → EDU-NAT-00; 'igi lab grown diamond' 1,000 → EDU-CERT-00; 'diamond facet' 1,000 → EDU-4C-06; 'hpht lab created diamonds' 880 → EDU-LG-03; 'hpht lab diamonds' 720 → EDU-LG-03. Stage 15 already marks these LOW confidence; they are informational in practice ('cvd diamond', 'diamond inclusions') but confirm with SERPs before relying on the labels. **Recommendation: none beyond SERP validation when budget allows.**

**7b. Informational-labelled heads reserved for commercial pages:** 'eternity ring' 12,100 / 'eternity band' 9,900 and 'toi et moi ring' 27,100 are DFS-informational but sit on commercial subcategories (and BC-023 'eternity ring meaning' is a blog) — SERP check required before assigning (risk: commercial page for an informational SERP).

**7c. Commercial/transactional SERPs targeted by Blog posts:** BC-008 'jewelry gifts for wife' and BC-009 'jewelry gifts for girlfriend' are SERP-verified TRANSACTIONAL_OR_COMMERCIAL (product/category + marketplace results lead); BC-004/BC-035 are MIXED commercial-research. Their primaries are small (320–390/mo; BC-035 33,100) and the calendar already limits them to listicle/guide format and avoids broad heads ('christmas gifts for wife' 27,100). **Risk: product-led SERPs favour commercial pages — keep these as guides linking to category pages, set expectations on traffic.** No change proposed.

**7d. Blog-vs-Education:** BLOG-WR-TYPES ('types of wedding rings' 12,100) is a Blog post while Stage 13 assigns 'how to choose / types' reference intent to Education — flagged by the calendar for confirmation.

**7e. Informational answers living on a support page:** /faq (see 4b).

## 8. Recommendations (evidence-supported; not applied)

| # | Recommendation | Evidence | Guardrail |
|---|---|---|---|
| R1 | Add a 1:1 301 for the renamed side-stone URL and update the research registry's recorded URL after the redirect exists. | Live 404 + ranking-equity file; CLAUDE.md rules 11–12. | Do not change ownership; change only the URL record. |
| R2 | Ratify a primary keyword for every Education page where the calendar and Stage 19 brief differ (12 pages) before writing; default to the SERP-validated calendar term with the Stage 15 term as co-primary. | §3a table. | Ownership of the page stays with Stage 15. |
| R3 | Confirm the 8 OWNERSHIP_CONFIRMATION items (4 new Education pages, EDU-LG-09 co-primary, EDU-RJG-01, EDU-RJG-03 activation, BLOG-WR-TYPES). | §3b; calendar notes. | Until confirmed, rows stay `REVIEW`. |
| R4 | Ratify commercial hub/child ownership using the candidate lists already in the map (zero cost): one owner per head term, hub = broad term, child = specific type; resolve 'lab grown diamond engagement rings' (COM-ER vs COM-LG-HUB). | §2, §3c; blog_keyword_research.csv RESERVED_COMMERCIAL_PAGE; Stage 12 D-05/D-07/D-19. | If SERP validation of commercial heads is wanted, submit a priced plan first (CLAUDE.md DataForSEO rules). |
| R5 | Decide COM-LG-HUB: the catalogue is lab-grown, so 'conditional' may no longer hold; the 135,000 head is unowned. | §5; live positioning. | Needs business confirmation of products + certification. |
| R6 | Resolve /engagement-rings vs /engagement-rings/by-design, and eternity (WB vs FJ rings), as one-home decisions. | §4b. | No automatic merge/delete. |
| R7 | Assign 'diamond stud earrings' (CL-125, 49,500) to the stud-earrings child once the D-07 gate is documented. | §5; Stage 15 CL-125 REVIEW. | Informational stud queries stay with EDU-4C-07. |
| R8 | Keep FAQ answers to one line + link (D-18). | §4b. | — |
| R9 | Triage the 156 REVIEW_REQUIRED keywords (94,960 vol): mostly dual-meaning/brand terms; likely excludable. | §5. | Human triage; no paid call needed. |
| R10 | Re-run this validation after AWS cut-over and after GSC data is available (GSC will show whether any two HOD URLs actually rank for one query). | GSC not available this session. | — |

## 9. Method and limits

- Ownership data are Stage 15 (frozen); live data from the 2026-10-09 read-only crawl; volumes/KD are existing DataForSEO values (no new calls, $0.00).
- Heuristic checks (e.g. entity/question presence in article text) are labelled heuristic in the CSV; they flag candidates for review, not defects.
- Without GSC, actual query→URL competition is unknown; cannibalization here is **risk by design**, not observed.
