# Stage 11 — Semantic Keyword Clustering Summary

Date: 2026-09-24. Scope: clustering only. This stage makes no URL, slug, page, merge, redirect, canonical, architecture, prioritization or scoring decision. **A cluster is not a page and not a recommendation.** It is a structured representation of related search demand and intent.

**Stage 11 completed with $0 additional DataForSEO spend.** No DataForSEO endpoint (paid or free) was called. Cumulative spend is unchanged at $0.33536.

Files: `11_cluster_registry.csv` (one row per cluster), `11_keyword_cluster_map.csv` (one row per keyword), `11_cluster_relationships.csv` (cluster pairs), `11_cluster_qc_inspection.csv` (manual-inspection groups), `11_cluster_methodology.md` (method, written before clustering), `scripts/rules.py`, `scripts/engine.py`, `scripts/build.py` and `scripts/summary.py` (the auditable rule set and builder; run `python3 clusters/scripts/summary.py` to regenerate every output).

---

## 1. What was processed

- **Total keywords processed: 1,936.** This is the full Stage 7 master database, with nothing dropped. Each keyword has exactly one row in the map.
- **Total meaningful clusters: 89.** They hold 1,024 keywords. 2 are single-keyword clusters and 8 have 2 to 3 keywords. Both are flagged in `cluster_size_flag`.
- **Unclustered / review: 154** (62 Stage 7 INCLUDE and 92 Stage 7 AMBIGUOUS).
- **Noise: 649.** Stage 7 NOISE is preserved: 457. Stage 11 added 192 more (128 INCLUDE and 64 AMBIGUOUS). See section 9.
- **Competitor / brand: 109.** Stage 7 COMPETITOR_BRAND is preserved: 43. Stage 11 added 66 more (65 INCLUDE and 1 AMBIGUOUS).

| Disposition in the map | Keywords |
|---|---|
| PRIMARY_CLUSTER | 1,000 |
| SECONDARY_CLUSTER | 24 |
| UNCLUSTERED_REVIEW | 154 |
| NOISE | 649 |
| COMPETITOR_BRAND | 109 |
| **Total** | **1,936** |

Stage 7 status against Stage 11 disposition:

| Stage 7 status | Keywords | Clustered | UNCLUSTERED_REVIEW | NOISE | COMPETITOR_BRAND |
|---|---|---|---|---|---|
| INCLUDE | 1,258 | 1003 | 62 | 128 | 65 |
| AMBIGUOUS | 178 | 21 | 92 | 64 | 1 |
| NOISE | 457 | 0 | 0 | 457 | 0 |
| COMPETITOR_BRAND | 43 | 0 | 0 | 0 | 43 |

The Stage 7 master file was **not edited**. Every map row keeps its `stage7_status`, and `stage11_status_override` marks each keyword whose Stage 11 disposition differs from it.

**Assignment types.**
- `PRIMARY_CLUSTER`: a core member. Its rule match is specific, its intent fits the cluster, and it is not a Stage 7 AMBIGUOUS keyword.
- `SECONDARY_CLUSTER`: a peripheral member. Either only a topic/lexical rule matched, or its verified intent is outside the cluster's intents, or Stage 7 marked it AMBIGUOUS and it was clustered on a topic-strong rule or Stage 8 evidence (21 AMBIGUOUS keywords).
- `other_matching_cluster_ids` lists other clusters whose rules also fired for the keyword. Use it to see where topics touch.

**Evidence labels.**
- `HIGH`: direct Stage 8 SERP evidence. Either the keyword shares 3 or more top-10 URLs with a validated peer in its cluster, or its own validated SERP intent and page type are consistent with the cluster.
- `MEDIUM`: a strong semantic and intent rule match with no direct SERP evidence, or a Stage 8 validated keyword whose SERP intent is unclear.
- `LOW`: a topic/lexical rule only, or a Stage 7 AMBIGUOUS keyword.
- Keyword-level evidence for the 1,024 clustered keywords: HIGH 70, MEDIUM 933, LOW 21. Only 100 of 1,936 keywords (5.2%) have direct SERP evidence, so most MEDIUM labels rest on semantics.
- Cluster-level evidence: HIGH 12, MEDIUM 77, LOW 0. A cluster is HIGH only when it has 2 or more validated members and at least one validated pair shares 3 or more top-10 URLs.

## 2. Clusters by business area

The area is set per cluster from its subject. It is not copied from Stage 5, and it is not forced when evidence is thin.

| Business area | Clusters | Keywords | Cluster IDs |
|---|---|---|---|
| 1. Engagement Rings | 4 | 22 | CL-120, CL-121, CL-122, CL-124 |
| 2. Wedding Bands | 0 | 0 | none |
| 3. Earrings | 1 | 6 | CL-125 |
| 4. Necklaces & Pendants | 0 | 0 | none |
| 5. Bracelets | 0 | 0 | none |
| 6. Fine Jewellery | 0 | 0 | none |
| 7. Bespoke / Custom Jewellery | 0 | 0 | none |
| 8. Lab-Grown Diamonds | 24 | 367 | CL-001, CL-002, CL-003, CL-004, CL-005, CL-006, CL-007, CL-008, CL-009, CL-010, CL-011, CL-012, CL-013, CL-014, CL-015, CL-016, CL-017, CL-018, CL-019, CL-020, CL-021, CL-022, CL-023, CL-026 |
| 9. Natural Diamonds | 6 | 58 | CL-070, CL-071, CL-073, CL-074, CL-075, CL-076 |
| 10. Diamond Shapes | 5 | 17 | CL-060, CL-061, CL-062, CL-063, CL-064 |
| 11. Diamond Cuts | 1 | 10 | CL-050 |
| 12. Diamond Quality / 4Cs | 12 | 151 | CL-040, CL-041, CL-042, CL-043, CL-044, CL-045, CL-046, CL-047, CL-048, CL-049, CL-051, CL-089 |
| 13. Diamond Certification | 5 | 72 | CL-030, CL-031, CL-032, CL-033, CL-034 |
| 14. Diamond Buying / Education | 10 | 103 | CL-024, CL-065, CL-080, CL-081, CL-082, CL-083, CL-085, CL-086, CL-087, CL-088 |
| 15. Jewellery Materials / Metals | 7 | 57 | CL-110, CL-111, CL-112, CL-113, CL-114, CL-115, CL-123 |
| 16. Gemstones | 13 | 151 | CL-090, CL-091, CL-092, CL-093, CL-094, CL-095, CL-096, CL-100, CL-101, CL-102, CL-103, CL-104, CL-105 |
| UNCLASSIFIED_OR_UNKNOWN | 1 | 10 | CL-084 |

Areas with **no cluster**: 2. Wedding Bands, 4. Necklaces & Pendants, 5. Bracelets, 6. Fine Jewellery, 7. Bespoke / Custom Jewellery. That is a keyword-data gap, not evidence of low demand. Earlier stages (4 to 10) repeatedly flagged thin or absent coverage for these areas. A few master keywords carry a Stage 5/6 area tag for them (table below), but they are questions about metals, wear and authenticity, so they were clustered by subject or set aside as brand queries, not by the tag.

Master keywords tagged (Stage 5, else Stage 6 best-effort) with an area that has no cluster, and where they went:

| Keyword | Tagged area | Stage 7 | Disposition | Cluster |
|---|---|---|---|---|
| can you wear silver bracelet with gold necklace | 4. Necklaces & Pendants | INCLUDE | CLUSTERED | CL-112 Jewellery Metals: Types, Best Metal &  |
| diesel bracelet | 5. Bracelets | INCLUDE | COMPETITOR_BRAND |  |
| how can you tell if a tiffany bracelet is real | 5. Bracelets | INCLUDE | COMPETITOR_BRAND |  |
| is titanium good for wedding bands | 2. Wedding Bands | INCLUDE | CLUSTERED | CL-113 Tungsten & Titanium Wedding Bands |
| is tungsten good for wedding bands | 2. Wedding Bands | INCLUDE | CLUSTERED | CL-113 Tungsten & Titanium Wedding Bands |
| will a gold plated necklace tarnish | 4. Necklaces & Pendants | INCLUDE | CLUSTERED | CL-115 Jewellery Tarnish, Water & Everyday We |

## 3. Clusters by primary intent

| Primary intent of the cluster | Clusters | Keywords |
|---|---|---|
| INFORMATIONAL | 51 | 602 |
| COMMERCIAL_RESEARCH | 14 | 172 |
| MIXED | 12 | 156 |
| TRANSACTIONAL | 11 | 79 |
| NAVIGATIONAL | 1 | 15 |

Each registry row also carries `secondary_intents` and an `intent_distribution` computed from its members. Intent was kept separate wherever the searcher need differs. Examples:
- What lab-grown diamonds are (CL-002).
- Lab-grown vs natural (CL-011).
- Are they real (CL-010).
- Are they worth it (CL-012).
- Head terms and shopping (CL-001).
- Wholesale (CL-007).
- Certification (CL-030 to CL-034).

Keyword-level intent precedence, recorded in `intent_source`:
1. Stage 8 validated SERP intent.
2. An explicit text cue: question form, comparison words, or purchase words.
3. Stage 5 explicit analyst intent.
4. Stage 5 INFORMATIONAL only where DataForSEO agrees.
5. The DataForSEO label alone, flagged `DATAFORSEO_LABEL_ONLY`.

Stage 5 never assigned TRANSACTIONAL and defaulted bare phrases to INFORMATIONAL. Stage 8 showed DataForSEO's label disagrees with the SERP for 62% of validated keywords. So **313 clustered keywords carry only a weak DataForSEO-label intent**, and 36 are UNCLEAR because Stage 5 and DataForSEO disagree and there is no text cue.

## 4. High-volume clusters

Ordered by the volume of the cluster's largest keyword. This is descriptive. It is not a ranking of opportunity, and per-keyword volumes are not summed into a demand figure because near-duplicate variants double-count. The registry keeps `keyword_volume_sum_raw_not_a_demand_estimate` for reference only.

| Cluster | Name | Head keyword | Volume | Keywords | Validated | Evidence |
|---|---|---|---|---|---|---|
| CL-090 | Moissanite: General & Head Terms | moissanite | 201,000 | 13 | 3 | MEDIUM |
| CL-001 | Lab-Grown Diamonds: General & Head Terms | lab grown diamonds | 135,000 | 27 | 4 | HIGH |
| CL-060 | Diamond Shapes Overview | diamond shape | 60,500 | 1 | 1 | MEDIUM |
| CL-011 | Lab-Grown vs Natural Diamonds | lab grown vs natural diamonds | 22,200 | 31 | 4 | HIGH |
| CL-043 | VVS, IF & Flawless Clarity Diamonds | v v s diamond | 18,100 | 2 | 1 | MEDIUM |
| CL-061 | Asscher Cut Diamonds | asscher cut diamond | 18,100 | 6 | 3 | HIGH |
| CL-070 | Natural Diamonds: General & Head Terms | natural diamonds | 18,100 | 9 | 3 | HIGH |
| CL-010 | Are Lab-Grown Diamonds Real? (Authenticity) | are lab grown diamonds real | 14,800 | 17 | 1 | MEDIUM |
| CL-040 | Diamond Grading Scales & 4Cs Charts (General) | diamond clarity grading scale | 12,100 | 13 | 1 | MEDIUM |
| CL-075 | How Diamonds Form (Natural Formation) | how is diamond formed | 12,100 | 14 | 0 | MEDIUM |
| CL-105 | Coloured Gemstone Rings & Jewellery (Tanzanite, Moldavite & Others) | tanzanite rings | 12,100 | 11 | 0 | MEDIUM |
| CL-071 | Rough & Raw Diamonds | raw diamond | 9,900 | 12 | 2 | HIGH |
| CL-017 | HPHT Lab-Grown Diamonds | hpht lab grown diamonds | 8,100 | 7 | 5 | HIGH |
| CL-104 | Morganite Rings & Jewellery | morganite rings | 8,100 | 4 | 1 | MEDIUM |
| CL-006 | Lab-Grown Diamonds by Carat Weight | ct diamond | 6,600 | 6 | 1 | MEDIUM |
| CL-065 | Types of Diamonds (General Overview) | types of diamonds | 6,600 | 7 | 0 | MEDIUM |
| CL-114 | Alternative Material & Novelty Rings (Cobalt, Tantalum, Uranium, Glow & Others) | hematite ring | 5,400 | 17 | 0 | MEDIUM |
| CL-063 | Marquise-Oval & Moval Diamonds (Elongated Cuts) | moval diamond | 4,400 | 3 | 1 | MEDIUM |
| CL-095 | Diamond Simulants & Alternatives | simulated diamond | 4,400 | 16 | 0 | MEDIUM |
| CL-123 | Mixed Metal Rings | mixed metal rings | 4,400 | 2 | 1 | MEDIUM |

## 5. Clusters with Stage 8 SERP evidence

40 of 89 clusters contain at least one of the 100 validated keywords. 17 contain two or more, so SERP similarity could be measured inside them. Overlap counts are shared top-10 organic URLs, computed from the raw Stage 8 SERP files.

| Cluster | Name | Validated | Mean shared URLs | Min | Max | Cluster evidence | Dominant SERP page types |
|---|---|---|---|---|---|---|---|
| CL-001 | Lab-Grown Diamonds: General & Head Terms | 4 | 3.3 | 1 | 7 | HIGH | BRAND:3; CATEGORY:1 |
| CL-011 | Lab-Grown vs Natural Diamonds | 4 | 5.2 | 3 | 7 | HIGH | COMPARISON:3; OTHER:1 |
| CL-016 | CVD vs HPHT Lab-Grown Diamonds | 11 | 5.1 | 1 | 7 | HIGH | EDITORIAL_GUIDE:11 |
| CL-017 | HPHT Lab-Grown Diamonds | 5 | 6.9 | 6 | 8 | HIGH | EDITORIAL_GUIDE:4; COMPARISON:1 |
| CL-018 | CVD Lab-Grown Diamonds | 2 | 4.0 | 4 | 4 | HIGH | OTHER:1; MIXED:1 |
| CL-022 | Diamond Testers & Testing Methods | 3 | 0.0 | 0 | 0 | MEDIUM | CATEGORY:1; OTHER:1; EDITORIAL_GUIDE:1 |
| CL-041 | SI Clarity Diamonds (SI1, SI2, SI3) | 2 | 7.0 | 7 | 7 | HIGH | EDITORIAL_GUIDE:2 |
| CL-061 | Asscher Cut Diamonds | 3 | 1.3 | 0 | 4 | HIGH | OTHER:2; BRAND:1 |
| CL-070 | Natural Diamonds: General & Head Terms | 3 | 2.7 | 1 | 5 | HIGH | BRAND:3 |
| CL-071 | Rough & Raw Diamonds | 2 | 3.0 | 3 | 3 | HIGH | CATEGORY:2 |
| CL-090 | Moissanite: General & Head Terms | 3 | 0.7 | 0 | 2 | MEDIUM | MIXED:1; EDITORIAL_GUIDE:1; OTHER:1 |
| CL-092 | Moissanite vs Lab-Grown Diamond | 2 | 5.0 | 5 | 5 | HIGH | COMPARISON:2 |
| CL-093 | Do Moissanite Pass a Diamond Tester? | 4 | 4.2 | 4 | 5 | HIGH | OTHER:3; EDITORIAL_GUIDE:1 |
| CL-110 | Gold Karat: 14K vs 18K (and 10K) | 4 | 2.0 | 0 | 7 | HIGH | EDITORIAL_GUIDE:4 |
| CL-111 | Rhodium Plating & Replating Rings | 2 | 1.0 | 1 | 1 | MEDIUM | EDITORIAL_GUIDE:1; OTHER:1 |
| CL-113 | Tungsten & Titanium Wedding Bands | 2 | 0.0 | 0 | 0 | MEDIUM | EDITORIAL_GUIDE:2 |
| CL-115 | Jewellery Tarnish, Water & Everyday Wear | 2 | 0.0 | 0 | 0 | MEDIUM | EDITORIAL_GUIDE:2 |

**Where SERP evidence decided a split or merge (not word overlap):**
- CVD vs HPHT (CL-016), HPHT (CL-017) and CVD (CL-018) are three clusters. Shared top-10 URLs inside each: CL-016 mean 5.1, range 1-7 over 55 pair(s); CL-017 mean 6.9, range 6-8 over 10 pair(s); CL-018 mean 4.0, range 4-4 over 1 pair(s). Across clusters: CL-016 to CL-017 mean 1.9, range 0-4 over 55 pair(s); CL-016 to CL-018 mean 1.5, range 0-4 over 22 pair(s); CL-017 to CL-018 mean 2.1, range 1-3 over 10 pair(s). Cross-cluster relationships are marked POSSIBLE_OVERLAP. QC caught two "CVD vs lab grown" queries that shared 4 to 5 URLs with the CVD-vs-HPHT SERPs, so they were moved into CL-016 (SERP evidence overrides wording).
- Moissanite vs diamond (CL-091) and moissanite vs lab-grown diamond (CL-092): mean 0.0, range 0-0 over 2 pair(s). Moissanite head terms and moissanite vs lab-grown (CL-090 vs CL-092): mean 0.0, range 0-0 over 6 pair(s). Moissanite tester questions (CL-093) form their own tight group.
- The five certification clusters (CL-030 to CL-034) are separate. The general lab-grown certification SERP and the GIA-vs-IGI SERP (CL-033 vs CL-030): mean 0.0, range 0-0 over 1 pair(s). Stage 8 labelled the AGS grading SERP BRAND-dominant (navigational).
- "Are lab-grown diamonds real" (CL-010) and "lab-grown vs natural" (CL-011) are separate: mean 1.0, range 0-2 over 4 pair(s).
- "Natural diamond wholesale" was merged into the natural head-term cluster (CL-070) because it shares 5 URLs with "natural diamonds".
- "Diamond stone" (18,100) was **not clustered**. Its SERP mixes an NBA player, sharpening stones and GIA.
- Head terms (`lab grown diamonds`, `lab diamonds`, `diamond growing lab`, `lab diamond companies`) sit together in CL-001 (mean 3.3, range 1-7 over 6 pair(s)) even though they carry different Stage 8 labels (NAVIGATIONAL, TRANSACTIONAL). That is why CL-001's intent is MIXED.

## 6. Clusters and existing HOD content

This records only the relationship between a cluster and existing HOD content, as evidence from Stage 10. It does **not** mean keep, merge, create or retire anything. The basis is Stage 10's topic string-match plus Stage 3 rankings. A URL counts when it is linked to at least 2 members and at least 25% of the cluster's matched members (1 member for clusters of 3 or fewer), or when it holds a Stage 3 ranking for a member. Stage 10 states that a string match is not proof of relevance, and no match is not proof of absence.

| Relationship | Clusters | Cluster IDs |
|---|---|---|
| STRONG_EXISTING_CONTENT_SIGNAL | 5 | CL-011, CL-016, CL-017, CL-018, CL-110 |
| EXISTING_CONTENT_SIGNAL | 24 | CL-008, CL-010, CL-020, CL-022, CL-023, CL-040, CL-041, CL-042, CL-043, CL-044, CL-045, CL-047, CL-048, CL-049, CL-051, CL-060, CL-061, CL-062, CL-063, CL-064, CL-089, CL-113, CL-120, CL-122 |
| MULTIPLE_EXISTING_CONTENT_POSSIBLE_OVERLAP | 7 | CL-024, CL-030, CL-031, CL-032, CL-033, CL-034, CL-125 |
| NO_EXISTING_CONTENT_EVIDENCE | 45 | CL-001, CL-002, CL-003, CL-004, CL-005, CL-006, CL-007, CL-012, CL-013, CL-014, CL-015, CL-019, CL-021, CL-026, CL-046, CL-065, CL-070, CL-071, CL-073, CL-074, CL-075, CL-076, CL-080, CL-081, CL-083, CL-084, CL-085, CL-087, CL-088, CL-090, CL-091, CL-092, CL-093, CL-094, CL-095, CL-096, CL-100, CL-101, CL-102, CL-103, CL-104, CL-105, CL-111, CL-114, CL-121 |
| INSUFFICIENT_EVIDENCE | 8 | CL-009, CL-050, CL-082, CL-086, CL-112, CL-115, CL-123, CL-124 |

Clusters with an existing-content signal:

| Cluster | Name | Relationship | Stage 3 ranking keywords | Linked HOD URLs | Stage 10 documented page-pair label |
|---|---|---|---|---|---|
| CL-008 | Lab-Grown Diamond Pricing & Affordability | EXISTING_CONTENT_SIGNAL | 0 | blog/are-lab-grown-diamonds-real-a-complete-buyer-s-guide | NONE |
| CL-010 | Are Lab-Grown Diamonds Real? (Authenticity) | EXISTING_CONTENT_SIGNAL | 0 | blog/are-lab-grown-diamonds-real-a-complete-buyer-s-guide | NONE |
| CL-011 | Lab-Grown vs Natural Diamonds | STRONG_SIGNAL | 3 | blog/lab-grown-vs-natural-diamonds-the-honest-comparison | NONE |
| CL-016 | CVD vs HPHT Lab-Grown Diamonds | STRONG_SIGNAL | 11 | blog/cvd-vs-hpht-lab-grown-diamonds-what-buyers-should-know | NONE |
| CL-017 | HPHT Lab-Grown Diamonds | STRONG_SIGNAL | 5 | blog/cvd-vs-hpht-lab-grown-diamonds-what-buyers-should-know | NONE |
| CL-018 | CVD Lab-Grown Diamonds | STRONG_SIGNAL | 2 | blog/cvd-vs-hpht-lab-grown-diamonds-what-buyers-should-know | NONE |
| CL-020 | Telling Lab-Grown from Natural Diamonds (Identification & Detection) | EXISTING_CONTENT_SIGNAL | 0 | blog/lab-grown-vs-natural-diamonds-the-honest-comparison | NONE |
| CL-022 | Diamond Testers & Testing Methods | EXISTING_CONTENT_SIGNAL | 1 | blog/cvd-vs-hpht-lab-grown-diamonds-what-buyers-should-know | NONE |
| CL-023 | Lab-Grown Diamond Quality Grades & Charts | EXISTING_CONTENT_SIGNAL | 0 | blog/the-4cs-of-lab-grown-diamonds-explained-cut-colour-clarity-and-ca | NONE |
| CL-024 | Choosing a Lab-Grown Diamond (Buying Guidance) | MULTIPLE_POSSIBLE_OVERLAP | 1 | blog/how-to-choose-a-lab-grown-diamond-engagement-ring-online; blog/how-to-choose-a-lab-grown-diamond-the-complete-buyer-s-guide; /engagement-rings | OV-06:POSSIBLE_OVERLAP |
| CL-030 | Diamond Certification Lab Comparisons (GIA vs IGI vs Others) | MULTIPLE_POSSIBLE_OVERLAP | 0 | blog/igi-certification-for-lab-grown-diamonds-what-it-means; /education/lab-grown-diamond-certification-explained-gia-vs-igi | OV-01:CLEAR_OVERLAP |
| CL-031 | GIA Lab-Grown & Natural Diamond Reports | MULTIPLE_POSSIBLE_OVERLAP | 0 | blog/igi-certification-for-lab-grown-diamonds-what-it-means; /education/lab-grown-diamond-certification-explained-gia-vs-igi | OV-01:CLEAR_OVERLAP |
| CL-032 | IGI Lab-Grown Diamond Certification & Reports | MULTIPLE_POSSIBLE_OVERLAP | 0 | blog/igi-certification-for-lab-grown-diamonds-what-it-means; /education/lab-grown-diamond-certification-explained-gia-vs-igi | OV-01:CLEAR_OVERLAP |
| CL-033 | Lab-Grown Diamond Certification & Grading (Overview) | MULTIPLE_POSSIBLE_OVERLAP | 0 | blog/igi-certification-for-lab-grown-diamonds-what-it-means; /education/lab-grown-diamond-certification-explained-gia-vs-igi | OV-01:CLEAR_OVERLAP |
| CL-034 | Other Grading Labs, Report Lookup & Generic Diamond Reports | MULTIPLE_POSSIBLE_OVERLAP | 0 | blog/igi-certification-for-lab-grown-diamonds-what-it-means; /education/lab-grown-diamond-certification-explained-gia-vs-igi | OV-01:CLEAR_OVERLAP |
| CL-040 | Diamond Grading Scales & 4Cs Charts (General) | EXISTING_CONTENT_SIGNAL | 0 | blog/the-4cs-of-lab-grown-diamonds-explained-cut-colour-clarity-and-ca | NONE |
| CL-041 | SI Clarity Diamonds (SI1, SI2, SI3) | EXISTING_CONTENT_SIGNAL | 0 | blog/the-4cs-of-lab-grown-diamonds-explained-cut-colour-clarity-and-ca | NONE |
| CL-042 | VS Clarity Diamonds (VS1, VS2) | EXISTING_CONTENT_SIGNAL | 0 | blog/the-4cs-of-lab-grown-diamonds-explained-cut-colour-clarity-and-ca | NONE |
| CL-043 | VVS, IF & Flawless Clarity Diamonds | EXISTING_CONTENT_SIGNAL | 0 | blog/the-4cs-of-lab-grown-diamonds-explained-cut-colour-clarity-and-ca | NONE |
| CL-044 | Clarity Grade Comparisons (VS vs SI, VVS vs VS, IF vs FL) | EXISTING_CONTENT_SIGNAL | 0 | blog/the-4cs-of-lab-grown-diamonds-explained-cut-colour-clarity-and-ca | NONE |
| CL-045 | Best Diamond Clarity to Buy | EXISTING_CONTENT_SIGNAL | 0 | blog/the-4cs-of-lab-grown-diamonds-explained-cut-colour-clarity-and-ca | NONE |
| CL-047 | Diamond Color Grades: Comparisons & Quality | EXISTING_CONTENT_SIGNAL | 0 | blog/the-4cs-of-lab-grown-diamonds-explained-cut-colour-clarity-and-ca | NONE |
| CL-048 | Color & Clarity Grade Combinations (e.g. G/VS, F-VS2) | EXISTING_CONTENT_SIGNAL | 0 | blog/the-4cs-of-lab-grown-diamonds-explained-cut-colour-clarity-and-ca | NONE |
| CL-049 | Diamond Carat Size Suitability (Is It Big Enough?) | EXISTING_CONTENT_SIGNAL | 0 | blog/the-4cs-of-lab-grown-diamonds-explained-cut-colour-clarity-and-ca | NONE |
| CL-051 | Fancy-Colored Diamonds (Black, Red, Pink, Green, Purple & Others) | EXISTING_CONTENT_SIGNAL | 0 | blog/lab-grown-vs-natural-diamonds-the-honest-comparison | NONE |
| CL-060 | Diamond Shapes Overview | EXISTING_CONTENT_SIGNAL | 0 | blog/the-best-lab-grown-diamond-shapes-for-engagement-rings | NONE |
| CL-061 | Asscher Cut Diamonds | EXISTING_CONTENT_SIGNAL | 0 | blog/the-best-lab-grown-diamond-shapes-for-engagement-rings | NONE |
| CL-062 | Radiant Cut Diamonds | EXISTING_CONTENT_SIGNAL | 0 | blog/the-best-lab-grown-diamond-shapes-for-engagement-rings | NONE |
| CL-063 | Marquise-Oval & Moval Diamonds (Elongated Cuts) | EXISTING_CONTENT_SIGNAL | 1 | blog/the-best-lab-grown-diamond-shapes-for-engagement-rings; /shop/oval-floral-diamond-ring | OV-11:DISTINCT |
| CL-064 | Choosing a Diamond Shape (Emerald, Princess & Other Cuts) | EXISTING_CONTENT_SIGNAL | 0 | blog/the-best-lab-grown-diamond-shapes-for-engagement-rings | NONE |
| CL-089 | Treated & Enhanced Diamonds (Irradiation, Post-Growth Treatment) | EXISTING_CONTENT_SIGNAL | 0 | blog/the-4cs-of-lab-grown-diamonds-explained-cut-colour-clarity-and-ca | NONE |
| CL-110 | Gold Karat: 14K vs 18K (and 10K) | STRONG_SIGNAL | 3 | blog/14k-vs-18k-gold-for-diamond-jewellery-which-is-better | NONE |
| CL-113 | Tungsten & Titanium Wedding Bands | EXISTING_CONTENT_SIGNAL | 0 | /wedding-bands | NONE |
| CL-120 | Side-Stone Engagement Rings | EXISTING_CONTENT_SIGNAL | 1 | /engagement-rings; /engagement-rings/by-desgin/side-stone-rings | OV-17:DISTINCT |
| CL-122 | Engagement Ring Buying Questions (Returns, Wearing & Alternatives) | EXISTING_CONTENT_SIGNAL | 0 | /engagement-rings | NONE |
| CL-125 | Diamond Stud Earrings | MULTIPLE_POSSIBLE_OVERLAP | 0 | blog/the-4cs-of-lab-grown-diamonds-explained-cut-colour-clarity-and-ca; /fine-jewellery/earrings | NONE |

Existing HOD ranking equity is confined to 9 clusters, all at Stage 3 positions 27 to 104. HOD was in 0 of 795 organic results across the 100 Stage 8 SERPs. This is Stage 3/8/10 evidence restated, not a new finding.

| Stage 3 ranking keywords by cluster | Cluster | Keywords |
|---|---|---|
| CL-011 | Lab-Grown vs Natural Diamonds | 3 |
| CL-016 | CVD vs HPHT Lab-Grown Diamonds | 11 |
| CL-017 | HPHT Lab-Grown Diamonds | 5 |
| CL-018 | CVD Lab-Grown Diamonds | 2 |
| CL-022 | Diamond Testers & Testing Methods | 1 |
| CL-024 | Choosing a Lab-Grown Diamond (Buying Guidance) | 1 |
| CL-063 | Marquise-Oval & Moval Diamonds (Elongated Cuts) | 1 |
| CL-110 | Gold Karat: 14K vs 18K (and 10K) | 3 |
| CL-120 | Side-Stone Engagement Rings | 1 |

## 7. Cluster-level overlap and possible cannibalization

`11_cluster_relationships.csv` has 93 rows: 79 RELATED_BUT_DISTINCT, 13 POSSIBLE_OVERLAP, 1 DISTINCT_INTENT.
- Rows come from three bases: Stage 8 cross-cluster SERP overlap, semantic judgment, and existing HOD content shared between clusters.
- There are no STRONG_OVERLAP rows. No pair of validated keywords in different clusters shares 5 or more top-10 URLs (QC check in section 11).
- SERP-overlap evidence exists only where both clusters have validated members. Elsewhere the row says so, with LOW confidence.

**No actual cannibalization is claimed.** Stage 3 found no keyword with two HOD URLs ranking, and Stage 11 adds no new evidence of it. The cannibalization column reads NOT_DEMONSTRATED throughout. The overlap shown is topic overlap and SERP-sharing between clusters.

POSSIBLE_OVERLAP pairs:

| A | Name A | B | Name B | Type | Confidence | Basis |
|---|---|---|---|---|---|---|
| CL-016 | CVD vs HPHT Lab-Grown Diamonds | CL-017 | HPHT Lab-Grown Diamonds | POSSIBLE_OVERLAP | HIGH | SEMANTIC+SERP_OVERLAP+SHARED_EXISTING_CONTENT |
| CL-016 | CVD vs HPHT Lab-Grown Diamonds | CL-018 | CVD Lab-Grown Diamonds | POSSIBLE_OVERLAP | HIGH | SEMANTIC+SERP_OVERLAP+SHARED_EXISTING_CONTENT |
| CL-017 | HPHT Lab-Grown Diamonds | CL-018 | CVD Lab-Grown Diamonds | POSSIBLE_OVERLAP | HIGH | SEMANTIC+SERP_OVERLAP+SHARED_EXISTING_CONTENT |
| CL-013 | Ethical & Sustainable Lab-Grown Diamonds | CL-073 | Blood Diamonds & Conflict-Free Sourcing | POSSIBLE_OVERLAP | LOW | SEMANTIC |
| CL-015 | How Lab-Grown Diamonds Are Made (Process) | CL-075 | How Diamonds Form (Natural Formation) | POSSIBLE_OVERLAP | LOW | SEMANTIC |
| CL-021 | Do Lab-Grown Diamonds Pass a Diamond Teste | CL-093 | Do Moissanite Pass a Diamond Tester? | POSSIBLE_OVERLAP | LOW | SEMANTIC |
| CL-030 | Diamond Certification Lab Comparisons (GIA | CL-031 | GIA Lab-Grown & Natural Diamond Reports | POSSIBLE_OVERLAP | LOW | SEMANTIC+SHARED_EXISTING_CONTENT |
| CL-030 | Diamond Certification Lab Comparisons (GIA | CL-032 | IGI Lab-Grown Diamond Certification & Repo | POSSIBLE_OVERLAP | LOW | SEMANTIC+SHARED_EXISTING_CONTENT |
| CL-033 | Lab-Grown Diamond Certification & Grading  | CL-031 | GIA Lab-Grown & Natural Diamond Reports | POSSIBLE_OVERLAP | LOW | SEMANTIC+SHARED_EXISTING_CONTENT |
| CL-033 | Lab-Grown Diamond Certification & Grading  | CL-032 | IGI Lab-Grown Diamond Certification & Repo | POSSIBLE_OVERLAP | LOW | SEMANTIC+SHARED_EXISTING_CONTENT |
| CL-094 | Cubic Zirconia vs Diamond & Lab-Grown Diam | CL-095 | Diamond Simulants & Alternatives | POSSIBLE_OVERLAP | LOW | SEMANTIC |
| CL-100 | Sapphire: Natural, Lab-Created & White Sap | CL-102 | Lab-Created Gemstones (General & Other Sto | POSSIBLE_OVERLAP | LOW | SEMANTIC |
| CL-101 | Emerald: Natural & Lab-Grown | CL-102 | Lab-Created Gemstones (General & Other Sto | POSSIBLE_OVERLAP | LOW | SEMANTIC |

DISTINCT_INTENT pair(s), where the subject is shared but the need differs:

| A | B | Evidence |
|---|---|---|
| CL-001 | CL-002 | Head-term SERP is retailer/brand-dominant (navigational/commercial); definitional queries are informational. N |

Existing HOD content linked to more than one cluster (a fact about the current content set, not a recommendation):

| HOD URL | Clusters | Cluster IDs |
|---|---|---|
| /blog/the-4cs-of-lab-grown-diamonds-explained-cut-colour-clarity-and-carat | 12 | CL-023, CL-040, CL-041, CL-042, CL-043, CL-044, CL-045, CL-047, CL-048, CL-049, CL-089, CL-125 |
| /blog/igi-certification-for-lab-grown-diamonds-what-it-means | 5 | CL-030, CL-031, CL-032, CL-033, CL-034 |
| /education/lab-grown-diamond-certification-explained-gia-vs-igi | 5 | CL-030, CL-031, CL-032, CL-033, CL-034 |
| /blog/the-best-lab-grown-diamond-shapes-for-engagement-rings | 5 | CL-060, CL-061, CL-062, CL-063, CL-064 |
| /blog/cvd-vs-hpht-lab-grown-diamonds-what-buyers-should-know | 4 | CL-016, CL-017, CL-018, CL-022 |
| /blog/lab-grown-vs-natural-diamonds-the-honest-comparison | 3 | CL-011, CL-020, CL-051 |
| /engagement-rings | 3 | CL-024, CL-120, CL-122 |
| /blog/are-lab-grown-diamonds-real-a-complete-buyer-s-guide | 2 | CL-008, CL-010 |

The 4Cs, IGI and GIA-vs-IGI articles link to many clusters largely because Stage 10's topic patterns are broad. For example, all 58 certification keywords match both certification pages by construction (Stage 10 OV-01, CLEAR_OVERLAP at topic level, not proven cannibalization).

## 8. Sub-topic checks called out in the brief

| Topic | Cluster(s) | Note |
|---|---|---|
| Lab-grown diamonds | CL-001 to CL-015, CL-019 to CL-024, CL-026 | Split by searcher need: head/shopping, definition, names, types, geo, carat, wholesale, industry, price, value, authenticity, vs natural, worth-it, ethics, history, process, appearance, detection, testers, quality charts. |
| CVD / HPHT | CL-016, CL-017, CL-018 | Three SERP-supported clusters; the tester-device query sits in CL-022. |
| Lab-grown vs natural | CL-011 (plus CL-010, CL-070) | Comparison intent kept apart from authenticity and from natural head terms. |
| Certification | CL-030 to CL-034 | GIA vs IGI, GIA, IGI, general lab-grown, other labs/lookup. |
| 4Cs | CL-040 to CL-049, CL-050, CL-089 | Scales, SI, VS, VVS, grade comparisons, best clarity, inclusions, colour, colour+clarity, carat, cut, treatments. |
| Diamond shapes | CL-060 to CL-065 | Overview, Asscher, Radiant, Marquise-oval/Moval, shape choice, types overview. |
| Engagement rings | CL-120 to CL-124 | Side-stone (category SERP), setting types (editorial SERP), practicalities, mixed metal, sizing. |
| Wedding bands | none of its own; CL-113 (metals) | Keyword data gap. |
| Earrings | CL-125 | 6 keywords; a thin area. |
| Necklaces / pendants, Bracelets, Fine jewellery, Bespoke/custom | none | No cluster subject falls in these areas (keyword-data gap, consistent with Stages 4 to 10). The few keywords that mention necklaces or bracelets are metal/wear questions (CL-112, CL-115) or third-party brand queries. |
| Gemstones | CL-100 to CL-105 | Sapphire, emerald, lab-created stones, natural stones, morganite, coloured-gem rings. |
| Metals | CL-110 to CL-115, CL-123 | Gold karat, rhodium, metal types, tungsten/titanium bands, alternative-material rings, tarnish/wear, mixed metal. |
| Moissanite | CL-090 to CL-093, CL-096 | Clustered on the evidence only. **Clustering is not an endorsement as a HOD target**; business relevance is left to later stages. |
| Diamond simulants / CZ | CL-094, CL-095 | Kept separate from moissanite clusters. |

## 9. Stage 7 status overrides (audit)

Stage 7 marked many keywords INCLUDE because Stage 6 only applied lightweight noise flags. Reading the keywords, and using Stage 8 SERPs where available, showed off-topic and brand keywords inside INCLUDE. Stage 11 does not put them in a meaningful cluster. They are **overridden and labelled** in the map (`stage11_status_override`, `clustering_reason`). Stage 7 is untouched.

| Override reason (off-topic) | Keywords |
|---|---|
| INDUSTRIAL_ABRASIVE_OR_TOOL | 33 |
| CANNABIS_PRODUCT | 32 |
| GENERIC_NON_JEWELLERY_MEANING | 29 |
| GAMING_REFERENCE | 28 |
| NAMED_PERSON_OR_LOCAL_BUSINESS_OR_HARDWARE | 24 |
| UNRELATED_RING_PRODUCT_OR_CHEMISTRY | 18 |
| UNRELATED_CONSUMER_PRODUCT_OR_GAME | 11 |
| NON_JEWELLERY_MEANING | 10 |
| CRAFT_KIT | 4 |
| CONSUMER_PRODUCT_BRAND_UNRELATED | 3 |

Brand overrides (66 keywords) name a recognizable retailer or brand or follow the "<name> lab grown diamonds" pattern Stage 5 already used. Named entities: Tiffany & Co., Blue Nile, QVC, Brilliant Earth, En Route Jewelry, Kay Jewelers, HSN, IDC, Luvansh, Adamante, Affinity Diamonds, Macy's, VRAI, Aurate, Bhanderi, Calavera, Dew Moissanite, Diamonluxe, Diesel, Cartier, Diamonds Direct, Pandora, Eterneva, Evolv, Goenka, Helzberg, Ethan & Lara, Loose Grown Diamond, Matilda & Milo, Slide Jewelry, JTV, Kira, Zales, LVMH, MiaDonna, Natural Diamond Council, Nivoda, Prazana, Rapaport, Tacori, Triton.

Company-style names whose brand identity is **not verified** in project data (for example "providence diamond", "universal diamonds", "canos diamonds") were not labelled brands. They stay in UNCLUSTERED_REVIEW with the reason `POSSIBLE_BRAND_NAME_NOT_VERIFIED`. Review reasons: STAGE7_AMBIGUOUS_NO_STRONG_EVIDENCE (91), NO_RULE_MATCH (34), POSSIBLE_BRAND_NAME_NOT_VERIFIED (20), SERP_OR_SEMANTIC_DUAL_MEANING (9).

Stage 8 evidence used for overrides and holds:
- `thc diamond(s)`, `thca diamond` and `dust diamonds` are off-topic (cannabis / diamond painting).
- `diamond construction`, `detailing`, `recycling` and `equipment` return local businesses. `diamond deshields` and `reed diamond` return people.
- `diamond stone` is dual-meaning and is held for review.

## 10. Important uncertainties

1. **SERP evidence covers 100 of 1,936 keywords (5.2%).** 954 of 1,024 clustered keywords rely on semantic or lexical judgment. Cluster boundaries away from the validated keywords may move if more SERPs are checked. No new SERP call was made.
2. **The engine is rule-based, not a keyword-by-keyword manual judgment.** The rules are explicit and auditable (`clusters/scripts/rules.py`). Every cluster's member list was read in full and rules were corrected from that reading (see the inspection log). Some mis-assignments may remain, especially in the larger clusters.
3. **Broad clusters.** The clusters with 30 or more keywords are CL-005, CL-011, CL-049, CL-082. The largest clusters are CL-049 (36), CL-011 (31), CL-082 (31), CL-005 (30), CL-021 (28), CL-047 (28), CL-001 (27), CL-023 (26). Sub-needs inside them may separate once SERPs are checked. CL-005 spans US and non-US modifiers.
4. **Heterogeneous SERPs inside clusters.** CL-022 (testers) and CL-113 (tungsten vs titanium) contain validated pairs sharing 0 URLs. They are grouped by searcher need across different entities, so treat the boundary as uncertain.
5. **Ambiguous senses.** "Types of diamonds", "diamond shape" and "how are diamonds made" may serve more than one sense (shapes / natural vs lab / formation vs manufacture). CL-065 is MIXED and CL-075/CL-015 are flagged POSSIBLE_OVERLAP for that reason.
6. **Intent labels are weak for many keywords** (see section 3). Stage 8 inferred intent and page type with a disclosed heuristic (24% OTHER/UNCLEAR). Stage 11 inherits that limit.
7. **Stage 10 topic matching is coarse.** It over-links (certification, 4Cs) and misses (single-keyword matches). Existing-content labels are evidence, not a content audit. INSUFFICIENT_EVIDENCE is used where only isolated single-keyword matches exist.
8. **Thin or absent commercial coverage.** Wedding Bands, Necklaces & Pendants, Bracelets, Fine Jewellery and Bespoke have no clusters, and Earrings has one small cluster. Commercial category clusters that exist are engagement-ring side-stone/settings and gemstone/metal shopping terms. The master database is dominated by lab-grown education and 4Cs queries (Stage 4-7 sampling limits carried forward), so a cluster map built from it says nothing about demand for the missing areas.
9. **154 keywords are held in UNCLUSTERED_REVIEW.** Most are company-style names ("ab diamonds"), truncated phrases and dual-meaning terms. 21 Stage 7 AMBIGUOUS keywords were clustered because they were validated in Stage 8 or matched a topic-strong rule, and are marked SECONDARY (evidence LOW unless validated).
10. **Singleton clusters.** 2 clusters contain a single keyword: CL-060 (diamond shape), CL-120 (side stones engagement rings). They are kept because each is a distinct validated or ranking search need with no variants in the data, not because it is a page.
11. **Business relevance is not judged here.** Clusters on moissanite, CZ, industrial-adjacent science, synonyms and trade topics exist because the data has them. Whether they matter to HOD is for later stages.
12. **Volume caveat.** Raw volumes are not summed into demand estimates, and no cluster is scored or ranked.

## 11. QC results

| Check | Result | Detail |
|---|---|---|
| 1936 unique keywords in the map equal the Stage 7 master set | PASS | 1936 rows |
| No duplicate keyword-cluster mappings (one row per keyword) | PASS |  |
| Every Stage 7 INCLUDE keyword has exactly one disposition | PASS | {'CLUSTERED': 1003, 'NOISE': 128, 'COMPETITOR_BRAND': 65, 'UNCLUSTERED_REVIEW': 62} |
| All Stage 7 NOISE keywords remain NOISE | PASS |  |
| All Stage 7 COMPETITOR_BRAND keywords remain COMPETITOR_BRAND | PASS |  |
| Registry keyword_count sums to clustered keywords in the map | PASS | 1024 |
| Per-cluster counts: registry equals map for every cluster | PASS |  |
| Cluster IDs unique; cluster names unique | PASS |  |
| AMBIGUOUS keywords are only clustered on a topic-strong rule or Stage 8 evidence (no forced clustering) | PASS |  |
| Metrics preserved unchanged from Stage 7 (volume/cpc/competition/difficulty) | PASS |  |
| Stage 7 provenance preserved (status and source_stages) | PASS |  |
| All 28 Stage 3 ranking keywords preserved with rank/URL | PASS |  |
| All 100 Stage 8 validated keywords preserved | PASS |  |
| All 28 Stage 3 keywords are clustered (none lost to noise/brand/review) | PASS |  |
| Relationships reference valid clusters and use only the five permitted types | PASS |  |
| No cross-cluster fragmentation signal: no validated pair in different clusters shares >=5 top-10 URLs | PASS | [] |
| No URL/slug/page-recommendation columns in outputs | PASS |  |

**Manual inspection log** (Part 9). Files: `11_cluster_qc_inspection.csv`.

| Inspection group | Rows | Dispositions |
|---|---|---|
| Top 60 keywords by volume | 60 | {'CLUSTERED': 33, 'COMPETITOR_BRAND': 2, 'NOISE': 21, 'UNCLUSTERED_REVIEW': 4} |
| Stage 3 ranking keywords (28) | 28 | {'CLUSTERED': 28} |
| Stage 8 validated keywords (100) | 100 | {'CLUSTERED': 81, 'COMPETITOR_BRAND': 6, 'NOISE': 12, 'UNCLUSTERED_REVIEW': 1} |
| Stage 5 strategic seeds (55) | 55 | {'CLUSTERED': 53, 'UNCLUSTERED_REVIEW': 2} |
| Commercial category terms (rings, bands, earrings, necklaces, bracelets, fine/bespoke) | 82 | {'CLUSTERED': 72, 'COMPETITOR_BRAND': 9, 'UNCLUSTERED_REVIEW': 1} |
| Ambiguous or review keywords | 240 | {'UNCLUSTERED_REVIEW': 154, 'CLUSTERED': 21, 'NOISE': 64, 'COMPETITOR_BRAND': 1} |

Top 25 keywords by volume and where they went:

| Keyword | Volume | Stage 7 | Disposition | Cluster |
|---|---|---|---|---|
| moissanite | 201,000 | INCLUDE | CLUSTERED | CL-090 Moissanite: General & Head Terms |
| diamond growing lab | 135,000 | INCLUDE | CLUSTERED | CL-001 Lab-Grown Diamonds: General & Head Terms |
| helzberg diamonds | 135,000 | INCLUDE | COMPETITOR_BRAND |  |
| lab grown diamonds | 135,000 | INCLUDE | CLUSTERED | CL-001 Lab-Grown Diamonds: General & Head Terms |
| diamond crystal kosher salt | 60,500 | NOISE | NOISE |  |
| diamond shape | 60,500 | INCLUDE | CLUSTERED | CL-060 Diamond Shapes Overview |
| diamond barre | 49,500 | NOISE | NOISE |  |
| herkimer diamond | 33,100 | NOISE | NOISE |  |
| lab diamonds | 27,100 | AMBIGUOUS | CLUSTERED | CL-001 Lab-Grown Diamonds: General & Head Terms |
| lab grown vs natural diamonds | 22,200 | INCLUDE | CLUSTERED | CL-011 Lab-Grown vs Natural Diamonds |
| asscher cut diamond | 18,100 | INCLUDE | CLUSTERED | CL-061 Asscher Cut Diamonds |
| diamond stone | 18,100 | INCLUDE | UNCLUSTERED_REVIEW |  |
| natural diamonds | 18,100 | INCLUDE | CLUSTERED | CL-070 Natural Diamonds: General & Head Terms |
| v v s diamond | 18,100 | INCLUDE | CLUSTERED | CL-043 VVS, IF & Flawless Clarity Diamonds |
| are lab grown diamonds real | 14,800 | INCLUDE | CLUSTERED | CL-010 Are Lab-Grown Diamonds Real? (Authentici |
| blue nile diamonds | 14,800 | INCLUDE | COMPETITOR_BRAND |  |
| diamond dotz | 14,800 | INCLUDE | NOISE |  |
| reed diamond | 14,800 | AMBIGUOUS | NOISE |  |
| diamond clarity grading scale | 12,100 | INCLUDE | CLUSTERED | CL-040 Diamond Grading Scales & 4Cs Charts (Gen |
| diamond thc | 12,100 | INCLUDE | NOISE |  |
| diamonds thc | 12,100 | INCLUDE | NOISE |  |
| how are diamonds created | 12,100 | INCLUDE | CLUSTERED | CL-075 How Diamonds Form (Natural Formation) |
| how are diamonds formed | 12,100 | INCLUDE | CLUSTERED | CL-075 How Diamonds Form (Natural Formation) |
| how are diamonds made | 12,100 | INCLUDE | CLUSTERED | CL-075 How Diamonds Form (Natural Formation) |
| how diamond created | 12,100 | INCLUDE | CLUSTERED | CL-075 How Diamonds Form (Natural Formation) |

Stage 8 validated keywords not placed in a meaningful cluster (all deliberate, with reasons):

| Keyword | Stage 7 | Disposition | Basis |
|---|---|---|---|
| are tiffany diamonds natural or lab grown | INCLUDE | COMPETITOR_BRAND | STAGE11_BRAND_OVERRIDE |
| blue nile diamonds | INCLUDE | COMPETITOR_BRAND | STAGE11_BRAND_OVERRIDE |
| can i buy a tiffany ring without the diamond | INCLUDE | COMPETITOR_BRAND | STAGE11_BRAND_OVERRIDE |
| diamond construction | INCLUDE | NOISE | STAGE11_OFFTOPIC_OVERRIDE: NAMED_PERSON_OR_LOCAL_BUSINESS_OR_HARDWARE  |
| diamond deshields | AMBIGUOUS | NOISE | STAGE11_OFFTOPIC_OVERRIDE: NAMED_PERSON_OR_LOCAL_BUSINESS_OR_HARDWARE  |
| diamond detailing | AMBIGUOUS | NOISE | STAGE11_OFFTOPIC_OVERRIDE: NAMED_PERSON_OR_LOCAL_BUSINESS_OR_HARDWARE  |
| diamond dotz | INCLUDE | NOISE | STAGE11_OFFTOPIC_OVERRIDE: CRAFT_KIT (Stage 8: dust diamonds SERP = di |
| diamond equipment | AMBIGUOUS | NOISE | STAGE11_OFFTOPIC_OVERRIDE: NAMED_PERSON_OR_LOCAL_BUSINESS_OR_HARDWARE  |
| diamond recycling | INCLUDE | NOISE | STAGE11_OFFTOPIC_OVERRIDE: NAMED_PERSON_OR_LOCAL_BUSINESS_OR_HARDWARE  |
| diamond stone | INCLUDE | UNCLUSTERED_REVIEW | SERP_OR_SEMANTIC_DUAL_MEANING: Stage 8 SERP mixes an NBA player (baske |
| diamond thc | INCLUDE | NOISE | STAGE11_OFFTOPIC_OVERRIDE: CANNABIS_PRODUCT (Stage 8: thc/thca SERPs a |
| diesel bracelet | INCLUDE | COMPETITOR_BRAND | STAGE11_BRAND_OVERRIDE |
| dust diamonds | AMBIGUOUS | NOISE | STAGE11_OFFTOPIC_OVERRIDE: CRAFT_KIT (Stage 8: dust diamonds SERP = di |
| helzberg diamonds | INCLUDE | COMPETITOR_BRAND | STAGE11_BRAND_OVERRIDE |
| how can you tell if a tiffany bracelet is real | INCLUDE | COMPETITOR_BRAND | STAGE11_BRAND_OVERRIDE |
| reed diamond | AMBIGUOUS | NOISE | STAGE11_OFFTOPIC_OVERRIDE: NAMED_PERSON_OR_LOCAL_BUSINESS_OR_HARDWARE  |
| thc diamond | AMBIGUOUS | NOISE | STAGE11_OFFTOPIC_OVERRIDE: CANNABIS_PRODUCT (Stage 8: thc/thca SERPs a |
| thc diamonds | AMBIGUOUS | NOISE | STAGE11_OFFTOPIC_OVERRIDE: CANNABIS_PRODUCT (Stage 8: thc/thca SERPs a |
| thca diamond | AMBIGUOUS | NOISE | STAGE11_OFFTOPIC_OVERRIDE: CANNABIS_PRODUCT (Stage 8: thc/thca SERPs a |

Corrections made during manual inspection (each was a first-pass error found by reading the member lists):
- Lab-grown emerald/sapphire "are real" and "vs natural" queries had landed in the lab-grown diamond authenticity and comparison clusters. They were moved to the emerald and sapphire clusters.
- Moissanite queries that had landed in worth-it, tester and comparison clusters were rerouted to the moissanite clusters (rule priority).
- A regex bug matched "cvd diamond full form" (via "or" inside "form") to CVD-vs-HPHT. CVD-vs-HPHT now requires both CVD and HPHT tokens.
- Minecraft "y level", THC "liquid diamonds", local businesses and sports names inside Stage 7 INCLUDE were moved to NOISE (section 9).
- "Diamond stone" moved from a facts cluster to review because of its mixed SERP.
- "Natural diamond wholesale" merged into CL-070 on SERP evidence (shares 5 URLs).
- Cluster-level primary intents were reset after computing intent distributions from members, for example price/worth-it/carat to INFORMATIONAL and geo to MIXED.
- Names such as "providence diamond" were downgraded from brand to review because the brand identity is unverified.

## 12. DataForSEO spend

**Stage 11 completed with $0 additional DataForSEO spend.** Every question was answered from existing Stage 3-10 data, including the raw Stage 8 SERP files re-read for cross-cluster URL overlap. No paid endpoint was proposed or called, and no clickstream data was used. Cumulative spend remains $0.33536 of $51.00.

