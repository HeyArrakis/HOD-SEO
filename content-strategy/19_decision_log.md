# Stage 19 — Decision log (content briefs)

Date: 2026-09-25. Scope: brief construction only. No DataForSEO or other API call, no live-site request, **$0.00**. No Stage 14–18.5 file was edited. Stage 15 keyword ownership, Stage 16 links, Stage 14 architecture and all 28 ranking-equity protections are unchanged.

Each entry gives the decision, the evidence and whether it resolves a conflict between sources. Conflicts are **recorded, not silently resolved**.

---

## A. Source conflicts (recorded, not resolved by Stage 19)

### C19-01 — `engagement ring settings`: Stage 15 owner vs 18.5 SERP (CONFLICT)
- **Stage 15:** the settings cluster (CL-121) is owned by EDU-RJG-01 (Education article).
- **18.5 (CL185-117):** the head-term SERP is MIXED and commercial-led: shop pages (Kesslers, Friendly Diamonds, Robbins Brothers "setting only", KayOutlet Design-A-Ring), popular products, a local pack and a shopping-oriented AI Overview. CL185-121 adds "setting only / no stone" transactional demand.
- **Stage 19 treatment:** the EDU-RJG-01 brief is marked `OWNERSHIP_REVIEW_REQUIRED` in `19_brief_registry.csv`. The Education guide stays useful for informational setting intent (`types of diamond settings` is validated EDITORIAL_GUIDE in Stage 8). The brief is written for that intent, with no shop framing, product listings or prices. Commercial ownership of the head term needs a separate decision. It depends on a business fact: whether HOD sells settings without a centre stone (`19_business_fact_requirements.csv`).
- **Not done:** no second owner, no Stage 15 change, no IA change.

### C19-02 — Stage 18 boundary rows ask for a link that Stage 16 does not define
Stage 18 `current_page_treatment` says "link to the owner" for every OWNED_ELSEWHERE concept. Stage 16 is authoritative for links, so where it has no contextual relationship the brief says **mention only (no contextual link)**. Stage 19 adds no link.

**16 pairs with no Stage 16 link (mention only):**

| Page | Owner | Concept |
|---|---|---|
| EDU-LG-01 | EDU-LG-05 | Price relative to natural |
| EDU-LG-02 | EDU-LG-09 | Can you tell them apart / identification |
| EDU-LG-02 | EDU-LG-08 | Appearance and sparkle parity |
| EDU-LG-02 | EDU-GEN-01 | Durability parity (Mohs 10) |
| EDU-LG-02 | EDU-CERT-00 | Both graded by the same labs (GIA, IGI) |
| EDU-LG-03 | EDU-GEN-01 | Type IIa classification |
| EDU-LG-03 | EDU-LG-01 | Are CVD / HPHT diamonds real |
| EDU-LG-03 | EDU-CERT-00 | Growth-method disclosure on grading reports |
| EDU-LG-05 | SUP-FAQ | HOD buy-back / trade-in / upgrade policy |
| EDU-LG-05 | EDU-CERT-00 | Certificate's role in resale |
| EDU-LG-10 | EDU-LG-05 | Understand resale value before buying |
| EDU-LG-10 | EDU-4C-03 | IF / flawless lab-grown — worth paying for? |
| EDU-4C-01 | EDU-4C-05 | Colour chart cross-reference |
| EDU-MET-00 | EDU-RJG-02 | Resizing by metal |
| COM-ER-SIDESTONE | COM-BESPOKE | Adding side stones / bespoke |
| COM-ER-SIDESTONE | EDU-LG-02 | Natural or lab-grown centre stone |

**5 pairs where only a structural link exists** (breadcrumb or hub list: EDU-LG-00→EDU-LG-05, EDU-LG-01→EDU-LG-00, EDU-4C-00→EDU-4C-03, EDU-4C-05→EDU-4C-00, EDU-CERT-01→EDU-CERT-00). The structural link is treated as sufficient and no contextual link is invented.

**Recommendation (not actioned):** review these pairs in any future Stage 16 revision. The strongest candidates are LG-02→LG-09, LG-02→CERT-00, LG-03→CERT-00 and LG-05→SUP-FAQ.

### C19-03 — 18.5-validated head terms that are absent from the Stage 15 keyword map
Examples: `what are lab grown diamonds`, `4cs of diamonds`, `diamond color chart`, `diamond carat size chart`, `diamond cut`, `diamond shapes`, `diamond certificate`, `14k vs 18k gold`, `white gold vs platinum`, `ring size chart`, `how to measure ring size`, `what are diamonds made of`, `how are diamonds formed`, `engagement ring settings`.

18.5 validated their SERPs and linked each one to a target through the Stage 18 data-gap rows (G18-0282…0295). Stage 19 uses them as **SERP-format evidence only**. The registry notes them per page. It does not add them to `primary_keyword` (that stays the Stage 17 choice), does not assign ownership, and states no volume. A Stage 15 map update is needed before they become owned keywords.

### C19-04 — 18.5 WEAKENED two Stage 18 CRITICAL gaps
- **G18-0116 (lab-grown graded on the same 4Cs, EDU-4C-00): CRITICAL → IMPORTANT.** The head-term SERP does not discuss lab-grown grading. The section is kept (S08, IMPORTANT) because the existing URL is lab-grown framed and the Stage 15 cluster includes lab-grown grading.
- **G18-0254 (resizing, EDU-RJG-02): CRITICAL → IMPORTANT.** Resizing is absent from both ring-size SERPs. It is kept as S08 (IMPORTANT) because Stage 15 maps resizing keywords here and Stage 16 requires the `our resizing policy` link.

### C19-05 — Fluorescence on EDU-LG-08 (G18-0079)
18.5 row CL185-032 is UNCHANGED: fluorescence does not appear on the cloudiness SERP. Stage 18 marked it CRITICAL from owned keywords (`do lab grown diamonds have fluorescence`, a co-primary). Stage 19 keeps it as a core section (S05). The absence from the 18.5 SERP is recorded in the section notes and the X5 control row.

### C19-06 — Price questions vs the Stage 13 "no hard-coded prices" rule
Stage 18 routes several price questions to FAQ on EDU-LG-05 (`average price of a 1 carat lab-grown diamond`, `price of a 2 carat…`) and inline elsewhere. Stage 13 forbids hard-coded prices. The brief keeps the questions because they are owned demand. It requires answers that explain price drivers, or cite a **dated, sourced** figure. No price is supplied in Stage 19.

---

## B. Construction decisions

| ID | Decision | Reason / evidence |
|---|---|---|
| D19-01 | Briefs built for exactly the 27 Stage 15 targets in `15_target_page_registry.csv`. No brief for conditional, deferred, excluded, competitor or noise topics. | Brief §3. Conditional topics (EDU-LG-04, LG-06, 4C-04, CERT-02, MET-02) have no target ID. They are covered only as the Stage 15/18 **interim-home sections** on LG-00, LG-02, 4C-01, CERT-00 and MET-00. |
| D19-02 | Status taxonomy: 12 `EXISTING_PAGE` and 15 `FUTURE_PAGE`, each carrying its Stage 15 status verbatim. There are **0 `CONDITIONAL_PAGE` briefs**: every conditional topic lacks a target ID. `INTERIM` is applied at section level (5 interim-home sections) because no target page is itself interim. | Brief §4 vs Stage 15 taxonomy. |
| D19-03 | Existing pages: every existing-page section carries "BODY_COVERAGE=UNKNOWN. Brief requirement: ensure this is addressed". No claim is made that the current article lacks anything. The existing title and H1 (Stage 10 inventory) are quoted in the registry. | Brief §4; Stage 18 recorded 0 CONFIRMED_MISSING. |
| D19-04 | Outlines were hand-built per page from searcher need, Stage 18 gaps, 18.5 AI Overview section order, Stage 15 ownership and Stage 14 page type. There is no fixed template: the ring-size guide leads with the chart and steps, the category and PDP use category/product blocks, and the 4Cs pillar uses one H3 block per C in the AI Overview order (cut → colour → clarity → carat). | Brief §6. |
| D19-05 | Effective gap weight = Stage 18 severity, adjusted by the 18.5 "Implied weight" notes (28 gaps re-weighted, e.g. G18-0105 kimberlite → CRITICAL, G18-0252/0253 ring-size steps/chart → CRITICAL). Stage 18 files are not edited; the adjusted weight lives only in Stage 19 outputs and `19_build_stats.json`. | 18.5 change log. |
| D19-06 | Every one of the 304 Stage 18 gaps has exactly one home. 293 sit in content sections. 11 sit in control rows: 3 unresolved head-term data gaps (X5), 1 deferred-topic boundary (X5), 4 AVOID gaps (X6), 3 business-only gaps (X4). All effective CRITICAL and IMPORTANT gaps are in content sections. | QC checks 5–6. |
| D19-07 | 18.5 NEW_EVIDENCE rows (34) are attached to the section they inform (for example CL185-069 carat-to-mm chart → EDU-4C-07 S02; CL185-132 accuracy tips → EDU-RJG-02 S04; CL185-025 lack of regulation → EDU-LG-07 S04). One row (CL185-079, non-jewellery senses of "diamond cut") becomes an EXCLUDED boundary. | 18.5 change log. |
| D19-08 | A section's importance = its highest effective weight among the gaps it owns. A brief mention of a concept owned elsewhere can raise a section to IMPORTANT, never to CRITICAL. The four per-C blocks on EDU-4C-00 are IMPORTANT: 18.5 raised G18-0119…0122, and the AI Overview shows one block per C. | Prevents a non-owner from carrying CRITICAL depth on a borrowed concept. |
| D19-09 | Questions: Stage 18 treatment is the default. A question labelled FAQ is answered **inline** when a dedicated section already covers its subject (66 cases). This avoids FAQ blocks that repeat the body. Two questions were moved into an FAQ because no body section fits (for example "Are CVD diamonds worth buying?"). Six planned FAQ sections were dropped because nothing was left for them (EDU-LG-08, 4C-00, 4C-03, SHP-00, CERT-00, MET-00). Result: 14 FAQ sections (one each on 14 pages) holding 23 FAQ-classified questions. Every FAQ section is backed by a Q18/V185 question ref or a Stage 18 FAQ-treatment gap. | Brief §17 "do not create FAQ blocks just for SEO". |
| D19-10 | 18.5 PAA questions were classified by hand (`Q185_CLASS` in `build_19.py`). Celebrity, trivia, budget-advice and styling-rule questions are NOT_NEEDED: Kim Kardashian's ring, the "2:1:1 rule", "$100,000 a year", divorce ring, "1000 times rarer", "poor man's diamond". So are questions owned by another page, such as perception questions on the value, ethics and cloudiness SERPs. Two 18.5 questions duplicated Stage 18 questions and were de-duplicated. | Brief §5F. |
| D19-11 | Three PAA questions Stage 18 had routed as cross-owner inline answers were set to NOT_NEEDED because the page has no relationship with the owner: "worst clarity characteristics" on EDU-4C-05; "VS1 or VS2" on EDU-4C-06 and EDU-RJG-01. | Would add off-topic content with no link path. |
| D19-12 | Entities are labelled MUST_MENTION (Stage 18 REQUIRED), SUPPORTING_ENTITY (owned here), MENTION_BRIEFLY_AND_LINK → owner (a Stage 16 contextual link exists), MENTION_BRIEFLY (no link, or structural only) or OPTIONAL_IF_RELEVANT (Stage 18 MENTION_IF_RELEVANT). 18.5 SERP entities were normalised to Stage 18 names and added when new (62). Eight lexicon hits judged irrelevant were skipped, for example "Natural / mined diamond" and "Round" on the ring-size SERP, and "Carat" on the ethics SERP. | Brief §5G. |
| D19-13 | Formats are taken from 18.5 `content_format_pattern` or Stage 18 SERP patterns and always phrased "SERP evidence suggests…". AEO notes state that no format assures AI Overview inclusion. The carat SERP has **no AI Overview** (image-led), so EDU-4C-07 is chart-first with no AEO claim. | Brief §5I, §7. |
| D19-14 | Visual requirements are set only where evidence exists: 4Cs summary chart (images pack in second position), colour chart (AI Overview chart images), carat-to-mm by shape (images pack in first position), ring-size table (AI Overview table), shape chart with pictures (related search + G18-0190), settings chart (related + G18-0243), clarity chart (G18-0127) and cut chart (G18-0176). The process diagrams on EDU-LG-03 rest on G18-0061 (optional). An annotated sample report on EDU-CERT-00 is marked as an editorial choice without specific SERP evidence. | Brief §8. |
| D19-15 | Comparison tables only where the SERP shows a comparison structure: LG-02, LG-03, 4C-01, 4C-05, SHP-00, CERT-01, MET-00 (white gold vs platinum), MET-01 and RJG-02 (conversions). Table rows use only attributes seen in Stage 18/18.5 evidence. | Brief §5H. |
| D19-16 | Internal links: `19_internal_link_requirements.csv` copies only Stage 16 contextual rows (CONTEXTUAL, RELATED_CONTENT, EDITORIAL, EDUCATIONAL_CTA, COMMERCIAL_CTA, PRODUCT_RECOMMENDATION) that touch a target. That is 168 distinct Stage 16 rows (243 brief-rows, because a link between two targets appears in both briefs). Each row keeps its Stage 16 row reference, anchor, variants and priority. Structural links (breadcrumb/nav) stay as Stage 16 defines them and are not repeated. Placement goes to the section that mentions the target's concept, otherwise to the page's decision or routing section. | Brief §10. |
| D19-17 | Business facts: 30 rows. 4 are BLOCKING: the side-stone assortment, centre-stone/metal options, PDP specifications, and any HOD sustainability-claim wording. The Education pages can all be drafted without HOD facts, so their facts are NON_BLOCKING, but any HOD-specific sentence waits for the fact. | Brief §13–14. |
| D19-18 | Content depth is qualitative (Essential 4, Moderate 16, Comprehensive 7). No word counts. | Brief §15. |
| D19-19 | Titles: only an H1 direction and "working" headings are given. No final SEO titles or meta descriptions. Existing H1s that already match intent are noted as such. | Brief §16. |
| D19-20 | Ranking equity: each of the 27 Stage 3 targeted keywords is quoted in its page's `existing_ranking_equity`. `cvd/hpht diamond tester` (the 28th) stays EXCLUDED, with explicit EXCLUDED boundaries on EDU-LG-03 and EDU-LG-09. Special rules are written into the registry: CVD/HPHT single home, LG-02 comparison strengthened, 14k vs 18k, how-to-choose kept non-commercial, side-stone and PDP URLs preserved. | Brief §11. |
| D19-21 | Extra boundaries (14 rows) record Stage 15/16 rules and 18.5 evidence that the Stage 18 cross-page file did not hold. Examples: the commercial lab-grown head terms reserved for COM-LG-HUB; no separate CVD or HPHT page; the coal myth owned by NAT-00; budget-to-size owned by 4C-07. None creates an owner; each names an existing Stage 14/15/16 page or `EXCLUDED`. | Brief §9. |
| D19-22 | DataForSEO spend is $0. No paid call was essential. The remaining gaps (search volume for the 18.5 head terms, and SERPs for the SI, VVS and clarity heads G18-0284…0286) are recorded as INSUFFICIENT EVIDENCE. They do not change the brief structure. | Brief §22. |
