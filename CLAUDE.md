# CLAUDE.md — House of Diams (HOD) SEO Workspace — MASTER CONTEXT

Workspace: `/Users/manavdesai/Desktop/HOD SEO/` (git repo, remote `HeyArrakis/HOD-SEO` on GitHub, branch `main`).
Last audited: **2026-10-09**; status synchronized **2026-10-10** (Step 2A/2B close-out) and **2026-10-24** (GitHub sync, fresh read-only live validation, developer handoff — §0, §2, §5, §6, §8 note, §9, §12 #14–#18 and §13 carry the 2026-10-24 updates; §8 is still the 2026-10-09 baseline). This is the single onboarding document for any Claude session working here. Read it fully before doing anything.

> Facts below come from the files present in the workspace. Anything not provable from a file is marked **VERIFY** or **UNKNOWN**. Do not upgrade a VERIFY to a fact without evidence.

---

## 0. TL;DR (read this if nothing else)

- **Project:** US SEO for **House of Diams** (https://www.houseofdiams.com/) — luxury diamond jewellery ecommerce (lab-grown and natural diamonds, engagement rings, wedding bands, fine jewellery, bespoke). Manufacturing/craft link to Surat, India; primary SEO market = **United States, English** (DataForSEO location 2840 / `en`).
- **Research Stages 1–19 (+18.5) are COMPLETE and FROZEN.** The final blog calendar is complete and is the publishing source of truth. Do not redo research.
- **Step 1 — Master SEO Planning Layer: COMPLETE** (`QA/01…06`, built 2026-10-09).
- **Step 2 — On-Page SEO Preparation: FINALIZED 2026-10-10, correction pass and close-out COMPLETE** (`On-page SEO/`; Step 2A resolved OD-01…OD-19 under the user's delegation, Step 2B propagated them; specification only — nothing implemented). Of 147 rows: **73 ready after AWS**, 41 pre-AWS writing tasks with final specs, 15 blocked by a named external input (HOD input 7, GSC baseline 6, product/offer confirmation 2), 18 no change / not planned. 624 internal-link specs; the package's read-only QC (`On-page SEO/_build/qc_step2.py`) = **65 checks, all pass**. Blocked only by named HOD facts (`11-…`, F-A1…F-E7), engineering inputs (`12-…`) and GSC data (`13-…`). **US market and American English are confirmed rules (2026-10-10): user-facing copy is US English; URL slugs are unchanged.**
- **BC-001 publication was HELD** (Step 2 status `HOD INPUT REQUIRED`, action `HOLD PUBLICATION (pending F-A1)`): its approved package says '6–9 days of insured shipping' and insurance is unconfirmed. The package stays protected and unedited. **Update 2026-10-24: the page is nevertheless LIVE** with that wording (verified), as are the other nine packaged posts. Needs a decision: HOD confirms insured shipping, or a separate, explicitly authorized revision (`DEVELOPER-HANDOFF/03` row MD-04).
- **The AWS migration is mostly implemented (verified 2026-10-24 at front-end level):** all responses come via CloudFront + nginx; images are on `media.houseofdiams.com`; sitemap/canonicals now use the apex host `houseofdiams.com` (www still serves 200). Cut-over date, CMS location and origin details remain UNKNOWN. Most Step 2 on-page specs are **not yet applied**; see `DEVELOPER-HANDOFF/`. Changes to templates, URLs, schema, sitemap, robots, redirects or image hosting are now developer implementation work and must follow the approved specs; preparation work (drafts, plans, decisions) continues as before.
- **Developer handoff (2026-10-24):** `DEVELOPER-HANDOFF/` — `01` page-by-page keyword implementation (147 rows), `02` work completed/planned overview, `03` remaining fixes (51 rows, controlled statuses). Consolidation only; the source files remain authoritative.
- **Never change the live site, the final calendar, source research, keyword ownership, or BC-001** unless the user explicitly says so. (Single approved exception to date: the calendar `target_owner` of `BLOG-WR-TYPES` was set to `EDU-WB-TYPES` on 2026-10-10 — see §12 #3.) **Never run a paid DataForSEO call without per-call user approval.**

---

## 1. Business context

- Name: House of Diams. Site: https://www.houseofdiams.com/. Business: luxury diamond jewellery ecommerce.
- Product/service areas: diamond engagement rings, wedding bands, fine jewellery (earrings, necklaces/pendants, bracelets, rings), bespoke/custom jewellery, natural and lab-grown (CVD) diamonds, diamond education.
- The live catalogue currently positions itself as lab-grown (home/engagement-ring titles and PDP copy) — see open decision COM-LG-HUB (§12).
- Spelling: **American English is the confirmed rule (2026-10-10)** — jewelry, color, center, customize, inquiry — in all customer-facing copy, nav labels and anchors. The research files and URL slugs (e.g. `/fine-jewellery/`) keep their original spelling; slugs are never changed just for spelling.
- Existing blog/education articles are **assets to evaluate** (retain / rewrite / merge / redirect / retire), not the final editorial plan. The 10 current `/blog` articles are not the final 10 topics.

### Confirmed HOD business facts (the only ones — do not invent others)
| Fact | Wording rule | Source |
|---|---|---|
| Bespoke jewellery typically takes **2–3 weeks to make**, then **~6–9 days delivery**; total **generally ~3–4 weeks**; depends on the stone selected | Never a guarantee. Always "typically / usually / approximately". | `Keywords/content SEO/content-strategy/blog-calendar/revision/confirmed_business_facts.md` (user-supplied 2026-09-29) |

Everything else (certification labs IGI/GIA, shipping cut-offs, returns terms, warranty, platinum availability, cleaning/appraisal services, founder names/roles, Hip Hop range, holiday order-by dates) is **UNCONFIRMED**. Rows in the calendar marked `BUSINESS_FACT_REQUIRED` stay unfilled until HOD confirms.

---

## 2. Directory structure (actual, audited 2026-10-09)

```
/Users/manavdesai/Desktop/HOD SEO/
├── CLAUDE.md                      ← THIS FILE (master context)
├── .gitignore                     (untracked; contains ".env")
├── .env                           (git-ignored, never tracked; holds a credential — NEVER read, print, copy or commit)
├── Keywords/
│   └── content SEO/               ← the frozen research project (Stages 1–19) + blog production
│       ├── CLAUDE.md              (original research-project rules — kept, see §3 note)
│       ├── README.md, LICENSE, .gitignore
│       ├── progress.md            (stage-by-stage log; authoritative index of outputs)
│       ├── decision-log.md        (Stage 1–… research decisions)
│       ├── cost-log.csv           (every DataForSEO call; 41 rows)
│       ├── FINAL-BLOG-CALENDAR/
│       │   └── BLOG_CALENDAR_FINAL.csv        (112 rows; 2026-10-04 → 2027-03-30)
│       ├── reference/
│       │   ├── BLOG_PUBLISHING_CONTEXT.md     (permanent blog rules)
│       │   ├── SEO_PLAYBOOK.md                (strategic reference; evidence-labelled)
│       │   └── VERIFICATION_AUDIT_2026-10-04.md (fact-check of the 3 rule files)
│       ├── site/                  (Stage 1 inventory 2026-09-17: 01_*.csv/.md, raw_sitemap.xml)
│       ├── dataforseo/
│       │   ├── raw/               (untouched API output: ranked kw, kw-for-site, ideas, 18_5_stage_serp, blog_calendar, final_calendar)
│       │   ├── processed/         (Stages 3–7: ranked keywords, universe, seed matrix, expansion, 07_hod_master_keyword_database.csv)
│       │   └── metrics/
│       ├── serp/
│       │   ├── raw/               (raw SERP pulls)
│       │   └── analysis/          (Stage 8 validation; Stage 18.5 targeted SERP supplement)
│       ├── competitors/analysis/  (Stage 9: landscape, frequency, keyword gap)
│       ├── clusters/              (Stage 11: registry, keyword→cluster map, methodology, scripts/)
│       ├── architecture/          (Stages 12, 14, 15, 16: IA, Education architecture, keyword→URL map, linking)
│       ├── content-strategy/      (Stages 10, 13, 17, 18, 19 + blog-calendar/)
│       │   └── blog-calendar/     (calendar build history: revision/, working/, final-consolidation/, scripts/, confirmed_business_facts.md)
│       ├── blogs/                 (10 publishing packages: bc-001, 003, 004, 006, 007, 008, 009, 018, 035, 036)
│       ├── scripts/               (Stage 18.5 build/QC)
│       └── exports/               (empty)
├── DEVELOPER-HANDOFF/             ← 2026-10-24 developer handoff: README.md, 01 keyword-implementation CSV, 02 completed/planned MD, 03 remaining-fixes CSV, _build/ (generators)
├── Off-page SEO/Backlink Acquisition/  ← backlink research & outreach planning (2026-10-10): 77-row database, gap summary, queue, mentions/PR, methodology, brand sheet draft (.docx), _raw/ (DataForSEO + page checks), _build/. Outreach NOT started.
├── QA/                            ← Step 1 outputs (generated, 2026-10-09); also main.md + easy.md (functional/UX bug handoff from GitHub, 2026-10-07; non-SEO)
│   ├── 01-MASTER-SEO-IMPLEMENTATION-MAP.csv   (147 rows, operational file)
│   ├── 02-MASTER-SEO-IMPLEMENTATION-MAP.md
│   ├── 03-SEO-IMPLEMENTATION-PRIORITIES.md
│   ├── 04-KEYWORD-URL-OWNERSHIP-VALIDATION.md
│   ├── 05-ON-PAGE-OPTIMIZATION-BACKLOG.md
│   ├── 06-PDP-AUDIT-APPENDIX.csv              (per-product audit, 184 PDPs)
│   └── _build/                (README.md, scripts/ = generators, evidence/ = raw live-crawl data)
├── On-page SEO/                   ← Step 2 outputs (finalized 2026-10-10): 01 master CSV, 02–09 docs, 10 log + keyword CSV, 11 HOD facts, 12 engineering, 13 GSC, 05/07 CSVs, README.md, _build/
└── Technical/                     ← `2026-10-24-live-validation/` (dated read-only post-AWS crawl: README, crawl JSON, sitemap, probes, scripts). Older technical task lists live outside the repo (`~/Desktop/New HOD SEO/`, 2026-09-29).
```

Outside the repo: `~/Desktop/HOD-SEO-Research` is a **second copy** of the research project (per `QA/02` C13: identical content except `.git`/`.env`). It exists on disk. **Treat `Keywords/content SEO/` in this repo as the working source of truth; do not edit the copy and do not sync between them without the user's instruction.**

Git state at audit (2026-10-09): branch `main`; last commit `94e5876 "Reorganize SEO project structure"`; `.gitignore` and everything under `QA/` were untracked. **Update 2026-10-24:** `origin/main` had one newer commit (`9aff1cb`, adds `QA/main.md`, `QA/easy.md`, `.gitignore`), integrated by fast-forward; local work (QA/ Step 1, On-page SEO/, Off-page SEO/, Technical/, DEVELOPER-HANDOFF/, this file, the single approved calendar edit) was committed and pushed in the 2026-10-24 handoff commit. The nested `Keywords/content SEO/CLAUDE.md` is **still deleted in the working tree and deliberately not committed** — restore it only on the user's instruction. Do not commit/push unless asked.

---

## 3. Source-of-truth hierarchy

The project's own documents establish this order (as applied in `QA/02` §4 and the research rules); do not invent a different one:

| # | Layer | Authoritative file(s) |
|---|---|---|
| 1 | Operating rules | this `CLAUDE.md` (+ `Keywords/content SEO/CLAUDE.md`, `reference/BLOG_PUBLISHING_CONTEXT.md`) and the user's explicit instruction in the current chat |
| 2 | Site architecture / strategy | `architecture/12_*` (IA), `14_*` (Education), decision logs `12_ia_decision_log.md`, `14_education_decision_log.md`, `content-strategy/13_blog_strategy.md` |
| 3 | Keyword → URL ownership | `architecture/15_keyword_url_map.csv`, `15_target_page_registry.csv`, `15_cannibalization_check.csv`, `15_keyword_mapping_decision_log.md` |
| 4 | Final blog calendar | `FINAL-BLOG-CALENDAR/BLOG_CALENDAR_FINAL.csv` (publishing dates/topics/primary keywords for scheduled items) |
| 5 | Content boundaries / briefs | `content-strategy/19_content_boundaries.csv`, `19_content_briefs.csv`, `19_brief_registry.csv`, `19_business_fact_requirements.csv`, `19_internal_link_requirements.csv` |
| 6 | Clustering | `clusters/11_*` |
| 7 | SERP / search-intent research | `serp/analysis/08_*`, `18_5_*`; calendar rounds under `content-strategy/blog-calendar/` (`revision/round2_serp_analysis.csv`, `final-consolidation/call2_serp_analysis.csv`) |
| 8 | AEO / PAA / entity / question research | `content-strategy/17_question_map.csv`, `17_topic_intelligence.csv`, `18_question_coverage.csv`, `18_entity_coverage.csv`, `18_semantic_gap_register.csv` |
| 9 | Competitor research | `competitors/analysis/09_*` |
| 10 | Keyword data | `dataforseo/processed/07_hod_master_keyword_database.csv`, `content-strategy/blog-calendar/blog_keyword_research.csv` |
| 11 | Live-site observations | `QA/_build/evidence/` (**dated 2026-10-09; point-in-time**) |
| 12 | Generated QA / implementation docs | `QA/01…06` (**derived from 1–11; never overrides them**) |

Higher beats lower. **Where sources conflict, document the conflict and ask — do not silently pick.** Known conflicts are in §12 and `QA/02` §9 (C1–C13) / `QA/04` §3.

Note on the two CLAUDE.md files: `Keywords/content SEO/CLAUDE.md` is the original research-project rulebook (includes the Stage-19 file map and "Website safety: research only"). This root file consolidates and supersedes it for workspace-level context; **the nested file was not edited** and its rules remain valid. If they ever disagree, stop and ask.

Known doc inconsistencies (not fixed, flagged): the calendar's final date is 2027-03-30 (progress.md says 2027-03-31); `blogs/bc-001/README.md` refers to `blogs/BC-001-*.md` paths that no longer exist at that location after the 2026-10-05 reorganization (the files live inside `blogs/bc-001/`); `progress.md` states cumulative spend $1.10052 while the sum of `cost-log.csv` actual column ≈ $1.0852 (the log has a known unquoted-comma row shift on Stage 3); `README.md` "Status: Keyword research has not started yet" is stale.

---

## 4. File ownership & authority

Categories: **SOURCE** (source of truth) · **REF** (reference) · **WORK** (working file) · **GEN** (generated output) · **QA** (QA/validation) · **HANDOFF** (client/CMS handoff) · **TEMP** (temporary/build/evidence) · **DNM** (do not modify).

| Path | Category | What it is / controls | Editable? | Read in future sessions? | Regenerate? |
|---|---|---|---|---|---|
| `CLAUDE.md` (root) | SOURCE (rules) | Master context | Yes — update when status changes (see §17) | Always first | No |
| `Keywords/content SEO/CLAUDE.md` | SOURCE (rules) / DNM | Original research rules + Stage-19 file map | Only on user request | Yes | No |
| `…/progress.md`, `decision-log.md`, `cost-log.csv` | SOURCE / log | Stage history, decisions, spend | Append only when new work is done and logged; never rewrite history | Yes (progress.md first) | No |
| `…/FINAL-BLOG-CALENDAR/BLOG_CALENDAR_FINAL.csv` | SOURCE / **DNM** | Publishing schedule; 62 scheduled items + 50 `UNUSED_SLOT` | **No** — don't move dates, swap topics, or create another calendar unless the user explicitly asks. (One authorized field edit made 2026-10-10: `BLOG-WR-TYPES.target_owner` = `EDU-WB-TYPES`.) | Yes, for any blog/Education work | No |
| `…/reference/BLOG_PUBLISHING_CONTEXT.md` | SOURCE (blog rules) | Permanent blog-production rules | Only on user request | Yes before any blog work | No |
| `…/reference/SEO_PLAYBOOK.md` | REF | Strategic reference with evidence labels ([Google-confirmed] / [Industry practice] / [Framework] / [Source-specific tactic]) | Only on user request | As needed — apply principles, don't copy | No |
| `…/reference/VERIFICATION_AUDIT_2026-10-04.md` | QA / REF | Fact-check of CLAUDE.md / playbook / publishing context | No | If Google-claim accuracy matters | No |
| `…/architecture/*` (Stages 12, 14, 15, 16) | SOURCE / **DNM** | IA, Education architecture, keyword→URL ownership, cannibalization, linking | **No** (ownership changes need explicit user approval + logging) | Yes | Scripts exist (`architecture/scripts/`) but **do not rerun** |
| `…/content-strategy/19_*` | SOURCE / **DNM** | Stage 19 briefs, boundaries, fact requirements, link requirements | No | Yes before writing a page | No |
| `…/content-strategy/10_*, 13_*, 15_ranking_equity_protection.csv, 14_education_existing_content_mapping.csv` | SOURCE / **DNM** | Existing-content decisions and ranking-equity protection | No | Yes for any existing-article work | No |
| `…/content-strategy/17_*, 18_*` | SOURCE / **DNM** | Questions, entities, semantic gaps, topic intelligence | No | Yes | No |
| `…/clusters/*`, `competitors/analysis/*`, `serp/analysis/*`, `dataforseo/processed/*` | SOURCE (research) / **DNM** | Clusters, competitor gap, SERP validation, keyword databases | No | Reference as needed | **No** — do not redo |
| `…/dataforseo/raw/*`, `serp/raw/*` | SOURCE (raw) / **DNM** | Untouched API output | **Never** | Rarely | No |
| `…/site/*` | SOURCE (historical) / **DNM** | Stage 1 site inventory (2026-09-17: 198 sitemap URLs). Superseded for current state by `QA/_build/evidence` | No | Reference only | No |
| `…/content-strategy/blog-calendar/*` (except revision/working/consolidation internals) | SOURCE (history) / **DNM** | Calendar build history (`blog_content_calendar.csv` = pre-final revised calendar, **not** the final) | No | `confirmed_business_facts.md`, `blog_keyword_research.csv` yes; rest reference | No |
| `…/scripts/`, `*/scripts/`, `blog_calendar_qc.py`, `qc_*.py` | TEMP/QA tooling | Reproducibility + QC for stages | No (don't rerun unless asked) | No | No |
| `…/blogs/bc-0xx/` | HANDOFF | CMS-ready publishing package per blog (see §9) | Only the item the user is currently working on; **BC-001 DNM** | When working that blog | No |
| `QA/01…06` | GEN / QA | Step 1 outputs | Edit only when the user asks to revise Step 1 or a decision changes a row; otherwise read-only | Yes for any implementation step | **Avoid** — `_build` scripts overwrite 01–06 |
| `QA/_build/scripts/` | TEMP (generators) | Rebuild scripts for 01–06 | No | Only to reproduce Step 1 | Rerun only with user OK (overwrites 01–06) |
| `QA/_build/evidence/` | TEMP / evidence | Raw read-only live crawl 2026-10-09 (crawl.json 270 URLs, sitemap, robots.txt, llms.txt, articles.json, kwlookup.json, rows.json) | No (it's a dated snapshot) | As baseline | Re-crawl only for a *new dated* snapshot, saved separately |
| `On-page SEO/` | GEN (Step 2) | On-page specification package (see its README.md) | Edit only when the user asks to revise Step 2 or a decision changes a row; otherwise read-only | Yes for any implementation step | **Avoid** — `_build/s2_write.py` overwrites the package |
| `Technical/` | placeholder | Empty (.gitkeep) | Technical-SEO outputs may go here **after confirming with the user** | — | — |
| `.env`, `.gitignore` | DNM | Local credential file / ignore rule | **Never read `.env`**, never copy its contents anywhere | No | No |

---

## 5. Project status

### COMPLETE (supported by files)
- **Research Stages 1–19 + 18.5** (`progress.md`): site inventory → DataForSEO setup → ranked keywords → keyword universe → seed universe → controlled expansion → master keyword database → US SERP validation → competitor/keyword-gap → existing-content & equity analysis → semantic clusters → IA → blog/Education strategy & existing-content decisions → Education architecture → keyword→URL mapping (1,936 keywords, 27 target pages) → internal linking → keyword deep dives → semantic gap analysis → targeted SERP supplement (18.5) → Stage 19 content briefs (27 briefs).
- **AEO/PAA/entity/question research** (Stages 17/18/18.5 + calendar rounds; PAA/AIO captured per calendar item).
- **Blog calendar:** original → hard SEO revision (2026-09-29…10-03) → **Final Master Blog Calendar** (2026-10-03): 112 rows, 62 scheduled (28 Education incl. 20 new pages + 8 in-place refreshes; 10 editorial Blog; 7 informational; 3 high-intent; 14 seasonal/festive/occasion) + 50 unused slots.
- **Blog production:** 10 CMS-ready packages exist in `blogs/` (BC-001, 003, 004, 006, 007, 008, 009, 018, 035, 036). BC-001 = approved with business facts confirmed; the other nine = "READY FOR FINAL HUMAN REVIEW". **None is live** (QA/02 live check, 2026-10-09).
- **Step 1 — Master SEO Planning Layer** (2026-10-09). See §6.
- Paid research spend to date ≈ **$1.10 total** (progress.md; cap discipline applied per call). No paid calls were made in Step 1.

### CURRENT
- Step 1 complete. **Step 2 finalized 2026-10-10, correction pass and close-out complete** (`On-page SEO/`, `README.md` is the index; decision log `10-DECISIONS-RESOLUTION-LOG.md`). Counts: 147 rows → 73 ready after AWS / 41 pre-AWS preparation / 7 HOD input / 6 GSC baseline / 2 product-offer confirmation / 18 no change or not planned; 624 link specs; QC 65 checks pass. Open items are external only: HOD facts F-A1…F-E7 (`11`; F-E7 = bangles category taxonomy; F-A1 also gates BC-001 publication), engineering E-01…E-13 (`12`), GSC G-01…G-06 (`13`). Nothing is implemented; implementation is Class B (after AWS). AWS cut-over date/status remains UNKNOWN.

### 2026-10-24 status (verified read-only; see `Technical/2026-10-24-live-validation/` and `DEVELOPER-HANDOFF/`)
- **Implemented and seen live:** CloudFront/nginx front end; media on `media.houseofdiams.com`; new sitemap (261 URLs) + apex canonicals; BlogPosting + BreadcrumbList on 21 articles (Organization author on 19); test sub-category and two empty Hip Hop pages removed; `tennis` → `tennis-bracelet` 301; ten blog packages published.
- **Still open (verified):** nine `by-desgin` 301s; 15 empty listings still indexable and in the sitemap; By-Design group-page canonical; FAQPage on 35 pages; on-page title/meta/H1 specs not applied; shipping placeholder, returns terms and `/bespoke` '4–6 weeks'; `/contact` 307; 51 specified internal links absent.
- **Needs a decision:** BC-001 live against the hold (§12 #14); apex vs www host (§12 #16); tennis-bracelet slug (§12 #17); logging the $0.213552 backlink spend (§12 #18).
- **Backlinks:** research and planning only; outreach NOT started; no new links earned; gate G0 not cleared.

### BLOCKED / WAITING
- **Developer implementation of the open Step 2 items** (AWS front end is live; remaining work is in `DEVELOPER-HANDOFF/03`; post-cut-over re-checks stay Class C, §7).
- **User decisions and business-fact confirmations** (§12).
- **GSC data:** NOT AVAILABLE in this environment (the "SEO Gets" connector requires a subscription; no GSC export exists in the project). All GSC columns in `QA/01` read `NOT AVAILABLE`. Ask the user for Pages + Queries exports (16 months) if needed.

### NOT CONFIRMED by any project file (do not claim)
- GA4 setup/status; GSC property type (domain vs URL-prefix); whether publishing is paused for the migration; AWS cut-over date; whether the CMS content store is part of the AWS move (inferred only); who owns the redirect map.

---

## 6. SEO Execution Roadmap

### STEP 1 — Master SEO Planning Layer — **STATUS: COMPLETE (2026-10-09)**
Planning only. Nothing on the site, in the research, in the calendar, or in the keyword database was changed. Method: read the rules, loaded Stages 11–19 + calendar + drafted blogs, read-only crawled 256 sitemap URLs + 14 probes, joined by URL/ID, generated rows by script, marked unknowns `UNKNOWN — VERIFY` / `NOT AVAILABLE`.

| File | What it does |
|---|---|
| `QA/01-MASTER-SEO-IMPLEMENTATION-MAP.csv` | **Operational file.** 147 rows (one per important page; 184 PDPs represented by a template row + the keyword-owning PDP). 50 spec columns + 13 helper columns: live state, owner keyword/intent, recommended action, priority, schema/AEO/GEO/link opportunities, `AWS Class (A/B/C)`, flags. Filter `Row Group`, `Priority`, `Recommended Action`, `AWS Class`. |
| `QA/02-MASTER-SEO-IMPLEMENTATION-MAP.md` | Human-readable map: purpose, method, row groups, source hierarchy, **live-site baseline**, opportunities, priority counts, **AWS dependencies**, **conflicts C1–C13**, next actions. |
| `QA/03-SEO-IMPLEMENTATION-PRIORITIES.md` | Top-10 cross-cutting priorities + Critical/High/Medium/Low lists, each split into PRE-AWS PREPARATION / POST-AWS IMPLEMENTATION / POST-AWS VERIFICATION. Counts: CRITICAL 13, HIGH 64, MEDIUM 49, LOW 21. |
| `QA/04-KEYWORD-URL-OWNERSHIP-VALIDATION.md` | Validates Stage 15 ownership against live site + calendar: confirmed owners, missing ownership, conflicts (3a–3d), cannibalization (4), recommendations R1–R10. **Nothing resolved.** |
| `QA/05-ON-PAGE-OPTIMIZATION-BACKLOG.md` | **Input to Step 2.** Draft titles/metas/H1s/links/schema/AEO/GEO recommendations per page. Drafts need fact-check and re-validation after the commercial keyword decision. |
| `QA/06-PDP-AUDIT-APPENDIX.csv` | Per-product audit of the 184 product pages (title/meta/schema issues). |
| `QA/_build/` | `README.md` (rerun order), `scripts/` (generators + `mm_qc.py`, 20 checks), `evidence/` (raw crawl). Rerunning scripts **overwrites 01–06** — don't, unless asked. |

### STEP 2 — On-Page SEO Preparation — **STATUS: FINALIZED (2026-10-10) — specification only; not implemented**
Output (user-authorised destination `On-page SEO/`): `01-ON-PAGE-SEO-MASTER.csv` (147 rows), `02` overview, `03` title/meta, `04` H1/content + trust-critical pages, `05` internal links (+csv), `06` schema/AEO/GEO/image, `07` PDP (+csv), `08` priorities, `09` original decision register (audit trail), `10-DECISIONS-RESOLUTION-LOG.md` (+ `10-COMMERCIAL-KEYWORD-ASSIGNMENTS.csv`), `11` HOD facts request, `12` engineering inputs, `13` GSC request, `README.md`, `_build/` (generator + read-only `qc_step2.py`, 65 checks). Titles are **pre-suffix** values (the template appends ` | House of Diams`; the homepage is absolute). Statuses (counts in §0): `READY FOR IMPLEMENTATION POST-AWS`, `PRE-AWS PREPARATION`, `HOD INPUT REQUIRED` (includes BC-001's publication hold), `GSC BASELINE REQUIRED`, `CONDITIONAL — PRODUCT/OFFER CONFIRMATION`, `NO CHANGE REQUIRED`, `NOT PLANNED — CONDITIONAL`. No new research, no paid call, no live-site change. SERP type is validated for only 4 head terms; other commercial assignments are volume + DFS-intent evidence (stated per row).

### Later workstreams (not numbered steps)
* **Off-page SEO / Backlink Acquisition** (`Off-page SEO/Backlink Acquisition/`, 2026-10-10): research and planning; outreach not started.
* **Developer handoff** (`DEVELOPER-HANDOFF/`, 2026-10-24): consolidation of Steps 1–2 and live validation.

### Later steps
**No further numbered steps are established in the project files.** `progress.md` lists "Stage 20 (not defined)" with an optional recommendation in `19_stage_summary.md` §13 (ownership/business-fact decisions, light Stage 15/16 maintenance pass for 18.5 head terms, existing-page body audit for the 12 existing URLs) — **awaiting user decision, not scheduled.** `QA/02` §10 lists "Next actions" (decide → approve → confirm → ask engineering → prepare now → after AWS verify + implement B items). Do not invent new strategic stages.

---

## 7. AWS migration context

The site is migrating **Vercel + Supabase + Cloudflare R2 → AWS**. Developers own the migration. Evidence of the current stack (QA/02 §5): Next.js on Vercel; product images served from a Supabase storage host and a Cloudflare `*.r2.dev` host. The user stated the migration is in progress. Cut-over date, content-freeze window, URL stability and CMS location are **UNKNOWN — VERIFY** (open questions to engineering are in `QA/02` §8).

Classification used in `QA/01` (`AWS Class`):

| Class | Meaning | Examples from the project |
|---|---|---|
| **A — PRE-AWS SAFE WORK** | Can be prepared now; no site change | Metadata/title/H1 drafts; copy and hub-intro drafts; keyword mapping & ownership decisions; internal-link plans; redirect-map entries (planning); content briefs (incl. the 20 new Education pages); fact-checking; decision memos; GSC export request; baseline capture plan |
| **B — POST-AWS IMPLEMENTATION (WAIT)** | Template/code/infra changes and publishing into the new CMS | Schema changes (BreadcrumbList on articles, author entity, retire boilerplate FAQPage); canonical changes; noindex/robots rules; sitemap generation (incl. removing empty/test URLs, optional `<lastmod>`); pagination handling; slug/URL changes; **redirect implementation** (e.g. `by-desgin`→`by-design`); product/OG image URL changes (update schema `image`, OG tags, `/llms.txt`); publishing new CMS content (76 rows have a template/URL-level B task; 53 planned pages depend on a safe publishing window) |
| **C — POST-AWS VERIFICATION** | Re-check after cut-over | Status codes (200 for sitemap URLs; 404+noindex for unknown; 307 `/contact`, 308 `/hiphop` or deliberate replacements); canonicals (host/protocol/trailing slash; homepage canonical has no slash); indexability & `?sort=`/`?shape=`/`?metal=` = `noindex, follow` + canonical; robots.txt (AI-bot allowances); sitemap; redirects; schema validity & `priceCurrency: USD` for US/Googlebot; internal links rendering; image URLs resolving; CWV/TTFB vs baseline; `/llms.txt`; GSC property stays verified, new sitemap submitted |

Rules: a row's A/B/C is a **classification, not an implementation**. Do not implement B items before AWS. Never modify AWS migration work. When asked to do something, state which class it is (§16 step 6).

---

## 8. LIVE-SITE BASELINE — 2026-10-09 (point-in-time; do NOT treat as permanent after AWS)

> **Superseded in part by `Technical/2026-10-24-live-validation/` (fresh read-only crawl, 2026-10-24).** Changed since this baseline: host (apex canonical), sitemap (261 URLs), image hosts (media.houseofdiams.com), article schema (BreadcrumbList + Organization author), removed test/Hip Hop pages, ten published blog posts. Unchanged: by-desgin 404s, 15 empty listings, FAQPage ×35, shipping/returns/bespoke text, `/contact` 307. The bullets below are kept as the dated historical record.

Source: read-only crawl, `QA/_build/evidence/`; narrative in `QA/02` §5. One vantage point; not CrUX.

- **Sitemap:** 256 URLs (184 products + 72 other). Stage 1 (2026-09-17) had 198 (+62 / −4). No `<lastmod>`. All return 200, self-canonical.
- **Stack:** Next.js on Vercel, `cache-control: private, no-cache, no-store`, HTTP/2. robots.txt allow-all with disallow for /api, /cart, /checkout, /login, /signup, /profile, /wishlist, /maintenance; explicit allows for 7 AI user-agents; `Sitemap:` declared. `/llms.txt` exists. No hreflang.
- **Metadata:** `<Page> | House of Diams` on 255/256 (homepage has no brand and overlaps `/engagement-rings`, OV-13). 50 category/subcategory pages use boilerplate metas ("Browse X in Y."). 6 PDPs have placeholder-style meta; 65 PDP titles exceed 60 chars. One H1 on every sitemap page (homepage H1 = tagline).
- **Schema:** Organization everywhere; BreadcrumbList on category pages but **not** on articles; **FAQPage on 35 pages** (boilerplate, repeated); Product+Offer on all 184 PDPs; BlogPosting on 11 articles with inconsistent `Person` authors.
- **Thin/empty/test pages in the sitemap:** 18 pages with 0 products or test artifacts (`/collection`, `/engagement-rings/round-rings`, all `/wedding-bands/for-him*`, four `/wedding-bands/for-her/*` styles, five empty Fine-Jewellery types, `/hiphop/*` incl. `/hiphop/test-subcat`). Stage 12 D-13 forbids indexable empty/test pages.
- **404 / redirect issues:** all `/engagement-rings/by-desgin/*` URLs → **404, no 301** (new path `/by-design/`), including the Stage 15 keyword-owner URL for side-stone rings (ranking equity at risk). `/contact` → 307 to a modal (`/?contact=open`); `/hiphop` → 308 to `/shop`. Test product and one other Stage-1 product now 404. Slug typos still live: `solitare`, `anniversay`, `pavee`, singular `bracelet`, `toi-moi`.
- **Trust-critical content defects:** `/shipping` shows placeholder text ("new test black / test desc"); `/returns` shows no return terms; `/bespoke` says "4–6 week typical lead time" (confirmed fact ≈ 3–4 weeks); unverified claims live ("IGI Certified", "IGI / GIA", "Complimentary Overnight Shipping", "Lifetime Warranty"); expired-looking "September sale … HOUSEOFDIAMS2026" banner; PDP material label "Gold Vermil" truncated.
- **Pagination:** `/shop` and `/engagement-rings` `?page=2` self-canonical with identical titles; `/blog?page=2` canonicalises to `/blog`.
- **Performance (indicative):** HTML TTFB 1.2–4.5 s, 130–515 KB/page; largest page 0.53 MB (well under Googlebot's ~2 MB fetch limit → no byte-optimization needed). Geo/currency cookies set from IP — confirm US/Googlebot sees USD.
- **Publishing status:** none of the 62 scheduled items is live. Six dated 2026-10-04…10-09 have passed unpublished: BC-001, BC-004, BC-035, BC-018, BC-036, BC-006. Whether publishing is paused for AWS is UNKNOWN.
- **GSC:** NOT AVAILABLE. Stage 3 "ranked keyword" positions are DataForSEO estimates, not GSC.
- **Ranking-equity articles (update in place, never change URL, baseline GSC first):** CVD vs HPHT (19 ranked keywords), lab-grown vs natural, 14K vs 18K, how-to-choose. Only 1 of 11 Education-owned articles sits under `/education`.

---

## 9. Blog / content system

**Source of truth for dates/topics/primary keywords:** `FINAL-BLOG-CALENDAR/BLOG_CALENDAR_FINAL.csv` (112 rows). Do not create another calendar, move dates, or swap topics. "Write this blog" = execute an approved calendar item using the existing system (`reference/BLOG_PUBLISHING_CONTEXT.md` §22).

**Calendar IDs:** `BC-###` (blog), `EDU-<AREA>-##` (Education, e.g. EDU-LG lab-grown, EDU-4C 4Cs, EDU-SHP shapes, EDU-MET metals, EDU-RJG rings/jewellery guides, EDU-CERT, EDU-NAT, EDU-GEN), `COM-*` (commercial pages), `BLOG-*`/`BRAND-*`/`SUP-*` (hubs/brand/support), `BLOG-WR-TYPES`, `BC-004-DEC-REFRESH`. Key columns: `content_id`, `publish_date`, `locked_date_status`, `status`, `production_status` (`READY_TO_WRITE` 51 · `OWNERSHIP_CONFIRMATION` 8 · `BUSINESS_FACT_REQUIRED` 3 · `BACKLOG` 50 unused), `primary_keyword`, `secondary_keywords`, `search_intent`, `target_owner`, `internal_link_targets`, `cannibalization_status`, `notes`.

**Workflow** (BUSINESS → DEMAND → INTENT → EXISTING-CONTENT CHECK → CONTENT JOB → RESEARCH → ARTICLE → INTERNAL LINKS → SEO/AEO QA → HUMAN REVIEW → PUBLISH → MEASURE → UPDATE):
1. Locate the item in the calendar; read keyword, intent, owner, boundary, cannibalization notes.
2. Read the Stage 19 brief + boundaries + business-fact requirements (`content-strategy/19_*`) where the item has one; blog items are Blog-owned by the calendar only (no Stage 15 owner).
3. Check ownership (`architecture/15_*`), existing content (`content-strategy/10_*`, `13_*`), internal-link requirements (`19_internal_link_requirements.csv`, `architecture/16_*`).
4. Use existing SERP/PAA/AIO/entity research (`serp/analysis`, `17_*`, `18_*`, calendar `call2_serp_analysis.csv` / `round2_*`). Never write from the keyword alone.
5. **AEO answer-first:** question → direct answer → explanation → evidence → details → next action. Tables/steps/lists only where the SERP/need supports them. FAQ only when useful and non-duplicative. No arbitrary word count.
6. **GEO/entity:** consistent entity facts (confirmed only), clear author/entity context, credible external sources; never fabricate expertise, labs, certifications, sourcing, awards, numbers.
7. Internal links: natural descriptive anchors per Stage 16/19 (Blog→Education, Education→Blog, Blog→Product/Category, Hub↔Spoke); don't invent URLs.
8. Schema per article rules in `blogs/*/seo-metadata.md` (template currently lacks BreadcrumbList on articles, author=Person; schema fixes need a code change = Class B).
9. QA (content, SEO, AEO, HOD facts, cannibalization); **every AI-generated element (body, title, meta, structured data, alt text) manually fact-checked.**
10. **Human review** before publishing. "Publish" means a QA'd, publish-ready draft; don't touch the CMS or live site unless explicitly told.
11. CMS-ready packaging and client handoff via the `blogs/bc-0xx/` package.

**Package structure** (each `blogs/bc-0xx/`): `BC-0xx.md` (draft/source), `BC-0xx-<slug>.md` (final article), `BC-0xx-qa.md` (QA record), `README.md` (CMS checklist), `cms-entry.md` (value for every CMS field), `article-content.html` (paste-ready body), `article-content.md` (formatting map), `seo-metadata.md` (approved title/meta/keywords/schema notes), `image-requirements.md`, `internal-links.md`.

**BC-001** (`blogs/bc-001/`, "How Long Does a Custom Engagement Ring Take?", calendar date 2026-10-04, carried forward from 2026-09-29) is the completed reference example of the full workflow: approved, business fact confirmed (2–3 weeks + 6–9 days, ~3–4 weeks, stone-dependent, no guarantee, no holiday cut-off stated), CMS checklist (untick "Show on website" first; Article Title fixes the URL `/blog/how-long-does-a-custom-engagement-ring-take`; 4 live links + 2 conditional anchors left as plain text). **DO NOT MODIFY BC-001.** Note: the calendar row still shows `READY_TO_WRITE` — leave it. **Update 2026-10-24: the page is LIVE at `/blog/how-long-does-a-custom-engagement-ring-take` with the 'insured shipping' wording; decision needed (§12 #14).** **Publication status (2026-10-10): HELD pending F-A1** — the approved meta/intro/article say 'insured shipping', which is not a confirmed fact (SR-02 in `On-page SEO/10-DECISIONS-RESOLUTION-LOG.md` §9). If HOD confirms insurance, the approved wording may proceed after normal human review; if not, a separate explicitly authorized content revision is required first. The package files are unchanged. Pending separate from the package: the live `/bespoke` "4–6 week" wording must be corrected (user said they're handling it) and schema items need a website code change.

Other packaged blogs (BC-003/004/006/007/008/009/018/035/036) = "READY FOR FINAL HUMAN REVIEW". Next unpackaged scheduled items are in the calendar (BC-024 2026-10-23 etc.); items with `OWNERSHIP_CONFIRMATION` or `BUSINESS_FACT_REQUIRED` must not be written until resolved (§12).

---

## 10. Keyword ownership rules

- **Existing ownership (Stage 15) is authoritative.** 1,936 keywords mapped to 27 target pages; its central claim — **no keyword has two HOD owners** — holds (`15_cannibalization_check` B-check = 0; Step 1 found 0 exact duplicate primaries across 147 rows).
- Do **not** casually reassign a primary keyword. Do **not** create duplicate primary ownership. A new opportunity that conflicts with ownership/boundaries → **STOP and flag**; never change silently.
- Cannibalization must be flagged (Stage 15 "E" pairs and `QA/04` §4 are carried forward: e.g. EDU-LG-00↔EDU-LG-03 HIGH; EDU-LG-01↔02, LG-02↔05, 4C-00↔4C-01, CERT-00↔CERT-01, 4C-06↔SHP-00 MEDIUM).
- Unresolved ownership conflicts need an explicit user decision; new Education-page ownership must be **ratified** where Stage 14/15 have no owner.
- Commercial keyword decisions already made are preserved (e.g. calendar states COM-BESPOKE reserves "custom engagement ring" 40,500 and "design your own engagement ring" 5,400 — but these are **not** mapped in Stage 15 → see below). Broad commercial heads stay off blog posts.

**Update 2026-10-10:** commercial keyword ownership, the 12 Education primary-keyword mismatches and the 8 ownership confirmations were resolved under the user's delegation — record: `On-page SEO/10-DECISIONS-RESOLUTION-LOG.md` and `10-COMMERCIAL-KEYWORD-ASSIGNMENTS.csv` (Stage 15 files untouched). The QA/04 status below is the 2026-10-09 starting point.

**Status from `QA/04-KEYWORD-URL-OWNERSHIP-VALIDATION.md` (2026-10-09, nothing resolved):**
- 11 existing owner URLs confirmed live; **1 stale** (COM-ER-SIDESTONE: registry URL `/engagement-rings/by-desgin/side-stone-rings` returns 404; live URL is `/by-design/`); 15 proposed/pending owners not built.
- Missing ownership: **9** commercial hubs/categories + **38** subcategories have no ratified keyword (Stage 12 D-19 data gap — candidate heads already exist in project data, zero cost: e.g. 'engagement ring' 673,000; 'diamond earrings' 74,000; 'tennis bracelet' 135,000; 'lab grown diamonds' 135,000); `/bespoke` has none mapped; 4 new Education pages have no Stage 14/15 owner; 50 calendar primaries are outside the Stage 15 map (new research).
- **12 Education pages** have a different primary keyword in the Stage 17/19 brief vs the final calendar (EDU-MET-01, 4C-00, SHP-00, RJG-02, LG-00, LG-09, 4C-01, 4C-03, 4C-05, 4C-06, 4C-07, MET-00) — same page, so not two pages competing, but the title/H1/volume basis differs. **Ratify before writing the 20 new pages.** (Recommendation R2 only *proposes* defaulting to the SERP-validated calendar term with the Stage 15 term as co-primary — not adopted.)
- Recommendations R1–R10 are proposals requiring user decision.

---

## 11. Operating rules (SEO implementation)

1. Research first; reuse existing datasets.
2. No fabricated HOD facts. Unknown → **VERIFY**. Never present assumptions as facts.
3. Don't change SEO strategy, keyword ownership, architecture, or the final calendar without explicit instruction. Preserve existing architecture and strong indexed URLs; no URL change without migration reasoning (1:1 301).
4. Don't modify source research files unless explicitly instructed.
5. Don't modify the live website, repo, CMS, robots.txt, sitemap.xml, redirects, metadata unless explicitly instructed.
6. Distinguish **recommendation** from **implemented change**, and say which in every report.
7. Avoid keyword cannibalization; don't create duplicate content; intent before wording; search volume alone never decides priority; no thin collection/filter pages; filters stay non-indexable unless they pass the Stage 12 D-07 gate.
8. No artificial brand mentions; no keyword stuffing; no guaranteed ranking / AI Overview / AI-search claims; no fake precision or arbitrary SEO scores; don't invent DataForSEO metrics; KD is a third-party metric, not a ranking probability.
9. Playbook tactics (URL refreshing, exact-match domains, clicks/PageRank claims, parasite SEO) are **off** unless the user explicitly asks. Don't auto-apply byte-level/2 MB HTML tactics (site pages are far below the limit).
10. Use `superseo:*` skills where they fit; if they conflict with HOD architecture or the user, HOD architecture and the user win.
11. Keep outputs modest in chat — never dump thousands of rows; write to files.
12. Security: never place credentials (DataForSEO, GitHub tokens, `.env` contents) in CLAUDE.md, CSVs, markdown, code or commits. DataForSEO credentials live only in the Claude Desktop MCP configuration.

### DataForSEO / paid research rules (verbatim intent — do not weaken)
DataForSEO (via MCP) is the primary keyword/SERP/competitor data source. Existing datasets must be **reused**; don't repeat completed research or paid calls without a reason. **Before every new paid call:**
1. Verify pricing.
2. Verify the exact task/configuration (endpoint, why appropriate, number of requests/tasks).
3. State the maximum expected cost.
4. Obtain user approval (**each paid call** individually — as practised throughout the project).
5. Run **only** the approved configuration.
6. Record actual cost (`cost-log.csv`, `progress.md`).
7. Save raw output locally and a processed dataset; reuse it afterward.
Also: use the cheapest suitable endpoint; don't use Google Ads keyword APIs as a substitute for DataForSEO Labs organic metrics; no Clickstream unless justified; market = US (2840) / English (`en`). Keep `cost-log.csv` and `progress.md` current for any new spend. **No paid calls have been made since the final calendar; Step 1 cost $0.00.**

### Google / SEO facts established by the project (`SEO_PLAYBOOK.md`, `VERIFICATION_AUDIT_2026-10-04.md`)
- **FAQ rich results were discontinued** (stopped appearing 2026-05-07). FAQPage is still valid schema but earns no rich result — **do not add FAQPage automatically**; add on-page FAQs only for users. The live site's boilerplate FAQPage on 35 pages is a clean-up item.
- GSC clicks/impressions/CTR/position are **measurement metrics**, not ranking factors. Google says it uses aggregated, anonymised interaction data for relevance but doesn't publish how — don't claim "more clicks = higher rankings".
- Core Web Vitals are used by Google's ranking systems but there is no single page-experience signal; CWV is one part, not the whole.
- No ideal word count; no requirement to chunk content for Google Search (use clear sections for readers).
- Googlebot fetch limit ≈ 2 MB per URL (headers included, uncompressed; each CSS/JS file has its own counter; PDFs 64 MB; "not set in stone") — apply only when relevant.
- `llms.txt` is not used by Google Search (neither helps nor harms); not required for Google AI features.
- AEO/GEO are industry terms; for Google, optimizing for AI search is part of SEO. "SEO→AEO→GEO" is a project planning framework, not Google's architecture. "Topical authority" is an industry strategy, not a published Google score for non-news sites.
- Search Console has a **Generative AI performance report** (impressions in AI Overviews/AI Mode) and a **Search generative AI** setting (defaults to include) — HOD action: check the property is not set to exclude (GSC currently inaccessible → VERIFY).
- Manually fact-check every AI-generated element (body, titles, meta descriptions, structured data, alt text) before publishing (Google guidance 2026-10-01). IPTC `DigitalSourceType` guidance for AI-generated ecommerce images: confirm scope before relying on it.
- Ahrefs is not connected/used in this project.

---

## 12. Open decisions & known issues (real, unresolved — do NOT resolve automatically)

| # | Issue | Why it matters | Status | Owner / decision | Dependency | File |
|---|---|---|---|---|---|---|
| 1 | **Commercial keyword ownership (Stage 12 D-19 gap):** 9 hubs, 38 subcategories, `/bespoke` own no ratified keyword; calendar claims COM-BESPOKE / COM-WB / style heads not mapped in Stage 15 | Without it, metadata/H1 for commercial pages can't be finalised and cannibalization with blog posts is unmanaged | **RESOLVED 2026-10-10** (delegated; assignments in `On-page SEO/10-…csv`; SERP not validated for most heads; any validation needs a priced DataForSEO plan + approval) | User (delegated) | — | `QA/04` §2, §3c, R4; `QA/01` |
| 2 | **COM-LG-HUB** (commercial Lab-Grown hub; 'lab grown diamonds' 135,000 unowned; Stage 12 D-05 says conditional; live catalogue already lab-grown). Also resolve 'lab grown diamond engagement rings' COM-ER vs COM-LG-HUB | Largest unowned head term; homepage/ER positioning | **RESOLVED 2026-10-10 (OD-02): no separate hub now**; reverses only if HOD sells loose lab-grown stones (F-E2); origin heads → /engagement-rings once F-E1 confirmed | User (delegated) / HOD facts F-E1, F-E2 | — | `QA/04` R4/R5; `QA/02` C6 |
| 3 | **Education page ownership ratification:** 8 `OWNERSHIP_CONFIRMATION` items (EDU-RJG-BR, EDU-RJG-NL, EDU-INS, EDU-WB-GUIDE new; EDU-LG-09 co-primary 'how to tell if a diamond is real'; EDU-RJG-01 'engagement ring settings' review carried from Stage 19; EDU-RJG-03 care activation; BLOG-WR-TYPES Blog-vs-Education) + **12 primary-keyword mismatches** (calendar vs Stage 17/19) | Pages can't be written until owner/primary is fixed; first date at stake: EDU-LG-00 (MUST_PUBLISH 2026-10-21) | **RESOLVED 2026-10-10 (OD-03 R2, OD-04)** — 'types of wedding rings' = Education page EDU-WB-TYPES (calendar ID BLOG-WR-TYPES; calendar `target_owner` updated to `EDU-WB-TYPES` on 2026-10-10, only that field) | User (delegated) | Pages may be written; human review still required | `QA/04` §3a, §3b, R2, R3; calendar |
| 4 | **`/engagement-rings/by-desgin/*` redirect** (404, no 301; Stage 15 keyword-owner URL for side-stone) | Ranking-equity loss | **Resolved as specification (OD-06)** — 9 1:1 301s in `On-page SEO/10` §5; not implemented | Developers implement (E-03/E-04) | AWS | `QA/02` C1; `QA/03` P1 |
| 5 | **`/contact`** — Stage 12 expects an indexable page; live is a 307 to a modal | Indexable contact/entity page vs modal | **Resolved (OD-09)**: build a real /contact page; contact facts F-C2 pending | Developers (E-12) / HOD | AWS | `QA/02` C7 (`BRAND-CONTACT`) |
| 6 | **Empty/test pages in sitemap (18)** — noindex + sitemap exclusion vs populate | Index integrity (Stage 12 D-13) | **Resolved (OD-07)**: per-page dispositions in `On-page SEO/10` §5; not implemented | Developers (E-05) | AWS (sitemap/noindex = Class B) | `QA/02` C2; `QA/03` P2 |
| 7 | **Trust-critical facts:** shipping (placeholder text, "overnight shipping" claim), returns terms, bespoke lead-time ("4–6 weeks" vs confirmed ~3–4), certification labs (IGI/GIA), warranty claim, founder names/roles, platinum, cleaning/appraisal, holiday cut-offs | Public statements contradict or lack confirmed facts; AI engines quote them; blocks BC-005, BC-015, BC-004 December refresh | **Partly resolved (OD-08)**: bespoke timeline applied (incl. 'from design approval', user 2026-10-10); other claims removed/neutral; questionnaire `On-page SEO/11` pending; BC-001 publication held for F-A1 ('insured shipping') | HOD | Content freeze | `QA/02` C8, C10; calendar (`BUSINESS_FACT_REQUIRED` ×3) |
| 8 | **Content freeze / publishing window:** 6 dated items passed unpublished (BC-001, 004, 035, 018, 036, 006); is publishing paused for AWS? Does CMS edit happen in Supabase CMS or code? | Calendar dates slipping; Class B publishing | UNKNOWN — VERIFY (intake prepared: `On-page SEO/12-ENGINEERING-INPUTS.md`) | Engineering | AWS | `QA/02` §8 |
| 9 | **FAQ page vs Education boundary** (Stage 14 D14-30 says one-line + link; live FAQ answers in full) and `/engagement-rings` vs `/by-design`, eternity WB vs FJ rings one-home decisions | Cannibalization | **Resolved (OD-10, OD-06, OD-16)**: FAQ one-line + link; group page canonical; eternity single home | User (delegated) | — | `QA/02` C9; `QA/04` R6, R8 |
| 10 | Oval-floral PDP renamed 'Oval Marquise Side-Stone…' (slug unchanged) vs Stage 15 'marquise oval diamond' owner; title now contains the COM-ER-SIDESTONE term | Boundary risk (MEDIUM) | **Resolved (OD-15)**: title/H1 'Oval Marquise Diamond Engagement Ring', schema name = H1, slug unchanged; live change waits for GSC baseline | User (delegated) | G-01 | `QA/02` C11; `QA/04` §3d |
| 11 | Housekeeping: second research copy `~/Desktop/HOD-SEO-Research`; `.gitignore` + `QA/` uncommitted | Two copies can drift; `.env` safety | Open | User | — | `QA/02` C13 |
| 12 | jewelry vs jewellery label decision (Stage 12 D-15) | Titles/H1s | **RESOLVED 2026-10-10 (OD-05): American English; slugs unchanged** | User | — | `architecture/12_ia_decision_log.md` |
| 13 | GSC data unavailable; `Search generative AI` setting unchecked | No performance baseline | Needs user export / access (request prepared: `On-page SEO/13-GSC-DATA-REQUEST.md`) | User | — | `reference/…AUDIT…` item 10; tooling note in memory |
| 14 | **BC-001 publication hold:** approved package says '6–9 days of insured shipping'; insurance is not a confirmed fact (SR-02) | Unverified claim must not be published; AI engines quote it | **HELD 2026-10-10; page found LIVE 2026-10-24** with that wording (title, meta, body) — NEEDS DECISION; package protected/unedited | HOD (F-A1); user for any content revision | Insurance confirmation or an explicitly authorized revision | `On-page SEO/10` §9 SR-02; `11` F-A1 |
| 15 | **Bangles category taxonomy (F-E7):** `/fine-jewellery/bracelet/bangles` holds 2 link bracelets, no bangles | Label vs contents mismatch; shares scope with `/chain-link` | **HELD**: interim 'Diamond Link Bracelets' wording, status `CONDITIONAL — PRODUCT/OFFER CONFIRMATION`; no keyword assigned | HOD (F-E7) | — | `On-page SEO/10` §7; `11` F-E7 |
| 16 | **Preferred host:** live canonicals, sitemap, robots and llms.txt now use `https://houseofdiams.com` (apex); `www` still returns 200 with canonical to the apex, no 301; all project documents assume `www` | Duplicate-host handling, GSC property, backlink targets | **NEEDS DECISION (found 2026-10-24)** | User / developers | GSC property type | `DEVELOPER-HANDOFF/03` MIG-03 |
| 17 | **Tennis bracelet URL:** `/fine-jewellery/bracelet/tennis` now 301 → `/tennis-bracelet`; ownership files and assignments still list the old path | Unrecorded URL decision against 'slugs unchanged' | **NEEDS DECISION (found 2026-10-24)** | User (ownership change needs approval + logging) | — | `DEVELOPER-HANDOFF/03` MIG-09 |
| 18 | **Backlink spend not logged:** C1–C6 ($0.213552) are recorded only in `Off-page SEO/Backlink Acquisition/05-…` | `cost-log.csv` / `progress.md` incomplete | Pending user decision — not changed | User | — | `DEVELOPER-HANDOFF/03` OFF-03 |

---

## 13. DO NOT

- **Do not modify the live website** (site, repo, CMS, robots.txt, sitemap.xml, redirects, metadata) unless explicitly instructed.
- **Do not modify `FINAL-BLOG-CALENDAR/BLOG_CALENDAR_FINAL.csv`** or create another calendar (the one approved `BLOG-WR-TYPES.target_owner` edit of 2026-10-10 is the only change so far).
- **Do not change keyword/URL ownership** without explicit approval and logging; never silently resolve conflicts.
- **Do not redo completed research** (Stages 1–19, calendar rounds) or rerun stage build scripts.
- **Do not run paid DataForSEO calls without approval** (§11 procedure).
- **Do not invent business facts**; never convert `BUSINESS_FACT_REQUIRED` into text.
- **Do not overwrite source-of-truth files with generated outputs.**
- **Do not treat recommendations (QA/01–06) as implemented.**
- **Do not modify BC-001** (anything in `blogs/bc-001/`) or its calendar row.
- **Do not modify or interfere with AWS migration work.**
- **Do not start any step after Step 2** unless the user asks (Step 2 is finalized; do not regenerate `On-page SEO/` outputs without a reason — `_build/s2_write.py` overwrites them).
- **BC-001 is already live (2026-10-24)**; do not edit its package or calendar row. Resolve via F-A1 confirmation or an explicitly authorized content revision (§12 #14).
- Do not rerun `QA/_build/scripts` (they overwrite `QA/01…06`) unless asked.
- Do not edit `dataforseo/raw/`, `serp/raw/`, `QA/_build/evidence/` (dated snapshots).
- Do not read, print or copy `.env`; never put tokens/credentials into any file or commit.
- Do not commit or push unless asked. Do not edit `~/Desktop/HOD-SEO-Research`.
- Do not copy FAQ boilerplate or add FAQPage schema automatically; do not claim FAQ rich results.
- Do not make guaranteed ranking/AIO/AI-citation claims.
- New Education pages: owners and primary keywords were ratified 2026-10-10 (`On-page SEO/10`); writing is allowed but every page still needs human review before publishing.
- Do not assume the live-site baseline (§8) is still true after AWS.

---

## 14. Tooling notes

- **GSC:** unavailable (SEO Gets connector needs a subscription; no export in project).
- **Live crawling:** use `curl` (Python `urllib` fails TLS verification on this Mac). The site takes ~4 s per HTML fetch — use ~4 parallel workers; GET-only, no forms/logins. Crawl script: `QA/_build/scripts/crawl.py`.
- **Python:** `QA/_build` scripts run with plain `python3` (not `-I`). Rerun order in `QA/_build/README.md` (overwrites 01–06).
- **Skills likely relevant:** `superseo:*` (content-brief, keyword-deep-dive, page-audit, write-content, semantic-gap-analysis, featured-snippet-optimizer, eeat-audit), `anthropic-skills:hod-blog-engine`, `houseofdiams-website-seo`, `houseofdiams-schema-markup`, `seo-aeo-geo`. HOD architecture and the user's instructions win on conflict.
- Cost so far: ≈ $1.10 DataForSEO (see §3 for the cost-log discrepancy note).

---

## 15. Quality-control checks run when writing this file (2026-10-09)

Folders and files named in §2/§4 were verified to exist, including the 10 `blogs/bc-*` folders, the 6 `QA/` files + `_build/`, the 3 `reference/` files, the 3 empty-placeholder/ignored items, and `~/Desktop/HOD-SEO-Research`. Calendar counts (112 rows; 62 scheduled; 50 unused; 51/8/3 production statuses) were computed from the CSV. Step 1 = COMPLETE, Step 2 = FINALIZED 2026-10-10 (specification only). Not verified (marked VERIFY in text): GA4/GSC configuration, AWS timeline, CMS location, Step 2 output folder, content of every Stage 1–19 CSV (large datasets were not read in full).

---

## 16. Future session startup procedure

1. **Read this CLAUDE.md** (then `Keywords/content SEO/CLAUDE.md` if touching research/blog work).
2. **Identify the current execution step** (§6): Step 1 complete; Step 2 finalized 2026-10-10 (specification only, not implemented); implementation is post-AWS.
3. **Read the source-of-truth files for the task** (§3/§4): for on-page work → `QA/05`, `QA/01` (filter rows), `QA/04`; for a blog → calendar row + Stage 19 brief/boundaries + `BLOG_PUBLISHING_CONTEXT.md`.
4. **Check open decisions/blockers** (§12) — don't proceed on a blocked item; ask.
5. **Check AWS migration status** with the user (cut-over date, content freeze) — it is UNKNOWN in the files.
6. **Classify the request** as PRE-AWS (A), POST-AWS implementation (B) or POST-AWS verification (C), and say so.
7. **Don't duplicate completed work**; reuse datasets; no paid call without approval.
8. **Don't modify protected files** (§4/§13) without instruction.
9. **Write outputs to the right folder:** generated planning docs → `QA/` (new numbered files; don't overwrite 01–06 unless asked); Step 2 outputs → `On-page SEO/` (confirmed destination); blog packages → `Keywords/content SEO/blogs/bc-0xx/`.
10. **Report clearly** what was changed and what was not, labelling recommendation vs implemented, and update the relevant tracking files (`progress.md`, `cost-log.csv`) and this CLAUDE.md status sections when a step completes.

---

## 17. Maintaining this file

Update §5/§6 when a step starts or finishes, §12 when a decision is made or a new blocker appears (record who decided and when), and §8 only with a *new dated* baseline label. Consolidate rather than append; keep one source for each fact; remove contradictions. Never add credentials.
