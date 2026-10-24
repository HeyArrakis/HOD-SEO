# HOD Backlink Acquisition — Workstream README

Workstream: **Off-page SEO / Backlink Acquisition** for House of Diams (US market). Created **2026-10-10**.
Nature: **research and planning**. It does not perform outreach, change the website or add new keyword research. It can run while the AWS migration is in progress (AWS Class A).

## Files

| File | What it is |
|---|---|
| `01-HOD-BACKLINK-ACQUISITION-DATABASE.csv` | **Operational database**: 77 rows (one per opportunity), 31 required columns + 10 helper columns. UTF-8, comma-delimited, RFC 4180 quoting. |
| `02-COMPETITOR-BACKLINK-GAP-SUMMARY.md` | Competitor set, provider data, verified findings, publisher patterns, HOD's own backlink baseline |
| `03-OUTREACH-PRIORITY-QUEUE.md` | Readiness gate G0, queue ranks 1–10, draft outreach approaches (not sent) |
| `04-UNLINKED-MENTIONS-AND-DIGITAL-PR.md` | Mention search (0 verified), digital-PR platforms, grounded angles, linkable-asset inventory |
| `05-METHODOLOGY-AND-DATA-LIMITATIONS.md` | Sources, paid calls and costs, verification process, filters, scoring formula, gaps, approvals needed |
| `_raw/dataforseo/` | C1–C6 raw API output + processed CSVs (dated snapshot; do not edit) |
| `_raw/page-checks/` | Live page-check and route-scan JSON + browser-check record (dated snapshot; do not edit) |
| `_build/` | Read-only scripts: `verify_pages.py`, `find_routes.py`, `parse_intersections.py`, `build_database.py` (regenerates 01), `qc_backlink_db.py` (QC); `urls_*.txt` / `domains_routes.txt` = the exact URL lists that were checked |

Naming note: the brief's suggested filenames were used as given. The workspace convention of numbered files plus `_build/` (as in `QA/` and `On-page SEO/`) was kept, with raw evidence added under `_raw/`.

## How to use the database
- **Start with** `Priority` = P1, sorted by `Queue rank`, then P2.
- Useful filters:
  - `Opportunity category`
  - `Outreach status`
  - `Evidence class`
  - `Competitor linking?` = Yes (verified gaps)
  - `Limitations / dependencies` contains "G0", "F-E3", "affiliate" and similar
- **Before contacting anyone:**
  1. Confirm gate G0 is cleared (03 §1).
  2. Re-open the source page and confirm it is still live.
  3. Re-read the confirmed-facts list.
  4. Personalize the draft only from what the current page actually says.
- **After each action:** update `Outreach status`, add a dated note in `Verification notes` (date, channel, no private email content) and set the `Next action`.

## Controlled values

**Outreach status**
| Value | Meaning |
|---|---|
| UNRESEARCHED | Listed but not yet examined (not used in this build) |
| VERIFICATION_REQUIRED | A key element (page, route, terms or eligibility) is not yet verified |
| VERIFIED_PROSPECT | Page/site, relevance and a route verified; not in the first queue |
| PRIORITIZED | Verified P1, waiting on gate G0 |
| OUTREACH_READY | G0 cleared **and** relevance, opportunity and contact/submission route all verified. **No row has this status yet.** |
| CONTACTED | First message sent (date in notes) |
| RESPONDED | Reply received |
| WON | Link or mention published (record URL, date, `rel`) |
| LOST | Declined or no reply after one follow-up |
| REVISIT_LATER | Valid but conditional (unpublished HOD asset, affiliate or business decision, unconfirmed product) |
| DISQUALIFIED | Rejected on quality, relevance or policy grounds (reason in `Priority rationale`); kept to avoid re-research |

**Priority:** P1 / P2 / P3 / NONE (disqualified). Formula and gates are in 05 §7. Authority metrics are not part of the score.

**Opportunity category:** COMPETITOR_BACKLINK_GAP, EDITORIAL_PUBLICATION, WEDDING_PUBLICATION, LUXURY_PUBLICATION, DIAMOND_RESOURCE, INDUSTRY_ASSOCIATION, RELEVANT_DIRECTORY, UNLINKED_MENTION, DIGITAL_PR, RESOURCE_PAGE, BROKEN_LINK_OPPORTUNITY, EXPERT_CONTRIBUTION, OTHER.

**Link type / acquisition route:** EDITORIAL_ROUNDUP_INCLUSION, EDITORIAL_PITCH, EXPERT_COMMENTARY, JOURNALIST_REQUEST_PLATFORM, PRESS_RELEASE_NEWS, MEMBERSHIP_DIRECTORY, BRAND_DIRECTORY_SUBMISSION, REVIEW_REQUEST, VENDOR_LISTING, SUBMISSION_FEATURE, BROKEN_LINK_REPLACEMENT, RESOURCE_PAGE_SUGGESTION, AFFILIATE_PROGRAM_DEPENDENT, COMMUNITY_PARTICIPATION, NONE.

**Relevance / feasibility:** HIGH / MEDIUM / LOW. Feasibility is derived from score F (3 = HIGH, 2 = MEDIUM, ≤ 1 = LOW).

**Evidence class:** see 05 §5.

## Verified backlink gap vs unverified prospect
- **Verified competitor backlink gap** (`Competitor linking?` = Yes): backlink data (DataForSEO) and/or the live page itself shows the page or domain linking to a named competitor, **and** HOD's domain is absent from HOD's own backlink list (C1). The evidence class says how strong this is: PROVIDER_AND_LIVE_VERIFIED is strongest; PROVIDER_DOMAIN_LEVEL has no page URL.
- **Unverified / standalone prospect** (`Competitor linking?` = Unknown, evidence class PUBLIC_SOURCE_PROSPECT): a relevant site or route found through public research, with no backlink data collected for it. Stage 9 SERP presence is **never** treated as link evidence.
- A competitor link is not by itself a reason to pursue a prospect. Spam, paid and irrelevant sources are disqualified.

## Maintenance
- Edit curated rows in `_build/build_database.py`, then run `python3 _build/build_database.py` (overwrites `01` only) and `python3 _build/qc_backlink_db.py`.
- Once outreach begins, either stop regenerating and edit `01` directly, or move status updates into the builder, so live statuses are not overwritten.
- New paid data needs per-call approval (05 §10). Save any new raw output with a **new dated filename**; never overwrite the 2026-10-10 snapshots.
- Re-verify links and contacts before each outreach wave; after the AWS cut-over, check that every target URL still resolves (Class C).
- Never add guessed emails, invented contacts, fabricated metrics or HOD claims not on the confirmed list.
