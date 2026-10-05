# Stage 15 — Keyword → URL mapping: decision log

Date: 2026-09-24. Local project files only: no DataForSEO call, no other API call, no live-site request, $0 spend.

Decision IDs are D15-01 to D15-16. Earlier decisions are cited as D-xx (Stage 12), D14-xx (Stage 14), OV-xx (Stage 10 overlaps) and REL-xxx (Stage 11 relationships). Every count in this log comes from the Stage 15 CSVs, which `architecture/scripts/build_15.py` regenerates.

---

## D15-01 — Mapping principles and order of precedence

- **Decision.** Every Stage 7 keyword gets exactly one row and one disposition from a fixed list of 11. The disposition is decided in this order:
  1. The Stage 11 status: NOISE, COMPETITOR_BRAND or UNCLUSTERED_REVIEW.
  2. An explicit keyword-level override. There are 72 overrides, each with its own reason in `build_15.py` (`KW` rules) and in the `reason` column.
  3. The Stage 14 PRIMARY decision for the keyword's cluster. The Stage 14 SECONDARY rows supply interim homes and sub-topic splits.
- **Rules applied.** One searcher need has one owner (Stage 14 rule 1). A cluster is not a page (rule 5). Volume never creates a page (rule 4). Informational owners never take a query whose validated SERP is CATEGORY, PRODUCT or BRAND (rule 3). Existing ranking URLs keep their keywords (rule 7). Conditional and deferred topics get no production URL (rule 8).
- **Evidence.** Stage 7 (universe), Stage 11 (cluster and status), Stage 14 consolidation (112 rows).
- **Result.** 1,936 rows: 659 mapped to an owner, 267 held (conditional or deferred), 854 excluded, 156 for review.

## D15-02 — What each disposition means

| Disposition | Used when |
|---|---|
| MAP_EXISTING_URL | An existing URL owns the need now. Stage 13 plans a move or retarget, but only when its conditions are met, with a 1:1 301. `target_url` is the **current** URL. |
| MAP_EXISTING_URL_KEEP | An existing URL owns the need and stays at its current URL. This covers DO_NOT_MOVE_NOW, update in place, deferred migration, and commercial URLs that are kept. |
| MAP_PROPOSED_URL | A Stage 14 PROPOSED or PROPOSED_PROVISIONAL resource that does not exist yet. |
| MAP_INTERIM_HOME | The primary topic is CONDITIONAL and Stage 14 names an interim home (a SECONDARY row). |
| CONDITIONAL_NOT_MAPPED | The owner is CONDITIONAL. That includes the commercial Lab-Grown hub and Earrings > Studs from Stage 12. |
| DEFERRED_NOT_MAPPED | The owner is DEFERRED: an Education topic, a Stage 12 commercial page marked INSUFFICIENT EVIDENCE — DEFER, or Blog content with no article planned. |
| EXCLUDE_COMMERCIAL | Commercial intent with no HOD destination: not in the catalogue, NOT_PROPOSED in Stage 12, or a non-indexable filter. |
| EXCLUDE_NOISE / EXCLUDE_COMPETITOR_BRAND | Stage 7/11 status, plus one competitor found here ('is 6 ice jewelry real'). |
| EXCLUDE_OFF_SCOPE | No jewelry need (CL-084, CL-114), or navigation to a third-party grading lab. |
| REVIEW_REQUIRED | Ambiguous. Needs SERP evidence or a business answer. |

## D15-03 — Target IDs and URL expressions

- **Decision.**
  - Education targets use the Stage 14 topic ID, for example `EDU-LG-03`. Commercial targets use `COM-…` IDs.
  - `target_url` holds the existing URL, or a proposed URL expression, or is blank when the slug is `URL_PENDING`.
  - `target_url_status` is one of `EXISTING_KEEP`, `EXISTING_MOVE_WHEN_CONDITIONS_MET`, `EXISTING_RETARGET_THEN_MOVE`, `PROPOSED_URL`, `URL_PENDING` or `NONE`.
- **URL expressions (Stage 12 D-12 principles).** These follow the pattern `/education/{hub}/{topic}`: lowercase, hyphenated, plural where the page is a listing, no IDs, no brand suffix, at most three segments. US spelling is used where the keywords use it (`diamond-color`; D-15 inference).
  - Hubs: `/education/lab-grown-diamonds`, `/education/diamond-4cs`, `/education/diamond-shapes`, `/education/diamond-certification`.
  - Children: `/education/diamond-4cs/{diamond-clarity, si-clarity-diamonds, vvs-diamonds, diamond-color, diamond-cut}`, and `/education/lab-grown-diamonds/are-lab-grown-diamonds-real` as the future home of the existing are-real article.
- **URL_PENDING (13 targets).**
  - Every PROPOSED_PROVISIONAL topic, because low evidence means the lead keyword and scope may still change.
  - The Ring & Jewellery Guides and Metals children, because the hub label and its "jewellery"/"jewelry" spelling are open (D-15) or the hub is provisional.
  - EDU-LG-10, whose migration is deferred.
  - The side-stone subcategory's future path.
- **Not decided.** The platform (D-17). A native Shopify build would express the same owners as `/blogs/…` or `/pages/…`. The owner does not change; only the path does.
- **Evidence.** Stage 12 D-09, D-12, D-15, D-17. Stage 14 D14-28 (the hierarchy was conceptual; Stage 15 translates it).

## D15-04 — Existing ranking equity: every Stage 3 URL is kept

- **Decision.** All 28 Stage 3 ranking keywords are in `content-strategy/15_ranking_equity_protection.csv`. All 6 ranking URLs are kept at their current address:
  - **27** keywords map to the URL they rank on (`KEEP_EXISTING_URL`).
  - **1** keyword, `cvd/hpht diamond tester` (pos 68), is `KEEP_EXISTING_URL_NOT_TARGETED`. The URL is untouched, but the keyword is EXCLUDE_COMMERCIAL: its validated SERP is CATEGORY (tester shopping), Stage 13 classed it MISALIGNED, and Stage 14 rule 3 forbids an informational page from targeting it. No other page targets it either.
- **No move is triggered by Stage 15.**
  - CVD vs HPHT and lab-vs-natural remain DO_NOT_MOVE_NOW (Stage 13), with all conditions preserved.
  - 14k vs 18k moves only when the Metals section exists.
  - how-to-choose stays deferred.
  - The side-stone subcategory and the PDP have no migration recommended.
- **Evidence.** Stage 3 (via Stage 7 columns), Stage 13 ranking equity and migration risk, Stage 14 D14-26.

## D15-05 — CVD, HPHT and CVD-vs-HPHT: one existing URL (EDU-LG-03)

- **Decision.** All 29 keywords containing "cvd" or "hpht" that are mapped go to the existing CVD-vs-HPHT article: CL-016 (14), CL-017 (7) and CL-018 (8). It also takes 2 CL-015 keywords as an interim home for method wording ('lab grown diamond(s) methods'). No CVD or HPHT page exists in the registry.
- **Evidence.**
  - Stage 14 D14-06: the HPHT head SERP is led by comparison pages (4 of 9), and single-method CVD SERPs share 3 to 4 URLs with the comparison SERPs.
  - Stage 3: 18 of the article's 19 rankings are in these clusters, including both HPHT 8,100 variants at pos 49.
  - Stage 13: HIGH migration risk.
- **Note.** 'cvd diamond' (3,600, TRANSACTIONAL label, unvalidated) is mapped here at LOW confidence. The D14-06 revisit condition for a CVD-only page is recorded in `notes`.
- **Special check.** `SPECIAL_CVD_HPHT_NO_NEW_PAGE` passes.

## D15-06 — Lab-grown vs natural (EDU-LG-02) and "are they real?" (EDU-LG-01)

- **Decision.**
  - All 31 CL-011 keywords go to the existing lab-vs-natural URL (MAP_EXISTING_URL_KEEP).
  - The 21 CL-012 "worth it" keywords use the same URL as their **interim home** (MAP_INTERIM_HOME), because EDU-LG-06 is CONDITIONAL (D14-09).
  - The 17 CL-010 authenticity keywords go to the existing are-real blog URL (MAP_EXISTING_URL). That URL moves to Education only when the Lab-Grown hub exists.
- **Boundary.** 'do lab-grown diamonds look real' is appearance (EDU-LG-08), and 'do lab grown diamonds test real' is detection (EDU-LG-09), not authenticity (D14-07, D14-13). No comparison-worded keyword ("vs", "difference", "better") sits on EDU-LG-01.
- **Evidence.** REL-020 (max 2 shared URLs), Stage 8 COMPARISON SERPs for both, Stage 13 DO_NOT_MOVE_NOW for lab-vs-natural.

## D15-07 — Commercial vs informational boundary

- **Decision.**
  - The commercial members of the clusters that Stage 14 excluded as commercial never map to Education: CL-001, CL-006, CL-063, CL-070, CL-071, CL-104, CL-105, CL-120, CL-123 and CL-125. The only members of these clusters that reach Education are plainly informational ones: 8 CL-070/CL-071 members go to the Natural pillar through the Stage 14 SECONDARY rows (for example 'natural untreated diamond' and 'how raw diamond look like'), and 4 CL-125 members follow D15-10.
  - They map to a commercial page only where Stage 12 already defines one that exists: the side-stone subcategory (CL-120) and the ranking PDP ('marquise oval diamond'). Otherwise they are held as follows:
    - **CONDITIONAL_NOT_MAPPED:** CL-001, which goes to the conditional commercial Lab-Grown hub (D-05), and CL-125 studs (Earrings > Studs is PROPOSED_CONDITIONAL).
    - **DEFERRED_NOT_MAPPED:** CL-006 (loose/carat pages), CL-007 (wholesale), CL-063 (shape landings, D-08), CL-070 (Natural hub, D-05) and CL-123 (Fine Jewellery > Rings).
    - **EXCLUDE_COMMERCIAL:** CL-005 (location pages NOT_PROPOSED), CL-071 (rough-diamond selling), CL-104 and CL-105 (gemstone rings NOT_PROPOSED).
  - Inside informational clusters, keywords with an explicit shopping or product meaning are pulled out at keyword level:
    - 'lab grown diamonds clearance' and 'affordable lab created diamonds' go to the conditional Lab-Grown hub.
    - Tester products, ring enhancers, tungsten and iridium rings, '10 kt rings' and 'diamond grading kit' are EXCLUDE_COMMERCIAL.
    - 'asscher cut diamond' (inventory-led SERP per D14-17) and 'asscher diamond' (validated BRAND) are DEFERRED_NOT_MAPPED. The Shapes pillar covers asscher as a section but does not target these queries.
- **Check.** `SPECIAL_NO_COMMERCIAL_SERP_ON_EDUCATION` passes: no validated CATEGORY, PRODUCT or BRAND keyword sits on an Education target.
- **Not done.** Keywords with a DataForSEO TRANSACTIONAL label but no validated SERP were **not** moved out of informational owners on the label alone. For example, 'gia lab diamonds' 2,400 and 'hpht lab created diamonds' 880 stay with their Stage 14 owners at LOW confidence, with a note in `notes`. Stage 11 and Stage 14 assigned their intent, and a SERP check (D14-29 #7) would settle it.

## D15-08 — 4Cs and clarity

- **Decision.**
  - EDU-4C-00 (existing 4Cs article, becoming the pillar) takes CL-040's general scale and chart queries, CL-048's colour+clarity combinations, and CL-023's lab-grown grade charts. There is no lab-grown 4Cs target (D14-15).
  - The CL-040 members containing "clarity" go to EDU-4C-01, the clarity guide. The reason is Stage 14's own flag: the 'diamond clarity grading scale' (12,100) SERP returns clarity pages.
  - The CL-023 VVS members go to EDU-4C-03 (the Stage 14 SECONDARY row).
  - SI (CL-041) goes to EDU-4C-02 and VVS/IF/FL (CL-043) to EDU-4C-03.
  - VS (CL-042) goes to the clarity guide as an interim home (EDU-4C-04 is CONDITIONAL).
- **Grade comparisons (CL-044, D14-14).**
  - A comparison inside one grade family goes to that family's page: IF vs FL and VVS vs flawless go to EDU-4C-03, and vs1 vs vs2 goes to the clarity guide as an interim home.
  - A comparison across families (VS vs SI, VS vs VVS) goes to the clarity guide.
- **Check.** `SPECIAL_CLARITY_FOLLOWS_STAGE14` passes. No page exists merely because a keyword contains "best", "vs", "chart" or "grade".

## D15-09 — Keyword-level split inside CL-048 (flagged)

- **Decision.** CL-048's primary owner is EDU-4C-00. Two members, 'vs and vvs diamond' and 'vvs vs diamond' (260 each), contain no colour grade and only compare clarity grades, so they follow the CL-044 rule and go to EDU-4C-01. EDU-4C-01 is not a Stage 14 PRIMARY or SECONDARY topic for CL-048, so check C flags it (REVIEW) for visibility.
- **Rationale.** The searcher need (VS vs VVS clarity) is the clarity guide's need. Keeping the keywords on the pillar would split one need across two pages.

## D15-10 — Informational members of the commercial stud cluster (CL-125) (flagged)

- **Decision.** Stage 14 excluded CL-125 as commercial. Its shopping head ('lab diamond studs', 1,000) is CONDITIONAL_NOT_MAPPED. Four 10-volume keywords are plainly informational:
  - The two carat-size questions go to the carat guide (EDU-4C-07), because they are the CL-049 "is X carat good/too small" need.
  - The two stud-setting questions go to the settings guide (EDU-RJG-01).
  - 'can you turn diamond earring into ring' (validated OTHER) is REVIEW_REQUIRED, because it may be a Bespoke/service question.
- **Rationale.** Stage 14 rule 9 stops Education from absorbing *commercial* intent. It does not require informational questions to be dropped because of the cluster they landed in. Check C flags these targets (REVIEW) for visibility.

## D15-11 — Shapes: one pillar, no per-shape pages

- **Decision.**
  - EDU-SHP-00 (the existing shapes article, becoming the pillar) takes 'diamond shape' (60,500, EDITORIAL_GUIDE), CL-064, 'radiant diamond', 'radiant diamond ratio', and the asscher and radiant comparison questions.
  - Inventory-led, brand or shape×origin shopping queries are held as deferred commercial (D15-07).
  - 'moval vs oval diamond' is REVIEW_REQUIRED: it is comparison wording inside CL-063, which Stage 14 excluded as commercial.
- **Evidence.** D14-17. Only the asscher SERP was measured, so 'radiant diamond' (3,600, unvalidated) is mapped at MEDIUM confidence and may prove inventory-led too.
- **Check.** `SPECIAL_NO_PER_SHAPE_PAGES` passes.

## D15-12 — Certification

- **Decision.**
  - The general certification need (CL-033) and the GIA and IGI report questions (CL-031 and CL-032, as sections) go to the existing IGI blog URL, which Stage 13 retargets to become the Certification pillar (`EXISTING_RETARGET_THEN_MOVE`).
  - The informational CL-034 members use the same URL as an interim home (EDU-CERT-02 is CONDITIONAL).
  - The third-party lab lookup and navigation queries (AGS, GCAL, GSL, EGL, "national diamond lab") are EXCLUDE_OFF_SCOPE.
  - GIA vs IGI (CL-030) stays on the existing Education article (MAP_EXISTING_URL_KEEP).
  - There is no IGI-only target (`SPECIAL_NO_IGI_ONLY_PAGE` passes).
- **Dependency.** The retarget and the GIA-vs-IGI narrowing must ship together (Stage 13), or OV-01 persists.

## D15-13 — Conditional, deferred and interim handling

- **Decision.** Conditional and deferred topics receive no target URL. Their keywords carry `stage14_topic_id` so the mapping is recoverable once a topic is approved.
  - **Interim homes (56 keywords):**
    - CL-012 → EDU-LG-02
    - CL-015 → EDU-LG-00 (general process) or EDU-LG-03 (method wording)
    - CL-034 → EDU-CERT-00
    - CL-042 and the VS-family comparison → EDU-4C-01
    - CL-111 → EDU-MET-00
  - **Conditional (140).** Commercial Lab-Grown hub, studs, fancy colour, types of diamonds, conflict-free sourcing, natural value/investment, moissanite comparisons, simulants/CZ, and care.
  - **Deferred (127).** Moissanite, gemstones, engagement-ring buying questions (pending D-19), deferred commercial pages, and Blog-only topics. The Blog-only topics are CL-014 trend and future terms and CL-026 industry/factory terms; Stage 13 starts the Blog from zero, so no Blog article exists to map them to.
- **Evergreen history.** The CL-014 history facts go to the Lab-Grown pillar as a short section (the Stage 14 SECONDARY row).
- **Rule.** When a conditional page is approved, its interim keywords move to it and the interim section shrinks to a summary plus a link (D14-27 rule 7).

## D15-14 — Cannibalization findings

- **A (many→one).** Expected. The largest owners are EDU-GEN-01 (74), EDU-CERT-00 (53), EDU-LG-02 (52, including 21 interim) and EDU-LG-00 (49).
- **B (one keyword→many URLs).** None. One row per keyword with one target, and no spelling or plural variant is split across two targets. One inherited status inconsistency: 'lab-grown melee diamonds' is Stage 7 NOISE while 'lab grown melee diamonds' is in CL-007. Neither has a URL, so it is recorded and not changed.
- **C (one cluster→many targets).** Six clusters. CL-015, CL-023, CL-040 and CL-044 split exactly along Stage 14 SECONDARY rows. CL-048 and CL-125 use keyword-level rules (D15-09, D15-10).
- **D (existing ranking vs proposed).** 27 of 28 keywords map to the URL they rank on. 1 is not targeted (D15-04). No proposed page targets a ranking keyword.
- **E (adjacent owners).** 12 pairs, carried forward from the D14-27 risk register for the targets that own keywords.
  - The one HIGH pair is the process split between the Lab-Grown pillar and CVD vs HPHT. It becomes a real risk only if EDU-LG-04 is created.
  - The MEDIUM pairs:
    - authenticity ↔ comparison
    - worth-it (interim) ↔ price/value
    - 4Cs pillar ↔ clarity guide (lab-grown clarity-chart queries)
    - certification pillar ↔ GIA vs IGI
    - cut ↔ shapes
    - appearance ↔ authenticity
    - Lab-Grown pillar ↔ the conditional commercial hub
- No cannibalization is demonstrated. No keyword has two HOD URLs ranking (Stage 3/10/11).

## D15-15 — Paid research: not run, and what it would change

- **Status.** Not run and not authorised. That covers the Stage 14 D14-29 SERP batch (16 tasks, max $0.0096) and the Stage 12 D-19 commercial supplement. Stage 15 is complete without them.
- **What D14-29 would change in this map:**
  - It would confirm or move the 2 method keywords and 16 process keywords (CL-015) from interim homes, depending on whether EDU-LG-04 is created.
  - It would confirm or move the 21 CL-012 worth-it keywords.
  - It would move CL-023 clarity-chart keywords from EDU-4C-00 to EDU-4C-01 if Google does not separate them.
  - It would settle the confidence of 'gia lab diamonds', 'cvd diamond' and 'is 1 carat diamond good'.
  - It would settle the sense of 'types of diamonds' (CL-065).
- **What D-19 would change.** It would supply the commercial keywords that no commercial hub currently owns, and resolve EDU-LG-10 ↔ EDU-RJG-04.
- **Why it is not needed now.** Each affected keyword is already held as CONDITIONAL, DEFERRED, INTERIM or LOW confidence. Nothing is forced onto a URL.

## D15-16 — Unresolved decisions (carried forward)

1. Platform and path expression (D-17). All proposed URLs are expressions.
2. "Jewellery" vs "jewelry" (D-15). This blocks the Ring & Jewellery Guides and Metals slugs.
3. The Provisional-topic slugs (9 targets are URL_PENDING).
4. Whether to change existing suffixed or misspelled slugs (GIA-vs-IGI; `/by-desgin/` side-stone). Stage 15 does not recommend a stand-alone change. A change belongs to an implementation migration with 1:1 301s.
5. 156 REVIEW_REQUIRED keywords, led by 'diamond stone' 18,100 (dual meaning).
6. The business questions from Stage 12: whether HOD sells natural diamonds, moissanite, gemstones or loose stones; wholesale; and a sourcing policy for conflict-free content. These gate the conditional and deferred owners.
7. A commercial Lab-Grown hub is conditional. Until it exists, 'lab grown diamonds' (135,000) and 'lab diamonds' (27,100) have no HOD owner. They must not be given to the Education pillar (D14-05).
