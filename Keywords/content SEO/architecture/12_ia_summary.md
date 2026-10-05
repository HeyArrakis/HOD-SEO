# Stage 12 — SEO Information Architecture: Summary

Date: 2026-09-24. Status: **COMPLETE**.

**Scope.** This stage sets the structural IA. It does not assign keywords to URLs (Stage 15), set blog strategy (Stage 13) or build the detailed Education architecture (Stage 14). It recommends no redirects, canonicals, robots, sitemap or site changes.

**DataForSEO spend this stage: $0.00.** No paid or free DataForSEO call was made. Cumulative spend is unchanged at **$0.33536**.

**Files**

| File | Contents |
|---|---|
| `12_ia_proposed_structure.csv` | 52 rows |
| `12_page_type_framework.csv` | 31 page types |
| `12_current_vs_proposed_ia.csv` | 25 rows |
| `12_ia_decision_log.md` | Decisions D-01 to D-19 |
| `scripts/build_12_csvs.py` | Regenerates the CSVs |
| `scripts/qc_12.py` | QC checks |

**Labels.** Every statement is marked as one of four things:
- **OBSERVED FACT**: taken directly from a project file.
- **INFERENCE**: a conclusion drawn from the facts.
- **PROPOSED ARCHITECTURE**: a design choice for the future site, not a description of the current one.
- **INSUFFICIENT EVIDENCE — DEFER**: the data cannot support a decision yet.

---

## 1. Executive summary

- **The informational side of the IA is well evidenced. The commercial side is not.**
  - OBSERVED FACT [STAGE 11]: 51 of 89 clusters are informational. The keyword universe has almost no commercial category queries:
    - 0 lab-grown × engagement-ring keywords
    - 0 shape × jewellery-type keywords
    - no wedding-band, necklace, bracelet, fine-jewellery or bespoke shopping terms
  - Commercial structure therefore rests on the catalogue, the live structure, a handful of commercial SERPs and business context.
  - Missing keywords are never treated as missing demand.
- **Proposed L1 sections:**
  - Engagement Rings
  - Wedding Bands
  - Fine Jewellery (umbrella for Earrings, Necklaces & Pendants, Bracelets and Rings)
  - Bespoke
  - Lab-Grown Diamonds (a commercial hub, *conditional*)
  - Education (evergreen) and Blog (editorial), grouped under "Resources"
  - Brand & Support
  - Natural Diamonds as a commercial hub is deferred, because it is unknown whether HOD sells natural pieces.
- **Commercial and informational pages are separate systems.**
  - Diamond concepts belong in Education: lab-grown science, CVD/HPHT, 4Cs, shapes, cuts and certification.
  - Commercial pages link into Education rather than hosting that content.
  - Lab-grown is the one entity where Google shows both a commercial SERP (head term) and informational SERPs (everything else). It therefore gets two page types.
- **Filters are filters by default.**
  - A filter or subcategory becomes an indexable page only through a seven-condition gate: demand, SERP type, inventory, distinctness, one home, business fit, and stability (D-07).
  - One subcategory passes today: engagement-ring **side-stone**, backed by a Stage 3 ranking and a CATEGORY SERP.
- **The biggest structural problems today:**
  - 41 live subcategories are not in the sitemap, and 13 of them are empty.
  - Several slugs are misspelled.
  - There is a grouping-only `/by-desgin/` segment.
  - Placeholder and test pages are live.
  - Carat variants are separate URLs named with CMS IDs.
  - Blog and Education have no distinction and overlap on certification.
  - The lab-grown head term has no commercial page.
- **The next research need is a targeted commercial keyword and SERP supplement before Stage 15 (D-19).** It is not run here and needs approval.

---

## 2. Current IA findings (OBSERVED FACT)

| Area | What exists today | Source |
|---|---|---|
| Sitemap | 198 URLs: 169 PDPs, 10 blog, 1 education, 5 categories (incl. /t-bar, /hiphop), 2 listings, core/utility | [STAGE 1] |
| Hidden layer | 41 live nav subcategories not in sitemap (9 ER, 11 WB, 21 fine jewellery); 13 empty | [STAGE 10] |
| Engagement rings | `/engagement-rings/by-desgin/{9 styles}`; only side-stone ranks (pos 104) | [STAGE 3], [STAGE 10] |
| Wedding bands | `/wedding-bands/for-her/*` (2 of 7 children populated), `/for-him/*` (all empty) | [STAGE 10] |
| Fine jewellery | `/fine-jewellery/{earrings, necklaces, bracelet, rings}/*`; singular "bracelet" | [STAGE 10] |
| Listings | `/shop` (all products), `/collection` (empty filtered view) | [STAGE 1] |
| Placeholders/tests | `/hiphop` "Coming Soon" + "TEST SUBCAT"; `/shop/fine-jewellery-test-product` | [STAGE 1] |
| PDPs | Flat `/shop/<slug>`; 3 `-copy-<id>` and 10 numeric-ID slugs; carat variants as URLs | [STAGE 1] |
| Content | 10 blog + 1 education article; no intent/format distinction; OV-01 CLEAR_OVERLAP (certification) | [STAGE 10] |
| Equity | 28 rankings on 6 URLs, all position ≥27; 26 on 4 blog articles; HOD in 0/795 top-10 results | [STAGE 3], [STAGE 9], [STAGE 10] |
| Templates | Boilerplate category meta descriptions; no H1 on /about, /faq, /hiphop | [STAGE 1] |

---

## 3. Proposed top-level architecture (PROPOSED ARCHITECTURE)

```
Home
├── Engagement Rings ........................ L1 category hub
│   ├── Side-Stone .......................... L2 style (confirmed)
│   ├── Solitaire / Halo / Pavé / Three-Stone / Bezel / Toi-et-Moi / Nature-Inspired
│   │                                         L2 styles (conditional, gate D-07)
│   └── [filters: shape*, origin*, metal, carat, price]   *landing pages deferred
├── Wedding Bands ........................... L1 category hub
│   ├── Women's / Men's ..................... L2 (conditional; men's currently empty)
│   └── [band styles: deferred]
├── Fine Jewellery .......................... L1 umbrella (label/spelling deferred, D-15)
│   ├── Earrings ............................ L2 (Studs, Hoops & Huggies, Drop & Dangle: L3 conditional)
│   ├── Necklaces & Pendants ................ L2 (type L3s conditional; T-Bar placement deferred)
│   ├── Bracelets ........................... L2 (Tennis, Bangles, Chain & Link: L3 conditional)
│   └── Rings (non-bridal) .................. L2 scope deferred
├── Lab-Grown Diamonds ...................... L1 commercial origin hub (conditional, D-05)
│   └── [loose/carat pages: deferred; only if loose stones are sold]
├── Natural Diamonds ........................ deferred (catalogue unknown)
├── Bespoke / Custom ........................ L1 service page (sub-pages deferred)
├── Shop All ................................ all-products listing; PDPs at /shop/<slug> (flat)
├── Resources (navigation grouping)
│   ├── Education ........................... L1 evergreen hub (topic hubs: Stage 14)
│   └── Blog / Journal ...................... L1 editorial/brand system (strategy: Stage 13)
└── Brand & Support: About · Contact · FAQ · Shipping · Returns · Privacy · Terms
Non-indexable: search · account · cart · checkout · wishlist · filter/sort/pagination states · test URLs
```

The tree shows the **logical** hierarchy and navigation. Nav placement is separate from URL depth; for example, Earrings can appear in the top menu while its URL nests under Fine Jewellery. How the paths are expressed depends on the platform (D-17).

---

## 4. Commercial hierarchy

| Family | Parent | Subcategory level | Filter level | Indexable now | Conditional | Not indexable |
|---|---|---|---|---|---|---|
| Engagement Rings | Home | Style (L2) | Shape, origin, metal, carat, price | Hub; Side-Stone | Other 7 styles; shape and origin landing pages (deferred) | Metal/carat/price states; multi-facet combinations |
| Wedding Bands | Home | Gender (L2) → style (L3) | Metal, width, stone | Hub | Women's/Men's (if populated); band styles (deferred) | Empty branches; style × gender combinations by default |
| Fine Jewellery | Home | Product type (L2) → type (L3) | Shape, metal, origin, price | Umbrella; Earrings; Necklaces & Pendants; Bracelets | L3 types (studs, hoops, tennis…); Rings scope | Empty L3s (tennis earrings, initials…); thin 1–2 product L3s until gated |
| Bespoke | Home | Service sub-pages | — | Service page | Sub-pages (deferred) | — |
| Lab-Grown Diamonds | Home | Loose/carat (only if sold) | Shape, carat | — | Hub (conditional); loose pages (deferred) | — |

---

## 5. Diamond, lab-grown and natural conceptual hierarchy

Each concept has one commercial role and one informational role. They are not merged.

| Concept | Commercial role | Informational home | Evidence |
|---|---|---|---|
| Lab-grown (head term) | **Commercial hub** (conditional) | Education > Lab-Grown | [STAGE 8] retailer collection SERPs for *lab grown diamonds* / *lab diamonds*; [STAGE 11] CL-001 vs CL-002 DISTINCT_INTENT |
| Natural (head term) | Commercial hub, deferred | Education > Natural | [STAGE 8] retailer SERPs; [STAGE 1] no natural PDPs observed |
| CVD / HPHT | None (possibly a PDP attribute) | Education > Lab-Grown (comparison) | [STAGE 8] EDITORIAL_GUIDE; [STAGE 3] 18 of 28 rankings |
| Lab-grown vs natural | None | Education comparison guide | [STAGE 8] COMPARISON SERP |
| Quality / 4Cs | Filters (colour/clarity only if loose stones are sold) | Education > Quality | [STAGE 11] 12 clusters, informational |
| Shapes | Filter (landing pages deferred) | Education > Shapes & Cuts | [STAGE 8] *diamond shape* EDITORIAL_GUIDE |
| Cuts | None | Education > Shapes & Cuts / Quality | [STAGE 11] CL-050 |
| Certification | Trust signal on PDPs | Education > Certification | [STAGE 11] CL-030 to CL-034; [STAGE 10] OV-01 |

---

## 6. Informational architecture framework

- **Education is the single evergreen home (D-09).** The existing `/education` path is kept.
- At concept level, its topic hubs are:
  - Lab-Grown Diamonds
  - Natural Diamonds
  - Diamond Quality (4Cs)
  - Shapes & Cuts
  - Certification
  - Metals & Materials
  - Gemstones & Diamond Alternatives (scope depends on business relevance)
  - Ring & Jewellery Guides (settings, sizing, care)
  - Buying Guides
- Comparison guides sit inside their topic hub.
- **Relationship to commerce:**
  - Education pages link down to the relevant category, filter or product views.
  - Category pages link up to the one guide that answers the buyer's main question.
  - Buying guides act as the bridge between the two.
- **Evidence:**
  - [STAGE 8]: PAA on 98% and AI Overview on 78% of SERPs.
  - [STAGE 9]: competitors rank from `/education/`, `/guides/` and `/diamond-education/` paths.
- The topic-hub list is **not final**. Stage 14 sets the hubs, articles and depth.

---

## 7. Blog / Education relationship

1. **Should Blog exist as a distinct system?** Yes, with a different job (D-10). Blog covers time-bound editorial and brand content. Education covers evergreen reference and decision content.
2. **How does it relate to Education?** An evergreen subject has one home, in Education. Blog posts link to Education and to categories. They do not re-explain Education topics.
3. **Main navigation or Resources?** Blog goes under a Resources grouping together with Education. It is not a primary commercial navigation item.
4. **What prevents the overlap from returning?**
   - Separate the two by *role* (evergreen vs time-bound), not by topic.
   - Keep a rule that one evergreen topic has one home.
   - Stop using the same title/slug pattern for both.
   - OV-01 (certification in both sections) is the case this rule prevents.

**Migration caveat.** 26 of HOD's 28 rankings sit on blog articles that are evergreen by this definition. Moving them is a Stage 13 decision that needs migration reasoning. It is not decided here.

---

## 8. Page-type framework

The full list is in `12_page_type_framework.csv` (31 types). In brief:

| Group | Page types | Indexable by default | Permanent URL |
|---|---|---|---|
| Commercial | Homepage, Category hub, Category, Shop-all listing, PDP, Bespoke service | Yes | Yes |
| Commercial, gated | Subcategory, Origin hub, Facet landing page, Curated collection | Conditional | Once gated |
| Commercial, never | Filter state, Variant state, Pagination | No | No |
| Informational | Education hub, Topic hub, Education article, Buying guide, Comparison guide, Certification guide, Shape guide, Blog hub, Blog article | Yes | Yes |
| Informational, conditional | Tool page (ring sizer), Author/expert profile | Conditional | Conditional |
| Brand/support | About, Contact, FAQ, Policies | Yes | Yes |
| Utility | Search, Account/Cart/Checkout/Wishlist, Blog taxonomy archives | No | No |
| Not proposed | Location pages | — | — |

---

## 9. Faceted navigation principles

- **Default:** every attribute is a filter state, and filter states are not permanent SEO URLs.
- **Gate (D-07):** a filter can become an indexable landing page only if all seven conditions hold: measured demand, a category/product SERP, enough inventory, distinctness from its parent, one home, business fit, and a stable path with unique content.
- **Multi-attribute combinations** are never indexable by default.

**Per-attribute defaults (D-08):**

| Attribute | Default role |
|---|---|
| Category / type | Subcategory (gated) |
| Design / style | Subcategory for engagement rings (gated; side-stone passes) |
| Shape | Filter. Landing pages deferred for lack of data. |
| Stone origin | Filter within categories. At L1 it is a commercial hub (D-05). |
| Carat | Filter. Loose stones only, if they are sold. |
| Metal | Filter only |
| Price | Filter only; never indexable |
| Gender | Wedding-band L2 split (gated); a filter elsewhere |

Technical handling of non-indexable states (canonical, robots, parameters) is **deferred to implementation**. It is not decided here.

---

## 10. URL architecture principles

These principles are listed in full in D-12.

- **Hierarchy:**
  - Categories: `/{category}/{subcategory}/`, with at most 3 segments for commercial listings.
  - Content: `/education/…` and `/blog/…`.
  - Products: flat `/shop/<slug>`.
- **Segments:** no grouping-only segments such as `/by-design/`.
- **Naming:**
  - Lowercase and hyphenated.
  - Correctly spelled.
  - Listings plural, products singular.
  - One term per concept.
  - No CMS IDs and no brand suffix in slugs.
- **Attributes:** query parameters by default. A clean path only for gated facet landing pages.
- **Products:** one product has one URL, and variants are selected on the page (D-11).
- **Platform:** a native Shopify build would force `/collections/`, `/products/`, `/blogs/` and `/pages/` prefixes with flat handles, so the hierarchy would be carried by breadcrumbs and links (D-17).
- **Exact URLs are not chosen here, and no redirects are recommended.**

---

## 11. Current vs proposed IA

The full table is in `12_current_vs_proposed_ia.csv` (25 rows). The main ones:

| Current | Problem | Future principle |
|---|---|---|
| 41 nav subcategories | Not in sitemap | P-DECLARED: indexable set = sitemap = link graph |
| 13 subcategories + /collection + /hiphop | Empty / placeholder | P-EMPTY |
| by-desgin, solitare, anniversay, pavee | Misspellings | P-SLUG |
| `/engagement-rings/by-desgin/<style>` | Grouping-only segment | P-DEPTH |
| bracelet vs earrings, toi-moi vs toi-et-moi | Inconsistent naming | P-NAMING |
| Eternity in WB and Fine Jewellery | Two homes | P-ONE-HOME |
| /t-bar at L1 | Style at product-family level | P-TAXONOMY |
| Test PDP, TEST SUBCAT | Test artifacts live | P-NO-TEST |
| `-copy-<id>` / numeric-ID variant URLs | Variant-per-URL | P-PRODUCT |
| /blog vs /education | No distinction; OV-01 | P-ONE-TOPIC-ONE-HOME |
| Lab-grown only in blog posts | No commercial page for a commercial SERP | Separate commercial and informational page types |

---

## 12. Decisions deferred to Stage 13 (future blog strategy / existing-content decisions)

- The Blog's topics, cadence and categories.
- Which existing blog articles become Education content, and the migration reasoning for the 26 ranking keywords on 4 articles.
- Resolving OV-01 (certification), OV-06/07/08 (buying guides) and OV-02/03 (lab-grown legitimacy).
- Whether content slugs drop the "-house-of-diams" suffix, weighed against ranking equity.

## 13. Decisions deferred to Stage 14 (Education strategy)

- The final topic-hub list and names, and URL depth under `/education`.
- The article inventory for each hub: how clusters combine into articles.
- The scope of Gemstones & Alternatives (moissanite, CZ, coloured stones) and Metals (novelty materials in CL-114).
- Whether a ring-size tool is a TOOL page or an article.
- Author/expert profiles.

## 14. Decisions deferred to Stage 15 (keyword→URL map)

- Exact URLs for every page. Whether misspelled or grouped paths change, with migration reasoning.
- Which conditional subcategories pass the D-07 gate.
- The eternity home (bands or rings), the T-Bar and Hip Hop placement, and the scope of Rings.
- The "jewelry" vs "jewellery" label and slug (D-15).
- Keyword targeting for the homepage, categories and FAQ (OV-13, OV-10).
- Natural Diamonds hub, loose-diamond pages, wholesale and bespoke sub-pages. These depend on business answers.

---

## 15. Risks and uncertainties

1. **The commercial keyword gap is the largest risk.** Commercial branches are structured on catalogue share and existing structure. If a commercial keyword pull shows different demand, for example strong shape-led queries, some filters would become landing pages. The IA is designed so they can be promoted without restructuring.
2. **SERP sample.** Only 100 of 1,936 keywords (5.2%) have SERPs, and only about 10 of those are commercial. The competitor URL conventions cited here come from that small commercial set.
3. **Catalogue facts are approximate.** Product-type counts are derived from slugs [STAGE 1], and subcategory product counts are approximate [STAGE 10].
4. **Business-model unknowns.** It is not known whether HOD sells natural diamonds, loose stones, gemstones or moissanite, or runs a trade business. Several branches depend on these answers.
5. **Platform unknown.** Native Shopify would constrain URL expression (D-17).
6. **Migration risk.** HOD's only measurable equity is 28 weak rankings, 26 of them on blog articles. Restructuring content systems must account for it in Stage 13.
7. **No GSC, backlink, internal-link or index-coverage data.** Equity judgments are partial [STAGE 10].
8. **Inherited limits.** Stage 8's page-type heuristic labelled 24% of SERPs OTHER. Stage 11's clustering is rule-based.

---

## 16. Recommended next research stage

The planned sequence continues with **Stage 13: future blog strategy and existing-content decisions**. It can run on current data, because the Blog/Education separation is now defined.

**Recommendation.** Before **Stage 15** maps keywords to URLs, run a **targeted commercial keyword and SERP supplement** (D-19). It should cover:
- engagement-ring style × shape × origin
- wedding bands by gender and style
- earrings, necklaces and bracelets by type
- fine jewelry / fine jewellery
- custom and bespoke engagement rings
- lab-grown engagement rings

Without it, most commercial subcategories stay conditional. This supplement:
- is a paid stage and needs its own endpoint verification, cost estimate and approval
- is **not authorised by this stage and was not run**
- could run before Stage 13 or between Stages 14 and 15. The timing is the user's decision.

Business questions for the owner, which cost no API spend:
1. Does HOD sell natural-diamond pieces?
2. Does HOD sell loose diamonds?
3. Does HOD sell gemstone or moissanite jewellery?
4. Does HOD run a trade/wholesale business?
5. Does HOD have US showrooms?
6. What platform will the new site use (native Shopify, headless or other)?
7. What are T-Bar and Hip Hop meant to be: product types or curated collections?
