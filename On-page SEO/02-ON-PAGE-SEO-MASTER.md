# 02 — On-Page SEO Master (human-readable)

Generated 2026-10-10 (Step 2A decision resolution + Step 2B finalization of the 2026-10-09 package). **Everything here is a specification. Nothing was implemented; no website, CMS, redirect, sitemap, robots.txt or schema was touched; no paid DataForSEO call was made.** The operational file is `01-ON-PAGE-SEO-MASTER.csv` (147 rows, one per important page of the Step 1 map).

## 1. What changed in Step 2A/2B

* **Decisions OD-01…OD-19 were resolved** under the user's delegation (2026-10-10): 15 adopted, 1 partly adopted pending HOD facts, 3 awaiting external input with the specification not blocked. Record: `10-DECISIONS-RESOLUTION-LOG.md`; original proposals preserved in `09`.
* **Commercial keyword ownership is assigned** for the category hubs, subcategories and /bespoke (`10-COMMERCIAL-KEYWORD-ASSIGNMENTS.csv`) — one primary per URL, no duplicates, SERP-validation status stated per row.
* **Education**: all 12 primary-keyword mismatches resolved (R2) and all 8 ownership items resolved; 'types of wedding rings' is a single Education page.
* **American English** is applied to all recommended copy, nav labels and anchors; slugs unchanged.
* **Status vocabulary replaced**: rows are now `READY FOR IMPLEMENTATION POST-AWS`, `PRE-AWS PREPARATION`, `HOD INPUT REQUIRED`, `ENGINEERING INPUT REQUIRED`, `GSC BASELINE REQUIRED`, `CONDITIONAL — PRODUCT/OFFER CONFIRMATION`, `NO CHANGE REQUIRED`, `NOT PLANNED — CONDITIONAL`. Engineering/HOD/GSC dependencies are itemized per row in `Remaining Dependencies`.
* New deliverables: `11-HOD-CLIENT-FACTS-REQUEST.md`, `12-ENGINEERING-INPUTS.md`, `13-GSC-DATA-REQUEST.md`.

## 2. Scope and counts

Rows: **147** (all Step 1 rows; excluded by rule: cart, checkout, login/signup/profile/wishlist, search, sort/filter/shape/metal parameter URLs, tracking URLs). The 184 PDPs are covered by one template row + the priority list in `07`.

| Row group | Rows | CRITICAL | HIGH | MEDIUM | LOW |
|---|---|---|---|---|---|
| COMMERCIAL SUBCATEGORY | 40 | 1 | 4 | 35 | 0 |
| PLANNED BLOG | 32 | 0 | 13 | 13 | 6 |
| PLANNED EDUCATION | 21 | 1 | 7 | 9 | 4 |
| CONDITIONAL EDUCATION | 13 | 0 | 0 | 0 | 13 |
| CORE LIVE | 11 | 2 | 4 | 3 | 2 |
| EXISTING ARTICLES (Education-owned) | 11 | 0 | 7 | 3 | 1 |
| COMMERCIAL CATEGORY | 9 | 0 | 4 | 5 | 0 |
| LEGACY / REDIRECT | 5 | 1 | 0 | 0 | 4 |
| HUBS | 2 | 0 | 1 | 1 | 0 |
| PRODUCT PAGES | 2 | 0 | 1 | 1 | 0 |
| CONDITIONAL COMMERCIAL | 1 | 0 | 1 | 0 | 0 |

**Priority:** CRITICAL 5 · HIGH 42 · MEDIUM 70 · LOW 30

**Status (primary):**

| Status | Rows |
|---|---|
| READY FOR IMPLEMENTATION POST-AWS | 73 |
| PRE-AWS PREPARATION | 41 |
| NOT PLANNED — CONDITIONAL | 13 |
| HOD INPUT REQUIRED | 7 |
| GSC BASELINE REQUIRED | 6 |
| NO CHANGE REQUIRED | 5 |
| CONDITIONAL — PRODUCT/OFFER CONFIRMATION | 2 |

**Readiness view:** **73 rows are ready for implementation after AWS**; 15 are blocked by a specific external input (HOD 7 · GSC baseline 6 · product/offer confirmation 2); 41 are pre-AWS writing tasks (content still to be written — the specification is final); 5 need no change; 13 are conditional/not planned.
**AWS class** (class of the implementation step): A = prepare/write now (57 rows) · B = apply after AWS (85 rows) · C = verify only (5 rows). Every live-page change also has a Class C verification step after cut-over.
**Dependency flags (independent of status):** 35 rows list HOD facts (most are enhancements — the page ships with neutral wording), 10 rows list a GSC dependency (blocking only where Status says so), 131 rows list engineering inputs (E-01/E-02 apply to all Class B rows).

## 3. Facts verified live (read-only, 2026-10-09; unchanged by Step 2A)

| Check | Result | Consequence |
|---|---|---|
| Title suffix | `<title>` = `og:title` + ` \| House of Diams`; the homepage uses an absolute title | All titles are **pre-suffix values**; the CSV also shows the rendered title and its length |
| Step 1 draft metas | Several repeated unconfirmed claims (free insured delivery, 15-day returns, family-run since 2014, free CAD consultation) | Not adopted; no recommended title/meta/H1 contains such a claim |
| PDP structured data | JSON-LD name ≠ H1; sku UUID ≠ visible SKU; six metals with one price; schema breadcrumb ≠ visible path | In `07` |
| PDP descriptions | 'IGI certified GH / VVS', 'Care & Warranty', shipping block | Unverified — replaced with neutral policy links until F-A/F-B answers |
| Product-set comparison (initial HTML) | /wedding-bands = /for-her (7 = 7); /engagement-rings = /by-design (24 = 24); T-bar, pendant, solitaire and toi et moi sets are disjoint | Drives OD-06 and OD-16 |

## 4. Controlled vocabularies

* **Priority:** CRITICAL (index-integrity / trust-fact / ranking-equity risk, or a MUST_PUBLISH page due within ~2 weeks) · HIGH · MEDIUM · LOW.
* **Ownership Status:** `RATIFIED 2026-10-10 (delegated)` · `RATIFIED — Stage 15 owner` · `RESERVED — INACTIVE UNTIL POPULATED` · `HELD — AMBIGUOUS` · `NOT BUILT` · `NO KEYWORD BY DESIGN` · `NO KEYWORD — NO MEASURED DEMAND` · `BLOG-OWNED` · `CONDITIONAL — NOT PLANNED`.
* **Action labels:** `REPLACE — FINAL`, `KEEP`, `HOLD` (noindex/canonical rows), `CARRY APPROVED` (packaged posts), `FINAL DRAFT` (pages to be written).
* **Remaining Dependencies:** `HOD: F-xx` (see 11) · `ENG: E-xx` (see 12) · `GSC: G-xx` (see 13).

## 5. Page-family rules (final)

| Family | Title | Meta | H1 | Content | Notes |
|---|---|---|---|---|---|
| Homepage | Brand-led, absolute | Offer summary, no claims | Keep tagline | Entity intro (verified facts only); remove unverified badges | D-18 |
| Commercial hubs / subcategories | Assigned keyword in plain US wording | "Shop <type>: <what defines it>" — no shipping/returns/certification | Plain type name | Short unique intro, 1–2 Education links, no boilerplate FAQ | Empty pages noindex; duplicates canonicalized |
| PDP | Template: shape + type + carat (≤~43 chars pre-suffix) | Spec-based, from the product record | Visible name = schema name | Specs, description and variant rules | `07` |
| Existing Education articles | Keep when aligned; assigned primary otherwise | Answer-first rewrite | Keep when aligned | Refresh in place; PAA as sections | URL never changes; GSC baseline for equity URLs |
| New Education pages | Calendar primary | Final draft | Final draft | Stage 19 brief sections | Owners ratified |
| Blog posts | 10 approved values carried; others final drafts | ≤155 chars, no unverified claims | Draft | Per calendar + PAA | Packages untouched (BC-001 DNM) |
| Policy / trust pages | Plain descriptive | Neutral | Keep | Rewrite from confirmed facts only | HOD questionnaire |

## 6. How to use the CSV

Filter `Status` + `AWS Class` for queues; `Remaining Dependencies` for what each row still needs; `Decision Resolution` links each row to its adopted decision (`10`). Titles/metas/H1/links/schema columns are copy-ready for rows whose Status allows.

## 7. Limits

* No GSC data (nothing here uses clicks, impressions, CTR or positions; DataForSEO positions quoted for equity URLs are Stage 3 estimates).
* No new keyword research; volumes/KD/intent labels come from existing project files. **SERP type is NOT validated for most commercial heads** (only side-stone, 'lab grown diamonds', 'lab diamonds', 'natural diamonds').
* Post-AWS state (URLs, templates, image hosts, CMS) is UNKNOWN; observations are dated 2026-10-09 and must be re-verified (Class C).
* Titles/metas are display guidelines (~60 / ~155 characters), not ranking rules.
