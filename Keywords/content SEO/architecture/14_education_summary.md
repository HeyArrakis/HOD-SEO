# Stage 14 — Education strategy & architecture: summary

Date: 2026-09-24 · Scope: Education architecture only (no keyword→URL mapping, internal links, briefs, redirects or canonical tags) · Data: local Stage 3–13 files only · API spend: **$0.00** (cumulative unchanged at $0.33536)

**Files**
- `architecture/14_education_architecture.csv`: 45 topic records
- `architecture/14_education_hierarchy.csv`: 60 nodes
- `architecture/14_education_cluster_consolidation.csv`: 112 rows; all 89 clusters, each with exactly one PRIMARY row
- `content-strategy/14_education_existing_content_mapping.csv`: 16 rows
- `architecture/14_education_page_type_framework.csv`: 18 page types
- `architecture/14_education_decision_log.md`: D14-01 to D14-30
- `architecture/scripts/build_14_csvs.py`
- `architecture/scripts/qc_14.py`

**Evidence caveat.** Only 100 of 1,936 keywords have direct SERP evidence. The architecture separates HIGH, MEDIUM, LOW and INSUFFICIENT_EVIDENCE. Where evidence is missing, topics are CONDITIONAL or DEFERRED with an explicit interim home. Nothing is invented.

Stage 14 also re-read the paid Stage 8 raw SERPs to measure overlaps that Stage 11 did not report. The results decided several boundaries:

| SERP pair | Shared top-10 URLs |
|---|---|
| clarity scale vs SI2 | 0 |
| clarity scale vs VVS | 1 |
| SI2 vs SI2 variant | 7 |
| 'diamond shape' vs 'asscher cut diamond' | 0 |
| single-method CVD vs CVD-vs-HPHT | 3–4 |

Stage 14 also read the make-up of the HPHT SERP: 4 of 9 results are comparison pages.

---

## 1. Education role

Education is the **single evergreen home** for questions with a stable answer: what things are, how they work, how they are graded, how options compare, and how to choose (D14-01).

| System | Owns | Education's relationship |
|---|---|---|
| Education | Definitions, science, grading, comparisons, buying decisions, practical how-to | — |
| Blog | Dated and brand content: trends, market news, history/industry (CL-014, CL-026), Surat craft stories, launches, gifts | Blog links to Education for concepts |
| Categories / commercial hubs | Queries whose SERP is CATEGORY, PRODUCT or BRAND (CL-001, CL-006, CL-063, CL-070, CL-071, CL-104, CL-105, CL-120, CL-123, CL-125) | Education buying guides and pillars link to them |
| Product pages | One product | Shape and 4Cs guides link to relevant products (Stage 16) |
| FAQ | HOD policy and one-line answers | Each FAQ answer points to its Education owner (D14-30) |
| Tools | The interaction (e.g. sizing) | Embedded in the owning guide by default; the guide owns the search need (D14-23) |

## 2. Proposed hubs

**8 hubs: 7 firm + 1 conditional.** 10 candidates were evaluated (D14-02).

| Hub | Decision | Landing page | Evidence |
|---|---|---|---|
| Lab-Grown Diamonds | KEEP | Pillar: "Lab-grown diamonds explained" | HIGH |
| Natural Diamonds | KEEP (education-only, provisional) | Pillar: formation & origin | LOW |
| Diamond Quality (4Cs) | KEEP | Pillar: the 4Cs | MEDIUM |
| Diamond Shapes | SPLIT from "Shapes & Cuts": cut grade moved to 4Cs | Pillar: shapes guide | MEDIUM |
| Certification & Grading Reports | KEEP | Pillar: certification explained | MEDIUM |
| Metals & Materials | KEEP | Pillar: metals guide | MEDIUM |
| Gemstones & Diamond Alternatives | **CONDITIONAL** (business dependency) | Pillar: simulants & alternatives | MEDIUM |
| Ring & Jewellery Guides | KEEP (absorbs Care) | Index page | MEDIUM |
| Buying Guides | **MERGE**: a page type inside subject hubs, not a hub | — | — |
| Diamond Basics & Science | **MERGE**: root-level articles, no hub | — | LOW |

A hub landing page doubles as the broad topic resource ("pillar") wherever the hub has one broad question. This avoids a thin hub and a competing overview article (D14-03).

## 3. Proposed topic architecture (conceptual — not URLs)

Status key: **P** proposed · **Pv** provisional · **C** conditional · **D** deferred · **SEC** section inside a resource (no page).

```
Education (root index)
├─ Lab-Grown Diamonds [pillar: what they are, names, types, short history]  P
│   ├─ Are lab-grown diamonds real? (authenticity)                         P   ← are-real blog (move)
│   ├─ Lab-grown vs natural (comparison)                                   P   ← existing blog, stays at its URL
│   ├─ CVD vs HPHT (single home)                                           P   ← existing blog, stays at its URL
│   │    ├─ HPHT explained                                                 SEC
│   │    └─ CVD explained                                                  SEC
│   ├─ How lab-grown diamonds are made                                     C   (SERP test)
│   ├─ Price, value & resale                                               Pv
│   ├─ Are they worth it? (pros & cons)                                    C   (interim: section of lab-vs-natural)
│   ├─ Ethics & sustainability                                             Pv
│   ├─ Appearance & durability (cloudiness, fluorescence, treatments)      Pv
│   ├─ Detecting lab-grown (testers & identification)                      Pv
│   └─ How to choose a lab-grown diamond (buying guide)                    P   ← how-to-choose blog (deferred)
├─ Natural Diamonds [pillar: how they form, mining, rough identification]  Pv
│   ├─ Value, rarity & investment                                          C
│   └─ Conflict-free & responsible sourcing                                C   (needs HOD sourcing policy)
├─ Diamond Quality (4Cs) [pillar: 4Cs overview incl. lab-grown grading]    P   ← 4Cs blog (move)
│   ├─ Clarity guide (scale, inclusions, eye-clean, best clarity)          P
│   │    └─ VS clarity (interim section)                                   SEC
│   ├─ SI clarity                                                          P
│   ├─ VVS, IF & flawless                                                  P
│   ├─ VS clarity                                                          C
│   ├─ Colour guide                                                        P
│   ├─ Cut guide (grade, facets, light)                                    P
│   ├─ Carat guide                                                         Pv
│   └─ Fancy-coloured diamonds                                             C
├─ Diamond Shapes [pillar: shapes guide incl. engagement-ring choice]      P   ← shapes blog (move)
│   ├─ Per-shape sections (asscher, radiant, …)                            SEC
│   └─ Individual shape pages                                              D
├─ Certification & Grading Reports [pillar: certification explained]      P   ← IGI blog (retarget)
│   ├─ GIA vs IGI                                                          P   ← existing Education article
│   ├─ How to read a grading report                                        C
│   └─ IGI-only page                                                       D
├─ Metals & Materials [pillar: metals guide]                               Pv
│   ├─ 14k vs 18k gold                                                     P   ← 14k-vs-18k blog (move)
│   └─ Rhodium plating                                                     C
├─ Gemstones & Diamond Alternatives [pillar: simulants & CZ]  (hub CONDITIONAL)  C
│   ├─ Moissanite vs lab-grown                                             C
│   ├─ Moissanite vs diamond                                               C
│   ├─ Moissanite explained                                                D
│   └─ Coloured & lab-created gemstones                                    D
├─ Ring & Jewellery Guides [index]                                         P
│   ├─ Ring settings                                                       P
│   ├─ Ring size guide                                                     P   ← ring-size blog (move)
│   ├─ Ring size tool (embedded by default)                                C
│   ├─ Jewellery care & everyday wear                                      C
│   └─ Engagement ring buying guide                                        D   ← online-ring blog (deferred)
├─ Diamond properties: composition, hardness & durability (root)           Pv
└─ Types of diamonds (root)                                                C
```

**Counts.** 45 topic records:

| Status | Count |
|---|---|
| PROPOSED | 18 |
| PROPOSED_PROVISIONAL | 8 |
| CONDITIONAL | 14 |
| DEFERRED | 5 |

So **26 resources are proposed now** (18 firm + 8 provisional), against 89 clusters. Each hub's why, need, owns and does-not-own are in `14_education_hierarchy.csv`.

## 4. Major consolidation decisions

All 89 clusters have one PRIMARY decision:

| Decision | Clusters |
|---|---|
| DEDICATED_RESOURCE | 24 |
| CONSOLIDATE_INTO_TOPIC | 27 |
| CONDITIONAL_RESOURCE | 14 |
| DEFER | 8 |
| EXCLUDE_NOT_EDUCATION | 14 |
| EXCLUDE_OFF_SCOPE | 2 |

23 SECONDARY rows record interim homes and shared sub-topics. The largest consolidations:

| Resource | Clusters merged |
|---|---|
| CVD vs HPHT | CL-016 + CL-017 + CL-018 |
| Lab-grown pillar | CL-002 + CL-003 + CL-004 |
| Price/value/resale | CL-008 + CL-009 + CL-086 |
| Detection | CL-020 + CL-021 + CL-022 |
| 4Cs pillar | CL-040 + CL-023 + CL-048 |
| Clarity guide | CL-044 + CL-045 + CL-046 |
| Shapes pillar | CL-060 + CL-061 + CL-062 + CL-064 |
| Certification pillar | CL-033 + CL-031 + CL-032 |
| Diamond properties | CL-080 + CL-081 + CL-082 + CL-083 + CL-087 |
| Natural pillar | CL-075 + CL-074 |

## 5. Lab-grown architecture

- **Head terms (CL-001)** are commercial (BRAND/CATEGORY SERPs). They are excluded from Education and belong to the conditional commercial Lab-Grown hub.
- **Pillar** (CL-002/003/004): definition, names (lab-grown / lab-created / synthetic / FTC), types, and a short history. Dated trends (CL-014) go to the Blog.
- **CVD / HPHT: one resource (D14-06).** HPHT and CVD are subordinate sections of the existing CVD-vs-HPHT article. **No independent CVD or HPHT pages.** The evidence:
  - The HPHT head SERP is led by HPHT-vs-CVD comparison pages (4 of 9) plus GIA's combined process page.
  - Single-method CVD SERPs share 3–4 URLs with CVD-vs-HPHT SERPs.
  - HOD's comparison article already ranks for HPHT (pos 49, about 34 of its 36.5 ETV) and for CVD (pos 27/36).
  - A CVD-only page may be revisited under two joint conditions. An HPHT split is not recommended.
- **Real vs lab-vs-natural boundary (D14-07).** "Real?" owns authenticity: identical material, FTC definition, synthetic vs simulant. The comparison page owns the choice: price, value, appearance, ethics side by side. The SERPs share at most 2 URLs, but both are COMPARISON-type, so the risk is **MEDIUM** and the boundary must be kept in content.
- **Process (CL-015).** Conditional, because process guides already rank inside the HPHT and CVD SERPs. A 3-URL SERP test decides fold vs separate.
- **Worth-it (CL-012).** Conditional. Interim home: a pros/cons section of the lab-vs-natural page.
- **Other topics:** quality/appearance (CL-019, CL-089), ethics (CL-013), detection (CL-020/021/022) and price/value/resale are separate, provisional resources. Lab-grown **quality charts (CL-023)** are integrated into the general 4Cs pillar.
- **Certification** for lab-grown is owned by the Certification hub.
- **Choosing a lab-grown diamond** (CL-024) is a buying guide. The existing article's migration stays deferred (Stage 13).

## 6. 4Cs architecture

One **4Cs pillar** (overview, charts, colour+clarity combinations, how lab-grown is graded) with:

| Resource | Status | Evidence |
|---|---|---|
| Clarity guide (scale, inclusions, eye-clean, best clarity, grade comparisons) | Proposed | Clarity-scale SERP shares 0–1 URLs with grade SERPs |
| SI clarity | Proposed | HIGH: two SI2 SERPs share 7 URLs |
| VVS/IF/FL | Proposed | MEDIUM: 18,100 head, EDITORIAL |
| VS clarity | Conditional (interim: clarity guide section) | No SERP |
| Colour guide | Proposed | Validated EDITORIAL |
| Cut guide (incl. facets/optics) | Proposed | Validated EDITORIAL |
| Carat guide | Provisional | 36 kw, no SERP; no per-carat pages |
| Fancy colour | Conditional | Business dependency |

Grade-vs-grade comparisons (CL-044) are sections, not pages: grade SERPs already contain comparison pages. **Lab-grown-specific quality is integrated, not separate**, because a separate lab-grown 4Cs page would compete with the general one. That boundary is INSUFFICIENT_EVIDENCE and needs a later SERP check.

**Stage 15 flag.** 'diamond clarity grading scale' (12,100) sits in CL-040, but its SERP is clarity pages, so it belongs to the clarity guide.

## 7. Certification architecture

- **Pillar = general lab-grown certification** (CL-033, with GIA/IGI report questions as sections). This is the **retarget destination for the IGI blog**. It resolves Stage 13's open question in favour of CL-033, the only non-comparison certification cluster with SERP evidence.
- **GIA vs IGI** (CL-030): the existing Education article, narrowed to the comparison intent (UPDATE_IN_PLACE).
- **How to read a grading report** (CL-034): conditional. Lab lookups are navigational to the labs.
- **IGI-only page:** deferred. No IGI SERP evidence, and building it would recreate OV-01.
- The Stage 13 split is preserved: the comparison SERP and the general SERP share 0 URLs. Both content changes ship together.

## 8. Shapes / cuts architecture

- **"Cut" is split:**
  - Cut *grade* goes to the 4Cs cut guide.
  - *Shape* names ('asscher cut') go to Shapes.
- **One shapes pillar** covers the overview and engagement-ring shape choice. The 'diamond shape' (60,500) SERP is led by GIA's shapes-for-engagement-rings guide, so Google blends the two. The existing shapes article becomes this pillar.
- **Per-shape pages are deferred.** The 'asscher cut diamond' (18,100) SERP is inventory-led (1 of 7 results is an education page) and shares 0 URLs with 'diamond shape'.
- Shapes appear as sections inside the pillar. Moval/marquise-oval (CL-063) is commercial (PRODUCT SERP; HOD PDP ranks).

## 9. Natural diamonds and gemstones

- **Natural (education only):**
  - Pillar = formation and mining ('how is diamond formed', 12,100), with rough-diamond identification as a section.
  - Value, rarity and investment: conditional.
  - Conflict-free sourcing: conditional. Its SERP is retailer sourcing-policy pages, and it needs a substantiated HOD policy.
  - 'natural diamonds' and 'raw diamond' are commercial SERPs. The commercial natural hub stays deferred (Stage 12 D-05).
- **Gemstones & Alternatives (hub CONDITIONAL):**
  - Simulants/CZ pillar, moissanite vs lab-grown (HIGH evidence, the most business-relevant) and moissanite vs diamond are all **conditional**. They share 0 URLs, so they would be separate pages.
  - Moissanite itself (201,000, retailer-led SERP) and coloured gemstones are **deferred**.
  - Gemstone ring shopping is excluded.
  - Volume is not treated as evidence that HOD should target moissanite (Stage 11/12).

## 10. Existing-content destinations

| Existing content | Hub → topic | Stage 14 status |
|---|---|---|
| CVD vs HPHT blog | Lab-Grown → CVD vs HPHT (single home) | **Stays at current URL** (HIGH risk; DO_NOT_MOVE_NOW) |
| Lab-grown vs natural blog | Lab-Grown → Lab-grown vs natural | **Stays at current URL** (HIGH risk; DO_NOT_MOVE_NOW) |
| Are lab-grown diamonds real blog | Lab-Grown → Authenticity | Move when conditions met |
| 4Cs of lab-grown blog | Diamond Quality → 4Cs pillar (general, with lab-grown section) | Move when conditions met |
| Best lab-grown shapes blog | Shapes → Shapes pillar | Move when conditions met |
| Ring size blog | Ring & Jewellery Guides → Ring size guide | Move when conditions met |
| 14k vs 18k blog | Metals → 14k vs 18k | Move when conditions met |
| IGI certification blog | Certification → Certification pillar (CL-033) | Retarget, then move when conditions met |
| GIA vs IGI (Education) | Certification → GIA vs IGI | Already in Education; update in place |
| How to choose a lab-grown diamond blog | Lab-Grown → Buying guide | Deferred (Stage 13) |
| Buy engagement ring online blog | Ring & Jewellery Guides → Engagement ring buying guide (deferred) | Deferred (D-19) |
| /education hub | Education root index | Root |
| /blog, /faq, ranking PDP, side-stone subcategory | Not Education | Unchanged |

No Stage 13 action, risk level or migration condition was changed. Stage 14 only names destinations and answers Stage 13's scope questions.

## 11. Cannibalization risks

The rules are listed in D14-27. In short:
- One need, one owning resource.
- Comparison stays separate from definition unless 3 or more URLs are shared.
- No informational page targets a CATEGORY, PRODUCT or BRAND SERP.
- A separate page needs SERP evidence or a distinct need; volume alone never justifies one.
- No merges on shared words alone.
- Pillars own the broad question and children own the narrow ones.
- Interim homes are explicit.
- New pages never target the queries existing ranking URLs hold.

Boundaries by risk level:
- **HIGH:**
  - CVD vs HPHT ↔ single-method or process pages
  - general 4Cs ↔ lab-grown 4Cs (if split)
  - certification pillar ↔ IGI-only page
- **MEDIUM:**
  - authenticity ↔ comparison
  - price/resale ↔ worth-it
  - ethics ↔ conflict-free
  - 4Cs pillar ↔ clarity guide
  - cut ↔ shapes
  - certification pillar ↔ GIA vs IGI
  - simulants ↔ authenticity
  - lab-grown detection ↔ moissanite tester
- **INSUFFICIENT_EVIDENCE:**
  - worth-it ↔ authenticity/comparison
  - lab process ↔ natural formation
  - VS page
  - engagement-ring guide ↔ lab-grown buying guide
  - 'types of diamonds'

No cannibalization is demonstrated anywhere: no keyword has two HOD URLs ranking.

## 12. Unresolved questions

1. **Business (no API cost):**
   - Does HOD sell natural diamonds? This affects the scope of the natural hub.
   - Moissanite, gemstones or fancy-colour diamonds? This affects the Gemstones hub and fancy colour.
   - White gold with rhodium aftercare? This affects the rhodium page.
   - A documented sourcing policy? This affects conflict-free content.
   - Loose diamonds? This affects per-shape and carat pages.
2. **SERP boundaries (INSUFFICIENT_EVIDENCE):**
   - process vs CVD/HPHT
   - worth-it vs real/comparison
   - lab-grown charts vs 4Cs
   - VS page
   - IGI-only page
   - 'types of diamonds' sense
   - ring-size tool vs guide
   - lab process vs natural formation
3. **Engagement-ring buying guide:** depends on the unapproved D-19 commercial supplement.
4. **CVD single-method revisit:** needs GSC after the in-place update, plus a 'cvd diamond' SERP.
5. **Ring-size and care demand:** not in the master database. It is unmeasured, not absent.
6. **Stage 13 UX question:** should the Blog hub list Education-owned articles that stay on /blog URLs?

**Is more paid research necessary?** Not to complete Stage 14. An **optional** 16-task SERP batch would resolve 8 of the INSUFFICIENT_EVIDENCE boundaries (D14-29):
- Endpoint: `serp/google/organic/task_post`
- Settings: US 2840 / en, desktop, depth 10, normal priority
- Maximum cost: **$0.0096**

It was **not run and is not authorised**. It could be bundled with the still-unapproved D-19 supplement before Stage 15. Every affected topic already has an interim home, so Stage 15 can proceed without it by mapping to the interim homes.

## 13. What Stage 15 must do next

1. Map keywords to URLs for the 26 proposed resources and the interim homes. The consolidation file's SECONDARY rows mark keywords that may sit on a different page from their cluster's primary home (for example clarity-scale keywords → clarity guide; 'vvs lab diamonds' → VVS page; SI/VVS comparisons → grade pages).
2. Keep the CVD-vs-HPHT and lab-vs-natural URLs as the mapping targets for CL-016/017/018 and CL-011. Do not map those keywords to any new page.
3. Keep commercial clusters (CL-001, CL-006, CL-063, CL-070, CL-071, CL-104, CL-105, CL-120, CL-123, CL-125) off Education URLs.
4. Decide Education URL expression and depth from this conceptual hierarchy: hub-as-pillar, and no slugs decided here. Stage 12 D-12 URL principles and D-17 platform constraints apply.
5. Check every assignment against the D14-27 rules.
6. Leave CONDITIONAL and DEFERRED topics unmapped, unless the owner approves the optional SERP batch (D14-29), the D-19 supplement, or answers the business questions.

Stage 15 was **not** started.
