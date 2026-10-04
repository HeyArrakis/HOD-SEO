# Stage 16: Internal linking rules

Date: 2026-09-24. Scope: internal-link architecture only. Built from local project files (Stages 7, 8 and 10–15). **No DataForSEO or other API call, no live-site request, $0.00.** Nothing here changes a URL, slug, redirect, canonical, indexability decision or keyword owner.

Companion files:

| File | Contents |
|---|---|
| `16_internal_link_map.csv` | 390 source→target relationships, one row each |
| `16_page_link_requirements.csv` | 72 rows: 70 pages + 2 site templates |
| `16_anchor_strategy.csv` | 157 rows: anchor guidance per target page and anchor type |
| `16_orphan_and_connectivity.csv` | 70 pages: current connectivity status and the fix required |
| `scripts/build_16.py`, `scripts/qc_16.py` | Build script and QC script (69 checks) |

**Source of truth.** Keyword→URL ownership comes from Stage 15 (`15_keyword_url_map.csv`, `15_target_page_registry.csv`). The hierarchy comes from Stage 14 (`14_education_hierarchy.csv`) and Stage 12 (`12_ia_proposed_structure.csv`). Stage 16 reinforces those decisions. It never creates or moves an owner.

---

## 1. Architecture in one picture

```
                         TPL-HEADER (every page)                  TPL-FOOTER (every page)
      Engagement Rings · Wedding Bands · Fine Jewellery ·        FAQ · Policies · About ·
      Earrings · Necklaces · Bracelets · Bespoke ·               Contact · Ring Size Guide
      Education · Journal · [Lab-Grown Diamonds: CONDITIONAL]
                    │                                   │
       COMMERCIAL TREE                               EDUCATION TREE                         BLOG
  COM-ER ─┬─ COM-ER-SIDESTONE ─┐               EDU-ROOT ─┬─ Lab-Grown pillar (LG-00) ─ LG-01…10     BLOG-HUB
          ├─ [styles: COND]    │                         ├─ Natural pillar (NAT-00)                    ├─ Craft & Making
          └─ PDPs ◄────────────┘                         ├─ 4Cs pillar (4C-00) ─ 4C-01…07              ├─ Style & Trends
  COM-WB ─── [gender: COND] ─ PDPs                       ├─ Shapes pillar (SHP-00)                     ├─ Gifts & Occasions
  COM-FJ ─┬─ Earrings / Necklaces / Bracelets ─ PDPs     ├─ Certification pillar (CERT-00) ─ CERT-01   ├─ Collections & Launches
          └─ [Rings, types, T-Bar: COND]                 ├─ Metals pillar (MET-00) ─ MET-01            ├─ [Stories: COND]
  COM-BESPOKE                                            ├─ Ring & Jewellery Guides index ─ RJG-01/02  └─ Industry Notes
  [COM-LG-HUB: COND]                                     ├─ Diamond properties (GEN-01, root level)
                                                         └─ [Gemstones & Alternatives: COND]

  Education ──(decision point: 1–3 links)──► Category / subcategory ──► PDP
  Category  ──(max 5 Education links)──────► the Education owner of the buyer's question
  PDP       ──(max 3 Education links)──────► ring size · grades · [certificate / karat: COND]
  Blog      ──► Education owner of any concept it mentions · category / product it features
  FAQ       ──► Education owner (one-line answer + link) · policies · contact
```

Link types used (brief §6): GLOBAL_NAV, PRIMARY_NAV, CATEGORY_NAV, BREADCRUMB and FOOTER are **structural**. CONTEXTUAL, RELATED_CONTENT, EDITORIAL, EDUCATIONAL_CTA, COMMERCIAL_CTA and PRODUCT_RECOMMENDATION are **contextual**, and every contextual row records a `context_reason`.

Priority and launch:

| priority | required_at_launch | Meaning |
|---|---|---|
| REQUIRED | YES | Ships with the later of the two pages to go live. A proposed page does not launch without its REQUIRED incoming links. |
| RECOMMENDED | NO | Add at launch where practical, or in the first content update. |
| OPTIONAL | NO | Use only where it reads naturally. It may be skipped. |
| CONDITIONAL | CONDITIONAL | Add only when a named business fact or page condition is met. |

Counts: 153 REQUIRED, 79 RECOMMENDED, 42 OPTIONAL, 116 CONDITIONAL.

## 2. Page-type rules

| Source → target | Rule | Rows |
|---|---|---|
| Education hub pillar → child | Hub topic list: REQUIRED. Also add a contextual body link where the pillar mentions the child's subject. | HUB_TO_CHILD 46 |
| Education child → hub | Breadcrumb to its Stage 14 parent: REQUIRED. The Education-owned `/blog` URLs carry the Education breadcrumb too (Stage 13 §6). | CHILD_TO_HUB (Education) |
| Child → related child | Only named Stage 14 neighbours: clarity↔grade explainers, authenticity↔comparison, and so on. Not every sibling. | CHILD_TO_RELATED_CHILD 38 |
| Education → other hub | Only where the other hub owns a term the page uses: cut grade ↔ shapes, colour ↔ metals, formation ↔ lab-grown process. | EDUCATION_CROSS_HUB 43 |
| Education → category | 1–3 links at the decision point: buying guides, comparisons, shape, metal, settings, sizing. None from pure science pages (GEN-01), none from Natural and none from Gemstones. | EDUCATION_TO_CATEGORY 24 |
| Education → product | Only as an illustrative example, and only while the product is live. One row: Shapes → the oval PDP. | EDUCATION_TO_PRODUCT 1 |
| Category → subcategory / product | Tiles and product grid: REQUIRED. Conditional styles, types and gender splits link only while populated (Stage 12 P-EMPTY). | 16 + 15 |
| Category → Education | The one or two guides that answer the buyer's main question, plus ring size where rings are sold. Maximum 5 non-conditional Education links per category page. | CATEGORY_TO_EDUCATION 20 |
| Product → category | Breadcrumb to the primary category and, for side-stone designs, to the side-stone subcategory. | PRODUCT_TO_CATEGORY 9 |
| Product → Education | Maximum 3 per PDP: ring size (ring and band PDPs), grades (PDPs that list grades), and certificate or karat only if CONDITIONAL facts are confirmed. | PRODUCT_TO_EDUCATION 7 |
| Blog → Education / category / product | Required whenever a post mentions an Education-owned concept or features a product family. Live products only. | 17 / 15 / 4 |
| Blog → Blog | Only where a story continues (craft ↔ commission, launch → making-of). | 3 |
| FAQ → Education / category | One-line answer + link to the owner named in D14-30. The FAQ never carries the full treatment. | 6 / 2 |

## 3. Education ↔ commercial rules

1. **Education links to commerce only at a decision point.** Buying guides, comparisons, shapes, metals, settings and sizing link to the matching category. Definitional and science pages do not, apart from an optional single exit.
2. **Commerce links to Education only when the buyer needs an explanation.** Category copy gets a short sentence and a link. It must not re-explain the concept (Stage 12 D-06). Engagement Rings links to Shapes, 4Cs and Ring Size (required), Lab-vs-natural (recommended) and How to Choose (optional).
3. **The lab-grown commercial head term never goes to Education.** `lab grown diamonds` (135,000) and `lab diamonds` (27,100) are held for the CONDITIONAL commercial Lab-Grown hub (COM-LG-HUB, Stage 12 D-05, Stage 15). Only COM-LG-HUB may take the bare anchor "Lab-Grown Diamonds".
   - Until the hub exists, the Education pillar's commercial exit goes to Engagement Rings with a descriptive anchor ("browse our engagement rings").
   - **Exception recorded here:** the Education hub's breadcrumb and nav label should read "Lab-Grown Diamond Guide", not the bare hub name. This is anchor text only; the D14-02 hub name is unchanged.
4. **Natural is Education-only.** EDU-NAT-00 links to lab-vs-natural, diamond properties and the lab-grown pillar. It sends **no commercial link**, because the natural commercial hub is deferred. For the same reason as rule 3, its label is "Natural Diamond Guide", not "Natural Diamonds".
5. **Certification.** The pillar (EDU-CERT-00) and GIA vs IGI (EDU-CERT-01) link to each other and ship together (Stage 13). No IGI-only page exists, so no anchor presents IGI as a standalone topic. A commercial link from certification pages is CONDITIONAL on confirming which products ship with grading reports.
6. **Shapes.** One pillar and no per-shape pages. Shape names are never linked to shape filter URLs, and cut-grade anchors go to EDU-4C-06 (D14-02 split).
7. **Metals.** The metals pillar and 14k vs 18k link to Engagement Rings and Wedding Bands. The validated band keywords are metal questions (CL-113). Karat links from PDPs are CONDITIONAL on karat options being offered.
8. **Gemstones & Alternatives** is a CONDITIONAL hub. All of its rows are CONDITIONAL, and it sends no commercial link, because HOD selling moissanite or gemstones is unconfirmed.

## 4. Blog rules

- Blog templates cover the six Stage 13 editorial categories: Craft, Style, Gifts, Launches, Stories (CONDITIONAL) and Industry Notes. There are **no Blog posts today**. These are launch requirements for future posts, not links on existing pages.
- A post that mentions an Education concept links to the **single Education owner**, never to another Blog post for that concept.
- Gift guides link to categories, not long product lists. Launch posts link to the live pieces **and** to the category page, which stays the page meant to rank.
- The Blog never receives an anchor that is an Education-owned keyword (QC 09).
- Education → Blog links are optional or CONDITIONAL only: first-hand craft evidence, never REQUIRED.
- **Transitional listing.** The Blog hub lists all 10 current articles (Stage 10). For the 9 Education-owned ones the listing is CONDITIONAL: keep it until the Education path to the article is live, then removing it is a UX choice (Stage 13 §14 Q2). **Never remove it before the replacement path exists.** The deferred online-ring article keeps a REQUIRED Blog-hub listing, because it has no Education destination yet.

## 5. Product and category rules

- Categories link to their subcategories and to products through grids. Conditional subcategories are linked only while populated. **Stage 16 does not decide indexability.**
- Link style URLs directly, never the `/by-desgin/` grouping page (Stage 12 P-DEPTH).
- PDP URLs stay flat. The category relationship is carried by breadcrumb (Stage 12 D-11).
- PDP → Education links are template UI labels ("Find your ring size", "What do these diamond grades mean?"), classed NAVIGATIONAL. They are never keyword strings, because they repeat on every PDP.
- Related-products modules link PDP → other PDPs. This is the only template-level self-relationship, and a product never links to itself.

## 6. Anchor-text rules

1. **Default to DESCRIPTIVE or NATURAL_LANGUAGE.** Of the 390 rows: 183 are NAVIGATIONAL, 106 DESCRIPTIVE, 68 NATURAL_LANGUAGE, 17 BRANDED, 12 PARTIAL_MATCH and **4 EXACT_MATCH_ALLOWED**.
2. **Exact match: at most one source per target.** The source is the parent pillar or the most closely related page, and the link sits in body copy, never in nav, footer, breadcrumb or template modules. The 4 exact-match anchors are:

   | Source | Target | Anchor |
   |---|---|---|
   | LG-00 | LG-02 | "lab-grown vs natural diamonds" |
   | LG-00 | LG-03 | "HPHT vs CVD" |
   | LG-00 | LG-01 | "are lab-grown diamonds real" |
   | LG-00 | LG-10 | "how to choose a lab-grown diamond" |

   Each is a keyword the target already owns in Stage 15 (QC 10).
3. **No anchor may equal a keyword that Stage 15 assigns or holds for a different page** (QC 10 tests every anchor and variant). This is how internal links avoid creating a second owner.
4. **No target receives the same contextual anchor from more than two sources** (QC 15). The lab-vs-natural comparison, for example, gets 13 contextual links with 13 different anchors.
5. **Anchors must describe the target accurately.** No "lab-grown engagement rings" to Engagement Rings, because that landing page is deferred and the anchor would imply it. No "customise this design", because product-level customisation is unconfirmed.
6. `16_anchor_strategy.csv` gives, per target, the anchors in use by type, where each is used, and an **avoid list** naming the other page that owns each avoided phrase.

## 7. Ranking-equity protection

All 28 Stage 3 ranking keywords sit on 6 URLs. **Every link to these pages uses the current ranking URL, and no link recommends a move, redirect or slug change** (QC 05). Where Stage 13 allows a future move, internal links are updated in the same release as the 1:1 301 (Stage 13 condition). That is not triggered here.

| Protected URL (page ID) | Stage 3 kw | Contextual sources (priority) | Anchor concepts | Must NOT use the ranking keyword as anchor |
|---|---|---|---|---|
| CVD vs HPHT `/blog/cvd-vs-hpht-…` (EDU-LG-03) | 19 (18 targeted; `cvd/hpht diamond tester` excluded) | LG-00 (REQ, exact "HPHT vs CVD"), LG-01 (REQ), LG-10 (REQ), LG-02 (REC), BLOG-INDUSTRY (REC), LG-08/LG-09 (OPT), LG-04 (COND) | growth methods; how CVD/HPHT are grown; "does it matter?" | Commercial pages and templates (no CVD/HPHT anchors from categories or PDPs). **No page anywhere** uses "cvd/hpht diamond tester". LG-01 must not carry an "are CVD diamonds real" section. The LG-00 pillar carries a one-paragraph mention only. |
| Lab-grown vs natural `/blog/lab-grown-vs-natural-…` (EDU-LG-02) | 3 | LG-00 (REQ, exact), LG-01 (REQ), LG-05 (REQ), NAT-00 (REQ), FAQ (REQ), COM-ER (REC), LG-07/LG-10/BLOG-INDUSTRY (REC), Homepage/LG-03 (OPT), COM-LG-HUB/LG-06 (COND) | how they differ/compare; worth it compared with natural; full comparison | Homepage hero and FAQ must not host the comparison (one line + link). EDU-LG-01 must not use comparison wording as its own heading. |
| 14k vs 18k `/blog/14k-vs-18k-…` (EDU-MET-01) | 3 | MET-00 (REQ, once it launches), COM-WB (REC), online-ring article (REC), PDP (COND: karat options) | 14k or 18k for your band; choosing between 14k and 18k | PDP template must not use "14k vs 18k gold" sitewide. MET-00 keeps general metal choice (avoid list). |
| How to choose a lab-grown diamond `/blog/how-to-choose-…` (EDU-LG-10) | 1 | LG-00 (REQ, exact), 4C-00 (REQ), LG-02/LG-03/CERT-00/CERT-01/online-ring article (REC), COM-ER (OPT) | using the 4Cs / a certificate to choose; step by step | The online-ring article must not use "how to choose a lab-grown diamond" (unresolved D-19 boundary). No "lab-grown engagement ring" anchors. |
| Side-stone `/engagement-rings/by-desgin/side-stone-rings` (COM-ER-SIDESTONE) | 1 | RJG-01 settings guide (REQ, partial "side-stone engagement rings"), BLOG-STYLE (OPT) + structural: COM-ER tile, header mega-menu, PDP breadcrumbs | side-stone engagement rings / designs | EDU-RJG-01 must not target the style shopping query. Never link the `/by-desgin/` grouping page. |
| Oval floral ring `/shop/oval-floral-diamond-ring` (COM-PDP-OVAL-FLORAL) | 1 | EDU-SHP-00 oval section (REC, while live), related-products (OPT) + grids in COM-ER, COM-ER-SIDESTONE and COM-SHOP | product name; "an oval centre stone with marquise side stones" | Education pages never use "marquise oval diamond" (the PDP's PRODUCT-SERP query; CL-063 is excluded from Education). |

Every protected URL has at least 2 non-conditional contextual recommendations, at least one of them REQUIRED or RECOMMENDED (QC 16).

## 8. Orphan and connectivity rules

- **Current status** (existing pages) uses only observed facts: sitemap membership, the Stage 10 nav check, and the Blog/Education hub listings. **The project has no crawl or internal-link-count data** (Stage 10 §9), so no page is labelled from a count that does not exist.
- **TRUE_ORPHAN: 0 confirmed.** Every in-scope existing page is reachable through the sitemap, navigation or a hub listing. Out-of-scope pages (test product, `/hiphop`, `/collection`) are not assessed.
- **WEAKLY_CONNECTED: 13.**
  - The 9 Education-owned `/blog` articles. They are reachable only from the Blog hub listing and are not on `/education`.
  - The GIA-vs-IGI article, which is the only item on `/education`.
  - The deferred online-ring article.
  - `/education` and `/blog`, whose nav placement is not recorded.
- **NAV_ONLY: 20.** Categories, the side-stone subcategory, other subcategories, the PDP set, the oval PDP, Bespoke, and support/brand pages. Each is reachable by nav or grid with no recorded contextual support.
- **WELL_CONNECTED: 1** (homepage).
- **Proposed and conditional pages** are never called orphans. Each carries `LINKING_REQUIREMENT_AT_LAUNCH` (36 pages: 16 proposed, 5 Blog templates, 15 conditional). A proposed page launches only with its REQUIRED incoming links, which are marked `LAUNCH_BLOCKER_IF_MISSING`.
- **Planned connectivity bar**, tested by QC X2:

  | Page kind | Bar |
  |---|---|
  | Articles | At least 1 structural and at least 2 REQUIRED/RECOMMENDED contextual incoming links |
  | Commercial / Blog pages | At least 1 structural and at least 1 contextual incoming link |
  | Hubs | At least 2 structural incoming links |
  | Homepage / Shop All | Navigation only |

  Every non-conditional page meets its bar. **One documented exception:** the deferred online-ring article. It keeps its Blog listing but is deliberately not boosted while its boundary with the lab-grown buying guide is unresolved (OV-06, D-19).
- **Transitional paths.** Until each Education hub launches, `/education` lists the Education-owned articles whose parent hub does not yet exist: LG-01, LG-02, LG-03, LG-10, MET-01, RJG-02 and CERT-01. These are CONDITIONAL rows that are replaced by the hub listing at launch.

## 9. Overlinking rules

| Page type | Structural | Contextual cap (non-conditional) |
|---|---|---|
| Category / subcategory | nav, tiles, grid | ≤ 5 Education links; 1 Bespoke CTA |
| PDP | breadcrumb, related products | ≤ 3 Education links, as template UI labels |
| Education article | breadcrumb, hub list | ≤ 10 contextual outgoing links; 1–3 commercial exits |
| FAQ | footer | one link per answer, to the named owner |
| Blog post | breadcrumb | concept owner(s) + featured category/product only |

**Counterproductive links. Do not add these:**

| Link | Why it is harmful |
|---|---|
| Any page → EDU-LG-00 with anchor "lab-grown diamonds" / "lab diamonds" | Pulls the commercial head term to an informational page (blurs the D-05 ownership) |
| Any page → EDU-NAT-00 with anchor "natural diamonds" | Same, for the deferred natural commercial hub |
| EDU-LG-00 pillar with its own CVD or HPHT sections, each linking to LG-03 | Makes the pillar look like a second CVD/HPHT page (Stage 15 HIGH pair) |
| EDU-LG-01 → LG-08 with "do lab-grown diamonds look real" | Appearance query owned by LG-08; wording makes LG-01 look like the owner |
| Shapes pillar → shape filter URLs (e.g. oval engagement rings) | Per-shape landing pages are deferred; filter states are not SEO URLs (D-07) |
| Cut-grade anchors → Shapes pillar, or shape anchors → cut guide | Blurs the D14-02 cut/shape split |
| Any page → IGI-only topic, or "IGI report explained" anchors → CERT-00 | Creates the IGI-only owner Stage 14 deferred |
| Education → moissanite/gemstone shopping | HOD selling these is unconfirmed |
| Category/PDP → the `/by-desgin/` grouping page | Grouping-only segment with no search meaning (P-DEPTH) |
| PDP template → "14k vs 18k gold" exact anchor on every product | Sitewide exact-match repetition |
| Two-way "see also" loops between every sibling Education page | Circular navigation with no user value; only named neighbours link |
| Removing the Blog-hub listing of an Education-owned article before an Education path exists | Creates an orphan out of a ranking URL |
| Launch post or gift guide → product list instead of category | Launch posts never replace category pages (Stage 13 rule 7) |

## 10. Cannibalization safeguards

- No keyword is assigned by Stage 16. The link map has no keyword column, and anchors are checked against Stage 15 ownership (QC 03, QC 10).
- **All 12 Stage 15 adjacent-intent pairs** plus the D14-27 register pairs are flagged on every row between them, with a guard sentence in `notes`. There are 39 such rows: 4 HIGH, 23 MEDIUM, 10 LOW and 2 INSUFFICIENT_EVIDENCE.
- The two HIGH pairs are:
  - LG-00 ↔ LG-03: the pillar keeps a one-paragraph mention of growth methods and links out.
  - LG-03 ↔ LG-04 (conditional): the process page, if created, must not target method queries.
- **New conflicts created by Stage 16: none.** No anchor equals a keyword owned or held by another page, no source uses one anchor for two targets, and no Education page receives a commercial CTA.

## 11. Launch vs post-launch

- **At launch of the rebuilt site:**
  - all REQUIRED structural rows (header, footer, breadcrumbs, hub lists, category tiles and grids)
  - REQUIRED contextual rows between pages that both exist
  - the CONDITIONAL transitional rows (`/education` and Blog-hub listings for Education-owned `/blog` articles)
- **At launch of each proposed page:** its REQUIRED incoming and outgoing rows ship in the same release (`LAUNCH_BLOCKER_IF_MISSING`).
- **Post-launch:** RECOMMENDED rows in the first content update, then OPTIONAL rows where they read naturally.
- **Only when the condition is met:** CONDITIONAL rows. These cover:
  - commercial Lab-Grown hub
  - conditional Education topics
  - Gemstones hub
  - style, type and gender subcategories
  - certificate and karat facts
  - craft posts and client stories

## 12. Exceptions

1. The Education hub labels "Lab-Grown Diamond Guide" and "Natural Diamond Guide" replace the bare hub names in anchors and breadcrumbs (§3). This is anchor text only. **Needs user sign-off**, because D14-02 fixed the hub names.
2. The Education-owned `/blog` URLs carry the Education breadcrumb and hub listing before any move (Stage 13 §6 transitional state).
3. The deferred online-ring article is intentionally left weakly connected (§8).
4. The PDP template self-relationship (related products) is the only self-row. It is justified and flagged.
5. The side-stone style keeps its nav link under the live `/by-desgin/` path. The path itself is not changed by Stage 16.

## 13. Unresolved items (not decided here)

- **Commercial Lab-Grown hub** (D-05): approval and inventory confirmation. 12 CONDITIONAL rows depend on it.
- **Grading reports per product.** Do HOD pieces ship with IGI/GIA reports? This gates PDP → certification and certification → category links.
- **Karat options per product.** Does HOD offer both 14k and 18k? This gates PDP → 14k vs 18k links.
- **Natural diamonds, moissanite, gemstones, loose stones, wholesale** (Stage 12 business questions). These gate the natural and gemstone conditional rows. No commercial links are proposed for them.
- **Populated style, type and gender subcategories.** Which stay live is a merchandising and D-07 decision.
- **D-19 commercial keyword supplement (unapproved).** This gates the online-ring article's role and any engagement-ring buying guide.
- **D-15 jewellery/jewelry spelling.** Affects nav labels and the RJG/Metals hub slugs (URL_PENDING).
- **Blog editorial capacity.** Craft and story posts must exist before Blog → Bespoke/About links go live.
- **Crawl data.** A post-launch crawl is needed to replace the current-state statuses with measured link counts.
