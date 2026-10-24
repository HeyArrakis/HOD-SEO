# 08 — On-Page Implementation Priorities

Generated 2026-10-10. Derived from `01-ON-PAGE-SEO-MASTER.csv` after the Step 2A resolutions. **Planning only — nothing has been implemented.** Class **A** = prepare/write now · **B** = apply after AWS · **C** = verify after cut-over.

**Counts:** CRITICAL 5 · HIGH 42 · MEDIUM 70 · LOW 30 (total 147). **Ready for implementation after AWS: 73 · blocked by a specific external input: 15.**

**Rubric:** CRITICAL = index-integrity, trust-fact or ranking-equity risk, or a MUST_PUBLISH page due within ~2 weeks; HIGH = live pages with clear problems or high-value pages with a ready specification; MEDIUM = worthwhile optimization without integrity risk; LOW = polish, low-demand, conditional. Volume alone never set priority; effort and AWS dependency were weighed.

## 1. Top 10 on-page priorities

1. **Fix the trust-critical copy** — delete the /shipping placeholder, publish returns terms, correct /bespoke ('4–6 weeks' → typically 2–3 weeks + ~6–9 days, generally ~3–4 weeks from design approval to delivery) and remove unverified badges. *Bespoke/badge/placeholder fixes are ready (B); policy text needs F-A1/F-A2.*
2. **Hand the redirect and index-control spec to developers** — 9 by-desgin 301s (the side-stone keyword-owner URL is a 404), canonical for the duplicate group page, noindex + sitemap/nav exclusion for 18 empty/test pages (`10` §5).
3. **Write the new Education pages in calendar order** — owners and primaries are ratified; EDU-LG-00 is due 2026-10-21 (CRITICAL); then ring size chart (165,000), diamond shapes/cut (60,500), clarity chart (33,100).
4. **Apply commercial metadata, H1s and unique intros** for 9 hubs, 23 live subcategories and /bespoke with the assigned keywords (final; Class B).
5. **Refresh the ranking-equity articles in place** after the GSC baseline — CVD vs HPHT (19 keywords), lab-grown vs natural, how-to-choose, 14K vs 18K; rewrite metas first.
6. **Fix the 19 REQUIRED internal links missing from live pages** and ship the Step 2A additions (Education index listings, wedding-band pair).
7. **PDP templates + the 8 flagged PDPs** — unique titles/metas, schema name/sku/breadcrumb alignment, neutral policy links instead of unverified claims.
8. **Schema and entity clean-up** — retire boilerplate FAQPage (35 pages), BreadcrumbList + Organization byline on articles, one Organization @id.
9. **Send the HOD questionnaire and the engineering intake** (`11`, `12`) and the GSC request (`13`) — they unlock the remaining 15 blocked rows.
10. **Unblock publishing** — 9 packaged posts are ready for human review (BC-001 is held until HOD confirms 'insured shipping', F-A1); 6 dated 2026-10-04…09 have passed; confirm the migration-safe window (E-01).

## 2. Work packages

| WP | Scope | State | Needs | Class B | Class C |
|---|---|---|---|---|---|
| WP-1 | Trust-critical copy (/shipping, /returns, /bespoke, /about, /contact, homepage badges, PDP blocks) | Placeholder removal, bespoke fix, badge removal = READY; policy/entity text = HOD INPUT REQUIRED | F-A1, F-A2, F-B1, F-C1, F-C2, F-D1 | Apply copy (E-02) | Re-read pages; schema valid |
| WP-2 | Redirect & index control (9 redirects, group canonical, 18 empty/test pages, /contact) | READY FOR IMPLEMENTATION POST-AWS | — | Implement (E-03…E-05) | Status codes, canonicals, sitemap membership |
| WP-3 | Education: 21 new pages + 10 refreshes | PRE-AWS PREPARATION (write) / READY (refresh) / GSC BASELINE REQUIRED (4 equity URLs) | G-01, G-02 for equity URLs | Publish in the migration-safe window | URL live, schema, links, CWV |
| WP-4 | Commercial metadata, H1s, intros (assigned keywords) | READY FOR IMPLEMENTATION POST-AWS | — | Apply metadata/intros/nav clean-up | Rendered titles/metas/H1s |
| WP-5 | Internal links (19 missing REQUIRED + launch links + Step 2A additions) | READY FOR IMPLEMENTATION POST-AWS | — | Edit templates/pages | Crawl REQUIRED rows |
| WP-6 | Schema & entity (Organization @id, article BreadcrumbList/byline, FAQPage retirement, Product fixes) | READY FOR IMPLEMENTATION POST-AWS | F-C1/F-C2 for sameAs/founder fields | Template/schema changes (E-07…E-10) | Rich Results Test, Schema.org validator |
| WP-7 | PDP templates + flagged PDPs | READY FOR IMPLEMENTATION POST-AWS; oval PDP = GSC BASELINE REQUIRED | F-A/F-B upgrades; G-01 for oval | Apply in product data/templates | Re-crawl 184 PDPs |
| WP-8 | Blog pipeline (10 packaged + 22 drafts; 2 drafts held for HOD facts; BC-001 publication held) | READY (9 packaged) / HOD INPUT REQUIRED (BC-001 publication; BC-005, BC-015 writing) / PRE-AWS PREPARATION (drafts) | F-A1 (BC-001), F-E6 | Publish in the window | URL, canonical, schema, links |

## 3. CRITICAL (5)

| Row | Page | Action | Status | AWS | Remaining dependencies |
|---|---|---|---|---|---|
| COM-BESPOKE | Bespoke / custom jewelry | OPTIMIZE | READY FOR IMPLEMENTATION POST-AWS | B | HOD: F-D1, F-B1 (enhance process copy; removal of unverified claims d… |
| SUP-POLICIES-SHIP | Shipping policy | OPTIMIZE | HOD INPUT REQUIRED | B | HOD: F-A1 \| ENG: E-01, E-02 |
| /hiphop/test-subcat | TEST SUBCATEGORY (artifact) | REMOVE | READY FOR IMPLEMENTATION POST-AWS | B | ENG: E-01, E-05, E-13 |
| LEG-ER-SIDESTONE | Legacy URL: /engagement-rings/by-desgin/side-ston… | REDIRECT | READY FOR IMPLEMENTATION POST-AWS | B | ENG: E-01, E-03, E-04 \| GSC: G-03 (confirm indexed state; non-blockin… |
| EDU-LG-00 | Lab-grown diamonds explained (Lab-Grown Education… | WRITE | PRE-AWS PREPARATION | A | ENG: E-01, E-02, E-07 |

## 4. HIGH (42)

| Row | Page | Action | Status | AWS | Remaining dependencies |
|---|---|---|---|---|---|
| NAV-HOME | Homepage | OPTIMIZE | READY FOR IMPLEMENTATION POST-AWS | B | HOD: F-A1, F-A3, F-B1, F-C1 (optional enhancements — page ships witho… |
| COM-COLLECTION | Collection (empty filtered view) | NOINDEX + EXCLUDE | READY FOR IMPLEMENTATION POST-AWS | B | ENG: E-01, E-05 |
| BRAND-ABOUT | About | OPTIMIZE | HOD INPUT REQUIRED | B | HOD: F-C1 \| ENG: E-01, E-02 |
| SUP-POLICIES-RET | Returns & exchanges policy | OPTIMIZE | HOD INPUT REQUIRED | B | HOD: F-A2, F-C2 \| ENG: E-01, E-02, E-08 |
| EDU-ROOT | Education index | OPTIMIZE | READY FOR IMPLEMENTATION POST-AWS | B | ENG: E-01, E-02 |
| COM-ER | Engagement rings (category hub) | OPTIMIZE | READY FOR IMPLEMENTATION POST-AWS | B | HOD: F-E1 (activates origin-qualified secondary heads) \| ENG: E-01, E… |
| COM-FJ-EARRINGS | Earrings (category) | OPTIMIZE | READY FOR IMPLEMENTATION POST-AWS | B | ENG: E-01, E-02, E-08, E-13 |
| COM-FJ-NECKLACES | Necklaces & pendants (category) | OPTIMIZE | READY FOR IMPLEMENTATION POST-AWS | B | ENG: E-01, E-02, E-08, E-13 |
| COM-ER-STYLES-GROUP | Engagement rings — 'By Design' grouping page | CANONICAL + EXCLUDE | READY FOR IMPLEMENTATION POST-AWS | B | ENG: E-01, E-05, E-13 \| GSC: G-03 (non-blocking) |
| /engagement-rings/by-design/side-stone-rings | Side-Stone Engagement Rings | OPTIMIZE | READY FOR IMPLEMENTATION POST-AWS | B | ENG: E-01, E-02, E-08 \| GSC: G-02 (non-blocking) |
| /engagement-rings/round-rings | Round Engagement Rings (shape landing) | NOINDEX + EXCLUDE | READY FOR IMPLEMENTATION POST-AWS | B | ENG: E-01, E-05, E-13 |
| /fine-jewellery/earrings/stud-earrings | Diamond Stud Earrings | OPTIMIZE | READY FOR IMPLEMENTATION POST-AWS | B | ENG: E-01, E-02, E-08 |
| /fine-jewellery/bracelet/tennis | Tennis Bracelets | OPTIMIZE | READY FOR IMPLEMENTATION POST-AWS | B | ENG: E-01, E-02, E-08 |
| COM-PDP | Product page template (184 PDPs) | OPTIMIZE (template) | READY FOR IMPLEMENTATION POST-AWS | B | HOD: F-A1, F-A2, F-A3, F-B1, F-E4 (upgrade PDP claims once confirmed)… |
| EDU-LG-03 | CVD vs HPHT lab-grown diamonds (ranking-equity ar… | REFRESH IN PLACE | GSC BASELINE REQUIRED | B | ENG: E-01, E-02, E-07 \| GSC: G-01, G-02 (blocking before title/H1/bod… |
| EDU-LG-02 | Lab-grown vs natural diamonds (ranking-equity art… | REFRESH IN PLACE | GSC BASELINE REQUIRED | B | HOD: F-E2 (keeps natural-diamond framing neutral) \| ENG: E-01, E-02, … |
| EDU-LG-01 | Are lab-grown diamonds real? | REFRESH IN PLACE | READY FOR IMPLEMENTATION POST-AWS | B | ENG: E-01, E-02, E-07 |
| EDU-4C-00 | The 4Cs of diamonds (4Cs pillar) | REFRESH IN PLACE | READY FOR IMPLEMENTATION POST-AWS | B | ENG: E-01, E-02, E-07 |
| EDU-SHP-00 | Diamond shapes (shapes pillar) | REFRESH IN PLACE | READY FOR IMPLEMENTATION POST-AWS | B | ENG: E-01, E-02, E-07 |
| EDU-RJG-02 | Ring size guide (tool-capable) | REFRESH IN PLACE | READY FOR IMPLEMENTATION POST-AWS | B | ENG: E-01, E-02, E-07 |
| EDU-CERT-00 | Diamond certification explained (retarget) | RETARGET + REFRESH | READY FOR IMPLEMENTATION POST-AWS | B | HOD: F-B1 (HOD-specific statements only) \| ENG: E-01, E-02, E-07 |
| EDU-LG-09 | Detecting lab-grown diamonds (testers & identific… | WRITE | PRE-AWS PREPARATION | A | ENG: E-01, E-02, E-07 |
| EDU-4C-01 | Diamond clarity guide | WRITE | PRE-AWS PREPARATION | A | ENG: E-01, E-02, E-07 |
| EDU-4C-03 | VVS, IF & flawless clarity diamonds | WRITE | PRE-AWS PREPARATION | A | ENG: E-01, E-02, E-07 |
| EDU-4C-05 | Diamond color guide (D to Z) | WRITE | PRE-AWS PREPARATION | A | ENG: E-01, E-02, E-07 |
| EDU-4C-06 | Diamond cut guide (cut grade, facets, light perfo… | WRITE | PRE-AWS PREPARATION | A | ENG: E-01, E-02, E-07 |
| EDU-RJG-NL | Necklace length chart (planned Education practica… | WRITE | PRE-AWS PREPARATION | A | ENG: E-01, E-02, E-07 |
| COM-LG-HUB | Commercial Lab-Grown Diamonds hub (not built) | DO NOT BUILD (reversible) | CONDITIONAL — PRODUCT/OFFER CONFIRMATION | A | HOD: F-E1, F-E2 \| ENG: E-01 |
| BC-001 | How long does a custom engagement ring take? The … | HOLD PUBLICATION (pending F-A1) | HOD INPUT REQUIRED | B | HOD: F-A1 (BLOCKS PUBLICATION: 'insured shipping' wording in the appr… |
| BC-004 | Holiday jewelry gift guide: diamond gifts by budg… | PUBLISH (packaged) | READY FOR IMPLEMENTATION POST-AWS | B | ENG: E-01, E-02, E-07 |
| BC-035 | 10 year anniversary gift ideas: tin, aluminum and… | PUBLISH (packaged) | READY FOR IMPLEMENTATION POST-AWS | B | ENG: E-01, E-02, E-07 |
| BC-018 | Anniversary gifts by year: the traditional and mo… | PUBLISH (packaged) | READY FOR IMPLEMENTATION POST-AWS | B | ENG: E-01, E-02, E-07 |
| BC-036 | What finger does a wedding ring go on? (And which… | PUBLISH (packaged) | READY FOR IMPLEMENTATION POST-AWS | B | ENG: E-01, E-02, E-07 |
| BC-006 | Necklace layering: how to layer necklaces by leng… | PUBLISH (packaged) | READY FOR IMPLEMENTATION POST-AWS | B | ENG: E-01, E-02, E-07 |
| BC-003 | Push presents: what they are, when to give one, a… | PUBLISH (packaged) | READY FOR IMPLEMENTATION POST-AWS | B | ENG: E-01, E-02, E-07 |
| BC-011 | What is a promise ring? Meaning, who gives one, a… | WRITE | PRE-AWS PREPARATION | A | ENG: E-01, E-02, E-07 |
| BC-037 | Engagement ring vs wedding ring: what is the diff… | WRITE | PRE-AWS PREPARATION | A | ENG: E-01, E-02, E-07 |
| BC-014 | Proposal ideas: how to plan a proposal she will r… | WRITE | PRE-AWS PREPARATION | A | ENG: E-01, E-02, E-07 |
| BC-024 | How much should an engagement ring cost? Average … | WRITE | PRE-AWS PREPARATION | A | ENG: E-01, E-02, E-07 |
| BC-039 | What finger does a promise ring go on? Placement,… | WRITE | PRE-AWS PREPARATION | A | ENG: E-01, E-02, E-07 |
| BC-038 | Ring finger meaning: what a ring on each finger s… | WRITE | PRE-AWS PREPARATION | A | ENG: E-01, E-02, E-07 |
| BLOG-WR-TYPES | Types of wedding rings: wedding band styles expla… | WRITE | PRE-AWS PREPARATION | A | ENG: E-01, E-02, E-07 |

## 5. By AWS class

* **A — now (57 rows):** write the 21 new Education pages and 22 Blog drafts; human-review the 9 publish-ready packaged posts (BC-001 stays held for F-A1); hand over the redirect/index-control spec, link spec and schema spec; send `11`, `12`, `13`.
* **B — after AWS (85 rows):** live metadata, H1s, intros, schema/template changes, canonical/noindex/sitemap rules, redirects, pagination, image-host updates, publishing into the new CMS. *If engineering confirms the content store is editable and outside the freeze (E-01/E-02), copy-only items may go earlier — their call, not assumed.*
* **C — verify (5 rows + the C-step of every B row):** 200/301/404, self-canonicals, indexability, sitemap membership, robots/AI-bot allowances, rendered titles/metas/H1s, schema validity, internal links, PDP currency, CWV against the pre-cut-over baseline.

## 6. Date-sensitive items (final calendar)

| Date | Item | Needs |
|---|---|---|
| 2026-10-21 | EDU-LG-00 What are lab-grown diamonds? (MUST_PUBLISH, CRITICAL) | Write + review now; `/education` index must link it; publishing window (E-01) |
| 2026-10-23 | BC-024 engagement-ring cost (MUST_PUBLISH) | Draft + review; window |
| 2026-11-12 / 11-13 | EDU-RJG-02 ring size, EDU-SHP-00 shapes (MUST_PUBLISH) | Write/refresh (primaries ratified) |
| 2026-11-25 | EDU-LG-02 refresh before December (MUST_PUBLISH) | GSC baseline (G-01) |
| 2026-12-01 / 12-08 | BC-031 trends, BC-034 Valentine's (MUST_PUBLISH) | Drafts |
| Passed, not live | BC-001, 004, 035, 018, 036, 006 (2026-10-04…09) | E-01 — is publishing paused for AWS? |
