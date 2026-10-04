# Stage 14 — Education architecture decision log

Date: 2026-09-24. Local project files only: no DataForSEO call, no other API, no live-site request, $0 spend.

Each decision lists the decision, evidence, rationale, uncertainty and the downstream stage it affects. IDs D14-01 to D14-30. Stage 12 decisions are cited as D-xx and Stage 10 overlaps as OV-xx. Stage 11 cluster relationships are cited as REL-xxx.

**Extra evidence computed in Stage 14.** Stage 14 re-read the 100 Stage 8 raw SERP JSON files (already paid for) and computed top-10 URL overlap for pairs that Stage 11 did not report, such as clarity scale vs SI2 vs VVS and 'diamond shape' vs 'asscher cut diamond'. It also read the composition of individual SERPs. The same 3-shared-URL "same intent" threshold as Stage 11 is used. URLs were normalised by removing `www.`, query strings and trailing slashes.

---

## D14-01 — What Education owns and what it does not

- **Decision.** Education is the single evergreen home for questions with a stable answer: definitions, how things work, grading, comparisons and buying decisions about diamonds, metals and ring practicalities. It does not own:
  - shopping queries (categories, commercial hubs, products)
  - time-bound or brand content (Blog)
  - HOD-specific service and policy answers (FAQ and policy pages)
  - the interaction inside a tool (the tool is embedded in its guide)
- **Boundaries with other page types:**
  - **Blog vs Education.** Evergreen vs dated. History and market trends (CL-014) and industry/factory content (CL-026) go to Blog. Care stays in Education, and craftsmanship moves to Blog, as Stage 13 decided.
  - **Category vs Education.** The SERP page type decides. Where Google returns CATEGORY, PRODUCT or BRAND pages, the query is commercial. This covers CL-001, CL-006, CL-063, CL-070, CL-071, CL-104, CL-120, CL-123 and CL-125.
  - **Product vs Education.** A PDP sells one item. Education explains attributes and links to products (links are decided in Stage 16).
  - **FAQ vs Education.** FAQ gives one-line answers and HOD policy, then links to the Education owner (D-18).
  - **Tools vs Education.** A tool performs a task. Its guide explains the task and owns the search need.
- **Evidence.** Stage 12 D-06, D-09, D-10, D-18. The Stage 13 framework (26 topic types). Stage 8 page types.
- **Rationale.** One topic has one home. The Stage 13 ownership rule is applied at topic level.
- **Uncertainty.** Low for the rule. Individual keyword placement is Stage 15.
- **Downstream.** Stage 15 (keyword→URL), Stage 16 (links).

## D14-02 — Hub set: 8 hubs (7 firm, 1 conditional); Buying Guides and Diamond Science are not hubs

| Candidate hub | Decision | Reason |
|---|---|---|
| Lab-Grown Diamonds | KEEP | 25 clusters (20 in Education topics), 22 of 28 HOD rankings |
| Natural Diamonds | KEEP (education-only, pillar-led, provisional) | Formation/mining/rarity/sourcing demand; balanced counterpart to lab-grown; commercial natural hub stays deferred (D-05) |
| Diamond Quality (4Cs) | KEEP | EDITORIAL_GUIDE SERPs for clarity, SI2, VVS, colour and cut |
| Shapes & Cuts | SPLIT | Shapes stay; *cut grade* moves to Diamond Quality (CL-050 SERP = 4Cs cut pages) |
| Certification | KEEP | Two validated SERPs with 0 shared URLs need two resources |
| Metals & Materials | KEEP | CL-110 HIGH; metal choice is a real purchase step |
| Gemstones & Alternatives | CONDITIONAL | Large demand, but no evidence HOD sells moissanite, simulants or gemstones |
| Ring & Jewellery Guides | KEEP (absorbs Care) | Settings SERP validated; sizing has clear business utility |
| Buying Guides | MERGE | Every validated buying question belongs to a subject hub; a separate hub would duplicate them |
| Diamond Basics & Science (new candidate) | MERGE | 10 clusters with no validated SERP and weak buyer relevance; one root-level article plus one conditional topic, no hub |

- **Evidence.** `14_education_hierarchy.csv` hub rows; Stage 11 registry; Stage 8 SERPs.
- **Uncertainty.** The Natural hub is provisional (LOW evidence). The Gemstones hub depends on the business.
- **Downstream.** Stage 15 hub URLs; Stage 16 navigation.

## D14-03 — The hub landing page is also the broad topic resource (pillar), unless the hub's topics are dissimilar

- **Decision.** Seven hubs use a **pillar** landing page: the hub page itself answers the broad question, for example "what are lab-grown diamonds", "the 4Cs", "diamond shapes", "diamond certification", "jewellery metals", "how natural diamonds form" or "diamond simulants". Ring & Jewellery Guides uses a navigation-only index, because its topics (settings, sizing, care, buying) share no common broad question.
- **Evidence.** Stage 8: broad queries such as 'diamond shape' and 'lab-grown diamond certification' are answered by single overview guides. Stage 11 shows no cluster whose need is "a list of articles".
- **Rationale.** A thin hub page plus a separate overview article would compete for the same broad queries. A pillar removes one page and one cannibalization pair per hub.
- **Uncertainty.** Medium. It depends on the template being able to carry substantial content (implementation is out of scope).
- **Downstream.** Stage 15 (hub = pillar URL), content briefs.

## D14-04 — Clusters are not pages: 89 clusters → 45 topic records → 26 proposed resources now

- **Decision.**
  - All 89 Stage 11 clusters have exactly one PRIMARY decision:
    - 24 DEDICATED_RESOURCE
    - 27 CONSOLIDATE_INTO_TOPIC
    - 14 CONDITIONAL_RESOURCE
    - 8 DEFER
    - 14 EXCLUDE_NOT_EDUCATION
    - 2 EXCLUDE_OFF_SCOPE
  - 23 SECONDARY rows record interim homes and shared sub-topics.
  - The 45 topic records split into 18 PROPOSED, 8 PROPOSED_PROVISIONAL, 14 CONDITIONAL and 5 DEFERRED.
- **Evidence.** `14_education_cluster_consolidation.csv`.
- **Rationale.** CLAUDE.md rules 2, 3, 6 and 19. Pages are split only where SERP overlap or a distinct searcher need supports it. Clusters are merged where the need is the same, even when the wording differs.
- **Uncertainty.** Only 100 of 1,936 keywords have direct SERP evidence. 9 topics carry INSUFFICIENT_EVIDENCE for the topic or for its main boundary.
- **Downstream.** Stage 15.

## D14-05 — Lab-grown commercial head terms stay out of Education

- **Decision.** CL-001 ('lab grown diamonds' 135,000; 'lab diamonds' 27,100) is EXCLUDE_NOT_EDUCATION and owned by the conditional commercial Lab-Grown hub. The Education pillar (EDU-LG-00) targets definition, names and types (CL-002/003/004).
- **Evidence.** Stage 8: BRAND/CATEGORY SERPs for the head terms. REL-004 DISTINCT_INTENT.
- **Rationale.** An informational page cannot be the primary answer on a retailer SERP (D-05).
- **Uncertainty.** Low.
- **Downstream.** Stage 15: the head term must not map to Education.

## D14-06 — CVD and HPHT do not get their own pages; the CVD-vs-HPHT article is the single home

- **Decision.** CL-016 (CVD vs HPHT), CL-017 (HPHT) and CL-018 (CVD) are consolidated into one Education resource, EDU-LG-03, which is the existing blog article. CVD and HPHT are SECTION_ONLY sub-nodes. No separate HPHT or CVD page is proposed.
- **Evidence.**
  - HPHT head SERP ('hpht lab grown diamonds', 8,100):
    - 4 of 9 organic results are HPHT-vs-CVD comparison articles (rarecarat, stienhardt, ritani, and a reddit 'hpht vs cvd' thread).
    - 1 is GIA's combined 'HPHT and CVD growth processes' page.
    - 3 are HPHT-only articles, and 1 is a shop.
  - The two HPHT head variants share 7 of 10 URLs with each other.
  - Single-method CVD SERPs ('what is cvd lab grown diamond', 'are cvd diamonds real') share 3 to 4 URLs with CVD-vs-HPHT SERPs and with each other. They are more single-method-led than HPHT: vrai, queensmith, growndiamondcorp and diamondnexus 'what is a CVD diamond' pages.
  - HOD's comparison article ranks for HPHT at position 49 (about 34 of its 36.5 ETV) and for CVD queries at 27 and 36 (Stage 3).
  - Stage 13: HIGH migration risk; a split could fragment equity.
- **Rationale.** Google already accepts comparison pages for HPHT queries, and HOD's only meaningful equity sits on one URL. Splitting it would create a new unranked page competing with the page that already ranks.
- **Uncertainty.** Medium for CVD, whose single-method SERP is more CVD-specific and whose 3,600 head term 'cvd diamond' is not validated. Low for HPHT.
- **Revisit condition (CVD only).** Two conditions must both hold: (a) after the in-place update, CVD single-method queries do not improve in GSC, and (b) a 'cvd diamond' SERP shows single-method pages dominating. An HPHT split is not recommended.
- **Downstream.** Stage 15 maps CL-017/CL-018 keywords to the existing URL. Content brief: strengthen HPHT and CVD sections.

## D14-07 — Boundary: "Are lab-grown diamonds real?" vs "Lab-grown vs natural"

- **Decision.** These are two resources.
  - EDU-LG-01 owns *authenticity*: is it a real diamond, chemically and physically identical, FTC definition, synthetic vs simulant.
  - EDU-LG-02 owns *the choice*: which to buy, and differences in price, value, appearance and ethics.
  - Each links to the other. 'do lab-grown diamonds look real' is appearance (EDU-LG-08), not authenticity.
- **Evidence.** REL-020 (HIGH confidence): validated pairs share mean 1.0 and max 2 URLs. Both SERPs are COMPARISON-dominant, and kay.com's lab-vs-natural page ranks in both.
- **Rationale.** The URL overlap is below the same-intent threshold, but both SERPs use the same page type, so the boundary must be enforced in content.
- **Uncertainty.** MEDIUM cannibalization risk.
- **Downstream.** Stage 15 keyword split; briefs.

## D14-08 — "How lab-grown diamonds are made" is conditional on a SERP test

- **Decision.** EDU-LG-04 is CONDITIONAL. Until tested, the process is summarised in the pillar and detailed in CVD vs HPHT.
- **Evidence.** CL-015 (18 kw, 880 head) has no SERP. brilliantearth's "how are lab-grown diamonds made" guide ranks inside both the HPHT and CVD SERPs. REL-014 ambiguity with natural formation.
- **Rationale.** A separate process page could compete with the HIGH-risk CVD-vs-HPHT URL.
- **Uncertainty.** INSUFFICIENT_EVIDENCE — requires later SERP validation.
- **Test.** 3 or more shared URLs with the CVD-vs-HPHT SERPs means fold permanently into EDU-LG-03; 0 to 2 means create the page.
- **Downstream.** Optional paid SERP check (D14-29); Stage 15.

## D14-09 — "Are lab-grown diamonds worth it?" is conditional, with an interim home in lab-vs-natural

- **Decision.** CL-012 → EDU-LG-06 CONDITIONAL. Interim: a pros/cons section in EDU-LG-02.
- **Evidence.** Demand exists: 1,900 + 1,300 + 880 on the main variants. There is no SERP. The 'are lab grown diamonds real' SERP includes a pros/cons page (frankdarling '7 reasons not to buy'). REL-011 RELATED_BUT_DISTINCT.
- **Rationale.** Worth-it may share a SERP with authenticity or comparison. Building it blind risks a three-way overlap.
- **Uncertainty.** INSUFFICIENT_EVIDENCE.
- **Downstream.** D14-29 check; Stage 15.

## D14-10 — Lab-grown price, value and resale are one resource

- **Decision.** CL-008 (price), CL-009 (value/resale) and CL-086 (pawn/sell) → EDU-LG-05. The resource avoids dated price tables.
- **Evidence.** REL-009 and REL-010 are RELATED_BUT_DISTINCT with no SERP. The CL-086 head terms are lab-grown pawn questions.
- **Rationale.** One money question family; three thin pages would compete.
- **Uncertainty.** LOW evidence. MEDIUM risk against worth-it.
- **Downstream.** Stage 15.

## D14-11 — Lab-grown ethics stays separate from natural conflict-free sourcing

- **Decision.** CL-013 → EDU-LG-07 (provisional). CL-073 → EDU-NAT-02 (conditional).
- **Evidence.** REL-013 POSSIBLE_OVERLAP (LOW). The validated 'conflict free diamonds' SERP is mostly retailers' own sourcing-policy pages (brilliantearth, jared, cleanorigin, robbinsbrothers), which is a brand-policy page type.
- **Rationale.** Different origin and different page type. Conflict-free content needs a substantiated HOD sourcing policy.
- **Uncertainty.** MEDIUM.
- **Downstream.** Business input; Stage 15.

## D14-12 — Lab-grown history, market trends and industry go to Blog

- **Decision.** CL-014 and CL-026 are EXCLUDE_NOT_EDUCATION (Blog/brand). Evergreen history facts form a short section of the pillar.
- **Evidence.** Stage 13 framework: industry history and trends are TIMEBOUND. The CL-026 terms (factory, production, business) match HOD's Surat manufacturing story.
- **Uncertainty.** Low.
- **Downstream.** Blog planning.

## D14-13 — Detection and testers form one lab-grown topic; moissanite tester questions are deferred

- **Decision.** CL-020, CL-021 and the informational members of CL-022 → EDU-LG-09. Tester shopping is not targeted. CL-093 is deferred with moissanite and gets a brief mention in EDU-LG-09.
- **Evidence.** REL-016 and REL-018 are RELATED_BUT_DISTINCT. REL-019: tester devices vs moissanite tester SERPs share mean 0.4 URLs. The CL-022 validated SERPs are mixed (CATEGORY, OTHER, EDITORIAL).
- **Uncertainty.** LOW evidence (the lab-grown tester SERP is not validated).
- **Downstream.** Stage 15.

## D14-14 — Diamond Quality: a 4Cs pillar, a clarity guide, grade explainers only where SERPs show them, and one guide each for colour, cut and carat

- **Decision.**
  - EDU-4C-00 4Cs overview (pillar; CL-040, CL-023 and CL-048)
  - EDU-4C-01 clarity guide (CL-044, CL-045 and CL-046)
  - EDU-4C-02 SI (HIGH)
  - EDU-4C-03 VVS/IF/FL
  - EDU-4C-04 VS (CONDITIONAL; interim section of the clarity guide)
  - EDU-4C-05 colour
  - EDU-4C-06 cut (CL-050 and CL-088)
  - EDU-4C-07 carat (provisional)
  - EDU-4C-08 fancy colour (CONDITIONAL)
  - Grade-vs-grade comparisons (CL-044) are not separate pages.
- **Evidence.**
  - The clarity-scale SERP shares 0 URLs with the SI2 SERP and 1 with the VVS SERP.
  - The two SI2 SERPs share 7 URLs.
  - The VVS SERP includes 'VVS vs VS' and 'VVS vs SI' pages, and the SI2 SERP includes 'SI1 vs SI2' pages.
  - The colour ('are g h diamonds good quality') and cut ('diamond cut grade') SERPs are EDITORIAL guides with 0 to 1 URLs shared with the clarity scale.
- **Rationale.** Google serves the scale, individual grades, colour and cut as separate SERPs. Comparisons already appear on grade-page SERPs, so they fold in. VS lacks direct evidence.
- **Uncertainty.** MEDIUM overall. VS and carat are LOW.
- **Downstream.** Stage 15 keyword split; briefs.

## D14-15 — Lab-grown quality is integrated into the general 4Cs pillar, not a separate lab-grown 4Cs page

- **Decision.** CL-023 (lab-grown grade charts) is consolidated into EDU-4C-00 as a lab-grown grading section. Its 'vvs lab diamonds' members are secondary to EDU-4C-03. The existing 4Cs-of-lab-grown article becomes the general 4Cs pillar, which answers the Stage 13 question.
- **Evidence.** Lab-grown stones are graded on the same scales (gia.edu and igi.org lab-grown report pages in the certification SERP). CL-023 has no SERP.
- **Rationale.** A lab-grown-only 4Cs page and a general 4Cs page would target near-identical chart queries: HIGH risk if both existed.
- **Uncertainty.** INSUFFICIENT_EVIDENCE on whether Google separates 'lab grown diamond clarity chart' from 'diamond clarity chart'.
- **Downstream.** D14-29 check; Stage 15.

## D14-16 — Lab-grown appearance and durability is a separate lab-grown topic

- **Decision.** CL-019 (cloudiness, fluorescence, fading) and CL-089 (treatments) → EDU-LG-08, provisional.
- **Evidence.** These questions are about how lab-grown stones behave, not about grading scales. No SERP.
- **Uncertainty.** LOW evidence. MEDIUM risk with authenticity ('look real').
- **Downstream.** Stage 15.

## D14-17 — Shapes: one pillar that includes engagement-ring shape choice; no per-shape pages now

- **Decision.** CL-060, CL-064, CL-061 and CL-062 → EDU-SHP-00 (pillar; existing shapes article). Per-shape pages (EDU-SHP-01) are DEFERRED. CL-063 (moval/marquise-oval) is commercial. Cut grade lives in Diamond Quality (D14-02 SPLIT).
- **Evidence.**
  - 'diamond shape' (60,500) is an EDITORIAL_GUIDE SERP led by GIA's guide to shapes for engagement rings, so Google blends overview and engagement-ring choice.
  - 'asscher cut diamond' (18,100) is inventory-led: bluenile, brilliantearth and adiamor inventory pages, goodstone collections and a brand site, with 1 of 7 results an education page. It shares 0 URLs with 'diamond shape'.
- **Rationale.** Per-shape Education pages do not match the dominant page type. Shape shopping is a filter by default (D-08). This answers the Stage 13 question: overview, not a separate chooser.
- **Uncertainty.** MEDIUM. Only asscher was measured; other shapes are unmeasured.
- **Downstream.** Stage 15; D-19 supplement for shape × jewellery queries.

## D14-18 — Certification: general-certification pillar, GIA vs IGI comparison, IGI-only deferred

- **Decision.**
  - EDU-CERT-00 (pillar) = general lab-grown certification (CL-033), with CL-031 (GIA) and CL-032 (IGI) as sections. It is the retarget destination for the IGI blog.
  - EDU-CERT-01 = GIA vs IGI (CL-030), the existing Education article, UPDATE_IN_PLACE.
  - EDU-CERT-02 (reading a report, CL-034) is CONDITIONAL.
  - EDU-CERT-03 (IGI-only page) is DEFERRED.
- **Evidence.** 'lab-grown diamond certification' and 'gia vs igi lab diamond' share 0 top-10 URLs (Stage 8/11/13). No IGI-only or GIA-only keyword is validated. CL-034's validated member is a BRAND SERP (AGS).
- **Rationale.** This preserves the Stage 13 split: comparison vs general. It resolves Stage 13's open question: retarget to CL-033, the only non-comparison certification cluster with SERP evidence. An IGI-only page now would recreate OV-01.
- **Uncertainty.** MEDIUM.
- **Downstream.** Both certification changes ship together (Stage 13). Stage 15 slugs.

## D14-19 — Natural diamonds: education only, formation-led pillar; commercial natural stays deferred

- **Decision.**
  - EDU-NAT-00 pillar = formation and mining (CL-075, CL-074), with a section on raw-diamond identification.
  - EDU-NAT-01 (value, rarity and investment: CL-076, CL-085) is CONDITIONAL.
  - EDU-NAT-02 (conflict-free) is CONDITIONAL.
  - CL-070 and CL-071 are commercial.
- **Evidence.** 'natural diamonds' (18,100) and 'raw diamond' (9,900) SERPs are BRAND/CATEGORY retailer pages. 'how is diamond formed' (12,100) is unvalidated. REL-056 and REL-057 show 0 to 2 shared URLs.
- **Rationale.** Educational coverage is kept separate from the commercial decision (D-05; business question 1).
- **Uncertainty.** LOW evidence. The 'how are diamonds made' ambiguity with lab manufacture (REL-014) is INSUFFICIENT_EVIDENCE.
- **Downstream.** Business question 1; Stage 15.

## D14-20 — Gemstones & Alternatives is a conditional hub; moissanite comparisons are separate; moissanite and gemstones themselves are deferred

- **Decision.**
  - EDU-GEM-00 (simulants and CZ: CL-095, CL-094), EDU-GEM-01 (moissanite vs lab-grown: CL-092) and EDU-GEM-02 (moissanite vs diamond: CL-091) are CONDITIONAL.
  - EDU-GEM-03 (moissanite: CL-090, CL-093, CL-096) and EDU-GEM-04 (gemstones: CL-100 to CL-103) are DEFERRED.
  - CL-104 and CL-105 are commercial.
- **Evidence.** CL-092 is HIGH evidence and shares 0 URLs with CL-091 and CL-090 (REL-036, REL-038). The 'moissanite' head SERP is retailer-led. No catalogue evidence exists for moissanite or gemstones (Stage 12 D-16).
- **Rationale.** Search volume is not a reason to publish (CLAUDE.md rules 3, 8, 9). Moissanite vs lab-grown has a business case: it supports a lab-grown decision. If only one moissanite page is built, build EDU-GEM-01.
- **Uncertainty.** A business decision is needed (Stage 12 question 3).
- **Downstream.** Owner decision; Stage 15.

## D14-21 — Metals: pillar plus 14k vs 18k; rhodium conditional; tungsten is a section; novelty metals out of scope

- **Decision.**
  - EDU-MET-00 pillar = CL-112, with CL-113 as an alternative-metals section and CL-123 mixing advice as a secondary.
  - EDU-MET-01 = 14k vs 18k (CL-110; existing article MOVE).
  - EDU-MET-02 rhodium (CL-111) is CONDITIONAL.
  - CL-114 is off scope.
- **Evidence.** CL-110 HIGH (4 validated). REL-045, REL-046 and REL-049 show 0 to 1 shared URLs between karat, rhodium, tungsten and general-metal SERPs.
- **Rationale.** Distinct SERPs show distinct intents but do not oblige HOD to build every page. Tungsten has no catalogue link, so it gets a section. Rhodium matters only for white-gold aftercare.
- **Uncertainty.** LOW for the pillar (its one validated keyword is off-centre).
- **Downstream.** Stage 15.

## D14-22 — Ring & Jewellery Guides: settings, ring size, conditional care, deferred engagement-ring buying guide

- **Decision.**
  - EDU-RJG-01 settings (CL-121).
  - EDU-RJG-02 ring size (CL-124; existing article MOVE).
  - EDU-RJG-03 care (CL-115) CONDITIONAL.
  - EDU-RJG-04 engagement-ring buying guide (CL-122; existing online-ring article) DEFERRED pending D-19.
  - CL-120 and CL-125 are commercial.
- **Evidence.** 'types of diamond settings' SERP is EDITORIAL and shares 0 URLs with the side-stone CATEGORY SERP (REL-050). Ring-size-finding keywords are absent from the master DB. CL-115's demand is mostly stainless-steel and plated jewellery.
- **Rationale.** Practical guides with a stable answer belong in Education. HOD-specific resizing and returns policy belongs in FAQ/policy pages. The engagement-ring buying intent is unmeasured, so Stage 13's DEFER stands.
- **Uncertainty.** Ring-size demand is unmeasured, not absent.
- **Downstream.** D-19 supplement (unapproved); Stage 15.

## D14-23 — Tools: the article owns the need, the tool performs the task, and category and product pages close the purchase

- **Decision.** The relationship chain is Education article → tool (embedded in the article by default) → category → product. The ring-size tool (EDU-RJG-05) is embedded in the ring size guide unless SERPs for 'ring size chart' or 'ring sizer' show tool pages dominating. No calculator, quiz or glossary is proposed; each is DEFERRED in the page-type framework for lack of supporting keywords.
- **Evidence.** Stage 12 TOOL type (conditional). The master DB has no calculator or quiz demand.
- **Rationale.** A separate tool page and a guide would compete for the same "find my ring size" need.
- **Uncertainty.** INSUFFICIENT_EVIDENCE on SERP page type.
- **Downstream.** Implementation stage (not decided here); Stage 16 links.

## D14-24 — Buying Guides is a page type, not a hub

- **Decision.** BUYING_GUIDE pages sit in their subject hub: EDU-LG-10, EDU-LG-06 (conditional) and EDU-RJG-04 (deferred). The 'best clarity' and 'carat size' buying questions sit in the 4Cs guides.
- **Evidence.** Stage 11: every buying cluster (CL-012, CL-024, CL-045, CL-049, CL-122) is about a specific subject.
- **Rationale.** A generic buying-guides hub would duplicate subject hubs (Stage 10 OV-06/07/08 already show buying-guide overlap).
- **Uncertainty.** Low.
- **Downstream.** Stage 16 navigation can still group buying guides for users without a separate indexable hub.

## D14-25 — Diamond science sits at the Education root, not in a hub

- **Decision.** EDU-GEN-01 (composition, hardness, heat, facts and cutting: CL-080 to CL-083, CL-087) is a single root-level article (provisional). EDU-GEN-02 'types of diamonds' (CL-065) is CONDITIONAL. CL-084 (synonyms) is off scope.
- **Evidence.** None of the 10 clusters is validated. The 'types of diamonds' (6,600) sense is unresolved (REL-053).
- **Uncertainty.** LOW evidence.
- **Downstream.** D14-29 check for CL-065; Stage 15.

## D14-26 — Existing content destinations respect every Stage 13 decision

- **Decision.** All 16 Stage 13 rows are mapped in `content-strategy/14_education_existing_content_mapping.csv`:
  - STAY_AT_CURRENT_URL_EDUCATION_OWNED: 2 (CVD vs HPHT, lab-vs-natural; HIGH risk, DO_NOT_MOVE_NOW preserved)
  - MOVE_WHEN_CONDITIONS_MET: 5
  - RETARGET_THEN_MOVE_WHEN_CONDITIONS_MET: 1 (IGI → EDU-CERT-00)
  - ALREADY_IN_EDUCATION_UPDATE_IN_PLACE: 1 (GIA vs IGI)
  - DEFERRED: 2
  - EDUCATION_ROOT: 1 (/education)
  - NOT_EDUCATION: 4 (Blog hub, FAQ, PDP, side-stone subcategory)
- **Evidence.** Stage 13 decisions and migration-risk files.
- **Rationale.** Stage 14 names destinations and resolves Stage 13's scope questions. It does not change any migration decision or condition.
- **Uncertainty.** Low.
- **Downstream.** Stage 15 URLs; migration execution is outside research.

## D14-27 — Cannibalization rules for Education

1. One stable searcher need has one canonical Education resource. Here "canonical" means the single owning resource, not a canonical tag.
2. Comparison intent (X vs Y) stays separate from definition intent (what is X), unless the SERP shows 3 or more shared URLs (as with CVD/HPHT, D14-06).
3. Informational intent never targets a query whose SERP is CATEGORY, PRODUCT or BRAND.
4. A separate page needs SERP evidence (0 to 2 shared URLs with the nearest resource) or a clearly distinct searcher need. Volume alone never justifies a page.
5. Topics are never merged just because they share words. Merges need a shared need or SERP overlap of 3 or more URLs.
6. A hub landing page does not compete with a child: the pillar owns the broad question and children own narrow ones.
7. Interim homes are explicit (SECONDARY rows). When a conditional page is created, the interim section is reduced to a summary plus a link.
8. Existing ranking URLs keep their topic. New pages must not target the queries they rank for (CVD vs HPHT; lab vs natural).
9. FAQ and Blog never hold the full treatment of an Education topic.

- **Boundary risk register** (from `14_education_architecture.csv` and the consolidation file):
  - HIGH:
    - CVD vs HPHT ↔ any single-method or process page (EDU-LG-03/04)
    - lab-grown 4Cs ↔ general 4Cs, if split (CL-023)
    - IGI-only ↔ certification pillar (EDU-CERT-03)
  - MEDIUM:
    - authenticity ↔ comparison
    - price/resale ↔ worth-it
    - ethics ↔ conflict-free
    - 4Cs pillar ↔ clarity guide (clarity-scale keywords)
    - cut ↔ shapes
    - certification pillar ↔ GIA vs IGI
    - simulants ↔ authenticity
    - lab-grown detection ↔ moissanite tester
  - INSUFFICIENT_EVIDENCE:
    - worth-it ↔ authenticity/comparison
    - process ↔ natural formation
    - VS page
    - engagement-ring guide ↔ lab-grown buying guide
    - 'types of diamonds'
  - LOW: SI, colour, 14k vs 18k, settings, moissanite vs lab-grown ↔ moissanite vs diamond.
- **Evidence.** Stage 11 relationships; Stage 14 overlap computation. No cannibalization is demonstrated anywhere: no keyword has two HOD URLs ranking (Stage 3/10/11).
- **Downstream.** Stage 15 must check each keyword assignment against these rules.

## D14-28 — The hierarchy is conceptual: no URLs, no redirects, no canonical tags

- **Decision.** Hierarchy paths are written as names ("Education > Lab-Grown Diamonds > …"). The only URLs in Stage 14 files are existing HOD URLs from the Stage 10/13 inventory. Stage 14 prescribes no redirects or canonical tags and no deletions. Migration conditions stay as Stage 13 wrote them.
- **Evidence.** Brief; CLAUDE.md website-safety rules.
- **Downstream.** Stage 15.

## D14-29 — An optional paid SERP check would resolve 8 boundaries. It is documented here and was NOT run.

- **Why it would help.** Nine topics or boundaries are INSUFFICIENT_EVIDENCE. A small SERP batch would decide 8 of them with the same 3-URL rule.
- **Endpoint.** `POST /v3/serp/google/organic/task_post` (Standard queue), then free `GET /v3/serp/google/organic/task_get/advanced/{id}`. This is the Stage 8 method.
- **Parameters.** location_code 2840, language_code "en", device "desktop", depth 10, priority normal (1). No optional paid parameters.
- **Keywords (16 tasks):**

| # | Keyword | Decision it would change |
|---|---|---|
| 1 | how are lab grown diamonds made | EDU-LG-04 fold vs separate |
| 2 | are lab grown diamonds worth it | EDU-LG-06 separate vs interim |
| 3 | lab grown diamond clarity chart | CL-023 integrated vs separate |
| 4 | cvd diamond | CVD split revisit (D14-06) |
| 5 | how is diamond formed | EDU-NAT-00 vs EDU-LG-04 ambiguity |
| 6 | igi lab grown diamond | EDU-CERT-03 |
| 7 | gia lab diamonds | GIA section vs page |
| 8 | vs diamond quality | EDU-4C-04 |
| 9 | do lab grown diamonds pass diamond tester | EDU-LG-09 vs moissanite tester |
| 10 | are lab grown diamonds ethical | EDU-LG-07 vs EDU-NAT-02 |
| 11 | do lab grown diamonds hold their value | EDU-LG-05 vs EDU-LG-06 |
| 12 | is 1 carat diamond good | EDU-4C-07 page type |
| 13 | types of diamonds | EDU-GEN-02 sense |
| 14 | ring size chart | EDU-RJG-05 tool vs guide (page type only; volume not in the DB) |
| 15 | diamond hardness | EDU-GEN-01 page type |
| 16 | simulated diamond | EDU-GEM-00 page type |

- **Estimated maximum cost.** 16 × $0.0006 = **$0.0096** at the Stage 8 verified normal-priority rate. Pricing must be re-verified via the free `appendix/user_data` before any run.
- **Status.** NOT executed and NOT authorised. It can be bundled with the unapproved D-19 commercial supplement. The Stage 14 architecture stands without it: every affected topic is already marked CONDITIONAL or provisional with an interim home.

## D14-30 — FAQ relationship

- **Decision.** The FAQ names the Education owner for every topic it touches:
  - legitimacy → EDU-LG-01
  - lab vs natural → EDU-LG-02
  - certification → EDU-CERT-00 / EDU-CERT-01
  - resizing → EDU-RJG-02 for the general explanation; the HOD resizing policy stays on the FAQ
- **Evidence.** Stage 10 OV-10; Stage 12 D-18.
- **Downstream.** Stage 15/16.
