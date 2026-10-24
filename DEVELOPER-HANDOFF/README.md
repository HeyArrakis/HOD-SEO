# Developer Handoff — House of Diams SEO

Prepared 2026-10-24. These three files **consolidate** work that already exists in this repository. They are not a new SEO strategy; the existing project files stay authoritative (`CLAUDE.md` is the master context).

| File | Use it to |
|---|---|
| [`01-PAGE-BY-PAGE-KEYWORD-IMPLEMENTATION.csv`](01-PAGE-BY-PAGE-KEYWORD-IMPLEMENTATION.csv) | See **which topic belongs on which page**: one row per distinct target page (147), with owner keyword, secondary topics, intent, required title/meta/H1/content, link and schema actions, and whether the live site already matches |
| [`02-SEO-WORK-COMPLETED-AND-PLANNED.md`](02-SEO-WORK-COMPLETED-AND-PLANNED.md) | See **what research and preparation is already done**, with exact file paths, the ten blog packages and what was verified live on 2026-10-24 |
| [`03-DEVELOPER-REMAINING-FIXES.csv`](03-DEVELOPER-REMAINING-FIXES.csv) | See **what remains to implement or verify** (51 de-duplicated rows, controlled statuses, evidence and validation method for each) |

Fresh live evidence behind the statuses: [`../Technical/2026-10-24-live-validation/`](../Technical/2026-10-24-live-validation/README.md) (read-only, dated; the older 2026-10-09 snapshot in `QA/_build/evidence/` is kept unchanged).

## How to read the statuses

* `01` column **Implementation status** starts with a controlled value (for example `READY_NOT_YET_APPLIED`, `PUBLISHED_LIVE_VERIFIED`, `PLANNED_NOT_LIVE_WRITE_PENDING`, `BLOCKED_BY_CLIENT`, `BLOCKED_BY_GSC`, `NEEDS_DECISION_URL_CHANGED`) followed by what the 2026-10-24 check saw.
* `03` **Current status** is one of: `VERIFIED_FIXED`, `IMPLEMENTED_NOT_YET_VERIFIED`, `OPEN`, `POST_MIGRATION_RECHECK`, `BLOCKED_BY_CLIENT`, `BLOCKED_BY_GSC_OR_DATA`, `NOT_PLANNED`, `NEEDS_DECISION`. "Open" means the problem was seen on the live site on 2026-10-24. Items that could not be checked with HTTP fetches are `POST_MIGRATION_RECHECK`, never "open defect" or "fixed".

## Rules that still apply

* Keep existing URL slugs unless the approved redirect plan says otherwise.
* Each primary keyword has one owner page; do not add a second.
* US market, American English in customer-facing copy.
* Only confirmed HOD facts may be published. The bespoke timeline is the one confirmed fact: typically 2–3 weeks to make plus about 6–9 days delivery, generally about 3–4 weeks from design approval to delivery, stone-dependent, not guaranteed. **Insured shipping, certification labs, warranty, returns terms and shipping cut-offs are not confirmed.**
* Do not edit the approved blog packages or the final blog calendar without explicit authorization.

## Source conflicts found while consolidating (nothing was silently changed)

| # | Conflict | Treatment |
|---|---|---|
| 1 | Stage 15 registry lists `/engagement-rings/by-desgin/side-stone-rings` (404); the live owner URL is `/by-design/` | Resolved earlier (OD-06): `01` uses the `/by-design/` URL; the redirect is `03` RED-01 |
| 2 | Stage 15 registry has 27 target pages; the Step 2 master has 147 rows | `01` follows the Step 2 master (superset); Stage 15 IDs are cited per row |
| 3 | Calendar ID `BLOG-WR-TYPES` is the Education page `EDU-WB-TYPES` | Calendar `target_owner` already updated (2026-10-10); both IDs are shown |
| 4 | 12 Education pages had different primary keywords in Stage 17/19 and the calendar | Resolved earlier (OD-03): calendar term is primary |
| 5 | BC-001: calendar says `READY_TO_WRITE`, Step 2 says publication held, the live site has the page | `03` MD-04 (decision); nothing edited |
| 6 | All project documents assume `www.houseofdiams.com`; the live site now canonicalizes to `houseofdiams.com` | `03` MIG-03 (decision); `01` shows paths only |
| 7 | Ownership files list `/fine-jewellery/bracelet/tennis`; the live site 301s to `/tennis-bracelet` | `03` MIG-09 (decision) |
| 8 | Step 2 master "Current URL Status" columns are the 2026-10-09 baseline (the ten blog URLs read "NOT LIVE") | The 2026-10-24 check is appended to `01`; the source files are unchanged |
| 9 | `progress.md` spend ($1.10052) differs from the `cost-log.csv` sum (≈$1.0852); backlink spend ($0.213552) is not logged | Recorded in `03` OFF-03; no historical change made |

## Not in this package

No implementation, outreach, publishing, paid API call or live-site change was made to produce it.
