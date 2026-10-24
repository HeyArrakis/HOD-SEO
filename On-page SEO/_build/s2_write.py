# -*- coding: utf-8 -*-
"""Writes the Step 2 package into 'On-page SEO/'. Reads Step 1 + source files READ-ONLY. (Step 2A/2B version, 2026-10-10)"""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s2_build import build, COLS
from s2_links import build_links, pdp_rows, LINK_COLS
import s2_docs_a as A, s2_docs_b as B, s2_docs_d as D

OUT = "/Users/manavdesai/Desktop/HOD SEO/On-page SEO"

QC_TEXT = """Disk-based checks (`_build/qc_step2.py`) — all PASS at the time of writing:

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

**Environment note (not caused by this step):** `Keywords/content SEO/CLAUDE.md` is deleted in the working tree (pre-existing); its text was read from git `HEAD` and not restored."""


import re
from s2_build import us_doc


def usdoc(t):
    """US spelling for narrative text (conservative; quoted current-site text, URLs and research terms stay verbatim)."""
    return us_doc(t)


def w(name, text):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(usdoc(text).rstrip() + "\n")


def wcsv(name, cols, rows):
    with open(os.path.join(OUT, name), "w", encoding="utf-8-sig", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=cols, extrasaction="raise")
        wr.writeheader()
        for r in rows:
            wr.writerow(r)


def main():
    rows = build()
    L = build_links(rows)
    P = pdp_rows()
    K = D.kw_rows(rows)
    wcsv("01-ON-PAGE-SEO-MASTER.csv", COLS, rows)
    wcsv("05-INTERNAL-LINK-IMPLEMENTATION.csv", LINK_COLS, L)
    wcsv("07-PDP-PRIORITY-ACTIONS.csv", list(P[0].keys()), P)
    wcsv("10-COMMERCIAL-KEYWORD-ASSIGNMENTS.csv", D.KWCOLS, K)
    w("02-ON-PAGE-SEO-MASTER.md", D.doc02(rows))
    w("03-TITLE-META-OPTIMIZATION.md", A.doc03(rows))
    w("04-H1-CONTENT-OPTIMIZATION.md", A.doc04(rows))
    w("05-INTERNAL-LINK-IMPLEMENTATION.md", B.doc05(rows, L))
    w("06-SCHEMA-AEO-GEO-SPEC.md", B.doc06(rows))
    w("07-PDP-ON-PAGE-SEO.md", B.doc07(rows, P))
    w("08-ON-PAGE-IMPLEMENTATION-PRIORITIES.md", D.doc08(rows))
    w("09-ON-PAGE-DECISIONS-REQUIRED.md", D.doc09(rows))
    w("10-DECISIONS-RESOLUTION-LOG.md", D.doc10(rows, K))
    w("11-HOD-CLIENT-FACTS-REQUEST.md", D.doc11())
    w("12-ENGINEERING-INPUTS.md", D.doc12())
    w("13-GSC-DATA-REQUEST.md", D.doc13())
    w("README.md", D.readme(rows, QC_TEXT))
    return rows, L, P, K


if __name__ == "__main__":
    rows, L, P, K = main()
    print(len(rows), len(L), len(P), len(K))
