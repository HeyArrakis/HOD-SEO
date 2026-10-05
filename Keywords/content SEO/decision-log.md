# Decision Log

Record of key research decisions and the reasoning behind them (page-type calls, URL preservation calls, cluster boundaries, intent classifications that weren't obvious, etc.). Ordered chronologically; newest at the bottom.

## 2026-09-17 — Project setup

- Decision: Treat the existing 10 blog articles and current Education content as unresolved SEO assets, not as the starting point for future architecture. Final blog and Education strategy will be derived from keyword demand, intent, SERP evidence, and competitor gaps.
- Reasoning: The website is being rebuilt; per project scope, building around current content would bias the architecture away from actual search demand.
- Decision: US location and English language DataForSEO identifiers will be verified via the locations/languages endpoint before the first paid keyword call, rather than assumed from memory.
- Reasoning: Project rule — never hard-code a location code from memory.

## 2026-09-17 — Stage 1 site inventory

- Decision: Individually crawled all non-product page types (18 core/utility/category pages, 10 blog articles, 1 education article) but sampled only 8 of 169 product pages, rather than crawling all 169 by hand.
- Reasoning: The 8 sampled PDPs (spanning main product families, a CMS "copy" carat-variant, a paired numeric-ID variant, and the visible test product) all showed one consistent, healthy template (self-referencing canonical, populated title/H1, descriptive meta). Manually crawling all 169 wasn't a good use of effort to establish that pattern; the CSV explicitly flags the remaining PDP rows as "not individually audited" so this isn't presented as verified fact. A real crawler (e.g. Screaming Frog) should re-verify at scale before any launch decision.
- Decision: Flagged, but did not resolve, the Blog/Education certification-topic overlap (IGI blog article vs. GIA-vs-IGI education article) and the 3-way overlap among general buying-guide blog articles.
- Reasoning: Per CLAUDE.md, existing-content decisions (retain/rewrite/merge/redirect/retire) are made in stage 13 from keyword + intent + SERP evidence — not during inventory, and not from a hunch that two titles look similar.
- Decision: Did not treat `/collection` (empty), `/hiphop` (placeholder + visible test nav item), or `/shop/fine-jewellery-test-product` (test product) as anything to fix.
- Reasoning: Website-safety rule — this project is research only; no site/CMS edits regardless of how obviously a placeholder or test artifact reads.

## 2026-09-17 — Stage 4 broader keyword universe

- Decision: Before running the paid `keywords_for_site/live` call, re-verified exact per-endpoint pricing directly from the account's own price table (`GET /v3/appendix/user_data` → `price.dataforseo_labs.keywords_for_site.live`) rather than relying on the Stage 3 sibling-endpoint cost as the basis for the estimate, per explicit user request.
- Reasoning: Stage 3's estimate had been inferred by analogy from a different (though related) endpoint. The user asked for endpoint-specific verification. The account price table gave an authoritative `per_request=$0.012` / `per_result=$0.00012` rate, cross-validated against Stage 3's actual charged cost ($0.01536 = $0.012 + 28×$0.00012, an exact match) — confirming the table is accurate against real billing, not just documentation.
- Decision: Used the free `dataforseo_labs/categories` reference endpoint (confirmed $0.00 in the same price table) to resolve numeric category codes into names for the cleaned dataset and summary, without additional approval.
- Reasoning: Same class of action as Stage 2's free locations/languages lookup — $0 cost, reference-only, directly supports the "preserve categories" requirement in the Stage 4 brief, not a second paid research call.
- Decision: Reported the discovered keyword universe's significant off-topic/polysemous content (Minecraft, industrial tooling, home-security brand comparisons, etc.) explicitly and in full, rather than silently filtering it out of the cleaned CSV or summary.
- Reasoning: Stage 4 instructions explicitly prohibit manual curation, merging, or removal of returned keywords at this stage ("Do NOT manually manufacture... Do not discard..."). Noting the noise as a data-limitation fact is consistent with the project's "avoid fake precision" principle — better to flag it now than to have a later stage silently inherit contaminated data.
- Decision: Did not treat the near-total absence of engagement-ring/wedding-band/necklace/bracelet vocabulary in this pull as evidence those categories lack demand.
- Reasoning: This is one relevance-ranked 1,000-row sample of a 518,487-keyword domain-relevant pool; Stage 5 (seed-based expansion built from the actual product catalog) is the designed mechanism to test that demand directly, per the project's staged workflow — jumping to that conclusion here would violate the "SERP evidence and demand must be established before judgment" principle.

## 2026-09-17 — Stage 5 strategic keyword seed universe

- Decision: Classified all 1,000 Stage 4 keywords using a rule-based (regex/keyword-pattern) classification engine rather than manual keyword-by-keyword judgment, after first manually reading the full list of 1,000 keyword strings to design the rule set.
- Reasoning: Manual one-by-one classification of 1,000 rows across 9 required fields each is not a tractable or reliable way to produce this deliverable. A rule-based engine, built from and validated against a full manual read of the actual data (not generic assumptions), is auditable (every rule and its match is traceable) and was iteratively spot-checked against the raw keyword list — including catching and fixing a regex bug that was silently routing ambiguous plural terms ("diamonds"/"rings") into the noise bucket instead of the AMBIGUOUS bucket, and a handful of specific misclassifications (e.g. "morganite rings" → ADJACENT_RELEVANT not noise; "does halo make diamond look bigger" → Engagement Ring setting attribute not generic trivia). This is disclosed explicitly in the Stage 5 summary as a limitation, not presented as manually-verified fact for every row.
- Decision: Left 137 keywords (13.7%) classified as AMBIGUOUS rather than force-assigning them to DIRECT_EDUCATION, ADJACENT_RELEVANT, or NOISE.
- Reasoning: Per the project's "avoid fake precision" principle and the stage's own AMBIGUOUS category definition, terms whose actual search meaning could not be confidently determined from the keyword text alone (e.g. short "[word] diamonds" tail terms that could be dealer/wholesaler brand names, or terms with a genuine dual meaning such as "is platinum better than diamonds") were left unresolved for later review rather than guessed.
- Decision: Selected strategic seeds (55 of 1,000) by grouping keywords into fine-grained sub-topic clusters within each business area (e.g. splitting "Diamond Quality/4Cs" into color-grade, clarity-grade, cut-quality, and carat-sizing sub-clusters) and capping selections at 2 YES + 2 REVIEW per cluster, rather than picking top-N by volume across the whole dataset.
- Reasoning: Directly implements the "avoid seed explosion" and "search volume must never be the sole priority driver" rules — without sub-clustering, the ~100+ near-duplicate single-letter diamond grade comparisons (e.g. "d vs e diamond," "e vs f diamond," "f vs g diamond" ...) would have either produced dozens of redundant seeds or, if picked by raw volume alone, silently dropped smaller but topically distinct clusters (e.g. certification, shapes, testing/authenticity) entirely.
- Decision: Mapped `current_site_representation` from the Stage 1 site inventory's already-documented findings (e.g. "CVD vs HPHT blog article exists," "no dedicated grade-comparison content exists," "GIA-vs-IGI content is split across /blog and /education") rather than performing a fresh per-keyword crawl/match against all 1,000 rows.
- Reasoning: A full per-keyword site crawl-match was out of scope for a $0.00, no-new-data classification stage. The mapping is explicitly flagged in the summary as a best-effort, topical, non-exhaustive approximation — not a verified page audit — so later stages don't treat it as ground truth.
- Decision: Kept all 43 competitor/brand keywords out of the strategic seed pool (seed_eligibility NO, except the top 5 by volume marked REVIEW) and did not perform any competitor analysis on them.
- Reasoning: Explicit stage instruction — competitor keywords are preserved for Stage 9 (competitor gap analysis), not analyzed or acted on here.

## 2026-09-17 — Stage 6 controlled keyword expansion

- Decision: Built a second, catalog-derived seed layer (34 seeds) directly from Stage 1's site inventory — live category pages and product-slug patterns — rather than relying solely on Stage 5's 55 discovery-derived seeds, before spending anything on the paid call.
- Reasoning: Stage 4 and Stage 5 had each independently confirmed that `keywords_for_site` domain-relevance discovery does not surface HOD's core product-category vocabulary (Wedding Bands, Necklaces & Pendants, Bracelets, Fine Jewellery, Bespoke all had zero seeds). The brief required addressing this specific, already-diagnosed gap with real catalog evidence rather than inventing keywords.
- Decision: Deliberately excluded "men's wedding bands" and "wedding ring styles" from the catalog seed layer despite the brief listing them as concepts to investigate.
- Reasoning: A full slug audit of all 169 PDPs found zero men's-specific products and no literal "styles" framing anywhere in the catalog — per the rule to include only concepts genuinely supported by HOD's actual business, not to manufacture seeds to fill out a checklist.
- Decision: Verified `dataforseo_labs.keyword_ideas.live` pricing fresh from the account's own price table (`GET /v3/appendix/user_data`) rather than assuming it matched Stage 3/4's `ranked_keywords`/`keywords_for_site` rate, even though it turned out to be numerically identical ($0.012 per_request + $0.00012 per_result).
- Reasoning: Explicit CLAUDE.md rule — never assume pricing from memory or a sibling endpoint; verify per-endpoint before every major paid stage.
- Decision: Ran exactly one `keyword_ideas/live` task with all 89 seeds combined (rather than splitting into multiple smaller tasks by business area), per explicit stage instruction not to split seeds or paginate automatically.
- Reasoning: Direct instruction compliance. This is flagged as a real limitation of the resulting dataset (see below), not silently accepted as sufficient.
- Decision: Reported plainly that the commercial-category blind spot (Wedding Bands, Earrings, Necklaces & Pendants, Bracelets, Fine Jewellery, Bespoke) was only barely corrected — none of the 34 catalog seeds themselves were returned as ideas, and Fine Jewellery/Bespoke matched zero items — rather than characterizing the stage as having "fixed" the Stage 4/5 gap.
- Reasoning: The single combined 89-seed task's default relevance sort mechanically favored the larger (55-seed) lab-grown/education cluster over the smaller (34-seed) catalog-commercial cluster in the top-1000-of-139,845 result. Per CLAUDE.md's "avoid fake precision" and "SERP evidence before judgment" principles, this is disclosed as a method limitation requiring a possible targeted follow-up (a future stage's decision, not made here) rather than glossed over or reframed as success.
- Decision: Marked `source_seeds`, `seed_count`, and `expansion_source` as `NOT_AVAILABLE_FROM_API_RESPONSE` / `UNKNOWN_NOT_ESTABLISHABLE_FROM_API_RESPONSE` for all 1,000 returned rows, rather than approximating a seed relationship from category overlap or keyword text similarity.
- Reasoning: Verified directly against the raw API response schema that `keyword_ideas/live` only returns `seed_keywords` at the task level (the full submitted list), not per-item. Approximating this relationship would violate the "never invent DataForSEO metrics" / "avoid fake precision" rules — an honest "not available" is preferred over a plausible-looking guess.

## 2026-09-17 — Stage 7 master keyword database

- Decision: Built the master keyword database entirely by **reusing** each keyword's own origin-stage DataForSEO metrics (Stage 3's `ranked_keywords/live`, Stage 4's `keywords_for_site/live`, Stage 6's `keyword_ideas/live`) instead of making a new `keyword_overview/live` enrichment call, after verifying current pricing/endpoint via `docs_search` and `GET /v3/appendix/user_data`.
- Reasoning: All three prior pulls already returned `search_volume`, `cpc`, `competition`, `keyword_difficulty`, and intent fields at collection time (100%/100%/99.3% search_volume coverage respectively). Reuse achieved 99.6% overall metric coverage at $0.00, directly implementing CLAUDE.md's "reuse previously collected datasets rather than rerunning calls" rule and Stage 7 instruction 8.9 ("check whether already-available Stage 3/4/6 metrics can be reused instead of paying again").
- Decision: Did NOT execute a `keyword_overview/live` call for the 7 keywords with zero volume data from any source, despite the maximum possible cost (~$0.0132) being trivial and well under the $0.50 stage cap.
- Reasoning: CLAUDE.md is explicit — "Even if the calculated cost is below $0.50, approval is still required" before any paid call. This was surfaced to the user as a separate, explicitly cost-gated optional action rather than executed unilaterally. It is also expected to add little value: `keyword_ideas/live` already queries the same DataForSEO Keyword Database backend and returned no volume for these terms, and DataForSEO's own docs state that keywords absent from their database are simply omitted from `keyword_overview` results (and not charged), suggesting they likely have no measurable Google Ads volume rather than being a data-collection gap.
- Decision: Did not attempt to fill 1,200 rows' missing `serp_summary`, or the ~317–691 keywords' missing `cpc`/`competition`/`keyword_difficulty`, via a new paid call.
- Reasoning: These gaps stem from (a) Stage 6's already-logged decision to run with `include_serp_info=false`, a stage-level scope choice, not a Stage 7 defect, and (b) genuine absence of Google Ads bid/competition data in DataForSEO's backend for low-commercial-intent terms — the same backend a fresh call would query, so re-querying would very likely return identical nulls. Spending against this expectation would violate the "what information will this call add that we don't already have" cost-gate test in CLAUDE.md.
- Decision: Derived the master `status` field (INCLUDE/NOISE/AMBIGUOUS/COMPETITOR_BRAND) from Stage 5's `primary_relevance_class` wherever a keyword was classified there, from Stage 6's own `possible_noise_flag`/`possible_ambiguity_flag` for keywords Stage 5 never saw, and — for the small number of keywords found only in Stage 3 — from the fact that they are a real, current organic ranking keyword on HOD's own domain.
- Reasoning: Preserves prior-stage classifications verbatim per instruction ("do not overwrite Stage 5's classification with guesses"). The Stage-3-only policy call is a low-risk, evidence-backed inference (a term the domain already ranks for is on-topic almost by construction, since HOD's own content was written to target it) rather than a speculative relevance judgment — disclosed explicitly here and in the row-level `notes` field rather than silently assumed.
- Decision: Kept the consolidated `search_volume`/`cpc`/`competition`/`keyword_difficulty`/`intent` fields at Stage 3 > Stage 4 > Stage 6 priority when a keyword had metrics from more than one stage, while preserving every stage's own independent value in `stage3_*`/`stage4_*`/`stage6_*` prefixed columns.
- Reasoning: Directly implements CLAUDE.md rule 4 ("do not overwrite Stage 3 values with newer estimates unless the source relationship is explicitly preserved") while ensuring no source data was discarded — the full audit trail remains inspectable per row.

## 2026-09-17 — Stage 8 SERP validation selection and method

- Decision: Reordered the nine selection pools so the explicitly-requested Stage 6 concepts (moissanite/diamond-tester queries) and the ambiguous-keyword sample ran early, before the 100-keyword cap could be reached by lower-priority pools.
- Reasoning: An initial pool ordering (current-rankings → commercial-category → informational → ... → new-concepts last) left only 1 of 8 intended Stage 6 concept keywords addable once the cap was hit, and 0 ambiguous keywords. The brief explicitly called out these two groups as important to validate; reordering so they run right after the non-negotiable current-ranking pool (and moving Long-tail to absorb the final truncation instead) ensured full representation without changing the overall 100-keyword cap or any other selection rule.
- Decision: Used `POST /v3/serp/google/organic/task_post` (Standard, normal priority, $0.0006/task) plus free `task_get/advanced` retrieval, rather than `live/advanced` ($0.002/task).
- Reasoning: Verified via the account's own price table that `task_get` retrieval (any result type, including `advanced`) is $0.00 within 30 days of posting — so Standard+advanced-retrieval gives identical SERP-feature richness to Live at roughly one-third the cost. Matches the user's explicit "prefer Standard Normal if sufficient" instruction and CLAUDE.md's "use the cheapest suitable endpoint" rule.
- Decision: Did not fetch the 100th task (`natural diamond wholesale`) until it was confirmed ready via `tasks_ready`, rather than assuming failure or substituting another keyword after 99/100 completed within the first ~90 seconds.
- Reasoning: Standard/queued SERP tasks do not all complete on an identical timeline; one task taking longer is normal, not evidence of an API problem. Waiting and re-polling preserved the exact approved 100-keyword configuration rather than silently dropping or substituting a keyword.
- Decision: Built `dominant_serp_page_type` and `validated_intent` via a disclosed, simple rule-based URL/domain/title pattern-matcher rather than a manual page-by-page review of all 500 top-ranking URLs, and left 24% of keywords as `OTHER`/`UNCLEAR` rather than forcing a page-type or intent label onto SERPs the heuristic couldn't confidently classify.
- Reasoning: A full manual audit of 500 URLs was out of scope for this stage's cost/time budget; the heuristic is disclosed explicitly as an approximation (not manually verified fact) in the summary, and every row's raw top-5 domains/URLs are preserved unedited regardless of whether the automated label was confident — so no evidence is lost, only the derived label is honestly marked uncertain where it is. This follows the same "avoid fake precision" principle already applied in Stage 5's classification engine.
- Decision: Reported the 62% DataForSEO-intent-vs-validated-SERP-intent mismatch rate plainly as a data-quality finding about DataForSEO's `main_intent` field, without treating any individual mismatch as an "error" needing correction or as grounds for reclassifying a keyword's status in the master database.
- Reasoning: Per CLAUDE.md rule 1 ("search intent is more important than keyword wording") and rule 15/16 (don't treat difficulty/metrics as guaranteed, avoid fake precision), the finding is presented as evidence for later stages (which will make the actual intent/architecture calls) rather than acted on here.
- Decision: Did not change any keyword's `status` field in the Stage 7 master database in response to the 3 AMBIGUOUS keywords the SERP resolved decisively (`thc diamond`/`thc diamonds`/`thca diamond` confirmed off-topic; `dust diamonds` confirmed off-topic; `raw diamond` confirmed on-topic).
- Reasoning: Stage 8's brief is validation/evidence-gathering only ("Stage 8 is NOT about... final architecture decisions"); applying a reclassification is a downstream decision left for whoever next touches the master database with this new evidence in hand, not an automatic side-effect of running a SERP check.
- Decision: Disclosed that a subset of the 99 raw SERP files saved by an assisting subagent were saved as cleaned/condensed JSON (verbose `xpath` paths and null `cache_url` fields trimmed) rather than byte-for-byte identical to the DataForSEO API response, after verifying via structural spot-checks that all substantive content (organic results, PAA, related searches, local pack, images, video, AI Overview, knowledge graph) was preserved in every one of the 100 files.
- Reasoning: The brief asks to "save the raw response" — a condensed-but-complete file is a meaningful deviation from strictly raw output and is disclosed rather than silently presented as untouched API output, consistent with the project's transparency principle. The deviation was verified not to have caused any data loss for this stage's processing needs before proceeding.

## 2026-09-17 — Stage 9 competitor + keyword gap analysis

- Decision: Attempted Stage 9 entirely without any new DataForSEO call, by re-parsing the 100 raw Stage 8 SERP JSON files (already collected/paid for) for full top-10 organic results instead of relying on Stage 8's processed CSV, which only preserved the top 5 per keyword.
- Reasoning: CLAUDE.md's "first try to complete Stage 9 without a paid call" instruction, and the stage's own "top 10 appearance count where available" requirement. The raw JSON (depth=10) already contained this data at $0.00 additional cost; re-querying would have duplicated data already on disk. Verified the extraction reproduced Stage 8's own top-5 domain list exactly (0 mismatches across 100 keywords) before relying on it further.
- Decision: Individually classified competitor type only for the 91 domains that repeat across ≥2 of the 100 validated keywords, leaving the 205 single-appearance domains marked `UNKNOWN`/`NOT_ASSESSED` rather than classifying all 296.
- Reasoning: The stage brief defines a competitor as "primarily a domain that repeatedly appears" — the 91 repeat domains are the actual object of this analysis. Individually classifying 205 single-occurrence domains (many clearly long-tail noise, e.g. one-off Yelp/LinkedIn/Pinterest hits) would have consumed significant effort for evidence with the least analytical value, and risked lower-confidence guesses on domains with only one data point. All 205 are still preserved as raw evidence in the landscape CSV, unclassified but not discarded.
- Decision: Marked `lgdusallc.com` (9 keyword appearances) as `competitor_type=UNKNOWN` despite its frequency, rather than guessing a business type from the domain name alone.
- Reasoning: Only blog-style URLs were observed for this domain in the sample (no product/category page evidence), and the domain name alone ("LGD USA LLC") was not enough to confidently confirm a business model. Per CLAUDE.md's explicit instruction ("if classification is uncertain, mark it UNKNOWN"), this was left unresolved rather than forced into DIRECT_JEWELLERY_ECOMMERCE by pattern-matching against similar-looking domains.
- Decision: Checked HOD's actual presence in Part 2/gap analysis directly against the raw Stage 8 organic results (0 of 795 appearances), rather than reusing the Stage 3 `current_HOD_rank` field carried over in the Stage 8 CSV as the presence signal.
- Reasoning: Stage 3's ranking data is a separate, earlier DataForSEO database snapshot (`ranked_keywords/live`), not the live Stage 8 SERP check itself. Treating a historical rank as "presence" in this stage's SERP-based gap analysis would conflate two different data sources/times. Both are reported side by side, clearly labeled, so nothing is lost — but the stage's own primary evidence (the raw SERP) is what determines `HOD_present_in_this_SERP`.
- Decision: Did not extend Stage 8's top-5 page-type classifier to organic positions 6–10; those cells are marked `NOT_CLASSIFIED_BEYOND_TOP5` in the landscape/frequency tables.
- Reasoning: Stage 8 explicitly disclosed its page-type heuristic as a top-5-only, non-manual approximation. Silently applying the same unverified heuristic to 5 more positions per keyword without the same disclosure rigor risked quietly expanding an already-flagged-as-imprecise method. Leaving it honestly unavailable follows the same "avoid fake precision" principle Stage 5/8 already established, rather than inventing a new classification pass.
- Decision: Generated Gap Types D and E as business-area-level aggregate rows (one row per business area) rather than trying to force them into individual per-keyword rows.
- Reasoning: The stage brief itself frames Type D ("a particular page/topic type HOD does not visibly represent") and Type E ("business areas with weak/absent representation") as area-level patterns, not single-keyword facts. Aggregating preserves the actual observed pattern (competitor domains, page types, example keywords) traceably in one row per area rather than manufacturing artificial per-keyword duplication.

## 2026-09-24 — Stage 10 existing content & blog equity analysis

- Decision: Completed Stage 10 without any DataForSEO call ($0.00).
- Reasoning: Parts 1–8 are descriptive and could all be answered from the Stage 1/3/7/8/9 data. A fresh `ranked_keywords` pull or a deeper SERP check would add precision but would not change the descriptive findings. Per the stage brief, a paid call is only made when it is genuinely required.
- Decision: Made free, read-only HTTP GETs of public site pages to verify `/engagement-rings/by-desgin/side-stone-rings`. That URL holds a Stage 3 ranking but is not in the sitemap or the Stage 1 inventory. The same check recorded the 41 nav-linked subcategory URLs it exposed, as inventory rows flagged `NOT in Stage 1 inventory`.
- Reasoning: The QC rule says to "verify every URL against the existing site inventory". A ranking URL missing from the inventory could not be verified from project files alone. The live check (HTTP status, title, H1, canonical, meta robots, empty-state marker) resolves this without touching the site.
- Decision: Did **not** edit the Stage 1 files. Stage 1's statement that no category URL exists for earrings, necklaces or bracelets is corrected in Stage 10 outputs and in this log only.
- Reasoning: Keep each stage's outputs as a record of what that stage observed. `/fine-jewellery/earrings`, `/fine-jewellery/necklaces` and `/fine-jewellery/bracelet` do exist, linked from nav, not in the sitemap. Whether they should be in the sitemap, indexed or restructured is an architecture decision for a later stage.
- Decision: Classified SERP alignment from HOD's actual page type (article / PDP / category) and treated Stage 8 `OTHER`/`MIXED` or LOW-confidence dominant types as INSUFFICIENT_EVIDENCE, not as a mismatch. This differs from Stage 9's Type C rows.
- Reasoning: Stage 9's Type C evidence text described every HOD ranking page as "blog/editorial-guide format". That is wrong for `/shop/oval-floral-diamond-ring` (PDP; PRODUCT SERP) and the side-stone subcategory (category; CATEGORY SERP), so both actually align. An unclassifiable SERP is not evidence of a mismatch. The Stage 9 file was left unedited; the correction is documented in `10_content_serp_alignment.csv` (`stage9_crosscheck` column).
- Decision: Linked master keywords to existing pages with a disclosed regex topic string-match. The output is labelled `TOPIC_STRING_MATCH_ONLY (not a URL assignment)`. It is not a keyword-to-URL map.
- Reasoning: Part 6 needs "existing content with topic coverage" separated from "master keyword without existing content", and that cannot be done without some topic linkage. A transparent pattern match avoids fake precision and does not pre-empt the Stage 12 keyword→URL map. The first-pass false positives were found in QC and fixed: gemstone "lab vs natural", "diamond grading scale" counted as certification, and an over-broad "buying" rule.
- Decision: Classified the IGI blog ↔ GIA-vs-IGI education pair as CLEAR_OVERLAP at topic/intent level, while stating that harmful cannibalization is not demonstrated.
- Reasoning: Same subject, business area and informational intent, and both pages match the same 58 certification keywords. However, neither page ranks, and the two validated certification SERPs (*gia vs igi lab diamond*, *lab-grown diamond certification*) share 0 top-10 URLs. Whether "IGI certification" and "GIA vs IGI" are one SERP intent is still untested, so the overlap is confirmed but its effect is not.
- Decision: Made no retain/merge/redirect/retire, architecture, URL or new-page recommendations.
- Reasoning: The Stage 10 brief is evidence-only. Those decisions belong to later stages.

## 2026-09-24 — Stage 11 semantic keyword clustering

- Decision: Completed Stage 11 with $0 additional DataForSEO spend and proposed no paid call.
- Reasoning: All clustering questions could be answered from Stage 3-10 data. The raw Stage 8 SERP files already hold full top-10 organic URLs, so keyword-to-keyword and cluster-to-cluster SERP similarity was computed locally. No clickstream, no new SERPs. Nothing that a new call would add was needed to draw a cluster boundary, and the brief forbids spending merely to make clustering "more accurate".
- Decision: Used a rule-based engine (explicit ordered patterns, saved in `clusters/scripts/rules.py`) rather than embeddings or a generic algorithm, and read every cluster's member list in full to correct the rules.
- Reasoning: Same auditable approach as Stage 5. A word-overlap or embedding method would merge "what are", "are they real", "how are they made" and "vs natural" because they share words, which the brief forbids. The engine is disclosed as rule-based, not a manual per-keyword judgment.
- Decision: Treated 3 or more shared top-10 URLs between validated keywords as "same intent", and 0-2 as a reason to split or flag. Let SERP evidence override wording.
- Reasoning: Direct SERP overlap is the strongest evidence in the project. Applied results: CVD vs HPHT, HPHT-only and CVD-only became three clusters (tight inside, 0-4 across); moissanite vs diamond and vs lab-grown became separate (0 shared); the certification family became five clusters (general vs GIA-vs-IGI share 0); "natural diamond wholesale" was merged into the natural head-term cluster (5 shared); "cvd diamond vs lab grown" and "what is cvd diamond vs lab grown" were moved into the CVD-vs-HPHT cluster after the QC check found 4-5 shared URLs with its SERPs.
- Decision: Overrode part of Stage 7's INCLUDE/AMBIGUOUS set at Stage 11 (192 to NOISE, 66 to COMPETITOR_BRAND, 154 total kept in UNCLUSTERED_REVIEW) instead of forcing them into clusters. Left `07_hod_master_keyword_database.csv` untouched, kept `stage7_status` on every row and labelled each change in `stage11_status_override` and `clustering_reason`.
- Reasoning: Stage 7 INCLUDE contained obvious off-topic terms (THC "liquid diamonds", Minecraft "y level", local businesses such as "diamond detailing", a basketball player, industrial abrasives) that Stage 6's lightweight flags missed. Clustering them as diamond topics would corrupt the cluster map. Where Stage 8 had a SERP (thc/thca, dust diamonds, diamond construction/detailing/recycling/equipment, deshields, reed diamond) the override rests on it. Stage 7 NOISE and COMPETITOR_BRAND were preserved exactly, per the brief.
- Decision: Company-style names whose brand identity cannot be verified in project data (for example "providence diamond", "universal diamonds", "canos diamonds") went to UNCLUSTERED_REVIEW, not COMPETITOR_BRAND. Recognizable retailers/brands and "<name> lab grown diamonds" patterns already used by Stage 5 went to COMPETITOR_BRAND.
- Reasoning: Avoid asserting a brand identity the data does not show. Consistent with Stage 9's rule of marking uncertain domains UNKNOWN.
- Decision: Held "diamond stone" (18,100) and two Stage 5 strategic seeds ("asl diamond shape", "is kite a diamond shape") in UNCLUSTERED_REVIEW rather than clustering or calling them noise.
- Reasoning: The "diamond stone" SERP mixes an NBA player, sharpening stones and GIA. The two seeds appear to be sign-language/geometry questions, but Stage 5 selected them and their meaning is unverified, so they are flagged for later review, not discarded.
- Decision: Keyword intent precedence is Stage 8 validated SERP intent, then an explicit text cue, then Stage 5 explicit intent, then Stage 5 INFORMATIONAL only where DataForSEO agrees, then the DataForSEO label flagged as weak. Cluster primary intents were reset after computing member intent distributions.
- Reasoning: Stage 5 never assigned TRANSACTIONAL and defaulted bare phrases to INFORMATIONAL, and Stage 8 showed DataForSEO's label disagrees with the SERP for 62% of validated keywords. 313 clustered keywords still carry only a DataForSEO label, disclosed in the summary.
- Decision: PRIMARY_CLUSTER vs SECONDARY_CLUSTER is defined by rule specificity, intent fit and Stage 7 AMBIGUOUS status, not by importance. UNCLUSTERED_REVIEW is used for unresolved keywords instead of a forced best guess. Every keyword has exactly one row.
- Reasoning: Meets the "no duplicate keyword-cluster mappings" and "no keyword silently disappears" QC rules while keeping uncertain keywords visible.
- Decision: Business area is assigned per cluster from its subject. Areas with no cluster (Wedding Bands, Necklaces & Pendants, Bracelets, Fine Jewellery, Bespoke) stay empty. Keywords tagged with those areas by Stage 5/6 were clustered by subject or set aside, and are listed in the summary.
- Reasoning: The keyword-data gap has been flagged since Stage 4. Inventing clusters to fill the controlled list would violate the no-invented-data rules. Mixed Metal Rings sits under Materials/Metals (Stage 5 had it under Engagement Rings) because the need is metal-based.
- Decision: Existing-content relationship per cluster uses Stage 10 links with a significance rule (at least 2 members and 25% of matched members; Stage 3 rankings always count) and downgrades to EXISTING_CONTENT_SIGNAL when Stage 10 documented the linked pages as DISTINCT (parent/child category vs child, shapes article vs PDP). Isolated single-keyword matches give INSUFFICIENT_EVIDENCE.
- Reasoning: Stage 10's topic patterns are coarse; for example every certification keyword matches both certification pages by construction. Without a significance rule a single stray keyword would mark a cluster as overlapping.
- Decision: Cluster relationships use the five permitted types. SERP-derived evidence takes precedence over curated semantic labels. No STRONG_OVERLAP was found, and no row claims actual cannibalization (column reads NOT_DEMONSTRATED). Shared-existing-content pairs are included only for clusters of the same parent topic.
- Reasoning: Stage 3 found no keyword with two HOD URLs ranking; topic overlap and SERP sharing are not cannibalization.
- Decision: Kept 2 single-keyword clusters (CL-060 "diamond shape", CL-120 "side stones engagement rings") and 8 clusters of 2-3 keywords, flagged in `cluster_size_flag`.
- Reasoning: Each is a validated or ranking search need with no variants in the data. They are not proposals for pages.
- Decision: Clustered moissanite, cubic zirconia, science trivia and trade topics on the evidence without judging business relevance. Raw volumes are not summed into demand and the high-volume list is ordered by head-keyword volume for description only.
- Reasoning: Brief: do not assume moissanite becomes a HOD target; no scoring, ranking of opportunities or "best cluster".
- Decision: Saved the rule set and builder in `clusters/scripts/` (no credentials, no API code) so any cluster boundary can be traced and regenerated.
- Reasoning: Auditability, consistent with the project's traceability rules.

## 2026-09-24 — Stage 12 SEO information architecture

- Decision: Completed Stage 12 from local files only, with $0 DataForSEO spend. No paid call was proposed for this stage.
- Reasoning: The structural questions could be answered from Stages 1–11. The one gap that data could close, commercial category demand, affects which conditional pages become indexable in Stage 15, not the structure itself. It is therefore recorded as a recommendation (D-19), not run.
- Decision: The full set of 19 architecture decisions, with evidence, alternatives, rationale, confidence and deferred questions, is kept in `architecture/12_ia_decision_log.md` rather than repeated here.
- Key decisions in brief: separate commercial and informational systems; a conditional Lab-Grown commercial hub (Natural deferred); engagement-ring style as the L2 dimension (side-stone confirmed); Fine Jewellery kept as the umbrella for earrings/necklaces/bracelets (existing URLs, no evidence for flattening); a seven-condition gate for indexable facets; Education as the single evergreen home, with Blog kept for time-bound editorial content; flat one-URL-per-product PDPs.
- Decision: Made no keyword→URL assignments, redirect, canonical, sitemap, robots, deletion or merge recommendations. Existing misspelled or grouped URLs are flagged against principles only. Any change needs migration reasoning in Stage 13/15.
- Reasoning: The brief and CLAUDE.md rules 11 and 12.

## 2026-09-24 — Stage 13 future blog strategy + existing content decisions

- Decision: Completed Stage 13 from local files only, with $0 DataForSEO spend. No paid call was needed.
- Reasoning: Existing Stage 3/8/10/11 evidence was enough to classify every article. The remaining gaps (IGI-specific SERPs, engagement-ring buying-guide SERPs, GSC/backlinks) are recorded as deferred conditions, not guessed.
- Decision: Separate topic *ownership* from URL *location*. All 10 blog articles are Education-owned. The two HIGH-risk ranking articles (CVD vs HPHT, lab-vs-natural) keep their /blog URLs (UPDATE_IN_PLACE, DO_NOT_MOVE_NOW) until 9 explicit conditions are met.
- Reasoning: They hold 22 of 28 rankings, the Education destination does not exist, and Stage 8/9 show competitors rank for these exact topics on /blog paths. A path move adds redirect risk with no demonstrated ranking benefit (CLAUDE.md rules 11 and 12).
- Decision: MOVE_TO_EDUCATION for 5 articles (4 unranked, plus 14k vs 18k at positions 81–95), conditional on the destination existing and a 1:1 301.
- Reasoning: Evergreen reference topics with no or negligible positional equity and no demonstrated overlap.
- Decision: Certification overlap (OV-01) is resolved by intent differentiation, not a merge. The Education GIA-vs-IGI article keeps the comparison; the IGI blog is RETARGETED to the non-comparison certification need.
- Reasoning: "gia vs igi lab diamond" and "lab-grown diamond certification" share 0 top-10 URLs. The retarget target (CL-032 vs CL-033) is deferred for lack of IGI-query SERP evidence.
- Decision: DEFER the how-to-choose / buy-online ring guide pair. No MERGE recommended anywhere.
- Reasoning: The ring-buying intent has no keyword or SERP evidence (commercial keyword gap, D-19); merging would be a guess. If consolidation happens later, the ranking how-to-choose article is the presumed survivor.
- Decision: The Blog's future role is editorial and brand content (craft/Surat workshop, style and trends, gifts, launches, stories, dated industry notes). No publishing quota; no empty category pages; tag archives not indexable.
- Reasoning: Stage 12 D-10, the business context, and the absence of any capacity or demand data for a cadence.

## 2026-09-24 — Stage 14 Education strategy & architecture

- Decision: Completed Stage 14 from local files only, with $0 DataForSEO spend. The one paid check that would help (16 SERP tasks, max $0.0096) is documented as D14-29 and was not run.
- Reasoning: Every boundary without evidence could be given an explicit interim home and a CONDITIONAL or DEFERRED status, so the architecture does not depend on the check.
- Decision: The full set of 30 decisions is kept in `architecture/14_education_decision_log.md`. In brief:
  - 8 hubs, with pillar landing pages
  - CVD and HPHT stay subordinate to one CVD-vs-HPHT resource
  - authenticity is kept separate from lab-vs-natural
  - lab-grown quality is integrated into the general 4Cs pillar
  - the IGI blog is retargeted to general certification (CL-033)
  - one shapes pillar, with no per-shape pages
  - Gemstones & Alternatives is conditional on business decisions
  - Buying Guides and Diamond Science are not hubs
- Decision: Made no keyword→URL assignments, URLs/slugs, redirect, canonical, deletion or migration changes. All Stage 13 actions, risks and conditions are preserved.
- Reasoning: Brief; CLAUDE.md rules 11–12 and website-safety rules.

## 2026-09-24 — Stage 15 Keyword → URL mapping

- Decision: Completed Stage 15 from local files only, with $0 DataForSEO spend. Neither the D14-29 SERP batch nor the D-19 supplement was run.
- Decision: Every one of the 1,936 Stage 7 keywords has exactly one disposition. Conditional and deferred topics get no URL. Commercial SERPs never map to Education. Existing ranking URLs keep their keywords.
- Decision: The CVD-vs-HPHT and lab-vs-natural articles stay at their /blog URLs as the single owners of CL-016/017/018 and CL-011. No new CVD, HPHT or lab-vs-natural page is created.
- Decision: Proposed URL expressions follow Stage 12 D-12. They are not implemented, and the path prefix depends on the platform (D-17). Provisional topics and hubs affected by D-15 are URL_PENDING. No redirect, canonical or migration is recommended beyond the conditions Stage 13 already set.
- Reasoning: `architecture/15_keyword_mapping_decision_log.md` (D15-01 to D15-16).

## 2026-09-24 — Stage 16 Internal linking architecture

- Decision: Completed Stage 16 from local files only, with $0 spend and no API or live-site request. Stage 15 ownership and the Stage 12/14 hierarchy are treated as fixed; no URL, slug, redirect, canonical, indexability or keyword-owner change is made or recommended.
- Decision: Internal links reinforce owners only. Every anchor is checked against Stage 15: no anchor may equal a keyword owned or held by a different page, and exact-match anchors (4 in total) are limited to keywords the target already owns, one source per target.
- Decision: The six protected ranking URLs are linked at their current URLs with varied contextual anchors. The nine Education-owned /blog articles get the Education breadcrumb and hub listing now (Stage 13 transitional state), and their Blog-hub listing is kept until an Education path exists.
- Decision: The bare labels "Lab-Grown Diamonds" and "Natural Diamonds" are not used as Education anchors/breadcrumbs ("… Guide" labels instead), because Stage 15 holds those head terms for the conditional/deferred commercial hubs. Hub names are unchanged. Flagged for user sign-off.
- Decision: Links that depend on unconfirmed business facts (commercial Lab-Grown hub, grading reports per product, karat options, natural/moissanite/gemstone offering, populated subcategories, Blog craft/story posts) are CONDITIONAL. Deferred topics get no links.
- Reasoning: `architecture/16_linking_rules.md` and `architecture/16_stage_summary.md`; CLAUDE.md principles 1, 6, 11, 12 and website-safety rules.

## 2026-09-24 — Stage 17 Keyword deep dives

- Decision: Completed Stage 17 from local files only, with $0 spend. Stage 15 ownership, Stage 11 clusters, Stage 8 intent and Stage 16 relationships are treated as fixed. All 1,936 keywords are carried. Only the 659 owned keywords are deep-profiled; held, review and excluded keywords are passed through without opportunity analysis.
- Decision: Primary terms were chosen by fit (intent, page type, ownership, ranking equity), not by volume. Examples: `hpht vs cvd` over `hpht lab grown diamond` for the comparison page; `lab-grown diamond certification` (validated) over `gia lab diamonds`; co-primaries where one term cannot carry the page need.
- Decision: A DataForSEO TRANSACTIONAL label with no commercial modifier is read as UNCLEAR, and a question form conflicting with its label is flagged. No intent is ever upgraded to TRANSACTIONAL, and Stage 8 always controls.
- Decision: Existing-content coverage is judged at title/H1/topic level only. Nothing is marked FULL without a body audit, and anything unevidenced is UNKNOWN rather than THIN.
- Decision: The missing core head terms (4Cs, colour/clarity/carat/cut charts, shapes, 14k vs 18k, metals, ring size, settings) are recorded as data gaps, not content gaps. A 36-keyword keyword_overview supplement (maximum $0.01632) is proposed and NOT run.
- Reasoning: `content-strategy/17_stage_summary.md`; CLAUDE.md principles 1–2, 8, 13–16 and the cost-gate and website-safety rules.


## 2026-09-25 — Stage 18 Semantic gap analysis

- Decision: Completed Stage 18 from local files only, with $0 spend. Stage 15 ownership, Stage 16 links and Stage 17 intelligence are treated as fixed. No page, URL, cluster or keyword owner was created or changed.
- Decision: A concept enters the register only if it matches project evidence (Stage 8 AI Overview/organic text, routed PAA, related searches, owned keywords, Stage 17 concepts). Severity follows a fixed role × evidence-strength rule; there is no page score or cross-page ranking.
- Decision: Concepts owned elsewhere are capped at IMPORTANT and are treated as brief mentions plus links. Ownership is verified against Stage 15 anchor keywords and xkeys.
- Decision: Existing-content coverage is judged on title/H1 only; bodies are UNKNOWN and nothing is marked CONFIRMED_MISSING.
- Decision: A 17-task SERP batch (maximum $0.0102) is recommended for the no-SERP targets and head terms but was not run; the keyword_overview metrics call is not needed for Stage 18.
- Reasoning: `content-strategy/18_stage_summary.md`; CLAUDE.md principles 1–2, 10, 13–16, 19–20 and the cost-gate and website-safety rules.

## 2026-09-25 — Stage 18.5 Targeted SERP validation supplement

- Decision: Ran the single approved paid call: `serp/google/organic/task_post`, 17 tasks, US/en, depth 10, desktop, normal priority, no clickstream. The price was re-verified at $0.0006/task. Actual spend was $0.0102, equal to the approved maximum and confirmed by the balance difference.
- Decision: Stage 18 files were not rewritten. New SERP evidence is recorded as a change log (CONFIRMED / STRENGTHENED / WEAKENED / CHANGED / NEW_EVIDENCE / CONFLICT / UNCHANGED). Each row cites a verbatim token from the raw SERP.
- Decision: `engagement ring settings` is commercial-led (CONFLICT with Stage 18's treatment as an Education head term). Stage 15 ownership was not changed; it is flagged for a Stage 15-style review.
- Decision: Corrected the Stage 18 reported gap total from 303 to 304 (reporting error only; data unchanged).
- Reasoning: `serp/analysis/18_5_semantic_supplement.md`; CLAUDE.md cost-gate rules and principles 1, 10, 13-16.

## 2026-09-25 — Stage 19 Content briefs

- Decision: Built implementation-ready briefs for exactly the 27 Stage 15 targets (12 existing, 15 future; 0 conditional pages, 5 interim-home sections) from local Stage 10–18.5 files, $0 spend. There is no article copy, final title, meta description, new URL, keyword owner, cluster or link.
- Decision: Stage 15 (ownership), 16 (links), 14 (architecture) and 18/18.5 (semantics, SERP formats) were treated as authoritative. Conflicts were recorded, not resolved.
  - `engagement ring settings` is flagged OWNERSHIP_REVIEW_REQUIRED on EDU-RJG-01. No second owner was created.
  - 16 Stage 18 boundaries lack a Stage 16 link, so the brief says mention only (a Stage 16 review item).
  - 18.5-validated head terms that are absent from the Stage 15 map are used as SERP evidence only.
- Decision: 18.5 "Implied weight" changes were applied to gap weights inside the Stage 19 outputs only (28 gaps). All effective CRITICAL/IMPORTANT gaps sit in content sections. Existing pages keep BODY_COVERAGE=UNKNOWN ("ensure X is addressed").
- Decision: 30 HOD business facts are listed, 4 BLOCKING (side-stone assortment and options, PDP specifications, HOD sustainability-claim wording). Nothing HOD-specific is asserted.
- Reasoning: `content-strategy/19_decision_log.md` and `content-strategy/19_stage_summary.md`; CLAUDE.md principles 1–20 and the website-safety rules.
