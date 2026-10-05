# Stage 12 — IA Decision Log

Date: 2026-09-24. Scope: SEO information architecture at the structural level. No keyword→URL assignment (Stage 15), no blog strategy (Stage 13), no detailed Education architecture (Stage 14), and no redirects, canonicals, robots or sitemap changes. Local project files only; **no DataForSEO call was made**.

**Labels used throughout**
- **OBSERVED FACT**: directly present in a project dataset.
- **INFERENCE**: reasoned from facts; could be wrong.
- **PROPOSED ARCHITECTURE**: a design choice for the future site. It is not a description of the current site.
- **INSUFFICIENT EVIDENCE — DEFER**: project data cannot support a decision.

**Confidence**
- **HIGH**: direct SERP, ranking or site evidence, and nothing contradicts it.
- **MEDIUM**: sound structural reasoning plus partial evidence.
- **LOW**: mostly business context or convention.

**Evidence sources**
- `[STAGE 1]` site inventory
- `[STAGE 3]` Labs ranked keywords
- `[STAGE 7]` master keyword DB
- `[STAGE 8]` 100 validated SERPs
- `[STAGE 9]` competitor landscape
- `[STAGE 10]` existing content and nav check
- `[STAGE 11]` clusters

---

## The evidence constraint behind most decisions

**OBSERVED FACT [STAGE 7/11]:** the master keyword universe contains almost no commercial product-category queries.

- 0 keywords combine lab-grown or natural with "engagement ring".
- 0 combine a diamond shape with a jewellery type.
- 0 are about tennis bracelets, eternity bands, solitaires or custom jewellery.
- Only 8 keywords mention wedding bands at all, and none is a shopping query.
- There are no clusters for Wedding Bands, Necklaces & Pendants, Bracelets, Fine Jewellery or Bespoke.

The universe was seeded from HOD's own domain (Stage 4) and from lab-grown-led seeds (Stage 6). That is why it covers informational topics well and commercial categories poorly.

**Consequence:** the informational side of the IA rests on strong evidence. The commercial side rests on four things:
- the product catalogue [STAGE 1]
- the live structure [STAGE 10]
- a small number of commercial SERPs [STAGE 8]
- business context

Missing commercial keywords are never read as missing demand. Wherever a commercial page's *indexability* depends on demand, it is marked conditional or deferred.

---

## D-01 — Top-level sections

**DECISION (PROPOSED ARCHITECTURE).** The future site has these L1 sections:

1. **Engagement Rings**
2. **Wedding Bands**
3. **Fine Jewellery**, the umbrella for Earrings, Necklaces & Pendants, Bracelets and non-bridal Rings
4. **Bespoke / Custom**
5. **Lab-Grown Diamonds**, a commercial origin hub. This one is *conditional*.
6. **Education**, the evergreen guide
7. **Blog / Journal**
8. **Brand & Support**: About, Contact, FAQ and Policies

Education and Blog sit together under a "Resources" navigation grouping. A **Natural Diamonds** commercial hub is deferred.

**EVIDENCE**
- [STAGE 1]:
  - The catalogue is roughly 74 engagement-ring, 40 earring, 24 necklace, 10 bracelet and 6 band PDP slugs. These counts are slug-derived and approximate.
  - Engagement Rings, Wedding Bands, Fine Jewellery and Bespoke already exist.
- [STAGE 10]: 41 live nav subcategories exist under these parents.
- [STAGE 11]: 51 of 89 clusters are INFORMATIONAL.
- [STAGE 8]:
  - Lab-grown head terms are served by retailer collection pages.
  - EDITORIAL_GUIDE is the most common dominant page type (39/100).

**ALTERNATIVES CONSIDERED**
- (a) Earrings, Necklaces and Bracelets as separate L1 sections. See D-02.
- (b) A single "Diamonds" L1 that merges commercial and educational content. Rejected: Stage 11 shows CL-001 (head/commercial) and CL-002 (definitional) are DISTINCT_INTENT, and their SERPs differ.
- (c) Keeping Blog as the only content system. Rejected (D-10).
- (d) Adding T-Bar and Hip Hop as L1 sections. Rejected (D-14).

**RATIONALE**
- L1 sections map to product families, one service, and two content systems with different jobs.
- Nothing is added at L1 just because it has search volume. The origin hub is the only addition, and it stays conditional.

**CONFIDENCE:** MEDIUM. The informational side is HIGH. The commercial L1 set is MEDIUM because it rests on catalogue share and existing structure, not measured demand.

**DEFERRED QUESTION**
- Does HOD sell natural-diamond pieces?
- Does HOD sell loose stones?
- Should a commercial keyword pull validate each L1 label before Stage 15?

---

## D-02 — Earrings, Necklaces & Pendants and Bracelets sit under Fine Jewellery in the hierarchy but are first-class in navigation

**DECISION.**
- Keep the product-type categories as L2 under the Fine Jewellery umbrella: `/fine-jewellery/earrings/` pattern.
- Expose them directly in the main navigation. Navigation placement and URL depth are separate choices.

**EVIDENCE**
- [STAGE 10]: they already live at `/fine-jewellery/{earrings,necklaces,bracelet}`, and they are populated.
- [STAGE 10] none of them has a ranking, and [STAGE 11] none has a cluster.
- CLAUDE.md rule 11 says to preserve existing URLs where practical.
- [STAGE 8] competitors nest ring styles under their category. For earrings, necklaces and bracelets there is no competitor-structure evidence either way.

**ALTERNATIVES CONSIDERED**
- Flat L1 URLs (`/earrings/`, `/necklaces/`, `/bracelets/`). These are shorter and a common convention. The project has no evidence that they would perform better, and adopting them would change live URLs (rule 12 requires migration reasoning).

**RATIONALE**
- Depth 2 is well within reasonable click and path depth.
- Keeping the current parent avoids a structural change that the evidence does not justify.

**CONFIDENCE:** MEDIUM.

**DEFERRED QUESTION**
- If the umbrella label changes (D-15), or the platform forces flat collection paths (D-17), this decision is revisited in Stage 15.

---

## D-03 — Engagement-ring styles are L2 subcategories; side-stone is confirmed and the others are conditional

**DECISION.**
- Style (solitaire, halo, pavé, side-stone, three-stone, bezel, toi-et-moi, nature-inspired) is the subcategory dimension for engagement rings.
- Side-stone is a confirmed indexable L2.
- The other styles are indexable only if they pass the D-07 gate.
- The `/by-design/` grouping segment has no place in the future hierarchy (P-DEPTH).

**EVIDENCE**
- [STAGE 3] the side-stone subcategory ranks: pos 104 for *side stones engagement rings* (1,000).
- [STAGE 8] that query's SERP is CATEGORY-dominant and TRANSACTIONAL. The top results are style category pages, 3 of them nested under an engagement-rings parent with no grouping segment:
  - helzberg `/engagement-rings/side-stone`
  - diamondsfactory `/engagement-rings/side-stone-rings`
  - sarahojewelry `/collections/engagement-rings/ring-style-side-stone`
  - zales uses a flat `/side-stones-engagement-rings`
- [STAGE 10]: the `/by-desgin` hub and all 8 style URLs are live and populated. None is in the sitemap, and the misspelled segment `by-desgin` is in use.
- [STAGE 11]: CL-121 (setting types) is an EDITORIAL_GUIDE SERP, which is an informational need.

**ALTERNATIVES CONSIDERED**
- (a) Keep a `/by-design/` layer. Rejected: it names no real level and adds depth.
- (b) Make every style indexable now. Rejected: demand for the other 7 styles is unmeasured.
- (c) Make shape the primary subcategory dimension. Rejected on evidence: 0 shape+ring keywords were measured (D-08).

**RATIONALE:** only one style has SERP proof. The page *type* is validated, but not every *instance* of it.

**CONFIDENCE:** HIGH for side-stone and for the style dimension. MEDIUM for removing the grouping segment. LOW on which other styles qualify.

**DEFERRED QUESTION**
- Style demand needs measuring.
- Any URL change for the side-stone page (the one ranking subcategory) needs migration reasoning. That belongs to Stage 13/15 and is not decided here.

---

## D-04 — Wedding bands: gender split is conditional; band styles are deferred

**DECISION.**
- Women's and Men's are an allowed L2 split, indexable only when populated.
- Band styles (eternity, anniversary, pavé, solid, classic, designer, cigar) are INSUFFICIENT EVIDENCE — DEFER.
- Eternity has one category home (P-ONE-HOME).

**EVIDENCE**
- [STAGE 10]:
  - `/for-him` and all its children are empty.
  - Of the 7 `/for-her` children, only 2 are populated.
  - OV-14: eternity sits in two places.
- [STAGE 11]: no wedding-band cluster. The 2 validated band keywords are informational metal questions (CL-113).

**ALTERNATIVES CONSIDERED**
- A style-first split with gender as a filter. That is also valid. The current gender-first split is kept only because it already exists. This is not a strong preference.

**RATIONALE:** there is no demand evidence and most of this layer is empty, so the structure is minimal and conditional.

**CONFIDENCE:** LOW to MEDIUM.

**DEFERRED QUESTION**
- Is the split gender-first or style-first?
- Where does eternity live: bands or rings?

---

## D-05 — Stone origin: a conditional commercial Lab-Grown hub, a deferred Natural hub, and a facet everywhere else

**DECISION**
- A commercial **Lab-Grown Diamonds** landing page is proposed, conditional on business confirmation and real inventory.
- **Natural Diamonds** commercial landing: INSUFFICIENT EVIDENCE — DEFER.
- Inside each category, origin is a **filter** by default.
- A "lab-grown engagement rings" landing page is INSUFFICIENT EVIDENCE — DEFER.

**EVIDENCE**
- [STAGE 8]:
  - *lab grown diamonds* (135,000) is BRAND/CATEGORY-dominant and *lab diamonds* (27,100) is CATEGORY/TRANSACTIONAL. The top results are retailer collection pages (withclarity `/collections/lab-diamonds`, brilliantearth `/lab-grown-diamonds/`, miadonna `/collections/lab-grown-diamond-jewelry`).
  - *natural diamonds* (18,100) shows the same pattern (solomonbrothers `/natural-diamonds`, diamondsdirect `/natural-diamonds/`).
- [STAGE 11]:
  - CL-001 and CL-070 are HIGH evidence.
  - CL-001 vs CL-002 is DISTINCT_INTENT.
  - 0 keywords combine lab-grown with engagement ring.
- [STAGE 10]:
  - The homepage title targets "Lab-Grown Diamond Engagement Rings".
  - All of HOD's lab-grown equity sits in informational blog posts.
- [STAGE 1]: no PDP slug indicates natural stones or loose diamonds.

**ALTERNATIVES CONSIDERED**
- (a) Answer the lab-grown head term with an Education article. Rejected: the SERP is commercial.
- (b) Make origin the top-level split of the whole catalogue (`/lab-grown/engagement-rings/`). Rejected: it doubles every category path and would create duplicate category sets if HOD also sells natural stones.
- (c) Do nothing commercial for origin. Rejected: the one entity with HIGH-evidence commercial SERPs would have no commercial page.

**RATIONALE**
- Google shows two different intents for the same entity. That calls for two page types, one commercial and one educational, and they cross-link.

**CONFIDENCE**
- MEDIUM for the Lab-Grown hub.
- LOW for Natural (catalogue unknown).
- HIGH that origin inside categories is a facet by default.

**DEFERRED QUESTION**
- Does HOD sell natural-diamond jewellery or loose stones?
- Is lab-grown the primary positioning?
- Does "lab-grown engagement rings" have measured demand?

---

## D-06 — Diamond concepts live in Education, not in the commercial tree

**DECISION.** Lab-grown science, CVD/HPHT, lab-vs-natural, 4Cs, shapes, cuts and certification are Education topic hubs. Commercial pages link *into* them. They do not host them.

**EVIDENCE**
- [STAGE 11]:
  - Lab-grown has 24 clusters.
  - Quality/4Cs has 12, plus CL-050.
  - Shapes has 5, plus CL-065.
  - Certification has 5.
  - Nearly all of these are INFORMATIONAL or COMMERCIAL_RESEARCH.
- [STAGE 8]:
  - CL-016/017/041 SERPs are EDITORIAL_GUIDE.
  - CL-011 is COMPARISON.
  - *diamond shape* is served by education paths (gia, tiffany `/diamond-education/`, brilliantearth `/guides/`, bluenile `/education/`).
- [STAGE 3]: 26 of 28 HOD rankings sit on informational articles.

**ALTERNATIVES CONSIDERED**
- (a) Put concept content on category pages, for example 4Cs text on the engagement-ring page. Rejected as the *primary* home, though short supporting copy on category pages is fine.
- (b) One page per cluster. Rejected: a cluster is not a page (Stage 11).

**RATIONALE:** the SERPs for these concepts are informational, so they belong in the informational system.

**CONFIDENCE:** HIGH.

**DEFERRED QUESTION:** the topic-hub list, article inventory and the merging or splitting of clusters into articles are all Stage 14.

---

## D-07 — The gate for any filter or subcategory to become an indexable page

**DECISION.** A filter state or subcategory becomes an indexable, permanent URL only if **all** of the following hold:

1. **Demand.** Independent search demand for the refinement is measured in project keyword data. A related informational question does not count.
2. **SERP type.** SERP validation shows Google serves category or product pages for it, not editorial guides.
3. **Inventory.** It holds enough in-stock products to be a useful listing. The minimum is set at implementation, not invented here.
4. **Distinctness.** Its product set and intent are materially different from its parent's.
5. **One home.** No other indexable page already serves the same intent (P-ONE-HOME).
6. **Business fit.** The refinement matches what HOD sells and wants to rank for.
7. **Stability.** It has a stable, clean path and unique introductory content.

Multi-attribute combinations (for example shape + metal + price) are never indexable by default.

**EVIDENCE**
- [STAGE 1]: `/collection`, an indexable filtered view, is empty.
- [STAGE 10]: 13 empty subcategories are live.
- [STAGE 11]: attribute keywords are overwhelmingly informational. Examples are metal questions and "are lab grown diamonds cheaper".
- [STAGE 8]: the one style with SERP proof is side-stone.
- CLAUDE.md rules 4, 5 and 6.

**ALTERNATIVES CONSIDERED:** a numeric threshold score. Rejected, per the no-fake-precision rule.

**RATIONALE:** this prevents both thin pages and page explosion, and it still allows attribute pages where evidence exists.

**CONFIDENCE:** HIGH as a principle.

**DEFERRED QUESTION:** the product-count minimum, and how non-indexable states are technically handled, belong to implementation.

---

## D-08 — Default role of each attribute

**DECISION (defaults, on current evidence)**

| Attribute | Default | Could justify a landing page? | Evidence |
|---|---|---|---|
| Category/type (earrings → studs) | Subcategory | Yes, via the gate | [STAGE 10] live populated types; [STAGE 11] CL-125 |
| Design/style (side-stone, halo…) | Subcategory for engagement rings | Yes, via the gate (side-stone passes) | [STAGE 3]/[STAGE 8] |
| Shape | Filter | Possibly. INSUFFICIENT EVIDENCE — DEFER | [STAGE 11] 0 shape+jewellery keywords; [STAGE 1] shapes widespread in slugs |
| Stone origin (lab/natural) | Filter in categories; commercial hub at L1 | Hub yes (D-05); origin × category deferred | [STAGE 8] |
| Carat | Filter | Only for loose stones, if sold (CL-006 CATEGORY SERP) | [STAGE 8] |
| Metal | Filter | No evidence | [STAGE 11] 3 metal+product keywords, all informational |
| Price | Filter | No; never indexable | [STAGE 11] price keywords all informational |
| Gender | L2 split for wedding bands only; filter elsewhere | Via the gate | [STAGE 10] men's branch empty |
| Other (setting height, band width, availability, sort) | Filter / sort | No | none |

**EVIDENCE:** as cited per row in the table above ([STAGE 1], [STAGE 3], [STAGE 8], [STAGE 10], [STAGE 11]).

**ALTERNATIVES CONSIDERED:** (a) make shape a landing-page dimension now, the most common competitor pattern for loose stones. Rejected: there is no project measurement for shape × jewellery type. (b) Make metal an L2 split. Rejected: every metal keyword is an informational question.

**RATIONALE:** each attribute gets the least committal role the evidence allows, so it can be promoted later through D-07 without restructuring.

**CONFIDENCE:** MEDIUM. Shape is the most likely to change once commercial data exists.

**DEFERRED QUESTION:** a targeted commercial keyword pull for shape × type and origin × type.

---

## D-09 — Education is the single evergreen informational home

**DECISION.**
- `/education` (the existing URL) is the one home for evergreen reference content, buying guides and comparison guides.
- It is organised into topic hubs. At concept level these are: Lab-Grown, Natural, Quality/4Cs, Shapes & Cuts, Certification, Metals & Materials, Gemstones & Alternatives, Ring & Jewellery Guides, and Buying Guides.

**EVIDENCE**
- [STAGE 11]: 51 INFORMATIONAL and 14 COMMERCIAL_RESEARCH clusters.
- [STAGE 8]: PAA on 98% of SERPs, AI Overview on 78%, EDITORIAL_GUIDE the most common dominant type.
- [STAGE 9]: 94 RELEVANT appearances come from education/guide paths across 10 domains.
- [STAGE 10]: `/education` already exists but holds 1 article.

**ALTERNATIVES CONSIDERED**
- A new path such as `/learn/` or `/diamond-guide/`. There is no evidence of a benefit, and `/education` already exists (rule 11).
- Blog-only. Rejected (D-10).

**RATIONALE:** evergreen content needs a stable, topic-organised home that can be updated in place.

**CONFIDENCE:** HIGH for the role. MEDIUM for the topic-hub list, which is subject to Stage 14.

**DEFERRED QUESTION:** the hub names, the article list and the URL depth under `/education` are Stage 14. Gemstones & Alternatives scope depends on business relevance.

---

## D-10 — Blog stays a distinct system with a different job

**DECISION.**
- Blog (or Journal) stays a separate content system for time-bound, editorial and brand content: trends, launches, stories, craftsmanship features and style.
- It sits under the Resources grouping, not in the primary commercial navigation.
- Any evergreen subject has exactly one home, in Education (P-ONE-TOPIC-ONE-HOME).
- Blog posts link to Education and category pages. They do not re-explain Education topics.

**EVIDENCE**
- [STAGE 10]:
  - Blog and Education have no observable difference in intent, format or topic.
  - OV-01 is a CLEAR_OVERLAP.
  - All 26 article rankings sit in `/blog`.
- [STAGE 9]:
  - 141 RELEVANT appearances are on `/blog(s)/` paths across 33 domains, so blogs do rank.
  - 5 domains (bluenile, ritani, stienhardt, rarecarat, whiteflash) rank with *both* blog and education paths.

**ALTERNATIVES CONSIDERED**
- (a) Fold the Blog into Education. This is possible, but it removes the home for brand and editorial content that has no evergreen role.
- (b) Keep both with overlapping scopes, as today. Rejected: that is the cause of OV-01.
- (c) Keep Blog as the evergreen home and drop Education. Rejected: date-led blog formats suit evolving reference topics poorly, and competitors that rank strongly on reference topics use guide/education paths (INFERENCE).

**RATIONALE:** separating the two by *job*, rather than by topic, is what prevents the overlap from coming back.

**CONFIDENCE:** MEDIUM. The separation principle is HIGH. Whether the Blog earns its place depends on Stage 13.

**DEFERRED QUESTION**
- Blog topics, cadence and categories are Stage 13.
- Which existing blog articles move to Education is Stage 13/14. This carries migration risk because 26 rankings sit on them.

---

## D-11 — Product URLs: flat, one product per URL, variants on the page

**DECISION.**
- Product detail pages keep a flat path under the shop prefix (`/shop/<descriptive-slug>` pattern).
- One sellable product has one URL.
- Carat, metal and size variants are selected on the page. They are not separate URLs, unless a variant is genuinely a separate product with independent demand.
- Slugs contain no CMS IDs and no "-copy-" tokens.
- The category relationship is expressed through breadcrumb and links, not the path.

**EVIDENCE**
- [STAGE 1]:
  - 169 PDPs sit under `/shop/`.
  - There are 3 `-copy-<id>` slugs and 10 numeric-ID slugs.
  - Carat variants are separate URLs.
- [STAGE 3]: no variant URL ranks. The one ranking PDP is a clean slug in a PRODUCT SERP [STAGE 8].

**ALTERNATIVES CONSIDERED**
- Category-nested product paths (`/engagement-rings/<product>`). Rejected: a product in several categories would get several paths.

**RATIONALE:**
- Flat product paths already exist, so keeping them preserves the current pattern (rule 11).
- One URL per product concentrates signals.
- CMS-ID slugs carry no meaning for users or search.

**CONFIDENCE:** MEDIUM to HIGH.

**DEFERRED QUESTION:** the platform's variant model (D-17), and what happens to existing variant URLs (implementation).

---

## D-12 — URL structure principles

**DECISION (PROPOSED ARCHITECTURE)**

| Principle | Rule |
|---|---|
| Hierarchy | `/{category}/` → `/{category}/{subcategory}/` → at most `/{umbrella}/{category}/{subcategory}/` for commercial listings. Education: `/education/…`. Blog: `/blog/…`. Products: flat. |
| Depth | Commercial listings: maximum 3 path segments. No grouping-only segments (P-DEPTH). |
| Naming | Lowercase, hyphen-separated, correctly spelled, plain English names of the thing. No brand suffix in content slugs. No CMS IDs. |
| Singular/plural | Listings plural (`engagement-rings`, `earrings`, `bracelets`). A product slug names one item. |
| One term per concept | For example "toi-et-moi" everywhere, and one spelling of "solitaire". |
| Attributes | Filters use query parameters by default. Only a gated facet landing page (D-07) gets a clean path segment. |
| Indexable vs non-indexable | Indexable = homepage, L1–L3 categories that pass P-EMPTY and, where required, D-07, PDPs, service, brand, support, Education and Blog content. Non-indexable = filter/sort/pagination states, search, account/cart/checkout, test URLs, blog taxonomy archives. |
| Stability | A permanent SEO URL does not change when merchandising changes. Curated or seasonal collections get their own page type. |

**EVIDENCE**
- [STAGE 10] misspellings, singular/plural mix and the `by-desgin` segment.
- [STAGE 1] CMS-ID slugs and the brand suffix in content slugs.
- [STAGE 8] competitor nesting for engagement-ring styles.
- CLAUDE.md rules 4 and 5.

**ALTERNATIVES CONSIDERED:** path-based facets (`/engagement-rings/oval/platinum/`). Rejected as a default because it causes page explosion.

**RATIONALE:** these principles remove every class of URL defect observed in Stages 1 and 10, and they keep the indexable URL count bounded by the gate rather than by the number of attribute combinations.

**CONFIDENCE:** HIGH for the principles. Exact URLs are **not** decided (Stage 15). No redirect is recommended.

**DEFERRED QUESTION:** whether existing misspelled or suffixed URLs change. That needs migration reasoning in Stage 13/15.

---

## D-13 — No empty, placeholder or test pages in the indexable IA

**DECISION.** A listing exists as an indexable page only while it holds products (P-EMPTY). No test or staging URL is part of the production IA (P-NO-TEST).

**EVIDENCE**
- [STAGE 10]: 13 empty subcategories.
- [STAGE 1]:
  - `/collection` shows 0 pieces.
  - `/hiphop` is "Coming Soon" with a "TEST SUBCAT" item.
  - `/shop/fine-jewellery-test-product` is live.

**ALTERNATIVES CONSIDERED:** none credible.

**RATIONALE:** empty and placeholder pages give searchers nothing and fall under CLAUDE.md rule 4 (no thin category pages).

**CONFIDENCE:** HIGH.

**DEFERRED QUESTION:** how each existing case is handled (populate, hide, remove, redirect) is implementation plus Stage 13/15. It is not decided here.

---

## D-14 — Curated collections (T-Bar, Hip Hop) are a separate page type; their placement is deferred

**DECISION.**
- Theme and merchandising collections are a CURATED_COLLECTION page type, kept outside the product-type taxonomy.
- They are indexable only if gated.
- Whether T-Bar is a necklace subtype or a curated collection, and whether Hip Hop becomes a category: INSUFFICIENT EVIDENCE — DEFER.

**EVIDENCE**
- [STAGE 1]: `/t-bar` and `/hiphop` are top-level.
- [STAGE 10]: OV-16 overlaps T-Bar with necklaces.
- [STAGE 11]: 0 keywords for either.

**ALTERNATIVES CONSIDERED:** (a) Keep both at L1, as today. Rejected: that mixes a style and a theme with product families (P-TAXONOMY). (b) Fold T-Bar into Necklaces now. Deferred: T-Bar may also cover bracelets or other pieces, and project data does not show this.

**RATIONALE:** themes change with merchandising, and the product-type taxonomy should not.

**CONFIDENCE:** MEDIUM on the principle. Placement is deferred.

**DEFERRED QUESTION:** merchandising intent from the business, plus a commercial keyword check.

---

## D-15 — "Jewellery" vs "jewelry" in a US-primary market

**DECISION.** INSUFFICIENT EVIDENCE — DEFER on the slug.

INFERENCE: US-English user-facing labels are preferable, because the primary market is the US.

**EVIDENCE**
- [STAGE 11 map]: "jewelry" appears in 23 master keywords and "jewellery" in 1.
- The master DB is US-market data.
- [STAGE 10]: `/fine-jewellery` has no rankings.
- [STAGE 11]: no master keyword targets the label itself.

**ALTERNATIVES CONSIDERED:** changing the slug now. Rejected here, because any URL change needs migration reasoning (rule 12) and the label's search role is unmeasured.

**RATIONALE:** the spelling signal is real, but the label's own demand is unmeasured and the slug holds no equity. Deciding it together with the commercial keyword pull costs nothing and avoids a second migration.

**CONFIDENCE:** LOW.

**DEFERRED QUESTION:** measure "fine jewelry" and related commercial terms, then decide in Stage 15 together with brand preference.

---

## D-16 — Evaluated and not proposed

**DECISION**
- **Not proposed:**
  - gemstone or moissanite commercial categories
  - diamond-tester product pages
  - location/city pages
- **Wholesale/trade section:** INSUFFICIENT EVIDENCE — DEFER.
- **Bespoke sub-pages:** INSUFFICIENT EVIDENCE — DEFER.

**EVIDENCE**
- [STAGE 8]:
  - Morganite rings and mixed-metal rings have CATEGORY SERPs.
  - The tester query has a CATEGORY SERP of tool retailers.
  - Local Pack appears on 10% of SERPs, mostly for off-topic businesses.
- [STAGE 1]: no gemstone, moissanite or loose-stone PDPs.
- [STAGE 11]:
  - CL-007 is wholesale (TRANSACTIONAL).
  - CL-005 is geo (MIXED).
  - There are 0 bespoke keywords.

**ALTERNATIVES CONSIDERED:** build gemstone or moissanite categories for their volume (moissanite 201,000; tanzanite rings 12,100). Rejected under CLAUDE.md rules 3 and 8.

**RATIONALE**
- Volume without catalogue fit does not justify a page (rules 3, 8, 9).
- Informational comparisons (moissanite vs diamond, testers) keep a slot in Education (D-09).

**CONFIDENCE:** MEDIUM.

**DEFERRED QUESTION:** these are business-model questions. Does HOD sell gemstones or moissanite? Does it run a trade business? Does it have US showrooms?

---

## D-17 — The IA is a logical hierarchy; how the URLs are expressed depends on the platform

**DECISION.**
- The hierarchy in this stage is logical: parent → child relationships, breadcrumbs, navigation and internal links.
- If the future build is native Shopify, its fixed path prefixes (`/collections/`, `/products/`, `/blogs/<blog>/`, `/pages/`) and flat collection handles will constrain the paths. The hierarchy must then be carried by breadcrumbs, handles and internal links rather than nested paths.
- A headless or custom frontend can express nesting in paths.

**EVIDENCE**
- OBSERVED FACT [STAGE 1/10]: the current site uses custom paths such as `/engagement-rings/by-desgin/…` and `/shop/…`, not Shopify-native ones.
- OBSERVED FACT [STAGE 9]: 28 RELEVANT ranking appearances across 9 competitor domains use flat `/collections/<handle>` paths, including in top results for *lab grown diamonds* and *side stones engagement rings*.
- INFERENCE: flat collection paths do not stop category pages from ranking.

**ALTERNATIVES CONSIDERED:** fixing exact paths now. Rejected, because the platform is not final.

**RATIONALE:** defining the hierarchy logically keeps Stage 12 valid on any platform. Only the way paths are expressed changes.

**CONFIDENCE:** HIGH that the platform matters. The choice itself is deferred.

**DEFERRED QUESTION:** confirm the platform (native Shopify, headless Shopify or other) before Stage 15 fixes URL patterns. Moving from the current custom paths to any new pattern is a migration project in its own right.

---

## D-18 — Role separation between homepage, category and FAQ

**DECISION**
- The homepage targets the brand and the overall offer.
- Category pages target category subjects.
- FAQ answers service and policy questions briefly and links out for topic depth.

**EVIDENCE:** [STAGE 10]
- OV-13: the homepage and `/engagement-rings` share a title subject.
- OV-10: the FAQ duplicates article topics.

**ALTERNATIVES CONSIDERED:** let the homepage keep targeting lab-grown engagement rings, as many single-category stores do. Not chosen, because HOD has several product families and a dedicated category page for engagement rings.

**RATIONALE:** one intent per page type avoids the subject overlaps Stage 10 observed.

**CONFIDENCE:** MEDIUM.

**DEFERRED QUESTION:** exact targeting is Stage 15.

---

## D-19 — The commercial keyword gap must be closed before Stage 15

**DECISION (recommendation; not executed).**
- The architecture's commercial branches (styles, product types, shape, origin × type, bespoke, band splits, the "jewelry" label) cannot be validated with the current keyword universe.
- A targeted commercial keyword-and-SERP supplement should run before Stage 15 maps keywords to URLs.
- It is **not** authorised by this stage and needs its own cost estimate and approval.

**EVIDENCE:** the constraint section at the top of this log.
- [STAGE 7/11]: 0 or near-0 commercial category keywords.
- [STAGE 10] §8: product areas 1–7 have 0–23 INCLUDE keywords each.

**ALTERNATIVES CONSIDERED:** proceed to Stage 15 on current data. That would leave most commercial pages "conditional" permanently, or force guesses.

**RATIONALE:** Stage 15 cannot map keywords that were never collected. A small, targeted pull is cheaper than repeatedly revising the architecture.

**CONFIDENCE:** HIGH that the gap exists. The timing (before Stage 13, or between 14 and 15) is the user's call.

**DEFERRED QUESTION:** endpoint choice, seed list and cost. The cheapest suitable DataForSEO Labs endpoint needs verifying against live pricing at that time.
