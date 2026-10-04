# House of Diams — Stage 5: Seed Matrix

Date: 2026-09-17

Shows whether the strategic seed universe (`05_hod_strategic_seed_universe.csv`, 55 keywords) has at least one representative seed, by role, for each of the areas CLAUDE.md's Stage 5 brief asks to check coverage against. Cells are populated **only** with actual selected seeds — nothing was invented to fill a gap. `MISSING` means no seed of that role exists for that area in this seed universe.

Roles not shown as their own column (`LONG_TAIL`, `ENTITY`) are listed as "Extra seeds" under the relevant area when present, since the required matrix header only has 7 role columns.

| Area | Head | Category | Product | Attribute | Education | Comparison | Question |
|---|---|---|---|---|---|---|---|
| Engagement Rings | MISSING | MISSING | MISSING | mixed metal ring | MISSING | MISSING | MISSING |
| Wedding Bands | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING |
| Earrings | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING | is 1 3 carat diamond earrings too small |
| Necklaces & Pendants | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING |
| Bracelets | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING |
| Fine Jewellery | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING |
| Bespoke / Custom Jewellery | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING |
| Lab-Grown Diamonds | lab grown diamonds | MISSING | MISSING | MISSING | MISSING | moissanite hardness vs diamond | how are diamonds made |
| Natural Diamonds | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING | are all diamonds blood diamonds |
| Diamond Shapes / Cuts | MISSING | MISSING | MISSING | asscher cut diamond | MISSING | moval vs oval diamond | is kite a diamond shape |
| 4Cs / Quality | MISSING | MISSING | MISSING | MISSING | v v s diamond | si vs vs diamond | what is the best cut diamond for sparkle |
| Certification | MISSING | MISSING | MISSING | MISSING | egl diamond report lookup | gia vs ags diamond | is egl a good diamond certificate |
| Diamond Buying / Education (general) | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING | does lab-grown diamonds pass diamond tester |
| Gemstones (adjacent) | MISSING | MISSING | MISSING | morganite rings | MISSING | morganite vs diamond hardness | MISSING |
| Jewellery Materials / Metals | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING | is a sterling silver ring worth anything |

### Extra seeds (LONG_TAIL / ENTITY roles, not shown in the matrix above)

- **Lab-Grown Diamonds**: `hpht lab grown diamonds`, `diamond growing lab`, `history of lab grown diamonds`, `cvd lab grown diamonds`
- **Natural Diamonds**: `blood diamond industry`
- **4Cs / Quality**: `diamond clarity grading scale`, `ct diamond`, `diamond grading and clarity`
- **Competitor / Brand** (not part of the strategic seed pool — REVIEW-queued only, kept separate per instruction): `ritani lab grown diamonds`, `diavik diamonds`, `rahaminov diamonds`, `does kay jewelers buy back rings`, `is tiffany jewelry worth it`

## Reading this matrix

- **Zero coverage in five of nine product/category areas** (Wedding Bands, Necklaces & Pendants, Bracelets, Fine Jewellery, Bespoke) — a direct consequence of the underlying Stage 4 `keywords_for_site` discovery pull containing almost no explicit product-category vocabulary (confirmed in both the Stage 4 and this stage's summaries). Not evidence of low demand for those categories.
- **No HEAD or CATEGORY seed exists for Engagement Rings** despite it being HOD's largest current product line (per Stage 1 inventory) — because the literal phrase "engagement ring" does not appear anywhere in this 1,000-keyword sample.
- **Lab-Grown Diamonds, Diamond Quality/4Cs, Diamond Shapes, and Certification are reasonably well covered** across QUESTION/COMPARISON/EDUCATION/ATTRIBUTE roles — these mirror both HOD's existing organic footprint (Stage 3) and this discovery pull's topical skew (Stage 4).
- This matrix is a coverage diagnostic for Stage 6, not a final architecture input. Stage 6's keyword expansion should be seeded partly from HOD's actual product/category taxonomy directly (not solely from this `keywords_for_site` sample) specifically to fill the MISSING cells above with real search data rather than invented terms.
