#!/usr/bin/env python3
"""Stage 19 — content briefs & final content architecture.

Local build only: reads Stage 10–18.5 outputs and writes the Stage 19 brief files.
No API call, no live-site request, no change to any upstream file.

Page outlines are hand-authored below (OUTLINES). Everything else (concepts, questions,
entities, boundaries, links, business facts, evidence refs) is pulled from the upstream files
so every brief row traces back to Stage 15/16/17/18/18.5 evidence.
"""
import csv
import json
import os
import re
from collections import defaultdict, OrderedDict

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
P = lambda *a: os.path.join(BASE, *a)
rd = lambda p: list(csv.DictReader(open(P(p), newline='', encoding='utf-8')))
OUT = P('content-strategy')

# ------------------------------------------------------------------ inputs
REG15 = rd('architecture/15_target_page_registry.csv')
TARGETS = [r['target_id'] for r in REG15]
REG = {r['target_id']: r for r in REG15}
GAPS = rd('content-strategy/18_semantic_gap_register.csv')
GAP = {g['gap_id']: g for g in GAPS}
QCOV = rd('content-strategy/18_question_coverage.csv')
ENT = rd('content-strategy/18_entity_coverage.csv')
XOWN = rd('content-strategy/18_cross_page_semantic_ownership.csv')
PAT = rd('content-strategy/18_serp_semantic_patterns.csv')
V185 = rd('serp/analysis/18_5_targeted_serp_validation.csv')
CH = rd('serp/analysis/18_5_stage18_change_log.csv')
L16 = rd('architecture/16_internal_link_map.csv')
ANCH = rd('architecture/16_anchor_strategy.csv')
EQ = rd('content-strategy/15_ranking_equity_protection.csv')
TI = {r['target_page_id']: r for r in rd('content-strategy/17_topic_intelligence.csv')}
DD = rd('content-strategy/17_keyword_deep_dive.csv')
KMAP = rd('architecture/15_keyword_url_map.csv')
INV = {r['url'].replace('https://www.houseofdiams.com', ''): r for r in rd('content-strategy/10_existing_content_inventory.csv')}

CONTEXTUAL = {'CONTEXTUAL', 'RELATED_CONTENT', 'EDITORIAL', 'EDUCATIONAL_CTA', 'COMMERCIAL_CTA', 'PRODUCT_RECOMMENDATION'}
SEV_ORDER = ['CRITICAL_COVERAGE', 'IMPORTANT_COVERAGE', 'SUPPORTING_COVERAGE', 'OPTIONAL_CONTEXT', 'BUSINESS_DEPENDENT', 'INSUFFICIENT_EVIDENCE']
SEV_SHORT = {'CRITICAL_COVERAGE': 'CRITICAL', 'IMPORTANT_COVERAGE': 'IMPORTANT', 'SUPPORTING_COVERAGE': 'SUPPORTING',
             'OPTIONAL_CONTEXT': 'OPTIONAL', 'BUSINESS_DEPENDENT': 'BUSINESS_DEPENDENT', 'INSUFFICIENT_EVIDENCE': 'INSUFFICIENT_EVIDENCE'}
WMAP = {'CRITICAL': 'CRITICAL_COVERAGE', 'IMPORTANT': 'IMPORTANT_COVERAGE', 'SUPPORTING': 'SUPPORTING_COVERAGE', 'OPTIONAL': 'OPTIONAL_CONTEXT'}

# ---- 18.5 change log: row ids and effective severity
CLID = {}
EFF = {g['gap_id']: g['gap_severity'] for g in GAPS}
EFF_NOTE = {}
for i, r in enumerate(CH, 1):
    cid = f'CL185-{i:03d}'
    r['_id'] = cid
    CLID[cid] = r
    gid = r['affected_gap_id'] if r['affected_gap_id'].startswith('G18-') else None
    m = re.search(r'Implied weight\s*([A-Z]*)\s*->\s*([A-Z]+)', r['notes'])
    if gid and m and m.group(2) in WMAP:
        EFF[gid] = WMAP[m.group(2)]
        EFF_NOTE[gid] = f"{cid}: {SEV_SHORT[GAP[gid]['gap_severity']]} -> {m.group(2)} ({r['change_type']})"
CL_BY_GAP = defaultdict(list)
for r in CH:
    if r['affected_gap_id'].startswith('G18-'):
        CL_BY_GAP[r['affected_gap_id']].append(r['_id'])
V185_BY_KW = {r['keyword']: r for r in V185}
V185_TARGET = {}
for r in CH:
    V185_TARGET.setdefault(r['keyword'], r['affected_target_id'])
V185_TARGET['ring size chart'] = V185_TARGET['how to measure ring size'] = 'EDU-RJG-02'

# ---- Stage 18 question ids
for i, q in enumerate(QCOV, 1):
    q['_id'] = f'Q18-{i:03d}'

# ------------------------------------------------------------------ page-level briefs (hand-authored)
# depth: Essential / Moderate / Comprehensive. journey: DISCOVER UNDERSTAND COMPARE EVALUATE VERIFY DECIDE BUY
PAGES = {
 'EDU-LG-00': dict(need='The user is trying to understand what a lab-grown diamond is, what it is also called, how it is made and where to go next for authenticity, comparison, price or buying detail.',
   journey='DISCOVER; UNDERSTAND', depth='Comprehensive', sec_intent='INFORMATIONAL (process overview; routing to comparison and buying guides)',
   h1='Definition-led pillar H1 naming lab-grown diamonds as the topic (Education framing, not a shop head term).',
   serp='DEFINITION_BLOCK; TYPE_LIST (growth methods); short comparison summary; hub topic list', home='S07'),
 'EDU-LG-01': dict(need='The user is trying to find out whether a lab-grown diamond is a real diamond or a fake, and what makes it real.',
   journey='UNDERSTAND; VERIFY', depth='Moderate', sec_intent='COMMERCIAL_RESEARCH (the SERP is comparison-led)',
   h1='Question-led H1 that keeps the existing "are lab-grown diamonds real" intent (existing H1 already matches).',
   serp='Answer-first direct answer; short simulant distinction; comparison-led SERP handled by brief summary + link', home='S06'),
 'EDU-LG-02': dict(need='The user is trying to decide between a lab-grown and a natural diamond by comparing what is the same, what differs and which suits their priorities.',
   journey='COMPARE; EVALUATE; DECIDE', depth='Comprehensive', sec_intent='INFORMATIONAL (differences, perception questions)',
   h1='Comparison H1 keeping the existing "lab-grown vs natural" framing (existing H1 already matches).',
   serp='Answer-first summary; COMPARISON_TABLE; PROS_CONS; decision framing; FAQ', home='S09'),
 'EDU-LG-03': dict(need='The user is trying to understand the two lab-grown growth methods (CVD and HPHT), how they differ and whether the method matters when buying.',
   journey='UNDERSTAND; COMPARE; EVALUATE', depth='Comprehensive', sec_intent='COMMERCIAL_RESEARCH (which method is better / worth buying)',
   h1='Comparison H1 keeping the existing CVD vs HPHT framing (existing H1 already matches; keep the ranking URL).',
   serp='DEFINITION_FIRST; COMPARISON_TABLE; PROCESS_EXPLAINER per method; answer to "which is better"; FAQ', home='S10'),
 'EDU-LG-05': dict(need='The user is trying to understand why lab-grown diamonds cost less, whether they hold value or can be resold, and whether they are an investment.',
   journey='EVALUATE; DECIDE', depth='Moderate', sec_intent='COMMERCIAL_RESEARCH (price and resale expectations before buying)',
   h1='Question-led H1 covering price and value retention together (co-primary questions).',
   serp='DEFINITION_BLOCK (direct "No" answer); worked calculation (absolute vs percentage loss); PROS_CONS; FAQ', home='S03'),
 'EDU-LG-07': dict(need='The user is trying to judge whether lab-grown diamonds are genuinely more ethical and better for the environment, including the caveats.',
   journey='EVALUATE; VERIFY', depth='Moderate', sec_intent='COMMERCIAL_RESEARCH (how to buy responsibly)',
   h1='Question-led H1 on whether lab-grown diamonds are ethical (qualified answer, not a claim).',
   serp='DEFINITION_BLOCK (qualified yes); PROS_CONS (benefits vs concerns); buying checklist', home='S02'),
 'EDU-LG-08': dict(need='The user is trying to find out whether a lab-grown diamond will get cloudy, fade, lose sparkle or show fluorescence over time, and how to keep it looking its best.',
   journey='EVALUATE; VERIFY', depth='Moderate', sec_intent='INFORMATIONAL (care and maintenance)',
   h1='Question-led H1 on whether lab-grown diamonds get cloudy or change over time.',
   serp='DEFINITION_BLOCK (direct "No"); TYPE_LIST (causes of a cloudy look); STEP_SEQUENCE (cleaning)', home='S04'),
 'EDU-LG-09': dict(need='The user is trying to learn whether a lab-grown diamond passes a diamond tester and how jewellers and labs actually tell lab-grown from natural.',
   journey='VERIFY', depth='Moderate', sec_intent='INFORMATIONAL (how testers work; where to test)',
   h1='Question-led H1 on whether lab-grown diamonds pass a diamond tester.',
   serp='Answer-first; TYPE_LIST + PROCESS_EXPLAINER (tester types); FAQ', home='S05'),
 'EDU-LG-10': dict(need='The user is trying to choose a lab-grown diamond step by step: which 4Cs to prioritise, what report to insist on and how to set a budget.',
   journey='EVALUATE; DECIDE; BUY', depth='Moderate', sec_intent='INFORMATIONAL (buying considerations)',
   h1='How-to H1 keeping the existing "how to choose a lab-grown diamond" intent (existing H1 already matches).',
   serp='STEP_SEQUENCE; BUYING_CONSIDERATIONS; FAQ', home='S07'),
 'EDU-NAT-00': dict(need='The user is trying to understand how natural diamonds form in the Earth, how they reach the surface and how they become jewellery.',
   journey='DISCOVER; UNDERSTAND', depth='Moderate', sec_intent='INFORMATIONAL (sources, mining, myths)',
   h1='Process-led H1 on how natural diamonds are formed (Education framing; commercial natural hub deferred).',
   serp='STEP_SEQUENCE / process explainer; short natural-vs-lab formation comparison; FAQ', home='S07'),
 'EDU-4C-00': dict(need='The user is trying to understand the 4Cs (cut, colour, clarity, carat), how each is graded and which C matters most for their budget.',
   journey='DISCOVER; UNDERSTAND; EVALUATE', depth='Comprehensive', sec_intent='COMMERCIAL_RESEARCH (which C to prioritise)',
   h1='Definition-led 4Cs H1; the existing lab-grown framing may stay as a subtitle angle, not the whole page.',
   serp='DEFINITION_BLOCK; one block per C (meaning + grade range); VISUAL_CHART; order-of-importance', home='S07'),
 'EDU-4C-01': dict(need='The user is trying to understand the clarity scale, what inclusions are, and which clarity grade is eye-clean and good value.',
   journey='UNDERSTAND; COMPARE; EVALUATE', depth='Moderate', sec_intent='COMMERCIAL_RESEARCH (best-value clarity)',
   h1='Clarity-guide H1 (scale + choosing a grade).',
   serp='GRADE_SCALE + VISUAL_CHART; PROS_CONS; COMPARISON_TABLE (grade vs grade); buying considerations', home='S06'),
 'EDU-4C-02': dict(need='The user is trying to find out what SI1/SI2 clarity means and whether an SI diamond is a good, eye-clean buy.',
   journey='UNDERSTAND; EVALUATE', depth='Essential', sec_intent='COMMERCIAL_RESEARCH (is SI good value)',
   h1='Grade-explainer H1 on SI clarity diamonds.',
   serp='DEFINITION_FIRST; PROS_CONS; buying tips (STEP_SEQUENCE); FAQ', home='S04'),
 'EDU-4C-03': dict(need='The user is trying to understand what VVS, IF and FL mean and whether paying for them is worth it.',
   journey='UNDERSTAND; EVALUATE', depth='Essential', sec_intent='COMMERCIAL_RESEARCH (is VVS worth it)',
   h1='Grade-explainer H1 on VVS and flawless clarity.',
   serp='DEFINITION_FIRST; grade comparison; FAQ', home='S04'),
 'EDU-4C-05': dict(need='The user is trying to read the D-to-Z colour scale and choose a colour grade that looks white for their budget and metal.',
   journey='UNDERSTAND; COMPARE; EVALUATE', depth='Moderate', sec_intent='INFORMATIONAL (colour chart)',
   h1='Colour-guide H1 (D-to-Z scale and choosing a grade).',
   serp='VISUAL_CHART; TYPE_LIST (five grade groups with appearance + value); COMPARISON_TABLE; metal pairing', home='S06'),
 'EDU-4C-06': dict(need='The user is trying to understand what diamond cut means (light performance, not shape), how cut is graded and whether cut matters.',
   journey='UNDERSTAND; COMPARE; EVALUATE', depth='Moderate', sec_intent='COMMERCIAL_RESEARCH (best cut for sparkle)',
   h1='Cut-guide H1 that signals cut quality (the head term is mixed with shape intent).',
   serp='DEFINITION_BLOCK; cut vs shape comparison; GRADE_SCALE + VISUAL_CHART; TYPE_LIST (quality factors)', home='S02'),
 'EDU-4C-07': dict(need='The user is trying to understand what carat weight means, how big a given carat looks in millimetres and on the hand, and whether a size is "good".',
   journey='UNDERSTAND; EVALUATE', depth='Moderate', sec_intent='COMMERCIAL_RESEARCH (size for budget)',
   h1='Carat-guide H1 (weight vs size, size chart).',
   serp='VISUAL_CHART (carat to mm by shape; image-led SERP, no AI Overview); on-hand comparison; PAA', home='S04'),
 'EDU-SHP-00': dict(need='The user is trying to see the main diamond shapes, what distinguishes each, and which shape suits their engagement ring and budget.',
   journey='DISCOVER; COMPARE; EVALUATE; DECIDE', depth='Comprehensive', sec_intent='COMMERCIAL_RESEARCH (choosing a shape for an engagement ring)',
   h1='Shapes-guide H1; the existing engagement-ring shape angle is kept as a core section.',
   serp='TYPE_LIST (10 shapes, one trait each); VISUAL_CHART (shape chart with pictures); COMPARISON_TABLE; FAQ', home='S05'),
 'EDU-CERT-00': dict(need='The user is trying to understand what a diamond certificate (grading report) is, who issues it, what it contains and how to verify one.',
   journey='UNDERSTAND; VERIFY', depth='Comprehensive', sec_intent='NAVIGATIONAL (lab look-ups: IGI/GIA sites rank at the top)',
   h1='Certification-hub H1 broader than the current IGI-only title (Stage 15 EXISTING_RETARGET_THEN_MOVE).',
   serp='DEFINITION_BLOCK; TYPE_LIST (what is included; top labs); STEP_SEQUENCE (check / look-up); FAQ', home='S03'),
 'EDU-CERT-01': dict(need='The user is trying to decide whether a GIA or an IGI report matters more for a lab-grown diamond, and why they differ in price.',
   journey='COMPARE; EVALUATE; DECIDE', depth='Moderate', sec_intent='INFORMATIONAL (how each lab grades lab-grown)',
   h1='Comparison H1 keeping the existing GIA vs IGI framing (existing URL stays).',
   serp='COMPARISON_STRUCTURE (side-by-side table); BUYING_CONSIDERATIONS; FAQ', home='S07'),
 'EDU-MET-00': dict(need='The user is trying to compare jewellery metals (gold colours and karats, platinum, silver, alternative metals) and pick the best one for a ring or band.',
   journey='DISCOVER; COMPARE; EVALUATE; DECIDE', depth='Comprehensive', sec_intent='COMMERCIAL_RESEARCH (best metal for rings; white gold vs platinum)',
   h1='Metals-guide H1 (types of jewellery metals and choosing one).',
   serp='TYPE_LIST; COMPARISON_TABLE (white gold vs platinum); PROS_CONS; FAQ', home='S07'),
 'EDU-MET-01': dict(need='The user is trying to decide between 14k and 18k gold (and where 10k fits) for jewellery they will wear, weighing purity, colour, durability and price.',
   journey='COMPARE; EVALUATE; DECIDE', depth='Moderate', sec_intent='INFORMATIONAL (what karat means; karat vs carat)',
   h1='Comparison H1 keeping the existing 14k vs 18k framing (existing URL stays until Stage 15 conditions are met).',
   serp='COMPARISON_TABLE (purity, colour, durability, price/value, hypoallergenic); PROS_CONS; FAQ', home='S09'),
 'EDU-RJG-01': dict(need='The user is trying to understand the main ring setting types and choose one that balances sparkle, security and lifestyle.',
   journey='DISCOVER; COMPARE; EVALUATE', depth='Moderate', sec_intent='TRANSACTIONAL signals on the engagement-ring head term (OWNERSHIP_REVIEW_REQUIRED)',
   h1='Informational settings-guide H1 (types of settings); do not frame as a shop page while ownership review is open.',
   serp='TYPE_LIST (setting types); VISUAL_CHART (settings chart); lifestyle trade-off; FAQ', home='S07'),
 'EDU-RJG-02': dict(need='The user is trying to find their ring size at home: read a size chart, measure accurately, convert between systems and understand resizing limits.',
   journey='VERIFY; DECIDE; BUY', depth='Moderate', sec_intent='TRANSACTIONAL support (size needed to order)',
   h1='Practical H1 on finding your ring size (existing H1 already matches).',
   serp='VISUAL_CHART / table (US size, inner circumference mm, inner diameter mm); STEP_SEQUENCE (numbered); printable / virtual sizer', home='S08'),
 'EDU-GEN-01': dict(need='The user is trying to learn what diamonds are made of and how hard and durable they really are.',
   journey='DISCOVER; UNDERSTAND', depth='Moderate', sec_intent='INFORMATIONAL (everyday durability)',
   h1='Definition-led H1 on what diamonds are made of and their properties.',
   serp='DEFINITION_BLOCK; COMPARISON (diamond vs graphite / other carbon forms); FAQ', home='S07'),
 'COM-ER-SIDESTONE': dict(need='The user is trying to browse and buy a side-stone engagement ring and understand the style options before choosing.',
   journey='EVALUATE; DECIDE; BUY', depth='Essential', sec_intent='COMMERCIAL_RESEARCH (benefits and styles of side stones)',
   h1='Category H1 for side-stone engagement rings (category naming; URL and "by-desgin" path unchanged).',
   serp='CATEGORY (product grid) with PROS_CONS + TYPE_LIST + buying considerations in AI Overview', home='S04'),
 'COM-PDP-OVAL-FLORAL': dict(need='The user is trying to evaluate and buy this specific oval ring with marquise side stones.',
   journey='EVALUATE; BUY', depth='Essential', sec_intent='COMMERCIAL_RESEARCH (oval vs marquise shape questions)',
   h1='Product-name H1 (current product title already names oval + marquise side stones).',
   serp='PRODUCT (images, shopping); PAA on shape price', home='S03'),
}


def S(sid, lvl, heading, purpose, fmt, gaps=(), cl=(), q=None, cmp='', note='', imp=None, v=None, links=(), add='', aeo=''):
    return dict(sid=sid, lvl=lvl, heading=heading, purpose=purpose, fmt=fmt, gaps=[f'G18-{g:04d}' for g in gaps],
                cl=[f'CL185-{c:03d}' for c in cl], q=q, cmp=cmp, note=note, imp=imp, v=v or [], links=list(links), add=add, aeo=aeo)


# Outline per target. Headings are working headings (not final SEO titles).
OUTLINES = {
 'EDU-LG-00': [
  S('S01', 'H1', 'What is a lab-grown diamond? (working H1 + answer-first definition)', 'Open with a concise direct answer defining a lab-grown diamond, then state composition and origin in one or two lines.',
    'DEFINITION_BLOCK', [1, 282, 296], [1, 2, 3], v=['what are lab grown diamonds'], imp='CRITICAL',
    aeo='Answer-first definition; the 18.5 AI Overview opens with a one-sentence definition and 5 of 6 organic snippets define the term.'),
  S('S02', 'H2', 'Other names for lab-grown diamonds', 'List the equivalent names (synthetic, lab-created, man-made, cultured) and state that they describe the same product; note FTC labelling in one line with a source.',
    'TYPE_LIST; INLINE_ANSWER', [2, 3], [4], q=r'called|another name|other name', note='FTC point needs a cited FTC source (Jewelry Guides); no legal advice.'),
  S('S03', 'H2', 'How lab-grown diamonds are made (overview)', 'Summarise the two growth methods at overview level and the kinds of lab-grown stones; interim home for EDU-LG-04, so keep it self-contained but short.',
    'TYPE_LIST (growth methods); IMAGE/DIAGRAM optional', [5, 4, 6], [5], v=['what are lab grown diamonds'], q=r'how .*made|process|grown|types', links=['EDU-LG-03', 'EDU-LG-04'],
    note='INTERIM_HOME for EDU-LG-04 (conditional). CVD-vs-HPHT depth stays on EDU-LG-03: summary + link only.'),
  S('S04', 'H2', 'A short history of lab-grown diamonds', 'Give the key milestones (first synthesis, General Electric) briefly; context only.', 'FACTUAL_LIST (dated milestones)', [7],
    note='Dates and firsts must be sourced (e.g. GIA, museum or peer-reviewed history).'),
  S('S05', 'H2', 'Real diamonds, not simulants — and how they compare with mined diamonds', 'State in one or two lines that lab-grown diamonds are real diamonds (not simulants) and summarise the key difference from mined diamonds; link out for depth.',
    'SHORT SUMMARY + contextual links', [8, 9], [6, 7], q=r'real|fake|tester|like real', links=['EDU-LG-01', 'EDU-LG-02'],
    note='Brief mention only: authenticity is owned by EDU-LG-01 and comparison by EDU-LG-02.'),
  S('S06', 'H2', 'Cost, value and common drawbacks (brief)', 'Name price and resale as considerations and point to the pages that own them; acknowledge that buyers ask about disadvantages.',
    'SHORT SUMMARY + links', [10], [8, 9], q=r'worth|disadvantage|cost|price', links=['EDU-LG-05'],
    note='Price/resale owned by EDU-LG-05; pros and cons live on EDU-LG-02 (interim home for EDU-LG-06). No prices on this page.'),
  S('S07', 'H2', 'Explore the lab-grown diamond guide', 'Route readers to each lab-grown child topic with one line on what each answers; add the commercial hand-off only when COM-LG-HUB exists.',
    'TYPE_LIST (hub topic list)', [11, 12], links=['EDU-LG-10', 'EDU-NAT-00', 'EDU-4C-00', 'EDU-CERT-00', 'COM-LG-HUB', 'COM-ER'],
    note='Hub routing per Stage 16. Commercial CTA to COM-LG-HUB is CONDITIONAL; never use the bare "lab-grown diamonds" anchor.'),
 ],
 'EDU-LG-01': [
  S('S01', 'H1', 'Are lab-grown diamonds real? (working H1 + direct answer)', 'Open with a direct yes/no answer in the first lines, then one line on why (same carbon crystal as mined diamonds).',
    'DEFINITION_BLOCK / direct answer', [14], q=r'^(are|is) (a )?lab.*(real|really|actually)', v=[], imp='CRITICAL',
    aeo='Direct answer in the opening lines; Stage 8 SERP for the primary shows AI Overview + PAA (18 G18-0014).'),
  S('S02', 'H2', 'Why a lab-grown diamond is a real diamond', 'Explain that composition, crystal structure and physical/optical properties match mined diamonds; keep science at summary level.',
    'CORE_SECTION', [13], q=r'real diamond|really a diamond', links=['EDU-LG-03'], note='Composition depth belongs to EDU-GEN-01 (no Stage 16 link from this page; mention only).'),
  S('S03', 'H2', 'Lab-grown vs "fake": how simulants differ', 'Distinguish lab-grown diamonds from simulants (cubic zirconia, moissanite) and clarify that the alternative names mean the same thing.',
    'SHORT DISTINCTION LIST', [15, 16], q=r'fake', links=['EDU-GEM-00'], note='EDU-GEM-00 link is CONDITIONAL (Gemstones hub not built).'),
  S('S04', 'H2', 'How lab-grown differs from natural (in brief)', 'Acknowledge that searchers compare with natural diamonds; give the key difference (origin) in 1-3 sentences and link to the comparison page.',
    'SHORT SUMMARY + link', [17], links=['EDU-LG-02'], note='The primary SERP is COMPARISON-led; ownership stays with EDU-LG-02.'),
  S('S05', 'H2', 'Can anyone tell it is lab-grown?', 'Answer briefly whether a tester or jeweller can tell and that a grading report states origin; link to detection and certification pages.',
    'SHORT SUMMARY + links', [18, 19, 22], links=['EDU-LG-09', 'EDU-CERT-00', 'EDU-LG-08']),
  S('S06', 'H2', 'Is a lab-grown diamond right for you?', 'Point to price/value and pros-and-cons coverage without reproducing it; acknowledge common buyer reassurance questions.',
    'SHORT SUMMARY', [20, 21, 23], q=r'worth|rich|downside', links=['COM-ER'],
    note='EDU-LG-05 has no Stage 16 link from this page: mention only. EDU-LG-06 is conditional: no link.'),
 ],
 'EDU-LG-02': [
  S('S01', 'H1', 'Lab-grown vs natural diamonds (working H1 + answer-first summary)', 'Open with a concise direct answer: what is identical, what differs (origin, price, value retention) and that the better choice depends on priorities.',
    'DEFINITION_BLOCK / answer-first summary', [], q=r'is there a difference|better to buy a real', imp='CRITICAL',
    aeo='Stage 8: AI Overview on 4/4 comparison SERPs with comparison structure (S18P EDU-LG-02 AGGREGATE).', add='Answer-first comparison summary'),
  S('S02', 'H2', 'Lab-grown vs natural at a glance', 'Provide an attribute-by-attribute comparison table.', 'COMPARISON_TABLE', [31],
    cmp='Rows: origin/formation; formation time; composition; hardness; 4Cs grading; appearance; price level (no dated figures); resale/value retention; rarity; ethics & environment (link EDU-LG-07); grading labs. Columns: lab-grown | natural. SERP evidence supports a table (Stage 8 AI Overview comparison structure).'),
  S('S03', 'H2', 'What is the same', 'Explain the shared chemistry, hardness and 4Cs grading; answer appearance, durability and grading-lab parity in one line each.',
    'CORE_SECTION + INLINE_ANSWERS', [24, 36, 37, 38, 40], q=r'sparkle|as good as|better quality'),
  S('S04', 'H2', 'What is different: origin, rarity and tradition', 'Explain formation in the earth over time vs growth in weeks, and the rarity/emotional value some buyers attach to natural.',
    'CORE_SECTION', [25, 28], links=['EDU-NAT-00', 'EDU-LG-03']),
  S('S05', 'H2', 'Price, size for budget and resale value', 'Explain the price gap, the larger stone for the same spend and the difference in value retention; no dated price levels.',
    'SUPPORTING_SECTION', [26, 27, 30], q=r'price|cost', links=['EDU-LG-05'], note='Price levels date quickly (Stage 13 rule): describe relative differences, cite and date any figure. Resale depth lives on EDU-LG-05.'),
  S('S06', 'H2', 'Ethics and environmental impact (in brief)', 'Summarise the ethics/environment row in 1-3 sentences and link to the ethics page.', 'SHORT SUMMARY + link', [29], links=['EDU-LG-07']),
  S('S07', 'H2', 'Pros and cons of lab-grown diamonds', 'Set out the advantages and disadvantages of lab-grown diamonds; interim home for EDU-LG-06, so keep self-contained.',
    'PROS_CONS', [33], q=r'worth|downside|good\?|better\?|popular|replace|avoid', links=['EDU-LG-06'],
    note='INTERIM_HOME for EDU-LG-06 (conditional). Do not expand beyond the interim keywords.'),
  S('S08', 'H2', 'Can you tell them apart?', 'Answer in 1-3 sentences that specialist equipment is needed and a report states origin.', 'INLINE_ANSWER', [35], q=r'jeweler tell',
    note='EDU-LG-09 owns detection; Stage 16 has no LG-02 -> LG-09 link, so mention without a contextual link.'),
  S('S09', 'H2', 'Which should you choose?', 'Frame the decision by buyer priority (budget and size, tradition/rarity, value retention, ethics) without declaring a universal winner.',
    'DECISION_FRAMEWORK (priority list)', [32, 39, 42], links=['EDU-LG-10', 'EDU-LG-01', 'EDU-4C-00', 'COM-ER', 'COM-LG-HUB'],
    note='Third options (moissanite, CZ) are conditional (EDU-GEM-01 not built): one-line mention, no link.'),
  S('S10', 'H2', 'FAQ', 'Answer the perception and social questions that the SERP raises, one or two lines each.', 'FAQ', [34, 41]),
 ],
 'EDU-LG-03': [
  S('S01', 'H1', 'CVD vs HPHT (working H1 + answer-first)', 'Open by spelling out both acronyms, then give a short conditional answer to "which is better" and state that the methods cannot be told apart by eye after cutting.',
    'DEFINITION_BLOCK', [56, 47], q=r'full form|what is cvd diamond vs', imp='CRITICAL',
    aeo='AI Overview on 17/18 Stage 8 SERPs; DEFINITION_FIRST + COMPARISON_STRUCTURE (S18P EDU-LG-03 AGGREGATE).'),
  S('S02', 'H2', 'CVD vs HPHT: key differences at a glance', 'Provide a side-by-side comparison table of the two methods.', 'COMPARISON_TABLE', [49],
    cmp='Rows: process conditions; seed and growth; crystal growth shape; typical inclusions/strain; colour tendencies; post-growth treatment; price; grading (same 4Cs); detection (link). Columns: CVD | HPHT. No live price figures.'),
  S('S03', 'H2', 'How HPHT diamonds are grown', 'Explain the HPHT process step by step (seed, carbon source, heat and pressure); satisfy single-method "HPHT lab-grown diamond" searches here.',
    'STEP_SEQUENCE / PROCESS_EXPLAINER; IMAGE/DIAGRAM (HPHT press and CVD reactor, optional)', [43, 61], q=r'hpht (a )?real|hpht diamond(s)? real|is hpht', note='Single-method HPHT heads are owned by this page (Stage 15); do not create a separate HPHT page.'),
  S('S04', 'H2', 'How CVD diamonds are grown (what a CVD diamond is)', 'Explain the CVD process (plasma, carbon-rich gas, layer deposition) and answer "what is a CVD diamond" for single-method searches.',
    'STEP_SEQUENCE / PROCESS_EXPLAINER (reactor visual shared with S03)', [44, 45], q=r'what is (a )?cvd|cvd lab grown diamond\?|cvd diamond(s)? real|real or fake|is a cvd',
    note='Single-method CVD heads are owned by this page (Stage 15); do not create a separate CVD page.'),
  S('S05', 'H2', 'Growth shape, inclusions and colour tendencies', 'Explain how the methods leave different crystal habits, inclusions, strain and colour tendencies, and that reports can disclose the method.',
    'SUPPORTING_SECTION', [46, 55, 54, 59], q=r'tell an hpht', note='Type IIa owned by EDU-GEN-01 and report disclosure by EDU-CERT-00; Stage 16 has no link to either from this page, so mention only.'),
  S('S06', 'H2', 'HPHT growth vs HPHT treatment', 'Separate HPHT as a growth method from HPHT as a post-growth colour treatment.', 'DEFINITION_BLOCK', [53], q=r'treated', links=['EDU-LG-08']),
  S('S07', 'H2', 'Price difference between CVD and HPHT', 'Explain what drives any price difference between the methods without live figures.', 'SUPPORTING_SECTION', [50], q=r'difference in price|how much'),
  S('S08', 'H2', 'Pros and cons of each method', 'List the advantages and disadvantages of CVD and HPHT.', 'PROS_CONS', [51], q=r'disadvantages'),
  S('S09', 'H2', 'Which is better: CVD or HPHT?', 'Answer the question with conditions (what matters is the finished stone and its report) and explain when the method might matter to a buyer.',
    'CORE_SECTION (conditional answer)', [48], q=r'better|best', links=['EDU-LG-10', 'COM-ER'], imp='CRITICAL'),
  S('S10', 'H2', 'Are CVD and HPHT diamonds real, and will they pass a tester?', 'Give one-line answers and link to the authenticity and detection pages.', 'INLINE_ANSWERS + links', [57, 58, 60],
    q=r'tester|jeweler tell|jewelers hate', links=['EDU-LG-09', 'EDU-LG-02', 'EDU-LG-08'],
    note='Do not target "cvd/hpht diamond tester" (excluded keyword; ranking kept but not targeted). No Stage 16 link to EDU-LG-01: mention only.'),
  S('S11', 'H2', 'FAQ', 'Short answers to the method-specific worth and value questions.', 'FAQ', [52], q=r'worth'),
 ],
 'EDU-LG-05': [
  S('S01', 'H1', 'Lab-grown diamond price and value (working H1 + direct answers)', 'Open with direct answers to "are they cheaper?" and "do they hold their value?" before the explanation.',
    'DEFINITION_BLOCK (direct answer)', [297], [10], q=r'^are lab grown diamonds cheaper\?$|^do lab grown diamonds hold', v=['do lab grown diamonds hold their value'], imp='CRITICAL',
    aeo='18.5: AI Overview gives a direct "No" to the value question; answer-first format supported.'),
  S('S02', 'H2', 'Why lab-grown diamonds cost less than natural', 'Explain the production and supply reasons for the lower price.', 'CORE_SECTION', [63], [13], q=r'cheaper than natural'),
  S('S03', 'H2', 'Do lab-grown diamonds hold their value?', 'Explain resale and depreciation, the limited secondary market and why the absolute money lost can be smaller than the percentage suggests.',
    'CORE_SECTION; CALCULATION (illustrative, ratio-based)', [64, 69, 70], [11, 16, 18], q=r'worth anything|without certificate',
    note='Any worked example must use clearly hypothetical numbers or dated, sourced figures. HOD buy-back policy belongs to SUP-FAQ (no Stage 16 link from this page).'),
  S('S04', 'H2', 'How natural diamonds compare on value retention', 'Contrast value retention for natural vs lab-grown on this page\'s value angle only.', 'SUPPORTING_SECTION', [71], [15], links=['EDU-LG-02', 'EDU-NAT-01'],
    note='Full comparison stays on EDU-LG-02. EDU-NAT-01 link is CONDITIONAL.'),
  S('S05', 'H2', 'Price trends over time', 'Explain that lab-grown prices have fallen and why; every figure must be dated and sourced.', 'SUPPORTING_SECTION', [66, 73], [14, 17], q=r'get cheaper',
    note='SERP carries conflicting, dated percentage claims: do not repeat them as fact; cite a dated source or describe direction only.'),
  S('S06', 'H2', 'Are lab-grown diamonds an investment?', 'Explain why they are a consumer purchase rather than a financial investment.', 'SUPPORTING_SECTION', [65], [12], q=r'investment',
    note='No financial advice; frame as general information.'),
  S('S07', 'H2', 'Selling, pawning or trading in a lab-grown diamond', 'Explain resale options and what buyers typically encounter.', 'SUPPORTING_SECTION', [68], q=r'pawn|sell'),
  S('S08', 'H2', 'Price per carat explained', 'Explain price per carat as a concept for comparing stones, without live figures.', 'INLINE / SUPPORTING', [67], links=['EDU-LG-06', 'COM-ER', 'COM-LG-HUB']),
  S('S09', 'H2', 'FAQ', 'Short answers to the remaining price questions, each dated or framed without live figures.', 'FAQ', [72]),
 ],
 'EDU-LG-07': [
  S('S01', 'H1', 'Are lab-grown diamonds ethical? (working H1 + qualified answer)', 'Open with a qualified direct answer: the ethical benefits and the environmental caveats in two lines.',
    'DEFINITION_BLOCK (qualified yes)', [298], [20, 21], v=['are lab grown diamonds ethical'], q=r'^are lab grown diamonds ethical', imp='CRITICAL',
    aeo='18.5: AI Overview gives a qualified "Yes" then benefits and concerns.'),
  S('S02', 'H2', 'The ethical case: no mining, conflict-free supply', 'Compare lab-grown sourcing with mined supply chains: mining risks, labour conditions and conflict diamonds.', 'PROS_CONS (benefits)', [74, 77], [21, 23, 27],
    links=['EDU-LG-02', 'EDU-NAT-02'], note='EDU-NAT-02 (conflict-free natural) is conditional: link only when built. Claims about mining impacts need cited sources.'),
  S('S03', 'H2', 'Environmental impact: energy use and where it comes from', 'Explain energy use in growing diamonds, the role of the power grid (including fossil-fuel grids) and what renewable-energy claims do and do not show.',
    'PROS_CONS (concerns)', [75, 76], [22, 24], q=r'environment',
    note='No HOD environmental claim without substantiation (BUSINESS_FACT_REQUIRED). Do not turn SERP claims into HOD claims.'),
  S('S04', 'H2', 'Transparency and regulation', 'Explain that disclosure standards in the lab-grown sector are limited and what information a buyer can ask for.', 'SUPPORTING_SECTION', [], [25],
    add='Lack of regulation / transparency (18.5 new evidence)'),
  S('S05', 'H2', 'How to buy a lab-grown diamond responsibly', 'Give a short checklist of questions to ask (origin facility, energy source, disclosure).', 'CHECKLIST (numbered)', [], [26],
    add='How to buy responsibly: ask for origin and energy source (18.5 new evidence)', links=['BLOG-CRAFT'], note='BLOG-CRAFT link is CONDITIONAL (Stage 16).'),
  S('S06', 'H2', 'What is the most ethical diamond?', 'Compare lab-grown, natural and recycled/antique options briefly on ethics, without declaring a single answer.', 'SHORT COMPARISON', [], [28],
    q=r'most ethical', add='Most ethical diamond comparison (18.5 PAA)'),
 ],
 'EDU-LG-08': [
  S('S01', 'H1', 'Do lab-grown diamonds get cloudy? (working H1 + direct answer)', 'Open with a direct "no" answer and one line on why (same material as mined diamonds).', 'DEFINITION_BLOCK (direct "No")',
    [299], [29, 30], v=['do lab grown diamonds get cloudy'], q=r'^do lab grown diamonds get cloudy', imp='CRITICAL', aeo='18.5: AI Overview direct "No"; 8 of 9 organic snippets agree.'),
  S('S02', 'H2', 'Do lab-grown diamonds fade or change over time?', 'Explain stability over time and answer lifespan questions.', 'CORE_SECTION', [78], [19], q=r'fade|lifespan'),
  S('S03', 'H2', 'Why a lab-grown diamond might look cloudy', 'List the real causes of a cloudy look: surface build-up, cloud inclusions/low clarity, poor cut, simulant confusion.', 'TYPE_LIST (causes)', [], [34],
    add='Causes of a cloudy look (18.5 AI Overview)', links=['EDU-4C-05']),
  S('S04', 'H2', 'Sparkle and looks compared with natural diamonds', 'Explain that sparkle and appearance match natural diamonds of the same cut and grade.', 'SUPPORTING_SECTION', [80], [31], q=r'sparkle|look real', links=['EDU-LG-01']),
  S('S05', 'H2', 'Fluorescence in lab-grown diamonds', 'Explain what fluorescence is, whether lab-grown diamonds show it and how it appears on reports.', 'CORE_SECTION', [79], [32], q=r'fluoresc',
    note='Fluorescence did not appear on the 18.5 cloudiness SERP (UNCHANGED); keyword evidence alone keeps it core.'),
  S('S06', 'H2', 'Treatments and disclosure', 'Explain post-growth treatments (irradiation, clarity enhancement) and why disclosure matters.', 'SUPPORTING_SECTION', [81, 82], q=r'clarity enhanced|irradiat'),
  S('S07', 'H2', 'Durability for everyday wear (in brief)', 'State hardness parity in 1-3 sentences and link to the diamond properties page.', 'SHORT SUMMARY + link', [83], [33], links=['EDU-GEN-01', 'EDU-LG-03']),
  S('S08', 'H2', 'How to keep a lab-grown diamond sparkling', 'Give numbered cleaning steps and when to get a professional check.', 'STEP_SEQUENCE', [], [35], add='Cleaning and professional check (18.5 AI Overview "How to Restore the Sparkle")'),
  S('S09', 'H2', 'FAQ', 'Short answers to remaining appearance questions.', 'FAQ', []),
 ],
 'EDU-LG-09': [
  S('S01', 'H1', 'Do lab-grown diamonds pass a diamond tester? (working H1 + direct answer)', 'Open with a direct answer and one line on why a standard tester cannot separate lab-grown from natural.',
    'DEFINITION_BLOCK', [], q=r'^do lab grown diamonds pass|^will a diamond tester work', imp='CRITICAL', add='Direct answer to the primary question',
    aeo='Stage 8: AI Overview on 2/2 tester SERPs, TYPE_LIST + PROCESS_EXPLAINER (S18P EDU-LG-09).'),
  S('S02', 'H2', 'Will a lab-grown diamond pass a diamond tester?', 'Explain the result on thermal and electrical testers and why.', 'CORE_SECTION', [84], q=r'pass|cvd'),
  S('S03', 'H2', 'How thermal and electrical testers work', 'Explain the two tester types and what each measures.', 'TYPE_LIST + PROCESS_EXPLAINER', [85], q=r'testers (really|actually) work|real\?|beeps'),
  S('S04', 'H2', 'Limits of testers: moissanite and false readings', 'Explain which gems can pass a tester and why readings can mislead.', 'SUPPORTING_SECTION', [87], q=r'what gems', links=['EDU-GEM-00'],
    note='EDU-GEM-00 link is CONDITIONAL.'),
  S('S05', 'H2', 'How jewellers and labs identify lab-grown diamonds', 'Explain spectroscopy/UV screening, magnification and laser inscriptions and report look-ups.', 'CORE_SECTION', [86, 88, 89],
    q=r'jeweler tell|serial|x ray', links=['EDU-CERT-00', 'EDU-LG-01', 'EDU-LG-03']),
  S('S06', 'H2', 'Where to get a diamond tested', 'Explain the options for professional testing.', 'INLINE_ANSWER', [91], q=r'where can i get'),
  S('S07', 'H2', 'FAQ', 'Short answers on home tests and tester edge cases.', 'FAQ', [90], q=r'heat test|home'),
 ],
 'EDU-LG-10': [
  S('S01', 'H1', 'How to choose a lab-grown diamond (working H1 + summary of steps)', 'Open with a one-paragraph summary of the choosing steps so the answer is visible immediately.', 'ANSWER-FIRST SUMMARY', [],
    q=r'^how to choose', imp='CRITICAL', add='Answer-first summary of the choosing sequence', aeo='Stage 8: AI Overview BUYING_CONSIDERATIONS structure (S18P EDU-LG-10).'),
  S('S02', 'H2', 'Step by step: choosing a lab-grown diamond', 'Give a numbered, beginner-friendly sequence (budget, shape, 4Cs priorities, report, compare).', 'STEP_SEQUENCE', [99]),
  S('S03', 'H2', 'Prioritising the 4Cs for a lab-grown diamond', 'Explain which Cs to prioritise and where it is sensible to save; answer whether flawless is worth paying for in one line.',
    'CORE_SECTION', [93, 101], q=r'vs1|vs2|clearer', links=['EDU-4C-00'], note='No Stage 16 link to EDU-4C-03 from this page: mention only.'),
  S('S04', 'H2', 'Insist on a grading report', 'Explain why a report (IGI/GIA) matters and link to the certification guide.', 'SUPPORTING_SECTION + link', [94], links=['EDU-CERT-00']),
  S('S05', 'H2', 'Set a budget and compare price per carat', 'Explain budgeting by price per carat and why resale value should be understood before buying.', 'SUPPORTING_SECTION', [95, 96],
    q=r'how much should i pay', note='EDU-LG-05 has no Stage 16 link from this page: mention only. No live prices.'),
  S('S06', 'H2', 'Shape and growth method', 'Summarise that shape is a personal choice (link shapes guide) and whether CVD vs HPHT matters (link).', 'SHORT SUMMARY + links', [97, 98], links=['EDU-SHP-00', 'EDU-LG-03']),
  S('S07', 'H2', 'Next steps', 'Point to comparison and product pages at the decision point, answering common last-minute hesitations (perception, lifespan) in one line each; commercial hand-off only once business facts are confirmed.', 'DECISION POINT + CTA', [100, 103],
    q=r'jewelers hate|lifespan', links=['EDU-LG-02', 'COM-ER', 'COM-LG-HUB', 'EXIST-BLOG-ER-ONLINE'],
    note='Do not take engagement-ring commercial ownership (ranking-equity rule). EDU-LG-06 conditional: no link.'),
  S('S08', 'H2', 'FAQ', 'Short answer to the lab-grown engagement ring question without commercial targeting.', 'FAQ', [], q=r'engagement ring'),
 ],
 'EDU-NAT-00': [
  S('S01', 'H1', 'How are diamonds formed? (working H1 + answer-first summary)', 'Open with a short answer covering carbon, depth, heat, pressure and time.', 'DEFINITION_BLOCK / process summary',
    [300], [36], v=['how are diamonds formed'], q=r'^how are diamonds formed', imp='CRITICAL', aeo='18.5: AI Overview "Natural Formation" then "Lab-Grown Formation".'),
  S('S02', 'H2', 'How natural diamonds form deep in the Earth', 'Explain formation in the mantle under heat and pressure over billions of years, including the timescale.', 'STEP_SEQUENCE / PROCESS_EXPLAINER', [104, 110, 111],
    [37], q=r'how long|white diamonds real', links=['EDU-GEN-01']),
  S('S03', 'H2', 'The journey to the surface: kimberlite pipes', 'Explain volcanic transport through kimberlite pipes.', 'CORE_SECTION', [105], [38]),
  S('S04', 'H2', 'Do diamonds start as coal?', 'Correct the coal myth in a short, sourced answer.', 'INLINE_ANSWER / myth check', [], [41, 55 + 85], q=r'coal',
    add='Coal myth (18.5 PAA on formation and made-of SERPs)'),
  S('S05', 'H2', 'Where natural diamonds are found', 'Name the main source regions at summary level.', 'FACTUAL_LIST', [108], [40]),
  S('S06', 'H2', 'From mine to jewellery: mining, cutting and polishing', 'Summarise extraction and the rough-to-polished process.', 'STEP_SEQUENCE', [106, 107, 112], q=r'extract|processed|raw diamond look',
    links=['EDU-NAT-01'], note='Natural value/rarity (EDU-NAT-01) and conflict-free sourcing (EDU-NAT-02) are conditional: one-line mention, link only when built.'),
  S('S07', 'H2', 'How lab-grown formation differs (in brief)', 'Summarise that diamonds can also be grown (HPHT, CVD) in a short section and link out.', 'SHORT COMPARISON + link', [109], [39],
    links=['EDU-LG-00', 'EDU-LG-02']),
  S('S08', 'H2', 'FAQ', 'Short answers to rough-diamond and ongoing-formation questions.', 'FAQ', [], [42], q=r'rough|identify|still creating'),
 ],
 'EDU-4C-00': [
  S('S01', 'H1', 'The 4Cs of diamonds (working H1 + definition)', 'Open with a concise definition of the 4Cs as the standard grading framework, then name the four Cs.', 'DEFINITION_BLOCK',
    [114, 123, 283, 301], [43, 44, 45, 51], v=['4cs of diamonds'], imp='CRITICAL',
    aeo='18.5: AI Overview gives a definition, then one block per C (meaning + grade range).'),
  S('S02', 'H3', 'Cut', 'Explain what cut means and its grade range in one block; link to the cut guide.', 'ONE BLOCK PER C (meaning + grade range)', [121], [52], imp='IMPORTANT', links=['EDU-4C-06']),
  S('S03', 'H3', 'Colour', 'Explain what colour means and the D-Z range in one block; link to the colour guide.', 'ONE BLOCK PER C (meaning + grade range)', [120], [50], imp='IMPORTANT', links=['EDU-4C-05']),
  S('S04', 'H3', 'Clarity', 'Explain what clarity means and the FL-I3 range in one block; link to the clarity guide.', 'ONE BLOCK PER C (meaning + grade range)', [119, 125], [49 + 0, 49 + 0][:0] or [50 - 1 + 1][:0] or [], q=r'flawless|clarity rating',
    imp='IMPORTANT', links=['EDU-4C-01', 'EDU-4C-03']),
  S('S05', 'H3', 'Carat', 'Explain what carat means (weight, not size) in one block; link to the carat guide.', 'ONE BLOCK PER C (meaning + grade range)', [122], [53], imp='IMPORTANT', links=['EDU-4C-07']),
  S('S06', 'H2', 'The 4Cs grading scales at a glance', 'Show all four scales in one summary chart.', 'VISUAL_CHART', [115], [46], v=['4cs of diamonds'],
    note='18.5: images pack in second position (grading charts); related "4cs of diamonds chart".'),
  S('S07', 'H2', 'Which C matters most?', 'Discuss order of importance and trade-offs, including common colour-clarity combinations; budget-to-size detail stays on the carat guide.',
    'SUPPORTING_SECTION (order of importance)', [117, 118], [47, 48, 55], q=r'f vs|f vs1', links=['EDU-LG-10', 'COM-ER'],
    note='Budget-to-size PAA (CL185-055) is answered on EDU-4C-07; no price figures here.'),
  S('S08', 'H2', 'Lab-grown diamonds are graded on the same scales', 'Explain that lab-grown diamonds use the same 4Cs scales and how reports show origin.', 'SUPPORTING_SECTION', [116], [49], links=['EDU-CERT-00'],
    note='18.5 WEAKENED this from CRITICAL to IMPORTANT (head-term SERP does not mention lab-grown), but it stays because the existing URL is lab-grown framed.'),
  S('S09', 'H2', 'Beyond the 4Cs', 'Mention fluorescence, polish and symmetry and address the "5th C" question briefly.', 'INLINE_ANSWER', [124], [54], q=r'5th c'),
  S('S10', 'H2', 'FAQ', 'Short answers to lab-grown grading questions.', 'FAQ', [], q=r'lab.grown'),
 ],
 'EDU-4C-01': [
  S('S01', 'H1', 'Diamond clarity (working H1 + definition)', 'Open with a concise definition of clarity and who set the scale (GIA).', 'DEFINITION_BLOCK', [136], q=r'^what is the best clarity|good clarity', imp='CRITICAL',
    aeo='Stage 8: AI Overview GRADE_SCALE + PROS_CONS + BUYING_CONSIDERATIONS (S18P EDU-4C-01).', add='Clarity definition'),
  S('S02', 'H2', 'The clarity scale from FL to I3 (with chart)', 'Present the GIA grade groups best to worst, with a visual chart.', 'GRADE_SCALE + VISUAL_CHART', [126, 127, 138],
    note='Chart evidence: Stage 18 G18-0127 (clarity chart best to worst); related "diamond clarity chart". Colour chart cross-reference: EDU-4C-05 has no Stage 16 link from here: mention only.'),
  S('S03', 'H2', 'Inclusions and blemishes', 'Explain the main inclusion and blemish types and which to avoid.', 'TYPE_LIST', [128], q=r'worst clarity|characteristics'),
  S('S04', 'H2', 'Eye-clean and best-value clarity', 'Explain eye-clean, where the value sweet spot usually sits, and why step cuts show more.', 'CORE_SECTION', [129, 130], q=r'bigger diamond or more clarity'),
  S('S05', 'H2', 'VS1 and VS2 clarity', 'Explain VS1 and VS2 and how they differ; interim home for EDU-4C-04, so keep self-contained.', 'SUPPORTING_SECTION', [133], q=r'vs1|vs2', links=['EDU-4C-04'],
    note='INTERIM_HOME for EDU-4C-04 (conditional). Link is CONDITIONAL.'),
  S('S06', 'H2', 'Comparing clarity grades: VVS vs VS vs SI', 'Compare adjacent grades in a table and link to the grade explainers for SI and VVS depth.', 'COMPARISON_TABLE', [132, 134, 135],
    q=r'vvs or vs|vs or si', links=['EDU-4C-02', 'EDU-4C-03'], cmp='Grades: VVS1/VVS2, VS1/VS2, SI1/SI2. Attributes: visibility under 10x, eye-clean likelihood, relative price, typical use. No live prices.'),
  S('S07', 'H2', 'Clarity vs carat: where to compromise', 'Explain the trade-off between clarity and size.', 'SUPPORTING_SECTION', [131]),
  S('S08', 'H2', 'Clarity in lab-grown diamonds', 'State in one or two lines that lab-grown diamonds are graded on the same clarity scale.', 'INLINE_ANSWER', [137]),
  S('S09', 'H2', 'FAQ', 'Short answers to lowest-grade questions.', 'FAQ', [], q=r'lowest'),
 ],
 'EDU-4C-02': [
  S('S01', 'H1', 'SI clarity diamonds (working H1 + definition)', 'Open with a definition of SI1/SI2 and where they sit on the scale.', 'DEFINITION_BLOCK', [139], imp='CRITICAL',
    aeo='Stage 8: AI Overview DEFINITION_FIRST + PROS_CONS on 2/2 SI2 SERPs.'),
  S('S02', 'H2', 'Is SI clarity good? Eye-clean SI diamonds', 'Answer whether SI can be eye-clean and when.', 'CORE_SECTION', [140], q=r'^is si2 a good|^is si1'),
  S('S03', 'H2', 'Pros and cons of SI clarity', 'List advantages and disadvantages.', 'PROS_CONS', [141]),
  S('S04', 'H2', 'SI vs VS and VVS', 'Compare SI with higher grades briefly and link to the clarity guide.', 'SHORT COMPARISON + link', [143], q=r'better than vs1', links=['EDU-4C-01', 'EDU-4C-03']),
  S('S05', 'H2', 'SI3 and the I1 boundary', 'Explain that SI3 is not a GIA grade and where I1 begins.', 'INLINE_ANSWER', [145]),
  S('S06', 'H2', 'SI price and value', 'Explain the value case for SI without live prices.', 'SUPPORTING_SECTION', [144], q=r'worth|increase in value'),
  S('S07', 'H2', 'Buying tips for SI diamonds', 'Give numbered tips: smaller sizes, avoid step cuts, inspect images/videos closely.', 'STEP_SEQUENCE; IMAGE (on-hand examples, optional)', [142, 147, 148]),
  S('S08', 'H2', 'FAQ', 'Short answers on SI with colour grades and testers.', 'FAQ', [146]),
 ],
 'EDU-4C-03': [
  S('S01', 'H1', 'VVS diamonds (working H1 + definition)', 'Open with what VVS means and that it is a clarity grade, not a diamond type.', 'DEFINITION_BLOCK', [149, 155], q=r'what does vvs mean', imp='CRITICAL',
    aeo='Stage 8: AI Overview DEFINITION_FIRST (S18P EDU-4C-03).'),
  S('S02', 'H2', 'VVS1 vs VVS2', 'Explain the difference between the two VVS grades.', 'SHORT COMPARISON', [150]),
  S('S03', 'H2', 'IF and FL: the flawless grades', 'Explain internally flawless and flawless grades.', 'SUPPORTING_SECTION', [151]),
  S('S04', 'H2', 'Is VVS worth it?', 'Explain whether the difference from VS is visible and when paying for VVS makes sense.', 'CORE_SECTION', [152], q=r'vvs or vs', links=['EDU-4C-01', 'EDU-4C-02']),
  S('S05', 'H2', 'VVS price context', 'Explain how VVS affects price without live figures.', 'SUPPORTING_SECTION', [153], q=r'expensive|how much'),
  S('S06', 'H2', 'VVS lab-grown diamonds', 'Explain VVS grades in lab-grown diamonds.', 'SUPPORTING_SECTION', [154, 156], q=r'lab grown'),
  S('S07', 'H2', 'FAQ', 'Short answers to remaining VVS questions.', 'FAQ', []),
 ],
 'EDU-4C-05': [
  S('S01', 'H1', 'Diamond colour (working H1 + definition)', 'Open with a concise definition of diamond colour grading on the GIA D-to-Z scale.', 'DEFINITION_BLOCK', [287], [56], v=['diamond color chart'], imp='CRITICAL',
    aeo='18.5: AI Overview shows chart images, then the D-to-Z definition and five grade groups.'),
  S('S02', 'H2', 'The D-to-Z colour scale and grade groups', 'Describe the five grade groups (D-F, G-J, K-M, N-R, S-Z), each with appearance and value.', 'TYPE_LIST (grade groups)', [157, 165], [57, 60],
    q=r'best to worst|what letter', links=['EDU-4C-08'], note='EDU-4C-08 link is CONDITIONAL.'),
  S('S03', 'H2', 'Diamond colour chart', 'Provide a visual D-to-Z chart.', 'VISUAL_CHART', [158], [58], v=['diamond color chart']),
  S('S04', 'H2', 'Is G-H colour good? The near-colourless range', 'Explain why the near-colourless range is a common balance of looks and budget and how colour appears face-up.', 'CORE_SECTION', [159, 160], [59],
    q=r'g h|gh good|best color'),
  S('S05', 'H2', 'Comparing colour grades', 'Compare commonly compared grades (D vs E, D vs G, GH vs FG) and the price effect of colour.', 'COMPARISON_TABLE', [163, 164], [60, 61],
    q=r'gh or fg|d or g', cmp='Pairs: D vs E; D vs G; FG vs GH. Attributes: visible difference face-up, relative price, when the higher grade is worth it. No live prices.'),
  S('S06', 'H2', 'Colour, metal, size and shape', 'Explain how metal choice, stone size and shape affect how colour shows.', 'SUPPORTING_SECTION', [161, 162], [62], links=['EDU-MET-00']),
  S('S07', 'H2', 'Beyond Z: fancy coloured diamonds (in brief)', 'Note that colours past Z and pink/blue stones are graded separately.', 'INLINE_ANSWER', [], [64], add='Fancy colour note (18.5 AI Overview)'),
  S('S08', 'H2', 'FAQ', 'Short answers to remaining colour-grade questions.', 'FAQ', [], q=r'least valuable'),
 ],
 'EDU-4C-06': [
  S('S01', 'H1', 'Diamond cut (working H1 + definition)', 'Open with a definition of cut as light performance (not shape).', 'DEFINITION_BLOCK', [288], [65], v=['diamond cut'], imp='CRITICAL',
    aeo='18.5: AI Overview definition, then "Cut vs. Shape", then cut quality factors.'),
  S('S02', 'H2', 'Cut grade vs diamond shape', 'Separate cut quality from shape and link to the shapes guide for shape choice.', 'COMPARISON (short)', [169], [66], q=r'called', links=['EDU-SHP-00'],
    note='The head term is MIXED (cut quality + shape lists): address the ambiguity, keep shape depth on EDU-SHP-00.'),
  S('S03', 'H2', 'The cut grade scale', 'Present the scale from Excellent/Ideal to Poor with a chart, explain Ideal vs Excellent and super ideal, and which labs grade cut.', 'GRADE_SCALE + VISUAL_CHART',
    [166, 176, 171, 172], [70], q=r'super ideal|best cut grade|poor cut'),
  S('S04', 'H2', 'Light performance: brightness, fire and scintillation', 'Explain the three light-performance terms.', 'TYPE_LIST', [167], [67]),
  S('S05', 'H2', 'Proportions, polish and symmetry', 'Explain how proportions, polish and symmetry make up cut, with the main facets named.', 'SUPPORTING_SECTION; labelled facet list', [168, 173], [68]),
  S('S06', 'H2', 'Cut grading for round vs fancy shapes', 'Explain that cut grades apply differently to rounds and fancy shapes.', 'INLINE_ANSWER', [170], q=r'brilliant cut'),
  S('S07', 'H2', 'Does cut matter? Choosing for sparkle', 'Explain why cut matters most for sparkle and what to prioritise.', 'CORE_SECTION', [174], q=r'sparkle|matter|best cut for|best in diamonds'),
  S('S08', 'H2', 'FAQ', 'Short answers to cheapest-cut and price questions.', 'FAQ', [175], [71], q=r'cheapest'),
 ],
 'EDU-4C-07': [
  S('S01', 'H1', 'Diamond carat (working H1 + definition)', 'Open with a definition: carat is a unit of weight (0.2 g), not a measure of face-up size.', 'DEFINITION_BLOCK', [177, 289], [67], imp='CRITICAL', add='Carat = 0.2 g (18.5 entity)'),
  S('S02', 'H2', 'Carat size chart: carat weight to millimetres', 'Provide a carat-to-millimetre chart, with sizes by shape.', 'VISUAL_CHART (carat to mm, by shape)', [302], [68, 69, 70], v=['diamond carat size chart'],
    note='18.5: image-led SERP, images pack in first position, no AI Overview. SERP evidence suggests the chart is the primary format.', links=['EDU-SHP-00']),
  S('S03', 'H2', 'How big does it look? On-hand comparison', 'Show carat sizes on a hand for visual comparison.', 'IMAGE (on-hand comparison)', [], [72], add='On-hand visual comparison (18.5 short videos, related "size on hand simulator")'),
  S('S04', 'H2', 'Is a 1 carat (or 2 carat) diamond a good size?', 'Explain how size perception depends on hand, setting and shape rather than a single "good" size.', 'CORE_SECTION', [178, 182],
    q=r'good\?|good size|big diamond|perfect|flashy'),
  S('S05', 'H2', 'Carat terms: ct, ctw and fractions', 'Explain carat vs total carat weight and fractional weights (1/4, 1/3, 1/2, 3/4).', 'INLINE_ANSWERS', [179, 180], q=r'ct tw'),
  S('S06', 'H2', 'Carat sizes for stud earrings', 'Explain how carat choices differ for studs (per stone vs total weight).', 'SUPPORTING_SECTION', [181], q=r'earrings'),
  S('S07', 'H2', 'Carat and price: what a budget buys', 'Explain how price rises with carat and what shapes the budget-to-size relationship, without live prices.', 'SUPPORTING_SECTION', [183], [71],
    q=r'\$|how many carats', links=['COM-ER'], note='No live prices; use dated sourced ranges only if at all. Loose-stone shopping is commercial and deferred (CL-006).'),
 ],
 'EDU-SHP-00': [
  S('S01', 'H1', 'Diamond shapes (working H1 + definition)', 'Open with what "shape" means (outline seen from above) and how it differs from cut quality.', 'DEFINITION_BLOCK', [185, 290], [80, 81], v=['diamond shapes'], imp='CRITICAL',
    aeo='18.5: AI Overview defines shape, then lists 10 shapes with one trait each.'),
  S('S02', 'H2', 'The main diamond shapes (with pictures)', 'Show each of the ten main shapes with an image and one distinguishing characteristic.', 'TYPE_LIST + VISUAL_CHART (shape chart with pictures)', [184, 190], [82, 84],
    q=r'different shapes|what are the different'),
  S('S03', 'H2', 'Shape characteristics compared', 'Compare shapes on length-to-width ratio, sparkle, finger coverage per carat and bow-tie; include asscher vs emerald.', 'COMPARISON_TABLE', [187, 189], [85],
    cmp='Shapes: round, oval, princess, cushion, emerald, pear, marquise, radiant, asscher, heart. Attributes: sparkle (brilliant/step), elongation/L:W, apparent size per carat, bow-tie risk, setting notes.',
    q=r'emerald cut diamond sparkle|princess'),
  S('S04', 'H2', 'Brilliant cuts vs step cuts', 'Explain the sparkle vs "clear, elegant gleam" choice.', 'SHORT COMPARISON', [], [88], add='Brilliant vs step cut decision (18.5 AI Overview prompt)', links=['EDU-4C-06']),
  S('S05', 'H2', 'Choosing a shape for an engagement ring', 'Help the reader choose by style, hand, setting and budget; keep the existing engagement-ring angle.', 'CORE_SECTION (decision)', [186], [83],
    q=r'what shape diamond should|prettiest', links=['EDU-RJG-01', 'COM-ER']),
  S('S06', 'H2', 'Shape and price', 'Explain why some shapes cost more per carat than others.', 'INLINE_ANSWER', [188], [86], q=r'expensive'),
  S('S07', 'H2', 'Shapes in jewellery', 'Illustrate a shape combination with the oval-with-marquise product example; per-shape depth pages are deferred.', 'EXAMPLE (product)', [193, 192, 194], [87],
    links=['COM-PDP-OVAL-FLORAL', 'EDU-4C-07'], note='Product example only while the product is live (Stage 16). EDU-SHP-01 conditional: no link.'),
  S('S08', 'H2', 'FAQ', 'Short answers to shape-specific questions not covered above.', 'FAQ', []),
 ],
 'EDU-CERT-00': [
  S('S01', 'H1', 'Diamond certification (working H1 + definition)', 'Open with a definition of a diamond certificate / grading report from an independent lab, and how it differs from an appraisal.', 'DEFINITION_BLOCK',
    [195, 291], [89, 90], v=['diamond certificate'], q=r'what does a diamond certificate mean', imp='CRITICAL',
    aeo='18.5: AI Overview definition, "What is Included", "Top Grading Laboratories".'),
  S('S02', 'H2', 'What a grading report includes', 'List the contents: 4Cs, measurements, polish, symmetry, fluorescence, origin, growth method, laser inscription.', 'TYPE_LIST', [198], [91], links=['EDU-4C-00']),
  S('S03', 'H2', 'Who issues diamond reports: the main labs', 'Name the main labs (GIA, IGI, AGS, GCAL) and explain GIA and IGI lab-grown reports; link to GIA vs IGI for the comparison.', 'TYPE_LIST', [197, 200, 201, 203],
    [92, 95, 98], q=r'gia (still )?(certify|grade)|top 5|best certificate|gia or igi|igi certification good', links=['EDU-CERT-01'],
    note='Detailed GIA vs IGI comparison is owned by EDU-CERT-01. IGI-only depth (EDU-CERT-03) is deferred.'),
  S('S04', 'H2', 'Do lab-grown diamonds come with certificates?', 'Explain lab-grown reports and origin disclosure.', 'CORE_SECTION', [196], [93], q=r'lab grown diamonds (certified|graded)|lab-grown diamonds get'),
  S('S05', 'H2', 'How to verify a diamond report', 'Give numbered steps for checking a report number or laser inscription on the lab\'s site.', 'STEP_SEQUENCE', [199], [94], q=r'check'),
  S('S06', 'H2', 'How to read a grading report', 'Walk through the sections of a report; interim home for EDU-CERT-02, so keep self-contained.', 'STEP_SEQUENCE / annotated walkthrough', [204], links=['EDU-CERT-02'],
    note='INTERIM_HOME for EDU-CERT-02 (conditional). An annotated sample report is an editorial choice; SERP format evidence is not specific to this section.'),
  S('S07', 'H2', 'Getting a diamond certified', 'Explain how a stone gets graded, roughly what it costs, and that a report can help identify a stone if lost or stolen.', 'SUPPORTING_SECTION', [202, 205], [97, 99],
    q=r'how do you get', links=['EDU-LG-10', 'COM-ER'], note='Cost: no live fees; describe what drives cost or cite dated lab fee schedules.'),
  S('S08', 'H2', 'FAQ', 'Short answers to remaining certification questions.', 'FAQ', []),
 ],
 'EDU-CERT-01': [
  S('S01', 'H1', 'GIA vs IGI (working H1 + answer-first)', 'Open with a concise conditional answer to which report is better for a lab-grown diamond.', 'ANSWER-FIRST SUMMARY', [], q=r'which is best, igi or gia|gia or igi certification better',
    imp='CRITICAL', add='Answer-first conditional verdict', aeo='Stage 8: AI Overview COMPARISON_STRUCTURE + BUYING_CONSIDERATIONS (S18P EDU-CERT-01).'),
  S('S02', 'H2', 'GIA vs IGI at a glance', 'Provide a side-by-side comparison table.', 'COMPARISON_TABLE', [210],
    cmp='Rows: lab-grown grading approach; report format; growth-method disclosure; cost; turnaround/availability; market perception; natural-diamond grading. Columns: GIA | IGI. No live fees.'),
  S('S03', 'H2', 'How each lab grades lab-grown diamonds', 'Explain the differences in grading approach for lab-grown stones.', 'CORE_SECTION', [206], q=r'still grade'),
  S('S04', 'H2', 'Growth-method disclosure', 'Explain how each report discloses growth method.', 'SUPPORTING_SECTION', [207]),
  S('S05', 'H2', 'Cost and availability: why IGI is cheaper', 'Explain the cost and availability differences.', 'SUPPORTING_SECTION', [208], q=r'cheaper'),
  S('S06', 'H2', 'Consistency and strictness: what buyers report', 'Summarise the perception of grading strictness with sourced evidence only.', 'INLINE_ANSWER', [213],
    note='Strictness claims need a cited source; forum sentiment is not evidence of grading practice.'),
  S('S07', 'H2', 'Which report should you choose?', 'Give decision guidance by use case.', 'DECISION_FRAMEWORK', [209, 214], q=r'best certificate for lab', links=['EDU-LG-10', 'COM-ER']),
  S('S08', 'H2', 'Other labs (GCAL, AGS, EGL, GSI)', 'Mention other labs briefly and how they compare.', 'SHORT TYPE_LIST', [211, 212], q=r'egl'),
  S('S09', 'H2', 'FAQ', 'Short answers to remaining lab questions.', 'FAQ', []),
 ],
 'EDU-MET-00': [
  S('S01', 'H1', 'Jewellery metals guide (working H1 + overview)', 'Open with a short overview naming the main metals and the choice factors (look, durability, maintenance, skin sensitivity, budget).',
    'ANSWER-FIRST SUMMARY', [292], [100], v=['white gold vs platinum'], imp='CRITICAL', add='Metals overview'),
  S('S02', 'H2', 'Types of jewellery metals', 'Describe gold (yellow, white, rose), platinum and sterling silver, one block each.', 'TYPE_LIST', [215, 223, 222], q=r'sterling silver|rose gold'),
  S('S03', 'H2', 'White gold vs platinum', 'Compare white gold and platinum in a table and cover the disadvantages of each.', 'COMPARISON_TABLE + PROS_CONS', [217], [101, 102, 103, 114, 115],
    v=['white gold vs platinum'], q=r'platinum|disadvantage of white gold', cmp='Rows: composition; colour and plating; durability (scratching vs patina); maintenance; skin sensitivity; weight; price level (no figures). Columns: white gold | platinum.'),
  S('S04', 'H2', 'Gold karats in brief', 'Summarise what karat means and link to the 14k vs 18k comparison.', 'SHORT SUMMARY + link', [224], [109], links=['EDU-MET-01']),
  S('S05', 'H2', 'Rhodium plating', 'Explain why white gold is rhodium plated, how long it lasts and re-plating; interim home for EDU-MET-02.', 'SUPPORTING_SECTION', [218],
    q=r'rhodium|replate|dip a white gold', links=['EDU-MET-02'], note='INTERIM_HOME for EDU-MET-02 (conditional). No live plating prices.'),
  S('S06', 'H2', 'Hypoallergenic metals and skin sensitivity', 'Explain nickel sensitivity and which metals suit sensitive skin.', 'SUPPORTING_SECTION', [219], links=['EDU-4C-05']),
  S('S07', 'H2', 'Best metal for engagement rings and wedding bands', 'Guide the choice by lifestyle, look and upfront vs long-term cost.', 'DECISION_FRAMEWORK', [216], [104], q=r'best for wedding bands|metal is best',
    links=['COM-ER', 'COM-WB']),
  S('S08', 'H2', 'Alternative metals: tungsten and titanium', 'Give short pros and cons of tungsten and titanium, including that they cannot be resized.', 'PROS_CONS (short)', [221, 225],
    q=r'tungsten|titanium|iridium', links=['EDU-RJG-03'], note='Catalogue evidence for these metals is missing: general information only, no product claims. EDU-RJG-03 is CONDITIONAL. Resizing detail owned by EDU-RJG-02 (no Stage 16 link from here).'),
  S('S09', 'H2', 'Mixing gold and silver', 'Answer whether mixing metals works and how to do it.', 'SUPPORTING_SECTION', [220], q=r'gold and silver|silver bracelet|tacky'),
  S('S10', 'H2', 'FAQ', 'Short answers to remaining metal questions.', 'FAQ', []),
 ],
 'EDU-MET-01': [
  S('S01', 'H1', '14k vs 18k gold (working H1 + answer-first)', 'Open with a concise conditional answer (which suits daily wear vs richer colour) before the detail.', 'ANSWER-FIRST SUMMARY', [293], [99 + 1],
    v=['14k vs 18k gold'], q=r'^is 18k gold or 14k|^which karat', imp='CRITICAL', add='Answer-first comparison verdict', aeo='18.5: COMPARISON SERP; AI Overview runs purity -> colour -> durability -> price -> hypoallergenic.'),
  S('S02', 'H2', '14k vs 18k at a glance', 'Provide a key-differences comparison table.', 'COMPARISON_TABLE', [233], [105], v=['14k vs 18k gold'],
    cmp='Rows: gold purity (%); colour; durability/scratch resistance; price and melt value; skin sensitivity. Columns: 10k (optional) | 14k | 18k.'),
  S('S03', 'H2', 'Purity: what karat means', 'Explain karat purity (10k, 14k, 18k), clear up karat vs carat, and place 22k/24k in context.', 'CORE_SECTION', [228, 237, 238], [101],
    q=r'14k diamond|24k|high quality'),
  S('S04', 'H2', 'Colour and appearance', 'Explain colour richness by karat.', 'SUPPORTING_SECTION', [230], [103]),
  S('S05', 'H2', 'Durability for everyday wear', 'Explain wear and softness by karat for rings worn daily.', 'CORE_SECTION', [229], [102], q=r'daily wear|everyday|lasts? longer|too soft|disadvantages of 18k|wear 14k'),
  S('S06', 'H2', 'Price and value, including resale', 'Explain price difference and resale/melt value by karat, without live gold prices.', 'SUPPORTING_SECTION', [231, 236], [104, 106],
    q=r'worth more|worth buying|worth getting', note='No live gold prices; describe proportional gold content instead.'),
  S('S07', 'H2', 'Skin sensitivity', 'Explain allergy considerations by karat.', 'INLINE_ANSWER', [234], [107]),
  S('S08', 'H2', 'Where 10k gold fits', 'Explain 10k gold and whether it is worth buying.', 'SUPPORTING_SECTION', [235], q=r'10k'),
  S('S09', 'H2', 'Which should you choose?', 'Guide the decision by use (engagement ring, daily wear, look).', 'DECISION_FRAMEWORK', [232], q=r'better', links=['COM-ER', 'COM-WB', 'EDU-4C-05']),
  S('S10', 'H2', 'FAQ', 'Short answers, including how gold stamps/hallmarks work.', 'FAQ', [240], [108], q=r'fake'),
 ],
 'EDU-RJG-01': [
  S('S01', 'H1', 'Ring settings guide (working H1 + definition)', 'Open with what a setting is (and setting vs mounting).', 'DEFINITION_BLOCK', [244, 294], [117], imp='CRITICAL', add='Setting definition',
    note='OWNERSHIP_REVIEW_REQUIRED: "engagement ring settings" SERP is MIXED/commercial-led (CL185-117). Stage 15 owner unchanged (EDU-RJG-01).', aeo='18.5: AI Overview defines settings, then lists types.'),
  S('S02', 'H2', 'Types of ring settings (with pictures)', 'Show each setting type (prong, bezel, pave, halo, channel, tension, three-stone, cathedral, solitaire) with an image and one distinguishing trait.',
    'TYPE_LIST + VISUAL_CHART (settings chart)', [241, 243], [118, 120], v=['engagement ring settings'], q=r'different diamond settings'),
  S('S03', 'H2', 'Sparkle vs security: choosing by lifestyle', 'Explain the trade-off between showing off the stone and protecting it.', 'CORE_SECTION', [242], [119], q=r'best|show off'),
  S('S04', 'H2', 'The most popular engagement ring settings', 'Name the commonly chosen settings briefly and why.', 'SHORT TYPE_LIST', [], [122], q=r'popular', add='Most popular setting (18.5 PAA)', links=['EDU-SHP-00']),
  S('S05', 'H2', 'Settings by jewellery type', 'Explain setting choices for engagement rings, necklaces and stud earrings.', 'SUPPORTING_SECTION', [245], q=r'stud'),
  S('S06', 'H2', 'Details that change the look: profile, halo and milgrain', 'Explain high vs low profile, how a halo affects apparent size, and milgrain.', 'INLINE_ANSWERS', [246, 247, 248], q=r'halo'),
  S('S07', 'H2', 'Explore setting styles', 'Hand off to side-stone and style collections at the decision point.', 'DECISION POINT + CTA', [250, 251], [121],
    links=['COM-ER-SIDESTONE', 'COM-ER', 'COM-ER-STYLES', 'BLOG-CRAFT'],
    note='Commercial "setting only" demand exists (CL185-121) but commercial ownership needs a separate decision. COM-ER-STYLES CTA is CONDITIONAL.'),
  S('S08', 'H2', 'FAQ', 'Short answer to the breathing-holes myth.', 'FAQ', [249], q=r'breathe'),
 ],
 'EDU-RJG-02': [
  S('S01', 'H1', 'How to find your ring size (working H1 + answer-first)', 'Open with a short answer: the quickest reliable ways to find a ring size.', 'ANSWER-FIRST SUMMARY', [303, 295], [123, 124],
    v=['ring size chart', 'how to measure ring size'], q=r'find out my ring size', imp='CRITICAL', add='Answer-first sizing summary',
    aeo='18.5: AI Overviews on both ring-size SERPs (US size table; numbered steps).'),
  S('S02', 'H2', 'Ring size chart', 'Provide a US ring size table with inner diameter and inner circumference in millimetres; answer size-to-dimension questions.', 'VISUAL_CHART / TABLE',
    [253], [125], v=['ring size chart'], q=r'how big is', cmp='Columns: US size | inner circumference (mm) | inner diameter (mm); optional inches.'),
  S('S03', 'H2', 'How to measure your ring size at home', 'Give numbered steps for the paper/string method and the existing-ring method.', 'STEP_SEQUENCE (numbered)', [252], [127], v=['how to measure ring size'],
    q=r'calculate|measure my finger'),
  S('S04', 'H2', 'Tips for an accurate fit', 'Give accuracy tips: time of day, temperature, band width, rounding up between sizes.', 'FACTUAL_LIST', [256], [128 + 0, 130, 132][1:]),
  S('S05', 'H2', 'International sizes and unit conversions', 'Provide conversions to other size systems and units.', 'COMPARISON_TABLE (conversion)', [], [128],
    add='International and unit conversions (18.5 related searches)', cmp='US to UK/AU letters, EU/ISO, Japan; mm, cm, inches.'),
  S('S06', 'H2', "Men's vs women's ring sizes", "Answer whether men's and women's sizes differ and typical ranges.", 'CORE_SECTION (short)', [255], [126], q=r'mens and womens'),
  S('S07', 'H2', 'Ring sizers and measuring on your phone', 'Explain printable and virtual sizers and their accuracy.', 'INTERACTIVE_TOOL / printable sizer', [258], [129], q=r'phone|virtual',
    note='Stage 14/15: tool embedded by default; EDU-RJG-05 conditional (no separate page, no link).'),
  S('S08', 'H2', 'Resizing a ring', 'Explain which rings can be resized up or down and which metals cannot; link to HOD\'s resizing policy.', 'SUPPORTING_SECTION', [254, 257, 259], [131],
    q=r'resized|smaller|cut off', links=['SUP-FAQ', 'COM-ER', 'COM-WB'], note='18.5 WEAKENED resizing (CRITICAL -> IMPORTANT). HOD policy stays on SUP-FAQ.'),
 ],
 'EDU-GEN-01': [
  S('S01', 'H1', 'What are diamonds made of? (working H1 + definition)', 'Open with a direct answer: diamonds are pure carbon in a crystal lattice.', 'DEFINITION_BLOCK', [260, 304], [134, 135],
    v=['what are diamonds made of'], q=r'what are (real )?diamonds made of', imp='CRITICAL', aeo='18.5: AI Overview opens "pure carbon", then atomic structure.'),
  S('S02', 'H2', 'Crystal structure and bonding', 'Explain the lattice and bonding and classify diamond as a mineral/crystal.', 'SUPPORTING_SECTION', [261, 267], [136, 137], q=r'mineral|crystal'),
  S('S03', 'H2', 'Trace elements and diamond types', 'Explain trace nitrogen/boron and Type IIa briefly.', 'INLINE_ANSWERS', [269], [139], add='Trace elements (18.5 new evidence)'),
  S('S04', 'H2', 'Diamond, graphite and other forms of carbon', 'Compare diamond with graphite and other carbon forms; address the coal question in one line and link.', 'COMPARISON (short)', [270], [138],
    links=['EDU-NAT-00'], note='Coal myth depth is owned by EDU-NAT-00.'),
  S('S05', 'H2', 'Hardness: Mohs 10', 'Explain hardness, what (if anything) is harder, scratching and what cuts a diamond.', 'CORE_SECTION', [262, 264, 268],
    q=r'stronger|scratch|water cut'),
  S('S06', 'H2', 'Toughness: can diamonds chip or break?', 'Explain the difference between hardness and toughness and when diamonds chip.', 'CORE_SECTION', [263], q=r'break'),
  S('S07', 'H2', 'Are lab-grown diamonds as hard?', 'State hardness parity for lab-grown diamonds briefly.', 'INLINE_ANSWER', [266], q=r'as hard', links=['EDU-LG-08', 'EDU-RJG-03']),
  S('S08', 'H2', 'FAQ', 'Short answers on melting and general diamond facts.', 'FAQ', [265, 271], [141], q=r'melt|rarer'),
 ],
 'COM-ER-SIDESTONE': [
  S('S01', 'H1', 'Side-stone engagement rings (category H1 + intro copy)', 'Write a short category intro that says what a side-stone engagement ring is (category copy, not an article).', 'CATEGORY_COPY', [272],
    q=r'what is a side stone|called', imp='CRITICAL', note='URL /engagement-rings/by-desgin/side-stone-rings is preserved (ranking equity).'),
  S('S02', 'CATEGORY_BLOCK', 'Side-stone styles', 'Name the side-stone styles (three-stone, baguette/tapered, pave, halo) in short category copy; the product grid carries the page.', 'CATEGORY_COPY', [273, 275],
    q=r'benefits'),
  S('S03', 'CATEGORY_BLOCK', 'What to consider', 'Short buying considerations: centre shape, metal, total carat weight.', 'CATEGORY_COPY', [274, 276, 277]),
  S('S04', 'CATEGORY_BLOCK', 'Learn more (Education links)', 'Link to the settings and shapes guides in one line each; do not re-explain them.', 'LINK_BLOCK', [279, 278], links=['EDU-RJG-01', 'EDU-SHP-00'],
    note='Natural vs lab-grown (EDU-LG-02) has no Stage 16 link from this category: mention only if needed.'),
 ],
 'COM-PDP-OVAL-FLORAL': [
  S('S01', 'H1', 'Product name H1 + design description', 'Describe the design (oval centre with marquise side stones) in product copy.', 'PRODUCT_COPY', [280], imp='IMPORTANT',
    note='URL /shop/oval-floral-diamond-ring is preserved (ranking equity).'),
  S('S02', 'PRODUCT_BLOCK', 'Specifications', 'List stone origin, carat, metal options and certificate once the business confirms each.', 'SPEC_TABLE', [281], imp='CRITICAL',
    note='A PDP cannot ship without its specifications (BLOCKING business fact).'),
  S('S03', 'PRODUCT_BLOCK', 'Guides for this ring', 'Link to ring size, shapes and 4Cs guides (max 3 Education links per PDP, Stage 16).', 'LINK_BLOCK', [], q=r'marquise diamond more expensive',
    links=['EDU-RJG-02', 'EDU-SHP-00', 'EDU-4C-00', 'COM-PDP']),
 ],
}

# Explicit change-log refs are only needed for 18.5 rows that are not tied to a Stage 18 gap (NEW_EVIDENCE);
# gap-linked rows attach automatically through the gap. Set them explicitly here and check the target matches.
EXPLICIT_CL = {
 ('EDU-LG-00', 'S06'): [9], ('EDU-LG-05', 'S03'): [18], ('EDU-LG-08', 'S02'): [19], ('EDU-LG-08', 'S03'): [34], ('EDU-LG-08', 'S08'): [35],
 ('EDU-LG-07', 'S02'): [27], ('EDU-LG-07', 'S04'): [25], ('EDU-LG-07', 'S05'): [26], ('EDU-LG-07', 'S06'): [28],
 ('EDU-NAT-00', 'S04'): [41, 140], ('EDU-NAT-00', 'S08'): [42], ('EDU-4C-00', 'S07'): [55], ('EDU-4C-00', 'S09'): [54],
 ('EDU-4C-05', 'S07'): [64], ('EDU-4C-07', 'S02'): [69, 70], ('EDU-4C-07', 'S03'): [72], ('EDU-4C-07', 'S07'): [71],
 ('EDU-SHP-00', 'S04'): [88], ('EDU-CERT-00', 'S03'): [98], ('EDU-CERT-00', 'S07'): [97, 99], ('EDU-MET-01', 'S10'): [108],
 ('EDU-MET-00', 'S03'): [115, 116], ('EDU-MET-00', 'S04'): [109], ('EDU-RJG-01', 'S04'): [122], ('EDU-RJG-02', 'S02'): [133],
 ('EDU-RJG-02', 'S04'): [132], ('EDU-RJG-02', 'S05'): [128], ('EDU-GEN-01', 'S03'): [139], ('EDU-GEN-01', 'S08'): [141],
}
for t, secs in OUTLINES.items():
    for s in secs:
        s['cl'] = [f'CL185-{c:03d}' for c in EXPLICIT_CL.get((t, s['sid']), [])]
        for c in s['cl']:
            r = CLID[c]
            assert not r['affected_gap_id'].startswith('G18-') and r['affected_target_id'] == t, (t, s['sid'], c)
CL_IN_BOUNDARY = {'CL185-079'}  # non-jewellery "diamond cut" senses: EXCLUDED boundary, not a section

# ------------------------------------------------------------------ 18.5 PAA questions: classification per target
Q185_CLASS = {
 'Are lab diamonds like real diamonds?': ('INLINE_ANSWER', 'S05'), 'Is it worth buying lab grown diamonds?': ('INLINE_ANSWER', 'S06'),
 'What are the disadvantages of lab grown diamonds?': ('INLINE_ANSWER', 'S06'), 'Will a diamond tester say a lab-grown diamond is real?': ('INLINE_ANSWER', 'S05'),
 'What are the downsides of lab-grown diamonds?': ('NOT_NEEDED', 'owned by EDU-LG-02 pros/cons (interim home for EDU-LG-06)'),
 'What do Jewellers think of lab diamonds?': ('NOT_NEEDED', 'perception owned by EDU-LG-02 FAQ'),
 'Do rich people buy lab diamonds?': ('NOT_NEEDED', 'perception owned by EDU-LG-02 FAQ'),
 'What is the lifespan of a lab diamond?': ('FAQ', 'S09'),
 'Can a jeweler tell if a diamond is lab or natural?': ('NOT_NEEDED', 'detection owned by EDU-LG-09'),
 'Is making lab grown diamonds bad for the environment?': ('CORE_SECTION', 'S03'),
 'Why do jewelers not like lab diamonds?': ('NOT_NEEDED', 'perception owned by EDU-LG-02 FAQ'),
 'What is the most ethical diamond?': ('SUPPORTING_SECTION', 'S06'),
 'What is the downside of a lab grown diamond?': ('NOT_NEEDED', 'owned by EDU-LG-02 pros/cons'),
 'Do lab diamonds lose their sparkle?': ('SUPPORTING_SECTION', 'S04'),
 'Why do jewelers hate lab grown diamonds?': ('NOT_NEEDED', 'perception owned by EDU-LG-02 FAQ'),
 'What is 1000 times rarer than a diamond?': ('NOT_NEEDED', 'trivia; off-topic for formation'),
 'Do diamonds start as coal?': ('SUPPORTING_SECTION', 'S04'), 'Is the earth still creating diamonds?': ('FAQ', 'S08'),
 'How long does a diamond take to form?': ('INLINE_ANSWER', 'S02'),
 'What is the 5th C of diamonds?': ('INLINE_ANSWER', 'S09'),
 'How big a diamond will $10,000 buy?': ('INLINE_ANSWER', 'S07'),
 "How many carats is Kim Kardashian's ring?": ('NOT_NEEDED', 'celebrity trivia'),
 'How much is a 4 CT diamond worth?': ('NOT_NEEDED', 'live price question; no hard-coded prices (Stage 13)'),
 'What is the best color of a diamond?': ('CORE_SECTION', 'S04'), 'What is better, a VS1 or VS2 diamond?': ('NOT_NEEDED', 'owned by EDU-4C-01 (interim home for EDU-4C-04)'),
 'Which diamond color is better, D or G?': ('SUPPORTING_SECTION', 'S05'), 'Which diamond color is the least valuable?': ('FAQ', 'S08'),
 'What is the perfect diamond carat size?': ('SUPPORTING_SECTION', 'S04'), 'How many carats is a $5000 diamond?': ('INLINE_ANSWER', 'S07'),
 'Is a 2 carat diamond a big diamond?': ('CORE_SECTION', 'S04'),
 'What is a diamond cut called?': ('INLINE_ANSWER', 'S02'), 'What does it mean if something is diamond cut?': ('NOT_NEEDED', 'non-jewellery sense of "diamond cut" (CL185-079)'),
 'Which cut is best in diamonds?': ('SUPPORTING_SECTION', 'S07'), 'Which diamond cut is the cheapest?': ('FAQ', 'S08'),
 'What are the different shapes of diamonds called?': ('CORE_SECTION', 'S02'), 'Which shape of diamond is most expensive?': ('INLINE_ANSWER', 'S06'),
 'What is a divorce ring?': ('NOT_NEEDED', 'off-topic'), 'What is the prettiest diamond shape?': ('INLINE_ANSWER', 'S05'),
 'How do you get a diamond certificate?': ('SUPPORTING_SECTION', 'S07'), 'What does a diamond certificate mean?': ('CORE_SECTION', 'S01'),
 'What are the top 5 diamond certifications?': ('SUPPORTING_SECTION', 'S03'), 'How do I check my diamond certificate?': ('CORE_SECTION', 'S05'),
 'What are the disadvantages of 18k gold?': ('SUPPORTING_SECTION', 'S05'), 'Can you wear 14k gold everyday?': ('SUPPORTING_SECTION', 'S05'),
 'Does 14k or 18k gold last longer?': ('SUPPORTING_SECTION', 'S05'), 'Can gold be fake if it says 14k?': ('FAQ', 'S10'),
 'Which is better, platinum or white gold?': ('CORE_SECTION', 'S03'), 'What is the most expensive, white gold or platinum?': ('INLINE_ANSWER', 'S03'),
 'What are the disadvantages of platinum?': ('SUPPORTING_SECTION', 'S03'), 'What is the disadvantage of white gold?': ('SUPPORTING_SECTION', 'S03'),
 'Which setting is best for an engagement ring?': ('SUPPORTING_SECTION', 'S03'), 'What is the 2:1:1 rule for wearing jewelry?': ('NOT_NEEDED', 'styling trivia; off-topic'),
 'How much should I spend on an engagement ring if I make $100,000 a year?': ('NOT_NEEDED', 'budget advice; engagement-ring buying guide EDU-RJG-04 is deferred'),
 'What is the most popular setting for an engagement ring?': ('SUPPORTING_SECTION', 'S04'),
 'How do I calculate my ring size?': ('CORE_SECTION', 'S03'), 'Can I measure my ring size on my phone?': ('SUPPORTING_SECTION', 'S07'),
 'How do I measure my finger ring size?': ('CORE_SECTION', 'S03'), 'Is there a virtual ring sizer?': ('SUPPORTING_SECTION', 'S07'),
 'How big is a 7 ring size?': ('INLINE_ANSWER', 'S02'), 'Can I measure a ring with my phone?': ('SUPPORTING_SECTION', 'S07'),
 'How big is a size 9 ring in inches?': ('INLINE_ANSWER', 'S02'), 'How can I find out my ring size?': ('CORE_SECTION', 'S01'),
 'What are real diamonds made of?': ('CORE_SECTION', 'S01'), 'Is coal under pressure a diamond?': ('INLINE_ANSWER', 'S04'),
 "What is a poor man's diamond called?": ('NOT_NEEDED', 'simulant naming; Gemstones & Alternatives hub is conditional'),
 'Is a diamond rarer than gold?': ('FAQ', 'S08'),
}

Q185_PAGE_CLASS = {('EDU-LG-05', 'What is the lifespan of a lab diamond?'): ('NOT_NEEDED', 'lifespan owned by EDU-LG-08 (same PAA on the cloudiness SERP)')}

# Stage 18 question overrides (only where Stage 19 changes the Stage 18 treatment). Reason recorded in the decision log.
Q18_OVERRIDE_NOT_NEEDED = {}  # none: every Stage 15-owned question keeps a home (the iridium question is answered inline in EDU-MET-00 S08)

KNOWN_PAGES = set(TARGETS) | {r['page_id'] for r in rd('architecture/16_page_link_requirements.csv')} | \
    {r['topic_id'] for r in rd('architecture/14_education_architecture.csv')}

# ------------------------------------------------------------------ helpers
def sev_rank(s):
    return SEV_ORDER.index(s)


def status_of(t):
    s = REG[t]['status']
    base = 'EXISTING_PAGE' if REG[t]['existing_or_proposed'] == 'EXISTING' else 'FUTURE_PAGE'
    return f'{base} (Stage 15: {s})'


def url_of(t):
    r = REG[t]
    cur = r['existing_url'] or ''
    prop = r['proposed_url'] or ''
    if cur and prop and prop != '(stays at existing URL)':
        return f'current: {cur} | proposed: {prop}'
    if cur:
        return f'current: {cur} (stays at existing URL)' if prop == '(stays at existing URL)' else f'current: {cur}'
    return f'proposed: {prop}'


LINKS_BY_SRC = defaultdict(list)
LINKS_BY_TGT = defaultdict(list)
for i, r in enumerate(L16, 1):
    r['_row'] = f'L16-{i:03d}'
    LINKS_BY_SRC[r['source_page_id']].append(r)
    LINKS_BY_TGT[r['target_page_id']].append(r)


def stage16_link(src, tgt):
    rows = [r for r in LINKS_BY_SRC[src] if r['target_page_id'] == tgt]
    ctx = [r for r in rows if r['link_type'] in CONTEXTUAL]
    return ctx, [r for r in rows if r['link_type'] not in CONTEXTUAL]


AVOID = defaultdict(set)
for a in ANCH:
    if a['avoid_anchor']:
        AVOID[a['target_page_id']].add(a['avoid_anchor'])

# ------------------------------------------------------------------ question placement
FALLBACK_LOG, DEDUP_LOG, CROSS_NN_LOG = [], [], []


def place_questions(t, secs):
    placed = defaultdict(list)   # sid -> list of (qid, class, text, source)
    nn = []
    faq_sid = next((s['sid'] for s in secs if s['heading'] == 'FAQ'), None)
    stats = {'faq_to_inline': 0, 'override_not_needed': 0}
    owner_sec = {}
    for s in secs:
        for g in s['gaps']:
            o = GAP[g]['owner_page_id']
            if o != t:
                owner_sec.setdefault(o, s['sid'])
    qs = [q for q in QCOV if q['target_page_id'] == t]
    for q in qs:
        text = q['question']
        cls = q['recommended_treatment']
        src = q['_id']
        if text in Q18_OVERRIDE_NOT_NEEDED:
            nn.append((src, 'NOT_NEEDED', text, 'Stage 19 override: ' + Q18_OVERRIDE_NOT_NEEDED[text]))
            stats['override_not_needed'] += 1
            continue
        if cls == 'NOT_NEEDED':
            nn.append((src, 'NOT_NEEDED', text, q['notes'][:120] or 'Stage 18 NOT_NEEDED'))
            continue
        target_sid = None
        for s in secs:
            if s['q'] and s['heading'] != 'FAQ' and re.search(s['q'], text.lower()):
                target_sid = s['sid']
                break
        if target_sid and cls == 'FAQ':
            cls = 'INLINE_ANSWER'
            stats['faq_to_inline'] += 1
        if not target_sid and faq_sid:
            fs = next(s for s in secs if s['sid'] == faq_sid)
            if fs['q'] and re.search(fs['q'], text.lower()):
                target_sid = faq_sid
                if cls != 'FAQ':
                    stats['to_faq'] = stats.get('to_faq', 0) + 1
                cls = 'FAQ'
        if not target_sid:
            if cls == 'FAQ' and faq_sid:
                target_sid = faq_sid
            elif q['owner_page_id'] != t and q['owner_page_id'] in owner_sec:
                target_sid = owner_sec[q['owner_page_id']]
            elif q['owner_page_id'] != t and any(q['owner_page_id'] in s['links'] for s in secs):
                target_sid = next(s['sid'] for s in secs if q['owner_page_id'] in s['links'])
            elif q['owner_page_id'] != t:
                nn.append((src, 'NOT_NEEDED', text, f"Stage 19: PAA surfaced on this page's SERP but owned by {q['owner_page_id']} with no relationship on this page"))
                stats['cross_owner_not_needed'] = stats.get('cross_owner_not_needed', 0) + 1
                CROSS_NN_LOG.append((t, src, text, q['owner_page_id']))
                continue
            elif cls == 'FAQ' and not faq_sid:
                cls = 'INLINE_ANSWER'
                target_sid = secs[0]['sid']
            else:
                # remaining questions are answered in the answer-first block
                target_sid = secs[0]['sid']
                FALLBACK_LOG.append((t, src, text, cls))
        if cls == 'CATEGORY_COPY' and not t.startswith('COM-'):
            cls = 'INLINE_ANSWER'
        placed[target_sid].append((src, cls, text, q['source']))
    # 18.5 PAA questions
    seen_q = {re.sub(r'[^a-z0-9 ]', '', q['question'].lower()): q['_id'] for q in qs}
    for kw, vr in V185_BY_KW.items():
        if V185_TARGET.get(kw) != t:
            continue
        for text in [x.strip() for x in vr['recurring_questions'].split(';') if x.strip()]:
            cls, where = Q185_PAGE_CLASS.get((t, text), Q185_CLASS[text])
            src = f'V185:{kw}'
            norm = re.sub(r'[^a-z0-9 ]', '', text.lower())
            if norm in seen_q:
                DEDUP_LOG.append((t, src, text, seen_q[norm]))
                continue
            seen_q[norm] = src
            if cls == 'NOT_NEEDED':
                nn.append((src, 'NOT_NEEDED', text, where))
            else:
                if where == 'S08' and t == 'EDU-LG-08':
                    where = 'S09'
                placed[where].append((src, cls, text, f'18.5 PAA on "{kw}"'))
    return placed, nn, stats


# ------------------------------------------------------------------ entity placement
ENT_ALIASES = {
 'CVD (chemical vapour deposition)': ['cvd'], 'HPHT (high pressure, high temperature)': ['hpht'], 'Mohs hardness scale': ['mohs', 'hardness', 'durab'],
 'The 4Cs': ['4cs', '4c'], 'FL / IF (flawless)': ['flawless', ' fl ', 'if and fl', 'fl to'], 'VVS1 / VVS2': ['vvs'], 'VS1 / VS2': ['vs1', 'vs '],
 'SI1 / SI2 / SI3': ['si1', 'si ', 'si3'], 'I1 / I2 / I3': ['i3', 'i1'], 'Brilliance / fire / scintillation': ['sparkle', 'light performance', 'brillian'],
 'Colour grades D-Z': ['colour', 'color', 'd-to-z'], 'Cut grade scale (Excellent/Ideal to Poor)': ['cut grade', 'cut'], 'Carat weight': ['carat', 'size'],
 'Total carat weight (ctw)': ['ctw', 'total carat'], 'Grading report / certificate': ['report', 'certif'], 'Natural (mined) diamond': ['natural', 'mined'],
 'Lab-grown diamond': ['lab-grown', 'lab grown'], 'Nickel (allergen)': ['nickel', 'skin', 'allerg'], 'Karat (gold purity)': ['karat', 'purity'],
 'Rhodium plating': ['rhodium'], 'Sterling silver (925)': ['silver'], 'US ring size': ['ring size', 'chart'], 'Side stones (accent stones)': ['side stone', 'side-stone'],
 'Thermal / electrical diamond tester': ['tester'], 'Spectroscopy / lab screening': ['identif', 'labs'], 'Post-growth treatment': ['treatment'],
 'Inclusions and blemishes': ['inclusion'], 'Eye-clean': ['eye-clean', 'eye clean'], 'Polish and symmetry': ['polish', 'symmetry'], 'Facets': ['facet'],
 'Three-stone / trilogy': ['three-stone'], 'Baguette side stones': ['baguette'], 'Laser inscription': ['inscription'], 'Type IIa': ['type iia'],
 '22k / 24k gold': ['24k', '22k'], 'Mining': ['mining', 'mine'],
}


def ent_label(t, own, req):
    if req == 'REQUIRED':
        return 'MUST_MENTION'
    if own == t:
        return 'SUPPORTING_ENTITY' if req == 'SUPPORTING' else 'OPTIONAL_IF_RELEVANT'
    ctx, struct = stage16_link(t, own)
    if req != 'SUPPORTING':
        return f'OPTIONAL_IF_RELEVANT (owner {own})'
    if ctx:
        return f'MENTION_BRIEFLY_AND_LINK -> {own}'
    if struct:
        return f'MENTION_BRIEFLY (owner {own}; structural link only)'
    return f'MENTION_BRIEFLY (owner {own}; no Stage 16 contextual link)'


def ent_home(t, secs, e):
    keys = ENT_ALIASES.get(e, [e.lower().split(' (')[0].replace(' shape', '').replace(' setting', '')])
    for s in secs:
        blob = (s['heading'] + ' ' + s['purpose'] + ' ' + ' '.join(GAP[g]['concept'] for g in s['gaps']) + ' ' + s['add'] + ' ' + s['cmp']).lower()
        if any(k in blob for k in keys):
            return s['sid']
    return secs[0]['sid']


E185_NORM = {'Natural / mined diamond': 'Natural (mined) diamond', 'HPHT': 'HPHT (high pressure, high temperature)', 'CVD': 'CVD (chemical vapour deposition)',
             'Mohs / hardness': 'Mohs hardness scale', 'Brilliance/fire/scintillation': 'Brilliance / fire / scintillation', 'Carat (0.2 g)': 'Carat weight',
             'Proportions/polish/symmetry': 'Polish and symmetry', 'D-Z colour scale': 'Colour grades D-Z', 'VS1/VS2': 'VS1 / VS2', 'Round': 'Round brilliant shape',
             'Oval': 'Oval shape', 'Princess': 'Princess shape', 'Cushion': 'Cushion shape', 'Emerald cut': 'Emerald cut shape', 'Pear': 'Pear shape',
             'Marquise': 'Marquise shape', 'Radiant': 'Radiant shape', 'Asscher': 'Asscher shape', 'Heart': 'Heart shape', 'Prong': 'Prong setting',
             'Bezel': 'Bezel setting', 'Pavé': 'Pavé setting', 'Halo': 'Halo setting', 'Three-stone': 'Three-stone / trilogy', 'Nickel': 'Nickel (allergen)',
             'Rhodium': 'Rhodium plating', 'FL-I3 clarity': 'Clarity scale FL-I3', 'Moissanite': 'Moissanite', 'Cubic zirconia': 'Cubic zirconia'}
# 18.5 lexicon hits judged irrelevant to the page's searcher need (recorded in the decision log)
E185_SKIP = {('EDU-RJG-02', 'Natural (mined) diamond'), ('EDU-RJG-02', 'Round brilliant shape'), ('EDU-LG-07', 'Carat weight'),
             ('EDU-MET-00', 'Natural (mined) diamond'), ('EDU-MET-00', 'Polish and symmetry'), ('EDU-SHP-00', 'Fancy colour'), ('EDU-RJG-01', '14k gold'),
             ('EDU-4C-07', 'Polish and symmetry')}
ENT_OWNER = defaultdict(lambda: defaultdict(int))
for e in ENT:
    if e['owner_page_id']:
        ENT_OWNER[e['entity']][e['owner_page_id']] += 1
V185_EXTRA_ENT = {}
E185_SKIPPED = []
for kw, vr in V185_BY_KW.items():
    t = V185_TARGET.get(kw)
    for e in [x.strip() for x in vr['recurring_entities'].split(';') if x.strip()]:
        n = E185_NORM.get(e, e)
        if (t, n) in E185_SKIP:
            E185_SKIPPED.append((t, n, kw))
            continue
        V185_EXTRA_ENT.setdefault(t, OrderedDict()).setdefault(n, kw)

# ------------------------------------------------------------------ build
sections_out, registry_out, boundaries_out, facts_out, links_out = [], [], [], [], []
decisions = []
stats = defaultdict(int)
gap_home = {}
control_home = {}
link_place = {}   # (src, tgt, link_type) -> (sid, heading)
EMPTY_FAQ_DROPPED = []

for t in TARGETS:
    secs = OUTLINES[t]
    page = PAGES[t]
    for s in secs:
        for g in s['gaps']:
            assert g not in gap_home, (g, t)
            assert GAP[g]['target_page_id'] == t, (g, t)
            gap_home[g] = (t, s['sid'])
    # outgoing Stage 16 contextual link placement
    out_ctx = [r for r in LINKS_BY_SRC[t] if r['link_type'] in CONTEXTUAL]
    for r in out_ctx:
        tgt = r['target_page_id']
        sid = None
        for s in secs:
            if any(GAP[g]['owner_page_id'] == tgt for g in s['gaps']):
                sid = s['sid']
                break
        if not sid:
            sid = next((s['sid'] for s in secs if tgt in s['links']), page['home'])
        link_place[(t, tgt, r['link_type'], r['_row'])] = sid

for t in TARGETS:
    secs = OUTLINES[t]
    page = PAGES[t]
    reg = REG[t]
    ti = TI.get(t, {})
    placed_q, not_needed_q, qstats = place_questions(t, secs)
    for k, v in qstats.items():
        stats[k] += v
    # entities
    ents = [e for e in ENT if e['target_page_id'] == t]
    ent_by_sec = defaultdict(list)
    for e in ents:
        own = e['owner_page_id'] or t
        ent_by_sec[ent_home(t, secs, e['entity'])].append(f"{ent_label(t, own, e['required_or_supporting'])}: {e['entity']}")
    known = {e['entity'] for e in ents}
    for e, kw in V185_EXTRA_ENT.get(t, {}).items():
        if e not in known:
            owners = ENT_OWNER.get(e)
            own = max(owners, key=owners.get) if owners else t
            lab = ent_label(t, own, 'SUPPORTING')
            ent_by_sec[ent_home(t, secs, e)].append(f'{lab} [18.5 SERP "{kw}"]: {e}')
            stats['entities_185'] += 1
            known.add(e)
    stats['entities_18'] += len(ents)

    critical, important, business, insufficient, dnd = [], [], [], [], []
    dropped = [s['sid'] for s in secs if s['heading'] == 'FAQ' and not s['gaps'] and not placed_q.get(s['sid'])]
    for d in dropped:
        EMPTY_FAQ_DROPPED.append((t, d))
    secs = [s for s in secs if s['sid'] not in dropped]
    for s in secs:
        own_gaps = [g for g in s['gaps'] if GAP[g]['owner_page_id'] == t or GAP[g]['owner_status'] == 'INTERIM_HOME_HERE']
        x_gaps = [g for g in s['gaps'] if g not in own_gaps]
        effs = [EFF[g] for g in own_gaps if EFF[g] in SEV_ORDER[:4]]
        # a brief mention of a concept owned elsewhere can make a section IMPORTANT, never CRITICAL
        effs += ['IMPORTANT_COVERAGE' for g in x_gaps if EFF[g] in ('CRITICAL_COVERAGE', 'IMPORTANT_COVERAGE')]
        imp = s['imp'] or (SEV_SHORT[min(effs, key=sev_rank)] if effs else ('CONDITIONAL' if all(EFF[g] == 'BUSINESS_DEPENDENT' for g in s['gaps']) and s['gaps'] else 'SUPPORTING'))
        if s['heading'] == 'FAQ':
            imp = s['imp'] or ('SUPPORTING' if not effs else SEV_SHORT[min(effs, key=sev_rank)])
        # concepts
        concepts = []
        for g in own_gaps:
            gg = GAP[g]
            if gg['recommended_treatment'] == 'VALIDATE_BEFORE_USE':
                continue
            tag = SEV_SHORT[EFF[g]]
            concepts.append(f"[{tag}] {gg['concept']}")
        for g in x_gaps:
            concepts.append(f"[BRIEF_MENTION -> {GAP[g]['owner_page_id']}] {GAP[g]['concept']}")
        for c in s['cl']:
            cr = CLID[c]
            if not cr['affected_gap_id'].startswith('G18-'):
                concepts.append(f"[18.5 {cr['change_type']}] {cr['new_evidence'][:150]}")
        if s['add']:
            concepts.insert(0, s['add'])
        # questions
        qrows = placed_q.get(s['sid'], [])
        qtxt = '; '.join(f'{qid} [{cls}] {txt}' for qid, cls, txt, _ in qrows)
        for _, cls, _, _ in qrows:
            stats[f'q_{cls}'] += 1
        # evidence
        ev = list(s['gaps'])
        for g in s['gaps']:
            ev += [c for c in CL_BY_GAP.get(g, []) if c not in ev]
        ev += [c for c in s['cl'] if c not in ev]
        ev += [f'V185:{k}' for k in s['v']]
        ev += sorted({qid for qid, _, _, _ in qrows})
        if s['aeo'] and 'S18P' in s['aeo']:
            ev.append(f'S18P:{t}')
        if not ev:
            ev.append(f'S18P:{t}')
        # business facts in section
        bf = []
        for g in s['gaps']:
            gg = GAP[g]
            if EFF[g] == 'BUSINESS_DEPENDENT' or gg['business_dependency']:
                bf.append(f"{g}: {gg['business_dependency'] or gg['concept']}")
        # cross-page owners
        xo = [f"{GAP[g]['owner_page_id']} ({GAP[g]['owner_status']}: {GAP[g]['concept'][:70]})" for g in x_gaps]
        interim = [f"INTERIM_HOME for {GAP[g]['owner_page_id']}" for g in own_gaps if GAP[g]['owner_status'] == 'INTERIM_HOME_HERE']
        # links placed here
        lk = []
        for (src, tgt, lt, row), sid in link_place.items():
            if src == t and sid == s['sid']:
                r = next(x for x in L16 if x['_row'] == row)
                lk.append(f"OUT->{tgt} [{lt}/{r['priority']}] anchor: '{r['recommended_anchor']}'")
        notes = []
        if s['aeo']:
            notes.append('AEO: ' + s['aeo'] + ' SERP evidence suggests this format; it does not assure AI Overview inclusion.')
        if s['note']:
            notes.append(s['note'])
        effn = [EFF_NOTE[g] for g in s['gaps'] if g in EFF_NOTE]
        if effn:
            notes.append('18.5 weight change: ' + '; '.join(effn))
        if reg['existing_or_proposed'] == 'EXISTING':
            notes.append('Existing page: BODY_COVERAGE=UNKNOWN. Brief requirement: ensure this is addressed (the brief makes no claim about current body content).')
        sections_out.append(OrderedDict([
            ('target_page_id', t), ('page_name', reg['target_page_name']), ('page_status', status_of(t)),
            ('section_id', f"{t}:{s['sid']}"), ('heading', s['heading']), ('heading_level', s['lvl']), ('section_purpose', s['purpose']),
            ('importance', imp), ('required_concepts', ' | '.join(concepts)), ('required_questions', qtxt),
            ('required_entities', '; '.join(ent_by_sec.get(s['sid'], []))), ('comparison_requirements', s['cmp']),
            ('format', s['fmt']), ('evidence_source', '; '.join(ev)), ('business_fact_required', ' | '.join(bf)),
            ('cross_page_owner', ' | '.join(xo + interim)), ('internal_link_context', ' | '.join(lk)), ('notes', ' '.join(notes))]))
        stats['sections'] += 1
        if imp == 'CRITICAL':
            critical.append(s['heading'].split(' (working')[0])
        elif imp == 'IMPORTANT':
            important.append(s['heading'].split(' (working')[0])

    # ---- control rows (brief boundaries)
    page_gaps = [g for g in GAPS if g['target_page_id'] == t]
    ins = [g for g in page_gaps if g['gap_severity'] == 'INSUFFICIENT_EVIDENCE']
    for g in ins:
        chg = [CLID[c] for c in CL_BY_GAP.get(g['gap_id'], [])]
        lab = 'SERP VALIDATED WITH CONFLICT by 18.5 (see ownership review)' if any(c['change_type'] == 'CONFLICT' for c in chg) else 'SERP RESOLVED by 18.5'
        status = lab + ' (' + ', '.join(c['_id'] + ' ' + c['change_type'] for c in chg) + '); search volume still unmeasured' if chg else 'UNRESOLVED (no 18.5 SERP for these head terms)'
        insufficient.append(f"{g['gap_id']}: {g['concept'][:110]} -> {status}")
    lowconf_notes = {
        'EDU-LG-00': 'Primary keyword confidence LOW (Stage 17); head term "what are lab grown diamonds" validated by 18.5 but not in the Stage 15 map.',
        'EDU-LG-07': 'Primary keyword confidence LOW (Stage 17).', 'EDU-LG-08': 'Primary keyword confidence LOW (Stage 17); fluorescence absent from the 18.5 SERP.',
        'EDU-4C-00': 'Primary keyword confidence LOW (Stage 17); 4Cs head term validated by 18.5 but not in the Stage 15 map.',
        'EDU-4C-05': 'Primary keyword confidence LOW (Stage 17).', 'EDU-4C-07': 'Primary keyword confidence LOW (Stage 17); no carat head term in the Stage 15 map.',
        'EDU-RJG-02': 'Primary keyword confidence LOW (Stage 17); ring-size head terms validated by 18.5 but not in the Stage 15 map.',
        'EDU-RJG-01': 'engagement ring settings SERP is MIXED/commercial-led (18.5 CONFLICT).',
        'EDU-4C-06': '"diamond cut" SERP meaning is MIXED (cut quality + shape lists).',
    }
    if t in lowconf_notes:
        insufficient.append(lowconf_notes[t])
    xrows = [x for x in XOWN if x['current_target_page_id'] == t]
    # gaps not placed in a content section are homed in a control row
    for g in page_gaps:
        if g['gap_id'] not in gap_home:
            ctl = {'VALIDATE_BEFORE_USE': 'X5', 'AVOID': 'X6', 'BUSINESS_INPUT_REQUIRED': 'X4'}.get(g['recommended_treatment'], 'X3')
            gap_home[g['gap_id']] = (t, ctl)
            control_home[g['gap_id']] = ctl
    for x in xrows:
        dnd.append(f"{x['concept'][:80]} -> {x['actual_owner_page_id']} ({x['relationship']})")
    bus_g = [g for g in page_gaps if g['gap_severity'] == 'BUSINESS_DEPENDENT' or g['business_dependency']]
    for g in bus_g:
        business.append(f"{g['gap_id']}: {g['business_dependency'] or g['concept']}")
    must = [f"{s['sid']} {s['heading'].split(' (working')[0]}" for s in secs if sections_out and any(
        r['section_id'] == f"{t}:{s['sid']}" and r['importance'] == 'CRITICAL' for r in sections_out)]
    should = [f"{s['sid']} {s['heading'].split(' (working')[0]}" for s in secs if any(
        r['section_id'] == f"{t}:{s['sid']}" and r['importance'] == 'IMPORTANT' for r in sections_out)]
    nn_txt = '; '.join(f'{qid} {txt} ({why[:80]})' for qid, _, txt, why in not_needed_q)
    avoid = [g for g in page_gaps if g['recommended_treatment'] == 'AVOID']
    controls = [
        ('X1', 'MUST COVER', 'Sections that must be present for the brief to be met.', ' | '.join(must), ''),
        ('X2', 'SHOULD COVER', 'Sections that should be present; drop only with a recorded reason.', ' | '.join(should), ''),
        ('X3', 'DO NOT DUPLICATE', 'Concepts owned elsewhere: brief mention only, per 19_content_boundaries.csv.', ' | '.join(dnd) or 'No Stage 18 cross-page concept on this page.', ''),
        ('X4', 'BUSINESS FACTS REQUIRED', 'HOD facts needed; never invent them (see 19_business_fact_requirements.csv).', ' | '.join(business) or 'None beyond general trust rules.', ''),
        ('X5', 'INSUFFICIENT EVIDENCE', 'Evidence gaps the writer must not fill with assumptions.', ' | '.join(insufficient) or 'None recorded.', ''),
        ('X6', 'NOT NEEDED / EXCLUDED', 'Questions and angles deliberately left out.', (nn_txt + (' | AVOID: ' + '; '.join(g['concept'] for g in avoid) if avoid else '')) or 'None.', ''),
    ]
    for cid, head, purpose, content, _ in controls:
        ev = []
        if cid == 'X3':
            ev = sorted({g['gap_id'] for g in page_gaps if g['owner_page_id'] != t and g['owner_status'] != 'INTERIM_HOME_HERE'}) or ['18_cross_page_semantic_ownership.csv']
        elif cid == 'X4':
            ev = [g['gap_id'] for g in bus_g] or ['15_target_page_registry.csv business_dependency']
        elif cid == 'X5':
            ev = [g['gap_id'] for g in ins] + [c for g in ins for c in CL_BY_GAP.get(g['gap_id'], [])] or ['17_topic_intelligence.csv evidence_confidence']
        elif cid == 'X6':
            ev = sorted({qid for qid, _, _, _ in not_needed_q}) + [g['gap_id'] for g in avoid] or ['18_question_coverage.csv']
        else:
            ev = ['derived from section rows above']
        sections_out.append(OrderedDict([
            ('target_page_id', t), ('page_name', reg['target_page_name']), ('page_status', status_of(t)),
            ('section_id', f'{t}:{cid}'), ('heading', head), ('heading_level', 'CONTROL'), ('section_purpose', purpose),
            ('importance', 'CONTROL'), ('required_concepts', content), ('required_questions', nn_txt if cid == 'X6' else ''),
            ('required_entities', ''), ('comparison_requirements', ''), ('format', 'BRIEF_CONTROL'), ('evidence_source', '; '.join(ev)),
            ('business_fact_required', content if cid == 'X4' else ''), ('cross_page_owner', content if cid == 'X3' else ''),
            ('internal_link_context', ''), ('notes', '')]))
        stats['control_rows'] += 1

    # ---- registry
    prim = ti.get('primary_keyword', '')
    co = ti.get('co_primary_keywords', '')
    kws = [r for r in DD if r['target_page_id'] == t and r['primary_or_secondary'] in ('PRIMARY', 'SECONDARY')]
    kws.sort(key=lambda r: (r['primary_or_secondary'] != 'PRIMARY', -(int(r['search_volume']) if r['search_volume'].isdigit() else 0)))
    eq_kw = [e['keyword'] for e in EQ if e['mapped_target_id'] == t]
    sec_list = [r['keyword'] for r in kws if r['keyword'] not in (prim, co)][:10]
    sec_list += [k for k in eq_kw if k not in sec_list and k not in (prim, co)]
    v_heads = [kw for kw, tt in V185_TARGET.items() if tt == t]
    eq_rows = [e for e in EQ if e['mapped_target_id'] == t]
    eq_txt = ('PROTECTED: ' + '; '.join(f"{e['keyword']} (pos {e['ranking_position']}, {e['action']})" for e in eq_rows) + f" at {eq_rows[0]['ranking_url']}") if eq_rows else 'None (no Stage 3 ranking keyword mapped to this target)'
    special = {
        'EDU-LG-03': ' | Keep the ranking URL and the CVD-vs-HPHT comparison intent; expand single-method depth inside this page; never create a separate CVD or HPHT page. "cvd/hpht diamond tester" ranks at this URL but stays EXCLUDED from targeting.',
        'EDU-LG-02': ' | Keep the existing URL; strengthen the comparison intent (table, decision framing).',
        'EDU-MET-01': ' | Keep the existing URL (Stage 15 move only when conditions are met).',
        'EDU-LG-10': ' | Keep the existing URL; do not force engagement-ring commercial ownership into this guide.',
        'COM-ER-SIDESTONE': ' | Keep the category URL (including the "by-desgin" path).',
        'COM-PDP-OVAL-FLORAL': ' | Keep the product URL.',
    }
    eq_txt += special.get(t, '')
    own_rev = 'NONE'
    if t == 'EDU-RJG-01':
        own_rev = ('OWNERSHIP_REVIEW_REQUIRED: current Stage 15 owner of the settings cluster = EDU-RJG-01; 18.5 SERP for "engagement ring settings" is MIXED and '
                   'commercial-led (shop pages, popular products, local pack, shopping-oriented AI Overview; CL185-117). The Education guide stays useful for informational '
                   'setting intent. Commercial ownership of the head term needs a separate decision; Stage 19 does not create a second owner or change Stage 15.')
    inv = INV.get(reg['existing_url'], {})
    ex_note = (f"Existing title: \"{inv.get('title', '')}\"; existing H1: \"{inv.get('h1', '')}\". BODY_COVERAGE=UNKNOWN (no body audit); requirements are phrased as 'ensure X is addressed'." if reg['existing_or_proposed'] == 'EXISTING' else 'Future page: no body exists.')
    interim_for = sorted({GAP[g]['owner_page_id'] for s in secs for g in s['gaps'] if GAP[g]['owner_status'] == 'INTERIM_HOME_HERE'})
    notes = [ex_note, 'H1 direction (not final): ' + page['h1']]
    if interim_for:
        notes.append('INTERIM_HOME sections for conditional topics: ' + ', '.join(interim_for) + ' (no separate URL).')
    if v_heads:
        notes.append('18.5-validated head term(s): ' + '; '.join(v_heads) + '. Where absent from the Stage 15 map they are recorded as SERP evidence only; Stage 19 assigns no keyword ownership. Search volume not measured.')
    if reg['proposed_url'] == 'URL_PENDING':
        notes.append('URL_PENDING (Stage 15): titles/URL not finalised.')
    if t == 'EDU-CERT-00':
        notes.append('Stage 15 EXISTING_RETARGET_THEN_MOVE: broaden the IGI-focused article into the certification hub; IGI-only depth (EDU-CERT-03) deferred.')
    registry_out.append(OrderedDict([
        ('target_page_id', t), ('page_name', reg['target_page_name']), ('page_type', reg['page_type']), ('status', status_of(t)),
        ('url', url_of(t)), ('primary_intent', reg['primary_intent']), ('secondary_intent', page['sec_intent']),
        ('primary_keyword', prim + (f' | co-primary: {co}' if co else '')), ('secondary_keywords', '; '.join(sec_list)),
        ('searcher_need', page['need']), ('journey_stages', page['journey']), ('content_depth', page['depth']), ('serp_format', page['serp']),
        ('critical_requirements', ' | '.join(must)), ('important_requirements', ' | '.join(should)),
        ('business_dependencies', ' | '.join(business) or (reg['business_dependency'] if reg['business_dependency'] not in ('', 'None.') else 'None')),
        ('ownership_review', own_rev), ('existing_ranking_equity', eq_txt), ('notes', ' '.join(notes))]))

    # ---- boundaries
    for x in xrows:
        g = next(gg for gg in page_gaps if gg['concept'] == x['concept'] and gg['owner_page_id'] == x['actual_owner_page_id'])
        ctx, struct = stage16_link(t, x['actual_owner_page_id'])
        if x['relationship'] == 'INTERIM_HOME_HERE':
            lr = 'NO (this page is the interim home; the Stage 16 CONDITIONAL link to the future page applies only once it is built)'
        elif x['relationship'] == 'CONDITIONAL_OWNER_NOT_BUILT':
            lr = 'NO (conditional owner not built)' if not ctx else 'CONDITIONAL (Stage 16 conditional link; add only when the page exists)'
        elif ctx:
            lr = f"YES (Stage 16 {ctx[0]['link_type']}/{ctx[0]['priority']}; anchor '{ctx[0]['recommended_anchor']}')"
        elif struct:
            lr = f"STRUCTURAL_ONLY (Stage 16 {struct[0]['link_type']}; no contextual link defined)"
        else:
            lr = 'NO_STAGE16_LINK (mention only; Stage 18 suggested a link; recorded as a Stage 16 review item)'
        sec = gap_home[g['gap_id']][1]
        treat = {'OWNED_ELSEWHERE': 'Brief mention (1-3 sentences) in ' + sec,
                 'COMMERCIAL_PAGE_OWNER': 'Hand-off/CTA only once business facts are confirmed (' + sec + ')',
                 'CONDITIONAL_OWNER_NOT_BUILT': 'One-line mention only if the searcher need requires it (' + sec + '); do not pre-build the topic',
                 'INTERIM_HOME_HERE': 'Self-contained interim section ' + sec + ' until the conditional page is approved'}[x['relationship']]
        boundaries_out.append(OrderedDict([
            ('target_page_id', t), ('concept', x['concept']), ('ownership_status', x['relationship']), ('owner_page_id', x['actual_owner_page_id']),
            ('current_page_treatment', treat), ('do_not_duplicate', x['avoid_treatment']), ('link_required', lr),
            ('evidence', f"{g['gap_id']}; 18_cross_page_semantic_ownership.csv; {x['evidence'][:120]}"),
            ('notes', x['notes'][:200])]))
    # owned-here anchor rows for CRITICAL / IMPORTANT concepts
    for g in page_gaps:
        if g['owner_page_id'] == t and EFF[g['gap_id']] in ('CRITICAL_COVERAGE', 'IMPORTANT_COVERAGE') and g['recommended_treatment'] != 'VALIDATE_BEFORE_USE':
            boundaries_out.append(OrderedDict([
                ('target_page_id', t), ('concept', g['concept']), ('ownership_status', 'OWNED_HERE'), ('owner_page_id', t),
                ('current_page_treatment', f"Full treatment in {gap_home[g['gap_id']][1]} ({SEV_SHORT[EFF[g['gap_id']]]})"),
                ('do_not_duplicate', 'Other pages give at most a brief mention and link here where Stage 16 defines a link.'),
                ('link_required', 'n/a (owner)'), ('evidence', g['gap_id'] + ('; ' + '; '.join(CL_BY_GAP[g['gap_id']]) if CL_BY_GAP.get(g['gap_id']) else '')), ('notes', '')]))
    for g in avoid:
        boundaries_out.append(OrderedDict([
            ('target_page_id', t), ('concept', g['concept']), ('ownership_status', 'EXCLUDED_AVOID'), ('owner_page_id', 'EXCLUDED'),
            ('current_page_treatment', 'Do not cover; do not target.'), ('do_not_duplicate', 'Not covered on any HOD page.'),
            ('link_required', 'NO'), ('evidence', g['gap_id'] + ('; ' + '; '.join(CL_BY_GAP[g['gap_id']]) if CL_BY_GAP.get(g['gap_id']) else '')), ('notes', g['notes'][:150])]))

# ---- extra Stage 15/16/18.5 boundaries (not in the Stage 18 cross-page file)
EXTRA_B = [
 ('EDU-LG-00', 'Commercial head terms "lab grown diamonds" / "lab diamonds"', 'COMMERCIAL_PAGE_OWNER', 'COM-LG-HUB',
  'Do not target these terms or use them as bare anchors; Education framing only.', 'Stage 15 holds the head terms for the conditional commercial hub.', 'NO (commercial hub conditional)', 'Stage 15 target registry EDU-LG-00 business_dependency; Stage 16 linking rules §3.3'),
 ('EDU-LG-03', 'Keyword "cvd/hpht diamond tester" (ranks at this URL, excluded from targeting)', 'EXCLUDED_AVOID', 'EXCLUDED',
  'Keep the URL (equity protected) but do not target or optimise for this keyword; detection is covered on EDU-LG-09 without targeting it.', 'Never add tester-device shopping or tester keywords as headings.', 'NO', '15_ranking_equity_protection.csv (KEEP_EXISTING_URL_NOT_TARGETED)'),
 ('EDU-LG-09', 'Keyword "cvd/hpht diamond tester"', 'EXCLUDED_AVOID', 'EXCLUDED',
  'Do not target; explain tester behaviour generally.', 'No tester-device shopping content.', 'NO', '15_ranking_equity_protection.csv; G18-0092'),
 ('EDU-LG-03', 'Separate single-method CVD or HPHT page', 'OWNED_HERE', 'EDU-LG-03',
  'Single-method heads (hpht lab grown diamond, cvd diamond) are served inside S03/S04 of this page.', 'No other page may target CVD-only or HPHT-only queries.', 'n/a (owner)', 'Stage 15 target registry EDU-LG-03; G18-0045'),
 ('EDU-LG-10', 'Engagement-ring commercial ownership / engagement-ring buying guide', 'CONDITIONAL_OWNER_NOT_BUILT', 'EDU-RJG-04',
  'Do not force engagement-ring commercial ownership into the lab-grown buying guide; one FAQ answer at most.', 'EDU-RJG-04 is deferred; commercial engagement-ring terms belong to COM-ER.', 'NO (deferred topic)', '15_ranking_equity_protection.csv; G18-0102'),
 ('EDU-LG-05', 'Perception questions (what jewellers think, do rich people buy)', 'OWNED_ELSEWHERE', 'EDU-LG-02',
  'Not answered here (18.5 PAA on the value SERP marked NOT_NEEDED).', 'Do not repeat the EDU-LG-02 FAQ set.', 'NO', 'V185:do lab grown diamonds hold their value; 18_question_coverage (EDU-LG-02 FAQ)'),
 ('EDU-LG-08', 'Downsides / perception questions surfaced on the cloudiness SERP', 'OWNED_ELSEWHERE', 'EDU-LG-02',
  'Not answered here (NOT_NEEDED).', 'Do not duplicate pros/cons.', 'NO', 'V185:do lab grown diamonds get cloudy'),
 ('EDU-LG-07', 'Detection question surfaced on the ethics SERP', 'OWNED_ELSEWHERE', 'EDU-LG-09', 'Not answered here (NOT_NEEDED).',
  'Do not duplicate detection content.', 'NO', 'V185:are lab grown diamonds ethical'),
 ('EDU-GEN-01', 'Coal myth ("Is coal under pressure a diamond?")', 'OWNED_ELSEWHERE', 'EDU-NAT-00', 'One-line answer in S04 and link (Stage 16 GEN-01 -> NAT-00 CONTEXTUAL).',
  'Full myth check lives on EDU-NAT-00 S04.', 'YES (Stage 16 CONTEXTUAL/RECOMMENDED)', 'CL185-140; CL185-041'),
 ('EDU-4C-00', 'Budget-to-size questions ("How big a diamond will $10,000 buy?")', 'OWNED_ELSEWHERE', 'EDU-4C-07', 'Not answered on the pillar; carat guide S07 answers without live prices.',
  'No price figures on the 4Cs pillar.', 'YES (Stage 16 CONTEXTUAL/REQUIRED 4C-00 -> 4C-07)', 'CL185-055'),
 ('EDU-4C-05', 'VS1 vs VS2 question surfaced on the colour SERP', 'OWNED_ELSEWHERE', 'EDU-4C-01', 'Not answered here (NOT_NEEDED).',
  'VS grades live on EDU-4C-01 S05 (interim home for EDU-4C-04).', 'NO_STAGE16_LINK', 'V185:diamond color chart'),
 ('EDU-4C-06', 'Non-jewellery senses of "diamond cut" (grillz, vegetables)', 'EXCLUDED_AVOID', 'EXCLUDED', 'Do not cover.', 'Not covered on any HOD page.', 'NO', 'CL185-079'),
 ('EDU-SHP-00', 'Shape and cut-quality grading', 'OWNED_ELSEWHERE', 'EDU-4C-06', 'Shape page explains shape vs cut in one line and links for cut grading.',
  'Do not reproduce the cut grade scale on the shapes page.', 'YES (Stage 16 CONTEXTUAL/REQUIRED SHP-00 -> 4C-06)', 'G18-0185; G18-0169'),
 ('EDU-RJG-01', 'Commercial "engagement ring settings" / setting-only shopping intent', 'COMMERCIAL_PAGE_OWNER', 'OWNERSHIP_REVIEW_REQUIRED',
  'Education guide keeps informational setting intent; commercial ownership is an open decision (no second owner created).', 'Do not add product listings or prices to the guide.', 'CONDITIONAL (COM-ER-STYLES CTA per Stage 16)', 'CL185-117; CL185-121'),
 ('EDU-RJG-02', 'HOD resizing policy', 'COMMERCIAL_PAGE_OWNER', 'SUP-FAQ', 'Covered already by the Stage 18 cross-page row; general resizing explained here.',
  'No policy wording on the guide.', "YES (Stage 16 CONTEXTUAL/REQUIRED 'our resizing policy')", 'G18-0259'),
]
seen = {(b['target_page_id'], b['concept']) for b in boundaries_out}
for t, c, st, own, treat, dnd_, lr, ev in EXTRA_B:
    if (t, c) in seen:
        continue
    boundaries_out.append(OrderedDict([('target_page_id', t), ('concept', c), ('ownership_status', st), ('owner_page_id', own),
                                       ('current_page_treatment', treat), ('do_not_duplicate', dnd_), ('link_required', lr), ('evidence', ev),
                                       ('notes', 'Stage 19 boundary derived from Stage 15/16 rules or 18.5 evidence; no ownership change.')]))
# RJG-02 extra row duplicates the Stage 18 row concept name differently; drop it if a SUP-FAQ row already exists for the page
boundaries_out = [b for b in boundaries_out if not (b['target_page_id'] == 'EDU-RJG-02' and b['concept'] == 'HOD resizing policy'
                                                     and any(x['target_page_id'] == 'EDU-RJG-02' and x['owner_page_id'] == 'SUP-FAQ' and x['concept'] != 'HOD resizing policy' for x in boundaries_out))]

# ------------------------------------------------------------------ business facts
FACTS = [
 # (target, fact, why, blocking, source)
 ('EDU-LG-00', 'Which lab-grown products HOD sells and whether the commercial lab-grown hub (COM-LG-HUB) will be built', 'Needed before the S07 commercial hand-off can link or name products.', 'NON_BLOCKING', 'HOD catalogue owner; Stage 12/15 conditional hub decision'),
 ('EDU-LG-00', 'HOD growth-method sourcing (CVD/HPHT) and how it is disclosed', 'Only needed if the pillar mentions HOD stones; general process content does not need it.', 'NON_BLOCKING', 'HOD sourcing records / supplier documentation'),
 ('EDU-LG-02', 'Whether HOD offers natural diamonds as well as lab-grown, and where each is sold', 'Needed for the decision-point CTA (S09) so the page does not imply an unavailable option.', 'NON_BLOCKING', 'HOD catalogue; Stage 12 natural commercial hub decision'),
 ('EDU-LG-03', 'Which growth method(s) HOD stones use and how the method is disclosed to buyers (G18-0062)', 'Needed before any statement about HOD stones in S09; the comparison itself can be drafted without it.', 'NON_BLOCKING', 'HOD sourcing records; grading reports showing growth method'),
 ('EDU-LG-05', 'HOD buy-back / trade-in / upgrade policy (G18-0069)', 'Resale section must not imply an HOD policy; the policy belongs on SUP-FAQ.', 'NON_BLOCKING', 'HOD policy owner; published FAQ/policy page'),
 ('EDU-LG-05', 'Dated, sourced price references (if any figure is used)', 'Stage 13 rule: no hard-coded prices; any figure must carry a date and source.', 'NON_BLOCKING', 'Named third-party price index or report with publication date'),
 ('EDU-LG-07', 'Energy source used to grow HOD stones (renewable vs grid mix) and any certification of it (G18-0076)', 'Any HOD environmental or carbon claim must be substantiated; general page can be drafted without HOD claims.', 'NON_BLOCKING', 'Supplier energy documentation; third-party certification (e.g. SCS-007 or equivalent) if claimed'),
 ('EDU-LG-07', 'Any HOD sustainability / ethical-sourcing claim wording', 'Blocks publication of any HOD-specific ethics statement (not the general article).', 'BLOCKING', 'Substantiation file approved by HOD; FTC Green Guides compliance review'),
 ('EDU-LG-08', 'HOD disclosure practice for treated stones (G18-0082)', 'Needed before S06 says anything about HOD stones.', 'NON_BLOCKING', 'HOD sourcing/QA records; grading reports'),
 ('EDU-LG-10', 'Which lab reports come with HOD stones and HOD lab-grown product range (G18-0103)', 'Needed for the S04 report advice to match what HOD provides, and for the S07 hand-off.', 'NON_BLOCKING', 'HOD catalogue; sample grading reports'),
 ('EDU-NAT-00', 'Whether HOD sells natural diamonds (G18-0113)', 'Education page only; determines whether any commercial natural link can ever be added.', 'NON_BLOCKING', 'HOD catalogue owner; Stage 12 D-05 decision'),
 ('EDU-4C-02', 'Whether HOD lists SI-grade stones/products with grades shown (G18-0148)', 'Needed only for any product hand-off from the SI page.', 'NON_BLOCKING', 'HOD product data (grade attributes)'),
 ('EDU-4C-03', 'Whether HOD products show VVS grades; VVS in jewellery types HOD sells (G18-0156)', 'Needed only for any product hand-off from the VVS page.', 'NON_BLOCKING', 'HOD product data (grade attributes)'),
 ('EDU-4C-07', 'HOD loose-stone offer (carat-led shopping is commercial and deferred, G18-0183)', 'Carat guide must not imply a loose-stone shop.', 'NON_BLOCKING', 'HOD catalogue owner; Stage 12 deferred decision'),
 ('EDU-SHP-00', 'Which shapes HOD offers in jewellery; shape x jewellery demand (D-19 unapproved, G18-0194)', 'Needed for shape-to-product hand-offs beyond the oval PDP example.', 'NON_BLOCKING', 'HOD catalogue; D-19 supplement if approved'),
 ('EDU-SHP-00', 'Oval floral PDP is live and in stock', 'Stage 16: product example links only while the product is live.', 'NON_BLOCKING', 'HOD product status'),
 ('EDU-CERT-00', 'Which labs grade HOD stones and whether a report is supplied per product (G18-0205)', 'Needed before the page says what HOD customers receive; the general guide can be drafted without it.', 'NON_BLOCKING', 'Sample HOD grading reports; product data'),
 ('EDU-CERT-01', 'Which lab (GIA, IGI or other) grades HOD lab-grown stones', 'Needed only if the comparison references HOD practice.', 'NON_BLOCKING', 'Sample HOD grading reports'),
 ('EDU-MET-00', 'Which metals and karats HOD offers; platinum availability (G18-0227)', 'Needed for the S07 decision hand-off; general comparison can be drafted without it.', 'NON_BLOCKING', 'HOD catalogue (metal attributes)'),
 ('EDU-MET-00', 'Whether HOD sells tungsten, titanium or other alternative metals (G18-0221)', 'Decides whether S08 stays general or links to products.', 'NON_BLOCKING', 'HOD catalogue'),
 ('EDU-MET-01', 'Which karats HOD offers (10k/14k/18k) (G18-0240)', 'Needed before any statement about HOD karat options.', 'NON_BLOCKING', 'HOD catalogue (metal attributes)'),
 ('EDU-RJG-01', 'HOD setting styles available (engagement style subcategories are conditional, G18-0251)', 'Needed for the S07 COM-ER-STYLES CTA (Stage 16 CONDITIONAL).', 'NON_BLOCKING', 'HOD catalogue; populated subcategories'),
 ('EDU-RJG-01', 'Whether HOD sells settings without a centre stone (setting-only / design-your-own)', 'Input to the OWNERSHIP_REVIEW of "engagement ring settings" (CL185-121); the guide can be drafted without it.', 'NON_BLOCKING', 'HOD product/ordering capability'),
 ('EDU-RJG-02', 'HOD resizing policy (G18-0259)', 'Linked via SUP-FAQ; the guide explains resizing generally.', 'NON_BLOCKING', 'HOD published policy page'),
 ('EDU-RJG-02', 'Whether HOD will provide a printable sizer / embedded ring-size tool', 'Stage 14/15: tool embedded by default; S07 format depends on it.', 'NON_BLOCKING', 'HOD web/product team'),
 ('COM-ER-SIDESTONE', 'Current side-stone assortment (about 4 products) and whether more are planned (G18-0277)', 'Category copy must match the actual grid; thin assortment risks a thin category.', 'BLOCKING', 'HOD catalogue'),
 ('COM-ER-SIDESTONE', 'Whether HOD adds side stones / ring enhancers / bespoke side-stone work (G18-0276)', 'Needed before any "customise" copy or bespoke hand-off.', 'NON_BLOCKING', 'HOD bespoke service owner'),
 ('COM-ER-SIDESTONE', 'Centre-stone origin(s), metals and carat ranges offered in the category', 'Buying-considerations copy must reflect real options.', 'BLOCKING', 'HOD catalogue'),
 ('COM-PDP-OVAL-FLORAL', 'Product specifications: stone origin, centre and side-stone carat, metal options, certificate/lab (G18-0281)', 'A PDP cannot be written without its specifications.', 'BLOCKING', 'HOD product data sheet; grading report'),
 ('COM-PDP-OVAL-FLORAL', 'Available ring sizes and resizing terms for this product', 'Needed for the ring-size link context and product details.', 'NON_BLOCKING', 'HOD product data; policy page'),
]
for t, f, why, blk, src in FACTS:
    facts_out.append(OrderedDict([('target_page_id', t), ('fact', f), ('why_needed', why), ('blocking_status', blk), ('source_required', src),
                                  ('notes', 'Never invent; leave the statement out until supplied.')]))

# ------------------------------------------------------------------ internal link requirements (Stage 16 rows only)
sec_heading = {r['section_id']: r['heading'] for r in sections_out}
for t in TARGETS:
    for r in LINKS_BY_SRC[t]:
        if r['link_type'] not in CONTEXTUAL:
            continue
        sid = link_place[(t, r['target_page_id'], r['link_type'], r['_row'])]
        av = '; '.join(sorted(AVOID.get(r['target_page_id'], [])))
        links_out.append(OrderedDict([
            ('brief_page_id', t), ('direction', 'OUTGOING'), ('stage16_row', r['_row']), ('source_page_id', t), ('target_page_id', r['target_page_id']),
            ('link_type', r['link_type']), ('relationship_type', r['relationship_type']), ('priority', r['priority']), ('required_at_launch', r['required_at_launch']),
            ('anchor_type', r['anchor_type']), ('recommended_anchor', r['recommended_anchor']), ('anchor_variants', r['anchor_variants']), ('avoid_anchor', av),
            ('purpose', r['context_reason']), ('placement_context', f"{t}:{sid} — {sec_heading.get(f'{t}:{sid}', '')}"),
            ('ranking_equity_protection', r['ranking_equity_protection']), ('notes', r['notes'])]))
    for r in LINKS_BY_TGT[t]:
        if r['link_type'] not in CONTEXTUAL:
            continue
        src = r['source_page_id']
        key = (src, t, r['link_type'], r['_row'])
        if key in link_place:
            sid = link_place[key]
            pc = f"On source brief {src}:{sid} — {sec_heading.get(f'{src}:{sid}', '')}"
        else:
            pc = f'On {src} (no Stage 19 brief for the source page): {r["context_reason"]}'
        av = '; '.join(sorted(AVOID.get(t, [])))
        links_out.append(OrderedDict([
            ('brief_page_id', t), ('direction', 'INCOMING'), ('stage16_row', r['_row']), ('source_page_id', src), ('target_page_id', t),
            ('link_type', r['link_type']), ('relationship_type', r['relationship_type']), ('priority', r['priority']), ('required_at_launch', r['required_at_launch']),
            ('anchor_type', r['anchor_type']), ('recommended_anchor', r['recommended_anchor']), ('anchor_variants', r['anchor_variants']), ('avoid_anchor', av),
            ('purpose', r['context_reason']), ('placement_context', pc), ('ranking_equity_protection', r['ranking_equity_protection']), ('notes', r['notes'])]))

# ------------------------------------------------------------------ write
def write(name, rows):
    with open(os.path.join(OUT, name), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


write('19_content_briefs.csv', sections_out)
write('19_brief_registry.csv', registry_out)
write('19_content_boundaries.csv', boundaries_out)
write('19_business_fact_requirements.csv', facts_out)
write('19_internal_link_requirements.csv', links_out)

unplaced = [g['gap_id'] for g in GAPS if g['gap_id'] not in gap_home]
stats['gaps_homed_in_control_rows'] = dict(sorted(control_home.items()))
stats.update({
    'targets': len(registry_out), 'section_rows_total': len(sections_out), 'content_sections': stats['sections'],
    'boundaries': len(boundaries_out), 'business_facts': len(facts_out),
    'business_facts_blocking': sum(1 for f in facts_out if f['blocking_status'] == 'BLOCKING'),
    'link_rows': len(links_out), 'link_rows_outgoing': sum(1 for l in links_out if l['direction'] == 'OUTGOING'),
    'link_rows_incoming': sum(1 for l in links_out if l['direction'] == 'INCOMING'),
    'gaps_placed_in_sections': len(gap_home) - len(control_home), 'gaps_unplaced_in_sections': len(unplaced),
    'gaps_effective': {SEV_SHORT[k]: sum(1 for v in EFF.values() if v == k) for k in SEV_ORDER},
    'weight_changes_applied': len(EFF_NOTE),
    'ownership_reviews': sum(1 for r in registry_out if r['ownership_review'] != 'NONE'),
    'existing_pages': sum(1 for r in registry_out if r['status'].startswith('EXISTING_PAGE')),
    'future_pages': sum(1 for r in registry_out if r['status'].startswith('FUTURE_PAGE')),
    'unplaced_gap_ids': unplaced,
})
json.dump(stats, open(os.path.join(OUT, 'scripts', '19_build_stats.json'), 'w'), indent=1, default=str)
print(json.dumps({k: v for k, v in stats.items() if k != 'unplaced_gap_ids'}, indent=1, default=str))
print('unplaced gaps:', unplaced)
print('empty FAQ dropped:', EMPTY_FAQ_DROPPED)
print('question fallbacks to S01:'); [print('  ', x) for x in FALLBACK_LOG]
print('18.5 duplicate questions:', DEDUP_LOG)
print('18.5 entities skipped:', E185_SKIPPED)
json.dump({'fallback_to_S01': FALLBACK_LOG, 'v185_dedup': DEDUP_LOG, 'e185_skipped': E185_SKIPPED, 'empty_faq_dropped': EMPTY_FAQ_DROPPED, 'cross_owner_not_needed': CROSS_NN_LOG},
          open(os.path.join(OUT, 'scripts', '19_build_log.json'), 'w'), indent=1)
