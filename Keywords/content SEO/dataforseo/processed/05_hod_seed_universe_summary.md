# House of Diams — Stage 5: Strategic Keyword Seed Universe Summary

Date: 2026-09-17
Source: Stage 4's `dataforseo/processed/04_hod_keyword_universe.csv` (1,000 keywords, already paid for — no new DataForSEO calls this stage).
Method: rule-based classification (regex/keyword-pattern rules built from a full manual read of all 1,000 keyword strings), applied programmatically because manual row-by-row judgment isn't tractable at this volume. The rule set and its outputs were spot-checked and iteratively corrected against the raw list before finalizing (see §15–16 for known limitations of this method).

**Paid DataForSEO API calls this stage: 0. Cost: $0.00.**

---

## 1. Total Stage 4 keywords classified

**1,000 of 1,000.** No keyword was dropped, deduplicated, or silently removed. Every row from `04_hod_keyword_universe.csv` appears exactly once in `05_hod_keyword_classification.csv`, including all noise.

## 2–3. Counts and percentages by relevance class

| Class | Label | Count | % of total |
|---|---|---:|---:|
| A | DIRECT_PRODUCT | 25 | 2.5% |
| B | DIRECT_EDUCATION | 338 | 33.8% |
| C | ADJACENT_RELEVANT | 8 | 0.8% |
| D | COMPETITOR_OR_BRAND | 43 | 4.3% |
| E | INFORMATIONAL_ADJACENT | 1 | 0.1% |
| F | AMBIGUOUS | 137 | 13.7% |
| G | IRRELEVANT_NOISE | 448 | 44.8% |

**Read this alongside Stage 4's own finding**: this specific 1,000-row `keywords_for_site` pull is a relevance-ranked *discovery* sample, not the full 518,487-keyword domain-associated pool, and it skews heavily toward diamond material/education/certification vocabulary plus a large amount of word-polysemy noise ("diamond," "ring," and gemstone-name collisions with Minecraft, Pokémon, home-security cameras, industrial tooling, and unrelated consumer brands). That pattern is confirmed and quantified here: **44.8% of this sample is noise**, and only **2.5% is direct product vocabulary** (engagement ring / wedding band / earrings / necklace / bracelet terms were almost entirely absent from the Stage 4 pull itself, as already flagged in that stage's summary).

## 4. Counts by business area

| Business area | Count |
|---|---:|
| 18. Other / Unclear (noise + ambiguous) | 584 |
| 12. Diamond Quality / 4Cs | 141 |
| 8. Lab-Grown Diamonds | 128 |
| 17. Competitor / Brand | 43 |
| 14. Diamond Buying / Education | 35 |
| 13. Diamond Certification | 32 |
| 1. Engagement Rings | 12 |
| 10. Diamond Shapes | 8 |
| 9. Natural Diamonds | 7 |
| 15. Jewellery Materials / Metals | 5 |
| 16. Gemstones | 3 |
| 3. Earrings | 2 |
| 2. Wedding Bands / 4. Necklaces & Pendants / 5. Bracelets / 6. Fine Jewellery / 7. Bespoke / 11. Diamond Cuts | 0 each |

Six of the eighteen controlled business areas have **zero** matched keywords in this specific sample — consistent with Stage 4's finding that explicit product-category vocabulary is essentially absent from this discovery pull. This is a property of the sample, not a claim that search demand doesn't exist for wedding bands, necklaces, bracelets, fine jewellery, or bespoke jewellery — see §18 (coverage gaps).

## 5. Counts by analyst intent

| Analyst intent | Count |
|---|---:|
| UNKNOWN (noise/ambiguous, intent not meaningfully assignable) | 585 |
| INFORMATIONAL | 313 |
| COMMERCIAL_RESEARCH | 62 |
| NAVIGATIONAL | 26 (mostly competitor/brand terms) |
| MIXED | 14 |
| TRANSACTIONAL | 0 |

`analyst_intent` was derived independently from `dataforseo_intent` using question-word and comparison-pattern heuristics on the keyword text itself, per instruction not to treat DataForSEO's own intent field as ground truth. Both fields are preserved separately in the full classification dataset (`05_hod_keyword_classification.csv`) for comparison. Note the absence of any TRANSACTIONAL analyst-intent assignment: this sample is overwhelmingly informational/comparison-shaped ("X vs Y," "is X good," "how is X made") rather than bare product-purchase phrasing — consistent with Stage 4's finding that explicit transactional product-category terms are largely absent from this pull.

## 6. Counts by seed eligibility

| Seed eligibility | Count |
|---|---:|
| NO | 904 |
| YES | 55 |
| REVIEW | 41 |

## 7–9. Seed / review / noise counts

- **Strategic seeds (YES): 55**
- **Review queue (REVIEW): 41** (36 non-competitor borderline terms + 5 highest-volume competitor/brand terms flagged for Stage 9 usefulness)
- **Noise (class G): 448**

## 10. Strategic seed coverage by business area

| Business area | Seed count |
|---|---:|
| 8. Lab-Grown Diamonds | 11 |
| 12. Diamond Quality / 4Cs | 10 |
| 13. Diamond Certification | 8 |
| 10. Diamond Shapes | 8 |
| 14. Diamond Buying / Education | 6 |
| 9. Natural Diamonds | 4 |
| 16. Gemstones | 2 |
| 1. Engagement Rings | 2 |
| 15. Jewellery Materials / Metals | 2 |
| 3. Earrings | 2 |
| Wedding Bands / Necklaces & Pendants / Bracelets / Fine Jewellery / Bespoke / Diamond Cuts | 0 |

## 11. Strategic seed coverage by search intent

| Analyst intent | Seed count |
|---|---:|
| INFORMATIONAL | 42 |
| COMMERCIAL_RESEARCH | 9 |
| MIXED | 4 |
| NAVIGATIONAL / TRANSACTIONAL | 0 |

The strategic seed list is currently informational-heavy. This mirrors the underlying Stage 4 sample rather than a deliberate editorial choice — Stage 6's expansion (and, if needed, a later fuller `keywords_for_site` pull or a catalog-driven `related_keywords`/`keyword_ideas` expansion in Stage 6B) is where transactional/commercial product-purchase vocabulary should be built out deliberately.

## 12. Strategic seed coverage by seed role

| Seed role | Count |
|---|---:|
| QUESTION | 27 |
| LONG_TAIL | 8 |
| COMPARISON | 9 |
| EDUCATION | 5 |
| ATTRIBUTE | 5 |
| HEAD | 1 |
| CATEGORY / PRODUCT | 0 |

Only one HEAD term was selected (`lab grown diamonds`) — deliberately, per instruction not to overuse HEAD. Zero CATEGORY or PRODUCT-role seeds exist because this specific discovery sample contains almost no explicit product-category phrasing (see §4); this is a real gap, not an oversight (see §18).

## 13. Existing HOD ranking overlap

- **Strategic seeds that currently rank: 1 of 55** — `hpht lab grown diamonds` (rank 49, ranking on `/blog/cvd-vs-hpht-lab-grown-diamonds-what-buyers-should-know-house-of-diams`).
- **Strategic seeds that do not currently rank: 54 of 55.**

This is consistent with Stage 3's finding that HOD's entire current organic footprint is 28 keywords, none in the top 20. The seed universe is intentionally built from strategic relevance, not existing rankings, so this low overlap is expected, not a defect.

## 14. Existing-site representation (across all 1,000 classified keywords)

| current_site_representation | Count |
|---|---:|
| UNKNOWN (noise/ambiguous — not applicable) | 586 |
| EXISTING_BLOG | 220 |
| NO_CLEAR_EXISTING_PAGE | 148 |
| MULTIPLE | 32 |
| EXISTING_CATEGORY | 12 |
| EXISTING_PRODUCT | 2 |
| EXISTING_EDUCATION / EXISTING_CORE_PAGE | 0 |

Among the **55 strategic seeds only**: EXISTING_BLOG 25, NO_CLEAR_EXISTING_PAGE 18, MULTIPLE 8, EXISTING_CATEGORY 2, EXISTING_PRODUCT 2.

**Important caveat**: `current_site_representation` here is a best-effort topical mapping from the Stage 1 site inventory's documented findings (e.g., "the CVD vs HPHT blog article exists," "no dedicated grade-comparison content exists," "GIA-vs-IGI content is split across /blog and /education") — it is **not** a fresh per-URL crawl match against every one of the 1,000 keywords. It should be read as directional, not verified, and is explicitly **not** a recommendation to create, merge, or retire any page (that is Stage 13).

## 15. Top examples of correctly classified noise

By volume of noise sub-type found in this sample:

| Noise type | Count | Examples |
|---|---:|---|
| Industrial diamond tooling / material science | 132 | `diamond core bit`, `diamond hardness mohs scale`, `diamond fcc structure`, `diamond wire die` |
| Video game (Minecraft / Pokémon / misc) | 89 | `netherite ingot`, `what is the best y level for diamonds`, `can you trade diamonds with villagers`, `which is better diamond or pearl` |
| Non-diamond hobbyist mineral/crystal | 67 | `selenite wand`, `onyx cinder`, `eli gemstone`, `shungite and black tourmaline` |
| Generic/industrial metal "ring" hardware | 88 | `epdm o rings`, `retaining ring e type`, `titanium split ring`, `galvanized d-rings` |
| Unrelated consumer brand/product | 29 | `diamondclean vs prestige` (Philips Sonicare), `ihg platinum vs diamond` (IHG hotel tier), `sapphire pulse vs pure` (GPU model) |
| Home-security "Ring" brand comparisons | 10 | `wyze vs ring`, `vivint vs ring`, `is arlo better than ring` |
| No diamond/jewellery signal at all | 32 | `ringer vs milorganite`, `sw emerald vs duration`, `titanite ds3` |

## 16. Top examples of ambiguous terms (class F)

137 keywords could not be confidently classified from the keyword text alone and were left AMBIGUOUS rather than force-fit into another class — consistent with the instruction to avoid fake precision:

`v v s diamond` (irregular spacing of "VVS diamond" — likely real but oddly tokenized), `diamond deshields`, `vimco diamonds`, `hrk diamonds`, `ld diamonds`, `ccs diamonds`, `tsc diamonds`, `oxford diamonds`, `allied diamond`, `cellini diamond`, `molteni diamond`, `is platinum better than diamonds` (could be metal-vs-diamond or a Pokémon Platinum reference, given how much Pokémon "Diamond/Pearl/Platinum" noise exists elsewhere in this sample), `what brand of diamond is the best`, `diamond lab report`, `what's inside diamond`.

Several short "[word] diamond(s)" entries (`vimco diamonds`, `dmi diamonds`, `hrk diamonds`, `ld diamonds`, `ccs diamonds`, `tsc diamonds`) read like they could be diamond dealer/wholesaler business names, but none could be confirmed from the keyword text alone — flagged for REVIEW rather than guessed into COMPETITOR_OR_BRAND or DIRECT_EDUCATION.

## 17. Competitor/brand keyword examples

43 keywords total (class D). Top by volume:

| Keyword | Volume |
|---|---:|
| ritani lab grown diamonds | 4,400 |
| diavik diamonds | 1,600 |
| rahaminov diamonds | 720 |
| does kay jewelers buy back rings | 390 |
| is tiffany jewelry worth it | 260 |
| are gld chains real diamonds | 140 |
| luvansh lab grown diamonds | 140 |
| does tiffany use lab grown diamonds | 110 |

Also present: lab-grown diamond grower/brand names (`caydia`, `maitri`, `idyl`, `titan`, `w d`/`wd`, `engrace`, `fenix`, `adamante`, `gemesis`, `apollo`, `evolv`, `stuller`, `limelight`, `ags`), luxury-house mentions (`van cleef`, `lvmh`, `tanishq`), and retailer-policy questions (`kay jewelers`, `jared`). All 43 are preserved in the main classification dataset and separately in the review queue (top 5 by volume, REVIEW) or main dataset (remainder, NO) — none were used as product/education seeds, and no competitor research was performed this stage.

## 18. Important coverage gaps in the seed universe

These are observations about what this seed universe does and doesn't cover — **not page, blog, or URL recommendations**:

1. **Zero seeds for Wedding Bands, Necklaces & Pendants, Bracelets, Fine Jewellery, and Bespoke/Custom Jewellery** — the Stage 4 discovery pull this stage worked from contained essentially no keywords in these business areas (confirmed in Stage 4's own summary: 0 matches for "wedding band," "necklace," "pendant," "bracelet" in that 1,000-row sample). Per Stage 1's site inventory, these are exactly the categories with the least existing dedicated site architecture (no category URL for earrings, necklaces/pendants, or bracelets at all) — so this is a gap in *this specific keyword sample*, not evidence about real-world search demand either way.
2. **Zero CATEGORY- or PRODUCT-role seeds anywhere** — the sample skews to comparison/question-shaped informational queries; head-and-category-level commercial phrasing ("lab grown diamond engagement rings," "diamond stud earrings," "tennis bracelet") is absent from this pull.
3. **Diamond Cuts (business area 11) has zero matched keywords** as a distinct area from Diamond Shapes (area 10) — shape and cut terminology overlapped heavily in this sample and were consolidated under Diamond Shapes; a dedicated cut-quality angle (ideal cut, super ideal cut, cut grade vs shape) exists only as a handful of rows nested inside Diamond Quality / 4Cs.
4. **Engagement Rings seeds are thin (2) and attribute-only** — no HEAD-level "engagement ring" seed exists because that literal phrase does not appear in this 1,000-row sample at all (confirmed against Stage 4).
5. **Natural Diamonds seeds skew toward mining ethics** (blood diamonds, Kimberley Process) rather than natural-diamond buying/value education — a real informational angle, but not the only one HOD may want to cover.

**Recommended (not decided) response**: Stage 6's quantitative expansion should deliberately seed from HOD's actual product/category vocabulary (engagement ring styles, settings, wedding band types, earring/necklace/bracelet subtypes) directly — rather than relying solely on this `keywords_for_site`-derived sample — precisely because this discovery method has now been shown twice (Stage 4 and this stage) not to surface that vocabulary on its own.

---

## Quality control checklist

- [x] Exactly 1,000 Stage 4 keywords classified (verified: `len(full_rows) == 1000`, no duplicate keyword strings)
- [x] No Stage 4 keyword silently lost — every row appears in `05_hod_keyword_classification.csv`
- [x] Raw Stage 4 CSV (`04_hod_keyword_universe.csv`) untouched
- [x] Noise (448 rows) remains inside the full classification dataset, not deleted
- [x] Competitor terms (43 rows) kept separate from the product/education seed pool
- [x] Zero paid DataForSEO calls made this stage
- [x] No clustering performed
- [x] No page, URL, or blog recommendations made
- [x] No competitor research performed (competitor terms only catalogued)
- [x] No keyword score, ranking, or priority number invented
- [x] Stage 3 ranking data used only as a cross-reference (`hod_currently_ranks` / `hod_current_rank` / `hod_ranking_url`)
- [x] Stage 1 site inventory used only for a best-effort `current_site_representation` mapping, explicitly caveated as non-exhaustive
- [x] Seed selection driven by strategic relevance + topical distinctiveness (subgroup coverage), with search volume used only as a tie-break within an already-relevance-filtered group — never as the sole or primary driver
