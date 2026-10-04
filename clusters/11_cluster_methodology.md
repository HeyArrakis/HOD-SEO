# Stage 11 — Clustering Methodology

Documents the method used (Part 1). The signal order, evidence labels and SERP-similarity thresholds were fixed before the full run. The rule set itself was corrected during quality control, and each correction is listed in `11_cluster_summary.md` §11 and in `decision-log.md`.

**A cluster is not a page and not a recommendation.** Stage 11 decides no URL, slug, new page, merge, deletion, redirect, canonical, architecture, priority or score.

## 1. Inputs

Local files only. No DataForSEO call, paid or free.

| Input | Use |
|---|---|
| `dataforseo/processed/07_hod_master_keyword_database.csv` | The keyword universe (1,936). Volume, CPC, competition, difficulty, Stage 7 status and provenance are copied unchanged. |
| `05_hod_keyword_classification.csv`, `06_hod_keyword_expansion.csv` | Stage 5 relevance class, area and analyst intent. Stage 6 flags and best-effort area. |
| `serp/analysis/08_hod_serp_validation.csv` and `serp/raw/08_stage8_by_id/*.json` | The 100 validated SERPs. The raw files are re-read for each keyword's full top-10 organic URLs. |
| `competitors/analysis/09_*` | Competitor presence per validated keyword. |
| `content-strategy/10_*` | Existing-content links (topic string-match, Stage 3 rankings, documented page-pair overlaps). |
| `site/01_site_inventory.md`, `progress.md`, `decision-log.md`, `CLAUDE.md` | Context and rules. |

## 2. Signal priority

Signals are used in this order, so wording never overrides stronger evidence:

1. **Search intent.** Stage 8 validated SERP intent first. Then an explicit text cue such as a question form, comparison words or purchase words. Then Stage 5 explicit analyst intent. DataForSEO's label is last and flagged, because Stage 8 found it disagrees with the SERP for 62% of validated keywords.
2. **SERP similarity.** Where two keywords were validated, the number of shared top-10 organic URLs (query strings and trailing slashes removed).
3. **Semantic and topical relationship.**
4. **Searcher need or question.** What the person is trying to find out or do.
5. **Business area.** From the 16 controlled areas plus `UNCLASSIFIED_OR_UNKNOWN`. It is assigned per cluster from its subject and is never forced.
6. **Query wording.** Least weight.

Shared words never create a cluster on their own. "What are lab-grown diamonds", "are lab-grown diamonds real", "how are lab-grown diamonds made" and "lab-grown vs natural" are four clusters because the need differs.

## 3. SERP similarity rules

Only the 100 Stage 8 keywords have direct SERP evidence. Nothing is inferred for the rest.

- **3 or more shared top-10 URLs** between two validated keywords: Google is treated as serving the same intent. They belong in the same cluster unless their validated intents conflict.
- **0 to 2 shared URLs** between validated keywords that would otherwise cluster: the cluster is split or the doubt is recorded. Examples: moissanite vs diamond vs moissanite vs lab-grown share 0; general lab-grown certification vs GIA-vs-IGI share 0.
- **5 or more shared URLs** between validated keywords in different clusters is treated as a fragmentation error and fixed. The QC check found and corrected one case (two "CVD vs lab grown" queries).
- A keyword's own SERP overrides its wording. Example: "diamond stone" is dual-meaning (an NBA player, sharpening stones, GIA), so it is held for review.

Evidence labels:

| Label | Meaning |
|---|---|
| HIGH | Direct SERP evidence. The keyword shares 3 or more URLs with a validated peer in its cluster, or its own validated SERP intent and page type fit the cluster. |
| MEDIUM | Strong semantic and intent rule match with no SERP evidence, or a validated keyword whose SERP intent is unclear. |
| LOW | Topic or lexical rule only, or a Stage 7 AMBIGUOUS keyword. |

Cluster evidence is HIGH only when the cluster has 2 or more validated members and at least one validated pair shares 3 or more URLs. It is MEDIUM with at least one validated member or mostly MEDIUM keyword evidence, and LOW otherwise.

## 4. Building clusters

1. **Dispositions first.**
   - Stage 7 NOISE stays NOISE. Stage 7 COMPETITOR_BRAND stays COMPETITOR_BRAND.
   - Stage 7 INCLUDE or AMBIGUOUS keywords that are clearly third-party brand queries or off-topic (cannabis, gaming, industrial abrasives, local businesses, unrelated products) are overridden to COMPETITOR_BRAND or NOISE and labelled.
   - Company-style names whose brand identity is not verified are held in `UNCLUSTERED_REVIEW`.
2. **Ordered rules.** Each cluster has explicit patterns. They are tested in priority order and the first match wins. The rules are in `clusters/scripts/rules.py`, and the first-match pattern is recorded per keyword in `clustering_reason`.
3. **AMBIGUOUS keywords** are clustered only when the cluster rule is topic-strong or the keyword was Stage 8 validated. Otherwise they stay in `UNCLUSTERED_REVIEW`. Any clustered AMBIGUOUS keyword is SECONDARY, and its evidence is LOW unless it was validated.
4. **Assignment type.**
   - PRIMARY_CLUSTER: a specific rule matched, the intent fits, and the keyword is not AMBIGUOUS.
   - SECONDARY_CLUSTER: a topic-only rule matched, the verified intent falls outside the cluster's intents, or the keyword is AMBIGUOUS.
   - Other clusters whose rules also fired are listed in `other_matching_cluster_ids`.
5. **Naming.** Cluster names describe the searcher's subject or need. They contain no URL, slug or page recommendation.
6. **Keyword intent.** Keyword intent may differ from its cluster's intent. `intent_fit_to_cluster` records this.

## 5. Existing HOD content relationship (Part 7)

- Basis: Stage 10's per-keyword topic string-match links and Stage 3 rankings.
- A URL is linked to a cluster when it is linked to at least 2 members and at least 25% of the cluster's matched members (1 member for clusters of 3 or fewer), or when it holds a Stage 3 ranking for a member.
- Categories:
  - STRONG_EXISTING_CONTENT_SIGNAL: 2 or more Stage 3 ranking members, all on one linked URL.
  - EXISTING_CONTENT_SIGNAL: one linked URL, or several whose pairs Stage 10 documented as DISTINCT.
  - MULTIPLE_EXISTING_CONTENT_POSSIBLE_OVERLAP: 2 or more linked URLs, not all documented DISTINCT.
  - NO_EXISTING_CONTENT_EVIDENCE: no member matched, in a cluster of 3 or more.
  - INSUFFICIENT_EVIDENCE: a cluster of 2 or fewer keywords with no match, or only isolated single-keyword matches.
- None of this means keep, merge, create or retire a page.

## 6. Cluster relationships (Part 8)

- SERP-derived: two clusters with validated members are compared using all cross pairs. STRONG_OVERLAP is a mean of 4 or more shared URLs. POSSIBLE_OVERLAP is a mean of 1.5 or more, or a maximum of 3 or more.
- Semantic and curated: sibling and adjacent clusters, using RELATED_BUT_DISTINCT, DISTINCT_INTENT or POSSIBLE_OVERLAP. A SERP result replaces the curated type when both clusters have validated members.
- Shared existing content: two clusters of the same parent topic that each have 3 or more members matched to the same HOD URL.
- Confidence:
  - HIGH: 4 or more validated cross pairs.
  - MEDIUM: 2 to 3 pairs, or a clear semantic split.
  - LOW: purely semantic or shared-content-only.
- **Cannibalization is never asserted.** Stage 3 found no keyword with two HOD URLs ranking, so every row reads NOT_DEMONSTRATED.

## 7. Limits

- Only 100 of 1,936 keywords have SERP evidence.
- The engine is rule-based (Stage 5's approach). Member lists were read in full and corrected, but it is not a manual per-keyword judgment.
- Stage 8's page-type and intent heuristics, and Stage 10's coarse topic matching, are inherited unchanged.
- Business relevance is not judged. A cluster exists because the data has it.
- Volumes are never summed into a demand estimate.

## 8. Reproduce

```bash
python3 clusters/scripts/summary.py
```

This regenerates the four CSVs, the QC inspection file and `11_cluster_summary.md`. It reads local files only and makes no API call.
