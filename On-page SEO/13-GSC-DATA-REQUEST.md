# 13 — GSC Data Request

Search Console data is not available in the project (the connector requires a subscription and no export exists), so **no clicks, impressions, CTR or positions are used anywhere in the package**; DataForSEO positions quoted for equity URLs are Stage 3 estimates. Routine specification work is not held up — only the items marked *blocking* below.

| ID | Export / access | Used for | Affects |
|---|---|---|---|
| G-01 | Pages report — clicks, impressions, CTR, position; 16 months; Web; all countries and United States | Baseline for every ranking-equity edit; /by-desgin/* and /shop/marquise-floral-* legacy URLs; thin-inventory review | EDU-LG-03, EDU-LG-02, EDU-LG-10, EDU-MET-01, COM-PDP-OVAL-FLORAL, LEG-marquise-floral… |
| G-02 | Queries report and Page×Query export for the URLs in G-01 plus /blog, /education, /faq, /engagement-rings, /shop, home and the 23 live subcategories | Confirms (or overturns) the volume-only keyword assignments; informational-labeled heads (toi et moi, eternity); shape-landing opportunity | OD-01/OD-16 reviews |
| G-03 | Page indexing report (indexed vs excluded + reasons), incl. URL inspection of the 8 /by-desgin/ URLs and the 18 empty pages | Whether legacy/empty URLs are indexed | Redirect and index-control rows |
| G-04 | Sitemaps report (submitted vs indexed) | Sitemap exclusion verification baseline | Index-control rows |
| G-05 | Core Web Vitals report + PageSpeed/CrUX for 10 template URLs (home, category, subcategory, 2 PDPs, article, /bespoke, /shipping, /faq, /blog) | Pre-cut-over performance baseline | Class C verification |
| G-06 | Property settings: 'Search generative AI' option and property type (domain vs URL-prefix) | Confirms the property is not excluding AI surfaces | Measurement |

## Which decisions this can change

| Item | Blocking? | Rows |
|---|---|---|
| Title/H1/body edits on ranking-equity URLs (CVD vs HPHT, lab-grown vs natural, how-to-choose, 14K vs 18K) | **Yes** — baseline first (CLAUDE.md §8) | EDU-LG-03, EDU-LG-02, EDU-LG-10, EDU-MET-01 |
| Oval PDP title/H1/schema-name change | **Yes** | COM-PDP-OVAL-FLORAL |
| 301 for the removed marquise-floral PDP | **Yes** (only redirect if equity) | LEG-marquise-floral… |
| by-desgin → by-design redirects | No — a 1:1 redirect is the safe direction; G-03 only confirms indexed state | R-01…R-09 |
| Thin-inventory/no-keyword page reviews, informational-labeled heads, shape landings, FJ rings | No — 90-day review after cut-over | see `10` §6 |

## Export format

CSV or the GSC UI export is fine: Pages and Queries tabs, 16 months, Search type = Web; one file for United States and one for all countries; include the 'Page × Query' export for the listed URLs if possible.
