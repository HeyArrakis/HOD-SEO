# 10 — Decisions Resolution Log (Step 2A)

Date 2026-10-10. **Authority:** the user delegated routine and research-supported decisions on 2026-10-10. **Scope:** decisions only — nothing is implemented; the final calendar, Stage 12–19 research files, Step 1 outputs and approved blog packages were not modified (Stage 15 ownership files are untouched; this log and `10-COMMERCIAL-KEYWORD-ASSIGNMENTS.csv` are the ratification record, per CLAUDE.md §10). **No paid DataForSEO call.** The original proposals are preserved in `09`.

## 1. Summary of dispositions (all 19 decisions)

| ID | Decision | Disposition | Final resolution (short) | Confidence |
|---|---|---|---|---|
| OD-01 | Commercial keyword ownership (Stage 12 D-19 gap) | **ADOPTED** | Keyword ownership is assigned for the 9 category hubs, the subcategories and /bespoke — one primary keyword per URL (hub = broad head, child = specific type, bespoke/custom kept distinct from the engagement-ring catalog). Full ta… | HIGH for hub heads and the side-stone owner |
| OD-02 | COM-LG-HUB / lab-grown positioning | **ADOPTED — NO SEPARATE HUB NOW; HOD FACT PENDING** | No separate commercial Lab-Grown hub now. 'lab grown diamond engagement rings' / 'lab grown diamond rings' (90,500 each) become secondary targets of /engagement-rings once HOD confirms all catalog stones are lab-grown; the head t… | MEDIUM |
| OD-03 | Education primary-keyword ratification (12 pages) | **ADOPTED** | R2 adopted for all 12: calendar (SERP-validated) term is primary, the Stage 17/19 term is co-primary or a section question; page owners unchanged; titles/H1s updated (see §4). | HIGH |
| OD-04 | Education / Blog ownership confirmation (8 items) | **ADOPTED** | All 8 items resolved: EDU-RJG-BR, EDU-RJG-NL, EDU-INS, EDU-WB-GUIDE, EDU-LG-09, EDU-RJG-01, EDU-RJG-03 are Education owners; 'types of wedding rings' is a single Education page (EDU-WB-TYPES, calendar ID BLOG-WR-TYPES kept as ali… | HIGH |
| OD-05 | 'Jewelry' vs 'jewellery' (Stage 12 D-15) | **ADOPTED (CONFIRMED PROJECT RULE)** | American English everywhere customer-facing (jewelry, color, center, customize). Slugs unchanged. | HIGH |
| OD-06 | Redirects & duplicate grouping page | **ADOPTED** | Developer redirect map adopted: 8 style URLs + the group URL, each 1:1 301 from /engagement-rings/by-desgin/<x> → /engagement-rings/by-design/<x> (targets confirmed live). The /engagement-rings/by-design duplicate group page gets… | HIGH |
| OD-07 | Empty / test pages policy | **ADOPTED** | Rule adopted and applied page by page (§5): 0 products → noindex,follow + out of sitemap/nav/llms.txt until populated; test artifact removed; no redirect to irrelevant pages; legitimate children preserved. | HIGH |
| OD-08 | Trust-critical business facts | **PARTLY ADOPTED — HOD INPUT PENDING** | Bespoke timeline applied everywhere ('typically 2–3 weeks to make, ~6–9 days delivery, generally ~3–4 weeks from design approval to delivery; stone-dependent; not guaranteed'). Every other unverified or contradictory claim is rem… | HIGH |
| OD-09 | /contact page vs modal | **ADOPTED — HOD CONTACT FACTS PENDING** | A real, crawlable /contact page is adopted (200, indexable, self-canonical, in sitemap; /?contact=open canonicalizes to it) with the existing inquiry fields; no contact details invented. | MEDIUM-HIGH |
| OD-10 | FAQ vs Education boundary | **ADOPTED** | FAQ answers become one line + link to the Education owner; policy answers neutral until F-A1/F-A2. | HIGH |
| OD-11 | Author / byline policy | **ADOPTED** | Default byline and schema author = 'House of Diams' (Organization). A named person only where identity, role and credentials are verified; visible byline and structured data must match. The approved packages' 'Written By = HOD Te… | HIGH |
| OD-12 | Blog vs Journal naming; hub pagination | **ADOPTED** | Public section name standardized to 'Blog' (URL /blog unchanged; 'Back to Journal' → 'Back to Blog'; anchors updated). H1 'Stories from House of Diams' kept. Paginated listings: self-referencing canonicals, 'Page N' titles where … | HIGH |
| OD-13 | Existing-article moves and the Education index | **ADOPTED** | No URL moves in this phase. Education-owned /blog articles are listed on /education by topic; the Blog hub keeps listing them until their Education path exists (Stage 16). | HIGH |
| OD-14 | PDP variant URLs | **ADOPTED (KEEP; REVIEW DEFERRED)** | Keep the 10 carat-variant PDP URLs; no merge, delete or redirect now. Review after cut-over with GSC data. | HIGH |
| OD-15 | Oval-floral PDP naming/boundary | **ADOPTED — GSC BASELINE BEFORE LIVE CHANGE** | Title 2.5 ct Oval Marquise Diamond Engagement Ring; H1 'Oval Marquise Diamond Engagement Ring'; Product schema name = H1; slug unchanged. Live change waits for the GSC baseline. | HIGH |
| OD-16 | One-home decisions | **ADOPTED (REVERSIBLE DEFAULTS)** | One home per intent: eternity → /wedding-bands/for-her/eternity (FJ eternity page empty/noindex); toi et moi ring ≠ necklace (disjoint sets); T-bar stays a separate collection (0 overlap with pendants); solitaire pendant vs penda… | MEDIUM |
| OD-17 | Content freeze / publishing window / CMS location (engineering) | **INTAKE PREPARED — ENGINEERING INPUT PENDING (NON-BLOCKING FOR SPEC)** | Engineering intake prepared (`12-ENGINEERING-INPUTS.md`, E-01…E-13). Specification is not blocked; every Class B item stays post-migration. | n/a |
| OD-18 | GSC baseline | **REQUEST PREPARED — GSC DATA PENDING (BLOCKS EQUITY-PAGE EDITS ONLY)** | GSC request prepared (`13-GSC-DATA-REQUEST.md`, G-01…G-06). Only edits to ranking-equity URLs wait for it. | n/a |
| OD-19 | Natural-diamond offer | **BUNDLED WITH OD-08 — HOD INPUT PENDING; NEUTRAL FRAMING ADOPTED** | Bundled with the HOD questionnaire (F-E2). Education framing stays neutral; no claim that HOD sells natural or loose stones. | n/a |

Dispositions: **ADOPTED** (decision made and propagated), **ADOPTED — … PENDING** (decision made; a named external fact/data item refines or reverses it), **INTAKE/REQUEST PREPARED** (genuinely external; specification not blocked). No decision is left silently unresolved.

## 2. Method and evidence rules

* **Evidence types.** *SERP-VALIDATED* (Stage 8/18.5) is claimed for only four head terms: 'side stones engagement rings' (CATEGORY-dominant), 'lab grown diamonds', 'lab diamonds' and 'natural diamonds'. Every other commercial assignment is *volume + DataForSEO intent label (SERP type NOT validated)* — stated per row.
* **Confidence.** HIGH = broad head → hub or unique specific match, measured volume, consistent with the architecture; MEDIUM = measured volume with unvalidated SERP type or some intent ambiguity; LOW = proxy volume, thin inventory or ambiguous head.
* **Inventory** facts come from product links in the initial HTML of the 2026-10-09 crawl (listing pages cap at 24, so large counts are lower bounds).
* **Reversible defaults** are used wherever evidence cannot settle a question; none involves a URL change or an irreversible index action.
* **No fake precision:** no scores, no invented volumes; GSC values are never shown.

## 3. Decisions in detail

### OD-01 — Commercial keyword ownership (Stage 12 D-19 gap)

**Disposition: ADOPTED**

* **Original proposal (09):** PROVISIONAL: keep titles/H1s as neutral descriptive names (as drafted); ratify the candidate list in §3 using existing data; defer any SERP validation until after AWS/GSC.
* **Final resolution:** Keyword ownership is assigned for the 9 category hubs, the subcategories and /bespoke — one primary keyword per URL (hub = broad head, child = specific type, bespoke/custom kept distinct from the engagement-ring catalog). Full table: `10-COMMERCIAL-KEYWORD-ASSIGNMENTS.csv`. Stage 15 itself is untouched; this log is the ratification record.
* **Rationale:** Existing US datasets already hold measured heads for most pages (volume + DFS intent label). Where no head is measured the page is deliberately not promoted rather than forced. Inventory facts come from the 2026-10-09 initial-HTML product sets.
* **Evidence / sources:** blog_keyword_research.csv / master keyword DB / QA evidence kwlookup.json (volumes, KD, DFS labels); Stage 8 SERP validation (only 'side stones engagement rings', 'lab grown diamonds', 'lab diamonds', 'natural diamonds'); Stage 12 D-03/D-05/D-07/D-08/D-18; Stage 16 anchor strategy; crawl 2026-10-09.
* **Confidence:** HIGH for hub heads and the side-stone owner; MEDIUM for most children (volume measured, SERP type NOT validated); LOW for thin-inventory pages.
* **External dependency:** None blocking. GSC Queries (G-02) later confirm or overturn volume-only assignments.
* **Reversibility / review:** Reversible per page; review triggers in §6.

### OD-02 — COM-LG-HUB / lab-grown positioning

**Disposition: ADOPTED — NO SEPARATE HUB NOW; HOD FACT PENDING**

* **Original proposal (09):** PROVISIONAL: keep hub/home titles origin-neutral until decided. If (a): hub title 'Lab-Grown Diamonds' + 'EDU-LG-00' stays educational; if (c): /engagement-rings title becomes 'Lab-Grown Diamond Engagement Rings: …'.
* **Final resolution:** No separate commercial Lab-Grown hub now. 'lab grown diamond engagement rings' / 'lab grown diamond rings' (90,500 each) become secondary targets of /engagement-rings once HOD confirms all catalog stones are lab-grown; the head terms 'lab grown diamonds' (135,000), 'lab diamonds' (27,100), 'lab created diamonds' (12,100) stay unowned by design; EDU-LG-00 stays informational.
* **Rationale:** A hub would duplicate /shop (finished jewelry only, all lab-grown), fail D-07 distinctness/one-home, and compete on a SERP of loose-stone retailer collections HOD cannot match without loose stones.
* **Evidence / sources:** Stage 8 (lab grown diamonds = NAVIGATIONAL; lab diamonds = TRANSACTIONAL, retailer collection pages); Stage 12 D-05; Stage 16 §3.3; catalog = rings/bands/earrings/necklaces/bracelets only (crawl); PDP spec tables 'Stone Type: Lab Grown Diamond'.
* **Confidence:** MEDIUM (no SERP evidence for the engagement-ring variant).
* **External dependency:** F-E1 (all stones lab-grown?) activates the secondary heads; F-E2 (loose lab-grown stones sold/planned?) is the single fact that would reverse the recommendation.
* **Reversibility / review:** Preferred option if F-E2 = yes: build the hub (own the head terms; Stage 16 hub links activate).

### OD-03 — Education primary-keyword ratification (12 pages)

**Disposition: ADOPTED**

* **Original proposal (09):** RECOMMENDATION (not adopted): adopt R2 for all 12 — calendar term primary, brief term co-primary. Titles for both options are in §4.
* **Final resolution:** R2 adopted for all 12: calendar (SERP-validated) term is primary, the Stage 17/19 term is co-primary or a section question; page owners unchanged; titles/H1s updated (see §4).
* **Rationale:** Each pair points to one page; the calendar terms carry the larger, SERP-validated demand (e.g. ring size chart 165,000 vs 1,000). No source contradicts R2; 2 pairs are mere wording variants (shapes, VVS).
* **Evidence / sources:** QA/04 §3a; calendar rounds + Stage 18.5; Stage 15 map; Stage 19 briefs.
* **Confidence:** HIGH.
* **External dependency:** Four of the pages sit on ranking-equity or Stage 13 URLs: MET-01 title change waits for the GSC baseline.
* **Reversibility / review:** Fully reversible (titles only).

### OD-04 — Education / Blog ownership confirmation (8 items)

**Disposition: ADOPTED**

* **Original proposal (09):** RECOMMENDATION: confirm the four new EDU-RJG pages as Education (sizing/insurance/buying decision), activate EDU-RJG-03, keep RJG-01 off 'engagement ring settings', and place 'types of wedding rings' in Education only if the Stage 13 reference-intent rule is to be applied literally.
* **Final resolution:** All 8 items resolved: EDU-RJG-BR, EDU-RJG-NL, EDU-INS, EDU-WB-GUIDE, EDU-LG-09, EDU-RJG-01, EDU-RJG-03 are Education owners; 'types of wedding rings' is a single Education page (EDU-WB-TYPES, calendar ID BLOG-WR-TYPES kept as alias, date/slot unchanged).
* **Rationale:** Stage 13 §3 assigns sizing, care, testing/identification and permanent buying guides to Education; §4 tests (shelf-life, question, ownership, brand) point 'types of wedding rings' to Education ('if tests disagree, Education wins for anything a searcher would ask repeatedly'). Blog posts BC-037/007/022/023 stay Blog and link to it.
* **Evidence / sources:** 13_blog_strategy.md §3–4; Stage 14 EDU-RJG-* rows; calendar boundary notes; Stage 19 ownership review; S18.5 'engagement ring settings' conflict.
* **Confidence:** HIGH (Education vs Blog); MEDIUM for EDU-INS (cost/insurance content is partly time-bound).
* **External dependency:** None blocking. Hub-index page EDU-RJG-00 now meets its activation condition (≥2 child guides) — documented follow-up, not scheduled.
* **Reversibility / review:** Calendar annotation done 2026-10-10: BLOG-WR-TYPES target_owner = EDU-WB-TYPES (the only calendar field changed).

### OD-05 — 'Jewelry' vs 'jewellery' (Stage 12 D-15)

**Disposition: ADOPTED (CONFIRMED PROJECT RULE)**

* **Original proposal (09):** PROVISIONAL: US spelling in all recommended copy (marked PROVISIONAL). Slugs unchanged.
* **Final resolution:** American English everywhere customer-facing (jewelry, color, center, customize). Slugs unchanged.
* **Rationale:** Confirmed project rule (US market).
* **Evidence / sources:** User instruction 2026-10-10; Stage 12 D-15; 23 vs 1 keyword usage.
* **Confidence:** HIGH.
* **External dependency:** None.
* **Reversibility / review:** n/a

### OD-06 — Redirects & duplicate grouping page

**Disposition: ADOPTED**

* **Original proposal (09):** RECOMMENDATION: approve §6 as written; canonicalize the group page to /engagement-rings and drop it from the sitemap; keep child URLs.
* **Final resolution:** Developer redirect map adopted: 8 style URLs + the group URL, each 1:1 301 from /engagement-rings/by-desgin/<x> → /engagement-rings/by-design/<x> (targets confirmed live). The /engagement-rings/by-design duplicate group page gets canonical → /engagement-rings, leaves the sitemap, and stops being linked; children preserved.
* **Rationale:** Identical product set (24 = 24) and FAQ; D-03/P-DEPTH. Redirecting the group page is held back only because PDP breadcrumbs still link to it (E-13) and GSC evidence is absent.
* **Evidence / sources:** crawl 2026-10-09 (404s, targets 200 in sitemap); Stage 10; Stage 12 D-03; Stage 16 §5.
* **Confidence:** HIGH (1:1 redirects); MEDIUM (canonical vs redirect for the group page).
* **External dependency:** E-03/E-04 (implementation); GSC G-03 confirms indexed state — non-blocking.
* **Reversibility / review:** Group page → 301 later once no internal link points to it.

### OD-07 — Empty / test pages policy

**Disposition: ADOPTED**

* **Original proposal (09):** RECOMMENDATION: adopt the rule; remove /hiphop/test-subcat outright.
* **Final resolution:** Rule adopted and applied page by page (§5): 0 products → noindex,follow + out of sitemap/nav/llms.txt until populated; test artifact removed; no redirect to irrelevant pages; legitimate children preserved.
* **Rationale:** Stage 12 D-13/P-EMPTY/P-NO-TEST; reversible (population simply re-enables indexing).
* **Evidence / sources:** crawl 2026-10-09 product counts; Stage 12 D-13.
* **Confidence:** HIGH.
* **External dependency:** E-05 (per-page noindex + sitemap exclusion).
* **Reversibility / review:** Re-evaluate on population with the D-07 gate.

### OD-08 — Trust-critical business facts

**Disposition: PARTLY ADOPTED — HOD INPUT PENDING**

* **Original proposal (09):** RECOMMENDATION: until supplied, remove or soften the claims rather than keep unverified ones; use the confirmed bespoke wording only.
* **Final resolution:** Bespoke timeline applied everywhere ('typically 2–3 weeks to make, ~6–9 days delivery, generally ~3–4 weeks from design approval to delivery; stone-dependent; not guaranteed'). Every other unverified or contradictory claim is removed or made neutral. One consolidated questionnaire issued (`11-HOD-CLIENT-FACTS-REQUEST.md`).
* **Rationale:** Only the bespoke timeline is confirmed; guessing shipping, returns, warranty, certification or founder facts would create public false statements.
* **Evidence / sources:** confirmed_business_facts.md; user instruction 2026-10-10; live pages re-read 2026-10-09.
* **Confidence:** HIGH.
* **External dependency:** HOD answers (F-A1…F-E7) complete /shipping, /returns, /about, /contact and upgrade claims elsewhere.
* **Reversibility / review:** n/a

### OD-09 — /contact page vs modal

**Disposition: ADOPTED — HOD CONTACT FACTS PENDING**

* **Original proposal (09):** PROVISIONAL: build a real page (entity/NAP consistency).
* **Final resolution:** A real, crawlable /contact page is adopted (200, indexable, self-canonical, in sitemap; /?contact=open canonicalizes to it) with the existing inquiry fields; no contact details invented.
* **Rationale:** Stage 12 expects a BRAND-CONTACT page; entity/NAP consistency; FAQ already points at /contact.
* **Evidence / sources:** Stage 12; crawl (307 → modal); modal topics.
* **Confidence:** MEDIUM-HIGH.
* **External dependency:** F-C2 (public contact set); E-12 (build).
* **Reversibility / review:** Fallback: keep modal and fix references.

### OD-10 — FAQ vs Education boundary

**Disposition: ADOPTED**

* **Original proposal (09):** RECOMMENDATION: approve.
* **Final resolution:** FAQ answers become one line + link to the Education owner; policy answers neutral until F-A1/F-A2.
* **Rationale:** Stage 14 D14-30; Stage 12 D-18.
* **Evidence / sources:** QA/04 §4b.
* **Confidence:** HIGH.
* **External dependency:** None.
* **Reversibility / review:** n/a

### OD-11 — Author / byline policy

**Disposition: ADOPTED**

* **Original proposal (09):** RECOMMENDATION: Organization byline unless a real expert reviews content.
* **Final resolution:** Default byline and schema author = 'House of Diams' (Organization). A named person only where identity, role and credentials are verified; visible byline and structured data must match. The approved packages' 'Written By = HOD Team' is standardized to 'House of Diams' at CMS entry (packages not edited).
* **Rationale:** No verified expert identities exist; founder names are inconsistent (F-C1).
* **Evidence / sources:** Package seo-metadata.md (author Person 'HOD Team'); live bylines.
* **Confidence:** HIGH.
* **External dependency:** E-07 (template author field); F-C1 only for named authors.
* **Reversibility / review:** n/a

### OD-12 — Blog vs Journal naming; hub pagination

**Disposition: ADOPTED**

* **Original proposal (09):** PROVISIONAL: neutral title (no label) until decided.
* **Final resolution:** Public section name standardized to 'Blog' (URL /blog unchanged; 'Back to Journal' → 'Back to Blog'; anchors updated). H1 'Stories from House of Diams' kept. Paginated listings: self-referencing canonicals, 'Page N' titles where supported.
* **Rationale:** Nav and URL already say Blog; consistency; Stage 13 category rules unchanged.
* **Evidence / sources:** crawl (/blog H1/canonical behavior); Stage 16.
* **Confidence:** HIGH.
* **External dependency:** E-06 (template support for page-number titles; canonical is the minimum).
* **Reversibility / review:** n/a

### OD-13 — Existing-article moves and the Education index

**Disposition: ADOPTED**

* **Original proposal (09):** RECOMMENDATION: no URL moves in this phase.
* **Final resolution:** No URL moves in this phase. Education-owned /blog articles are listed on /education by topic; the Blog hub keeps listing them until their Education path exists (Stage 16).
* **Rationale:** Stage 13 move conditions are not met; ranking URLs.
* **Evidence / sources:** Stage 13 content-migration risk; Stage 16 §4/§8.
* **Confidence:** HIGH.
* **External dependency:** None.
* **Reversibility / review:** Moves re-open only with a Stage 13 plan.

### OD-14 — PDP variant URLs

**Disposition: ADOPTED (KEEP; REVIEW DEFERRED)**

* **Original proposal (09):** RECOMMENDATION: keep; revisit with GSC data.
* **Final resolution:** Keep the 10 carat-variant PDP URLs; no merge, delete or redirect now. Review after cut-over with GSC data.
* **Rationale:** No consolidation evidence; each variant has distinct carat/price.
* **Evidence / sources:** QA/06 flags; IA D-11.
* **Confidence:** HIGH.
* **External dependency:** G-01 for the later review; E-09.
* **Reversibility / review:** n/a

### OD-15 — Oval-floral PDP naming/boundary

**Disposition: ADOPTED — GSC BASELINE BEFORE LIVE CHANGE**

* **Original proposal (09):** RECOMMENDATION: approve.
* **Final resolution:** Title 2.5 ct Oval Marquise Diamond Engagement Ring; H1 'Oval Marquise Diamond Engagement Ring'; Product schema name = H1; slug unchanged. Live change waits for the GSC baseline.
* **Rationale:** Stage 15 owner of 'marquise oval diamond' (est. pos 90 = DataForSEO estimate); keeps COM-ER-SIDESTONE separate.
* **Evidence / sources:** live PDP re-read (JSON-LD name ≠ H1).
* **Confidence:** HIGH.
* **External dependency:** G-01/G-02.
* **Reversibility / review:** n/a

### OD-16 — One-home decisions

**Disposition: ADOPTED (REVERSIBLE DEFAULTS)**

* **Original proposal (09):** PROVISIONAL: keep 'ring'/'necklace' in the titles to separate the pairs; no merges.
* **Final resolution:** One home per intent: eternity → /wedding-bands/for-her/eternity (FJ eternity page empty/noindex); toi et moi ring ≠ necklace (disjoint sets); T-bar stays a separate collection (0 overlap with pendants); solitaire pendant vs pendant necklace (0 overlap) split by qualifier; stud earrings child owns 'diamond stud earrings', hub keeps 'diamond earrings'.
* **Rationale:** Initial-HTML product sets are disjoint for every pair except hub-vs-child (stud: expected). No merges needed.
* **Evidence / sources:** crawl product-set comparison 2026-10-09; Stage 12 D-07 #4–5.
* **Confidence:** MEDIUM (volume-only; informational-labeled heads unvalidated).
* **External dependency:** G-02 later.
* **Reversibility / review:** Each default is reversible; no URL changes.

### OD-17 — Content freeze / publishing window / CMS location (engineering)

**Disposition: INTAKE PREPARED — ENGINEERING INPUT PENDING (NON-BLOCKING FOR SPEC)**

* **Original proposal (09):** Needed to date every Class B item.
* **Final resolution:** Engineering intake prepared (`12-ENGINEERING-INPUTS.md`, E-01…E-13). Specification is not blocked; every Class B item stays post-migration.
* **Rationale:** These are engineering facts.
* **Evidence / sources:** QA/02 §8.
* **Confidence:** n/a
* **External dependency:** E-01…E-13.
* **Reversibility / review:** n/a

### OD-18 — GSC baseline

**Disposition: REQUEST PREPARED — GSC DATA PENDING (BLOCKS EQUITY-PAGE EDITS ONLY)**

* **Original proposal (09):** Do not block preparation; block only title/H1 edits on ranking URLs.
* **Final resolution:** GSC request prepared (`13-GSC-DATA-REQUEST.md`, G-01…G-06). Only edits to ranking-equity URLs wait for it.
* **Rationale:** No GSC data; DataForSEO positions are estimates.
* **Evidence / sources:** CLAUDE.md §5.
* **Confidence:** n/a
* **External dependency:** G-01…G-06.
* **Reversibility / review:** n/a

### OD-19 — Natural-diamond offer

**Disposition: BUNDLED WITH OD-08 — HOD INPUT PENDING; NEUTRAL FRAMING ADOPTED**

* **Original proposal (09):** PROVISIONAL: Education framing stays neutral; no claim that HOD sells natural stones.
* **Final resolution:** Bundled with the HOD questionnaire (F-E2). Education framing stays neutral; no claim that HOD sells natural or loose stones.
* **Rationale:** Offer unconfirmed.
* **Evidence / sources:** Stage 12 D-05 deferred question.
* **Confidence:** n/a
* **External dependency:** F-E2.
* **Reversibility / review:** n/a


## 4. Education resolutions

### OD-03 — the 12 primary-keyword mismatches (R2 adopted)

| Page | Final primary | Co-primary / treatment of the brief term | Final title (pre-suffix) | Final H1 | Status | Note |
|---|---|---|---|---|---|---|
| EDU-MET-01 | '14k vs 18k gold' (12,100/mo) | co-primary: 'is 18k gold or 14k gold better' (Stage 17/19) — answered in the first section | 14K vs 18K Gold (and 10K) for Diamond Jewelry | 14K vs 18K Gold (and 10K) for Diamond Jewelry: Which Is Better? | GSC BASELINE REQUIRED | Existing ranking-equity URL: title/H1 change waits for the GSC baseline |
| EDU-4C-00 | '4 cs of diamonds' (6,600/mo) | co-primary: 'diamond grading scale' (Stage 17/19) | The 4Cs of Diamonds Explained | The 4Cs of Diamonds Explained: Cut, Color, Clarity and Carat | READY FOR IMPLEMENTATION POST-AWS | Pillar; depth handed to 4C-01/05/06/07 |
| EDU-SHP-00 | 'diamond shapes' (60,500/mo) | co-primary: 'diamond shape' (same volume 60,500 — wording variant) | Diamond Shapes: Chart and How to Choose | Diamond Shapes Guide: The 10 Main Shapes and How to Choose One | READY FOR IMPLEMENTATION POST-AWS | Single page; no new page |
| EDU-RJG-02 | 'ring size chart' (165,000/mo) | 'are mens and womens ring sizes the same' (Stage 17/19, 1,000) becomes an H2 answer block, not a co-primary | Ring Size Chart: How to Measure Your Size | Ring Size Guide: Ring Size Chart and How to Measure Your Size at Home | READY FOR IMPLEMENTATION POST-AWS | Largest volume in the plan; tool optional |
| EDU-LG-00 | 'what are lab grown diamonds' (12,100/mo) | co-primary: 'synthetic diamonds' (2,900) via the 'other names' section | What Are Lab-Grown Diamonds? | What Are Lab-Grown Diamonds? Definition, Other Names and How They Are Made | PRE-AWS PREPARATION | Must not take commercial head terms |
| EDU-LG-09 | 'how to tell if a diamond is real' (18,100/mo) | co-primary: 'do lab grown diamonds pass a diamond tester' (720) | How to Tell If a Diamond Is Real | How to Tell If a Diamond Is Real: At-Home Tests, Jeweler Tests and Why Lab-Grown Diamonds Pass a Tester | PRE-AWS PREPARATION | Generic testing intent with lab-grown tester section; boundary with EDU-LG-01/08 |
| EDU-4C-01 | 'diamond clarity chart' (33,100/mo) | co-primary: 'diamond clarity grading scale' (12,100) | Diamond Clarity Chart: FL to I3 Explained | Diamond Clarity Chart: Every Grade From FL to I3, Eye-Clean Grades and Which Clarity to Buy | PRE-AWS PREPARATION | General scale here; lab-grown clarity-chart queries stay on the pillar (MEDIUM pair) |
| EDU-4C-03 | 'vvs diamonds' (18,100/mo) | co-primary: 'v v s diamond' (same volume — spacing variant) | VVS Diamonds: VVS1 vs VVS2 Explained | VVS Diamonds: What VVS1 and VVS2 Mean, How They Compare With VS and Flawless, and Whether VVS Is Worth It | PRE-AWS PREPARATION | Title identical either way |
| EDU-4C-05 | 'diamond color scale' (27,100/mo) | co-primary: 'color grade diamond' | Diamond Color Scale: D-to-Z Chart | Diamond Color Scale: D-to-Z Color Chart, What Each Grade Looks Like and Which Color to Buy | PRE-AWS PREPARATION | — |
| EDU-4C-06 | 'diamond cut' (60,500/mo) | co-primary: 'diamond cut grade' | Diamond Cut: Grades, Cut vs Shape and Sparkle | Diamond Cut: What Cut Grade Means, Cut vs Shape, and How Cut Drives Sparkle | PRE-AWS PREPARATION | Cut-grade here; shape queries → EDU-SHP-00 |
| EDU-4C-07 | 'diamond carat size chart' (4,400/mo) | 'is 1 carat diamond good' (320) becomes a section question, not a co-primary | Diamond Carat Size Chart by Shape | Diamond Carat Size Chart: Carat to Millimeters by Shape and What Size to Choose | PRE-AWS PREPARATION | Informational stud queries land here |
| EDU-MET-00 | 'white gold vs platinum' (8,100/mo) | co-primary: 'types of jewelry metals' | Jewelry Metals Guide: White Gold vs Platinum | Jewelry Metals Guide: White Gold vs Platinum, Yellow vs White vs Rose Gold, and the Best Metal for Rings | PRE-AWS PREPARATION | No claim that HOD offers platinum (F-E4) |

### OD-04 — the 8 ownership items

| Item | Final owner | Treatment | Source rule | Status |
|---|---|---|---|---|
| EDU-RJG-BR | EDU-RJG-BR — Education (Ring & Jewelry Guides) | Sizing reference = Education (Stage 13 §3 'ring sizing…reference'). Owns 'bracelet size chart' only; BC-021 keeps tennis-bracelet meaning/wear. | Stage 13 §3, tests 1–2; calendar boundary note | PRE-AWS PREPARATION |
| EDU-RJG-NL | EDU-RJG-NL — Education (Ring & Jewelry Guides) | Sizing reference = Education. BC-006 keeps layering/styling. | Stage 13 §3; D-BC-14 gap note | PRE-AWS PREPARATION |
| EDU-INS | EDU-INS — Education (Ring & Jewelry Guides) | Permanent 'is it worth it / what does it cover' buying question = Education; no personalized financial advice; no HOD insurance/appraisal service claims (F-E5). | Stage 13 §3 permanent buying guides, tests 1–2 | PRE-AWS PREPARATION |
| EDU-WB-GUIDE | EDU-WB-GUIDE — Education (Ring & Jewelry Guides) | Permanent 'how to choose' buying guide = Education; owns the buying decision (metal, width, fit, pairing). | Stage 13 §3; boundary BC-007/BC-022/EDU-WB-TYPES | PRE-AWS PREPARATION |
| EDU-LG-09 | EDU-LG-09 — Education (Lab-Grown) | Co-primary adopted (see OD-03). Testing/identification reference is Education. | Stage 13 §3 'testing/identification reference'; Stage 14 EDU-LG-09 | PRE-AWS PREPARATION |
| EDU-RJG-01 | EDU-RJG-01 — Education (Ring & Jewelry Guides) | Targets 'types of diamond settings' (720). 'engagement ring settings' stays off (S18.5 commercial-led CONFLICT); style heads stay on commercial child pages, which this guide links to. | Stage 19 ownership review carried; S18.5 | PRE-AWS PREPARATION |
| EDU-RJG-03 | EDU-RJG-03 — Education (Ring & Jewelry Guides) — ACTIVATED | Care is Education (Stage 13 keeps care in Education); no Blog post targets care. Activation condition met (≥2 child guides in the hub). No HOD cleaning/appraisal service claims (F-E5). | Stage 13 §3; Stage 14 EDU-RJG-03; calendar note | PRE-AWS PREPARATION |
| BLOG-WR-TYPES | EDU-WB-TYPES — Education (Ring & Jewelry Guides); calendar ID BLOG-WR-TYPES retained as alias | Stage 13 §4 tests: shelf-life ✓ (permanent), question ✓ ('types of …' stable query), ownership ✓ (no Blog owner), brand test ✗ → Education; 'if tests disagree Education wins'. One page only: owns the style catalog ('types of wedding rings' 12,100); EDU-WB-GUIDE owns the buying decision; BC-037/007/022/023 stay Blog and link here. Calendar date/slot unchanged. | Stage 13 §3–4; calendar cannibalization note (merged phrasings) | PRE-AWS PREPARATION |

## 5. Developer-ready redirect and index-control specification (planning only — Class B)

**Redirects (OD-06)** — 1:1, permanent (301), no chains, query strings preserved (E-04):

| # | Source (404 today) | Destination (200, in sitemap) | Type | Why | Priority | Note |
|---|---|---|---|---|---|---|
| R-01 | /engagement-rings/by-desgin/solitare-rings | /engagement-rings/by-design/solitare-rings | 301 | Typo path (404, re-verified 2026-10-10). Target confirmed live 2026-10-10 (200, self-canonical; in the 2026-10-09 sitemap). | HIGH | Live at the old path per Stage 10; may be indexed — GSC check is non-blocking |
| R-02 | /engagement-rings/by-desgin/halo-ring | /engagement-rings/by-design/halo-ring | 301 | Typo path (404, re-verified 2026-10-10). Target confirmed live 2026-10-10 (200, self-canonical; in the 2026-10-09 sitemap). | HIGH | Live at the old path per Stage 10; may be indexed — GSC check is non-blocking |
| R-03 | /engagement-rings/by-desgin/toi-moi-rings | /engagement-rings/by-design/toi-moi-rings | 301 | Typo path (404, re-verified 2026-10-10). Target confirmed live 2026-10-10 (200, self-canonical; in the 2026-10-09 sitemap). | HIGH | Live at the old path per Stage 10; may be indexed — GSC check is non-blocking |
| R-04 | /engagement-rings/by-desgin/pave | /engagement-rings/by-design/pave | 301 | Typo path (404, re-verified 2026-10-10). Target confirmed live 2026-10-10 (200, self-canonical; in the 2026-10-09 sitemap). | HIGH | Live at the old path per Stage 10; may be indexed — GSC check is non-blocking |
| R-05 | /engagement-rings/by-desgin/nature-inspired-rings | /engagement-rings/by-design/nature-inspired-rings | 301 | Typo path (404, re-verified 2026-10-10). Target confirmed live 2026-10-10 (200, self-canonical; in the 2026-10-09 sitemap). | HIGH | Live at the old path per Stage 10; may be indexed — GSC check is non-blocking |
| R-06 | /engagement-rings/by-desgin/three-stone-rings | /engagement-rings/by-design/three-stone-rings | 301 | Typo path (404, re-verified 2026-10-10). Target confirmed live 2026-10-10 (200, self-canonical; in the 2026-10-09 sitemap). | HIGH | Live at the old path per Stage 10; may be indexed — GSC check is non-blocking |
| R-07 | /engagement-rings/by-desgin/bezel-rings | /engagement-rings/by-design/bezel-rings | 301 | Typo path (404, re-verified 2026-10-10). Target confirmed live 2026-10-10 (200, self-canonical; in the 2026-10-09 sitemap). | HIGH | Live at the old path per Stage 10; may be indexed — GSC check is non-blocking |
| R-08 | /engagement-rings/by-desgin/side-stone-rings | /engagement-rings/by-design/side-stone-rings | 301 | Typo path (404, re-verified 2026-10-10). Target confirmed live 2026-10-10 (200, self-canonical; in the 2026-10-09 sitemap). | CRITICAL | Stage 15 keyword-owner URL |
| R-09 | /engagement-rings/by-desgin | /engagement-rings/by-design | 301 | 1:1 to the corresponding valid group URL (which itself canonicalizes to /engagement-rings). | LOW | Old grouping URL |

**Duplicate grouping page (OD-06):** `/engagement-rings/by-design` — canonical → /engagement-rings; remove from sitemap; stop internal links to the group page (breadcrumbs, nav) ; child pages untouched. Reason: Identical 24 = 24 initial-HTML products and the same boilerplate FAQ as /engagement-rings; D-03/P-DEPTH. Redirect remains the alternative once no internal link points here and GSC shows no standalone demand.

**Empty and test pages (OD-07)** — each handled individually; none redirected to an irrelevant destination:

| Page | Treatment | Redirect? | Note |
|---|---|---|---|
| /collection | noindex,follow; out of sitemap, nav and /llms.txt | No redirect (empty, no equity; /shop is the all-products listing but a redirect would hide a template defect) | Revisit if engineering confirms /collection is a retired route → 301 /shop |
| /engagement-rings/round-rings | noindex,follow; out of sitemap/nav; shape stays a filter (D-08) | No redirect — shape filter URLs already canonicalize to the parent | Shape landing pages: opportunity logged, not adopted |
| /wedding-bands/for-him | noindex,follow; out of sitemap/nav | No redirect (irrelevant destinations) | CONDITIONAL on men's range (F-E3) |
| /wedding-bands/for-him/classic | noindex,follow; out of sitemap/nav | No redirect | CONDITIONAL on men's range (F-E3) |
| /wedding-bands/for-him/diamonds | noindex,follow; out of sitemap/nav | No redirect | CONDITIONAL on men's range (F-E3) |
| /wedding-bands/for-him/designer | noindex,follow; out of sitemap/nav | No redirect | CONDITIONAL on men's range (F-E3) |
| /wedding-bands/for-her/nature | noindex,follow; out of sitemap/nav until populated | No redirect | Populate or retire — merchandising |
| /wedding-bands/for-her/solid | noindex,follow; out of sitemap/nav until populated | No redirect | Populate or retire — merchandising |
| /wedding-bands/for-her/cigar-band | noindex,follow; out of sitemap/nav until populated | No redirect | Populate or retire — merchandising |
| /wedding-bands/for-her/pavee | noindex,follow; out of sitemap/nav until populated | No redirect | Slug typo 'pavee' — fix only with a migration plan if populated |
| /fine-jewellery/earrings/tennis-earrings | noindex,follow; out of sitemap/nav until populated | No redirect | Remove the empty tab from the earrings hub |
| /fine-jewellery/earrings/personalized-charm | noindex,follow; out of sitemap/nav until populated | No redirect | Personalization service unconfirmed (F-E5) |
| /fine-jewellery/necklaces/tennis-necklace | noindex,follow; out of sitemap/nav until populated | No redirect | Reserved head 'tennis necklace' (33,100) activates on population |
| /fine-jewellery/necklaces/initials | noindex,follow; out of sitemap/nav until populated | No redirect | Reserved head 'initial necklace' (40,500); personalization unconfirmed (F-E5) |
| /fine-jewellery/rings/eternity-rings | noindex,follow; out of sitemap/nav until populated | No redirect (one-home is /wedding-bands/for-her/eternity) | Do not redirect to a populated page that serves a different (bridal) intent |
| /hiphop/chains | noindex,follow; out of sitemap/nav | No redirect (parent /hiphop already 308 → /shop) | CONDITIONAL on Hip Hop range (F-E3) |
| /hiphop/chains/cuban-links | noindex,follow; out of sitemap/nav | No redirect | CONDITIONAL on Hip Hop range (F-E3) |
| /hiphop/test-subcat | REMOVE: return 404/410; delete the record; out of sitemap | No redirect (test artifact has no equity) | Stage 12 D-13 / P-NO-TEST |

**Other URL behaviors:**

| URL / set | Treatment | Dependency |
|---|---|---|
| /contact | Replace the 307-to-modal with a real indexable /contact page (200, self-canonical, in sitemap); /?contact=open canonicalizes to /contact | OD-09; HOD contact facts F-C2; engineering E-12 |
| /hiphop | Keep 308 → /shop (range unconfirmed) | OD-07; F-E3 |
| /shop/marquise-floral-diamond-engagement-ring | 404 today; 301 to nearest equivalent ONLY if the GSC Pages export shows impressions/links; otherwise leave 404/410 | GSC G-01 |
| /shop/fine-jewellery-test-product | Keep 404/410 | — |
| Slug typos (solitare ×2, anniversay, pavee, singular /bracelet, toi-moi vs toi-et-moi) | NO URL change; fix visible category names to US spelling/correct words only | OD-05; CLAUDE.md rule 12 |
| /blog?page=N | Self-referencing canonical per distinct page; title 'Blog – Page N' | OD-12; E-06 |
| /shop?page=N and /engagement-rings?page=N | Self-referencing canonical; add 'Page N' to title/H1 for N>1 | E-06 |

**Implementation notes for developers:** (1) apply `noindex,follow` via meta robots (not robots.txt) so crawlers can see the directive; (2) remove the same URLs from sitemap.xml, `/llms.txt` and the header menu; (3) re-add automatically when a listing has ≥1 product only after the D-07 gate has been run (no numeric threshold is invented here — D-07 leaves the minimum to implementation); (4) verify after AWS: 301 → 200 single hop, group-page canonical, noindex present, sitemap membership, no internal links to /by-desgin/.

## 6. Reversible defaults and review triggers

| Item | Default adopted | Review trigger | Evidence needed |
|---|---|---|---|
| Wedding-band hub vs /for-her duplicate | /for-her canonical → hub | Men's range confirmed (F-E3) | F-E3 |
| Thin-inventory assigned pages (bezel 2, toi et moi 1, anniversary 1, lariat 1, chain-link 1, pendant 3, T-bar 4) | Indexable with unique intro | 90 days post-cut-over | G-02 Queries/Pages |
| No-keyword populated pages (pavé, nature-inspired, multi-stone, toi-et-moi necklace) | Indexable, not promoted | 90 days post-cut-over (D-07 gate #1 unmet) | G-02 |
| Bangles category (label vs contents) | Interim title/meta/H1 scoped to 'link bracelets'; copy held; no keyword | HOD answers F-E7 | F-E7 |
| 'toi et moi ring', 'eternity ring/band' (DFS-informational) | Secondary on the commercial page | First GSC Queries read | G-02 / SERP check |
| Shape landing pages (round 22,200; oval 60,500) | Not created — shapes stay filters (D-08) | GSC shows query demand landing on filters | G-02 |
| FJ rings ('diamond ring' 110,000) | HELD, descriptive title | GSC Queries | G-02 |
| Lab-grown commercial hub | Not built | F-E2 = yes | F-E2 |
| Group page canonical → redirect | Canonical | Breadcrumbs repointed + no standalone demand | E-13, G-03 |
| Carat-variant PDP URLs | Keep | Post-cut-over review | G-01, E-09 |

## 7. What could not be fully resolved, and why

* **FJ rings (`/fine-jewellery/rings`)** — HELD: 'diamond ring' (110,000) spans engagement/wedding/fashion intent, the page lists 2 products and its only child is empty; no SERP evidence. Reversible default: descriptive non-bridal title.
* **Informational-labeled heads** ('toi et moi ring', 'eternity ring/band') — assigned as same-page secondaries; SERP type cannot be confirmed without GSC/SERP data.
* **Bangles page (`/fine-jewellery/bracelet/bangles`)** — the category label is 'Bangles' but both listed products are named link bracelets, and no product in the catalog is described as a bangle. Whether HOD sells or plans bangles, and whether the page should be kept, renamed or folded into `/chain-link`, cannot be inferred from the catalog. Resolution: interim copy scoped to 'link bracelets' (no bangle claim), copy HELD, status `CONDITIONAL — PRODUCT/OFFER CONFIRMATION`, one narrow question (F-E7). Product sets of `/bangles` (2), `/chain-link` (1) and `/tennis` (8) are disjoint.
* **Lab-grown hub** — decided (not built), but reverses on one HOD fact (F-E2).
* **Calendar annotation (done 2026-10-10)** — in `Keywords/content SEO/FINAL-BLOG-CALENDAR/BLOG_CALENDAR_FINAL.csv`, the single field `target_owner` of row `content_id = BLOG-WR-TYPES` was changed from 'Blog (Style & Trends)' to `EDU-WB-TYPES` with your explicit approval. Nothing else in the calendar changed (date, slot, title, primary keyword and every other field are untouched); this is separate from the finalized Step 2 specification.

## 8. Correction pass and close-out 2026-10-10

A targeted correction pass and close-out, not a new SEO stage; all 147 rows and all 19 dispositions are unchanged.

1. **Spelling defect (`jewelery`).** Root cause: the generator's US-spelling list replaced the prefix `jeweller` before `jewellery`, producing the misspelling `jewelery`, and its verb stems also turned `symbolism` into `symbolizm`. Fixed at source (`_build/s2_build.py`, `s2_write.py`): longest forms first, verb stems need an inflection suffix, hyphenated words (`ring-centered`, `near-colorless`) are normalized, URL/slug-like tokens are protected, and quoted current-site text is marked verbatim. A generated link-spec note that described anchor spelling as still awaiting OD-05 (22 link rows) was removed; OD-05 is adopted. Current-site text kept verbatim as evidence: the live About tile 'Certified Jewelery', current titles/metas/H1s, schema category values and URL slugs.
2. **Bangles category.** See §7 and F-E7: label vs contents contradiction resolved by scoped interim wording plus a held status.
3. **Bespoke timeline vs shipping facts.** See §9.
4. **BC-001 publication hold (close-out).** The approved package is protected and was **not** edited; only the status of its *future publication* changed. BC-001 moved from `READY FOR IMPLEMENTATION POST-AWS` to `HOD INPUT REQUIRED` (action `HOLD PUBLICATION (pending F-A1)`) because its approved meta, intro and article say '6–9 days of insured shipping' and insurance is unconfirmed (SR-02) — the questionnaire's rule is that unverified claims are not published. If HOD confirms insured shipping, the existing approved wording may proceed after the normal human review; if not, a separate, explicitly authorized content revision is required before publication.
5. **Calendar annotation (close-out).** Done with your approval: only `target_owner` of `BLOG-WR-TYPES` changed, to `EDU-WB-TYPES` (§7).
6. **Root `CLAUDE.md` and project memory** synchronized with the counts above.

## 9. Source reconciliation

| ID | Item | Authoritative source | Result | Action |
|---|---|---|---|---|
| SR-01 | Bespoke timeline start point ('from design approval') | `confirmed_business_facts.md` (user-supplied 2026-09-29) records '2–3 weeks to make + ~6–9 days delivery; generally ~3–4 weeks; depends on the stone selected' and does not name a start point. The project owner stated 'from design approval to delivery' in the 2026-10-10 Step 2A brief, and the approved BC-001 package uses the same bracket. | **Confirmed** — the whole timeline is treated as confirmed. HOD is not asked to repeat it. | Optional housekeeping for the user: add the start point to the protected facts file. |
| SR-02 | 'Insured' shipping wording | Not in the confirmed-facts file, which says only 'delivery'. The approved BC-001 package says '6–9 days of insured shipping'; the live header badge says 'Complimentary Insured Shipping'. | **Unconfirmed.** Insurance, carrier and signature terms belong to the broader shipping policy (F-A1). | BC-001 is protected and not modified, but its **publication is HELD** (status `HOD INPUT REQUIRED`) until F-A1 is answered. If shipments are insured: the approved wording may proceed after the normal human review. If not: a separate, explicitly authorized content revision is required before publication. The bespoke delivery fact itself is unaffected. |

The bespoke **timeline** (confirmed) and the **shipping policy** (regions, carriers, insurance, duties/taxes, free-shipping terms, holiday order-by dates — F-A1) are separate facts: the first is applied everywhere; the second stays removed/neutral until HOD answers.

## 10. Changes made by Step 2A/2B

Master CSV, link spec, PDP priority list and docs `02–09` regenerated from the updated sources (`_build/`); new files `10`, `10-COMMERCIAL-KEYWORD-ASSIGNMENTS.csv`, `11`, `12`, `13`. Root `CLAUDE.md` status/decision sections updated per its §17. Nothing else changed.

## Appendix — OD-01 assignment summary (64 assignment rows; full detail in the CSV)

Assignment states: NO KEYWORD BY DESIGN 17; ASSIGNED 17; NO KEYWORD — NO MEASURED DEMAND 17; ASSIGNED — INVENTORY WATCH 7; RESERVED — INACTIVE UNTIL POPULATED 3; HELD — AMBIGUOUS 1; HELD — TAXONOMY CONFIRMATION 1; NOT BUILT 1.

### Category hubs, bespoke and conditional hub

| Row | Primary | Vol/mo | KD | DFS label | Secondary / held | State | Conf. |
|---|---|---|---|---|---|---|---|
| COM-BESPOKE | custom engagement ring | 40,500 | 12 | transactional | design your own engagement ring (5,400/mo; KD 0; DFS transactional); bespoke engagement ring (1,300/mo; KD 18; DFS tran… | ASSIGNED | MEDIUM |
| COM-ER | engagement ring | 673,000 | 31 | transactional | engagement rings for women (110,000/mo; KD 52; DFS transactional); lab grown diamond engagement rings (90,500/mo; KD 19… | ASSIGNED | HIGH |
| COM-WB | diamond wedding bands | 18,100 | 0 | transactional | wedding bands for women (60,500/mo; KD 10; DFS transactional) [conditional] | ASSIGNED | MEDIUM |
| COM-FJ | — |  |  |  | — | NO KEYWORD — NO MEASURED DEMAND | MEDIUM |
| COM-FJ-EARRINGS | diamond earrings | 74,000 | 0 | transactional | earrings (246,000/mo; KD 25; DFS transactional) | ASSIGNED | HIGH |
| COM-FJ-NECKLACES | diamond necklace | 49,500 | 0 | transactional | necklace (201,000/mo; KD 15; DFS transactional) | ASSIGNED | HIGH |
| COM-FJ-BRACELETS | diamond bracelet | 27,100 | 0 | transactional | bracelet (201,000/mo; KD 27; DFS transactional) | ASSIGNED | HIGH |
| COM-FJ-RINGS | — |  |  |  | diamond ring (110,000/mo; KD 21; DFS transactional) [conditional] | HELD — AMBIGUOUS | LOW |
| COM-CURATED-TBAR | t bar necklace | 2,400 | 0 | transactional | — | ASSIGNED — INVENTORY WATCH | MEDIUM |
| COM-ER-STYLES-GROUP | — |  |  |  | — | NO KEYWORD BY DESIGN | HIGH |
| COM-LG-HUB | — |  |  |  | lab grown diamonds (135,000/mo; KD 38; DFS transactional) [conditional]; lab diamonds (27,100/mo; KD 41; DFS transactio… | NOT BUILT | MEDIUM |

### Subcategories

| Row | Primary | Vol/mo | KD | DFS label | Secondary / held | State | Conf. |
|---|---|---|---|---|---|---|---|
| /engagement-rings/by-design/side-stone-rings | side stones engagement rings | 1,000 | 0 | transactional | — | ASSIGNED | HIGH |
| /engagement-rings/by-design/solitare-rings | solitaire engagement rings for women | 12,100 | 0 | transactional | solitaire engagement ring (volume not measured in project datasets) | ASSIGNED | MEDIUM |
| /engagement-rings/by-design/halo-ring | halo engagement rings | 14,800 | 0 | transactional | — | ASSIGNED | MEDIUM |
| /engagement-rings/by-design/toi-moi-rings | toi et moi engagement ring | 6,600 | 0 | transactional | toi et moi ring (27,100/mo; KD 0; DFS informational) [conditional] | ASSIGNED — INVENTORY WATCH | MEDIUM |
| /engagement-rings/by-design/pave | — |  |  |  | — | NO KEYWORD — NO MEASURED DEMAND | MEDIUM |
| /engagement-rings/by-design/nature-inspired-rings | — |  |  |  | — | NO KEYWORD — NO MEASURED DEMAND | MEDIUM |
| /engagement-rings/by-design/three-stone-rings | three stone engagement ring | 9,900 | 0 | transactional | — | ASSIGNED | MEDIUM |
| /engagement-rings/by-design/bezel-rings | bezel engagement ring | 22,200 | 0 | transactional | — | ASSIGNED — INVENTORY WATCH | MEDIUM |
| /engagement-rings/round-rings | — |  |  |  | round engagement rings (22,200/mo; KD 0; DFS transactional) [conditional] | NO KEYWORD — NO MEASURED DEMAND | MEDIUM |
| /wedding-bands/for-her | — |  |  |  | wedding bands for women* (held on hub) | NO KEYWORD BY DESIGN | MEDIUM |
| /wedding-bands/for-him | — |  |  |  | — | NO KEYWORD — NO MEASURED DEMAND | MEDIUM |
| /wedding-bands/for-her/nature | — |  |  |  | — | NO KEYWORD — NO MEASURED DEMAND | MEDIUM |
| /wedding-bands/for-her/solid | — |  |  |  | — | NO KEYWORD — NO MEASURED DEMAND | MEDIUM |
| /wedding-bands/for-her/cigar-band | — |  |  |  | — | NO KEYWORD — NO MEASURED DEMAND | MEDIUM |
| /wedding-bands/for-her/eternity | eternity rings for women | 8,100 | 1 | transactional | eternity band (9,900/mo; KD 0; DFS informational) [conditional]; eternity ring (12,100/mo; KD 0; DFS informational) [co… | ASSIGNED | MEDIUM |
| /wedding-bands/for-her/anniversay | anniversary ring | 9,900 | 0 | transactional | — | ASSIGNED — INVENTORY WATCH | LOW |
| /wedding-bands/for-her/pavee | — |  |  |  | — | NO KEYWORD — NO MEASURED DEMAND | MEDIUM |
| /wedding-bands/for-him/classic | — |  |  |  | — | NO KEYWORD — NO MEASURED DEMAND | MEDIUM |
| /wedding-bands/for-him/diamonds | — |  |  |  | — | NO KEYWORD — NO MEASURED DEMAND | MEDIUM |
| /wedding-bands/for-him/designer | — |  |  |  | — | NO KEYWORD — NO MEASURED DEMAND | MEDIUM |
| /fine-jewellery/earrings/stud-earrings | diamond stud earrings | 49,500 | 0 | transactional | stud earrings (60,500/mo; KD 0; DFS transactional) | ASSIGNED | HIGH |
| /fine-jewellery/earrings/hoops-huggies | huggie earrings | 22,200 | 2 | transactional | diamond hoop earrings (12,100/mo; KD 0; DFS transactional) | ASSIGNED | MEDIUM |
| /fine-jewellery/earrings/drop-dangle | diamond drop earrings | 8,100 | 0 | transactional | dangle earrings (18,100/mo; KD 0; DFS transactional) | ASSIGNED | MEDIUM |
| /fine-jewellery/earrings/tennis-earrings | — |  |  |  | — | NO KEYWORD — NO MEASURED DEMAND | MEDIUM |
| /fine-jewellery/earrings/personalized-charm | — |  |  |  | personalized jewelry (too broad) | NO KEYWORD — NO MEASURED DEMAND | MEDIUM |
| /fine-jewellery/necklaces/solitare | diamond solitaire necklace | 4,400 | 0 | transactional | solitaire necklace (1,300/mo; KD 0; DFS transactional) | ASSIGNED | MEDIUM |
| /fine-jewellery/necklaces/pendant-necklace | diamond pendant necklace | 12,100 | 4 | transactional | diamond pendant (8,100/mo; KD 0; DFS transactional) | ASSIGNED — INVENTORY WATCH | MEDIUM |
| /fine-jewellery/necklaces/charm-necklace | charm necklace | 33,100 | 0 | transactional | — | ASSIGNED | MEDIUM |
| /fine-jewellery/necklaces/multi-stone | — |  |  |  | — | NO KEYWORD — NO MEASURED DEMAND | MEDIUM |
| /fine-jewellery/necklaces/lariat-necklace | lariat necklace | 18,100 | 0 | transactional | — | ASSIGNED — INVENTORY WATCH | MEDIUM |
| /fine-jewellery/necklaces/toi-et-moi | — |  |  |  | — | NO KEYWORD — NO MEASURED DEMAND | MEDIUM |
| /fine-jewellery/necklaces/tennis-necklace | tennis necklace | 33,100 | 0 | transactional | — | RESERVED — INACTIVE UNTIL POPULATED | MEDIUM |
| /fine-jewellery/necklaces/initials | initial necklace | 40,500 | 9 | transactional | — | RESERVED — INACTIVE UNTIL POPULATED | LOW |
| /fine-jewellery/bracelet/tennis | tennis bracelet | 135,000 | 0 | transactional | diamond tennis bracelet (90,500/mo; KD 0; DFS transactional) | ASSIGNED | MEDIUM |
| /fine-jewellery/bracelet/bangles | — |  |  |  | gold bangles (27,100/mo; KD 0; DFS transactional) | HELD — TAXONOMY CONFIRMATION | LOW |
| /fine-jewellery/bracelet/chain-link | chain bracelet | 8,100 | 0 | transactional | — | ASSIGNED — INVENTORY WATCH | LOW |
| /fine-jewellery/rings/eternity-rings | — |  |  |  | — | NO KEYWORD BY DESIGN | MEDIUM |
| /hiphop/chains | — |  |  |  | — | NO KEYWORD — NO MEASURED DEMAND | MEDIUM |
| /hiphop/chains/cuban-links | cuban link chain diamond | 720 | 0 | transactional | — | RESERVED — INACTIVE UNTIL POPULATED | LOW |
| /hiphop/test-subcat | — |  |  |  | — | NO KEYWORD BY DESIGN | MEDIUM |
