# CLAUDE.md — House of Diams US SEO Research Project

This file contains the operating rules for this project. Read it before doing any work here.

## Project

- Name: House of Diams
- Website: https://www.houseofdiams.com/
- Primary SEO market: United States
- Language: English
- Business type: Luxury diamond jewellery ecommerce

## Business context

House of Diams sells and/or promotes:
- diamond engagement rings
- wedding bands
- fine jewellery
- diamond earrings
- diamond necklaces and pendants
- diamond bracelets
- bespoke/custom jewellery
- natural diamonds
- lab-grown/CVD diamonds
- diamond education and buying information

Manufacturing/craft connection to Surat, India, but the primary SEO research market is the United States.

## Website context — important

The current website is being rebuilt.

- The current blog articles are NOT the final editorial strategy. Do not treat the existing 10 blog articles as the final 10 blog topics. Do not build future architecture around current blog titles.
- Existing blog content is an existing SEO asset that may later be retained, rewritten, merged, redirected, or retired — decided from research, not assumption.
- The same principle applies to Education: the final Education strategy is determined from SEO research, not from the current education content count.

## SEO objective

Build the complete US SEO keyword universe, then turn it into:

keyword universe → keyword metrics → search intent → SERP validation → competitor gaps → semantic clusters → page opportunities → site architecture → keyword-to-URL map → education strategy → future blog strategy → internal linking strategy → content briefs

- Do NOT begin by deciding article topics.
- Do NOT begin by creating pages for every keyword.
- The goal is not maximum URL count — it is maximum useful search coverage with clean architecture and minimal keyword cannibalization.

## SEO principles

1. Search intent is more important than keyword wording.
2. Similar keywords should normally target the same page when SERP intent is the same.
3. Do not create a URL simply because a keyword has search volume.
4. Do not create thin collection/category pages.
5. Do not create indexable parameter/filter pages unless independent search demand and SERP evidence justify them.
6. Do not create multiple pages for synonymous keywords when Google is serving the same intent.
7. Commercial, transactional, informational, comparison, and navigational intent must be distinguished.
8. Search volume alone must never determine priority.
9. Business relevance must be considered.
10. SERP evidence must be considered before creating a new page.
11. Preserve strong existing indexed URLs whenever practical.
12. Do not recommend URL changes without migration reasoning.
13. Do not invent DataForSEO metrics.
14. Distinguish paid competition from organic keyword difficulty.
15. Do not treat DataForSEO keyword difficulty as a guaranteed ranking probability.
16. Avoid fake precision and arbitrary SEO scores.
17. A lower-volume keyword can be more valuable than a high-volume keyword if it has much stronger commercial relevance.
18. The architecture must support both users and search engines.
19. Avoid page explosion.
20. Do not write final content during keyword research.

## DataForSEO rules

Use the DataForSEO MCP for keyword research.

Before every major paid stage:
1. Identify the exact DataForSEO endpoint.
2. Explain why that endpoint is appropriate.
3. Determine number of requests/tasks.
4. Estimate maximum API cost.
5. Run only after the estimate is understood (get user confirmation for non-trivial spend).
6. After execution, record actual API cost from the API response whenever available.
7. Save raw API output locally.
8. Create a cleaned/processed dataset.
9. Never dump thousands of rows into the chat.
10. Reuse previously collected datasets rather than rerunning calls.

- Use the cheapest suitable endpoint.
- Do not use Google Ads keyword APIs as a substitute for organic SEO research when DataForSEO Labs can provide the required organic metrics.
- Do not use Clickstream data unless specifically justified because it increases cost.

## Market settings

- Location: United States
- Language: English
- Do not hard-code a location code from memory — use the DataForSEO locations/languages capability to verify the exact US and English identifiers before the first paid keyword call.

## File naming (sequential workflow)

01_site_inventory.csv
02_hod_ranked_keywords.csv
03_hod_domain_keyword_universe.csv
04_hod_seed_list.csv
05_hod_keyword_expansion.csv
06_hod_master_keywords.csv
07_hod_keyword_metrics.csv
08_hod_serp_analysis.csv
09_hod_competitor_gap.csv
10_hod_keyword_clusters.csv
11_hod_information_architecture.md
12_hod_keyword_url_map.csv
13_hod_existing_content_decisions.csv
14_hod_future_blog_strategy.csv
15_hod_education_strategy.csv
16_hod_internal_linking.csv

## Cost tracking

Maintain `cost-log.csv` with columns: date, stage, endpoint, market, number_of_requests, estimated_cost_usd, actual_cost_usd, result_count, notes.

Maintain `progress.md`. For each completed stage record: completed, output files, API endpoints used, actual cost, next stage.

## Security

Never place DataForSEO credentials inside CLAUDE.md, CSV files, markdown reports, source code, or git commits. Credentials remain in Claude Desktop MCP configuration only.

## Website safety

This is a research project only. Do NOT edit the live website, edit the website repository, deploy code, change URLs, modify the CMS, modify metadata, modify robots.txt, modify sitemap.xml, or modify redirects. Research first.

## Final quality standard

The finished project should allow us to answer the 20 questions listed in README.md (site coverage, demand, intent, clustering, page-type decisions, existing-content decisions, architecture, and future blog/education strategy).

## Blog production (permanent context)

Research Stages 1–19 are done, and this project is now the source of truth for HOD content. When asked to write, optimize or publish a blog, follow `reference/BLOG_PUBLISHING_CONTEXT.md` in full. Apply `reference/SEO_PLAYBOOK.md` as a strategic reference; don't copy it.

Rules that can't be broken:
- Publishing dates and topics come from `FINAL-BLOG-CALENDAR/BLOG_CALENDAR_FINAL.csv`. Don't create another calendar, move a date, or swap a topic unless the user explicitly asks.
- Don't create new strategy, keyword research or calendars unless asked. Reuse existing research before any paid DataForSEO call.
- Keyword/URL ownership and content boundaries are fixed. If a new opportunity conflicts with them, STOP and flag it. Never change ownership silently.
- Never invent HOD facts. Rows marked `BUSINESS_FACT_REQUIRED` stay unfilled until HOD confirms the fact. Bespoke timeline: typically 2–3 weeks to make plus about 6–9 days delivery (about 3–4 weeks in total). It depends on the stone and is never a guarantee.
- Playbook tactics (URL refreshing, exact-match domains, clicks/PageRank claims, parasite SEO) are off by default. Use one only when the user explicitly asks.
- Do not automatically apply byte-level/2 MB HTML optimization tactics unless relevant to the task. The Googlebot approximately 2 MB fetch limit is documented by Google; the optimization tactic should be applied selectively.
- Use the `superseo:*` skills where they apply. If they conflict with HOD architecture or with the user, HOD architecture and the user win.
- "Publish" means a QA'd, publish-ready draft for human review. The Website safety rule above still applies: don't touch the CMS or live site unless the user explicitly says to.

File map for writing a calendar item:
- Brief and boundaries: `content-strategy/19_content_briefs.csv`, `19_brief_registry.csv`, `19_content_boundaries.csv`, `19_business_fact_requirements.csv`
- Internal links: `content-strategy/19_internal_link_requirements.csv`, `architecture/16_page_link_requirements.csv`, `16_anchor_strategy.csv`, `16_linking_rules.md`
- Ownership: `architecture/15_keyword_url_map.csv`, `15_target_page_registry.csv`, `15_cannibalization_check.csv`
- Existing content: `content-strategy/10_existing_content_inventory.csv`, `13_existing_content_decisions.csv`
- Questions, semantics and SERP: `content-strategy/17_question_map.csv`, `18_question_coverage.csv`, `18_entity_coverage.csv`, `serp/analysis/`, `content-strategy/blog-calendar/final-consolidation/call2_serp_analysis.csv`
