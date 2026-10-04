# Blog Content Calendar Stage: decision log

Date: 2026-09-29. Each decision records what was decided, the evidence, and whether it needs user review. "Stage N" refers to the project's completed research stages. No Stage 1–19 file was edited, and no Stage 15 owner was changed.

## A. Method and scope

**D-BC-01: The calendar follows the Stage 13 definition of the Blog.** The Blog is HOD's editorial layer (gifts and occasions, style and trends, craft, launches, stories, dated industry notes). Education is the single evergreen home for diamond concepts and permanent buying guides. The brief asked for "evergreen SEO" topics, but it also said "do not create a separate blog if the topic should actually be an Education page". The two are reconciled like this:
- Evergreen blog topics are limited to jewellery **culture, meaning, styling, occasions and craft**. These have no Stage 14 hub and are assigned to the Blog in the Stage 13 framework.
- Diamond/material concepts are never scheduled.

*Review:* 6 posts carry `promote_to_education_flag = CANDIDATE`: BC-006, 007, 011, 021 and 025 (style/occasion) and BC-019 (buying timing). If Stage 14 later adds a "jewellery types & styling", "ring traditions" or engagement-ring buying hub, their substance moves there (Stage 13 section 6 "Promote").

**D-BC-02: One paid call, a curated measurement list, not open discovery.** The Stage 7 master (1,936 keywords) contains essentially no gift, holiday, proposal, trend or styling terms. A text search found none usable, and the Stage 13 open question 5 had already flagged seasonal demand as unmeasured. So new research was required.
- **Chosen:** `keyword_overview/live` on 292 hypothesis keywords, because it returns 12-month `monthly_searches` (needed for peak timing), SERP feature types, KD and intent, and bills only for keywords that exist.
- **Rejected:** a `keyword_ideas` discovery pull. In Stage 6, a combined relevance-ranked pull skewed toward the dominant seed cluster.
- **Cost:** $0.04404 actual against a $0.04704 approved maximum.

**D-BC-03: Existing monthly data reused for free.** The Stage 4/6 raw JSON already holds monthly searches for 1,913 existing keywords. December indices were computed per Stage 15 owner at no cost. This produced the finding that the Education owners peak in December (summary section 10).

**D-BC-04: Search volume never decided a topic by itself.** Examples:
- `october birthstone` (246,000) and `tennis bracelet` (135,000) were not scheduled: one is not an HOD fit, the other is a reserved commercial head.
- `how long does a custom engagement ring take` (210) was scheduled P1 for timing and bespoke value.

**D-BC-05: No composite score.** Priority has four labels (P1 time-critical to P4 low), each with a written reason covering demand, SERP/intent, HOD fit, commercial link, timing and risk.

## B. Topic selection and rejection

**D-BC-06: Proposal content is in scope; wedding planning is not.** Stage 13 excluded "wedding-planning content beyond jewellery".
- A proposal is the moment the engagement ring is used, and demand is measured (`proposal ideas` 14,800; Christmas/NYE/Valentine's proposal spikes of 5–7×). So proposal posts are scheduled.
- Each must centre the ring: ring timing, sizing (via EDU-RJG-02) and style.
- Venues, photographers and wedding logistics stay out.

*Review:* confirm this scope.

**D-BC-07: Black Friday "deals" rejected for the Blog; the informational timing question selected (BC-019).**
- All 14 measured deal terms with SERP data show product features. Black Friday terms spike 9–11× in November and Cyber Monday terms 5–8× in early December.
- A blog cannot credibly rank for "deals", and publishing one without a real HOD offer would mislead.
- BC-019 targets `best time to buy an engagement ring` (AI Overview/forum SERP, KD 0) and is published four weeks before Black Friday.

**D-BC-08: The Christmas gift series is split by recipient, not by product.** Recipient intents (wife, girlfriend, mom) are distinct searches with distinct needs. Product splits (e.g. "christmas earrings gifts") would compete with category pages. BC-004 is the generic hub. BC-013 (luxury) is MEDIUM priority because `best jewelry gifts for her` may share a SERP with BC-004 (see D-BC-21).

**D-BC-09: Winter proposal ideas merged into Christmas proposal ideas (BC-017); NYE and Valentine's proposals kept separate.**
- Winter and Christmas proposal searches peak in the same weeks and likely share results, so a merge avoids two near-identical posts.
- NYE (Dec-only spike, different date) and Valentine's (Feb) are different events.

*Review:* split winter out only if SERP validation shows distinct results.

**D-BC-10: Thanksgiving handled as the start of engagement season (BC-016), not as a gift occasion.** Thanksgiving gift terms are hostess/novelty intent. Thanksgiving proposal terms total 70/month, too thin for a post of their own, so they are secondaries of BC-016.

**D-BC-11: Halloween, fall and October birthstone excluded.** They are costume/novelty intent, the fall peak had already passed (September), and HOD sells no gemstones (Stage 12 D-16). Measured to confirm rather than assumed.

**D-BC-12: Sweetest Day not scheduled.** 27,100 searches, but the day is Oct 17 (under 3 weeks from the calendar start), the SERP is product-led, and it is a regional holiday. Backlogged for 2027.

**D-BC-13: Diwali used as a timing hook for a Surat brand/industry post (BC-015), not a gift guide.**
- Diwali 2026 is Nov 8, about 2.5 weeks later than 2025 because of the Adhik Maas.
- Generic Diwali gift searches are product-led, and targeting the Indian-American gifting audience is a business decision.
- BC-015 targets `where are lab grown diamonds made` plus `surat diamonds`, an angle only HOD can tell.

**D-BC-14: The largest unowned opportunities go to Education, not the Blog.** Necklace length chart (9,900), bracelet size (2,380), engagement ring insurance (8,100) and engagement ring budget advice (23,100 combined) all fail the Stage 13 shelf-life/question tests. They are logged as `EDUCATION_GAP` / `EDUCATION_OWNER_DEFERRED`.

*Review:* these need a Stage 14/15 ownership decision. They are the strongest non-blog finding of this stage.

**D-BC-15: Blog-to-blog links are limited to two series.** The gift hub links to its spokes, and the proposal hub to its seasonal spokes. They are recorded in `related_articles`. Stage 16 allows Blog→Blog "only where a story continues".

*Review:* add these as Stage 16 `BLOG_TO_RELATED_BLOG` rows in a future maintenance pass. Stage 16 was not modified.

**D-BC-16: Proposal posts satisfy the Gifts template's REQUIRED category links.** Stage 16 makes BLOG-GIFTS posts link to the earrings, necklaces and bracelets categories. Proposal posts (BC-014/017/029/034) comply through the template's standard shop-gifts module. QC check 14 enforces this.

**D-BC-17: Average engagement ring cost (BC-024) is a dated Industry Note; budget advice is not targeted.**
- Stage 13 puts dated market figures in the Blog.
- The survey-statistic intent (`average engagement ring cost` 8,100) is separable from advice intent (`engagement ring budget`, `how much to spend`), which belongs to the deferred EDU-RJG-04.

*Review:* MEDIUM cannibalization risk once EDU-RJG-04 exists. The two must link to each other and must not share headings.

**D-BC-18: Craft posts are bounded against three Education owners.** QC check 4 found real word overlaps, now documented as boundaries:
- BC-005 (cutting *process*) vs EDU-GEN-01 hardness questions ("can you cut diamonds").
- BC-010 (making *jewellery*) vs EDU-NAT-00 formation ("how are diamonds made").
- BC-015 (*where*, geography) vs EDU-LG-00 process, EDU-NAT-00 formation and EDU-GEN-01 composition.
- EDU-NAT-00 S06 keeps its short "mining, cutting and polishing" summary and may optionally link to BC-005 as first-hand evidence (Stage 16 optional Education→Blog).

**D-BC-19: Style heads reserved for commercial pages.** `toi et moi ring` (27,100), `bezel engagement ring` (22,200), `huggie earrings` (22,200), `eternity ring` (12,100) and similar product-led heads are not targeted. They are evidence for the Stage 12 D-07 subcategory gate. The Blog takes the "what is / meaning / how to wear" neighbour, or covers the style as a trend section (BC-031).

**D-BC-20: Launch and Stories categories left empty.** There are no confirmed launches (Hip Hop is a placeholder; T-bar's form is undecided) and no consented client commissions. Inventing them would break Stage 13 section 8.

## C. Timing

**D-BC-21: Lead-time rule.**
- Publish at least 4 weeks before searches start rising.
- Christmas gift guides at least 45 days before Dec 25; other Christmas content at least 28 days.
- Black Friday at least 21 days before.
- Valentine's at least 6 weeks before Feb 14 and before the January surge.

This is a planning assumption (crawl, index and internal links), not a ranking promise. QC checks 9–11 and 23 enforce it.

**D-BC-22: Christmas gift content is published in October, weeks ahead.** Gift searches start rising in November (index ~3×) and peak in December (~7–9×).
- The hub (BC-004) goes out on Oct 5.
- Recipient spokes follow on Oct 12–20.
- The last-minute guide (BC-028), whose searches spike 11.5× in December with almost nothing in November, still publishes on Nov 16 so it is indexed before mid-December.

**D-BC-23: Valentine's content starts in December; two posts only.** Measured demand rises about 8× from December to January (`valentines day jewelry` 1,600 → 12,100 → 14,800 in Feb). So BC-033 (Dec 15) and BC-034 (Dec 22) are published early. More Valentine's posts were not justified (Galentine's is not HOD; one gift URL covers the need).

**D-BC-24: 20 slots left unused.** Four per week is a ceiling. After ~Dec 1, new Christmas content is too late and no other topic met the bar. The capacity is better spent on refreshing the gift series (shipping cut-offs), producing the December-peaking Education owners, and gathering the business facts listed per blog.

## D. Open items for review

1. Scope of proposal content (D-BC-06).
2. Ownership decision for the Education gaps: necklace/bracelet sizing, insurance, budget (D-BC-14).
3. Optional SERP validation call (20 tasks, max ~$0.012; list in summary section 14). It would settle D-BC-08 (BC-013 overlap), D-BC-09 (winter merge), BC-027 and BC-030 (mixed intent) before briefs are written.
4. Business facts: holiday shipping cut-offs (BLOCKING for BC-028), bespoke production time (BC-001), HOD cutting/manufacturing claims (BC-005/010/015), whether HOD runs a Black Friday offer (BC-019), and resizing of full eternity bands (BC-023).
5. Stage 16 maintenance: blog series links (D-BC-15).

---

# HARD REVISION (2026-09-29 to 2026-10-03): decisions R-01 to R-16

The 34-blog calendar was re-audited against new discovery research (Round 1), live Google results pages with AI Overview and People Also Ask (Round 2), and measured question phrases (Round 3). Every paid call was approved individually by the user. The user approved the Round 2 recommendations on 2026-09-29 with the decisions recorded in R-03, R-04 and R-05. Full evidence: `revision/round2_decision_table.csv`. Mapping of all original IDs: `blog_calendar_revision_log.csv`.

**Superseded original decisions:**
- **D-BC-08:** recipient gift series → mom and luxury removed (R-07).
- **D-BC-14:** budget advice as an Education gap → now Blog-owned (R-04).
- **D-BC-17:** BC-024 statistic-only split → superseded by R-04.
- **D-BC-23:** two Valentine's posts → one (R-08).

All other D-BC decisions stand.

**R-01 Volume is never the deciding factor alone.** A topic needs measured demand, a results page where an article can compete (verified in Round 2), HOD fit and a clean owner. High-volume shopping searches (ring stacking 40,500; promise rings 301,000; tennis bracelet 135,000; eternity ring 12,100) stay with commercial pages. The blog targets the informational neighbour.

**R-02 One intent = one article, measured by results-page overlap.**
- 3+ shared top-10 results means merge: necklace layering phrasings share 4; ring-finger-meaning phrasings share 3.
- Fewer than 2 means separate articles: wedding-ring finger vs promise-ring finger; promise ring vs promise-ring finger; anniversary by year vs 10th anniversary; how-to-wear vs which-finger.
- Identical DataForSEO monthly series (demand groups) are treated as one keyword, so volume is not double-counted.

**R-03 NEW-06 not scheduled (user decision).** "does the man wear an engagement ring" (8,100) matches Stage 15 CL-122, which is deferred to EDU-RJG-04. Ownership is unchanged; the evidence is recorded in the backlog for EDU-RJG-04.

**R-04 BC-024 owns cost and budget in one Blog article (user decision).** The AI Overview text is identical across "how much should an engagement ring cost" and "how much to spend", and the PAA questions overlap with "average engagement ring cost". A separate budget article would cannibalise BC-024. None of these keywords is in Stage 15. EDU-RJG-04 is unchanged; if it is built, it links to BC-024 for budget.

**R-05 Five new articles (user-approved).**
- BC-035: 10 year anniversary gift (33,100)
- BC-036: what finger does a wedding ring go on (27,100)
- BC-037: engagement ring vs wedding ring (18,100)
- BC-038: ring finger meaning (9,900)
- BC-039: what finger does a promise ring go on (12,100)

They form a "ring traditions" group, with no Stage 14 hub; each is flagged as a promote-to-Education candidate if Stage 14 adds one.

**R-06 Six primary upgrades.** BC-003 → push present (18,100); BC-006 → necklace layering (14,800); BC-018 → anniversary gifts by year (74,000); BC-024 → combined cost article; BC-025 → different types of earrings (1,600 + earring backs 3,600); BC-034 → valentines day proposal (720).

**R-07 Eight removals.** BC-012, 013, 020, 026, 027, 028, 030 and 033: product-led, brand-led or generic non-jewellery results pages, or demand too small. Useful demand is folded into BC-004, BC-031 and BC-038 as sections. The Valentine's jewellery and gifts-for-mom intents are flagged as commercial collection-page opportunities.

**R-08 Valentine's: one post.** BC-033 (Valentine's jewellery) was removed after its results page showed 10 of 10 product/category pages. BC-034 (proposals) is the single Valentine's post, moved to Dec 8, about 4 weeks before the January surge.

**R-09 Three merges.**
- BC-002 → BC-015: one dated industry note covering geography, Surat and the market.
- BC-010 → BC-001: its results page was incoherent; the making stages fit the custom timeline.
- BC-029 → BC-017: NYE alone is 90/month.

**R-10 "christmas proposal" dropped from BC-017.** Its results page is the Hallmark / Prime Video movie.

**R-11 Low-volume primaries kept only with a written reason** (`low_volume_justification`):
- BC-001: bespoke assist plus the confirmed timeline fact.
- BC-015: Surat angle, Stage 13 industry role, Diwali.
- BC-016: anchors engagement season before Thanksgiving.
- BC-019: the only winnable Black Friday angle.

**R-12 BC-008 and BC-009 kept at P3 with a commercial-lean flag.** Retailer gift categories dominate, but editorial lists (The Knot, Byrdie) rank and demand peaks in December. Revisit once a gifts collection exists.

**R-13 Confirmed bespoke timeline used with hedged wording.** Typically 2–3 weeks to make plus ~6–9 days delivery (generally ~3–4 weeks, stone-dependent). It is never stated as a guarantee. Used in BC-001, BC-017 and BC-034.

**R-14 PAA and AI Overview built into each article plan.** Every scheduled blog lists its PAA questions with a placement (answer block, H2/H3, FAQ, table, list, steps, or link to owner) and an answer format based on the AI Overview structure. Questions owned elsewhere are linked, not answered (budget → BC-024; hardness → EDU-GEN-01; lab-grown price → EDU-LG-05). The "2:1:1" and "3 month" rules (70 and ~10/month) are FAQ one-liners only.

**R-15 Boundary fixes found by the new QC.**
- BC-015 secondary "when did lab grown diamonds become popular" removed: near-match to an EDU-LG-02 keyword.
- BC-001 ring-making vs EDU-NAT-00 formation documented as a boundary.
- 10 Round 1 keywords that already exist in the Stage 7 master are labelled EXISTING_DATA (re-measured), not new research.

**R-16 Revision cost.** Round 1 $0.54108 + Round 2 $0.0972 (billed) + Round 3 $0.02388 = **$0.66216** of the $4 cap. The balance implies $0.00084 more for Round 2 (unexplained; recorded in the cost log). S2, S3, S4 and S10 were not run, at the user's instruction.
