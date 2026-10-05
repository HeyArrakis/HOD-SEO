#!/usr/bin/env python3
"""Stage 14 — Education strategy & architecture: build the Stage 14 CSV outputs.

Local project files only. No DataForSEO or other API call. No live-site change.
Every row below is a written decision; this script only lays the decisions out
as CSVs and fills evidence columns from Stage 11 files so they cannot drift.

Outputs:
  architecture/14_education_architecture.csv
  architecture/14_education_hierarchy.csv
  architecture/14_education_cluster_consolidation.csv
  architecture/14_education_page_type_framework.csv
  content-strategy/14_education_existing_content_mapping.csv
  architecture/scripts/14_upstream_checksums.json   (used by qc_14.py)

Run: python3 architecture/scripts/build_14_csvs.py
"""
import csv, hashlib, json, os, glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
P = lambda *a: os.path.join(ROOT, *a)

REG = {r["cluster_id"]: r for r in csv.DictReader(open(P("clusters/11_cluster_registry.csv")))}

# --------------------------------------------------------------------------
# 1. Hubs (candidate hubs and their Stage 14 decision)
# --------------------------------------------------------------------------
HUBS = [
    # hub_id, name, decision, pillar_topic, why_exists, searcher_need, owns, does_not_own, evidence_level, status
    ("H-LG", "Lab-Grown Diamonds", "KEEP", "EDU-LG-00",
     "Largest informational area: 25 Stage 11 clusters, 20 routed to Education topics; holds 22 of HOD's 28 Stage 3 rankings (CVD vs HPHT and lab-vs-natural articles).",
     "Understand what lab-grown diamonds are, whether they are real, how they are made and how they compare, before buying one.",
     "Definition and terminology; authenticity; lab-vs-natural comparison; CVD/HPHT growth methods; price, value and resale; worth-it evaluation; ethics; appearance and durability; detection and testers; choosing a lab-grown stone.",
     "Commercial head terms such as 'lab grown diamonds' and 'lab diamonds' (retailer/brand SERPs: commercial Lab-Grown hub, Stage 12 D-05); carat and loose-stone shopping (CL-006); wholesale (CL-007); location queries (CL-005); dated market news and history (Blog); certification (Certification hub owns it); the 4Cs grading scale (Diamond Quality hub owns it).",
     "HIGH", "PROPOSED"),
    ("H-NAT", "Natural Diamonds", "KEEP", "EDU-NAT-00",
     "Informational demand exists for formation, mining, rarity and conflict-free sourcing (CL-073 to CL-076, CL-085). Lab-vs-natural decisions need a balanced natural-diamond reference. Education only; the commercial natural hub stays deferred (Stage 12 D-05).",
     "Learn how natural diamonds form and where they come from, and what makes them rare or valuable.",
     "Formation and geology; mining and extraction; rough/raw diamond identification (as a section); rarity, supply and investment (conditional); conflict-free sourcing explainer (conditional).",
     "Natural-diamond shopping head terms (CL-070 'natural diamonds' 18,100 is a retailer/brand SERP); rough-diamond buying (CL-071 CATEGORY SERP); the lab-vs-natural comparison (Lab-Grown hub owns it); HOD's own sourcing claims (brand/trust page, not Education).",
     "LOW", "PROPOSED_PROVISIONAL"),
    ("H-4C", "Diamond Quality (4Cs)", "KEEP", "EDU-4C-00",
     "12 quality clusters plus cut grade (CL-050). Stage 8 SERPs for clarity, SI2, VVS, colour and cut are EDITORIAL_GUIDE and served by education paths (4cs.gia.edu, brilliantearth /guides/, whiteflash /diamond-education/).",
     "Understand how diamonds are graded and which grades to choose.",
     "4Cs overview (including how lab-grown stones are graded); clarity scale, inclusions and eye-clean; clarity grade explainers; colour; cut grade and light performance; carat and size; fancy colour (conditional).",
     "Shape names ('asscher cut', 'emerald cut': Shapes hub); certification labs and reports (Certification hub); lab-grown appearance issues such as cloudiness and fluorescence (Lab-Grown hub); carat-led shopping pages (commercial).",
     "MEDIUM", "PROPOSED"),
    ("H-SHP", "Diamond Shapes", "SPLIT", "EDU-SHP-00",
     "Candidate 'Shapes & Cuts' is split. Shapes stay here ('diamond shape' 60,500 is an EDITORIAL_GUIDE SERP served by education paths). 'Cut' as a quality grade moves to Diamond Quality (CL-050 'diamond cut grade' SERP is 4Cs cut pages).",
     "Compare diamond shapes and pick one, usually for an engagement ring.",
     "Shapes overview and shape selection for engagement rings; per-shape characteristics as sections; shape vs cut terminology.",
     "Cut grade (Diamond Quality); shape shopping and shape filter states (commercial, Stage 12 D-08); per-shape landing pages (deferred); the marquise-oval PDP (commercial).",
     "MEDIUM", "PROPOSED"),
    ("H-CERT", "Certification & Grading Reports", "KEEP", "EDU-CERT-00",
     "5 certification clusters; Stage 8 shows the general lab-grown certification SERP and the GIA-vs-IGI SERP share 0 top-10 URLs, so two distinct resources are needed. Existing IGI blog and GIA-vs-IGI Education article both belong here.",
     "Know what a diamond certificate is, which lab to trust and how the labs compare.",
     "General (lab-grown-focused) certification explainer; GIA vs IGI comparison; reading a grading report (conditional); IGI-only explainer (deferred).",
     "Grade definitions (Diamond Quality); lab report-lookup navigation (users go to the lab's own site); HOD's certificate policy (FAQ/product pages).",
     "MEDIUM", "PROPOSED"),
    ("H-MET", "Metals & Materials", "KEEP", "EDU-MET-00",
     "CL-110 is HIGH evidence with 3 Stage 3 rankings; CL-111/CL-112/CL-113 have validated EDITORIAL_GUIDE SERPs. Metal choice is a real step in every ring purchase.",
     "Choose a metal for a ring or piece of jewellery.",
     "Metals overview (gold karats, white/yellow/rose gold, platinum, hypoallergenic, mixing metals, alternative metals as a section); 14k vs 18k; rhodium plating (conditional).",
     "Novelty/alternative-material ring shopping (CL-114, off scope); mixed-metal ring shopping (CL-123 CATEGORY SERP); stainless-steel and plated-jewellery care (Ring & Jewellery Guides, conditional); metal filter states (commercial).",
     "MEDIUM", "PROPOSED"),
    ("H-GEM", "Gemstones & Diamond Alternatives", "CONDITIONAL", "EDU-GEM-00",
     "13 clusters with large demand (moissanite 201,000) but no evidence that HOD sells moissanite, simulants or coloured gemstones (Stage 12 business question 3). Comparison content that defends a lab-grown purchase has a business case; standalone gemstone education does not yet.",
     "Compare diamond alternatives with diamonds before choosing.",
     "Simulants and CZ explainer; moissanite vs lab-grown; moissanite vs diamond (all conditional); moissanite and coloured gemstones (deferred).",
     "Gemstone or moissanite shopping (CL-104, CL-105, CL-090 head: commercial, not in catalogue); synthetic-vs-simulant authenticity for lab-grown (Lab-Grown hub, 'are lab-grown diamonds real').",
     "MEDIUM", "CONDITIONAL"),
    ("H-RJG", "Ring & Jewellery Guides", "KEEP", "EDU-RJG-00",
     "Practical ownership and selection topics with validated editorial SERPs (settings) or clear business utility (ring size). Absorbs the candidate 'care' topic.",
     "Practical help choosing, sizing and caring for rings and jewellery.",
     "Ring settings; ring sizing and resizing; ring-size tool (conditional); jewellery care and everyday wear (conditional); engagement-ring buying guide (deferred).",
     "Engagement-ring style shopping (commercial style subcategories, Stage 12 D-03); HOD resizing/returns policy (FAQ/policy pages); stud-earring shopping (CL-125, commercial).",
     "MEDIUM", "PROPOSED"),
    ("H-BUY", "Buying Guides", "MERGE", "",
     "Not a hub. Every validated buying question is about a specific subject (choosing a lab-grown stone, best clarity, carat size, worth-it), so a separate Buying Guides hub would duplicate the topic hubs and compete with them. BUYING_GUIDE stays a page type inside the relevant hub.",
     "n/a (need is served inside topic hubs)", "Nothing; the page type is distributed.",
     "Everything; topic hubs own their buying guides.", "MEDIUM", "NOT_PROPOSED_AS_HUB"),
    ("H-SCI", "Diamond Basics & Science", "MERGE", "",
     "Not a hub. Candidate surfaced by Stage 11 clusters CL-065 and CL-080 to CL-088 (composition, hardness, melting point, facts, facets). No member is SERP-validated and business relevance is limited to durability. One consolidated article plus one conditional topic sit at the Education root instead of a thin hub.",
     "n/a (served by root-level articles)", "Nothing.",
     "Everything; see EDU-GEN-01 and EDU-GEN-02 at root level.", "LOW", "NOT_PROPOSED_AS_HUB"),
]
HUB_BY_ID = {h[0]: h for h in HUBS}

# --------------------------------------------------------------------------
# 2. Topics
# --------------------------------------------------------------------------
# Fields: id, hub, name, purpose, need, intent, evidence, serp_avail, existing, ex_action,
#         page_type, separate, consolidation_reason, risk, business_dep, status, notes, owns, not_owns
T = []
def topic(**k): T.append(k)

NONE_EX = "None"
topic(id="EDU-LG-00", hub="H-LG", name="Lab-grown diamonds explained (hub pillar: definition, names, types, short history)",
      purpose="Broad definitional resource that doubles as the Lab-Grown hub landing page.",
      need="What is a lab-grown diamond, what else is it called, what types exist?",
      intent="INFORMATIONAL", evidence="LOW", serp="NO", existing=NONE_EX, ex_action="NONE",
      page_type="EDUCATION_TOPIC_HUB_PILLAR", separate="YES",
      reason="CL-002 (definition), CL-003 (names/terminology incl. 'synthetic diamonds' 2,900) and CL-004 (types) are all 'what is it' needs with small demand each; one pillar avoids three thin pages and avoids a separate hub page competing with a separate 'what are' article.",
      risk="MEDIUM", dep="None for Education. The commercial head term belongs to the conditional commercial Lab-Grown hub (Stage 12 D-05).",
      status="PROPOSED",
      notes="REL-004: head-term SERP is BRAND/CATEGORY, definitional queries are informational (DISTINCT_INTENT). The pillar must not target 'lab grown diamonds' / 'lab diamonds' (commercial). History facts from CL-014 may appear as a short section; dated market commentary is Blog.",
      owns="Definition, terminology (lab-grown / lab-created / synthetic / man-made, FTC naming), types, brief evergreen history, links to every lab-grown topic.",
      not_owns="Commercial head terms; authenticity debate (EDU-LG-01); method detail (EDU-LG-03).")
topic(id="EDU-LG-01", hub="H-LG", name="Are lab-grown diamonds real? (authenticity)",
      purpose="Answer the trust question: is a lab-grown diamond a real diamond, and how does it differ from fakes and simulants.",
      need="Is it real / fake / a 'real diamond'?",
      intent="INFORMATIONAL", evidence="MEDIUM", serp="YES", existing="Blog: are-lab-grown-diamonds-real article", ex_action="MOVE_TO_EDUCATION",
      page_type="EDUCATION_ARTICLE", separate="YES",
      reason="Stage 11 REL-020 (HIGH confidence): CL-010 vs CL-011 validated pairs share mean 1.0, max 2 top-10 URLs, below the 3-URL same-intent threshold. Kept separate from the comparison.",
      risk="MEDIUM", dep="None.", status="PROPOSED",
      notes="Both SERPs are COMPARISON-dominant and kay.com's lab-vs-natural page ranks in both, so the boundary needs discipline: this page answers 'is it real' (chemistry, grading, FTC definition, synthetic vs simulant) and links to EDU-LG-02 for 'which should I buy'. 'do lab-grown diamonds look real' (CL-019) is appearance, not authenticity.",
      owns="Real vs fake, chemically/physically identical, synthetic vs simulant distinction, 'are CVD diamonds real' as a mention linking to EDU-LG-03.",
      not_owns="Head-to-head buying comparison (EDU-LG-02); tester questions (EDU-LG-09); pros/cons (EDU-LG-06).")
topic(id="EDU-LG-02", hub="H-LG", name="Lab-grown vs natural diamonds (comparison)",
      purpose="Head-to-head decision support between the two origins.",
      need="Which should I buy, lab-grown or natural, and how do they differ?",
      intent="COMMERCIAL_RESEARCH", evidence="HIGH", serp="YES", existing="Blog: lab-grown-vs-natural article (HOD's 2nd-best ranking, pos 29)", ex_action="UPDATE_IN_PLACE",
      page_type="COMPARISON_GUIDE", separate="YES",
      reason="CL-011 is HIGH evidence (4 validated, COMPARISON SERP for the 22,200 head term). Primary home for CL-011; also the interim home for the worth-it evaluation (CL-012) until that boundary is SERP-tested.",
      risk="MEDIUM", dep="None.", status="PROPOSED",
      notes="HIGH migration risk: stays at its current /blog URL (Stage 13 DO_NOT_MOVE_NOW, 9 conditions). Ownership is Education; location is unchanged. REL-057: natural head terms (CL-070) share mean 0.6 URLs with this cluster, so the commercial natural SERP is not this page's job.",
      owns="Origin comparison: price, value, appearance, ethics, durability, grading compared side by side; 'which is better' queries.",
      not_owns="'Is it real' (EDU-LG-01); detailed resale (EDU-LG-05); natural formation (EDU-NAT-00).")
topic(id="EDU-LG-03", hub="H-LG", name="CVD vs HPHT (single home for CVD and HPHT)",
      purpose="Explain both growth methods and compare them, including 'what is an HPHT / CVD diamond'.",
      need="What are CVD and HPHT diamonds, and which is better?",
      intent="INFORMATIONAL", evidence="HIGH", serp="YES", existing="Blog: cvd-vs-hpht article (19 of HOD's 28 Stage 3 rankings)", ex_action="UPDATE_IN_PLACE",
      page_type="COMPARISON_GUIDE", separate="YES",
      reason="CL-016/017/018 consolidated into one resource. (1) The HPHT head SERP ('hpht lab grown diamonds', 8,100) is led by comparison pages: 4 of 9 organic results are HPHT-vs-CVD articles, plus gia.edu's combined 'HPHT and CVD growth processes' page; only 3 are HPHT-only. (2) The comparison article already ranks for HPHT (pos 49, about 34 of its 36.5 ETV) and for CVD ('are cvd diamonds real' pos 27). (3) Single-method CVD SERPs share 3 to 4 URLs with CVD-vs-HPHT SERPs. A separate HPHT or CVD page would split the only equity HOD has.",
      risk="HIGH", dep="None.", status="PROPOSED",
      notes="HIGH migration risk: stays at its current /blog URL (Stage 13 DO_NOT_MOVE_NOW). Risk is HIGH at the boundary with any future single-method page or a separate 'how lab-grown diamonds are made' page (EDU-LG-04), not inside the resource. CVD and HPHT are SECTION_ONLY sub-nodes. The tester query 'cvd/hpht diamond tester' (PAGE_TYPE_MISMATCH) is not this page's target.",
      owns="HPHT explained, CVD explained, CVD vs HPHT comparison, post-growth treatment mention, 'CVD vs lab-grown' confusion queries.",
      not_owns="General 'how are lab-grown diamonds made' beginner process (EDU-LG-04, conditional); tester shopping.")
topic(id="EDU-LG-04", hub="H-LG", name="How lab-grown diamonds are made (process)",
      purpose="Beginner explanation of the manufacturing process.",
      need="How are lab diamonds made?",
      intent="INFORMATIONAL", evidence="INSUFFICIENT_EVIDENCE", serp="NO", existing=NONE_EX, ex_action="NONE",
      page_type="EDUCATION_ARTICLE", separate="CONDITIONAL",
      reason="CL-015 (18 kw, 'how are synthetic diamonds made' 880) has no validated SERP. brilliantearth's 'how are lab-grown diamonds made' guide ranks inside both the HPHT and CVD SERPs, so Google may treat process and method as one need. Until tested, the process is covered in the pillar (EDU-LG-00) and in the CVD vs HPHT resource.",
      risk="HIGH", dep="None.", status="CONDITIONAL",
      notes="INSUFFICIENT_EVIDENCE — requires later SERP validation. Test: if 'how are lab grown diamonds made' shares 3 or more top-10 URLs with the CVD-vs-HPHT SERPs, fold CL-015 into EDU-LG-03 permanently; if 0 to 2, create this page. Also ambiguous with natural formation ('how are diamonds made', REL-014). Industry/factory questions (CL-026) are Blog/brand material (Surat manufacturing).",
      owns="Process overview (seed, growth, cutting) if created.", not_owns="Method comparison (EDU-LG-03); natural formation (EDU-NAT-00).")
topic(id="EDU-LG-05", hub="H-LG", name="Lab-grown diamond price, value & resale",
      purpose="Explain why lab-grown costs less, whether it holds value and whether it can be resold or pawned.",
      need="Are they cheaper, do they hold value, can I sell one?",
      intent="INFORMATIONAL", evidence="LOW", serp="NO", existing=NONE_EX, ex_action="NONE",
      page_type="EDUCATION_ARTICLE", separate="YES",
      reason="CL-008 (price) and CL-009 (value/resale) are related-but-distinct money questions (REL-009, REL-010) with no SERP evidence either way; CL-086's head terms are lab-grown pawn/sell questions. One money resource avoids three thin pages.",
      risk="MEDIUM", dep="Avoid hard-coded prices (Stage 13 framework: price levels date; dated price commentary is Blog).", status="PROPOSED_PROVISIONAL",
      notes="Boundary with EDU-LG-06 (worth it) is the main risk: resale is the leading 'con'. Worth-it links here for detail. General diamond investment (CL-085) sits in Natural Diamonds.",
      owns="Why cheaper, price principles (no dated price tables), value retention, resale and pawn.", not_owns="Overall worth-it evaluation (EDU-LG-06); natural-diamond investment (EDU-NAT-01).")
topic(id="EDU-LG-06", hub="H-LG", name="Are lab-grown diamonds worth it? (pros & cons)",
      purpose="Evaluate lab-grown on its own merits, including disadvantages.",
      need="Is a lab-grown diamond a good buy, what are the downsides?",
      intent="COMMERCIAL_RESEARCH", evidence="LOW", serp="NO", existing=NONE_EX, ex_action="NONE",
      page_type="BUYING_GUIDE", separate="CONDITIONAL",
      reason="CL-012 has real demand ('are lab grown diamonds worth it' 1,900; 'are lab-grown diamonds good' 1,300; 'disadvantages' 880) but no SERP. The 'are lab grown diamonds real' SERP already contains a pros/cons page (frankdarling '7 reasons not to buy'), so worth-it may share a SERP with authenticity or comparison. Interim home: a pros/cons section of EDU-LG-02.",
      risk="INSUFFICIENT_EVIDENCE", dep="None.", status="CONDITIONAL",
      notes="INSUFFICIENT_EVIDENCE — requires later SERP validation of 'are lab grown diamonds worth it' against the CL-010 and CL-011 SERPs (3-URL rule).",
      owns="Pros and cons, who it suits, disadvantages.", not_owns="Head-to-head comparison (EDU-LG-02); resale detail (EDU-LG-05).")
topic(id="EDU-LG-07", hub="H-LG", name="Lab-grown diamond ethics & sustainability",
      purpose="Explain the ethical and environmental case, with its limits.",
      need="Are lab-grown diamonds ethical / better for the environment?",
      intent="INFORMATIONAL", evidence="LOW", serp="NO", existing=NONE_EX, ex_action="NONE",
      page_type="EDUCATION_ARTICLE", separate="YES",
      reason="CL-013 (16 kw) is a distinct evaluative question (REL-012). Kept separate from natural conflict-free sourcing (CL-073) because that SERP is retailer sourcing-policy pages, a different page type.",
      risk="MEDIUM", dep="Any environmental or sourcing claim about HOD must be substantiated (trust principle).", status="PROPOSED_PROVISIONAL",
      notes="REL-013 POSSIBLE_OVERLAP (LOW confidence) with CL-073. HOD's own sourcing and Surat workshop story is Blog/brand content.",
      owns="Ethics, carbon/energy, sustainability claims explained.", not_owns="Conflict-free natural sourcing (EDU-NAT-02); HOD brand story (Blog).")
topic(id="EDU-LG-08", hub="H-LG", name="Lab-grown diamond appearance & durability (cloudiness, fluorescence, treatments)",
      purpose="Answer post-purchase worries about how lab-grown stones look and age.",
      need="Do lab-grown diamonds get cloudy, fluoresce, fade, or get treated?",
      intent="INFORMATIONAL", evidence="LOW", serp="NO", existing=NONE_EX, ex_action="NONE",
      page_type="EDUCATION_ARTICLE", separate="YES",
      reason="CL-019 (cloudiness, UV/fluorescence, fading, 'look real') and CL-089 (irradiated / post-growth treated) are lab-grown-specific appearance questions that the 4Cs pages do not answer.",
      risk="MEDIUM", dep="None.", status="PROPOSED_PROVISIONAL",
      notes="'do lab-grown diamonds look real' (110) sits close to EDU-LG-01; Stage 15 decides keyword placement. Lab-grown grading charts (CL-023) are NOT here; they are integrated into the 4Cs overview.",
      owns="Cloudiness, fluorescence, glow, fading, colour tints, treatments.", not_owns="Grading scales (Diamond Quality); authenticity (EDU-LG-01).")
topic(id="EDU-LG-09", hub="H-LG", name="Detecting lab-grown diamonds (testers & identification)",
      purpose="Explain whether testers and jewellers can tell lab-grown from natural.",
      need="Will a lab-grown diamond pass a diamond tester; can a jeweller tell?",
      intent="INFORMATIONAL", evidence="LOW", serp="PARTIAL", existing="Blog: cvd-vs-hpht article ranks for 'cvd/hpht diamond tester' (pos 68, PAGE_TYPE_MISMATCH)", ex_action="NONE",
      page_type="EDUCATION_ARTICLE", separate="YES",
      reason="CL-020 (identification), CL-021 (tester results, 28 kw, 880 head) and the informational members of CL-022 (tester methods) answer one need: can it be detected. REL-016/REL-018 are RELATED_BUT_DISTINCT without SERP evidence; the lab-grown tester SERP itself is not validated.",
      risk="MEDIUM", dep="Tester device shopping is not HOD's business (Stage 12 D-16); transactional CL-022 members are not targeted.", status="PROPOSED_PROVISIONAL",
      notes="Moissanite tester questions (CL-093) share only 1 URL with tester-device SERPs (REL-019) and are deferred with moissanite; this page may mention moissanite briefly (REL-017 POSSIBLE_OVERLAP LOW).",
      owns="Thermal/conductivity testers, lab detection, jeweller identification, inscriptions.", not_owns="Tester shopping; moissanite tester deep-dive (deferred).")
topic(id="EDU-LG-10", hub="H-LG", name="How to choose a lab-grown diamond (buying guide)",
      purpose="Step-by-step selection of a lab-grown stone.",
      need="How do I pick a good lab-grown diamond?",
      intent="COMMERCIAL_RESEARCH", evidence="MEDIUM", serp="YES", existing="Blog: how-to-choose-a-lab-grown-diamond article (pos 35)", ex_action="DEFER",
      page_type="BUYING_GUIDE", separate="YES",
      reason="CL-024 is small (3 kw, max 30) but validated EDITORIAL_GUIDE and HOD ranks at pos 35. The topic stays; the existing article's migration is deferred by Stage 13 because its relationship with the online engagement-ring guide is unresolved.",
      risk="MEDIUM", dep="Depends on the D-19 commercial keyword/SERP supplement (unapproved) for the engagement-ring buying-guide boundary.", status="PROPOSED",
      notes="Bridges Education to the commercial Lab-Grown hub and engagement-ring categories. Boundary with EDU-RJG-04 (engagement-ring buying guide) is INSUFFICIENT_EVIDENCE (OV-06). If consolidated later, this article is the presumed survivor (Stage 13).",
      owns="Stone selection priorities for lab-grown (4Cs trade-offs, certificate, budget).", not_owns="Ring buying process and online purchase logistics (EDU-RJG-04, deferred).")

topic(id="EDU-NAT-00", hub="H-NAT", name="Natural diamonds: how they form and where they come from (hub pillar)",
      purpose="Formation, geology and mining explained; landing page for natural-diamond education.",
      need="How are diamonds formed / mined?",
      intent="INFORMATIONAL", evidence="LOW", serp="NO", existing=NONE_EX, ex_action="NONE",
      page_type="EDUCATION_TOPIC_HUB_PILLAR", separate="YES",
      reason="CL-075 ('how is diamond formed' 12,100) and CL-074 (mining, kimberlite 'diamond pipes') describe one process from depth to mine; one pillar covers both. Raw/rough identification (CL-071 informational members) is a section.",
      risk="INSUFFICIENT_EVIDENCE", dep="Education only. Commercial natural hub deferred (Stage 12 D-05; business question 1).", status="PROPOSED_PROVISIONAL",
      notes="REL-014: 'how are diamonds made' is ambiguous between natural formation and lab manufacture; no SERP separates them. INSUFFICIENT_EVIDENCE — requires later SERP validation.",
      owns="Formation, kimberlite pipes, mining and extraction, what rough diamonds look like.", not_owns="Natural shopping head terms (CL-070); rough-diamond buying (CL-071 CATEGORY SERP); lab manufacture.")
topic(id="EDU-NAT-01", hub="H-NAT", name="Natural diamond value, rarity & investment",
      purpose="Explain supply, rarity and whether diamonds are an investment.",
      need="Are diamonds rare, a good investment, do they rise in value?",
      intent="INFORMATIONAL", evidence="LOW", serp="NO", existing=NONE_EX, ex_action="NONE",
      page_type="EDUCATION_ARTICLE", separate="CONDITIONAL",
      reason="CL-076 (supply/rarity) and CL-085 (investment, 'are diamonds a good investment' 720) share a searcher worry about value. Conditional because demand is modest and investment claims carry risk.",
      risk="MEDIUM", dep="HOD's natural offering unconfirmed (Stage 12 business question 1). No investment advice; explain principles only.", status="CONDITIONAL",
      notes="Boundary with EDU-LG-05 (lab-grown resale) is RELATED_BUT_DISTINCT (REL-058). Interim: a value section in EDU-LG-02 covers the origin contrast.",
      owns="Rarity, supply, value trends explained.", not_owns="Lab-grown resale (EDU-LG-05).")
topic(id="EDU-NAT-02", hub="H-NAT", name="Conflict-free diamonds & responsible sourcing",
      purpose="Explain blood diamonds, the Kimberley Process and sourcing assurance.",
      need="What are conflict-free diamonds and how is sourcing assured?",
      intent="INFORMATIONAL", evidence="MEDIUM", serp="PARTIAL", existing=NONE_EX, ex_action="NONE",
      page_type="EDUCATION_ARTICLE", separate="CONDITIONAL",
      reason="CL-073 has one validated SERP ('conflict free diamonds' 2,900) dominated by retailers' own sourcing-policy pages (brilliantearth, jared, cleanorigin, robbinsbrothers) plus one gemsociety explainer. Google mostly serves a brand-policy page type, which HOD can only publish with a substantiated sourcing policy.",
      risk="MEDIUM", dep="HIGH: requires HOD's documented sourcing policy; may be better served by a brand/trust page than an Education article.", status="CONDITIONAL",
      notes="REL-013 POSSIBLE_OVERLAP (LOW) with lab-grown ethics (EDU-LG-07). Kept separate: different origin, different page type.",
      owns="Blood diamonds, Kimberley Process, sourcing assurance explained.", not_owns="Lab-grown ethics (EDU-LG-07); HOD's own claims (brand page).")

topic(id="EDU-4C-00", hub="H-4C", name="The 4Cs of diamond quality (hub pillar, incl. how lab-grown diamonds are graded)",
      purpose="Overview of cut, colour, clarity, carat and grading charts; landing page for Diamond Quality.",
      need="How are diamonds graded; what do the 4Cs mean?",
      intent="INFORMATIONAL", evidence="MEDIUM", serp="PARTIAL", existing="Blog: 4Cs-of-lab-grown-diamonds article", ex_action="MOVE_TO_EDUCATION",
      page_type="EDUCATION_TOPIC_HUB_PILLAR", separate="YES",
      reason="CL-040 (grading scales and charts), CL-023 (lab-grown grade charts) and CL-048 (colour+clarity combinations) are overview-level needs. Lab-grown grading is integrated rather than separate: lab-grown stones are graded on the same scales, and a separate lab-grown 4Cs page would compete directly with this one.",
      risk="MEDIUM", dep="None.", status="PROPOSED",
      notes="Resolves the Stage 13 question: the existing 4Cs article becomes the general 4Cs overview with a lab-grown section, not a lab-grown-only page. Stage 15 flag: CL-040's 'diamond clarity grading scale' (12,100) SERP is clarity pages (4cs.gia.edu clarity, tiffany clarity), so that keyword belongs to EDU-4C-01. Separating CL-023 from CL-040 is INSUFFICIENT_EVIDENCE — requires later SERP validation ('lab grown diamond clarity chart').",
      owns="4Cs overview, grading charts, how grades combine, lab-grown grading.", not_owns="Deep single-C guides (EDU-4C-01 to 4C-07); certification labs.")
topic(id="EDU-4C-01", hub="H-4C", name="Diamond clarity guide (scale, inclusions, eye-clean, best clarity to buy)",
      purpose="Explain the clarity scale and how to choose a clarity grade.",
      need="What do clarity grades mean and which should I buy?",
      intent="INFORMATIONAL", evidence="MEDIUM", serp="YES", existing="Covered today only inside the 4Cs article", ex_action="NONE",
      page_type="EDUCATION_ARTICLE", separate="YES",
      reason="The clarity-scale SERP shares 0 URLs with the SI2 SERP and 1 with the VVS SERP, so Google serves the scale separately from single-grade pages. CL-046 (inclusions, eye-clean), CL-045 (best clarity to buy) and CL-044 (grade-vs-grade comparisons) consolidate here.",
      risk="MEDIUM", dep="None.", status="PROPOSED",
      notes="CL-044 comparisons are PRIMARY here and SECONDARY on the grade pages. The VVS SERP contains 'VVS vs VS' and 'VVS vs SI' pages, and the SI2 SERP contains 'SI1 vs SI2' pages, so Stage 15 may place individual comparison keywords on the grade page of the better grade.",
      owns="Clarity scale, inclusion types, eye-clean, which clarity to buy, grade comparisons.", not_owns="Single-grade deep dives (EDU-4C-02/03/04).")
topic(id="EDU-4C-02", hub="H-4C", name="SI clarity diamonds (SI1, SI2, SI3)",
      purpose="Single-grade explainer for SI clarity.", need="Is an SI1/SI2 diamond good?",
      intent="INFORMATIONAL", evidence="HIGH", serp="YES", existing=NONE_EX, ex_action="NONE",
      page_type="GRADE_EXPLAINER", separate="YES",
      reason="CL-041 is HIGH evidence: 'si2 diamond clarity' and 'si2 diamond' share 7 of 10 URLs with each other and 0 with the clarity-scale SERP. Competitors (whiteflash, brilliantearth, rarecarat, rockher) rank single-grade pages.",
      risk="LOW", dep="None.", status="PROPOSED", notes="Receives SI-related comparison keywords from CL-044 in Stage 15 where appropriate.",
      owns="SI1/SI2/SI3 meaning, eye-clean likelihood, value.", not_owns="Full clarity scale (EDU-4C-01).")
topic(id="EDU-4C-03", hub="H-4C", name="VVS, IF & flawless clarity diamonds",
      purpose="Single-grade explainer for the top clarity grades.", need="What is a VVS / flawless diamond; is it worth it?",
      intent="INFORMATIONAL", evidence="MEDIUM", serp="YES", existing=NONE_EX, ex_action="NONE",
      page_type="GRADE_EXPLAINER", separate="YES",
      reason="CL-043 head 'v v s diamond' (18,100) SERP is EDITORIAL_GUIDE (4cs.gia.edu, whiteflash, brilliantearth vvs guide) and shares 0 URLs with SI2 and 1 with the clarity scale.",
      risk="MEDIUM", dep="None.", status="PROPOSED",
      notes="The VVS SERP also has shopping results (diamondere vvs rings, bluenile vvs inventory). The page must stay explanatory and link to commercial pages. 'vvs lab diamonds' members of CL-023 may map here in Stage 15.",
      owns="VVS1/VVS2, IF, FL meaning and value.", not_owns="VVS jewellery shopping.")
topic(id="EDU-4C-04", hub="H-4C", name="VS clarity diamonds (VS1, VS2)",
      purpose="Single-grade explainer for VS clarity.", need="Is a VS1/VS2 diamond good?",
      intent="INFORMATIONAL", evidence="LOW", serp="NO", existing=NONE_EX, ex_action="NONE",
      page_type="GRADE_EXPLAINER", separate="CONDITIONAL",
      reason="CL-042 (6 kw, 880 head) has no validated SERP. The SI and VVS pattern suggests grade pages are a distinct SERP type, but that is inference. Interim: VS is a section of the clarity guide.",
      risk="INSUFFICIENT_EVIDENCE", dep="None.", status="CONDITIONAL",
      notes="INSUFFICIENT_EVIDENCE — requires later SERP validation ('vs diamond quality' / 'vs1 clarity').",
      owns="VS1/VS2 meaning if created.", not_owns="Full clarity scale.")
topic(id="EDU-4C-05", hub="H-4C", name="Diamond colour guide (D to Z colour grades)",
      purpose="Explain colour grades and which to choose.", need="What colour grade should I buy; are G/H diamonds good?",
      intent="COMMERCIAL_RESEARCH", evidence="MEDIUM", serp="YES", existing="Covered today only inside the 4Cs article", ex_action="NONE",
      page_type="EDUCATION_ARTICLE", separate="YES",
      reason="CL-047 (28 kw, 'colorless diamond' 3,600): validated 'are g h diamonds good quality' is EDITORIAL_GUIDE (brilliantearth diamond-color, gia 4cs-color) and shares 0 URLs with the clarity-scale SERP.",
      risk="LOW", dep="None.", status="PROPOSED", notes="Colour+clarity combination queries (CL-048) live in the 4Cs pillar.",
      owns="D to Z colour scale, near-colourless value, colour vs metal.", not_owns="Fancy colours (EDU-4C-08).")
topic(id="EDU-4C-06", hub="H-4C", name="Diamond cut guide (cut grade, facets & light performance)",
      purpose="Explain cut grade, sparkle and facet optics.", need="What is a good cut grade; which cut sparkles most?",
      intent="INFORMATIONAL", evidence="MEDIUM", serp="YES", existing=NONE_EX, ex_action="NONE",
      page_type="EDUCATION_ARTICLE", separate="YES",
      reason="CL-050 validated 'diamond cut grade' is EDITORIAL_GUIDE (4cs.gia.edu cut, tiffany cut, brilliantearth cut). CL-088 (facets, refraction) is the optics behind cut and consolidates here.",
      risk="MEDIUM", dep="None.", status="PROPOSED",
      notes="Boundary with Diamond Shapes: 'cut' as grade lives here; 'cut' as shape name ('asscher cut') lives in Shapes. CL-050 existing-content relationship is INSUFFICIENT_EVIDENCE in Stage 11.",
      owns="Cut grades, proportions, facets, brilliance/fire.", not_owns="Shape names and shape choice.")
topic(id="EDU-4C-07", hub="H-4C", name="Diamond carat guide (weight, size & 'is it big enough')",
      purpose="Explain carat weight and size suitability.", need="Is a 1 / 2 / 3 carat diamond good or too big?",
      intent="INFORMATIONAL", evidence="LOW", serp="NO", existing="Covered today only inside the 4Cs article", ex_action="NONE",
      page_type="EDUCATION_ARTICLE", separate="YES",
      reason="CL-049 (36 kw) is one repeated question pattern across carat sizes; one guide serves it. No SERP validation; Stage 11 flagged the cluster as broad.",
      risk="LOW", dep="Carat-led loose-stone shopping (CL-006) is commercial and deferred (Stage 12).", status="PROPOSED_PROVISIONAL",
      notes="Do not create one page per carat size.", owns="Carat vs size, size on hand, suitability by carat.", not_owns="Carat shopping pages.")
topic(id="EDU-4C-08", hub="H-4C", name="Fancy-coloured diamonds",
      purpose="Explain coloured diamonds (black, pink, red, green) natural and lab-grown.", need="Are black/pink diamonds real; what are fancy colours?",
      intent="INFORMATIONAL", evidence="LOW", serp="NO", existing=NONE_EX, ex_action="NONE",
      page_type="EDUCATION_ARTICLE", separate="CONDITIONAL",
      reason="CL-051 (15 kw, 'are black diamonds real' 1,600) is a distinct need from the D to Z colour scale, but its business value depends on HOD offering coloured diamonds.",
      risk="MEDIUM", dep="Depends on whether HOD sells fancy-colour (lab-grown) diamonds.", status="CONDITIONAL",
      notes="REL-062 RELATED_BUT_DISTINCT with lab-grown authenticity ('are black diamonds real' vs 'are lab-grown diamonds real').",
      owns="Fancy colour types, natural vs lab-grown colours.", not_owns="D to Z colour grading (EDU-4C-05).")

topic(id="EDU-SHP-00", hub="H-SHP", name="Diamond shapes guide (hub pillar, incl. choosing a shape for an engagement ring)",
      purpose="Compare shapes and help choose one.", need="What diamond shapes exist and which should I choose?",
      intent="INFORMATIONAL", evidence="MEDIUM", serp="YES", existing="Blog: best-lab-grown-diamond-shapes-for-engagement-rings article", ex_action="MOVE_TO_EDUCATION",
      page_type="DIAMOND_SHAPE_GUIDE", separate="YES",
      reason="'diamond shape' (60,500) SERP is EDITORIAL_GUIDE via education paths, and its top result is GIA's guide to diamond shapes for engagement rings, so Google blends the overview with engagement-ring shape choice. CL-060 and CL-064 therefore share one resource; CL-061 (asscher) and CL-062 (radiant) are sections until per-shape pages are justified.",
      risk="LOW", dep="None.", status="PROPOSED",
      notes="Resolves the Stage 13 question: the existing shapes article becomes the shapes overview (which includes engagement-ring shape choice), not a separate chooser page.",
      owns="All shapes compared, shape vs cut terminology, shape by ring style and hand, per-shape sections.", not_owns="Cut grade (EDU-4C-06); shape shopping/filters (commercial).")
topic(id="EDU-SHP-01", hub="H-SHP", name="Individual shape guides (per-shape pages)",
      purpose="Deeper page for a single shape.", need="Is an asscher / radiant cut right for me?",
      intent="MIXED", evidence="MEDIUM", serp="PARTIAL", existing=NONE_EX, ex_action="NONE",
      page_type="DIAMOND_SHAPE_GUIDE", separate="DEFERRED",
      reason="The 'asscher cut diamond' (18,100) SERP is inventory-led: bluenile /diamonds/asscher-cut, brilliantearth /diamond/asscher, goodstone collections, adiamor search, a brand site; only 1 of 7 is an education page. It shares 0 URLs with 'diamond shape'. A per-shape Education page does not match the dominant page type.",
      risk="MEDIUM", dep="Loose-diamond / shape landing pages are a commercial question (Stage 12 business question 2; D-08 shape is a filter by default).", status="DEFERRED",
      notes="Revisit per shape only with SERP evidence that education pages dominate for that shape's query. No shape page is proposed now.",
      owns="Nothing now.", not_owns="Shape shopping.")

topic(id="EDU-CERT-00", hub="H-CERT", name="Diamond certification explained (hub pillar; lab-grown focus; GIA, IGI and other labs)",
      purpose="Explain what certification is, why it matters and which labs grade lab-grown diamonds.",
      need="What is diamond certification; should my lab-grown diamond be certified?",
      intent="INFORMATIONAL", evidence="MEDIUM", serp="YES", existing="Blog: IGI-certification article (to be retargeted here)", ex_action="RETARGET",
      page_type="CERTIFICATION_GUIDE", separate="YES",
      reason="Validated 'lab-grown diamond certification' (390) SERP is EDITORIAL_GUIDE (igi.org report page, gia.edu lab-grown service, retailer certification guides) and shares 0 URLs with 'gia vs igi lab diamond'. CL-033 is primary; CL-031 (GIA reports) and CL-032 (IGI reports) are sections because neither has SERP evidence for a separate page.",
      risk="MEDIUM", dep="None.", status="PROPOSED",
      notes="Resolves Stage 13's RETARGET question: the IGI blog is retargeted to CL-033 (general lab-grown certification), not to CL-032 (IGI-only), because only CL-033 has SERP evidence. The guide doubles as the Certification hub landing page, so a separate thin hub does not compete for the same queries.",
      owns="Certification purpose, labs overview (GIA, IGI, others), lab-grown reports, 'does GIA certify lab-grown', IGI report basics.", not_owns="GIA-vs-IGI head-to-head (EDU-CERT-01); grade definitions (Diamond Quality).")
topic(id="EDU-CERT-01", hub="H-CERT", name="GIA vs IGI (comparison)",
      purpose="Head-to-head comparison of the two main labs.", need="Is GIA or IGI better for a lab-grown diamond?",
      intent="COMMERCIAL_RESEARCH", evidence="MEDIUM", serp="YES", existing="Education: lab-grown-diamond-certification-explained-gia-vs-igi article", ex_action="UPDATE_IN_PLACE",
      page_type="COMPARISON_GUIDE", separate="YES",
      reason="CL-030 validated 'gia vs igi lab diamond' is an EDITORIAL comparison SERP (bluenile, stienhardt, whiteflash, plumdiamonds). Preserves the Stage 13 split: comparison intent stays distinct from general certification.",
      risk="MEDIUM", dep="None.", status="PROPOSED",
      notes="Stage 10 OV-01 (CLEAR_OVERLAP at topic level) is resolved by narrowing this page to the comparison and moving general certification to EDU-CERT-00. Both changes should ship together (Stage 13).",
      owns="GIA vs IGI (and vs other labs) comparison.", not_owns="General certification explainer (EDU-CERT-00).")
topic(id="EDU-CERT-02", hub="H-CERT", name="How to read a diamond grading report",
      purpose="Walk through a grading report's fields.", need="What does my diamond report say?",
      intent="INFORMATIONAL", evidence="LOW", serp="PARTIAL", existing=NONE_EX, ex_action="NONE",
      page_type="CERTIFICATION_GUIDE", separate="CONDITIONAL",
      reason="CL-034 ('diamond grading report' 1,600) mixes an informational need with lab navigation and report lookups (AGS, GCAL, EGL, GSL). The one validated member ('ags diamond grading') is a BRAND SERP. Only the informational part is Education's; lookup queries go to the labs.",
      risk="MEDIUM", dep="None.", status="CONDITIONAL",
      notes="Interim: a 'reading your report' section in EDU-CERT-00.",
      owns="Report fields explained.", not_owns="Report lookup; lab brand queries.")
topic(id="EDU-CERT-03", hub="H-CERT", name="IGI report explained (IGI-only page)",
      purpose="IGI-specific explainer.", need="What is an IGI-certified lab diamond?",
      intent="INFORMATIONAL", evidence="INSUFFICIENT_EVIDENCE", serp="NO", existing=NONE_EX, ex_action="NONE",
      page_type="CERTIFICATION_GUIDE", separate="DEFERRED",
      reason="No IGI-only keyword was SERP-validated (Stage 13). Creating it next to EDU-CERT-00 and EDU-CERT-01 without evidence would recreate the OV-01 overlap.",
      risk="HIGH", dep="None.", status="DEFERRED",
      notes="INSUFFICIENT_EVIDENCE — requires later SERP validation ('igi lab grown diamond', 1,000).",
      owns="Nothing now.", not_owns="n/a")

topic(id="EDU-MET-00", hub="H-MET", name="Jewellery metals guide (hub pillar: gold, platinum, white gold, hypoallergenic, mixing, alternatives)",
      purpose="Help choose a metal; landing page for Metals & Materials.", need="Which metal is best for my ring or jewellery?",
      intent="INFORMATIONAL", evidence="LOW", serp="PARTIAL", existing=NONE_EX, ex_action="NONE",
      page_type="EDUCATION_TOPIC_HUB_PILLAR", separate="YES",
      reason="CL-112 (types, best metal, hypoallergenic) is primary. CL-113 (tungsten/titanium bands) is consolidated as an 'alternative metals' section, not a page: its SERP is tungsten-seller pros/cons pages and there is no evidence HOD sells these metals.",
      risk="LOW", dep="Alternative-metal coverage depends on the catalogue (no tungsten/titanium evidence).", status="PROPOSED_PROVISIONAL",
      notes="REL-046/REL-049: rhodium and tungsten SERPs share 0 URLs with the general-metal SERP. That makes them distinct intents; it does not oblige HOD to build pages for them. The single validated CL-112 keyword is an off-centre styling query, so evidence is LOW.",
      owns="Metal types, gold colours, platinum vs gold, hypoallergenic, mixing metals, alternative metals section.", not_owns="Karat comparison detail (EDU-MET-01); novelty rings (off scope).")
topic(id="EDU-MET-01", hub="H-MET", name="14k vs 18k gold (and 10k)",
      purpose="Karat comparison for diamond jewellery.", need="Is 14k or 18k better for a diamond ring?",
      intent="COMMERCIAL_RESEARCH", evidence="HIGH", serp="YES", existing="Blog: 14k-vs-18k-gold article (pos 81-95)", ex_action="MOVE_TO_EDUCATION",
      page_type="COMPARISON_GUIDE", separate="YES",
      reason="CL-110 is HIGH evidence (4 validated EDITORIAL_GUIDE SERPs) and shares at most 1 URL with the general-metal SERP (REL-045).",
      risk="LOW", dep="None.", status="PROPOSED", notes="Moves only when the Metals section exists (Stage 13 conditions).",
      owns="10k/14k/18k comparison.", not_owns="General metal choice (EDU-MET-00).")
topic(id="EDU-MET-02", hub="H-MET", name="Rhodium plating (white-gold upkeep)",
      purpose="Explain rhodium plating and replating.", need="What is rhodium plating; does my ring need replating?",
      intent="INFORMATIONAL", evidence="MEDIUM", serp="PARTIAL", existing=NONE_EX, ex_action="NONE",
      page_type="EDUCATION_ARTICLE", separate="CONDITIONAL",
      reason="CL-111 has 2 validated SERPs: 'rhodium plating ring' is EDITORIAL_GUIDE, 'rhodium ring' is mixed service/product pages; they share 1 URL and 0 with general metals. Relevant to white-gold owners, but the page would be conditional on HOD offering white gold and replating aftercare.",
      risk="MEDIUM", dep="Relevant only if HOD sells white gold and supports replating.", status="CONDITIONAL",
      notes="Interim: white-gold/rhodium section of EDU-MET-00. Overlaps care topics (EDU-RJG-03).",
      owns="Rhodium plating, replating frequency.", not_owns="General care.")

topic(id="EDU-GEM-00", hub="H-GEM", name="Diamond alternatives & simulants (hub pillar: CZ, simulated diamonds)",
      purpose="Explain simulants and how they compare with diamonds.", need="What is a simulated diamond; is CZ like a diamond?",
      intent="COMMERCIAL_RESEARCH", evidence="LOW", serp="NO", existing=NONE_EX, ex_action="NONE",
      page_type="EDUCATION_TOPIC_HUB_PILLAR", separate="CONDITIONAL",
      reason="CL-095 (simulants, 'simulated diamond' 4,400) and CL-094 (CZ vs diamond/lab-grown, 3,600) are one need (what is a diamond look-alike); REL-035 POSSIBLE_OVERLAP. No SERP evidence.",
      risk="MEDIUM", dep="Business decision: does HOD want alternative-comparison content (no sale of simulants required)?", status="CONDITIONAL",
      notes="Boundary with EDU-LG-01: synthetic (lab-grown, real diamond) vs simulant (not diamond). 'simulated diamond vs lab grown' belongs here; 'are lab grown diamonds real' belongs there.",
      owns="Simulants, CZ, synthetic vs simulant from the simulant side.", not_owns="Lab-grown authenticity (EDU-LG-01).")
topic(id="EDU-GEM-01", hub="H-GEM", name="Moissanite vs lab-grown diamond",
      purpose="Comparison that supports a lab-grown decision.", need="Should I choose moissanite or a lab-grown diamond?",
      intent="COMMERCIAL_RESEARCH", evidence="HIGH", serp="YES", existing=NONE_EX, ex_action="NONE",
      page_type="COMPARISON_GUIDE", separate="CONDITIONAL",
      reason="CL-092 is HIGH evidence (2 validated COMPARISON SERPs) and shares 0 URLs with both moissanite head terms and moissanite-vs-diamond (REL-036, REL-038). If built, it must be its own page.",
      risk="LOW", dep="Conditional on the Gemstones & Alternatives hub being approved. HOD selling moissanite is NOT assumed.", status="CONDITIONAL",
      notes="The most business-relevant alternative topic: it defends a lab-grown purchase.",
      owns="Moissanite vs lab-grown comparison.", not_owns="Moissanite shopping.")
topic(id="EDU-GEM-02", hub="H-GEM", name="Moissanite vs diamond",
      purpose="Comparison of moissanite with diamonds in general.", need="Is moissanite better than diamond?",
      intent="COMMERCIAL_RESEARCH", evidence="MEDIUM", serp="YES", existing=NONE_EX, ex_action="NONE",
      page_type="COMPARISON_GUIDE", separate="CONDITIONAL",
      reason="CL-091 validated COMPARISON SERP; 0 shared URLs with moissanite-vs-lab-grown, so one combined page would not serve both.",
      risk="LOW", dep="Conditional on the hub; lower priority for HOD than EDU-GEM-01.", status="CONDITIONAL",
      notes="If only one moissanite comparison is built, build EDU-GEM-01.",
      owns="Moissanite vs diamond.", not_owns="Moissanite vs lab-grown (EDU-GEM-01).")
topic(id="EDU-GEM-03", hub="H-GEM", name="Moissanite explained (what it is, tester results, vs other stones)",
      purpose="Standalone moissanite education.", need="What is moissanite; does it pass a diamond tester?",
      intent="MIXED", evidence="MEDIUM", serp="PARTIAL", existing=NONE_EX, ex_action="NONE",
      page_type="EDUCATION_ARTICLE", separate="DEFERRED",
      reason="CL-090 head 'moissanite' (201,000) is a MIXED SERP led by moissanite retailers plus Wikipedia and AGS; CL-093 tester SERPs are moissanite-specific; CL-096 compares moissanite with other stones. Search volume alone is not a reason to build it (CLAUDE.md rules 3, 8, 9).",
      risk="MEDIUM", dep="HIGH: Stage 12 business question 3 (does HOD sell moissanite?).", status="DEFERRED",
      notes="Stage 11 explicitly did not establish moissanite as a HOD target.", owns="Nothing now.", not_owns="n/a")
topic(id="EDU-GEM-04", hub="H-GEM", name="Coloured & lab-created gemstones (sapphire, emerald, others)",
      purpose="Gemstone education.", need="What is lab-grown sapphire / natural emerald?",
      intent="MIXED", evidence="LOW", serp="PARTIAL", existing=NONE_EX, ex_action="NONE",
      page_type="EDUCATION_ARTICLE", separate="DEFERRED",
      reason="CL-100 to CL-103 are MIXED clusters with 2 validated SERPs (OTHER/MIXED). No evidence HOD sells gemstones (Stage 12 D-16 NOT_PROPOSED for gemstone categories).",
      risk="LOW", dep="HIGH: gemstone catalogue.", status="DEFERRED",
      notes="Revisit only if HOD adds gemstone jewellery.", owns="Nothing now.", not_owns="n/a")

topic(id="EDU-RJG-00", hub="H-RJG", name="Ring & jewellery guides (hub index)",
      purpose="Index of practical guides.", need="Navigation to practical guides.",
      intent="INFORMATIONAL", evidence="LOW", serp="NO", existing=NONE_EX, ex_action="NONE",
      page_type="EDUCATION_TOPIC_HUB_INDEX", separate="YES",
      reason="The practical topics (settings, sizing, care, buying) are dissimilar, so no single topic can double as the landing page. An index page is used instead of a pillar.",
      risk="LOW", dep="None.", status="PROPOSED",
      notes="Must not be thin: it only makes sense once at least two child guides exist (Stage 12 D-13 no empty pages).",
      owns="Navigation to child guides.", not_owns="Any keyword cluster of its own.")
topic(id="EDU-RJG-01", hub="H-RJG", name="Ring settings guide (prong, bezel, halo, pavé and more)",
      purpose="Explain setting types and how to choose.", need="What types of ring settings are there?",
      intent="INFORMATIONAL", evidence="MEDIUM", serp="YES", existing=NONE_EX, ex_action="NONE",
      page_type="EDUCATION_ARTICLE", separate="YES",
      reason="CL-121 validated 'types of diamond settings' (720) is EDITORIAL_GUIDE and shares 0 URLs with the side-stone CATEGORY SERP (REL-050). Education explains styles; commercial style subcategories sell them.",
      risk="LOW", dep="None.", status="PROPOSED",
      notes="Links to engagement-ring style subcategories (Stage 12 D-03; links are Stage 16).",
      owns="Setting types explained.", not_owns="Style shopping pages.")
topic(id="EDU-RJG-02", hub="H-RJG", name="Ring size guide (finding your size, resizing)",
      purpose="Help buyers find and adjust ring size.", need="How do I find my ring size; can a ring be resized?",
      intent="INFORMATIONAL", evidence="INSUFFICIENT_EVIDENCE", serp="NO", existing="Blog: how-to-find-your-ring-size article", ex_action="MOVE_TO_EDUCATION",
      page_type="PRACTICAL_GUIDE", separate="YES",
      reason="Clear business utility (every ring purchase, returns reduction). CL-124 covers resizing and sizing questions ('are mens and womens ring sizes the same' 1,000). Size-finding demand ('ring size', 'ring size chart') is not in the master database, so demand is unmeasured, not absent.",
      risk="LOW", dep="HOD's resizing policy belongs on FAQ/policy pages; this guide explains general resizing.", status="PROPOSED",
      notes="Tool relationship: see EDU-RJG-05. Default is one resource with the sizing tool embedded.",
      owns="Measuring methods, size charts, resizing options.", not_owns="HOD resizing policy (FAQ).")
topic(id="EDU-RJG-03", hub="H-RJG", name="Jewellery care & everyday wear",
      purpose="Care, cleaning, tarnish and everyday-wear questions.", need="Can I shower in it; will it tarnish; how do I care for it?",
      intent="INFORMATIONAL", evidence="LOW", serp="PARTIAL", existing=NONE_EX, ex_action="NONE",
      page_type="PRACTICAL_GUIDE", separate="CONDITIONAL",
      reason="CL-115 has 2 validated EDITORIAL_GUIDE SERPs, but most of its demand is about stainless-steel and gold-plated jewellery, which HOD is not shown to sell. HOD-relevant care queries ('how to clean a diamond ring') are not in the master database.",
      risk="MEDIUM", dep="Care content should match HOD's materials (solid gold, platinum, diamonds).", status="CONDITIONAL",
      notes="The existing Education hub states 'care' in scope (Stage 10). Stage 13 keeps care in Education.",
      owns="Care, cleaning, everyday wear.", not_owns="Rhodium replating detail (EDU-MET-02).")
topic(id="EDU-RJG-04", hub="H-RJG", name="Engagement ring buying guide (incl. buying online)",
      purpose="Guide to buying an engagement ring, including online.", need="How do I buy an engagement ring (online)?",
      intent="COMMERCIAL_RESEARCH", evidence="INSUFFICIENT_EVIDENCE", serp="NO", existing="Blog: how-to-choose-a-lab-grown-diamond-engagement-ring-online article", ex_action="DEFER",
      page_type="BUYING_GUIDE", separate="DEFERRED",
      reason="No keyword or SERP evidence for engagement-ring buying-guide intent (commercial keyword gap, Stage 12 D-19). CL-122 (return an engagement ring, do men get engagement rings, must it be a diamond) is general engagement-ring Q&A that would sit in this guide.",
      risk="INSUFFICIENT_EVIDENCE", dep="D-19 commercial keyword/SERP supplement (UNAPPROVED).", status="DEFERRED",
      notes="Stage 13 DEFER preserved. Whether this merges with EDU-LG-10 or stands alone is decided only after D-19 data.",
      owns="Nothing yet.", not_owns="Stone selection (EDU-LG-10).")
topic(id="EDU-RJG-05", hub="H-RJG", name="Ring size tool (interactive or printable sizer)",
      purpose="Interactive or printable aid to find ring size.", need="Measure my ring size now.",
      intent="INFORMATIONAL", evidence="INSUFFICIENT_EVIDENCE", serp="NO", existing=NONE_EX, ex_action="NONE",
      page_type="TOOL", separate="CONDITIONAL",
      reason="Same searcher need as EDU-RJG-02. Default: embed the tool in the ring size guide so one resource owns 'find my ring size'. A separate tool page only if SERPs for 'ring size chart' / 'ring sizer' show tool pages dominating.",
      risk="MEDIUM", dep="Implementation is out of scope (no Shopify/Hydrogen decision here).", status="CONDITIONAL",
      notes="INSUFFICIENT_EVIDENCE — requires later SERP validation.", owns="The sizing interaction only.", not_owns="Sizing explanation (EDU-RJG-02).")

topic(id="EDU-GEN-01", hub="ROOT", name="Diamond properties: composition, hardness & durability",
      purpose="What diamonds are made of and how tough they are.", need="What are diamonds made of; can a diamond break or scratch?",
      intent="INFORMATIONAL", evidence="LOW", serp="NO", existing=NONE_EX, ex_action="NONE",
      page_type="EDUCATION_ARTICLE", separate="YES",
      reason="CL-080 (composition), CL-081 (melting point), CL-082 (hardness/durability), CL-083 (facts) and CL-087 (cutting a diamond) are one 'diamond as a material' need. No member is validated; one consolidated article at the Education root, no hub.",
      risk="LOW", dep="Commercial relevance is mainly durability (everyday wear; 'are lab-grown diamonds as hard as natural').", status="PROPOSED_PROVISIONAL",
      notes="Stage 11 flagged CL-082 as broad. Science trivia ('diamond lattice', 'is diamond an element') has weak buyer relevance; do not build separate pages for it.",
      owns="Composition, structure, hardness, heat, durability, facts.", not_owns="Formation (EDU-NAT-00); cut optics (EDU-4C-06).")
topic(id="EDU-GEN-02", hub="ROOT", name="Types of diamonds",
      purpose="Overview of diamond 'types' (sense unresolved).", need="What types of diamonds are there?",
      intent="MIXED", evidence="INSUFFICIENT_EVIDENCE", serp="NO", existing=NONE_EX, ex_action="NONE",
      page_type="EDUCATION_ARTICLE", separate="CONDITIONAL",
      reason="CL-065 ('types of diamonds' 6,600) could mean shapes, origins, colours or Type Ia/IIa. REL-053 left the sense unresolved.",
      risk="INSUFFICIENT_EVIDENCE", dep="None.", status="CONDITIONAL",
      notes="INSUFFICIENT_EVIDENCE — requires later SERP validation. If the SERP means shapes, it folds into EDU-SHP-00; if origins, into EDU-LG-00/EDU-NAT-00.",
      owns="TBD by SERP.", not_owns="n/a")

TOPIC_BY_ID = {t["id"]: t for t in T}

# --------------------------------------------------------------------------
# 3. Cluster consolidation (every Stage 11 cluster; exactly one PRIMARY row)
# --------------------------------------------------------------------------
C = []
def cons(cid, role, tid, decision, reason, evidence, risk, notes=""):
    C.append(dict(cid=cid, role=role, tid=tid, decision=decision, reason=reason, evidence=evidence, risk=risk, notes=notes))

N = "NONE"
# Lab-grown
cons("CL-001","PRIMARY",N,"EXCLUDE_NOT_EDUCATION","Head terms ('lab grown diamonds' 135,000; 'lab diamonds' 27,100) return BRAND/CATEGORY retailer SERPs. Owned by the conditional commercial Lab-Grown hub (Stage 12 D-05), not Education.","HIGH","LOW","Education pillar EDU-LG-00 must not target these terms.")
for cid in ["CL-002"]:
    cons(cid,"PRIMARY","EDU-LG-00","DEDICATED_RESOURCE","Definition need; lead cluster of the Lab-Grown pillar.","LOW","MEDIUM","REL-004 DISTINCT_INTENT from CL-001.")
cons("CL-003","PRIMARY","EDU-LG-00","CONSOLIDATE_INTO_TOPIC","Names/terminology is part of 'what is it'; too small and too close to the definition for its own page.","LOW","LOW","'synthetic diamonds' (2,900) is the largest member.")
cons("CL-004","PRIMARY","EDU-LG-00","CONSOLIDATE_INTO_TOPIC","Types of lab-grown diamonds (4 kw) is a section of the definition; method detail links to EDU-LG-03.","LOW","MEDIUM","'types' could be read as CVD/HPHT; the pillar summarises and links.")
cons("CL-005","PRIMARY",N,"EXCLUDE_NOT_EDUCATION","Location modifiers are local/commercial; Stage 12 proposed no location pages.","MEDIUM","LOW")
cons("CL-006","PRIMARY",N,"EXCLUDE_NOT_EDUCATION","Carat-led loose-stone shopping (CATEGORY SERP); commercial, deferred in Stage 12.","MEDIUM","LOW","Carat education is EDU-4C-07.")
cons("CL-007","PRIMARY",N,"EXCLUDE_NOT_EDUCATION","Wholesale/trade is a business question (Stage 12 business question 4).","MEDIUM","LOW")
cons("CL-008","PRIMARY","EDU-LG-05","DEDICATED_RESOURCE","Price/affordability money question; lead cluster of the price, value & resale resource.","LOW","MEDIUM","REL-010 with CL-012.")
cons("CL-009","PRIMARY","EDU-LG-05","CONSOLIDATE_INTO_TOPIC","Value/resale shares the money worry with price (REL-009); one resource.","LOW","MEDIUM")
cons("CL-010","PRIMARY","EDU-LG-01","DEDICATED_RESOURCE","Authenticity is distinct from comparison (REL-020 HIGH: max 2 shared URLs).","MEDIUM","MEDIUM","Existing are-real article is its home (Stage 13).")
cons("CL-011","PRIMARY","EDU-LG-02","DEDICATED_RESOURCE","HIGH-evidence comparison cluster; existing ranking article.","HIGH","MEDIUM","Location retained (HIGH migration risk).")
cons("CL-012","PRIMARY","EDU-LG-06","CONDITIONAL_RESOURCE","Real demand but no SERP; the authenticity SERP already contains a pros/cons page.","LOW","INSUFFICIENT_EVIDENCE","Test against CL-010/CL-011 SERPs.")
cons("CL-012","SECONDARY","EDU-LG-02","CONSOLIDATE_INTO_TOPIC","Interim home: pros/cons section of the lab-vs-natural comparison until the SERP test.","LOW","MEDIUM")
cons("CL-013","PRIMARY","EDU-LG-07","DEDICATED_RESOURCE","Distinct ethics/environment question (REL-012).","LOW","MEDIUM","REL-013 with CL-073.")
cons("CL-014","PRIMARY",N,"EXCLUDE_NOT_EDUCATION","History and market trends are time-bound: Blog is primary (Stage 13 framework).","LOW","LOW","Evergreen history facts appear as a section of EDU-LG-00.")
cons("CL-014","SECONDARY","EDU-LG-00","CONSOLIDATE_INTO_TOPIC","Short evergreen history section only.","LOW","LOW")
cons("CL-015","PRIMARY","EDU-LG-04","CONDITIONAL_RESOURCE","No SERP; process pages rank inside HPHT/CVD SERPs, so a separate page may compete with CVD vs HPHT.","INSUFFICIENT_EVIDENCE","HIGH","3-URL test against CL-016 SERPs decides.")
cons("CL-015","SECONDARY","EDU-LG-00","CONSOLIDATE_INTO_TOPIC","Interim: process summary in the pillar.","LOW","MEDIUM")
cons("CL-015","SECONDARY","EDU-LG-03","CONSOLIDATE_INTO_TOPIC","Interim: method detail in CVD vs HPHT.","LOW","HIGH")
cons("CL-016","PRIMARY","EDU-LG-03","DEDICATED_RESOURCE","Tightest SERP group in the dataset (mean 5.1 shared URLs); HOD's main equity.","HIGH","HIGH","HIGH migration risk; stays at current URL.")
cons("CL-017","PRIMARY","EDU-LG-03","CONSOLIDATE_INTO_TOPIC","HPHT head SERP is led by HPHT-vs-CVD pages (4 of 9) plus a combined GIA page; the comparison article already ranks (pos 49). A separate HPHT page would fragment equity.","HIGH","HIGH","HPHT is SECTION_ONLY. Split rejected now.")
cons("CL-018","PRIMARY","EDU-LG-03","CONSOLIDATE_INTO_TOPIC","Single-method CVD SERPs share 3 to 4 URLs with CVD-vs-HPHT SERPs; HOD ranks for CVD queries on the comparison article.","HIGH","HIGH","CVD is SECTION_ONLY. The 'cvd diamond' head (3,600) is not SERP-validated.")
cons("CL-019","PRIMARY","EDU-LG-08","DEDICATED_RESOURCE","Lab-grown-specific appearance/durability worries not answered by the 4Cs pages.","LOW","MEDIUM")
cons("CL-020","PRIMARY","EDU-LG-09","CONSOLIDATE_INTO_TOPIC","Identification ('can a jeweler tell') is the same detection need as tester results.","LOW","MEDIUM","REL-016.")
cons("CL-021","PRIMARY","EDU-LG-09","DEDICATED_RESOURCE","Largest detection cluster (28 kw); lead cluster.","LOW","MEDIUM","REL-017 with CL-093.")
cons("CL-022","PRIMARY","EDU-LG-09","CONSOLIDATE_INTO_TOPIC","Informational tester-method members only; transactional tester shopping is not HOD's business.","MEDIUM","MEDIUM","3 validated: CATEGORY, OTHER, EDITORIAL_GUIDE.")
cons("CL-023","PRIMARY","EDU-4C-00","CONSOLIDATE_INTO_TOPIC","Lab-grown grade charts are graded on the same scales; integrated into the 4Cs overview instead of a competing lab-grown 4Cs page.","INSUFFICIENT_EVIDENCE","HIGH","HIGH risk would arise only if a separate lab-grown quality page were built.")
cons("CL-023","SECONDARY","EDU-4C-03","CONSOLIDATE_INTO_TOPIC","'vvs lab diamonds' members fit the VVS explainer.","LOW","LOW")
cons("CL-024","PRIMARY","EDU-LG-10","DEDICATED_RESOURCE","Validated EDITORIAL_GUIDE; HOD ranks pos 35.","MEDIUM","MEDIUM","Existing article DEFER (Stage 13).")
cons("CL-026","PRIMARY",N,"EXCLUDE_NOT_EDUCATION","Industry/factory/business terms suit Blog/brand content (Surat manufacturing), not evergreen Education.","LOW","LOW")
cons("CL-026","SECONDARY","EDU-LG-04","CONSOLIDATE_INTO_TOPIC","Possible short manufacturing context if the process page is created.","LOW","LOW")
# Certification
cons("CL-030","PRIMARY","EDU-CERT-01","DEDICATED_RESOURCE","Validated comparison SERP; 0 shared URLs with general certification.","MEDIUM","MEDIUM","Existing Education article (UPDATE_IN_PLACE).")
cons("CL-031","PRIMARY","EDU-CERT-00","CONSOLIDATE_INTO_TOPIC","GIA report questions ('does GIA certify lab-grown') are sections of the certification guide; no SERP for a GIA-only page.","LOW","MEDIUM","REL-024.")
cons("CL-031","SECONDARY","EDU-CERT-01","CONSOLIDATE_INTO_TOPIC","GIA side of the comparison.","LOW","MEDIUM","REL-021.")
cons("CL-032","PRIMARY","EDU-CERT-00","CONSOLIDATE_INTO_TOPIC","IGI report questions are a section of the certification guide (retargeted IGI article).","LOW","MEDIUM","REL-025.")
cons("CL-032","SECONDARY","EDU-CERT-01","CONSOLIDATE_INTO_TOPIC","IGI side of the comparison.","LOW","MEDIUM","REL-022.")
cons("CL-032","SECONDARY","EDU-CERT-03","DEFER","IGI-only page deferred: no IGI SERP evidence.","INSUFFICIENT_EVIDENCE","HIGH")
cons("CL-033","PRIMARY","EDU-CERT-00","DEDICATED_RESOURCE","Validated 'lab-grown diamond certification' EDITORIAL_GUIDE; retarget destination for the IGI blog.","MEDIUM","MEDIUM")
cons("CL-034","PRIMARY","EDU-CERT-02","CONDITIONAL_RESOURCE","Mixed informational and lab-navigation/lookup; only the informational part is Education's.","LOW","MEDIUM","Validated member is a BRAND SERP.")
cons("CL-034","SECONDARY","EDU-CERT-00","CONSOLIDATE_INTO_TOPIC","Interim 'reading your report' section.","LOW","MEDIUM")
# 4Cs
cons("CL-040","PRIMARY","EDU-4C-00","DEDICATED_RESOURCE","Grading scales and charts overview; lead cluster of the 4Cs pillar.","MEDIUM","MEDIUM","Stage 15 flag: clarity-scale keywords go to EDU-4C-01.")
cons("CL-040","SECONDARY","EDU-4C-01","CONSOLIDATE_INTO_TOPIC","'diamond clarity grading scale' SERP is clarity pages.","MEDIUM","MEDIUM")
cons("CL-041","PRIMARY","EDU-4C-02","DEDICATED_RESOURCE","HIGH: 7 shared URLs inside, 0 with the clarity scale.","HIGH","LOW")
cons("CL-042","PRIMARY","EDU-4C-04","CONDITIONAL_RESOURCE","No SERP; grade-page pattern inferred from SI/VVS.","LOW","INSUFFICIENT_EVIDENCE")
cons("CL-042","SECONDARY","EDU-4C-01","CONSOLIDATE_INTO_TOPIC","Interim VS section in the clarity guide.","LOW","MEDIUM")
cons("CL-043","PRIMARY","EDU-4C-03","DEDICATED_RESOURCE","Validated EDITORIAL_GUIDE (18,100); 0 shared with SI2.","MEDIUM","MEDIUM")
cons("CL-044","PRIMARY","EDU-4C-01","CONSOLIDATE_INTO_TOPIC","Grade-vs-grade comparisons consolidate into the clarity guide; grade SERPs already contain comparison pages.","LOW","MEDIUM","No separate comparison pages per grade pair.")
for t in ["EDU-4C-02","EDU-4C-03","EDU-4C-04"]:
    cons("CL-044","SECONDARY",t,"CONSOLIDATE_INTO_TOPIC","Comparison keywords involving this grade may map here in Stage 15.","LOW","MEDIUM")
cons("CL-045","PRIMARY","EDU-4C-01","CONSOLIDATE_INTO_TOPIC","'Best clarity to buy' is the decision part of the clarity guide (REL-032).","LOW","LOW")
cons("CL-046","PRIMARY","EDU-4C-01","CONSOLIDATE_INTO_TOPIC","Inclusions and eye-clean explain the clarity scale (REL-034).","LOW","LOW")
cons("CL-047","PRIMARY","EDU-4C-05","DEDICATED_RESOURCE","Validated EDITORIAL colour guides; 0 shared with clarity scale.","MEDIUM","LOW")
cons("CL-048","PRIMARY","EDU-4C-00","CONSOLIDATE_INTO_TOPIC","Colour+clarity combinations are about how the Cs interact; overview-level.","LOW","LOW","REL-033.")
cons("CL-049","PRIMARY","EDU-4C-07","DEDICATED_RESOURCE","One repeated 'is X carat good/too big' pattern; one guide.","LOW","LOW","No per-carat pages.")
cons("CL-050","PRIMARY","EDU-4C-06","DEDICATED_RESOURCE","Validated 'diamond cut grade' EDITORIAL_GUIDE.","MEDIUM","MEDIUM","Cut grade, not shape.")
cons("CL-051","PRIMARY","EDU-4C-08","CONDITIONAL_RESOURCE","Distinct need; business value depends on fancy-colour offering.","LOW","MEDIUM")
# Shapes
cons("CL-060","PRIMARY","EDU-SHP-00","DEDICATED_RESOURCE","Validated 60,500 EDITORIAL_GUIDE via education paths.","MEDIUM","LOW")
cons("CL-061","PRIMARY","EDU-SHP-00","CONSOLIDATE_INTO_TOPIC","Asscher SERP is inventory-led (1 of 7 education); covered as a shape section.","MEDIUM","MEDIUM","Asscher validated members share 4 URLs with each other, 0 with 'diamond shape'.")
cons("CL-061","SECONDARY","EDU-SHP-01","DEFER","Per-shape page deferred.","MEDIUM","MEDIUM")
cons("CL-062","PRIMARY","EDU-SHP-00","CONSOLIDATE_INTO_TOPIC","Radiant (3 kw, no SERP) covered as a shape section.","LOW","LOW")
cons("CL-062","SECONDARY","EDU-SHP-01","DEFER","Per-shape page deferred.","LOW","LOW")
cons("CL-063","PRIMARY",N,"EXCLUDE_NOT_EDUCATION","PRODUCT SERP; HOD's marquise-oval PDP ranks (pos 90). Commercial.","MEDIUM","LOW","Shape pillar may mention moval shapes.")
cons("CL-064","PRIMARY","EDU-SHP-00","CONSOLIDATE_INTO_TOPIC","Shape choice for engagement rings is blended into the overview SERP (GIA's top result).","MEDIUM","LOW")
cons("CL-065","PRIMARY","EDU-GEN-02","CONDITIONAL_RESOURCE","Sense of 'types of diamonds' unresolved.","INSUFFICIENT_EVIDENCE","INSUFFICIENT_EVIDENCE")
# Natural
cons("CL-070","PRIMARY",N,"EXCLUDE_NOT_EDUCATION","Natural head terms are BRAND/retailer SERPs; commercial natural hub deferred (Stage 12 D-05).","HIGH","LOW")
cons("CL-070","SECONDARY","EDU-NAT-00","CONSOLIDATE_INTO_TOPIC","Informational framing only ('natural untreated diamond').","LOW","LOW")
cons("CL-071","PRIMARY",N,"EXCLUDE_NOT_EDUCATION","Raw/rough diamond SERPs are CATEGORY (rough-diamond sellers).","HIGH","LOW")
cons("CL-071","SECONDARY","EDU-NAT-00","CONSOLIDATE_INTO_TOPIC","'how raw diamond look like' / identification as a section.","LOW","LOW")
cons("CL-073","PRIMARY","EDU-NAT-02","CONDITIONAL_RESOURCE","SERP mostly retailer sourcing-policy pages; needs HOD sourcing policy.","MEDIUM","MEDIUM")
cons("CL-074","PRIMARY","EDU-NAT-00","CONSOLIDATE_INTO_TOPIC","Mining and kimberlite pipes are part of the formation-to-mine story.","LOW","LOW")
cons("CL-075","PRIMARY","EDU-NAT-00","DEDICATED_RESOURCE","'how is diamond formed' (12,100); lead cluster of the natural pillar.","LOW","INSUFFICIENT_EVIDENCE","REL-014 ambiguity with CL-015.")
cons("CL-076","PRIMARY","EDU-NAT-01","CONDITIONAL_RESOURCE","Supply/rarity; modest demand.","LOW","MEDIUM")
# Basics / science
cons("CL-080","PRIMARY","EDU-GEN-01","DEDICATED_RESOURCE","Composition; lead cluster of the diamond-properties article.","LOW","LOW")
cons("CL-081","PRIMARY","EDU-GEN-01","CONSOLIDATE_INTO_TOPIC","Melting point/heat is one material property (REL-061).","LOW","LOW")
cons("CL-082","PRIMARY","EDU-GEN-01","CONSOLIDATE_INTO_TOPIC","Hardness/durability is one material property; the buyer-relevant part.","LOW","LOW","REL-060.")
cons("CL-083","PRIMARY","EDU-GEN-01","CONSOLIDATE_INTO_TOPIC","General facts (3 kw).","LOW","LOW")
cons("CL-084","PRIMARY",N,"EXCLUDE_OFF_SCOPE","Synonyms/thesaurus queries have no jewellery need.","LOW","LOW")
cons("CL-085","PRIMARY","EDU-NAT-01","CONDITIONAL_RESOURCE","General diamond investment; natural-value context (REL-058).","LOW","MEDIUM","No investment advice.")
cons("CL-086","PRIMARY","EDU-LG-05","CONSOLIDATE_INTO_TOPIC","Head terms are lab-grown pawn/sell questions (REL-059).","LOW","MEDIUM","General selling members are a minor part.")
cons("CL-087","PRIMARY","EDU-GEN-01","CONSOLIDATE_INTO_TOPIC","'can water cut diamonds' / recutting are material-property questions.","LOW","LOW")
cons("CL-088","PRIMARY","EDU-4C-06","CONSOLIDATE_INTO_TOPIC","Facets and refraction are the optics behind cut grade.","LOW","LOW")
cons("CL-089","PRIMARY","EDU-LG-08","CONSOLIDATE_INTO_TOPIC","Treatments (irradiation, post-growth) are appearance questions, most relevant to lab-grown.","LOW","LOW")
# Gemstones & alternatives
cons("CL-090","PRIMARY","EDU-GEM-03","DEFER","MIXED retailer-led SERP; business dependency.","MEDIUM","MEDIUM")
cons("CL-091","PRIMARY","EDU-GEM-02","CONDITIONAL_RESOURCE","Validated COMPARISON; 0 shared with CL-092.","MEDIUM","LOW")
cons("CL-092","PRIMARY","EDU-GEM-01","CONDITIONAL_RESOURCE","HIGH-evidence comparison; most business-relevant alternative topic.","HIGH","LOW")
cons("CL-093","PRIMARY","EDU-GEM-03","DEFER","Moissanite tester SERPs are moissanite-specific; deferred with moissanite.","HIGH","MEDIUM","REL-017 with CL-021.")
cons("CL-093","SECONDARY","EDU-LG-09","CONSOLIDATE_INTO_TOPIC","Brief mention in the lab-grown detection page.","LOW","MEDIUM")
cons("CL-094","PRIMARY","EDU-GEM-00","CONSOLIDATE_INTO_TOPIC","CZ is one simulant (REL-035).","LOW","MEDIUM")
cons("CL-095","PRIMARY","EDU-GEM-00","CONDITIONAL_RESOURCE","Simulants overview; lead cluster of the conditional hub pillar.","LOW","MEDIUM")
cons("CL-096","PRIMARY","EDU-GEM-03","DEFER","Moissanite vs other stones (4 kw).","LOW","LOW")
for cid in ["CL-100","CL-101","CL-102","CL-103"]:
    cons(cid,"PRIMARY","EDU-GEM-04","DEFER","Gemstone education depends on a gemstone catalogue (not evidenced).","LOW","LOW")
cons("CL-104","PRIMARY",N,"EXCLUDE_NOT_EDUCATION","Morganite rings: CATEGORY SERP, not in catalogue (Stage 12 NOT_PROPOSED).","MEDIUM","LOW")
cons("CL-105","PRIMARY",N,"EXCLUDE_NOT_EDUCATION","Coloured-gem ring shopping; commercial, not in catalogue.","LOW","LOW")
# Metals
cons("CL-110","PRIMARY","EDU-MET-01","DEDICATED_RESOURCE","HIGH: 4 validated EDITORIAL_GUIDE; 3 rankings.","HIGH","LOW")
cons("CL-111","PRIMARY","EDU-MET-02","CONDITIONAL_RESOURCE","2 validated, mixed page types; depends on white-gold aftercare.","MEDIUM","MEDIUM")
cons("CL-111","SECONDARY","EDU-MET-00","CONSOLIDATE_INTO_TOPIC","Interim white-gold/rhodium section.","MEDIUM","MEDIUM")
cons("CL-112","PRIMARY","EDU-MET-00","DEDICATED_RESOURCE","General metal choice; lead cluster of the metals pillar.","LOW","LOW")
cons("CL-113","PRIMARY","EDU-MET-00","CONSOLIDATE_INTO_TOPIC","Tungsten/titanium: 0 shared URLs with general metals, but no evidence HOD sells them; a section, not a page.","MEDIUM","LOW","Business dependency.")
cons("CL-114","PRIMARY",N,"EXCLUDE_OFF_SCOPE","Novelty/alternative-material ring shopping (hematite, uranium glass) is outside a luxury diamond business.","LOW","LOW")
cons("CL-115","PRIMARY","EDU-RJG-03","CONDITIONAL_RESOURCE","Care/wear questions; most demand is stainless/plated jewellery.","LOW","MEDIUM")
# Ring & jewellery guides
cons("CL-120","PRIMARY",N,"EXCLUDE_NOT_EDUCATION","Side-stone: CATEGORY SERP; confirmed commercial subcategory (Stage 12 D-03).","MEDIUM","LOW")
cons("CL-121","PRIMARY","EDU-RJG-01","DEDICATED_RESOURCE","Validated EDITORIAL_GUIDE; 0 shared with the side-stone SERP.","MEDIUM","LOW")
cons("CL-122","PRIMARY","EDU-RJG-04","DEFER","General engagement-ring Q&A; the buying guide is deferred pending D-19.","LOW","INSUFFICIENT_EVIDENCE")
cons("CL-123","PRIMARY",N,"EXCLUDE_NOT_EDUCATION","Mixed-metal rings: CATEGORY SERP (REL-047).","MEDIUM","LOW")
cons("CL-123","SECONDARY","EDU-MET-00","CONSOLIDATE_INTO_TOPIC","'Mixing metals' advice sits in the metals guide.","LOW","LOW")
cons("CL-124","PRIMARY","EDU-RJG-02","DEDICATED_RESOURCE","Sizing/resizing; business utility; size-finding demand unmeasured.","INSUFFICIENT_EVIDENCE","LOW")
cons("CL-124","SECONDARY","EDU-RJG-05","CONSOLIDATE_INTO_TOPIC","Tool serves the same need.","INSUFFICIENT_EVIDENCE","MEDIUM")
cons("CL-125","PRIMARY",N,"EXCLUDE_NOT_EDUCATION","Stud earrings: mainly commercial ('lab diamond studs' 1,000); earring subcategory is commercial (Stage 12).","LOW","LOW","Stud-setting questions (10 each) may be answered in EDU-RJG-01.")

# --------------------------------------------------------------------------
# 4. Page-type framework
# --------------------------------------------------------------------------
PT = [
 # page_type, system, status, purpose, intent, owns, does_not_own, when_to_use, when_not_to_use, rel_commercial, rel_other, examples, evidence
 ("EDUCATION_HUB","EDUCATION","USED","Root index of all Education hubs and root-level articles.","INFORMATIONAL","Navigation to hubs; Education's overall scope statement.","Any keyword cluster; commercial head terms.","Exactly one.","Never duplicated in Blog.","Links to category hubs where a reader is ready to shop.","Blog hub is a separate system (Stage 12 D-10).","Education root","Stage 12 D-09; existing /education hub."),
 ("EDUCATION_TOPIC_HUB_PILLAR","EDUCATION","USED","Hub landing page that is also the broad definitional resource for its topic.","INFORMATIONAL","The broad 'what is X' need of the hub plus navigation to children.","Narrow child needs that have their own resource.","When the hub's broad question has demand and no child page already owns it.","When the hub's topics are dissimilar (use an index).","Links to the matching commercial hub or category.","FAQ answers link here for depth.","EDU-LG-00, EDU-NAT-00, EDU-4C-00, EDU-SHP-00, EDU-CERT-00, EDU-MET-00, EDU-GEM-00","Avoids a thin hub plus an overview article competing for the same queries (Stage 11 one-need-one-resource)."),
 ("EDUCATION_TOPIC_HUB_INDEX","EDUCATION","USED","Navigation-only hub for dissimilar practical topics.","INFORMATIONAL","Navigation.","Any keyword cluster.","Only when no single topic can represent the hub.","While fewer than two child guides exist (Stage 12 D-13).","Links to relevant categories.","n/a","EDU-RJG-00","Stage 12 D-13 no empty pages."),
 ("EDUCATION_ARTICLE","EDUCATION","USED","Evergreen explainer for one stable question.","INFORMATIONAL","One searcher need.","Comparison or buying-decision intent.","Stable answer, informational SERP.","Dated news (Blog); shopping queries (commercial).","Contextual links to categories.","Blog links in for evergreen explanation.","EDU-LG-01, EDU-4C-01, EDU-GEN-01","Stage 13 framework."),
 ("GRADE_EXPLAINER","EDUCATION","USED","Single-grade explainer (one clarity level).","INFORMATIONAL","One grade and its adjacent comparisons.","The full scale (clarity guide).","Only where a validated SERP shows grade-specific pages distinct from the scale page.","Grades without SERP evidence (stay sections).","Links to products filtered by that grade only if such pages are indexable (Stage 12 gate).","n/a","EDU-4C-02 SI, EDU-4C-03 VVS; EDU-4C-04 VS conditional","Stage 8: SI2 and VVS SERPs share 0 to 1 URLs with the clarity-scale SERP."),
 ("COMPARISON_GUIDE","EDUCATION","USED","X vs Y decision content inside the hub it belongs to.","COMMERCIAL_RESEARCH","The head-to-head comparison.","Single-option explainers.","A validated COMPARISON or editorial SERP for the pair.","Pairs without evidence; pairs Google serves on another page.","Bridges to the category for the chosen option.","n/a","EDU-LG-02, EDU-LG-03, EDU-CERT-01, EDU-MET-01, EDU-GEM-01/02","Stage 12 COMPARISON_GUIDE; Stage 8 COMPARISON SERPs."),
 ("BUYING_GUIDE","EDUCATION","USED","Decision support for choosing within one subject; distributed across hubs, not its own hub.","COMMERCIAL_RESEARCH","How to choose / is it worth it for one subject.","General education; shopping queries.","One guide per distinct buyer decision (Stage 13).","A generic guide duplicating topic hubs.","Primary bridge from Education into categories and products.","Blog gift guides link in.","EDU-LG-10, EDU-LG-06 (conditional), EDU-RJG-04 (deferred)","Stage 13 framework row 13; H-BUY MERGE decision."),
 ("CERTIFICATION_GUIDE","EDUCATION","USED","Explain labs and reports.","INFORMATIONAL","Certification concepts.","Lab report lookup (navigational to labs).","Certification hub pages.","n/a","Product pages show the certificate; the guide explains it.","FAQ states HOD's certificate policy and links here.","EDU-CERT-00, EDU-CERT-02","Stage 12 page type."),
 ("DIAMOND_SHAPE_GUIDE","EDUCATION","USED","Explain and compare shapes.","INFORMATIONAL","Shape comparison and choice.","Shape shopping; cut grade.","Shapes pillar; per-shape only if the SERP is education-led.","Per-shape pages on inventory-led SERPs.","Links to shape filter states / PDPs (Stage 16).","n/a","EDU-SHP-00; EDU-SHP-01 deferred","Stage 8 'diamond shape' vs 'asscher cut diamond'."),
 ("PRACTICAL_GUIDE","EDUCATION","USED","How-to guidance for owning or buying jewellery.","INFORMATIONAL","A practical task (sizing, care).","HOD's policies.","Utility topics with a stable answer.","Policy questions (FAQ/policy pages).","Links to products at the point of need.","FAQ/policy pages hold HOD-specific rules.","EDU-RJG-02, EDU-RJG-03","Stage 13 framework rows 14-15."),
 ("TOOL","EDUCATION","CONDITIONAL","Interactive or printable aid.","INFORMATIONAL","The interaction.","The explanation (lives in the guide).","Embedded in its guide by default; separate only if tool pages dominate the SERP.","Tools without a user need or SERP support.","Tool result links to category/product (e.g. size selection).","n/a","EDU-RJG-05","Stage 12 TOOL type (conditional)."),
 ("SECTION_ONLY","EDUCATION","USED","A concept covered inside a resource, with no page of its own.","n/a","Nothing independently.","n/a","Subordinate concepts and clusters without evidence for a page.","n/a","n/a","n/a","CVD, HPHT, asscher, radiant, rhodium (interim), VS (interim)","Stage 11: a cluster is not a page."),
 ("CALCULATOR_OR_QUIZ","EDUCATION","DEFERRED","Price/carat calculators, shape or style quizzes.","n/a","Nothing now.","n/a","Only with measured demand and a clear business case.","No keyword in the master database supports one.","n/a","n/a","None proposed","No supporting keyword data."),
 ("GLOSSARY","EDUCATION","DEFERRED","A-Z term list.","INFORMATIONAL","Nothing now.","n/a","Only if SERP evidence shows glossary pages win term queries.","Terms answered inside topic resources.","n/a","n/a","None proposed","CL-003/CL-084 terminology is served in the pillar or excluded."),
 ("FAQ_ANSWER","OTHER_SYSTEM","REFERENCE_ONLY","One-line service/policy answer (FAQ system).","INFORMATIONAL (support)","HOD policies (shipping, returns, resizing, certificates supplied).","Full topic treatment.","Service/policy questions.","Topic depth (link to Education).","n/a","Links to the Education owner of each topic (Stage 12 D-18).","FAQ page","Stage 12 D-18; Stage 10 OV-10."),
 ("BLOG_ARTICLE","OTHER_SYSTEM","REFERENCE_ONLY","Time-bound editorial and brand content.","INFORMATIONAL (editorial)","News, trends, craft/Surat stories, launches, gifts, market commentary.","Evergreen reference topics.","Dated or brand topics.","Anything with a stable evergreen answer.","Links to categories and launches.","Links to Education for concepts.","CL-014 history/trends, CL-026 industry","Stage 12 D-10; Stage 13 framework."),
 ("CATEGORY_OR_ORIGIN_HUB","OTHER_SYSTEM","REFERENCE_ONLY","Commercial listing pages (categories, commercial Lab-Grown hub).","TRANSACTIONAL / COMMERCIAL","Shopping queries.","Informational questions.","Retailer/category SERPs.","n/a","n/a","Receives links from Education buying guides and pillars.","CL-001, CL-006, CL-120, CL-123, CL-125","Stage 12 D-05, D-06."),
 ("PRODUCT_DETAIL_PAGE","OTHER_SYSTEM","REFERENCE_ONLY","One sellable product.","TRANSACTIONAL","Product queries.","Education.","PRODUCT SERPs.","n/a","n/a","Shape and 4Cs guides link to relevant PDPs (Stage 16).","CL-063 marquise-oval PDP","Stage 12 D-11."),
]

# --------------------------------------------------------------------------
# 5. Existing content mapping (all 16 Stage 13 rows)
# --------------------------------------------------------------------------
S13 = {r["url"]: r for r in csv.DictReader(open(P("content-strategy/13_existing_content_decisions.csv")))}
S13R = {r["url"]: r for r in csv.DictReader(open(P("content-strategy/13_content_migration_risk.csv")))}
B = "https://www.houseofdiams.com"
EXM = [
 (B+"/blog/cvd-vs-hpht-lab-grown-diamonds-what-buyers-should-know-house-of-diams","H-LG","EDU-LG-03","STAY_AT_CURRENT_URL_EDUCATION_OWNED",
  "Single Education home for CVD vs HPHT, HPHT and CVD (CL-016/017/018). Stays at its current URL; Stage 13 DO_NOT_MOVE_NOW and all 9 conditions preserved.",
  "Stage 13 question answered: CL-017 (HPHT) and CL-018 (CVD) do NOT get their own Education pages now; this article remains the single home and should strengthen its HPHT and CVD sections.",
  "Re-evaluate a CVD-only page only if (a) after the in-place update the CVD single-method queries still do not move and (b) a CVD-head SERP check shows single-method pages dominate. HPHT split not recommended."),
 (B+"/blog/lab-grown-vs-natural-diamonds-the-honest-comparison-house-of-diams","H-LG","EDU-LG-02","STAY_AT_CURRENT_URL_EDUCATION_OWNED",
  "Primary home for CL-011 and interim home for the worth-it pros/cons (CL-012). Stays at its current URL; Stage 13 DO_NOT_MOVE_NOW preserved.",
  "Stage 13 question answered: boundary with the authenticity page is 'which to buy / how they differ' (here) vs 'is it a real diamond' (EDU-LG-01).",
  "Worth-it SERP test may move pros/cons to EDU-LG-06."),
 (B+"/blog/14k-vs-18k-gold-for-diamond-jewellery-which-is-better-house-of-diams","H-MET","EDU-MET-01","MOVE_WHEN_CONDITIONS_MET",
  "Becomes the 14k vs 18k comparison in Metals & Materials.","Destination topic confirmed.","Move only once the Metals section exists (Stage 13 conditions)."),
 (B+"/blog/how-to-choose-a-lab-grown-diamond-the-complete-buyer-s-guide","H-LG","EDU-LG-10","DEFERRED",
  "Intended destination: Lab-Grown buying guide (EDU-LG-10). Migration stays deferred (Stage 13).",
  "Topic confirmed in Stage 14; relationship with the online engagement-ring guide still unresolved.","D-19 supplement (unapproved) for engagement-ring buying-guide SERPs; presumed survivor if consolidated."),
 (B+"/blog/are-lab-grown-diamonds-real-a-complete-buyer-s-guide","H-LG","EDU-LG-01","MOVE_WHEN_CONDITIONS_MET",
  "Becomes the authenticity resource (CL-010).","Stage 13 question answered: scope is authenticity only; pricing (CL-008) goes to EDU-LG-05; comparison stays with EDU-LG-02.",
  "Lab-Grown Education hub must exist first (Stage 13 conditions)."),
 (B+"/blog/the-4cs-of-lab-grown-diamonds-explained-cut-colour-clarity-and-carat-house-of-diams","H-4C","EDU-4C-00","MOVE_WHEN_CONDITIONS_MET",
  "Becomes the 4Cs overview pillar (general 4Cs with a lab-grown grading section).",
  "Stage 13 question answered: general 4Cs overview (CL-040 + CL-023 integrated), not a lab-grown-only page; the 4Cs become a pillar plus single-C guides.",
  "Diamond Quality hub must exist first; single-C guides are new content."),
 (B+"/blog/how-to-choose-a-lab-grown-diamond-engagement-ring-online-house-of-diams","H-RJG","EDU-RJG-04","DEFERRED",
  "Intended destination: engagement-ring buying guide (EDU-RJG-04), itself deferred.","No change from Stage 13: merge vs separate still undecided.","D-19 supplement (unapproved)."),
 (B+"/blog/the-best-lab-grown-diamond-shapes-for-engagement-rings-house-of-diams","H-SHP","EDU-SHP-00","MOVE_WHEN_CONDITIONS_MET",
  "Becomes the diamond shapes pillar (overview incl. engagement-ring shape choice).",
  "Stage 13 question answered: overview (CL-060) with CL-064 shape choice consolidated; no per-shape pages now.","Shapes hub must exist first."),
 (B+"/blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-house-of-diams","H-RJG","EDU-RJG-02","MOVE_WHEN_CONDITIONS_MET",
  "Becomes the ring size guide; tool embedded by default (EDU-RJG-05 conditional).",
  "Stage 13 question answered: article is the primary resource; a tool is embedded, a separate tool page is conditional.","Size-finding demand unmeasured."),
 (B+"/blog/igi-certification-for-lab-grown-diamonds-what-it-means-house-of-diams","H-CERT","EDU-CERT-00","RETARGET_THEN_MOVE_WHEN_CONDITIONS_MET",
  "Retargeted to general lab-grown certification (CL-033) and becomes the Certification pillar; IGI and GIA report questions are sections.",
  "Stage 13 question answered: retarget to CL-033, not CL-032 (only CL-033 has SERP evidence).","Must ship with the GIA-vs-IGI narrowing (Stage 13)."),
 (B+"/education/lab-grown-diamond-certification-explained-gia-vs-igi-house-of-diams","H-CERT","EDU-CERT-01","ALREADY_IN_EDUCATION_UPDATE_IN_PLACE",
  "GIA vs IGI comparison (CL-030); narrowed to the comparison intent.","Unchanged from Stage 13.","Slug clean-up is a Stage 15 question."),
 (B+"/blog","NONE","NONE","NOT_EDUCATION",
  "Blog hub: time-bound editorial system (Stage 13 KEEP_BLOG). Not an Education destination.","n/a","Stage 13 open question on listing Education-owned /blog articles is a UX choice."),
 (B+"/education","ROOT","EDU-ROOT","EDUCATION_ROOT",
  "Existing Education hub becomes the Education root index for the 8 hubs and root-level articles.","Structure defined in Stage 14.","Its stated 'craftsmanship' scope moves to Blog/brand (Stage 13)."),
 (B+"/faq","NONE","NONE","NOT_EDUCATION",
  "FAQ keeps service/policy answers and one-line topic answers that point to the Education owner (Stage 12 D-18).","Owners now named: EDU-LG-01 (legitimacy), EDU-LG-02 (lab vs natural), EDU-CERT-00/01 (certification).","Stage 15/16."),
 (B+"/shop/oval-floral-diamond-ring","NONE","NONE","NOT_EDUCATION",
  "Commercial PDP; CL-063 excluded from Education.","n/a","Shapes pillar may link to it (Stage 16)."),
 (B+"/engagement-rings/by-desgin/side-stone-rings","NONE","NONE","NOT_EDUCATION",
  "Commercial subcategory; CL-120 excluded. Ring settings guide (EDU-RJG-01) explains styles.","n/a","Stage 15 URL question (Stage 13)."),
]

# --------------------------------------------------------------------------
# Writers
# --------------------------------------------------------------------------
def w(path, header, rows):
    with open(P(path), "w", newline="") as f:
        wr = csv.writer(f); wr.writerow(header); wr.writerows(rows)
    print(f"wrote {path} ({len(rows)} rows)")

def serp_ev(cid):
    r = REG[cid]
    n = r["validated_keyword_count"]
    return f"{n} validated kw; page types: {r['stage8_dominant_page_types']}; Stage 11 evidence {r['evidence_level']}"

def exist_ev(cid):
    r = REG[cid]
    rk = r["current_HOD_ranking_keyword_count"]
    return f"{r['existing_content_relationship']}; Stage 3 rankings: {rk}"

# consolidation
rows = []
for c in C:
    r = REG[c["cid"]]
    tname = TOPIC_BY_ID[c["tid"]]["name"] if c["tid"] != "NONE" else "NONE (not an Education topic)"
    rows.append([c["cid"], r["cluster_name"], c["role"], c["tid"], tname, c["decision"], c["reason"],
                 c["evidence"], serp_ev(c["cid"]), exist_ev(c["cid"]), c["risk"], c["notes"]])
w("architecture/14_education_cluster_consolidation.csv",
  ["cluster_id","cluster_name","assignment_role","education_topic_id","education_topic","decision","reason",
   "evidence_level","serp_evidence","existing_content","cannibalization_risk","notes"], rows)

# topic inventory
rows = []
for t in T:
    prim = [c["cid"] for c in C if c["tid"] == t["id"] and c["role"] == "PRIMARY"]
    sec = [c["cid"] for c in C if c["tid"] == t["id"] and c["role"] == "SECONDARY"]
    ids = "; ".join(prim) + (("; " if prim else "") + "secondary: " + ", ".join(sec) if sec else "")
    hubname = HUB_BY_ID[t["hub"]][1] if t["hub"] != "ROOT" else "Education root (no hub)"
    rows.append([t["id"], hubname, t["name"], t["purpose"], t["need"], ids or "none", len(prim), t["intent"],
                 t["evidence"], t["serp"], t["existing"], t["ex_action"], t["page_type"], t["separate"],
                 t["reason"], t["risk"], t["dep"], t["status"], t["notes"]])
w("architecture/14_education_architecture.csv",
  ["topic_id","education_hub","topic_name","topic_purpose","primary_searcher_need","relevant_cluster_ids","cluster_count",
   "primary_intent","evidence_level","SERP_validation_available","existing_HOD_content","existing_content_action",
   "proposed_page_type","separate_page_required","consolidation_reason","cannibalization_risk","business_dependency",
   "architecture_status","notes"], rows)

# hierarchy
rows = []
rows.append(["H-00","L0","","ROOT","Education","","EDUCATION_HUB","n/a",
             "Single evergreen home for reference and buying-decision content (Stage 12 D-09).",
             "Find trustworthy diamond and jewellery knowledge before and after buying.",
             "All evergreen informational and comparison topics listed below.",
             "Shopping queries (commercial system), dated editorial (Blog), service/policy answers (FAQ).",
             "Education","HIGH","PROPOSED"])
for h in HUBS:
    hid, name, dec, pillar, why, need, owns, notown, ev, status = h
    rows.append([hid,"L1","H-00","HUB",name,pillar,
                 "EDUCATION_TOPIC_HUB_PILLAR" if pillar and hid != "H-RJG" else ("EDUCATION_TOPIC_HUB_INDEX" if hid == "H-RJG" else "n/a"),
                 dec, why, need, owns, notown, f"Education > {name}", ev, status])
sec_nodes = {"EDU-LG-03": [("SECTION","HPHT explained","HPHT growth method (CL-017) as a section, not a page."),
                           ("SECTION","CVD explained","CVD growth method (CL-018) as a section, not a page.")],
             "EDU-SHP-00": [("SECTION","Per-shape sections (asscher, radiant, oval, emerald, others)","Shapes covered inside the pillar until per-shape SERPs justify pages.")],
             "EDU-4C-01": [("SECTION","VS clarity (interim)","Interim home for CL-042 until EDU-4C-04 is justified.")]}
n = 0
for t in T:
    parent = t["hub"] if t["hub"] != "ROOT" else "H-00"
    pname = HUB_BY_ID[t["hub"]][1] if t["hub"] != "ROOT" else None
    is_pillar = t["hub"] != "ROOT" and HUB_BY_ID[t["hub"]][3] == t["id"]
    lvl = "L1" if is_pillar else "L2"
    hid = "N-" + t["id"][4:]
    path = f"Education > {pname} > {t['name']}" if pname else f"Education > {t['name']}"
    if is_pillar:
        path = f"Education > {pname} (hub landing)"
        lvl = "L1_PILLAR"
    rows.append([hid, lvl, parent, "TOPIC", t["name"], t["id"], t["page_type"], "n/a",
                 t["reason"], t["need"], t["owns"], t["not_owns"], path, t["evidence"], t["status"]])
    for i, (nt, nm, why) in enumerate(sec_nodes.get(t["id"], []), 1):
        rows.append([f"{hid}-S{i}", "L3", hid, nt, nm, t["id"], "SECTION_ONLY", "n/a", why, "Answered inside the parent resource.",
                     nm, "A separate page.", f"{path} > {nm}", t["evidence"], "PROPOSED"])
w("architecture/14_education_hierarchy.csv",
  ["hierarchy_id","level","parent_id","node_type","node_name","topic_or_pillar_id","page_type","hub_decision",
   "why_it_exists","searcher_need","owns","does_not_own","conceptual_path_not_a_url","evidence_level","status"], rows)

# page types
w("architecture/14_education_page_type_framework.csv",
  ["page_type","system","status","purpose","primary_intent","owns","does_not_own","when_to_use","when_not_to_use",
   "relationship_to_commercial","relationship_to_blog_faq_tools","examples_in_stage14","evidence"], PT)

# existing content mapping
rows = []
for url, hub, tid, mstat, role, s13q, dep in EXM:
    d = S13[url]; rk = S13R[url]
    hubname = HUB_BY_ID[hub][1] if hub in HUB_BY_ID else ("Education root" if hub == "ROOT" else "NONE")
    tname = TOPIC_BY_ID[tid]["name"] if tid in TOPIC_BY_ID else ("Education root index" if tid == "EDU-ROOT" else "NONE")
    rows.append([url, d["title"], d["content_type"], d["action"], d["migration_risk"], rk["decision"], d["ranking_keyword_count"],
                 hubname, tid, tname, mstat, role, s13q, dep])
w("content-strategy/14_education_existing_content_mapping.csv",
  ["existing_url","title","content_type","stage13_action","stage13_migration_risk","stage13_migration_decision",
   "stage3_ranking_keywords","education_hub","education_topic_id","education_topic","stage14_migration_status",
   "intended_role","stage13_question_resolution","open_dependency"], rows)

# upstream checksums for QC (files Stage 14 must not modify)
up = sorted(glob.glob(P("clusters/*.csv")) + glob.glob(P("clusters/*.md")) + glob.glob(P("architecture/12_*")) +
            glob.glob(P("content-strategy/10_*")) + glob.glob(P("content-strategy/13_*")) +
            glob.glob(P("serp/analysis/*")) + glob.glob(P("dataforseo/processed/07_*")) +
            glob.glob(P("site/**/*"), recursive=True) + glob.glob(P("dataforseo/raw/*")))
cs = {os.path.relpath(f, ROOT): hashlib.sha256(open(f, "rb").read()).hexdigest() for f in up if os.path.isfile(f)}
json.dump(cs, open(P("architecture/scripts/14_upstream_checksums.json"), "w"), indent=1)
print(f"recorded {len(cs)} upstream checksums")
