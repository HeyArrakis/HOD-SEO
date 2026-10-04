# Stage 18.5 — Targeted SERP validation: semantic supplement

Date: 2026-09-25. This is an **evidence supplement to Stage 18**. It does not edit any Stage 18 file, change Stage 14 architecture, Stage 15 keyword/URL ownership or Stage 16 links, and it creates no page and no content brief. Changes to Stage 18 assumptions are recorded in `18_5_stage18_change_log.csv` for Stage 19 to apply.

## 1. Methodology

1. **Authentication and price.** `GET /v3/appendix/user_data` (free) returned 20000 after the credentials were fixed. The account price table gives SERP `task_post` at normal priority as **$0.0006 per task**. `task_get` is free. Balance before submission: $49.853896.
2. **Cost gate.** The user approved exactly 17 tasks × $0.0006 = **$0.0102** maximum.
3. **Execution.**
   - One `POST /v3/serp/google/organic/task_post` carrying the 17 tasks (location 2840, language en, depth 10, desktop, priority 1 = normal, no optional paid parameters, no clickstream, tag `hod_stage18_5`).
   - The response reported `cost 0.0102`, `tasks_error 0`.
   - The results were retrieved with 17 free `GET task_get/advanced/{id}` calls; every task returned 20000 with `result_count 1`.
4. **Spend check.** Balance after all calls: $49.843696. The difference is exactly $0.0102.
5. **Raw preservation.** `dataforseo/raw/18_5_stage_serp/` holds:
   - the verbatim `task_post` response;
   - 17 verbatim `task_get` responses, recovered unmodified from the session transcript / client tool-result files by `extract_from_session.py` (sources listed in `_raw_sources.json`);
   - `manifest.csv`;
   - `_account_balance_check.json`.

   Stage 8 raw files were not touched.
6. **Analysis.** `scripts/build_18_5.py` reads only these 17 files and the Stage 18 outputs.
   - **Features:** AI Overview, PAA, shopping (popular products / product considerations), video (video / short videos), images, local pack, featured snippet. They are read from the SERP item types.
   - **Topics:** AI Overview headings and bolded terms.
   - **Entities and attributes:** fixed lexicons applied to the AI Overview, organic titles/snippets and PAA.
   - **Intent and page type:** a documented reading of the actual SERP, in Stage 8 vocabulary.
   - **Traceability:** every change-log row cites a verbatim evidence token that QC re-checks against the raw SERP.
7. **Wording.** Format signals are stated as "SERP evidence suggests…". Nothing here claims that any format makes AI Overview inclusion certain. No search volume was requested or is stated.

## 2. Exact queries (17)

`what are lab grown diamonds`; `do lab grown diamonds hold their value`; `are lab grown diamonds ethical`; `do lab grown diamonds get cloudy`; `how are diamonds formed`; `4cs of diamonds`; `diamond color chart`; `diamond carat size chart`; `diamond cut`; `diamond shapes`; `diamond certificate`; `14k vs 18k gold`; `white gold vs platinum`; `engagement ring settings`; `ring size chart`; `how to measure ring size`; `what are diamonds made of`.

## 3. Cost

| Item | Value |
|---|---|
| Verified price | $0.0006 / task (task_post, normal priority) |
| Approved maximum | $0.0102 |
| Actual (task_post response) | **$0.0102** |
| Actual (balance delta) | **$0.0102** |
| task_get retrieval | $0.00 |

Cumulative project spend: $0.33536 + $0.0102 = **$0.34556**.

## 4. Results overview

| Query | Stage 15 owner | Intent | Page type | AIO | PAA | Shopping | Video | Images | Local |
|---|---|---|---|---|---|---|---|---|---|
| what are lab grown diamonds | EDU-LG-00 | INFORMATIONAL | EDITORIAL_GUIDE | Y | Y | – | Y | Y | – |
| do lab grown diamonds hold their value | EDU-LG-05 | INFORMATIONAL | EDITORIAL_GUIDE | Y | Y | – | – | – | – |
| are lab grown diamonds ethical | EDU-LG-07 | INFORMATIONAL | EDITORIAL_GUIDE | Y | Y | – | – | – | – |
| do lab grown diamonds get cloudy | EDU-LG-08 | INFORMATIONAL | EDITORIAL_GUIDE | Y | Y | – | – | – | – |
| how are diamonds formed | EDU-NAT-00 | INFORMATIONAL | EDUCATIONAL | Y | Y | – | Y | Y | – |
| 4cs of diamonds | EDU-4C-00 | INFORMATIONAL | EDUCATIONAL | Y | Y | – | – | Y | – |
| diamond color chart | EDU-4C-05 | INFORMATIONAL | EDITORIAL_GUIDE | Y | Y | – | – | – | – |
| diamond carat size chart | EDU-4C-07 | INFORMATIONAL | EDITORIAL_GUIDE (image-led) | **N** | Y | – | Y | Y | – |
| diamond cut | EDU-4C-06 | INFORMATIONAL | EDITORIAL_GUIDE (meaning mixed) | Y | Y | Y | Y | – | – |
| diamond shapes | EDU-SHP-00 | INFORMATIONAL | EDITORIAL_GUIDE | Y | Y | Y | – | – | – |
| diamond certificate | EDU-CERT-00 | INFORMATIONAL | MIXED | Y | Y | Y | – | Y | – |
| 14k vs 18k gold | EDU-MET-01 | INFORMATIONAL | COMPARISON | Y | Y | Y | – | Y | – |
| white gold vs platinum | EDU-MET-00 | INFORMATIONAL | COMPARISON | Y | Y | – | Y | Y | – |
| engagement ring settings | EDU-RJG-01 | **MIXED** | **MIXED** | Y | Y | Y | – | Y | **Y** |
| ring size chart | EDU-RJG-02 | INFORMATIONAL | EDITORIAL_GUIDE | Y | Y | – | – | – | – |
| how to measure ring size | EDU-RJG-02 | INFORMATIONAL | EDITORIAL_GUIDE | Y | Y | – | Y | – | – |
| what are diamonds made of | EDU-GEN-01 | INFORMATIONAL | EDUCATIONAL | Y | Y | – | Y | – | – |

Totals: AI Overview 16/17, PAA 17/17, shopping units 5/17, video 7/17, images 8/17, local pack 1/17, featured snippet 0/17.

## 5. Intent and page types

- **16/17 informational.** The only exception is `engagement ring settings`, which is **MIXED/commercial-led**:
  - shop pages (Kesslers, Friendly Diamonds, Robbins Brothers "setting only", KayOutlet Design-A-Ring);
  - a local pack and popular products;
  - an AI Overview section "Shopping for Settings" with a price range.

  Editorial guides (Brilliant Earth, Tiffany, Blue Nile, VRAI) rank below them.
- **`diamond certificate` is MIXED.** The labs' own pages rank first (IGI homepage, GIA grading-service page), then editorial guides. The shopping unit is Etsy "certificate" listings, which is irrelevant.
- **`diamond cut` is informational, but the meaning is mixed.** It covers cut quality (GIA cut scale, Tiffany cut grades, Blue Nile grading scale) and shape lists ("Top 10 Diamond Cuts", "Shapes & Cuts"). Non-jewellery senses (grillz, vegetables) appear in related searches.
- **`diamond carat size chart` has no AI Overview.** It is image-led (images pack at rank 1, short videos). Every organic result is a carat-to-millimetre chart.

## 6. AI Overview patterns (semantic structure, not copied text)

| Query | Pattern |
|---|---|
| what are lab grown diamonds | definition → composition & properties (same carbon lattice, same 4Cs, lab-certified) → how made (HPHT, CVD) → key differences from mined (origin, cost, not fakes) |
| do … hold their value | direct "No" → resale & depreciation (low resale, falling prices, thin secondary market) → absolute vs percentage loss → why buy anyway / not an investment |
| are … ethical | qualified "Yes" → ethical benefits (no mining risks, conflict-free, labour) → concerns (energy use, fossil-fuel grids, lack of regulation) → how to buy responsibly |
| do … get cloudy | direct "No" → why it may look cloudy (surface buildup, inclusions, poor cut, simulant confusion) → how to restore sparkle |
| how are diamonds formed | natural formation (mantle depth, heat/pressure, time, kimberlite) → lab-grown formation (HPHT, CVD) |
| 4cs of diamonds | definition (GIA standard) → Cut → Color → Clarity → Carat, each "what it means + grade range" → which C to prioritise |
| diamond color chart | chart images → D-to-Z definition → five groups (appearance + value) → fancy-colour boundary → metal/shape prompt |
| diamond cut | definition (light performance) → cut vs shape → quality factors (brilliance, fire, scintillation, proportions) → popular shapes |
| diamond shapes | definition → 10 shapes with one trait each → prompts (jewellery type, brilliant vs step cut, budget) |
| diamond certificate | definition → what is included (4Cs, measurements, polish, symmetry, fluorescence, origin, laser inscription) → top labs (GIA, IGI, AGS) |
| 14k vs 18k gold | purity → colour → durability & wear → price & value → hypoallergenic |
| white gold vs platinum | composition → price → maintenance (rhodium vs patina) → skin sensitivity → decision prompt (upfront vs long-term cost) |
| engagement ring settings | definition → setting types (solitaire, halo, pavé, bezel, three-stone, cathedral) → shopping for settings |
| ring size chart | definition → **US size table (inner circumference / diameter, mm)** → measure at home |
| how to measure ring size | direct answer → **7 numbered steps** (paper/string) → existing-ring method → accuracy tips |
| what are diamonds made of | carbon → atomic structure (99.95% carbon, trace N/B, lattice) → vs graphite |

Recurring decision prompts at the end of the AI Overviews:
- budget;
- carat size;
- shape;
- metal type;
- lifestyle / daily wear;
- natural vs lab-grown.

## 7. PAA patterns (only those that inform Stage 19)

- **Lab-grown:** "Are lab diamonds like real diamonds?"; "Is it worth buying lab grown diamonds?"; "What are the disadvantages…"; "Will a diamond tester say… real?"; "What is the lifespan of a lab diamond?" (value and cloudiness SERPs); "Do lab diamonds lose their sparkle?"; "Is making lab grown diamonds bad for the environment?"; "What is the most ethical diamond?". Perception questions ("Do rich people buy…", "Why do jewelers…") recur, as in Stage 8.
- **Formation/composition:** "Do diamonds start as coal?" and "Is coal under pressure a diamond?" (two SERPs); "How long does a diamond take to form?"; "Is the earth still creating diamonds?".
- **4Cs/colour/carat:** "What is the 5th C of diamonds?"; budget-to-size questions ("How big a diamond will $10,000 buy?" on two SERPs; "How many carats is a $5000 diamond?"); "Is a 2 carat diamond a big diamond?"; "Which diamond color is better, D or G?"; "Which diamond color is the least valuable?".
- **Cut/shapes:** "What is a diamond cut called?"; "Which diamond cut is the cheapest?" (repeats from Stage 8); "Which shape of diamond is most expensive?".
- **Certificate:** "How do you get a diamond certificate?"; "How do I check my diamond certificate?"; "What are the top 5 diamond certifications?".
- **Metals:** "What are the disadvantages of 18k gold?"; "Can you wear 14k gold everyday?"; "Can gold be fake if it says 14k?"; "Which is better, platinum or white gold?"; "What are the disadvantages of platinum?" / "…of white gold?".
- **Rings:** "Which setting is best…?"; "What is the most popular setting…?"; "Is there a virtual ring sizer?"; "Can I measure my ring size on my phone?"; "How big is a 7 ring size?".
- **Off-topic, not used:** celebrity carat questions, "2:1:1 rule", "divorce ring", engagement-ring spend-by-salary.

## 8. Semantic concepts, entities, attributes

- **New concepts evidenced** (see the change log for gap links):
  - absolute vs percentage resale loss;
  - lab-grown sector transparency / lack of regulation;
  - how to buy lab-grown responsibly (ask origin, energy source);
  - causes of a cloudy look;
  - care/cleaning to restore sparkle;
  - coal myth;
  - formation timescale;
  - carat-to-mm chart by shape;
  - on-hand size comparison;
  - brilliant vs step-cut appearance;
  - getting a certificate;
  - certificate as identification;
  - gold stamp authenticity;
  - platinum patina;
  - international ring-size conversions;
  - measuring accuracy tips;
  - trace elements in diamond.
- **New entities:**
  - settings: solitaire, cathedral;
  - labs: AGS (certificate SERP);
  - metals: palladium and nickel (white-gold alloys);
  - composition: nitrogen/boron (trace elements);
  - production geography: India/China (lab-grown production and energy).
- **Attributes most often recurring** across the 17 SERPs: PRICE/VALUE, DURABILITY, SIZE, MATERIAL, ORIGIN, CERTIFICATION and CARE.

## 9. Content formats (SERP evidence suggests)

| Format | Where |
|---|---|
| VISUAL_CHART | colour, carat size (dominant), ring size (table), 4Cs (images), settings/shapes (related "chart with pictures") |
| STEP_SEQUENCE | how to measure ring size; certificate check; formation "step by step" |
| COMPARISON_TABLE | 14k vs 18k; white gold vs platinum; cut vs shape |
| DEFINITION_BLOCK / answer-first | lab-grown definition, value, ethics, cloudiness, composition, certificate |
| PROS_CONS | ethics; value; per-metal disadvantages |
| TYPE_LIST | shapes, settings, 4Cs, report contents, labs, causes of cloudiness |
| Printable/interactive tool | ring size (PDF sizers, virtual sizer PAA); carat on-hand simulator (related) |

## 10. Stage 18 confirmations and changes

141 change-log rows across 16 targets:

| Change type | Rows | Meaning |
|---|---|---|
| CHANGED | 19 | 9 "page format unvalidated" rows resolved; 10 head-term rows now SERP-validated (volume still unmeasured) |
| CONFIRMED | 36 | Stage 18 concept seen on the new SERP |
| STRENGTHENED | 47 | More or stronger evidence. 26 imply a higher Stage 19 weight, e.g. kimberlite IMPORTANT→CRITICAL; ring-size chart and measuring IMPORTANT→CRITICAL; 4Cs order of importance OPTIONAL→IMPORTANT; lab-grown price trend and natural value retention SUPPORTING→IMPORTANT; ethics mining/labour OPTIONAL→IMPORTANT |
| WEAKENED | 3 | Lab-grown grading on the 4Cs head-term SERP; resizing on the ring-size SERPs; geometric intent on "diamond shapes". Each stays covered via owned keywords or as AVOID, at a lower implied weight |
| CONFLICT | 1 | `engagement ring settings` (see §11) |
| UNCHANGED | 1 | Lab-grown fluorescence: not on the cloudiness SERP; still keyword-only |
| NEW_EVIDENCE | 34 | New concepts, or previously dropped concepts now evidenced: fancy-colour boundary, care/cleaning, conflict-free mention, carat size chart, price-by-carat |

Special-case answers (brief section 13):

| Query | Finding |
|---|---|
| A. 4cs of diamonds | EDUCATIONAL guide with a chart expectation (images pack at rank 2). All four Cs are expected, each as meaning + grade range, plus "order of importance". Not commercial. |
| B. Diamond color chart | Grading scale + visual chart + buying advice (value per group, metal pairing). No gemstone-colour intent beyond a fancy-colour boundary note. |
| C. Diamond carat size chart | Physical size (mm) and visual/on-hand comparison dominate, by shape. Weight-vs-size and "is 2 ct big" appear as questions. Budget-to-carat questions appear; no live prices. |
| D. Diamond cut | Cut grade / light performance first, with strong shape conflation. The cutting process is not evidenced. |
| E. Diamond shapes | Jewellery intent dominates the plural; geometric intent is marginal (related only). |
| F. Diamond certificate | Definition, report contents, labs (GIA/IGI/AGS), verification (PAA + 3 lookup related searches), lab-grown origin disclosure. Lab navigational results sit at the top. |
| G. 14k vs 18k | Purity, colour, durability/daily wear, price/value (intrinsic metal value), hypoallergenic. Resale appears only as "intrinsic metal value". |
| H. White gold vs platinum | Composition/purity, price, maintenance (rhodium re-plating vs patina), skin sensitivity (nickel), durability/scratching (related). Colour is only implied via rhodium. |
| I. Engagement ring settings | Types list (solitaire, halo, pavé, bezel, three-stone, cathedral), chart expectation, but a commercial-led SERP. |
| J. Ring size chart | Chart (US sizes with mm), at-home measurement, conversions (EU, cm, inches), men/women, band-width fit. Resizing absent. |
| K. How to measure ring size | Step-by-step at-home measurement (string/paper, existing ring), accuracy tips, video. Professional measurement not prominent. |
| L. Lab-grown queries | Definition, process summary, value/resale, ethics/environment, appearance-over-time and comparison with natural all appear. The definition SERP is partly comparison-led (organic #1–#2), so EDU-LG-00 needs a brief comparison framing that links to EDU-LG-02. |

## 11. Unresolved items

1. **CONFLICT — `engagement ring settings`.** The head term is transactional/mixed, so it is unlikely to be served by an Education article alone. This is a Stage 15-style ownership question and was **not changed** here. EDU-RJG-01 keeps its validated editorial query.
2. **No search volumes.** No volume lookup was run. All head terms remain unmeasured for demand; only the SERP shape is now known.
3. **Business facts needed:**
   - HOD's energy source / sustainability claims (higher stakes: the SERP names India and China coal grids);
   - buy-back policy;
   - which labs grade HOD stones;
   - settings sold without centre stone / design-your-own;
   - metal options.
4. **"What is the 5th C?"** The SERP does not define it; Stage 19 must not assume an answer.
5. **Still no SERP evidence:**
   - the clarity-chart / VS / SI / VVS head terms (EDU-4C-01/02/03 rows remain INSUFFICIENT_EVIDENCE);
   - the EDU-LG-10 engagement-ring boundary (D-19);
   - lab-grown fluorescence.
6. **Point-in-time QC.** `qc_17` and `qc_18` now flag the Stage 18.5 raw files in their "no new files / no DataForSEO call" checks. This is expected and the same pattern as earlier stages.

Stage 19 has not been started.
