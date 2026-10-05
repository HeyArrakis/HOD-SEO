# Stage 19 — Content briefs & final content architecture: summary

Date: 2026-09-25. **DataForSEO spend: $0.00** (no API call of any kind). This stage adds no URL, keyword owner, cluster, page, redirect, canonical, sitemap change or internal-link relationship. It contains no article copy, final title or meta description.

## 1. Outputs

| File | Rows | Contents |
|---|---|---|
| `19_brief_registry.csv` | 27 | One row per Stage 15 target. Covers identity, intents, keywords, searcher need, journey, depth, SERP format, MUST/SHOULD requirements, business dependencies, ownership review, ranking equity and H1 direction. |
| `19_content_briefs.csv` | 370 | 208 content sections (heading-level outline) and 162 control rows. Each page has six control rows: MUST COVER, SHOULD COVER, DO NOT DUPLICATE, BUSINESS FACTS REQUIRED, INSUFFICIENT EVIDENCE, NOT NEEDED/EXCLUDED. |
| `19_content_boundaries.csv` | 226 | 66 Stage 18 cross-page rows, 142 OWNED_HERE anchor rows (CRITICAL/IMPORTANT concepts), 4 Stage 18 AVOID rows, and 14 Stage 19 rows from Stage 15/16/18.5 rules (3 EXCLUDED, 1 OWNED_HERE, 10 owned elsewhere or under review). |
| `19_business_fact_requirements.csv` | 30 | HOD facts needed (4 BLOCKING, 26 NON_BLOCKING). |
| `19_internal_link_requirements.csv` | 243 | Incoming and outgoing contextual links. All come from Stage 16 (168 distinct Stage 16 rows). |
| `19_decision_log.md` | — | 6 recorded source conflicts and 22 construction decisions. |
| `scripts/build_19.py`, `scripts/qc_19.py` | — | Build script (hand-authored outlines, plus generators); QC script (28 checks). |
| `scripts/19_upstream_checksums.json`, `19_upstream_qc_baseline.json`, `19_build_stats.json`, `19_build_log.json`, `19_output_checksums.json` | — | Pre-stage snapshot (255 files), upstream QC baseline, build statistics and routing log, output checksums. |

How to read a brief: filter `19_content_briefs.csv` by `target_page_id`. Rows appear in heading order: H1/answer-first, then H2/H3, then FAQ, then the X1–X6 control rows. Page-level context is in the matching `19_brief_registry.csv` row. Links are in `19_internal_link_requirements.csv` and boundaries in `19_content_boundaries.csv`.

## 2. Methodology

1. **Scope.** The 27 targets come from `architecture/15_target_page_registry.csv`, and nothing else.
2. **Gap weighting.** Each Stage 18 gap severity is adjusted by the 18.5 "Implied weight" notes; 28 gaps are re-weighted. Stage 18 files are left unedited.
3. **Outlines.** Each page's outline was written by hand from:
   - the searcher need;
   - the Stage 18 gaps;
   - the 18.5 AI Overview section order (or the Stage 8 AI Overview structure where 18.5 did not cover the page);
   - the Stage 15 ownership;
   - the Stage 14 page type.

   Every one of the 304 Stage 18 gaps has exactly one home: 293 in content sections and 11 in control rows. 33 of the 34 18.5 NEW_EVIDENCE rows are attached to sections. The remaining one (non-jewellery "diamond cut") is an EXCLUDED boundary.
4. **Questions.** 268 Stage 18 question rows and 68 18.5 PAA questions were classified as CORE_SECTION, SUPPORTING_SECTION, INLINE_ANSWER, FAQ, CATEGORY_COPY or NOT_NEEDED, then placed in sections. A question the body already answers is not repeated as an FAQ; 66 FAQ-labelled questions became inline answers.
5. **Entities.** 304 Stage 18 entity rows plus 62 normalised 18.5 SERP entities. Each is labelled MUST_MENTION, SUPPORTING_ENTITY, MENTION_BRIEFLY_AND_LINK, MENTION_BRIEFLY or OPTIONAL_IF_RELEVANT.
6. **Boundaries.** These come from `18_cross_page_semantic_ownership.csv`. The link status of each is checked against Stage 16, which is authoritative.
7. **Links.** Stage 16 contextual rows only, each placed in a section.
8. **Business facts.** These come from Stage 18 BUSINESS_DEPENDENT gaps, the Stage 15 business dependencies and 18.5 evidence (for example "setting only" demand).
9. **Wording.** All requirement text is instructional ("Explain…", "Open with a concise direct answer…"). Formats are stated as "SERP evidence suggests…". There are no volumes, rankings or AI Overview promises.

## 3. Pages briefed: existing vs future

| Status | Count | Pages |
|---|---|---|
| EXISTING_PAGE | 12 | LG-01, LG-02, LG-03, LG-10, 4C-00, SHP-00, CERT-00, CERT-01, MET-01, RJG-02, COM-ER-SIDESTONE, COM-PDP-OVAL-FLORAL |
| FUTURE_PAGE | 15 | LG-00, LG-05, LG-07, LG-08, LG-09, NAT-00, 4C-01, 4C-02, 4C-03, 4C-05, 4C-06, 4C-07, MET-00, RJG-01, GEN-01 (8 of them PROPOSED_PROVISIONAL / URL_PENDING) |
| CONDITIONAL_PAGE | 0 | Conditional topics have no Stage 15 target ID |
| INTERIM (section level) | 5 sections | LG-00 S03 (for LG-04); LG-02 S07 (for LG-06); 4C-01 S05 (for 4C-04); CERT-00 S06 (for CERT-02); MET-00 S05 (for MET-02) |

For the existing pages, body coverage is **UNKNOWN**. The briefs quote the existing title and H1 (Stage 10) and phrase every requirement as "ensure X is addressed".

Content depth: Comprehensive 7 (LG-00, LG-02, LG-03, 4C-00, SHP-00, CERT-00, MET-00), Moderate 16, Essential 4 (4C-02, 4C-03, side-stone category, PDP).

## 4. Major content requirements (MUST COVER highlights)

- **LG-00 (hub pillar):**
  - answer-first definition;
  - alternative names, with the FTC labelling point sourced;
  - an overview of how lab-grown diamonds are made (interim home for LG-04);
  - short "real, not simulants" and "vs mined" summaries that link out;
  - hub routing.
- **LG-01:** a direct yes/no in the opening lines; why a lab-grown diamond is a real diamond; how simulants differ.
- **LG-02:**
  - answer-first summary;
  - an attribute comparison table;
  - what is the same and what differs;
  - price, size for budget and resale;
  - pros and cons (interim home for LG-06);
  - decision framing by buyer priority.
- **LG-03:**
  - a definition-first opening;
  - a key-differences table;
  - HPHT and CVD process sections, which also serve single-method searches;
  - growth shape, inclusions and colour;
  - price difference;
  - a conditional answer to "which is better".
- **LG-05:** direct answers to "cheaper?" and "hold value?"; why they cost less; resale and depreciation (illustrative calculation, no live prices); investment suitability.
- **4C-00:** definition; one block per C, each with its grade range; a summary chart; order of importance.
- **4C-05, 4C-07, RJG-02, SHP-00, RJG-01:** chart-led pages (see §6).
- **MET-00:** types of metal; white gold vs platinum table; best metal by lifestyle.
- **MET-01:** comparison table; purity; colour; durability; price and melt value; decision.
- **CERT-00:** definition vs appraisal; report contents; labs; lab-grown certificates; numbered verification steps.
- **CERT-01:** side-by-side table; grading approach; disclosure; cost; which to choose.
- **Category and PDP:** category copy and product specifications only. There is no article body.

## 5. AEO requirements (answer-first)

Answer-first or definition blocks are required on 21 sections. Each rests on AI Overview or PAA evidence:
- 18.5 AI Overview on 16 of 17 head-term SERPs;
- Stage 8 AI Overview on the LG-01, 02, 03, 09, 10, 4C-01, 02, 03, CERT-01 and side-stone SERPs.

What is specified:
- **Direct yes/no answers:** LG-01, LG-05 value, LG-07 (qualified), LG-08, LG-09.
- **Concise definitions:** LG-00, 4C-00, 4C-01, 4C-02, 4C-03, 4C-05, 4C-06, 4C-07, SHP-00, CERT-00, GEN-01.
- **Conditional verdicts:** LG-03, CERT-01, MET-01.
- **Numbered processes:** ring-size measuring, report verification, SI buying tips, cleaning.
- **Factual lists:** report contents, labs, formation stages.

The carat size-chart SERP has **no AI Overview** and is image-led, so no AEO requirement is set for EDU-4C-07 beyond its definition. SERP evidence suggests these formats; none assures AI Overview inclusion.

## 6. Visual requirements (evidence-backed only)

| Page | Visual | Evidence |
|---|---|---|
| 4C-00 | One summary chart covering all four grading scales | 18.5 images pack in second position; related "4cs of diamonds chart" (CL185-046) |
| 4C-05 | D-to-Z colour chart; five grade groups, each with appearance and value | AI Overview chart images; Tiffany image result (CL185-058) |
| 4C-07 | Carat-to-mm chart by shape; on-hand comparison | Images pack in first position, no AI Overview (CL185-069/070/072) |
| RJG-02 | US size table (inner circumference and diameter in mm); numbered steps; conversions; printable/virtual sizer | AI Overview table and 7 steps; related conversions (CL185-125/129/128/127) |
| SHP-00 | Shape chart with pictures; one trait per shape; characteristics table | AI Overview 10 shapes with traits; related "chart with pictures" (CL185-081/083/085) |
| RJG-01 | Settings chart with pictures | Related "settings chart"; G18-0243 (CL185-120) |
| 4C-01 / 4C-06 | Clarity chart; cut-grade chart; facet anatomy diagram | G18-0127, G18-0176, G18-0173 |
| MET-00 / MET-01 / LG-02 / LG-03 / CERT-01 | Comparison tables | 18.5/Stage 8 comparison structures |

## 7. Cross-page boundaries (key)

| Concept | Owner | Treatment on other pages |
|---|---|---|
| CVD vs HPHT, and single-method CVD/HPHT | EDU-LG-03 | Summary and link from LG-00 and LG-10. No separate CVD or HPHT page. |
| Authenticity ("are lab-grown real") | EDU-LG-01 | One or two lines and a link from LG-00. Mention only from LG-03, which has no Stage 16 link. |
| Lab-grown vs natural | EDU-LG-02 | Summary and link from LG-00, LG-01, LG-03 and NAT-00. Pros and cons live here as the interim home for LG-06. |
| Certification basics | EDU-CERT-00 | Link from LG-01, LG-09, LG-10 and 4C-00. |
| GIA vs IGI | EDU-CERT-01 | Link from CERT-00 only; CERT-00 answers the questions in one line. |
| Price, resale and investment | EDU-LG-05 | Link from LG-02. Mention only from LG-01 and LG-10, which have no link. |
| Commercial lab-grown head terms | COM-LG-HUB (conditional) | Never targeted on Education pages. |

Where Stage 18 asked for a link that Stage 16 does not define (16 pairs), the brief says **mention only**. These pairs are listed for a future Stage 16 review (decision log C19-02).

## 8. Business facts required (30; 4 BLOCKING)

- **BLOCKING:**
  - side-stone category assortment;
  - side-stone centre-stone, metal and carat options;
  - Oval Floral PDP specifications;
  - any HOD sustainability or ethical-claim wording.
- **NON_BLOCKING (the Education content can be drafted now; the HOD-specific statement waits for the fact):**
  - growth method used for HOD stones;
  - energy source;
  - labs grading HOD stones, and whether a report comes per product;
  - buy-back and trade-in;
  - resizing policy;
  - metals and karats offered;
  - alternative metals;
  - settings sold without a centre stone;
  - natural diamond availability;
  - treated-stone disclosure;
  - SI/VVS grade display;
  - loose-stone offer;
  - ring-size tool;
  - dated price sources.

## 9. Ownership review issues

1 issue: **EDU-RJG-01 / `engagement ring settings` — OWNERSHIP_REVIEW_REQUIRED.**
- **Current owner:** EDU-RJG-01 (Stage 15).
- **New evidence:** the 18.5 SERP is MIXED and commercial-led (shops, products, local pack, shopping-oriented AI Overview).
- **Brief approach:** the Education guide is briefed for informational setting intent. Commercial ownership needs a separate decision. No second owner was created.

## 10. Ranking-equity protections (28/28)

- All 27 targeted Stage 3 keywords are quoted in their page's registry row with URL unchanged:
  - LG-03: 18 keywords;
  - LG-02: 3;
  - MET-01: 3;
  - LG-10: 1;
  - side-stone category: 1;
  - PDP: 1.
- `cvd/hpht diamond tester` (the 28th) keeps its URL but stays **excluded from targeting**, with EXCLUDED boundaries on LG-03 and LG-09.
- Special rules are written into the registry:
  - LG-03 stays the single CVD/HPHT home and gains single-method depth;
  - LG-02 comparison intent is strengthened;
  - LG-10 does not take engagement-ring commercial ownership;
  - the side-stone and PDP URLs are preserved, including the `by-desgin` path.

## 11. Unresolved issues

1. **Commercial ownership of `engagement ring settings`** (C19-01).
2. **16 Stage 18 boundaries with no Stage 16 link** (C19-02). These are candidates for a Stage 16 revision.
3. **18.5 head terms not in the Stage 15 map** (C19-03). Their volumes are unmeasured, and the 36-term `keyword_overview` supplement from Stage 17 is still unapproved.
4. **SERPs never validated for the SI, VVS and clarity head terms** (G18-0284…0286). Their format rests on the Stage 8 SERPs for `si2 diamond`, `v v s diamond` and `diamond clarity grading scale`.
5. **30 business facts**, 4 of them blocking.
6. **Primary keywords with LOW Stage 17 confidence:** LG-00, LG-07, LG-08, 4C-00, 4C-05, 4C-07, RJG-02.
7. **URL_PENDING targets** (8) cannot have final titles until URLs are set.

## 12. QC

`python3 content-strategy/scripts/qc_19.py` runs 28 checks. The result is reported in `progress.md` and in the final report.

The upstream QC scripts were re-run:
- The pre-Stage-19 failures are unchanged (they are recorded in `19_upstream_qc_baseline.json`).
- The only new failures are the expected point-in-time "no Stage 19 brief exists" checks: qc_17 #14, qc_18 #25 and qc_18_5 #25. The qc_18_5 #29 chain check also fails, because it sees qc_18 #25.

## 13. Stage 20 recommendation (not started)

Suggested next steps, all awaiting approval:
- a user decision on the RJG-01 ownership review and the business-fact list;
- a light Stage 15/16 maintenance pass to add the 18.5 head terms (after a volume check) and the recommended boundary links;
- an existing-page body audit for the 12 existing URLs, so that "ensure X" can become a confirmed gap list.

Only after that should writing begin, starting with the BLOCKING-free Education pages.
