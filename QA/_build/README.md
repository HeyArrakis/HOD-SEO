# QA/_build — how the master map was produced

Supporting material for `QA/01…06`. Nothing here touches the website or the research files.

- `evidence/` — raw observations from the **read-only** live crawl on 2026-10-09: `crawl/crawl.json` (270 URLs: status, title, meta, H1, canonical, robots, JSON-LD types, internal links, image-alt counts), `sitemap_live.xml`, `robots_txt_2026-10-09.txt`, `llms_txt_2026-10-09.txt`, `articles/articles.json` (visible text/headings of the 11 existing articles for the entity/question heuristics), `kwlookup.json` (volumes/KD merged from datasets already in the project — no new API call), `rows.json` (generated map rows).
- `scripts/` — `crawl.py` (GET-only crawler; run from `evidence/` with `urls.txt`; uses `curl`), `mm_build.py` (builds rows from research + crawl), `mm_docs2.py` / `mm_docs3.py` / `mm_docs4.py` (write documents 02+03, 04, 05; each also rewrites the two CSVs), `mm_qc.py` (20 automated checks).
- Re-run (from `scripts/`, plain `python3`, not `-I`): `python3 mm_build.py && python3 mm_docs2.py && python3 mm_docs3.py && python3 mm_docs4.py && python3 mm_qc.py`.
- Research inputs are read from `Keywords/content SEO/` (path in `lib_research.py`). Re-running overwrites `QA/01…06`.
- Heuristic text matching (entity/question presence in article bodies) is labelled "heuristic" wherever it appears in the outputs.
