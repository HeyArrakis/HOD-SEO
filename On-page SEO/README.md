# On-page SEO — Step 2 package (finalized 2026-10-10)

**Status:** Step 2A (decision resolution) and Step 2B (finalization) complete. This is a **specification package**: nothing on the live site, the CMS, the research, the keyword-ownership files or the BC-001 package was changed (the only edit outside this folder is the single approved `target_owner` annotation in the final calendar, plus status synchronization of root `CLAUDE.md`), and no paid DataForSEO call was made. Step 1 (`../QA/01–06`) was not modified.

## What is final, what is blocked

* **Final and ready for developers after the AWS migration:** 73 of 147 rows (`READY FOR IMPLEMENTATION POST-AWS`).
* **Final specification, content still to be written (Class A):** 41 rows (`PRE-AWS PREPARATION`).
* **Blocked by one named external input:** 15 rows — HOD facts 7 (`HOD INPUT REQUIRED`), GSC baseline 6 (`GSC BASELINE REQUIRED`), product/offer confirmation 2 (`CONDITIONAL — PRODUCT/OFFER CONFIRMATION`). Engineering inputs (E-xx) never change *what* to do, only *how/when*.
* **No change / not planned:** 18 rows.
* **Intended implementation:** after the AWS cut-over, in the order of `08`; copy-only items may move earlier only if engineering confirms the content store is editable and outside the freeze (E-01/E-02).

## Close-out status (2026-10-10) and remaining actions outside this package

**Done:**

* **BC-001 publication held.** The approved package is protected and unedited; only the status of its future publication changed (`HOD INPUT REQUIRED`, action `HOLD PUBLICATION (pending F-A1)`). Its approved meta, intro and article say '6–9 days of insured shipping', and insurance is unconfirmed (SR-02). If HOD confirms insured shipping, the existing approved wording may proceed after the normal human review; if not, a separate, explicitly authorized content revision is required before publication.
* **Calendar owner annotation.** In `Keywords/content SEO/FINAL-BLOG-CALENDAR/BLOG_CALENDAR_FINAL.csv`, row `content_id = BLOG-WR-TYPES`, field `target_owner` changed from `Blog (Style & Trends)` to `EDU-WB-TYPES` with the user's approval. No other calendar field changed.
* **Root `CLAUDE.md` and project memory** synchronized with this status.

**Still open (external inputs only):**

1. **HOD facts** (`11`): F-A1 (also decides BC-001 publication), F-A2, F-B1, F-C1, F-C2, F-D1 (must answer); F-A3, F-E1, F-E2, F-E3, F-E7 (should answer); F-E4, F-E5, F-E6 (nice to have).
2. **Engineering inputs** (`12`, E-01…E-13) and the **GSC exports** (`13`, G-01…G-06).
3. **Confirmed-facts file (optional housekeeping, SR-01).** `Keywords/content SEO/content-strategy/blog-calendar/revision/confirmed_business_facts.md` does not record the start point 'from design approval' (stated by the project owner on 2026-10-10). The package already treats the timeline as fully confirmed.

## Files

| File | What it is |
|---|---|
| `01-ON-PAGE-SEO-MASTER.csv` | **Operational file** — 147 rows: current vs final title/meta/H1, content, links, schema, AEO/GEO, image rules, priority, AWS class, decision resolution, remaining dependencies, status, evidence. |
| `02-ON-PAGE-SEO-MASTER.md` | Overview, counts, vocabularies, page-family rules, limits. |
| `03-TITLE-META-OPTIMIZATION.md` | Brand-suffix verification, rules, every title and meta, claims removed from the Step 1 drafts. |
| `04-H1-CONTENT-OPTIMIZATION.md` | H1 table, content specs per page, trust-critical pages. |
| `05-INTERNAL-LINK-IMPLEMENTATION.md` + `.csv` | Link specifications with real URLs (Stage 16 + calendar + Step 2A additions). |
| `06-SCHEMA-AEO-GEO-SPEC.md` | Schema (current / recommended / why / dependency / validation), AEO, GEO/entity, image rules. |
| `07-PDP-ON-PAGE-SEO.md` + `07-PDP-PRIORITY-ACTIONS.csv` | PDP rules and the PDPs needing special treatment. |
| `08-ON-PAGE-IMPLEMENTATION-PRIORITIES.md` | Top 10, work packages, CRITICAL/HIGH lists, A/B/C split. |
| `09-ON-PAGE-DECISIONS-REQUIRED.md` | Original decision register (2026-10-09) with final dispositions — audit trail. |
| `10-DECISIONS-RESOLUTION-LOG.md` + `10-COMMERCIAL-KEYWORD-ASSIGNMENTS.csv` | All 19 decisions: disposition, rationale, evidence, confidence, dependency; keyword assignments; Education resolutions; redirect/index-control spec. |
| `11-HOD-CLIENT-FACTS-REQUEST.md` | One consolidated questionnaire for HOD. |
| `12-ENGINEERING-INPUTS.md` | Engineering intake and what each answer unblocks. |
| `13-GSC-DATA-REQUEST.md` | GSC exports/access needed and what they affect. |
| `_build/` | Generator, resolution data (`s2_final.py`) and read-only QC (`qc_step2.py`). Do not rerun `s2_write.py` unless asked — it overwrites the files above. |

## Conventions

American English for all customer-facing copy (slugs such as `/fine-jewellery/` are unchanged). Titles are **pre-suffix** values (the template appends ` | House of Diams`; the homepage is absolute). Volumes/KD/intent labels come from existing project files — SERP type is validated for only four head terms. GSC values are never shown. Business facts are never invented: only the bespoke timeline is confirmed.

## QA performed

Disk-based checks (`_build/qc_step2.py`) — all PASS at the time of writing:

* all 147 Step 1 Row IDs present, same order; URL column identical to Step 1 for every live page (no slug changed by spelling cleanup);
* all 19 decisions have an explicit disposition in `10`, and every `OD-xx` used in the CSV is defined there; no row is marked "awaiting decision";
* recommended rendered titles, metas and H1s are unique; no shipping/returns/warranty/certification/"free" wording in any recommended title, meta or H1 (BC-001's approved package meta, carried unchanged, is excluded and noted in its row);
* American English in recommended titles, metas, H1s and link anchors (UK spellings allowed only inside quoted current text or URLs);
* each primary keyword is assigned to at most one URL (no duplicate primary ownership; none collides with a Stage 15 owner or a calendar primary); every ASSIGNED commercial title/H1 contains its assigned head;
* PDP schema name = H1 recommendation, oval-PDP link anchors = final H1; Education index/H1/anchors use 'Blog' (no 'Journal');
* no status claims readiness while a HOD, GSC or product-confirmation dependency blocks the main deliverable; every link destination is a real crawl URL, a proposed Stage 15 URL, or `URL PENDING` / `NO URL`;
* no GSC value in any cell; FAQPage never recommended; the confirmed bespoke timeline is preserved with its hedging;
* no order-tracking promise in any recommended title, meta, H1 or target question (not a confirmed feature; F-A1 gates it) and no founder/design-team capability claim while F-C1 is open;
* close-out checks: BC-001 cannot be marked publish-ready while F-A1 is unconfirmed (status `HOD INPUT REQUIRED`, action `HOLD PUBLICATION`), status totals reconcile to 147, the calendar differs from git HEAD in exactly one cell (`BLOG-WR-TYPES.target_owner`), `blogs/` and `.env` are unchanged;
* correction-pass checks: no `jewelery`/`symbolizm`-type misspelling in any active recommendation, anchor or page label (current-site quotes are allow-listed); no leftover note that treats the US-spelling decision as still open; the Bangles row makes no bangle claim that its documented inventory contradicts and is held with F-E7; no unresolved "please confirm the start point" ask for the already-confirmed timeline; every `insured` mention is either a removed-claim note or points to F-A1/SR-02; the calendar `target_owner` action is tracked in the README; README status counts equal the master CSV counts.

**Protected files:** this step wrote only inside `On-page SEO/` (plus status synchronization of the root `CLAUDE.md`, one memory note, and the single user-approved `target_owner` annotation in the final calendar, verified against git HEAD). `QA/01–06`, the rest of `FINAL-BLOG-CALENDAR/`, `architecture/`, `dataforseo/`, `serp/`, `clusters/`, `competitors/`, `content-strategy/`, `blogs/` (incl. bc-001), `.env` and `~/Desktop/HOD-SEO-Research` have unchanged modification times; no commit or push; no `QA/_build` script was run.

**Environment note (not caused by this step):** `Keywords/content SEO/CLAUDE.md` is deleted in the working tree (pre-existing); its text was read from git `HEAD` and not restored.
