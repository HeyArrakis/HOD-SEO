# _build — generator for the Step 2 package (2026-10-09; Step 2A/2B 2026-10-10; correction pass 2026-10-10)

`s2_write.py` builds every file in the parent folder from (a) the Step 1 outputs in `../../QA/` and the frozen source files in `../../Keywords/content SEO/` (read-only) and (b) the hand-authored specifications in `s2_core.py` (core pages, hubs, categories, PDP, legacy URLs), `s2_subs.py` (subcategories), `s2_edu.py` (Education), `s2_blog.py` (Blog). `s2_docs_a/b/c.py` render the Markdown documents. `pkg_meta.json` holds the approved title/H1/meta values read from `blogs/bc-*/seo-metadata.md` (read-only copy; BC-001 untouched).

* **Do not rerun `s2_write.py` unless asked** — it overwrites the package files.
* `qc_step2.py` is read-only and re-checks the written files (65 checks, incl. the close-out checks (BC-001 publication hold, status totals = 147, calendar single-cell diff vs git HEAD, `.env`/blogs untouched) and the correction-pass checks: misspellings, stale notes, bangles contradiction, timeline/shipping consistency, README counts).
* No network calls, no DataForSEO, no writes outside this package.
* **Spelling normalizer (`s2_build.us`, `us_doc`):** longest forms first; verb stems need an inflection suffix; URL/slug-like tokens are skipped; wrap quoted current-site/historical text in U+27E6 … U+27E7 to keep it verbatim (the markers are stripped on output). Do not reorder `_UK_STEMS` so that `jeweller` precedes `jewellery` (that produced the misspelling fixed on 2026-10-10).
