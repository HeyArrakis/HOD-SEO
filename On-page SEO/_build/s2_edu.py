# -*- coding: utf-8 -*-
"""Education specs: existing articles (11), planned pages (20), conditional pages (14), COM-LG-HUB."""
from s2_core import SCH_ART

# ---- The 12 primary-keyword mismatches (QA/04 §3a): calendar vs Stage 17/19 --------------------------------
# id: (stage19_primary, calendar_primary, calendar_vol, title_if_calendar, title_if_brief)
MISMATCH = {
 "EDU-MET-01": ("is 18k gold or 14k gold better", "14k vs 18k gold", "12,100", "14K vs 18K Gold (and 10K) for Diamond Jewelry", "Is 18K or 14K Gold Better for Diamond Jewelry?"),
 "EDU-4C-00": ("diamond grading scale", "4 cs of diamonds", "6,600", "The 4Cs of Diamonds Explained", "Diamond Grading Scale: The 4Cs Explained"),
 "EDU-SHP-00": ("diamond shape", "diamond shapes", "60,500", "Diamond Shapes: Chart and How to Choose", "Diamond Shape Guide: Chart and How to Choose"),
 "EDU-RJG-02": ("are mens and womens ring sizes the same", "ring size chart", "165,000", "Ring Size Chart: How to Measure Your Size", "Are Men's and Women's Ring Sizes the Same? Ring Size Guide"),
 "EDU-LG-00": ("synthetic diamonds", "what are lab grown diamonds", "12,100", "What Are Lab-Grown Diamonds?", "Synthetic Diamonds: Lab-Grown Diamonds Explained"),
 "EDU-LG-09": ("do lab grown diamonds pass a diamond tester", "how to tell if a diamond is real", "18,100", "How to Tell If a Diamond Is Real", "Do Lab-Grown Diamonds Pass a Diamond Tester?"),
 "EDU-4C-01": ("diamond clarity grading scale", "diamond clarity chart", "33,100", "Diamond Clarity Chart: FL to I3 Explained", "Diamond Clarity Grading Scale Explained"),
 "EDU-4C-03": ("v v s diamond", "vvs diamonds", "18,100", "VVS Diamonds: VVS1 vs VVS2 Explained", "VVS Diamonds: VVS1 vs VVS2 Explained (spacing variant of the same query — title identical either way)"),
 "EDU-4C-05": ("color grade diamond", "diamond color scale", "27,100", "Diamond Color Scale: D-to-Z Chart", "Diamond Color Grade Scale Explained"),
 "EDU-4C-06": ("diamond cut grade", "diamond cut", "60,500", "Diamond Cut: Grades, Cut vs Shape and Sparkle", "Diamond Cut Grade: What Each Grade Means"),
 "EDU-4C-07": ("is 1 carat diamond good", "diamond carat size chart", "4,400", "Diamond Carat Size Chart by Shape", "Is a 1 Carat Diamond Good? Carat Size Guide"),
 "EDU-MET-00": ("types of jewelry metals", "white gold vs platinum", "8,100", "Jewelry Metals Guide: White Gold vs Platinum", "Types of Jewelry Metals Compared"),
}
# 8 ownership-confirmation items (calendar production_status OWNERSHIP_CONFIRMATION)
CONFIRM = {"EDU-RJG-BR", "EDU-RJG-NL", "EDU-INS", "EDU-WB-GUIDE", "EDU-LG-09", "EDU-RJG-01", "EDU-RJG-03", "BLOG-WR-TYPES"}

def S(t):
    return t

# ---- Existing articles (11) ----------------------------------------------------------------------------------
EXIST = {}
def ex(**kw):
    return kw

EXIST["EDU-LG-03"] = ex(
    name="CVD vs HPHT lab-grown diamonds (ranking-equity article)",
    title="CVD vs HPHT Lab-Grown Diamonds: What Buyers Should Know", tact="KEEP — already aligned with 'hpht vs cvd'; 19 ranked keywords (best DataForSEO-estimated position 27) → no title change before a GSC baseline",
    meta="CVD and HPHT are the two main ways lab-grown diamonds are made. Both produce real diamonds. Here is how the methods differ and what to check when you buy.", mact="REPLACE (current meta is the article's first paragraph)",
    h1="CVD vs HPHT Lab-Grown Diamonds: What's the Difference?", hact="KEEP — core keywords present; Step 1 longer H1 not adopted",
    cact="REFRESH IN PLACE (calendar 2027-01-21)",
    sect=("Structure: (1) answer-first block under the H1: 'CVD and HPHT are two ways of growing diamonds; neither makes a 'more real' diamond' + what actually differs; (2) comparison table (growth process, typical use/appearance notes, what the grading report states) built only from sourced statements; "
          "(3) one section per method (HPHT: seed, carbon, heat and pressure; CVD: plasma, carbon-rich gas, layer deposition — Stage 18 CORE); (4) 'Does it matter when buying?' with link to certification (EDU-CERT-00) and buying guide (EDU-LG-10); (5) post-growth treatment/'HPHT-treated' explained; (6) sources + visible 'last updated'. "
          "Add the uncovered questions as sections, not an FAQ block: Are HPHT diamonds worth anything? Are CVD diamonds worth buying? Are CVD/HPHT diamonds real? What does 'HPHT treated' mean? The live article has the heading 'Featured Projects' twice (likely a product module, VERIFY in the rendered page): give module headings descriptive names or make them non-heading elements. Boundary: process OVERVIEW stays on EDU-LG-00 (HIGH cannibalization pair)."),
    sch=SCH_ART, sact="UPDATE (Class B)", aeo="HIGH — AI Overview present on the topic; answer-first block + comparison table are the extractable units.",
    qs="Which is better, CVD or HPHT? | Are CVD diamonds real? | Are HPHT diamonds worth buying? | What does HPHT treated mean?",
    geo="Entity-clear definitions of CVD and HPHT; cite the grading labs' own explanations (GIA/IGI) and show 'last updated'; avoid claims about which method HOD's stones use (BUSINESS FACT, not blocking).",
    trust="Organization byline (OD-11); a named reviewer only if verified; never invent expertise.", img="Diagram of each method with descriptive alt text (what the diagram shows); comparison table as HTML table, not an image.",
    prio="HIGH", aws="B", dep="GSC baseline BEFORE editing (ranking-equity page); URL stays at /blog (OD-13); publishing window (E-01).", dec="OD-11; OD-13; OD-18",
    status="GSC BASELINE REQUIRED", bf="N", gsc="Y", notes="Do not change the URL. EDU-LG-03 ↔ EDU-LG-00 is the HIGH-severity cannibalization pair: EDU-LG-04 (if ever created) must not target CVD/HPHT method queries.")

EXIST["EDU-LG-02"] = ex(
    name="Lab-grown vs natural diamonds (ranking-equity article)",
    title="Lab-Grown vs Natural Diamonds: The Honest Comparison", tact="KEEP — aligned with 'lab grown vs natural diamonds'; ranking-equity URL (3 ranked keywords, best est. pos 29)",
    meta="Lab-grown and natural diamonds are both real diamonds. Compare origin, price, quality and long-term value before you choose.", mact="REPLACE (current meta is the article intro)",
    h1="Lab-Grown vs Natural Diamonds: Which One Is Right for You?", hact="KEEP — core keywords present",
    cact="REFRESH IN PLACE (calendar 2026-11-25, MUST_PUBLISH before the December peak)",
    sect=("(1) Answer-first: they are the same material; what differs is origin, price and resale. (2) Side-by-side table: similarities (same carbon, same hardness, same optical properties) and differences (origin, price, how value is treated, disclosure) — Stage 18 CRITICAL gaps. "
          "(3) Sections for the uncovered PAA: Is it better to buy a real diamond or lab-grown? Are lab-grown diamonds worth it / good / better / popular? (4) Keep price/value depth short and link to EDU-LG-05 (planned) — money-worry overlap with LG-05 is a MEDIUM boundary. "
          "(5) Keep authenticity depth short and link to EDU-LG-01. (6) Sources and 'last updated'. No price figures without a dated source. Do not state that HOD sells natural diamonds (UNCONFIRMED, F-E2)."),
    sch=SCH_ART, sact="UPDATE (Class B)", aeo="HIGH — comparison table + one-sentence answer.", qs="Is it better to buy a real diamond or a lab-grown diamond? | Are lab-grown diamonds worth it? | Are lab-grown diamonds better? | Are lab-grown diamonds popular?",
    geo="Consistent definitions; cite GIA/IGI/FTC-style primary sources where relevant; dated update.", trust="F-E2: do not imply HOD sells natural stones.", img="Comparison table in HTML; diagram alt describes the comparison.",
    prio="HIGH", aws="B", dep="GSC baseline BEFORE editing; URL unchanged (OD-13); must refresh before December (E-01).", dec="OD-13; OD-18; OD-19", status="GSC BASELINE REQUIRED", bf="N", gsc="Y",
    notes="Boundary pairs: EDU-LG-01↔02 (MEDIUM), EDU-LG-02↔05 (MEDIUM).")

EXIST["EDU-MET-01"] = ex(
    name="14K vs 18K gold (ranking-equity article)",
    title="14K vs 18K Gold (and 10K) for Diamond Jewelry", tact="REPLACE — FINAL (OD-03 resolved; US spelling OD-05); apply only after the GSC baseline. Current title is acceptable: ⟦'14K vs 18K Gold for Diamond Jewellery: Which Is Better?'⟧ (verbatim current-site text)",
    meta="14K gold is about 58% pure gold and 18K about 75%. Compare color, durability and value to choose the right gold for diamond jewelry.", mact="REPLACE (current meta is the article intro)",
    h1="14K vs 18K Gold (and 10K) for Diamond Jewelry: Which Is Better?", hact="REPLACE — FINAL (apply with the title, after the baseline). Current H1 ('…Best for Your Engagement Ring?') is narrower than the refresh scope (all diamond jewelry, plus 10K).",
    cact="REFRESH IN PLACE (calendar 2026-11-18)",
    sect=("Add: answer-first (which suits whom), a purity/durability/color/price table (14K vs 18K vs 10K; purity percentages are standard — 58.3% / 75% / 41.7%), 'Is a 10K gold ring worth anything?', 'Is it worth getting 18K over 14K when buying?', 'Is 14K diamond jewelry good?' (Stage 17/18 uncovered: 6 of 16). "
          "Link: metals hub EDU-MET-00 (planned) and ring pages. Keep the URL (it contains ⟦'jewellery'⟧, the current-site spelling; URL spelling is NOT changed). Note: HOD's catalogue is mostly 10K (PDP schema) — the page should still be neutral and generic; do not claim HOD offers 18K (VERIFY)."),
    sch=SCH_ART, sact="UPDATE (Class B)", aeo="HIGH — direct comparison + table.", qs="Is 18K or 14K gold better? | Which karat gold is best? | Is 18K worth more than 14K? | Is a 10K gold ring worth anything? | Is 14K diamond jewelry good?",
    geo="Standard purity facts with a cited source; dated update.", trust="Do not imply availability of metals HOD does not sell.", img="Karat comparison table as HTML; color swatch images need descriptive alt.",
    prio="MEDIUM", aws="B", dep="GSC baseline (3 ranked keywords, best est. pos 81 = DataForSEO estimate); primary resolved (OD-03).", dec="OD-03; OD-05; OD-18", status="GSC BASELINE REQUIRED", bf="N", gsc="Y",
    notes="Stage 13: MOVE_TO_EDUCATION when conditions met — URL unchanged until then.")

EXIST["EDU-LG-10"] = ex(
    name="How to choose a lab-grown diamond (ranking-equity article)",
    title="How to Choose a Lab-Grown Diamond: The Complete Buyer's Guide", tact="KEEP — aligned with 'how to choose a lab grown diamond' (est. pos 35); Step 1 shorter title not adopted",
    meta="How to choose a lab-grown diamond: which of cut, color, clarity and carat matter most, why certification matters and the mistakes to avoid.", mact="REPLACE (current meta is the article intro)",
    h1="How to Choose the Right Lab-Grown Diamond", hact="KEEP — core keywords present",
    cact="UPDATE IN PLACE (no scheduled refresh)",
    sect=("Add the Stage 18 CORE gap '4Cs priorities when choosing a lab-grown diamond' with links to EDU-4C-00 and EDU-CERT-00 (both REQUIRED, missing today). Answer-first: 'start with cut, then pick color and clarity by eye-clean, then carat'. "
          "Boundary: 'should I buy a lab-grown diamond engagement ring' sits here today vs deferred EDU-RJG-04 (INSUFFICIENT_EVIDENCE) — do not expand into ring-buying. Page ≈ 1030 words."),
    sch=SCH_ART, sact="UPDATE (Class B)", aeo="MEDIUM — step list is genuinely list-shaped.", qs="How to choose a lab grown diamond? | Which is clearer, VS1 or VS2? | How much should I pay for a 1 carat lab-grown diamond?",
    geo="Entity clarity on 4Cs and certification.", trust="No price figures without dated source.", img="Descriptive alt for any diagrams.",
    prio="MEDIUM", aws="B", dep="GSC baseline BEFORE editing; publishing window (E-01).", dec="OD-13; OD-18", status="GSC BASELINE REQUIRED", bf="N", gsc="Y", notes="")

EXIST["EDU-LG-01"] = ex(
    name="Are lab-grown diamonds real?",
    title="Are Lab-Grown Diamonds Real? A Complete Buyer's Guide", tact="KEEP — already aligned with 'are lab grown diamonds real' (14,800)",
    meta="Yes. Lab-grown diamonds are real diamonds with the same carbon crystal structure as mined stones. How they differ from simulants and how to verify one.", mact="REPLACE (current meta is generic: 'Everything you need to know…')",
    h1="Are Lab-Grown Diamonds Real? A Complete Buyer's Guide", hact="KEEP",
    cact="REFRESH IN PLACE (calendar 2026-12-02)",
    sect=("Answer-first: 'Yes — same carbon crystal, same chemical/physical/optical properties as mined diamonds' (Stage 18 CORE). Sections: real vs fake vs simulant (moissanite, cubic zirconia) — hand off depth to deferred EDU-GEM pages; how to verify (certificate/report, inscription) — hand off testers to EDU-LG-09; "
          "'Are they considered fake? / actually real / do rich people buy them' as PAA-driven subsections. Boundary: appearance questions → EDU-LG-08; comparison → EDU-LG-02."),
    sch=SCH_ART, sact="UPDATE (Class B)", aeo="HIGH — AI Overview present; one-sentence answer is the extractable unit.", qs="Are lab grown diamonds real? | Are lab grown diamonds fake? | Are lab-grown diamonds considered fake? | Do rich people buy lab diamonds?",
    geo="Cite GIA/IGI/FTC definitions; dated update.", trust="Organization byline (OD-11).", img="Descriptive alt.", prio="HIGH", aws="B", dep="URL unchanged (OD-13); publishing window (E-01).", dec="OD-11; OD-13",
    status="READY FOR IMPLEMENTATION POST-AWS", bf="N", gsc="N", notes="Not in the Stage 15 ranking-equity list, so no GSC dependency; still update in place (URL unchanged).")

EXIST["EDU-4C-00"] = ex(
    name="The 4Cs of diamonds (4Cs pillar)",
    title="The 4Cs of Diamonds Explained", tact="REPLACE — FINAL (OD-03 resolved). Current: 'The 4Cs of Lab-Grown Diamonds Explained: Cut, Colour, Clarity & Carat'",
    meta="The 4Cs — cut, color, clarity and carat — explained, including how lab-grown diamonds are graded and which C matters most for how a diamond looks.", mact="REPLACE (current meta is the article intro; uses 'Colour')",
    h1="The 4Cs of Diamonds Explained: Cut, Color, Clarity and Carat", hact="REPLACE — FINAL (OD-03 resolved). Current H1 'The 4Cs of Lab-Grown Diamonds Explained: How to Choose the…' narrows the topic to lab-grown.",
    cact="REFRESH IN PLACE as the 4Cs pillar (calendar 2026-12-10)",
    sect=("Pillar structure: define the 4Cs; grading scales with one summary table each; which C to prioritize; hand off depth to EDU-4C-01 (clarity), -05 (color), -06 (cut), -07 (carat) — each with a descriptive link; lab-grown grading note (Stage 18 CORE). "
          "Uncovered PAA: Is F VS2/VS1 a good diamond? Are lab-grown diamonds flawless? Do lab-grown diamonds have clarity ratings? Boundary: EDU-4C-00↔4C-01 (MEDIUM): keep lab-grown clarity-chart queries on the pillar, general clarity-scale depth on EDU-4C-01. Spelling: US 'color' vs live 'Colour' (OD-05)."),
    sch=SCH_ART, sact="UPDATE (Class B)", aeo="HIGH — grading tables are extractable.", qs="Is F VS2 a good diamond? | Are lab grown diamonds flawless? | Do lab-grown diamonds have clarity ratings? | What are the 4Cs?",
    geo="Entity-clear scales (cut grade scale, color D–Z, clarity FL–I3, carat) with GIA scale reference.", trust="Organization byline (OD-11).", img="Scale charts as HTML tables; diagrams with descriptive alt.",
    prio="HIGH", aws="B", dep="Primary resolved (OD-03); US spelling (OD-05); URL unchanged (OD-13).", dec="OD-03; OD-05; OD-13", status="READY FOR IMPLEMENTATION POST-AWS", bf="N", gsc="N", notes="Required missing links (Stage 16): EDU-LG-10 → 4Cs; /education → 4Cs.")

EXIST["EDU-SHP-00"] = ex(
    name="Diamond shapes (shapes pillar)",
    title="Diamond Shapes: Chart and How to Choose", tact="REPLACE — FINAL (OD-03 resolved). Current: 'The Best Lab-Grown Diamond Shapes for Engagement Rings'",
    meta="Compare the main diamond shapes — round, oval, pear, emerald, cushion and more — and how shape affects sparkle, apparent size and price in a ring.", mact="REPLACE",
    h1="Diamond Shapes Guide: The 10 Main Shapes and How to Choose One", hact="REPLACE — FINAL (OD-03 resolved). Current H1 'Diamond Shapes Guide: Which Lab-Grown Diamond Shape Is Right…'",
    cact="REFRESH IN PLACE as the shapes pillar (calendar 2026-11-13, MUST_PUBLISH)",
    sect=("Add a shape chart (name, look, sparkle/size notes), 'what shape diamond should I get?' decision section (1 of 5 PAA uncovered), emerald/princess/marquise price & sparkle questions as subsections. Boundary: 'diamond cut' (grade) belongs to EDU-4C-06 — use 'shape' consistently; link to it. Link to engagement-ring style pages and the ring-size guide."),
    sch=SCH_ART, sact="UPDATE (Class B)", aeo="HIGH — shape chart.", qs="What shape diamond should I get? | Does an emerald cut diamond sparkle? | Is an emerald cut diamond more expensive? | Is princess cut good? | Is a marquise more expensive than round?",
    geo="Shape names as entities; consistent with category filters.", trust="Organization byline (OD-11).", img="Shape chart: HTML table + descriptive alt on each shape image.",
    prio="HIGH", aws="B", dep="Primary resolved (OD-03); URL unchanged (OD-13).", dec="OD-03; OD-13", status="READY FOR IMPLEMENTATION POST-AWS", bf="N", gsc="N", notes="Required missing link: /education → EDU-SHP-00; COM-ER → EDU-SHP-00.")

EXIST["EDU-RJG-02"] = ex(
    name="Ring size guide (tool-capable)",
    title="Ring Size Chart: How to Measure Your Size", tact="REPLACE — FINAL (OD-03 resolved). Current: 'How to Find Your Ring Size at Home: Complete Ring Size Guide'",
    meta="Find your ring size at home: measure an existing ring or your finger, use our ring size chart, and learn when to size up or down.", mact="REPLACE",
    h1="Ring Size Guide: Ring Size Chart and How to Measure Your Size at Home", hact="REPLACE — FINAL (OD-03 resolved).",
    cact="REFRESH IN PLACE (calendar 2026-11-12, MUST_PUBLISH; 'ring size chart' 165,000 = largest volume in the project)",
    sect=("Lead with the chart (US sizes ↔ circumference/diameter, HTML table) and a 3-step measure-at-home method; then secret-sizing, resizing ('can you make a ring smaller?', 'where can I get my ring resized?'), width/fit, men's vs women's sizes, titanium cut-off question. "
          "Stage 14: tool embedded by default — specify an interactive sizing aid only if engineering supports it; otherwise printable chart. Link from every ring PDP/category (Stage 16 REQUIRED)."),
    sch=SCH_ART, sact="UPDATE (Class B)", aeo="HIGH — chart + step list; PAA: 4 uncovered.", qs="What is my ring size? | Are men's and women's ring sizes the same? | Where can I get my ring resized? | Can you make a ring smaller? | Can titanium rings be cut off?",
    geo="Units and size systems explicit (US sizing; note UK/EU if shown).", trust="No fit guarantee.", img="Printable chart image needs descriptive alt + an HTML table equivalent.",
    prio="HIGH", aws="B", dep="Primary resolved (OD-03); printable chart + HTML table by default; an interactive sizer is optional (E-02).", dec="OD-03; OD-13", status="READY FOR IMPLEMENTATION POST-AWS", bf="N", gsc="N", notes="Largest-volume page in the plan; every ring category must link here.")

EXIST["EDU-CERT-00"] = ex(
    name="Diamond certification explained (retarget)",
    title="What a Lab-Grown Diamond Certificate Shows", tact="REPLACE — ships TOGETHER with EDU-CERT-01 (Stage 13 RETARGET). Current: 'IGI Certification for Lab-Grown Diamonds: What It Means'. A title that began 'Lab-Grown Diamond Certification Explained' would collide with EDU-CERT-01's live title, hence this wording.",
    meta="What a lab-grown diamond certificate (a GIA or IGI report) shows, why it matters and how to check one before you buy.", mact="REPLACE",
    h1="Lab-Grown Diamond Certification Explained: What an IGI or GIA Report Shows", hact="REPLACE — broadens from IGI-only to the general certification intent (Stage 13 RETARGET)",
    cact="RETARGET + REFRESH IN PLACE (calendar 2026-12-15)",
    sect=("Define certificate vs appraisal; 'do lab-grown diamonds come with certificates?'; which labs certify (GIA, IGI, GCAL, others); what a report contains (4Cs, origin disclosure, growth method, inscription); how to verify a report number. 'Does GIA still grade lab diamonds?' (3 PAA uncovered; GIA entity missing in page text). "
          "Boundary: keep the GIA-vs-IGI comparison to ONE short section and link to EDU-CERT-01 (REQUIRED, missing both ways today). Never state which lab certifies HOD stones (UNCONFIRMED, F-B1)."),
    sch=SCH_ART, sact="UPDATE (Class B)", aeo="HIGH — definition block + 'what a report includes' list.", qs="Are lab grown diamonds certified? | Does GIA certify lab grown diamonds? | Does GIA still grade lab diamonds? | Do lab-grown diamonds get a certificate?",
    geo="Entities: GIA, IGI, grading report; cite the labs' own pages.", trust="F-B1: no claims about HOD's own certification.", img="Sample report anatomy diagram with descriptive alt; use a generic/illustrative sample only if rights are clear.",
    prio="HIGH", aws="B", dep="Must ship with EDU-CERT-01 change (OV-01); publishing window (E-01); F-B1 for any HOD-specific statement.", dec="OD-08; OD-13", status="READY FOR IMPLEMENTATION POST-AWS", bf="N", gsc="N",
    notes="Live cannibalization today (OV-01): both articles target certification. Not a Stage 15 ranking-equity URL.")

EXIST["EDU-CERT-01"] = ex(
    name="GIA vs IGI (comparison)",
    title="GIA vs IGI Lab-Grown Diamond Certification", tact="REPLACE — ships TOGETHER with EDU-CERT-00. Current 'Lab-Grown Diamond Certification Explained: GIA vs IGI' leads with the general phrase that EDU-CERT-00 is being retargeted to; re-lead with the comparison.",
    meta="GIA vs IGI for lab-grown diamonds: what each report shows, how their grading approaches differ and how to verify a report number.", mact="REPLACE",
    h1="GIA vs IGI: What Your Lab-Grown Diamond Report Actually Tells You", hact="KEEP — already comparison-led.",
    cact="UPDATE IN PLACE",
    sect=("Cover uncovered PAA: Is EGL a good diamond certificate? Why is IGI so much cheaper than GIA? Add grading-approach differences and growth-method disclosure (Stage 18 CORE). Link back to EDU-CERT-00 (REQUIRED, missing today). Do not recommend one lab for HOD stones."),
    sch=SCH_ART, sact="UPDATE (Class B)", aeo="HIGH — comparison table.", qs="Which is best, IGI or GIA? | Why is IGI so much cheaper than GIA? | Is EGL a good diamond certificate? | What is the best certificate for lab-grown diamonds?",
    geo="Entities GIA/IGI/EGL; cite lab sources.", trust="F-B1.", img="Comparison as HTML table.", prio="MEDIUM", aws="B", dep="Ships with EDU-CERT-00; lives under /education already.", dec="OD-08",
    status="READY FOR IMPLEMENTATION POST-AWS", bf="N", gsc="N", notes="Only Education-owned article already under /education.")

EXIST["EXIST-BLOG-ER-ONLINE"] = ex(
    name="How to choose a lab-grown engagement ring online (no Stage 15 owner)",
    title="How to Choose a Lab-Grown Diamond Engagement Ring Online", tact="KEEP — no on-page change in this phase (OD-13 adopted)",
    meta="— (no change)", mact="KEEP", h1="How to Choose a Lab-Grown Diamond Engagement Ring Online", hact="KEEP",
    cact="RETAIN AT CURRENT URL — consolidation decision deferred to the GSC baseline",
    sect=("Stage 13 DEFER preserved: the article overlaps the lab-grown buying guide (EDU-LG-10, a ranking-equity URL) and the 4Cs article; its intended destination EDU-RJG-04 stays deferred (INSUFFICIENT_EVIDENCE). "
          "FINAL for this phase: no title/H1/body edits, no merge, no redirect is prepared. Boundary: EDU-LG-10 owns 'how to choose a lab grown diamond' — this article must not be re-targeted at it. Re-evaluate retain/merge with G-01/G-02 after cut-over. Page ≈ 1663 words."),
    sch=SCH_ART, sact="NO CHANGE (template-level fixes apply when the article template changes)", aeo="NONE planned.", qs="Which route to buy a lab-grown engagement ring online? (deferred)", geo="—", trust="—", img="—", prio="LOW", aws="C",
    dep="Verify after AWS: URL 200, listed on /blog (Stage 16 REQUIRED listing). Any consolidation needs GSC data.", dec="OD-13; OD-18", status="NO CHANGE REQUIRED", bf="N", gsc="N",
    notes="Retained deliberately; protects LG-10 by documenting the boundary rather than editing.")

# ---- Planned Education pages (20) ---------------------------------------------------------------------------
# id: (title, meta, h1, prio, extra note)
PLANNED = {
 "EDU-LG-00": ("What Are Lab-Grown Diamonds?",
   "Lab-grown diamonds are real diamonds made in a laboratory rather than mined. What they are, other names for them, how they are made and how they compare.",
   "What Are Lab-Grown Diamonds? Definition, Other Names and How They Are Made", "CRITICAL",
   "MUST_PUBLISH 2026-10-21 (11 days from 2026-10-10); primary resolved (OD-03); the commercial hand-off links to /engagement-rings per OD-02. Pillar must NOT target commercial head terms ('lab grown diamonds' 135,000). HIGH cannibalization pair with EDU-LG-03: give process an overview only (interim home, S03)."),
 "EDU-LG-05": ("Do Lab-Grown Diamonds Hold Their Value?",
   "Do lab-grown diamonds hold their value? How lab-grown diamond prices work, what to expect on resale and how they compare with natural diamonds.",
   "Do Lab-Grown Diamonds Hold Their Value? Price, Resale and What to Expect", "MEDIUM",
   "No financial advice; dated sources for any price statement. Boundary with EDU-LG-02 (MEDIUM)."),
 "EDU-LG-07": ("Are Lab-Grown Diamonds Ethical?",
   "Are lab-grown diamonds ethical? The environmental and sourcing questions, what is and is not known, and what to ask a seller.",
   "Are Lab-Grown Diamonds Ethical? The Environmental and Sourcing Case, and Its Limits", "LOW",
   "Cite primary sources; make no claim about HOD's own sourcing (BUSINESS FACT; non-blocking)."),
 "EDU-LG-08": ("Do Lab-Grown Diamonds Get Cloudy?",
   "Do lab-grown diamonds get cloudy? What causes a hazy look, how clarity and fluorescence affect appearance, and how durable lab-grown diamonds are.",
   "Do Lab-Grown Diamonds Get Cloudy? Appearance, Fluorescence and Durability Over Time", "LOW",
   "Appearance only; authenticity questions stay with EDU-LG-01 (MEDIUM boundary)."),
 "EDU-LG-09": ("How to Tell If a Diamond Is Real",
   "How to tell if a diamond is real: simple at-home checks, what a jeweler's tester can and cannot show, and why lab-grown diamonds pass a diamond tester.",
   "How to Tell If a Diamond Is Real: At-Home Tests, Jeweler Tests and Why Lab-Grown Diamonds Pass a Tester", "HIGH",
   "Primary resolved (OD-03) and owner confirmed (OD-04): 'how to tell if a diamond is real' (18,100) is NEW (not in Stage 15), placed in EDU-LG-09 as the closest owner. The lab-grown-passes-tester wording must be sourced."),
 "EDU-NAT-00": ("How Are Diamonds Formed?",
   "How are diamonds formed? Natural diamond formation deep in the earth, how diamonds reach the surface, and how this differs from growing a diamond in a lab.",
   "How Are Diamonds Formed? Natural Formation, Mining and How It Differs From Lab Growing", "MEDIUM",
   "F-E2: HOD's natural-diamond offer is UNCONFIRMED — keep the page educational; no product claims."),
 "EDU-4C-01": ("Diamond Clarity Chart: FL to I3 Explained",
   "A diamond clarity chart from Flawless to I3: what each grade means, which grades look clean to the eye and which clarity to buy.",
   "Diamond Clarity Chart: Every Grade From FL to I3, Eye-Clean Grades and Which Clarity to Buy", "HIGH",
   "Boundary with EDU-4C-00 (MEDIUM): general scale here; lab-grown clarity-chart queries stay on the pillar."),
 "EDU-4C-02": ("SI Clarity Diamonds: SI1 vs SI2 Explained",
   "SI1 vs SI2 diamonds: what SI clarity means, when an SI diamond is eye-clean and when to avoid it.",
   "SI Clarity Diamonds: SI1 vs SI2, When an SI Diamond Is Eye-Clean and When to Avoid It", "LOW",
   "Owner confirmed in architecture; no keyword mismatch."),
 "EDU-4C-03": ("VVS Diamonds: VVS1 vs VVS2 Explained",
   "What VVS1 and VVS2 mean, how VVS compares with VS and flawless, and whether a VVS diamond is worth the price.",
   "VVS Diamonds: What VVS1 and VVS2 Mean, How They Compare With VS and Flawless, and Whether VVS Is Worth It", "HIGH",
   "'v v s diamond' vs 'vvs diamonds' is a spacing variant of one query; the SERP mixes informational and commercial (C2)."),
 "EDU-4C-05": ("Diamond Color Scale: D-to-Z Chart",
   "The diamond color scale from D to Z: what each grade looks like, how color affects value and which color to buy.",
   "Diamond Color Scale: D-to-Z Color Chart, What Each Grade Looks Like and Which Color to Buy", "HIGH", ""),
 "EDU-4C-06": ("Diamond Cut: Grades, Cut vs Shape and Sparkle",
   "Diamond cut explained: what cut grade means, how cut differs from shape and how cut drives a diamond's brilliance.",
   "Diamond Cut: What Cut Grade Means, Cut vs Shape, and How Cut Drives Sparkle", "HIGH",
   "'Cut' is ambiguous (grade vs shape): cut-grade queries here, shape queries on EDU-SHP-00 (MEDIUM pair)."),
 "EDU-4C-07": ("Diamond Carat Size Chart by Shape",
   "A diamond carat size chart: carat to millimeters by shape, how big each carat looks and what size diamond studs to choose.",
   "Diamond Carat Size Chart: Carat to Millimeters by Shape and What Size to Choose", "MEDIUM",
   "Informational stud-earring queries land here (QA/04 R7)."),
 "EDU-MET-00": ("Jewelry Metals Guide: White Gold vs Platinum",
   "Compare white gold, platinum, and yellow, white and rose gold for diamond jewelry: durability, color, care and cost.",
   "Jewelry Metals Guide: White Gold vs Platinum, Yellow vs White vs Rose Gold, and the Best Metal for Rings", "MEDIUM",
   "Do not state that HOD offers platinum (UNCONFIRMED). Catalogue is mostly 10K gold (PDP schema)."),
 "EDU-RJG-01": ("Engagement Ring Settings Guide",
   "Engagement ring settings explained: prong, bezel, halo, pavé, solitaire and more, and how to choose the right setting.",
   "Engagement Ring Settings Guide: Prong, Bezel, Halo, Pavé, Solitaire and More — and How to Choose", "MEDIUM",
   "OWNERSHIP REVIEW CARRIED from Stage 19: 'engagement ring settings' is commercial-led (S18.5 CONFLICT); the page targets 'types of diamond settings' (720) only. Style heads stay with the commercial style subcategories."),
 "EDU-GEN-01": ("What Are Diamonds Made Of?",
   "What are diamonds made of? Carbon, how its structure gives a diamond its hardness, and how durable a diamond really is.",
   "What Are Diamonds Made Of? Carbon, Hardness and How Durable a Diamond Really Is", "MEDIUM", ""),
 "EDU-RJG-03": ("How to Clean a Diamond Ring at Home",
   "How to clean a diamond ring and diamond earrings at home: safe steps, what to avoid and everyday-wear care.",
   "How to Clean a Diamond Ring (and Diamond Earrings): Safe At-Home Steps, What to Avoid and Everyday-Wear Care", "MEDIUM",
   "EDU-RJG-03 activated (OD-04 adopted). HOD cleaning/appraisal SERVICES are UNCONFIRMED — mention none."),
 "EDU-RJG-BR": ("Bracelet Size Chart: How to Measure Your Wrist",
   "A bracelet size chart: how to measure your wrist, how much room to add and how to choose the right fit, including tennis bracelets.",
   "Bracelet Size Chart: How to Measure Your Wrist and Choose the Right Fit (Including Tennis Bracelets)", "MEDIUM",
   "NEW page — owner ratified 2026-10-10 (OD-04). Boundary with BC-021 (tennis bracelet meaning/wear): this page owns sizing only."),
 "EDU-RJG-NL": ("Necklace Length Chart: Find Your Length",
   "A necklace length chart: what each length looks like, how to measure and which length suits a pendant.",
   "Necklace Length Chart: What Each Length Looks Like, How to Measure and Which Length Suits a Pendant", "HIGH",
   "NEW page — owner ratified 2026-10-10 (OD-04). Boundary with BC-006: layering = styling, this = sizing reference."),
 "EDU-INS": ("Engagement Ring Insurance: Is It Worth It?",
   "Engagement ring insurance: whether it is worth it, what it typically costs and covers, and how to insure a ring.",
   "Engagement Ring Insurance: Is It Worth It, What It Costs, What It Covers and How to Insure a Ring", "MEDIUM",
   "NEW page — owner ratified 2026-10-10 (OD-04). No personalized financial advice; dated sources. HOD's own insurance/appraisal services are UNCONFIRMED."),
 "EDU-WB-GUIDE": ("How to Choose a Wedding Band",
   "How to choose a wedding band: metal, width and fit, and how to pair it with your engagement ring in an oval, solitaire or halo style.",
   "How to Choose a Wedding Band: Metal, Width, Fit and Pairing It With Your Engagement Ring", "LOW",
   "NEW page — owner ratified 2026-10-10 (OD-04). Boundaries: BC-007 (wearing order), BC-022 (stacks), EDU-WB-TYPES (style catalogue); this page owns the buying decision."),
}

# ---- Conditional / deferred pages (14): documented, NOT planned ----------------------------------------------
COND_IDS = ["EDU-RJG-00", "EDU-LG-04", "EDU-LG-06", "EDU-NAT-01", "EDU-NAT-02", "EDU-4C-04", "EDU-4C-08", "EDU-CERT-02", "EDU-MET-02", "EDU-GEM-00", "EDU-GEM-01", "EDU-GEM-02", "EDU-GEN-02"]
COND_NOTE = ("CONDITIONAL / DEFERRED — not planned, no URL, no on-page spec until Stage 14 activation conditions are met. When activated: run the Stage 19 brief process, "
             "ratify ownership at activation and add the Stage 16 conditional link rows. Until then keep out of the sitemap/nav; do not write titles or metas.")

LG_HUB = dict(
    name="Commercial Lab-Grown Diamonds hub (not built)",
    title="— (no page)", tact="N/A — OD-02: no separate hub now", meta="—", mact="N/A", h1="—", hact="N/A",
    cact="DO NOT BUILD NOW — reversible; reverses only if HOD sells loose lab-grown diamonds (F-E2)",
    sect=("OD-02 FINAL: no separate commercial Lab-Grown hub now. Reasoning: (1) the catalog is finished jewelry — every product is lab-grown (F-E1 to confirm), so a 'lab-grown diamonds' page would duplicate /shop and fail D-07 distinctness/one-home; "
          "(2) the SERP for 'lab grown diamonds' (135,000; Stage 8 NAVIGATIONAL) and 'lab diamonds' (27,100; TRANSACTIONAL) is retailer collection/loose-stone pages HOD cannot match without loose stones; "
          "(3) EDU-LG-00 stays informational and must not take the head terms. Origin-qualified ring heads ('lab grown diamond engagement rings' 90,500; 'lab grown diamond rings' 90,500) become secondary targets of /engagement-rings once F-E1 is confirmed — no separate URL (D-05). "
          "PREFERRED OPTION if HOD confirms loose lab-grown stones are (or will be) sold: build the hub (own the head terms; keep EDU-LG-00 educational; Stage 16 hub links activate). No natural-diamond or loose-stone offering is assumed."),
    sch="If ever built: CollectionPage/ItemList + BreadcrumbList; no FAQPage.", sact="N/A", aeo="N/A", qs="—", geo="Head terms remain unowned by design; origin stated at product level and, after F-E1, in the engagement-ring intro.",
    trust="Needs F-E1 and F-E2.", img="N/A", prio="HIGH", aws="A",
    dep="Narrow HOD facts only: F-E1 (all stones lab-grown?) and F-E2 (loose/natural stones sold or planned?). No paid keyword/SERP check is needed — existing evidence is sufficient.",
    dec="OD-02; OD-19", status="CONDITIONAL — PRODUCT/OFFER CONFIRMATION", bf="Y", gsc="N", deps=dict(hod="F-E1, F-E2", eng="E-01"),
    notes="Impacts home, /engagement-rings and EDU-LG-00 only through the F-E1/F-E2 answers; current titles are origin-neutral so nothing is blocked.")
