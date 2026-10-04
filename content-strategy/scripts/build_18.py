#!/usr/bin/env python3
"""Stage 18 — semantic gap analysis.

LOCAL ONLY. Reads accepted Stage 7-17 files and the raw Stage 8 SERP JSON already on disk
(paid for in Stage 8). No DataForSEO or other API call; no live-site request.

Stage 15 is authoritative for keyword ownership, Stage 16 for link relationships and Stage 17
for keyword intelligence. Nothing here changes those. The curated concept lexicon below is
interpretation; a concept is only written out if it is matched to real project evidence
(owned keyword, Stage 8 AI Overview / organic text, routed PAA, related search, Stage 17
concept or gap row). Concepts with no evidence are dropped and logged.

Outputs (content-strategy/):
  18_semantic_gap_register.csv, 18_entity_coverage.csv, 18_question_coverage.csv,
  18_serp_semantic_patterns.csv, 18_cross_page_semantic_ownership.csv,
  18_related_search_classification.csv (supporting), scripts/18_build_stats.json
"""
import collections
import csv
import glob
import json
import os
import re

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
P = lambda *a: os.path.join(BASE, *a)
OUT = P('content-strategy')


def rd(path):
    with open(P(path), newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def wr(name, cols, rows):
    with open(os.path.join(OUT, name), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction='raise')
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, '') for c in cols})


# ---------------------------------------------------------------- upstream
M15 = rd('architecture/15_keyword_url_map.csv')
BYKW = {r['keyword']: r for r in M15}
REG15 = {r['target_id']: r for r in rd('architecture/15_target_page_registry.csv')}
TARGETS = list(REG15)
ARCH14 = {r['topic_id']: r for r in rd('architecture/14_education_architecture.csv')}
PLR16 = {r['page_id']: r for r in rd('architecture/16_page_link_requirements.csv')}
S8 = {r['keyword']: r for r in rd('serp/analysis/08_hod_serp_validation.csv')}
S7 = {r['keyword'] for r in rd('dataforseo/processed/07_hod_master_keyword_database.csv')}
INV10 = {r['url']: r for r in rd('content-strategy/10_existing_content_inventory.csv')}
Q17 = rd('content-strategy/17_question_map.csv')
C17 = rd('content-strategy/17_semantic_concepts.csv')
G17 = rd('content-strategy/17_gap_register.csv')
REL17 = rd('content-strategy/17_keyword_relationships.csv')
OWNER_IDS = set(TARGETS) | set(ARCH14) | set(PLR16)

EXCLUDED_TESTER_KW = 'cvd/hpht diamond tester'   # never used as evidence (Stage 15/16/17 rule)
MAPPED = ('MAP_EXISTING_URL', 'MAP_EXISTING_URL_KEEP', 'MAP_PROPOSED_URL', 'MAP_INTERIM_HOME')

# raw Stage 8 SERPs
SERP = {}
for f in sorted(glob.glob(P('serp/raw/08_stage8_by_id/*.json'))):
    d = json.load(open(f, encoding='utf-8'))
    for t in d.get('tasks') or []:
        for res in t.get('result') or []:
            kw = res.get('keyword')
            items = res.get('items') or []
            aio = '\n'.join((it.get('markdown') or '') for it in items if it.get('type') == 'ai_overview')
            org = [(it.get('title') or '') + ' — ' + (it.get('description') or '')
                   for it in items if it.get('type') == 'organic']
            paa = [q.get('title') for it in items if it.get('type') == 'people_also_ask'
                   for q in (it.get('items') or []) if q.get('title')]
            rel = [(q if isinstance(q, str) else q.get('title')) for it in items
                   if it.get('type') == 'related_searches' for q in (it.get('items') or [])]
            SERP[kw] = dict(aio=aio, org=org, paa=paa, rel=[q for q in rel if q], file=os.path.basename(f))

SERP_TARGET = {}
for kw in SERP:
    r = BYKW.get(kw)
    if kw != EXCLUDED_TESTER_KW and r and r['mapping_disposition'] in MAPPED and r['target_id']:
        SERP_TARGET[kw] = r['target_id']
OWN_SERPS = collections.defaultdict(list)
for kw, t in SERP_TARGET.items():
    OWN_SERPS[t].append(kw)

OWNED_KW = collections.defaultdict(list)
for r in M15:
    if r['mapping_disposition'] in MAPPED and r['target_id']:
        OWNED_KW[r['target_id']].append(r['keyword'])

ROUTED_PAA = collections.defaultdict(list)      # routed, relevant PAA per owner target
for q in Q17:
    if q['source_type'] == 'STAGE8_PAA' and q['recommended_role'] != 'EXCLUDE_OFF_TOPIC':
        ROUTED_PAA[q['target_page_id']].append(q['question'])


def linked(t):
    p = PLR16.get(t, {})
    ids = set()
    for c in ('parent_page_id', 'child_page_ids', 'related_page_ids'):
        ids |= {x.strip() for x in re.split(r'[;,]', p.get(c, '')) if x.strip()}
    return ids & set(TARGETS) - {t}


def existing_text(t):
    url = REG15[t]['existing_url']
    if not url:
        return None
    for u, r in INV10.items():
        if u.endswith(url):
            return (r['title'] + ' | ' + r['h1']).lower()
    return ''


# ---------------------------------------------------------------- concept lexicon
LEX = []


def C(t, concept, gap_type, ctype, role, rx, need, treat, owner=None, anchor=None, biz='', xkey='',
      stage='UNDERSTAND', note='', extra=None):
    LEX.append(dict(t=t, concept=concept, gap_type=gap_type, ctype=ctype, role=role, rx=rx, need=need,
                    treat=treat, owner=owner, anchor=anchor, biz=biz, xkey=xkey, stage=stage, note=note,
                    extra=extra))


HEAD = {
    'EDU-LG-00': ['what are lab grown diamonds', 'lab grown diamonds meaning'],
    'EDU-4C-00': ['4cs of diamonds', 'diamond 4cs', '4 cs of diamonds'],
    'EDU-4C-01': ['diamond clarity chart', 'vs1 diamond', 'vs2 diamond'],
    'EDU-4C-02': ['si1 diamond'],
    'EDU-4C-03': ['vvs diamonds'],
    'EDU-4C-05': ['diamond color chart', 'diamond color scale'],
    'EDU-4C-06': ['diamond cut', 'diamond cut chart'],
    'EDU-4C-07': ['diamond carat', 'diamond carat size chart', 'carat weight'],
    'EDU-SHP-00': ['diamond shapes', 'diamond shapes chart'],
    'EDU-CERT-00': ['igi certification', 'gia certification', 'diamond certificate'],
    'EDU-MET-00': ['white gold vs platinum', 'platinum vs white gold'],
    'EDU-MET-01': ['14k vs 18k gold', '10k vs 14k gold', '14k gold', '18k gold'],
    'EDU-RJG-01': ['engagement ring settings', 'ring settings', 'prong setting', 'bezel setting'],
    'EDU-RJG-02': ['ring size chart', 'ring size guide', 'how to measure ring size', 'ring sizer'],
}
NO_SERP_NOTE = 'No Stage 8 SERP for any keyword owned by this target; page format and section order are unvalidated.'

# --- EDU-LG-00 lab-grown pillar
T = 'EDU-LG-00'
C(T, 'Definition of a lab-grown diamond (what it is)', 'DEFINITION_GAP', 'DEFINITION', 'CORE',
  r'what (is|are) (a )?(lab|synthetic|man[- ]made)|meaning|definition|\bwiki|synthetic diamonds?$', 'Understand what a lab-grown diamond is before any comparison or purchase', 'DEFINITION_BLOCK', xkey='LG_DEFINITION')
C(T, 'Terminology: synthetic / lab-created / man-made / cultured as names for the same thing', 'DEFINITION_GAP', 'TERMINOLOGY', 'CORE',
  r'synthetic|lab[- ]created|man[- ]made|artificial|cultured|called|name', 'Know that the different names describe one product', 'SUPPORTING_SECTION', xkey='LG_TERMINOLOGY')
C(T, 'FTC labelling of lab-grown diamonds', 'TRUST_EVIDENCE_GAP', 'TRUST', 'SUPPORT', r'\bftc\b', 'Trust that the labelling is regulated and honest', 'INLINE_ANSWER', stage='VERIFY')
C(T, 'Types of lab-grown diamonds', 'SUPPORTING_CONCEPT_GAP', 'PROCESS', 'SUPPORT', r'types? of', 'Know the kinds of lab-grown stones', 'SUPPORTING_SECTION')
C(T, 'How lab-grown diamonds are made (process overview; EDU-LG-04 conditional, interim home here)', 'PROCESS_GAP', 'PROCESS', 'CORE',
  r'how (are|is|do).*(made|grown|created|make)|process|grow', 'Understand how a diamond can be grown', 'SUPPORTING_SECTION', owner='EDU-LG-04', anchor='lab grown diamond process', xkey='LG_PROCESS')
C(T, 'CVD vs HPHT detailed method comparison', 'COMPARISON_GAP', 'PROCESS', 'SUPPORT', r'\bcvd\b|\bhpht\b|chemical vapou?r|high pressure',
  'Know the two growth methods exist', 'BRIEF_MENTION_AND_LINK', owner='EDU-LG-03', anchor='hpht vs cvd', xkey='CVD_VS_HPHT')
C(T, 'History of lab-grown diamonds (first synthesis, General Electric)', 'SUPPORTING_CONCEPT_GAP', 'HISTORY', 'SUPPORT',
  r'history|first|invent|general electric|\bge\b', 'Context and credibility for the technology', 'SUPPORTING_SECTION')
C(T, 'Lab-grown diamonds are real diamonds (authenticity)', 'CORE_CONCEPT_GAP', 'AUTHENTICITY', 'SUPPORT', r'\breal\b|fake|genuine',
  'Reassurance that the product is a diamond', 'BRIEF_MENTION_AND_LINK', owner='EDU-LG-01', anchor='are lab grown diamonds real', xkey='LG_AUTHENTICITY')
C(T, 'Lab-grown vs natural comparison', 'COMPARISON_GAP', 'ORIGIN', 'SUPPORT', r'natural|mined|\bvs\b|real diamonds?',
  'Orientation against the natural alternative', 'BRIEF_MENTION_AND_LINK', owner='EDU-LG-02', anchor='lab grown vs natural diamonds', xkey='LG_VS_NATURAL')
C(T, 'Price, value and resale', 'COMMERCIAL_CONTEXT_GAP', 'PRICE', 'SUPPORT', r'price|cost|cheap|value|worth|expensive',
  'Orientation on cost questions', 'BRIEF_MENTION_AND_LINK', owner='EDU-LG-05', anchor='do lab grown diamonds hold their value', xkey='LG_PRICE_VALUE')
C(T, 'Hub routing to lab-grown child topics (Stage 16 child links)', 'INTERNAL_CONTEXT_GAP', 'NAVIGATION', 'SUPPORT', None,
  'Move from overview to the specific question', 'SUPPORTING_SECTION', stage='DISCOVER', extra=('Stage 16 child/related links from EDU-LG-00', None))
C(T, 'Hand-off to lab-grown products (commercial hub COM-LG-HUB is conditional)', 'COMMERCIAL_CONTEXT_GAP', 'COMMERCIAL', 'BIZ', None,
  'Move from learning to shopping', 'BUSINESS_INPUT_REQUIRED', owner='COM-LG-HUB', anchor='lab grown diamonds', biz='Which lab-grown products HOD sells and whether COM-LG-HUB is built (Stage 12/15 conditional)', stage='BUY',
  extra=('Stage 15: lab grown diamonds = CONDITIONAL_NOT_MAPPED (commercial hub held)', 1))

# --- EDU-LG-01 authenticity
T = 'EDU-LG-01'
C(T, 'Lab-grown diamonds are real diamonds: same carbon crystal, same chemical/physical/optical properties', 'CORE_CONCEPT_GAP', 'AUTHENTICITY', 'CORE',
  r'\breal\b|actually|really a diamond|identical|same (as|chemical)|pure carbon|chemically', 'Get a clear yes/no on whether the stone is a real diamond', 'CORE_SECTION', xkey='LG_AUTHENTICITY', stage='UNDERSTAND')
C(T, 'Direct answer in the opening lines (AI Overview + PAA on the primary SERP)', 'AEO_GAP', 'AUTHENTICITY', 'CORE', r'\breal\b',
  'Get the answer without reading the whole page', 'INLINE_ANSWER', note='SERP evidence suggests a concise answer-first block; no format guarantees AI Overview inclusion.')
C(T, '"Fake" vs simulant: lab-grown is not a simulant (CZ, moissanite)', 'DEFINITION_GAP', 'AUTHENTICITY', 'CORE',
  r'fake|simulant|cubic zirconia|\bcz\b|moissanite', 'Separate lab-grown diamonds from look-alikes', 'SUPPORTING_SECTION')
C(T, 'Equivalent terms (lab-created, lab-made, lab diamond, synthetic)', 'DEFINITION_GAP', 'TERMINOLOGY', 'SUPPORT',
  r'lab[- ]created|lab[- ]made|lab diamond|synthetic|man[- ]made', 'Recognise the product under any name', 'INLINE_ANSWER', owner='EDU-LG-00', anchor='synthetic diamonds', xkey='LG_TERMINOLOGY')
C(T, 'Natural-vs-lab framing (the primary SERP is COMPARISON-led)', 'SERP_FORMAT_GAP', 'ORIGIN', 'CORE',
  r'natural|mined|\bvs\b|versus|compar|real diamonds? (cost|vs)', 'Understand "real" relative to mined diamonds', 'BRIEF_MENTION_AND_LINK', owner='EDU-LG-02', anchor='lab grown vs natural diamonds', xkey='LG_VS_NATURAL',
  note='Answer "same material, different origin" only; the full attribute comparison stays on EDU-LG-02 (Stage 14 MEDIUM risk).')
C(T, 'Will it pass a diamond tester', 'QUESTION_GAP', 'AUTHENTICITY', 'SUPPORT', r'test', 'Verify the claim practically', 'BRIEF_MENTION_AND_LINK',
  owner='EDU-LG-09', anchor='do lab grown diamonds pass a diamond tester', xkey='LG_DETECTION', stage='VERIFY')
C(T, 'Can a jeweller or lab tell it is lab-grown', 'QUESTION_GAP', 'AUTHENTICITY', 'SUPPORT', r'\btell\b|identify|detect', 'Know whether others can tell', 'BRIEF_MENTION_AND_LINK',
  owner='EDU-LG-09', anchor='do lab grown diamonds pass a diamond tester', xkey='LG_DETECTION', stage='VERIFY')
C(T, 'Downsides / is it worth buying', 'COMMERCIAL_CONTEXT_GAP', 'VALUE', 'SUPPORT', r'downside|disadvantage|worth', 'Weigh the purchase', 'BRIEF_MENTION_AND_LINK',
  owner='EDU-LG-06', anchor='are lab grown diamonds worth it', xkey='LG_WORTH_IT', stage='EVALUATE', note='EDU-LG-06 is conditional; its interim home is EDU-LG-02.')
C(T, 'Price relative to natural', 'COMMERCIAL_CONTEXT_GAP', 'PRICE', 'SUPPORT', r'price|cost|cheap|expensive', 'Understand why "real" can cost less', 'BRIEF_MENTION_AND_LINK',
  owner='EDU-LG-05', anchor='do lab grown diamonds hold their value', xkey='LG_PRICE_VALUE', stage='EVALUATE')
C(T, 'Certificate as proof of identity and origin', 'TRUST_EVIDENCE_GAP', 'CERTIFICATION', 'SUPPORT', r'certif|\bgia\b|\bigi\b|report',
  'Verify what the stone is', 'BRIEF_MENTION_AND_LINK', owner='EDU-CERT-00', anchor='lab-grown diamond certification', xkey='CERT_BASICS', stage='VERIFY')
C(T, 'Experience/forum reassurance (Reddit related search; Forums feature)', 'USER_JOURNEY_GAP', 'PERCEPTION', 'OPTIONAL', r'reddit|forum|quora',
  'Hear how other buyers feel', 'INLINE_ANSWER', stage='EVALUATE')

# --- EDU-LG-02 lab vs natural
T = 'EDU-LG-02'
C(T, 'Key similarities: same carbon, same hardness, same 4Cs grading', 'CORE_CONCEPT_GAP', 'QUALITY', 'CORE',
  r'similar|identical|same|chemically|physically|optically', 'See what does not change between the two', 'CORE_SECTION', xkey='LG_VS_NATURAL', stage='COMPARE')
C(T, 'Key difference: origin (formed in the earth over time vs grown in weeks)', 'CORE_CONCEPT_GAP', 'ORIGIN', 'CORE',
  r'origin|formed|billion|weeks|mined|earth', 'See the fundamental difference', 'CORE_SECTION', stage='COMPARE')
C(T, 'Price difference between origins (no dated price levels, Stage 13)', 'ATTRIBUTE_GAP', 'PRICE', 'CORE',
  r'price|cost|cheaper|afford', 'Understand the cost gap', 'SUPPORTING_SECTION', stage='COMPARE', note='Comparison-level only; depth on EDU-LG-05.')
C(T, 'Resale value / value retention difference', 'ATTRIBUTE_GAP', 'RESALE', 'CORE', r'resale|value|invest',
  'Understand long-term value', 'SUPPORTING_SECTION', stage='EVALUATE', note='Comparison-level only; depth on EDU-LG-05.')
C(T, 'Rarity and tradition / emotional value of natural', 'ATTRIBUTE_GAP', 'VALUE', 'SUPPORT', r'rarity|\brare\b|tradition|sentimental|emotional',
  'Weigh non-financial reasons', 'SUPPORTING_SECTION', stage='EVALUATE')
C(T, 'Ethics and environment as a comparison row', 'ATTRIBUTE_GAP', 'ETHICS', 'SUPPORT', r'ethic|environment|sustainab|\beco\b|conflict',
  'Weigh ethical factors', 'BRIEF_MENTION_AND_LINK', owner='EDU-LG-07', anchor='are lab grown diamonds ethical', xkey='LG_ETHICS', stage='EVALUATE')
C(T, 'Size for budget (larger stone for the same spend)', 'ATTRIBUTE_GAP', 'SIZE', 'SUPPORT', r'\bsize\b|bigger|larger|maximi[sz]ing stone',
  'Translate price difference into what you get', 'SUPPORTING_SECTION', stage='EVALUATE')
C(T, 'Attribute-by-attribute comparison table', 'SERP_FORMAT_GAP', 'COMPARISON', 'CORE', r'side by side|\bvs\b|differences?|similarities',
  'Scan the comparison quickly', 'COMPARISON_TABLE', stage='COMPARE', note='SERP evidence suggests a similarities/differences structure (AI Overview headings).')
C(T, 'Which is better — decision framing by buyer priority', 'USER_JOURNEY_GAP', 'DECISION', 'CORE', r'better|should i|which',
  'Reach a decision', 'CORE_SECTION', stage='DECIDE')
C(T, 'Pros and cons / downsides of lab-grown (EDU-LG-06 conditional, interim home here)', 'SUPPORTING_CONCEPT_GAP', 'VALUE', 'SUPPORT',
  r'downside|disadvantage|\bcons\b|\bpros\b|avoid|worth', 'Hear the honest drawbacks', 'SUPPORTING_SECTION', owner='EDU-LG-06', anchor='are lab grown diamonds worth it', xkey='LG_WORTH_IT', stage='EVALUATE')
C(T, 'Perception and social acceptance (jewellers, "do rich people buy")', 'QUESTION_GAP', 'PERCEPTION', 'SUPPORT',
  r'rich people|jewel+ers hate|tacky|popular|perception|avoid lab', 'Handle social worry', 'FAQ', stage='EVALUATE')
C(T, 'Can you tell them apart / identification', 'QUESTION_GAP', 'AUTHENTICITY', 'SUPPORT', r'\btell\b|identify|detect|detection',
  'Know if anyone can tell', 'BRIEF_MENTION_AND_LINK', owner='EDU-LG-09', anchor='do lab grown diamonds pass a diamond tester', xkey='LG_DETECTION', stage='VERIFY')
C(T, 'Appearance and sparkle parity', 'ATTRIBUTE_GAP', 'QUALITY', 'SUPPORT', r'sparkle|\blooks?\b|appearance|as good as',
  'Know if it looks the same', 'INLINE_ANSWER', owner='EDU-LG-08', anchor='do lab grown diamonds get cloudy', xkey='LG_APPEARANCE', stage='COMPARE')
C(T, 'Durability parity (Mohs 10)', 'ATTRIBUTE_GAP', 'DURABILITY', 'SUPPORT', r'mohs|hardness|durab',
  'Know it will last as well', 'INLINE_ANSWER', owner='EDU-GEN-01', anchor='diamond hardness', xkey='DIAMOND_HARDNESS', stage='COMPARE')
C(T, 'Both graded by the same labs (GIA, IGI)', 'ENTITY_GAP', 'CERTIFICATION', 'SUPPORT', r'\bgia\b|\bigi\b|grading',
  'Know both come with reports', 'BRIEF_MENTION_AND_LINK', owner='EDU-CERT-00', anchor='lab-grown diamond certification', xkey='CERT_BASICS', stage='VERIFY')
C(T, 'Third options: moissanite and cubic zirconia', 'COMPARISON_GAP', 'COMPARISON', 'OPTIONAL', r'moissanite|cubic zirconia|\bcz\b',
  'Place the two against simulants', 'BRIEF_MENTION_AND_LINK', owner='EDU-GEM-01', anchor='what is the difference between moissanite and lab grown diamonds', xkey='MOISSANITE_VS_LAB', stage='COMPARE')
C(T, 'Clarity/quality differences by origin', 'ATTRIBUTE_GAP', 'CLARITY', 'OPTIONAL', r'clarity|quality', 'Check quality myths', 'INLINE_ANSWER', stage='COMPARE')
C(T, 'Buyer discussion demand (Reddit variants, forums)', 'USER_JOURNEY_GAP', 'PERCEPTION', 'OPTIONAL', r'reddit', 'Peer reassurance', 'INLINE_ANSWER', stage='EVALUATE')
C(T, 'Which origins HOD offers and where to shop each', 'COMMERCIAL_CONTEXT_GAP', 'COMMERCIAL', 'BIZ', None, 'Move to shopping after deciding',
  'BUSINESS_INPUT_REQUIRED', owner='COM-LG-HUB', anchor='lab grown diamonds', biz='Natural offer unconfirmed (natural commercial hub deferred, Stage 12); COM-LG-HUB conditional', stage='BUY',
  extra=('Stage 12: Natural Diamonds commercial hub INSUFFICIENT EVIDENCE — DEFER; Lab-Grown hub PROPOSED_CONDITIONAL', 1))

# --- EDU-LG-03 CVD vs HPHT
T = 'EDU-LG-03'
C(T, 'HPHT growth process (seed, carbon, heat and pressure)', 'PROCESS_GAP', 'PROCESS', 'CORE', r'\bhpht\b|high pressure|high temperature',
  'Understand HPHT', 'CORE_SECTION', xkey='CVD_VS_HPHT')
C(T, 'CVD growth process (plasma, carbon-rich gas, layer deposition)', 'PROCESS_GAP', 'PROCESS', 'CORE', r'\bcvd\b|chemical vapou?r|deposition|plasma',
  'Understand CVD', 'CORE_SECTION')
C(T, 'Single-method CVD depth ("what is a CVD diamond"; cvd diamond has no HOD ranking)', 'CORE_CONCEPT_GAP', 'PROCESS', 'CORE',
  r'what is (a )?cvd|cvd diamonds?\b(?! vs)', 'Understand CVD on its own, not only as a comparison', 'CORE_SECTION')
C(T, 'Growth shape and characteristic differences (crystal habit, inclusions, strain)', 'ATTRIBUTE_GAP', 'PROCESS', 'CORE',
  r'growth shape|characteristic|cuboctahedr|cubic|inclusion|metallic|strain|graining|distinguishing', 'Know how the stones differ physically', 'SUPPORTING_SECTION', stage='COMPARE')
C(T, 'No visual difference after cutting; both graded on the 4Cs', 'CORE_CONCEPT_GAP', 'QUALITY', 'CORE',
  r'no visual difference|visual appearance|identical|4 ?cs|\bsame\b', 'Know whether the method matters to the eye', 'INLINE_ANSWER', stage='EVALUATE')
C(T, 'Which method is better (answer + conditions)', 'AEO_GAP', 'DECISION', 'CORE', r'better|\bbest\b|which',
  'Get a direct answer to "which is better"', 'CORE_SECTION', stage='DECIDE', note='PAA repeats this across the validated SERPs; SERP evidence suggests an answer-first paragraph.')
C(T, 'Key differences at a glance (comparison table)', 'SERP_FORMAT_GAP', 'COMPARISON', 'CORE', r'key differences|at a glance|pros and cons|\bvs\b',
  'Scan the differences', 'COMPARISON_TABLE', stage='COMPARE')
C(T, 'Price difference between CVD and HPHT (no live figures)', 'ATTRIBUTE_GAP', 'PRICE', 'CORE', r'price|cost|afford|cheap',
  'Understand cost implications of method', 'SUPPORTING_SECTION', stage='EVALUATE', note='Method-level only; value/resale depth on EDU-LG-05.')
C(T, 'Pros and cons / disadvantages by method', 'SUPPORTING_CONCEPT_GAP', 'VALUE', 'SUPPORT', r'\bpros\b|\bcons\b|disadvantage|downside',
  'Weigh each method', 'SUPPORTING_SECTION', stage='EVALUATE')
C(T, 'Are CVD / HPHT diamonds worth buying / worth anything', 'QUESTION_GAP', 'VALUE', 'SUPPORT', r'worth', 'Decide if a method is a good buy', 'FAQ', stage='EVALUATE')
C(T, 'HPHT treatment (post-growth colour treatment) vs HPHT growth', 'DEFINITION_GAP', 'PROCESS', 'SUPPORT', r'treat|post[- ]growth|anneal',
  'Avoid confusing treated stones with HPHT-grown stones', 'SUPPORTING_SECTION')
C(T, 'Type IIa classification', 'ENTITY_GAP', 'MATERIAL', 'SUPPORT', r'\biia\b|type ii', 'Decode "Type IIa" seen in listings', 'INLINE_ANSWER', owner='EDU-GEN-01', anchor='diamond hardness', xkey='TYPE_IIA',
  note='Stage 15 owner of the Type IIa keyword is EDU-GEN-01; here only the CVD/HPHT relevance.')
C(T, 'Colour tendencies by method (e.g. fancy colours)', 'ATTRIBUTE_GAP', 'COLOUR', 'SUPPORT', r'colou?r|fancy', 'Know colour implications', 'INLINE_ANSWER')
C(T, 'CVD full form / acronym', 'DEFINITION_GAP', 'TERMINOLOGY', 'SUPPORT', r'full form|stands for|chemical vapou?r deposition', 'Decode the acronym', 'DEFINITION_BLOCK')
C(T, 'Are CVD / HPHT diamonds real (method-specific yes; general authenticity on EDU-LG-01)', 'QUESTION_GAP', 'AUTHENTICITY', 'SUPPORT', r'\breal\b|fake',
  'Confirm method does not affect authenticity', 'INLINE_ANSWER', owner='EDU-LG-01', anchor='are lab grown diamonds real', xkey='LG_AUTHENTICITY')
C(T, 'Diamond tester behaviour of CVD/HPHT stones', 'QUESTION_GAP', 'AUTHENTICITY', 'SUPPORT', r'tester|\btest', 'Know tester outcome', 'INLINE_ANSWER',
  owner='EDU-LG-09', anchor='do lab grown diamonds pass a diamond tester', xkey='LG_DETECTION', stage='VERIFY')
C(T, 'Growth-method disclosure on grading reports (how to know which method)', 'TRUST_EVIDENCE_GAP', 'CERTIFICATION', 'SUPPORT', r'\bgia\b|report|disclos|identify|\btell\b',
  'Verify the method of a specific stone', 'BRIEF_MENTION_AND_LINK', owner='EDU-CERT-00', anchor='lab-grown diamond certification', xkey='CERT_BASICS', stage='VERIFY')
C(T, 'Comparison with natural diamonds / moissanite', 'COMPARISON_GAP', 'COMPARISON', 'OPTIONAL', r'natural|moissanite', 'Place methods against other options', 'BRIEF_MENTION_AND_LINK',
  owner='EDU-LG-02', anchor='lab grown vs natural diamonds', xkey='LG_VS_NATURAL', stage='COMPARE')
C(T, 'Equipment visuals (HPHT press, CVD reactor)', 'EXAMPLE_GAP', 'PROCESS', 'OPTIONAL', r'machine|\bpress\b|reactor', 'See the process', 'SUPPORTING_SECTION')
C(T, 'Which growth method HOD\'s stones use and how it is disclosed', 'TRUST_EVIDENCE_GAP', 'COMMERCIAL', 'BIZ', r'for sale|for jewelry',
  'Connect method knowledge to HOD products', 'BUSINESS_INPUT_REQUIRED', biz='HOD growth-method sourcing and disclosure practice (Surat manufacturing; not documented in project files)', stage='BUY')

# --- EDU-LG-05 price / value / resale
T = 'EDU-LG-05'
C(T, 'Why lab-grown costs less than natural (production and supply)', 'CORE_CONCEPT_GAP', 'PRICE', 'CORE', r'cheap|cost|price|expensive|afford',
  'Understand the price level', 'CORE_SECTION', xkey='LG_PRICE_VALUE', stage='EVALUATE')
C(T, 'Resale value / do lab-grown diamonds hold value', 'CORE_CONCEPT_GAP', 'RESALE', 'CORE', r'resale|hold (their )?value|worth anything|value',
  'Understand long-term value before buying', 'CORE_SECTION', stage='EVALUATE')
C(T, 'Investment suitability', 'QUESTION_GAP', 'VALUE', 'CORE', r'invest', 'Know if it is an investment', 'SUPPORTING_SECTION', stage='EVALUATE')
C(T, 'Price trend over time (prices falling)', 'SUPPORTING_CONCEPT_GAP', 'PRICE', 'SUPPORT', r'cheaper|drop|fall|trend|going down|getting', 'Understand timing', 'SUPPORTING_SECTION')
C(T, 'Price per carat as a concept (no live figures)', 'ATTRIBUTE_GAP', 'PRICE', 'SUPPORT', r'per carat|\d carat|carat', 'Compare offers fairly', 'SUPPORTING_SECTION', stage='EVALUATE')
C(T, 'Selling, pawning and trade-in of lab-grown diamonds', 'SUPPORTING_CONCEPT_GAP', 'RESALE', 'SUPPORT', r'\bsell|pawn|trade', 'Know exit options', 'SUPPORTING_SECTION')
C(T, 'HOD buy-back / trade-in / upgrade policy', 'COMMERCIAL_CONTEXT_GAP', 'COMMERCIAL', 'BIZ', r'trade|buy ?back|upgrade|pawn',
  'Know what HOD offers after purchase', 'BUSINESS_INPUT_REQUIRED', owner='SUP-FAQ', biz='HOD buy-back/trade-in/upgrade policy unknown (Stage 15/17 business dependency)', stage='BUY')
C(T, 'Certificate\'s role in resale', 'TRUST_EVIDENCE_GAP', 'CERTIFICATION', 'SUPPORT', r'certif', 'Protect resale', 'BRIEF_MENTION_AND_LINK', owner='EDU-CERT-00', anchor='lab-grown diamond certification', xkey='CERT_BASICS')
C(T, 'Natural diamond value retention (comparison)', 'COMPARISON_GAP', 'RESALE', 'SUPPORT', r'natural|mined', 'Compare value retention', 'SUPPORTING_SECTION', stage='COMPARE')
C(T, 'Cost to grow a diamond', 'SUPPORTING_CONCEPT_GAP', 'PRICE', 'OPTIONAL', r'cost to (grow|make)|cost .* grow', 'Curiosity about production cost', 'FAQ')
C(T, 'Undated price guidance and sourcing of any price context (Stage 13 rule)', 'TRUST_EVIDENCE_GAP', 'TRUST', 'SUPPORT', None,
  'Trust that price information is not stale', 'SUPPORTING_SECTION', extra=('Stage 13/15 business dependency: avoid hard-coded prices on Education pages', 1))

# --- EDU-LG-07 ethics
T = 'EDU-LG-07'
C(T, 'Ethical sourcing compared with mined supply chains', 'CORE_CONCEPT_GAP', 'ETHICS', 'CORE', r'ethic|conflict|sourc|moral', 'Know whether it is ethical', 'CORE_SECTION', xkey='LG_ETHICS', stage='EVALUATE')
C(T, 'Environmental impact (energy use, footprint)', 'CORE_CONCEPT_GAP', 'ETHICS', 'CORE', r'environment|energy|footprint|carbon|\beco\b|sustainab|green',
  'Know the environmental trade-off', 'CORE_SECTION', stage='EVALUATE')
C(T, 'Carbon-neutral / renewable-energy claims and their substantiation', 'TRUST_EVIDENCE_GAP', 'ETHICS', 'BIZ', r'carbon neutral|renewable|certified',
  'Trust any sustainability claim', 'BUSINESS_INPUT_REQUIRED', biz='Any HOD environmental claim must be substantiated (Stage 15 business dependency)', stage='VERIFY')
C(T, 'Natural conflict-free sourcing (EDU-NAT-02 conditional)', 'COMPARISON_GAP', 'ETHICS', 'OPTIONAL', r'conflict|blood', 'Contrast with natural sourcing',
  'BRIEF_MENTION_AND_LINK', owner='EDU-NAT-02', anchor='conflict free diamonds', xkey='NAT_CONFLICT_FREE')
C(T, 'Mining and labour impacts (comparison context)', 'SUPPORTING_CONCEPT_GAP', 'ETHICS', 'SUPPORT', r'mining|labou?r|worker', 'Understand the mined side', 'SUPPORTING_SECTION')

# --- EDU-LG-08 appearance & durability
T = 'EDU-LG-08'
C(T, 'Do lab-grown diamonds get cloudy, fade or change over time', 'CORE_CONCEPT_GAP', 'DURABILITY', 'CORE', r'cloudy|fade|fading|discolou?r|lifespan|\blast\b|change colou?r',
  'Know the stone will not deteriorate', 'CORE_SECTION', xkey='LG_APPEARANCE', stage='EVALUATE')
C(T, 'Fluorescence / UV glow', 'ATTRIBUTE_GAP', 'QUALITY', 'CORE', r'fluoresc|glow|\buv\b|black light', 'Understand glow under UV', 'CORE_SECTION')
C(T, 'Sparkle and looks compared with natural', 'ATTRIBUTE_GAP', 'QUALITY', 'CORE', r'sparkle|\blooks?\b|appearance|shine|brillian', 'Know it looks the same', 'SUPPORTING_SECTION', stage='COMPARE')
C(T, 'Post-growth treatments (irradiation, clarity enhancement) and disclosure', 'SUPPORTING_CONCEPT_GAP', 'PROCESS', 'SUPPORT', r'treat|irradiat|enhanc',
  'Understand treatments', 'SUPPORTING_SECTION')
C(T, 'HOD disclosure practice for treated stones', 'TRUST_EVIDENCE_GAP', 'COMMERCIAL', 'BIZ', r'treat|irradiat|enhanc', 'Trust HOD stones', 'BUSINESS_INPUT_REQUIRED',
  biz='HOD treated-stone disclosure practice unknown (Stage 17 business dependency)', stage='VERIFY')
C(T, 'Hardness / durability parity', 'ATTRIBUTE_GAP', 'DURABILITY', 'SUPPORT', r'hard|durab|scratch|chip|strong', 'Know it will last', 'BRIEF_MENTION_AND_LINK',
  owner='EDU-GEN-01', anchor='diamond hardness', xkey='DIAMOND_HARDNESS')
C(T, 'Care and cleaning to keep sparkle (EDU-RJG-03 conditional)', 'SUPPORTING_CONCEPT_GAP', 'CARE', 'OPTIONAL', r'clean|\bcare\b', 'Maintain appearance',
  'BRIEF_MENTION_AND_LINK', owner='EDU-RJG-03', anchor='does stainless steel jewelry tarnish', xkey='JEWELLERY_CARE')

# --- EDU-LG-09 detection
T = 'EDU-LG-09'
C(T, 'Will a lab-grown diamond pass a diamond tester (thermal/electrical)', 'CORE_CONCEPT_GAP', 'AUTHENTICITY', 'CORE', r'tester|\bpass\b|\btest',
  'Know the tester outcome', 'CORE_SECTION', xkey='LG_DETECTION', stage='VERIFY')
C(T, 'How thermal and electrical testers work', 'PROCESS_GAP', 'PROCESS', 'CORE', r'thermal|conductiv|electric|heat', 'Understand why testers cannot separate lab from natural', 'SUPPORTING_SECTION', stage='VERIFY')
C(T, 'How jewellers and labs identify lab-grown (spectroscopy, UV screening)', 'CORE_CONCEPT_GAP', 'AUTHENTICITY', 'CORE',
  r'jewel+er|spectro|\buv\b|screen|identify|\btell\b', 'Know who can tell and how', 'CORE_SECTION', stage='VERIFY')
C(T, 'Reliability and limits of testers (moissanite false positives)', 'SUPPORTING_CONCEPT_GAP', 'AUTHENTICITY', 'SUPPORT', r'reliab|accura|\bwork\b|moissanite|limitation|false',
  'Know what testers miss', 'SUPPORTING_SECTION')
C(T, 'Laser inscription and report number lookup', 'TRUST_EVIDENCE_GAP', 'CERTIFICATION', 'SUPPORT', r'inscri|serial|laser|report number',
  'Verify via the inscription', 'INLINE_ANSWER', owner='EDU-CERT-00', anchor='lab-grown diamond certification', xkey='CERT_VERIFY')
C(T, 'Microscope / loupe inspection', 'SUPPORTING_CONCEPT_GAP', 'AUTHENTICITY', 'SUPPORT', r'microscop|loupe|magnif', 'Know visual checks', 'INLINE_ANSWER')
C(T, 'Home tests (fog, heat, light) and why they are unreliable', 'QUESTION_GAP', 'AUTHENTICITY', 'SUPPORT', r'\bhome\b|\bfog|water|heat test|x ?ray|light test|beeps',
  'Handle DIY test questions', 'FAQ')
C(T, 'Where to get a diamond tested', 'USER_JOURNEY_GAP', 'AUTHENTICITY', 'SUPPORT', r'where (to|can|do)|tested\b|professional jewel+er|appraiser', 'Find a professional check', 'INLINE_ANSWER', stage='VERIFY')
C(T, 'Tester-device shopping (Amazon, prices, best tester)', 'SERP_FORMAT_GAP', 'COMMERCIAL', 'AVOID', r'amazon|for sale|tester (price|cost)|best .*tester|smartpro',
  'Device purchase — not HOD business (Stage 12 D-16)', 'AVOID', note='Recorded so Stage 19 does not chase the device-shopping part of the SERP.')

# --- EDU-LG-10 how to choose
T = 'EDU-LG-10'
C(T, '4Cs priorities when choosing a lab-grown diamond', 'CORE_CONCEPT_GAP', 'QUALITY', 'CORE', r'4 ?cs|\bcut\b|colou?r|clarity|carat',
  'Know which grades to target', 'CORE_SECTION', stage='DECIDE', note='Priorities only; grade definitions stay on the 4Cs pages.')
C(T, 'Get a certificate (IGI/GIA)', 'TRUST_EVIDENCE_GAP', 'CERTIFICATION', 'CORE', r'certif|\bigi\b|\bgia\b', 'Buy a verified stone', 'SUPPORTING_SECTION',
  owner='EDU-CERT-00', anchor='lab-grown diamond certification', xkey='CERT_BASICS', stage='VERIFY')
C(T, 'Check price per carat / set a budget', 'ATTRIBUTE_GAP', 'PRICE', 'SUPPORT', r'price per carat|budget|\bprice', 'Judge value', 'SUPPORTING_SECTION', stage='DECIDE')
C(T, 'Understand resale value before buying', 'COMMERCIAL_CONTEXT_GAP', 'RESALE', 'SUPPORT', r'resale', 'Set expectations', 'BRIEF_MENTION_AND_LINK',
  owner='EDU-LG-05', anchor='do lab grown diamonds hold their value', xkey='LG_PRICE_VALUE')
C(T, 'Shape choice', 'SUPPORTING_CONCEPT_GAP', 'SHAPE', 'SUPPORT', r'shape', 'Choose a shape', 'BRIEF_MENTION_AND_LINK', owner='EDU-SHP-00', anchor='diamond shape', xkey='SHAPES_OVERVIEW', stage='DECIDE')
C(T, 'Does growth method matter (CVD vs HPHT)', 'COMPARISON_GAP', 'PROCESS', 'SUPPORT', r'\bcvd\b|\bhpht\b', 'Know if method affects the choice', 'BRIEF_MENTION_AND_LINK',
  owner='EDU-LG-03', anchor='hpht vs cvd', xkey='CVD_VS_HPHT')
C(T, 'Step-by-step choosing sequence (beginner framing)', 'SERP_FORMAT_GAP', 'DECISION', 'SUPPORT', r'beginner|how to (choose|buy)|tips|step',
  'Follow a clear sequence', 'STEP_SEQUENCE', stage='DECIDE')
C(T, 'Is it worth it (lab-grown overall)', 'COMMERCIAL_CONTEXT_GAP', 'VALUE', 'OPTIONAL', r'worth', 'Confirm the category choice', 'BRIEF_MENTION_AND_LINK',
  owner='EDU-LG-06', anchor='are lab grown diamonds worth it', xkey='LG_WORTH_IT')
C(T, 'IF / flawless lab-grown — worth paying for?', 'ATTRIBUTE_GAP', 'CLARITY', 'OPTIONAL', r'\bif\b|flawless', 'Avoid overpaying for clarity', 'BRIEF_MENTION_AND_LINK',
  owner='EDU-4C-03', anchor='v v s diamond', xkey='VVS_IF_FL')
C(T, 'Engagement-ring purchase decision (boundary with deferred EDU-RJG-04; D-19 unapproved)', 'USER_JOURNEY_GAP', 'OCCASION', 'HEAD', r'engagement|\bring\b',
  'Choose a stone for an engagement ring', 'VALIDATE_BEFORE_USE', owner='EDU-RJG-04', anchor='can you return an engagement ring', stage='BUY',
  note='Evidence-dependent: D-19 commercial supplement not approved.')
C(T, 'Hand-off to HOD lab-grown products', 'COMMERCIAL_CONTEXT_GAP', 'COMMERCIAL', 'BIZ', r'lab grown diamond rings|lab grown diamonds$',
  'Buy after choosing', 'BUSINESS_INPUT_REQUIRED', owner='COM-LG-HUB', anchor='lab grown diamonds', biz='COM-LG-HUB conditional; HOD product range for lab-grown stones', stage='BUY')

# --- EDU-NAT-00 natural formation
T = 'EDU-NAT-00'
C(T, 'Natural formation: carbon under heat and pressure in the mantle over billions of years', 'PROCESS_GAP', 'PROCESS', 'CORE',
  r'form|formed|made|mantle|pressure|heat|billion|earth', 'Understand how natural diamonds form', 'CORE_SECTION')
C(T, 'Kimberlite pipes / volcanic transport to the surface', 'ENTITY_GAP', 'PROCESS', 'CORE', r'kimberlite|volcan|pipe', 'Know how diamonds reach the surface', 'SUPPORTING_SECTION')
C(T, 'Mining and extraction', 'PROCESS_GAP', 'PROCESS', 'SUPPORT', r'\bmin(e|ed|es|ing)\b|extract', 'Know how they are recovered', 'SUPPORTING_SECTION')
C(T, 'From rough to polished (cutting process)', 'PROCESS_GAP', 'PROCESS', 'SUPPORT', r'rough|\braw\b|uncut|unpolished|polish', 'Follow the journey to a gem', 'SUPPORTING_SECTION')
C(T, 'Where natural diamonds come from (sources)', 'SUPPORTING_CONCEPT_GAP', 'ORIGIN', 'SUPPORT', r'where|countr|source|africa|botswana|russia|canada', 'Know origin', 'SUPPORTING_SECTION')
C(T, '"How are diamonds made" ambiguity: natural formation vs lab growth', 'COMPARISON_GAP', 'ORIGIN', 'SUPPORT', r'\blab\b|synthetic|how are diamonds made',
  'Resolve which process the searcher means', 'INLINE_ANSWER', owner='EDU-LG-00', anchor='lab grown diamond process', xkey='LG_PROCESS',
  note='Stage 15 routes lab process keywords to EDU-LG-00 as interim home of EDU-LG-04.')
C(T, 'Untreated natural diamonds', 'ATTRIBUTE_GAP', 'ORIGIN', 'OPTIONAL', r'untreated', 'Know what "untreated" means', 'INLINE_ANSWER')
C(T, 'Controlled metamorphosis (term)', 'DEFINITION_GAP', 'TERMINOLOGY', 'OPTIONAL', r'metamorph', 'Decode the term', 'INLINE_ANSWER')
C(T, 'Natural value/rarity (EDU-NAT-01 conditional) and conflict-free sourcing (EDU-NAT-02 conditional)', 'COMMERCIAL_CONTEXT_GAP', 'VALUE', 'OPTIONAL',
  r'value|rare|rarity|conflict|supply|industry', 'Orientation on value and ethics', 'BRIEF_MENTION_AND_LINK', owner='EDU-NAT-01', anchor='diamond supply', xkey='NAT_VALUE')
C(T, 'Natural diamond offer at HOD (commercial natural hub deferred)', 'COMMERCIAL_CONTEXT_GAP', 'COMMERCIAL', 'BIZ', None, 'Move to natural products',
  'BUSINESS_INPUT_REQUIRED', biz='Whether HOD sells natural diamonds (Stage 12 natural commercial hub deferred)', stage='BUY',
  extra=('Stage 12: Natural Diamonds (commercial hub) INSUFFICIENT EVIDENCE — DEFER', 1))

# --- EDU-4C-00 4Cs hub
T = 'EDU-4C-00'
C(T, 'The 4Cs framework defined (cut, colour, clarity, carat)', 'CORE_CONCEPT_GAP', 'QUALITY', 'CORE', r'4 ?cs?\b|four cs|\bcut\b|colou?r|clarity|carat',
  'Understand how diamond quality is described', 'CORE_SECTION', xkey='FOUR_CS')
C(T, 'Grading scales and one summary chart', 'SERP_FORMAT_GAP', 'QUALITY', 'CORE', r'chart|scale|grading|classification', 'See all scales at a glance', 'VISUAL_CHART')
C(T, 'Lab-grown diamonds are graded on the same scales', 'CORE_CONCEPT_GAP', 'QUALITY', 'CORE', r'\blab\b', 'Know grading applies equally', 'SUPPORTING_SECTION')
C(T, 'Relative importance of the Cs and trade-offs', 'USER_JOURNEY_GAP', 'DECISION', 'SUPPORT', r'most important|matter|trade|priorit|which|best', 'Prioritise spend', 'SUPPORTING_SECTION', stage='DECIDE')
C(T, 'Colour–clarity combinations (e.g. F VS2, G/VS, GH SI)', 'ATTRIBUTE_GAP', 'QUALITY', 'SUPPORT', r'\b[d-k]\s?-?\s?[d-k]?\s?/?\s?(vs|si|vvs)\s?[12]?\b',
  'Judge a specific combination', 'FAQ', xkey='COLOUR_CLARITY_COMBOS', note='Several "x vs diamond" keywords are ambiguous (colour + VS clarity, not "versus"); Stage 17 POSSIBLE_OVERLAP.')
C(T, 'Clarity scale detail', 'ATTRIBUTE_GAP', 'CLARITY', 'SUPPORT', r'clarity', 'Go deeper on clarity', 'BRIEF_MENTION_AND_LINK', owner='EDU-4C-01', anchor='diamond clarity grading scale', xkey='CLARITY_SCALE')
C(T, 'Colour scale detail', 'ATTRIBUTE_GAP', 'COLOUR', 'SUPPORT', r'colou?r', 'Go deeper on colour', 'BRIEF_MENTION_AND_LINK', owner='EDU-4C-05', anchor='color grade diamond', xkey='COLOUR_SCALE')
C(T, 'Cut grade detail', 'ATTRIBUTE_GAP', 'CUT', 'SUPPORT', r'\bcut\b', 'Go deeper on cut', 'BRIEF_MENTION_AND_LINK', owner='EDU-4C-06', anchor='diamond cut grade', xkey='CUT_GRADE')
C(T, 'Carat detail', 'ATTRIBUTE_GAP', 'CARAT', 'SUPPORT', r'carat', 'Go deeper on carat', 'BRIEF_MENTION_AND_LINK', owner='EDU-4C-07', anchor='is 1 carat diamond good', xkey='CARAT_WEIGHT')
C(T, 'Who grades (GIA created the 4Cs system; IGI, AGS)', 'ENTITY_GAP', 'CERTIFICATION', 'SUPPORT', r'\bgia\b|\bigi\b|\bags\b', 'Know the authority behind the scale',
  'BRIEF_MENTION_AND_LINK', owner='EDU-CERT-00', anchor='lab-grown diamond certification', xkey='CERT_BASICS', stage='VERIFY')
C(T, 'Beyond the 4Cs (fluorescence, polish, symmetry)', 'SUPPORTING_CONCEPT_GAP', 'QUALITY', 'OPTIONAL', r'fluoresc|polish|symmetr', 'Know other report fields', 'INLINE_ANSWER')
C(T, 'Flawless lab-grown diamonds', 'ATTRIBUTE_GAP', 'CLARITY', 'OPTIONAL', r'flawless', 'Understand top grades', 'BRIEF_MENTION_AND_LINK', owner='EDU-4C-03', anchor='v v s diamond', xkey='VVS_IF_FL')

# --- EDU-4C-01 clarity
T = 'EDU-4C-01'
C(T, 'Clarity scale FL to I3 (GIA grade groups)', 'CORE_CONCEPT_GAP', 'CLARITY', 'CORE', r'\bfl\b|flawless|\bif\b|vvs|\bvs ?[12]?\b|\bsi ?[12]?\b|\bi[123]\b|scale|grade',
  'Understand the clarity grades', 'CORE_SECTION', xkey='CLARITY_SCALE')
C(T, 'Clarity chart best to worst (visual reference)', 'SERP_FORMAT_GAP', 'CLARITY', 'CORE', r'chart|best to worst', 'See the scale visually', 'VISUAL_CHART',
  note='The validated head SERP is reference/chart-led (Stage 17).')
C(T, 'Inclusions and blemishes (types, which to avoid)', 'CORE_CONCEPT_GAP', 'CLARITY', 'CORE', r'inclusion|blemish|feather|crystal|cloud|pinpoint|needle|characteristics',
  'Know what clarity grades describe', 'SUPPORTING_SECTION')
C(T, 'Eye-clean and best-value clarity', 'ATTRIBUTE_GAP', 'VALUE', 'CORE', r'eye[- ]clean|value|best clarity|good clarity|what clarity', 'Pick the clarity worth paying for', 'CORE_SECTION', stage='DECIDE')
C(T, 'Clarity and shape (step cuts show more)', 'ATTRIBUTE_GAP', 'SHAPE', 'SUPPORT', r'shape|step cut|emerald|asscher', 'Adjust clarity to shape', 'INLINE_ANSWER')
C(T, 'Clarity vs carat trade-off', 'COMPARISON_GAP', 'CARAT', 'SUPPORT', r'bigger|carat|size', 'Balance size and clarity', 'SUPPORTING_SECTION', stage='DECIDE')
C(T, 'Grade comparisons (VVS vs VS, VS vs SI)', 'COMPARISON_GAP', 'CLARITY', 'SUPPORT', r'vvs (or|vs) vs|vs (or|vs) si|\bvs\b.*\b(si|vvs)', 'Compare adjacent grades', 'COMPARISON_TABLE', stage='COMPARE')
C(T, 'VS1 / VS2 grades (EDU-4C-04 conditional; interim home here)', 'ATTRIBUTE_GAP', 'CLARITY', 'SUPPORT', r'vs ?1|vs ?2|\bvs clarity|vs diamond clarity',
  'Understand VS grades', 'SUPPORTING_SECTION', owner='EDU-4C-04', anchor='vs clarity diamond', xkey='VS_GRADES')
C(T, 'SI grades detail', 'ATTRIBUTE_GAP', 'CLARITY', 'SUPPORT', r'\bsi ?[123]?\b', 'Go deeper on SI', 'BRIEF_MENTION_AND_LINK', owner='EDU-4C-02', anchor='si2 diamond clarity', xkey='SI_GRADES')
C(T, 'VVS / IF / FL detail', 'ATTRIBUTE_GAP', 'CLARITY', 'SUPPORT', r'vvs|flawless|\bif\b', 'Go deeper on top grades', 'BRIEF_MENTION_AND_LINK', owner='EDU-4C-03', anchor='v v s diamond', xkey='VVS_IF_FL')
C(T, 'GIA as the grading authority for the clarity scale', 'ENTITY_GAP', 'CERTIFICATION', 'SUPPORT', r'\bgia\b', 'Trust the scale', 'INLINE_ANSWER', stage='VERIFY')
C(T, 'Lab-grown diamond clarity', 'ATTRIBUTE_GAP', 'CLARITY', 'SUPPORT', r'\blab\b', 'Know clarity applies to lab-grown', 'INLINE_ANSWER')
C(T, 'Colour chart cross-reference (related search "diamond color chart")', 'INTERNAL_CONTEXT_GAP', 'COLOUR', 'OPTIONAL', r'colou?r', 'Find the colour scale', 'BRIEF_MENTION_AND_LINK',
  owner='EDU-4C-05', anchor='color grade diamond', xkey='COLOUR_SCALE')

# --- EDU-4C-02 SI
T = 'EDU-4C-02'
C(T, 'What SI1 / SI2 mean and where they sit on the scale', 'DEFINITION_GAP', 'CLARITY', 'CORE', r'\bsi ?[123]?\b|slightly included|meaning|definition|what is',
  'Understand SI', 'DEFINITION_BLOCK', xkey='SI_GRADES')
C(T, 'Is SI good / eye-clean SI', 'QUESTION_GAP', 'CLARITY', 'CORE', r'\bgood\b|eye[- ]clean|visible|\bbad\b|appearance', 'Know if SI is acceptable', 'CORE_SECTION', stage='EVALUATE')
C(T, 'Pros and cons of SI clarity', 'SUPPORTING_CONCEPT_GAP', 'VALUE', 'CORE', r'\bpros\b|\bcons\b', 'Weigh SI', 'SUPPORTING_SECTION', stage='EVALUATE')
C(T, 'Buying tips (smaller sizes, avoid step cuts, inspect closely)', 'SERP_FORMAT_GAP', 'DECISION', 'CORE', r'tips|step cut|smaller|inspect|\bshape\b',
  'Buy an SI stone safely', 'STEP_SEQUENCE', stage='DECIDE')
C(T, 'SI vs VS / SI vs VVS', 'COMPARISON_GAP', 'CLARITY', 'SUPPORT', r'vs ?1|vvs|\bvs\b', 'Compare to higher grades', 'SUPPORTING_SECTION', stage='COMPARE')
C(T, 'SI value / price context (no live prices)', 'ATTRIBUTE_GAP', 'PRICE', 'SUPPORT', r'price|worth|value|cost|increase', 'Understand savings', 'SUPPORTING_SECTION', stage='EVALUATE')
C(T, 'SI3 (non-GIA) and the I1 boundary', 'ATTRIBUTE_GAP', 'CLARITY', 'SUPPORT', r'si3|\bi1\b', 'Decode unusual grades', 'INLINE_ANSWER')
C(T, 'Colour + SI combinations (e.g. G SI2)', 'ATTRIBUTE_GAP', 'COLOUR', 'OPTIONAL', r'\b[d-k] si', 'Judge combinations', 'FAQ')
C(T, 'SI on-hand appearance (visual examples)', 'EXAMPLE_GAP', 'CLARITY', 'OPTIONAL', r'on hand|photo|picture', 'See real examples', 'SUPPORTING_SECTION')
C(T, 'HOD SI-grade stones / rings (Shopping unit on both SERPs)', 'COMMERCIAL_CONTEXT_GAP', 'COMMERCIAL', 'BIZ', r'\bring\b|price',
  'Shop SI stones', 'BUSINESS_INPUT_REQUIRED', biz='Whether HOD lists SI-grade stones/products with grades shown (catalogue attribute)', stage='BUY')

# --- EDU-4C-03 VVS / IF / FL
T = 'EDU-4C-03'
C(T, 'What VVS means', 'DEFINITION_GAP', 'CLARITY', 'CORE', r'vvs|very very|\bmeans?\b|definition', 'Understand VVS', 'DEFINITION_BLOCK', xkey='VVS_IF_FL')
C(T, 'VVS1 vs VVS2', 'COMPARISON_GAP', 'CLARITY', 'CORE', r'vvs ?1|vvs ?2', 'Tell the two apart', 'SUPPORTING_SECTION', stage='COMPARE')
C(T, 'IF and FL (flawless) grades', 'ATTRIBUTE_GAP', 'CLARITY', 'CORE', r'\bif\b|internally flawless|flawless|\bfl\b', 'Understand the top grades', 'SUPPORTING_SECTION')
C(T, 'Is VVS worth it (visible difference vs VS)', 'QUESTION_GAP', 'VALUE', 'CORE', r'worth|vs diamonds|difference|appearance', 'Decide if VVS is worth paying for', 'CORE_SECTION', stage='DECIDE')
C(T, 'VVS price context (no live prices)', 'ATTRIBUTE_GAP', 'PRICE', 'SUPPORT', r'price|expensive|cost|how much', 'Understand cost', 'SUPPORTING_SECTION', stage='EVALUATE')
C(T, 'VVS lab-grown diamonds', 'ATTRIBUTE_GAP', 'ORIGIN', 'SUPPORT', r'\blab\b', 'Know VVS lab-grown options', 'SUPPORTING_SECTION')
C(T, '"Are VVS diamonds real" (VVS is a grade, not a type)', 'DEFINITION_GAP', 'CLARITY', 'SUPPORT', r'\breal\b', 'Clear up the misconception', 'INLINE_ANSWER')
C(T, 'VVS in jewellery (chains, earrings, rings)', 'COMMERCIAL_CONTEXT_GAP', 'COMMERCIAL', 'BIZ', r'chain|earring|\bring\b',
  'Shop VVS jewellery', 'BUSINESS_INPUT_REQUIRED', biz='Whether HOD products show VVS grades (catalogue attribute)', stage='BUY')

# --- EDU-4C-05 colour
T = 'EDU-4C-05'
C(T, 'D-to-Z colour scale and grade groups (colourless, near-colourless, faint)', 'CORE_CONCEPT_GAP', 'COLOUR', 'CORE', r'd[- ]to[- ]z|scale|colou?rless|near[- ]colou?rless|faint|grade',
  'Understand colour grades', 'CORE_SECTION', xkey='COLOUR_SCALE')
C(T, 'Colour chart (visual)', 'SERP_FORMAT_GAP', 'COLOUR', 'CORE', r'chart', 'See colour grades visually', 'VISUAL_CHART')
C(T, 'Is G–H good (near-colourless value)', 'QUESTION_GAP', 'VALUE', 'CORE', r'\bg[- ]?h\b|\bgh\b|\bgood\b', 'Pick good-value colour', 'CORE_SECTION', stage='DECIDE')
C(T, 'No visible tint / face-up appearance', 'ATTRIBUTE_GAP', 'COLOUR', 'SUPPORT', r'tint|visible|yellow', 'Know what you will see', 'SUPPORTING_SECTION')
C(T, 'Colour and metal / setting flexibility', 'ATTRIBUTE_GAP', 'MATERIAL', 'SUPPORT', r'metal|setting|gold|platinum', 'Match colour to metal', 'SUPPORTING_SECTION', stage='DECIDE')
C(T, 'Colour with size and shape', 'ATTRIBUTE_GAP', 'SHAPE', 'SUPPORT', r'carat size|\bshape\b|\bsize\b', 'Adjust colour to size/shape', 'INLINE_ANSWER')
C(T, 'Grade comparisons (GH vs FG, D vs E)', 'COMPARISON_GAP', 'COLOUR', 'SUPPORT', r'\b(gh|fg|[d-k])\b (vs|or) \b(gh|fg|[d-k])\b|better', 'Compare adjacent grades', 'COMPARISON_TABLE', stage='COMPARE')
C(T, 'Colour price effect', 'ATTRIBUTE_GAP', 'PRICE', 'SUPPORT', r'price|value|cost', 'Understand savings', 'INLINE_ANSWER', stage='EVALUATE')
C(T, 'Ambiguous "x vs diamond" keywords (colour + VS clarity)', 'ATTRIBUTE_GAP', 'QUALITY', 'OPTIONAL', r'^[d-k](-[d-k])? vs diamond$|^[d-k][d-k] vs diamond$',
  'Interpret colour+clarity shorthand', 'BRIEF_MENTION_AND_LINK', owner='EDU-4C-00', anchor='diamond grading scale', xkey='COLOUR_CLARITY_COMBOS',
  note='Stage 17 POSSIBLE_OVERLAP; ownership unchanged (Stage 15 maps them here).')
C(T, 'Fancy colours boundary (EDU-4C-08 conditional)', 'SUPPORTING_CONCEPT_GAP', 'COLOUR', 'OPTIONAL', r'fancy', 'Know where fancy colours start', 'BRIEF_MENTION_AND_LINK',
  owner='EDU-4C-08', anchor='are black diamonds real', xkey='FANCY_COLOUR')
C(T, 'Lab-grown colour grades', 'ATTRIBUTE_GAP', 'ORIGIN', 'SUPPORT', r'\blab\b', 'Know colour applies to lab-grown', 'INLINE_ANSWER')

# --- EDU-4C-06 cut
T = 'EDU-4C-06'
C(T, 'Cut grade scale (Excellent/Ideal to Poor)', 'CORE_CONCEPT_GAP', 'CUT', 'CORE', r'excellent|very good|ideal|\bpoor\b|\bfair\b|grade|scale',
  'Understand cut grades', 'CORE_SECTION', xkey='CUT_GRADE')
C(T, 'Light performance: brightness, fire, scintillation', 'CORE_CONCEPT_GAP', 'CUT', 'CORE', r'brightness|\bfire\b|scintillation|sparkle|light|refract',
  'Understand why cut drives sparkle', 'SUPPORTING_SECTION')
C(T, 'Proportions, polish and symmetry', 'ATTRIBUTE_GAP', 'CUT', 'CORE', r'polish|symmetr|proportion|depth|table', 'Know what is measured', 'SUPPORTING_SECTION')
C(T, 'Cut grade vs shape disambiguation', 'DEFINITION_GAP', 'SHAPE', 'CORE', r'\bshape|types of diamond cuts|cuts in diamond|brilliant',
  'Separate cut quality from shape', 'INLINE_ANSWER', note='Shapes overview is owned by EDU-SHP-00.')
C(T, 'Cut grading for round vs fancy shapes', 'ATTRIBUTE_GAP', 'CUT', 'SUPPORT', r'\bround\b|fancy', 'Know grading limits for fancy shapes', 'INLINE_ANSWER')
C(T, 'Ideal vs Excellent', 'COMPARISON_GAP', 'CUT', 'SUPPORT', r'ideal vs excellent|\bideal\b', 'Compare top grades', 'INLINE_ANSWER', stage='COMPARE')
C(T, 'GIA / IGI cut grading', 'ENTITY_GAP', 'CERTIFICATION', 'SUPPORT', r'\bgia\b|\bigi\b', 'Know who assigns cut grades', 'INLINE_ANSWER', stage='VERIFY')
C(T, 'Facets and diamond anatomy', 'ENTITY_GAP', 'CUT', 'SUPPORT', r'facet|crown|pavilion|culet|girdle', 'Learn the terms', 'SUPPORTING_SECTION')
C(T, 'Best cut for sparkle / does cut matter', 'QUESTION_GAP', 'CUT', 'SUPPORT', r'\bbest\b|matter|sparkle', 'Prioritise cut', 'CORE_SECTION', stage='DECIDE')
C(T, 'Cheapest cut (shape/cut price confusion)', 'QUESTION_GAP', 'PRICE', 'OPTIONAL', r'cheap', 'Understand price by cut', 'FAQ')
C(T, 'Cut grade chart (visual)', 'SERP_FORMAT_GAP', 'CUT', 'SUPPORT', r'chart', 'See grades visually', 'VISUAL_CHART')

# --- EDU-4C-07 carat
T = 'EDU-4C-07'
C(T, 'Carat is weight, not size (weight vs face-up size)', 'DEFINITION_GAP', 'CARAT', 'CORE', r'carat|weight|\bsize\b|\bmm\b', 'Understand carat', 'DEFINITION_BLOCK', xkey='CARAT_WEIGHT')
C(T, 'Is N carat good / big enough (size perception)', 'QUESTION_GAP', 'SIZE', 'CORE', r'\bgood\b|\bbig\b|small|too', 'Judge whether a size is right', 'CORE_SECTION', stage='EVALUATE',
  note='About 36 variants collapse into one section (Stage 17); not separate FAQs.')
C(T, 'Carat size chart (mm, on hand)', 'SERP_FORMAT_GAP', 'SIZE', 'CORE', r'chart|\bmm\b|on hand', 'Visualise sizes', 'VISUAL_CHART')
C(T, 'Carat (ct) vs total carat weight (ctw)', 'DEFINITION_GAP', 'CARAT', 'SUPPORT', r'ctw|total carat|\btw\b', 'Read product specs correctly', 'INLINE_ANSWER', stage='VERIFY')
C(T, 'Fractional carat weights (1/2, 1/3, 1/4, 3/4)', 'ATTRIBUTE_GAP', 'CARAT', 'SUPPORT', r'1/2|1/3|1/4|3/4|half', 'Decode fractions', 'INLINE_ANSWER')
C(T, 'Carat sizes for stud earrings', 'ATTRIBUTE_GAP', 'SIZE', 'SUPPORT', r'stud|earring', 'Choose stud size', 'SUPPORTING_SECTION', stage='DECIDE')
C(T, 'Price by carat', 'ATTRIBUTE_GAP', 'PRICE', 'SUPPORT', r'price|cost|worth', 'Understand price jumps', 'INLINE_ANSWER', stage='EVALUATE')
C(T, 'Karat vs carat confusion', 'DEFINITION_GAP', 'TERMINOLOGY', 'OPTIONAL', r'karat|14k|18k', 'Avoid unit confusion', 'BRIEF_MENTION_AND_LINK',
  owner='EDU-MET-01', anchor='is 18k gold or 14k gold better', xkey='KARAT_VS_CARAT')
C(T, 'Flashiness / social perception of large stones', 'QUESTION_GAP', 'PERCEPTION', 'OPTIONAL', r'flashy', 'Social worry', 'FAQ')
C(T, 'Carat-led loose-stone shopping (CL-006 commercial, deferred)', 'COMMERCIAL_CONTEXT_GAP', 'COMMERCIAL', 'BIZ', r'lab grown|loose|for sale',
  'Shop by carat', 'BUSINESS_INPUT_REQUIRED', biz='Loose-stone / carat-led commercial pages deferred (Stage 12); HOD loose-stone offer unknown', stage='BUY')

# --- EDU-SHP-00 shapes
T = 'EDU-SHP-00'
C(T, 'Main shapes overview (round, princess, oval, cushion, emerald, pear, marquise, radiant, asscher, heart)', 'CORE_CONCEPT_GAP', 'SHAPE', 'CORE',
  r'\bround\b|princess|\boval\b|cushion|emerald|\bpear\b|marquise|radiant|asscher|heart', 'See the shape options', 'CORE_SECTION', xkey='SHAPES_OVERVIEW')
C(T, 'Shape vs cut distinction', 'DEFINITION_GAP', 'SHAPE', 'CORE', r'shape vs|versus cut|\bcut\b', 'Separate shape from cut quality', 'INLINE_ANSWER')
C(T, 'Choosing a shape for an engagement ring', 'USER_JOURNEY_GAP', 'STYLE', 'CORE', r'engagement|choose|should i get|\bring\b', 'Choose a shape', 'CORE_SECTION', stage='DECIDE')
C(T, 'Shape characteristics (length-to-width ratio, sparkle, finger coverage, bow-tie)', 'ATTRIBUTE_GAP', 'SHAPE', 'SUPPORT', r'ratio|sparkle|finger|elongat|bow[- ]?tie',
  'Compare shape traits', 'COMPARISON_TABLE', stage='COMPARE')
C(T, 'Price differences by shape', 'ATTRIBUTE_GAP', 'PRICE', 'SUPPORT', r'price|expensive|cheap', 'Understand shape pricing', 'INLINE_ANSWER', stage='EVALUATE')
C(T, 'Asscher vs emerald', 'COMPARISON_GAP', 'SHAPE', 'SUPPORT', r'asscher|emerald', 'Compare similar step cuts', 'INLINE_ANSWER', stage='COMPARE')
C(T, 'Shapes chart with images', 'SERP_FORMAT_GAP', 'SHAPE', 'SUPPORT', r'chart|pictures|images', 'Recognise shapes visually', 'VISUAL_CHART')
C(T, 'Geometric "diamond shape" intent (rhombus, face shape, drawing)', 'SERP_FORMAT_GAP', 'SHAPE', 'AVOID', r'rhombus|kite|\bface\b|drawing|another word|shape called|shape name|shape meaning',
  'Non-jewellery intent', 'AVOID', note='Do not target geometric meaning; keep the page jewellery-specific.')
C(T, 'Individual shape depth (per-shape pages EDU-SHP-01 deferred)', 'SUPPORTING_CONCEPT_GAP', 'SHAPE', 'SUPPORT', r'radiant cut|asscher cut|princess cut',
  'Learn one shape in detail', 'SUPPORTING_SECTION', owner='EDU-SHP-01', xkey='PER_SHAPE',
  note='No per-shape page exists; short per-shape entries stay inside this pillar (Stage 14 D14-17).', extra=('Stage 14 D14-17: EDU-SHP-01 DEFERRED', 1))
C(T, 'Oval with marquise side stones (product example)', 'EXAMPLE_GAP', 'SHAPE', 'OPTIONAL', r'marquise|\boval\b', 'See a shape in a real design', 'BRIEF_MENTION_AND_LINK',
  owner='COM-PDP-OVAL-FLORAL', anchor='marquise oval diamond', xkey='OVAL_MARQUISE_PDP')
C(T, 'Shape x jewellery shopping (D-19 unapproved)', 'COMMERCIAL_CONTEXT_GAP', 'COMMERCIAL', 'BIZ', r'shape ring|shape jewelry',
  'Shop by shape', 'BUSINESS_INPUT_REQUIRED', biz='Shape filters are commercial (Stage 12 D-08); shape x jewellery demand needs D-19', stage='BUY')

# --- EDU-CERT-00 certification
T = 'EDU-CERT-00'
C(T, 'What a diamond certificate / grading report is (vs an appraisal)', 'DEFINITION_GAP', 'CERTIFICATION', 'CORE', r'certif|report|grading|appraisal',
  'Understand certification', 'DEFINITION_BLOCK', xkey='CERT_BASICS')
C(T, 'Do lab-grown diamonds come with certificates', 'QUESTION_GAP', 'CERTIFICATION', 'CORE', r'\blab\b', 'Know whether to expect one', 'CORE_SECTION', stage='VERIFY')
C(T, 'Which labs certify (GIA, IGI, GCAL and others)', 'ENTITY_GAP', 'CERTIFICATION', 'CORE', r'\bgia\b|\bigi\b|gcal|\bags\b|laborator', 'Know the labs', 'SUPPORTING_SECTION')
C(T, 'What a report includes (4Cs, origin disclosure, growth method, inscription)', 'ATTRIBUTE_GAP', 'CERTIFICATION', 'CORE', r'4 ?cs|origin|growth|inscri|includes?',
  'Read what the report tells you', 'SUPPORTING_SECTION', stage='VERIFY')
C(T, 'Verify a report (report check / serial number lookup)', 'PROCESS_GAP', 'CERTIFICATION', 'CORE', r'check|verify|lookup|look up|serial',
  'Confirm the report is genuine', 'STEP_SEQUENCE', xkey='CERT_VERIFY', stage='VERIFY')
C(T, 'GIA lab-grown reports (does GIA still certify lab-grown)', 'ENTITY_GAP', 'CERTIFICATION', 'SUPPORT', r'\bgia\b', 'Know GIA\'s position', 'SUPPORTING_SECTION')
C(T, 'IGI reports (IGI-only page EDU-CERT-03 deferred)', 'ENTITY_GAP', 'CERTIFICATION', 'SUPPORT', r'\bigi\b', 'Understand IGI reports', 'SUPPORTING_SECTION',
  note='Existing article is IGI-only; retarget to general certification (Stage 13/14).')
C(T, 'Certification cost', 'ATTRIBUTE_GAP', 'PRICE', 'OPTIONAL', r'price|cost', 'Know the cost', 'INLINE_ANSWER')
C(T, 'GIA vs IGI detailed comparison', 'COMPARISON_GAP', 'CERTIFICATION', 'SUPPORT', r'\bvs\b|better|best', 'Choose between labs', 'BRIEF_MENTION_AND_LINK',
  owner='EDU-CERT-01', anchor='gia vs igi lab diamond', xkey='GIA_VS_IGI', stage='COMPARE')
C(T, 'How to read a grading report (EDU-CERT-02 conditional; interim home here)', 'PROCESS_GAP', 'CERTIFICATION', 'SUPPORT', r'read|report',
  'Interpret each field', 'SUPPORTING_SECTION', owner='EDU-CERT-02', anchor='diamond grading report', xkey='READ_REPORT')
C(T, 'Which lab reports come with HOD stones', 'TRUST_EVIDENCE_GAP', 'COMMERCIAL', 'BIZ', r'certified', 'Trust HOD stones', 'BUSINESS_INPUT_REQUIRED',
  biz='Which labs grade HOD stones and whether reports are per product (Stage 16 conditional link)', stage='BUY')

# --- EDU-CERT-01 GIA vs IGI
T = 'EDU-CERT-01'
C(T, 'Grading approach differences for lab-grown', 'CORE_CONCEPT_GAP', 'CERTIFICATION', 'CORE', r'grading|approach|scale|descriptive', 'Understand how the labs differ', 'CORE_SECTION', xkey='GIA_VS_IGI', stage='COMPARE')
C(T, 'Growth-method disclosure on each report', 'ATTRIBUTE_GAP', 'CERTIFICATION', 'CORE', r'growth|method|disclos|\bcvd\b|\bhpht\b', 'Know what each report states', 'SUPPORTING_SECTION', stage='VERIFY')
C(T, 'Cost and availability (why IGI is cheaper)', 'ATTRIBUTE_GAP', 'PRICE', 'CORE', r'cost|cheaper|price|availab', 'Understand price differences', 'SUPPORTING_SECTION', stage='EVALUATE')
C(T, 'Which to choose (by use case)', 'USER_JOURNEY_GAP', 'DECISION', 'CORE', r'choose|better|\bbest\b|which', 'Pick a lab', 'CORE_SECTION', stage='DECIDE')
C(T, 'Side-by-side comparison table', 'SERP_FORMAT_GAP', 'COMPARISON', 'CORE', r'\bvs\b', 'Scan differences', 'COMPARISON_TABLE', stage='COMPARE')
C(T, 'Other labs (GCAL, AGS, EGL, GSI)', 'COMPARISON_GAP', 'CERTIFICATION', 'SUPPORT', r'gcal|\bags\b|\begl\b|\bgsi\b', 'Place other labs', 'SUPPORTING_SECTION', stage='COMPARE')
C(T, 'IGI for natural diamonds', 'ATTRIBUTE_GAP', 'ORIGIN', 'OPTIONAL', r'natural', 'Know IGI grades natural too', 'INLINE_ANSWER')
C(T, 'Consistency / strictness perception (forums)', 'TRUST_EVIDENCE_GAP', 'PERCEPTION', 'SUPPORT', r'reddit|strict|consisten|reputable', 'Weigh reputations', 'INLINE_ANSWER', stage='EVALUATE')
C(T, 'Certification basics', 'DEFINITION_GAP', 'CERTIFICATION', 'SUPPORT', r'certif', 'Basics first', 'BRIEF_MENTION_AND_LINK', owner='EDU-CERT-00', anchor='lab-grown diamond certification', xkey='CERT_BASICS')

# --- EDU-MET-00 metals
T = 'EDU-MET-00'
C(T, 'Types of jewellery metals (gold, platinum, silver, alternative metals)', 'CORE_CONCEPT_GAP', 'MATERIAL', 'CORE', r'gold|platinum|silver|tungsten|titanium|metal',
  'See the metal options', 'CORE_SECTION', xkey='METALS_OVERVIEW')
C(T, 'Best metal for rings / wedding bands by lifestyle', 'USER_JOURNEY_GAP', 'DURABILITY', 'CORE', r'\bbest\b|wedding band|lifestyle|durab|job type',
  'Choose a metal', 'CORE_SECTION', stage='DECIDE')
C(T, 'White gold vs platinum', 'COMPARISON_GAP', 'MATERIAL', 'CORE', r'platinum', 'Compare the two white metals', 'COMPARISON_TABLE', stage='COMPARE',
  note='Head terms absent from Stage 7; SERP unvalidated.')
C(T, 'Rhodium plating (why, how long, re-plating) — EDU-MET-02 conditional, interim home here', 'SUPPORTING_CONCEPT_GAP', 'CARE', 'SUPPORT', r'rhodium|re-?plat|plating',
  'Understand white-gold upkeep', 'SUPPORTING_SECTION', owner='EDU-MET-02', anchor='rhodium plating ring', xkey='RHODIUM')
C(T, 'Hypoallergenic metals / skin sensitivity', 'ATTRIBUTE_GAP', 'MATERIAL', 'SUPPORT', r'hypoallergenic|allerg|nickel|skin', 'Avoid reactions', 'SUPPORTING_SECTION')
C(T, 'Mixing gold and silver', 'QUESTION_GAP', 'STYLE', 'SUPPORT', r'gold and silver|\bmix|together', 'Style question', 'FAQ')
C(T, 'Tungsten and titanium (pros/cons; cannot be resized)', 'ENTITY_GAP', 'MATERIAL', 'BIZ', r'tungsten|titanium', 'Evaluate alternative metals',
  'BUSINESS_INPUT_REQUIRED', biz='No catalogue evidence HOD sells tungsten/titanium (Stage 15 business dependency)')
C(T, 'Sterling silver (925)', 'ENTITY_GAP', 'MATERIAL', 'SUPPORT', r'925|sterling|silver', 'Understand silver', 'INLINE_ANSWER')
C(T, 'Gold colours (yellow, white, rose)', 'ATTRIBUTE_GAP', 'MATERIAL', 'SUPPORT', r'rose gold|yellow gold|white gold', 'Choose a gold colour', 'SUPPORTING_SECTION')
C(T, 'Gold karat comparison (10k/14k/18k)', 'COMPARISON_GAP', 'MATERIAL', 'SUPPORT', r'\b1[048] ?k\b|karat', 'Choose purity', 'BRIEF_MENTION_AND_LINK',
  owner='EDU-MET-01', anchor='is 18k gold or 14k gold better', xkey='GOLD_KARATS')
C(T, 'Resizing by metal', 'SUPPORTING_CONCEPT_GAP', 'SIZE', 'OPTIONAL', r'resiz', 'Know resizing limits', 'BRIEF_MENTION_AND_LINK', owner='EDU-RJG-02', anchor='are mens and womens ring sizes the same', xkey='RESIZING')
C(T, 'Astrology / health-benefit claims (related searches)', 'SERP_FORMAT_GAP', 'OTHER', 'AVOID', r'astrolog|luck|health benefit', 'Not a trust-safe topic', 'AVOID')
C(T, 'HOD metal options (karats, platinum availability)', 'COMMERCIAL_CONTEXT_GAP', 'COMMERCIAL', 'BIZ', None, 'Shop by metal', 'BUSINESS_INPUT_REQUIRED',
  biz='HOD metal/karat options per product (Stage 16 conditional links)', stage='BUY', extra=('Stage 16: karat-option links conditional on business facts', 1))

# --- EDU-MET-01 14k vs 18k
T = 'EDU-MET-01'
C(T, 'Purity by karat (10k 41.7%, 14k 58.3%, 18k 75%)', 'CORE_CONCEPT_GAP', 'MATERIAL', 'CORE', r'pur(e|ity)|%|percent|karat', 'Understand what the numbers mean', 'CORE_SECTION', xkey='GOLD_KARATS')
C(T, 'Durability for daily wear (18k softness)', 'ATTRIBUTE_GAP', 'DURABILITY', 'CORE', r'durab|soft|scratch|daily|everyday|lasts?\b|strength', 'Know which lasts', 'CORE_SECTION', stage='COMPARE')
C(T, 'Appearance / colour richness', 'ATTRIBUTE_GAP', 'MATERIAL', 'CORE', r'appearance|colou?r|yellow|rich', 'Know how they look', 'SUPPORTING_SECTION', stage='COMPARE')
C(T, 'Price difference', 'ATTRIBUTE_GAP', 'PRICE', 'CORE', r'price|cost|expensive|cheap', 'Understand cost', 'SUPPORTING_SECTION', stage='EVALUATE')
C(T, 'Which is better (for engagement rings / jewellery)', 'USER_JOURNEY_GAP', 'DECISION', 'CORE', r'better|engagement|\bring\b', 'Decide', 'CORE_SECTION', stage='DECIDE')
C(T, 'Key-differences comparison table', 'SERP_FORMAT_GAP', 'COMPARISON', 'CORE', r'key differences|\bvs\b', 'Scan differences', 'COMPARISON_TABLE', stage='COMPARE')
C(T, 'Skin sensitivity / allergies', 'ATTRIBUTE_GAP', 'MATERIAL', 'SUPPORT', r'skin|allerg|nickel|hypoallergenic', 'Avoid reactions', 'INLINE_ANSWER')
C(T, '10k gold (is it cheap / worth anything)', 'ATTRIBUTE_GAP', 'MATERIAL', 'SUPPORT', r'10 ?k', 'Evaluate 10k', 'SUPPORTING_SECTION', stage='EVALUATE')
C(T, 'Resale / melt value by karat', 'ATTRIBUTE_GAP', 'RESALE', 'SUPPORT', r'resale|melt|worth|\bsell|scrap|value', 'Understand value retention', 'SUPPORTING_SECTION', stage='EVALUATE')
C(T, 'Karat vs carat clarification ("14k diamond")', 'DEFINITION_GAP', 'TERMINOLOGY', 'SUPPORT', r'14k diamond|carat', 'Avoid unit confusion', 'INLINE_ANSWER', xkey='KARAT_VS_CARAT',
  note='Serves the ranking keyword "is 14k diamond good".')
C(T, '22k / 24k context', 'COMPARISON_GAP', 'MATERIAL', 'OPTIONAL', r'2[24] ?k', 'Place higher karats', 'INLINE_ANSWER')
C(T, 'Pawn-shop value questions', 'QUESTION_GAP', 'RESALE', 'AVOID', r'pawn', 'Off-topic for HOD', 'AVOID')
C(T, 'Which karats HOD offers', 'COMMERCIAL_CONTEXT_GAP', 'COMMERCIAL', 'BIZ', None, 'Buy in the chosen karat', 'BUSINESS_INPUT_REQUIRED',
  biz='HOD karat options per product (Stage 16 conditional)', stage='BUY', extra=('Stage 16: karat-option links conditional on business facts', 1))

# --- EDU-RJG-01 settings
T = 'EDU-RJG-01'
C(T, 'Setting types (prong, bezel, pavé, halo, channel, tension, three-stone)', 'CORE_CONCEPT_GAP', 'SETTING', 'CORE',
  r'prong|bezel|pav[eé]|halo|channel|tension|three[- ]stone|solitaire|cathedral|settings?', 'See the setting options', 'CORE_SECTION', xkey='SETTING_TYPES')
C(T, 'Sparkle vs security trade-off (best setting to show off a diamond)', 'USER_JOURNEY_GAP', 'SETTING', 'CORE', r'\bbest\b|sparkle|durab|secure|show off|protect',
  'Choose a setting', 'CORE_SECTION', stage='DECIDE')
C(T, 'Settings with pictures / chart', 'SERP_FORMAT_GAP', 'SETTING', 'CORE', r'picture|chart|pdf|image', 'Recognise settings visually', 'VISUAL_CHART')
C(T, 'Setting vs mounting terminology', 'DEFINITION_GAP', 'TERMINOLOGY', 'SUPPORT', r'mounting', 'Decode terms', 'INLINE_ANSWER')
C(T, 'Settings by jewellery type (engagement rings, necklaces, studs)', 'ATTRIBUTE_GAP', 'SETTING', 'SUPPORT', r'necklace|earring|\bstud|engagement', 'Apply to other pieces', 'SUPPORTING_SECTION')
C(T, 'High vs low setting profile', 'ATTRIBUTE_GAP', 'SETTING', 'SUPPORT', r'high|low profile|profile', 'Choose height', 'INLINE_ANSWER')
C(T, 'Halo effect on apparent size', 'ATTRIBUTE_GAP', 'SIZE', 'SUPPORT', r'halo', 'Understand halo benefits', 'INLINE_ANSWER')
C(T, 'Milgrain detailing', 'ATTRIBUTE_GAP', 'STYLE', 'OPTIONAL', r'milgrain', 'Decode the term', 'INLINE_ANSWER')
C(T, '"Do diamonds need breathing holes" myth', 'QUESTION_GAP', 'SETTING', 'OPTIONAL', r'breath', 'Clear up a myth', 'FAQ')
C(T, 'Side-stone rings (commercial subcategory)', 'COMMERCIAL_CONTEXT_GAP', 'STYLE', 'OPTIONAL', r'side stone', 'Shop side-stone styles', 'BRIEF_MENTION_AND_LINK',
  owner='COM-ER-SIDESTONE', anchor='side stones engagement rings', xkey='SIDE_STONE_CATEGORY', stage='BUY')
C(T, 'HOD setting styles available (engagement style subcategories conditional)', 'COMMERCIAL_CONTEXT_GAP', 'COMMERCIAL', 'BIZ', r'tiffany|for engagement',
  'Shop by setting', 'BUSINESS_INPUT_REQUIRED', owner='COM-ER-STYLES', biz='Populated engagement style subcategories (Stage 12 PROPOSED_CONDITIONAL)', stage='BUY')

# --- EDU-RJG-02 ring size
T = 'EDU-RJG-02'
C(T, 'How to measure ring size at home (string/paper, existing ring)', 'PROCESS_GAP', 'SIZE', 'CORE', r'measure|\bfind\b|at home|string|paper',
  'Find the right size', 'STEP_SEQUENCE', stage='DECIDE',
  extra=('Stage 14 topic scope for EDU-RJG-02: "Ring size guide (finding your size, resizing)"; existing article title is a measuring guide', 1))
C(T, 'Ring size chart (US sizes with diameter/circumference in mm)', 'SERP_FORMAT_GAP', 'SIZE', 'CORE', r'chart|\bmm\b|diameter|circumference|\bsizes?\b',
  'Convert measurement to size', 'VISUAL_CHART')
C(T, 'Resizing (up/down, feasibility)', 'CORE_CONCEPT_GAP', 'SIZE', 'CORE', r'resiz|smaller|bigger|larger', 'Fix a wrong size', 'CORE_SECTION', xkey='RESIZING')
C(T, 'Men\'s vs women\'s ring sizes', 'COMPARISON_GAP', 'SIZE', 'SUPPORT', r'\bmen|women', 'Size for the right wearer', 'INLINE_ANSWER')
C(T, 'Band width and fit', 'ATTRIBUTE_GAP', 'SIZE', 'SUPPORT', r'thick|width|wide|\bfit\b', 'Adjust for band width', 'INLINE_ANSWER')
C(T, 'Metals that cannot be resized (titanium, stainless, tungsten)', 'ATTRIBUTE_GAP', 'MATERIAL', 'SUPPORT', r'titanium|stainless|tungsten', 'Know limits', 'INLINE_ANSWER')
C(T, 'Ring sizer tool (EDU-RJG-05 conditional; tool embedded by default)', 'SERP_FORMAT_GAP', 'SIZE', 'SUPPORT', r'sizer|tool|printable',
  'Measure with a tool', 'BRIEF_MENTION_AND_LINK', owner='EDU-RJG-05', xkey='RING_SIZER', extra=('Stage 14/15: tool embedded in EDU-RJG-02 by default', 1))
C(T, 'HOD resizing policy (belongs on FAQ/policy pages)', 'COMMERCIAL_CONTEXT_GAP', 'COMMERCIAL', 'BIZ', r'where can i|resiz', 'Know HOD\'s resizing service',
  'BUSINESS_INPUT_REQUIRED', owner='SUP-FAQ', biz='HOD resizing policy (Stage 15 business dependency)', stage='BUY')

# --- EDU-GEN-01 properties
T = 'EDU-GEN-01'
C(T, 'Composition: pure carbon', 'CORE_CONCEPT_GAP', 'MATERIAL', 'CORE', r'carbon|made of|element|composition|chemical', 'Know what a diamond is made of', 'CORE_SECTION')
C(T, 'Crystal structure / lattice', 'CORE_CONCEPT_GAP', 'MATERIAL', 'CORE', r'crystal|lattice|structure|cubic', 'Understand why diamond is hard', 'SUPPORTING_SECTION')
C(T, 'Hardness (Mohs 10) and what is harder than diamond', 'ATTRIBUTE_GAP', 'DURABILITY', 'CORE', r'\bhard|mohs', 'Understand hardness', 'CORE_SECTION', xkey='DIAMOND_HARDNESS')
C(T, 'Toughness: can diamonds chip, crack or break', 'ATTRIBUTE_GAP', 'DURABILITY', 'CORE', r'chip|crack|break|shatter|tough', 'Know real-world durability', 'CORE_SECTION', stage='EVALUATE')
C(T, 'Scratching', 'ATTRIBUTE_GAP', 'DURABILITY', 'SUPPORT', r'scratch', 'Know scratch risk', 'INLINE_ANSWER')
C(T, 'Melting / burning point', 'ATTRIBUTE_GAP', 'MATERIAL', 'SUPPORT', r'melt|burn|\bfire\b|heat', 'Curiosity', 'FAQ')
C(T, 'Lab-grown durability parity', 'COMPARISON_GAP', 'DURABILITY', 'SUPPORT', r'\blab\b', 'Know lab-grown is as durable', 'INLINE_ANSWER', stage='COMPARE')
C(T, 'Mineral classification', 'DEFINITION_GAP', 'MATERIAL', 'SUPPORT', r'mineral|\brock\b|\bgem\b', 'Classify diamond', 'INLINE_ANSWER')
C(T, 'Cutting diamonds (what cuts a diamond)', 'PROCESS_GAP', 'PROCESS', 'SUPPORT', r'\bcut', 'Understand cutting', 'INLINE_ANSWER')
C(T, 'Type IIa diamonds', 'ENTITY_GAP', 'MATERIAL', 'SUPPORT', r'type ?ii|\biia\b', 'Decode classification', 'INLINE_ANSWER', xkey='TYPE_IIA',
  note='Diamond types page EDU-GEN-02 is conditional.')
C(T, 'Related carbon forms (graphite, lonsdaleite)', 'ENTITY_GAP', 'MATERIAL', 'OPTIONAL', r'graphite|lonsdaleite', 'Context', 'INLINE_ANSWER')
C(T, 'Uses of diamonds and general facts', 'SUPPORTING_CONCEPT_GAP', 'OTHER', 'OPTIONAL', r'\buses?\b|fact', 'Curiosity', 'FAQ')

# --- COM-ER-SIDESTONE category
T = 'COM-ER-SIDESTONE'
C(T, 'What a side-stone engagement ring is / what side stones are called', 'DEFINITION_GAP', 'STYLE', 'CORE', r'what (is|are)|called|side (stone|diamond)',
  'Understand the style before browsing', 'CATEGORY_COPY', xkey='SIDE_STONE_CATEGORY', stage='DISCOVER')
C(T, 'Side-stone styles (three-stone, baguette/tapered, pavé, halo)', 'ATTRIBUTE_GAP', 'STYLE', 'SUPPORT', r'three[- ]stone|trilogy|baguette|tapered|pav|halo',
  'Browse by sub-style', 'CATEGORY_COPY', stage='COMPARE')
C(T, 'Considerations: centre shape, metal, total carat weight', 'ATTRIBUTE_GAP', 'STYLE', 'SUPPORT', r'\bshape|metal|gold|carat|proportion|\boval\b|\bround\b|emerald',
  'Filter by what matters', 'CATEGORY_COPY', stage='EVALUATE')
C(T, 'Benefits of side stones', 'QUESTION_GAP', 'STYLE', 'SUPPORT', r'benefit', 'Know why to choose side stones', 'CATEGORY_COPY')
C(T, 'Adding side stones / ring enhancer / bespoke', 'COMMERCIAL_CONTEXT_GAP', 'COMMERCIAL', 'BIZ', r'\badd\b|enhancer', 'Customise an existing ring',
  'BUSINESS_INPUT_REQUIRED', owner='COM-BESPOKE', biz='Whether HOD adds side stones / offers enhancers or bespoke (Stage 17 business dependency)', stage='BUY')
C(T, 'Assortment depth for the category (about 4 products; template meta)', 'COMMERCIAL_CONTEXT_GAP', 'COMMERCIAL', 'BIZ', None, 'Enough choice to browse',
  'BUSINESS_INPUT_REQUIRED', biz='Product count and variants in the side-stone category (catalogue)', stage='BUY',
  extra=('Stage 10/17: thin category (template meta, about 4 products)', 1))
C(T, 'Natural or lab-grown centre stone', 'COMMERCIAL_CONTEXT_GAP', 'ORIGIN', 'OPTIONAL', r'\blab\b|natural', 'Choose stone origin', 'BRIEF_MENTION_AND_LINK',
  owner='EDU-LG-02', anchor='lab grown vs natural diamonds', xkey='LG_VS_NATURAL')
C(T, 'Setting types explained', 'INTERNAL_CONTEXT_GAP', 'SETTING', 'OPTIONAL', r'setting', 'Learn settings', 'BRIEF_MENTION_AND_LINK', owner='EDU-RJG-01', anchor='types of diamond settings', xkey='SETTING_TYPES')

# --- COM-PDP-OVAL-FLORAL
T = 'COM-PDP-OVAL-FLORAL'
C(T, 'Design description: oval centre with marquise side stones', 'ATTRIBUTE_GAP', 'STYLE', 'SUPPORT', r'marquise|\boval\b', 'Recognise the design searched for', 'CATEGORY_COPY', xkey='OVAL_MARQUISE_PDP', stage='EVALUATE',
  note='PRODUCT SERP aligned; no content gap evidenced beyond product facts.')
C(T, 'Product specifications (stone origin, carat, metal options, certificate)', 'COMMERCIAL_CONTEXT_GAP', 'COMMERCIAL', 'BIZ', r'real diamond|gold|carat',
  'Verify what is being bought', 'BUSINESS_INPUT_REQUIRED', biz='Product facts (origin, carat, metal, report) from the catalogue', stage='BUY')
C(T, 'Marquise vs oval price question', 'QUESTION_GAP', 'PRICE', 'OPTIONAL', r'expensive', 'Price curiosity', 'BRIEF_MENTION_AND_LINK', owner='EDU-SHP-00', anchor='diamond shape', xkey='SHAPES_OVERVIEW')

# head-term insufficient-evidence rows and unvalidated-format rows
for t, terms in HEAD.items():
    C(t, 'Core head-term demand and SERP unmeasured: ' + '; '.join(terms), 'SERP_FORMAT_GAP', 'DATA_GAP', 'HEAD', None,
      'The most natural query for this page has no Stage 7 row or Stage 8 SERP', 'VALIDATE_BEFORE_USE',
      extra=('Stage 17 gap register / summary finding 1 (missing head terms)', 1), note='No volume is assumed or recorded.')
for t in TARGETS:
    if not any(SERP_TARGET.get(k) == t for k in SERP_TARGET):
        C(t, 'Page format and section order unvalidated (no Stage 8 SERP for owned keywords)', 'SERP_FORMAT_GAP', 'DATA_GAP', 'HEAD', None,
          'Structure must be inferred from keywords and adjacent SERPs only', 'VALIDATE_BEFORE_USE', extra=('Stage 17 serp_confidence INSUFFICIENT_EVIDENCE', 1), note=NO_SERP_NOTE)


# ---------------------------------------------------------------- evidence engine
def m(rx, s):
    return bool(re.search(rx, s.lower())) if rx else False


S17C = collections.defaultdict(list)
for r in C17:
    S17C[r['target_page_id']].append(r['concept'])
S17G = collections.defaultdict(list)
for r in G17:
    S17G[r['target_page_id']].append(r['gap_description'])


def evidence(t, rx):
    own = OWN_SERPS.get(t, [])
    e = dict(kw=sum(m(rx, k) for k in OWNED_KW.get(t, [])),
             aio=sum(m(rx, SERP[k]['aio']) for k in own),
             org=sum(any(m(rx, o) for o in SERP[k]['org']) for k in own),
             serp=sum(m(rx, SERP[k]['aio']) or any(m(rx, o) for o in SERP[k]['org']) for k in own),
             paa=sum(m(rx, q) for q in ROUTED_PAA.get(t, [])),
             rel=len({r for k in own for r in SERP[k]['rel'] if m(rx, r)}),
             adj=sum(m(rx, SERP[k]['aio']) for u in linked(t) for k in OWN_SERPS.get(u, [])),
             s17=any(m(rx, c) for c in S17C.get(t, [])))
    return e


def strength(e):
    if e['serp'] >= 2 or (e['serp'] >= 1 and e['paa'] + e['rel'] >= 1) or e['paa'] >= 3:
        return 'STRONG'
    if e['serp'] >= 1 or e['paa'] >= 1 or e['rel'] >= 2 or e['kw'] >= 3:
        return 'MODERATE'
    return 'WEAK'


def evidence_text(t, e, extra):
    n = len(OWN_SERPS.get(t, []))
    parts = []
    if e['aio']: parts.append(f'Stage 8 AI Overview text {e["aio"]}/{n} SERPs')
    if e['org']: parts.append(f'Stage 8 organic titles/snippets {e["org"]}/{n} SERPs')
    if e['paa']: parts.append(f'Stage 8 PAA routed by Stage 17 ({e["paa"]})')
    if e['rel']: parts.append(f'Stage 8 related searches ({e["rel"]})')
    if e['kw']: parts.append(f'Stage 15 owned keywords ({e["kw"]})')
    if e['s17']: parts.append('Stage 17 semantic concept')
    if e['adj']: parts.append(f'Adjacent Stage 16-linked target SERPs, AI Overview ({e["adj"]})')
    if extra: parts.append(extra[0])
    return '; '.join(parts)


SEV_REL = {'CRITICAL_COVERAGE': 'REQUIRED_IN_BRIEF', 'IMPORTANT_COVERAGE': 'STRONGLY_RECOMMENDED_IN_BRIEF',
           'SUPPORTING_COVERAGE': 'RECOMMENDED_IN_BRIEF', 'OPTIONAL_CONTEXT': 'OPTIONAL_IN_BRIEF',
           'BUSINESS_DEPENDENT': 'HOLD_FOR_BUSINESS_INPUT', 'INSUFFICIENT_EVIDENCE': 'HOLD_FOR_EVIDENCE'}


def severity(c, e, st, owner_status):
    if c['role'] == 'BIZ':
        return 'BUSINESS_DEPENDENT'
    if c['role'] == 'HEAD':
        return 'INSUFFICIENT_EVIDENCE'
    if c['role'] in ('OPTIONAL', 'AVOID'):
        return 'OPTIONAL_CONTEXT'
    if c['role'] == 'CORE':
        s = 'CRITICAL_COVERAGE' if st in ('STRONG', 'MODERATE') else 'IMPORTANT_COVERAGE'
    else:
        s = {'STRONG': 'IMPORTANT_COVERAGE', 'MODERATE': 'SUPPORTING_COVERAGE'}.get(st)
        if not s:
            s = 'SUPPORTING_COVERAGE' if e['kw'] + e['paa'] + e['rel'] or c['extra'] else 'OPTIONAL_CONTEXT'
    if owner_status in ('OWNED_ELSEWHERE', 'CONDITIONAL_OWNER_NOT_BUILT', 'COMMERCIAL_PAGE_OWNER') and s == 'CRITICAL_COVERAGE':
        s = 'IMPORTANT_COVERAGE'
    return s


def owner_status_of(c):
    o = c['owner']
    if not o or o == c['t']:
        return 'OWNED_HERE'
    if o in REG15:
        return 'OWNED_ELSEWHERE'
    if o in ARCH14:
        if c['anchor'] and BYKW.get(c['anchor'], {}).get('mapping_disposition') == 'MAP_INTERIM_HOME' \
                and BYKW[c['anchor']]['target_id'] == c['t']:
            return 'INTERIM_HOME_HERE'
        return 'CONDITIONAL_OWNER_NOT_BUILT'
    return 'COMMERCIAL_PAGE_OWNER'


def coverage(t, rx):
    txt = existing_text(t)
    if txt is None:
        return 'FUTURE_PAGE', 'No page exists (Stage 15 proposed). BODY_COVERAGE=N/A'
    url = REG15[t]['existing_url']
    if rx and m(rx, txt):
        return 'BODY_UNKNOWN', f'Existing {url}: concept evident in title/H1; BODY_COVERAGE=UNKNOWN (no body audit)'
    return 'TITLE/H1_NOT_EVIDENT', f'Existing {url}: not evident in title/H1; BODY_COVERAGE=UNKNOWN (no body audit)'


GAPS, DROPPED = [], []
for c in LEX:
    t = c['t']
    e = evidence(t, c['rx'])
    extra = c['extra']
    if c['xkey'] == '' and c['concept'].startswith('Hub routing'):
        pass
    if extra and extra[1] is None:   # Stage 16 link count
        n16 = sum(1 for r in rd('architecture/16_internal_link_map.csv') if r['source_page_id'] == t)
        extra = (f'{extra[0]} ({n16} outgoing relationships)', n16)
    total = e['kw'] + e['serp'] + e['paa'] + e['rel'] + e['adj'] + int(e['s17']) + (extra[1] if extra else 0)
    if total == 0:
        DROPPED.append((t, c['concept']))
        continue
    st = strength(e)
    if c['role'] == 'HEAD':
        st = 'WEAK'
    if not OWN_SERPS.get(t) and st == 'STRONG':
        st = 'MODERATE'
    os_ = owner_status_of(c)
    sev = severity(c, e, st, os_)
    conf = {'STRONG': 'HIGH', 'MODERATE': 'MEDIUM', 'WEAK': 'LOW'}[st]
    if conf == 'HIGH' and not OWN_SERPS.get(t):
        conf = 'MEDIUM'
    if c['role'] == 'HEAD':
        conf = 'LOW'
    cov, cov_txt = coverage(t, c['rx'])
    rel19 = SEV_REL[sev]
    if os_ in ('OWNED_ELSEWHERE', 'CONDITIONAL_OWNER_NOT_BUILT', 'COMMERCIAL_PAGE_OWNER') and sev not in ('BUSINESS_DEPENDENT', 'INSUFFICIENT_EVIDENCE'):
        rel19 = 'LINK_AND_BRIEF_MENTION' if c['treat'] != 'AVOID' else rel19
    if c['treat'] == 'AVOID':
        rel19 = 'EXCLUDE_FROM_BRIEF'
    notes = []
    if c['note']: notes.append(c['note'])
    if c['anchor']:
        a = BYKW[c['anchor']]
        notes.append(f'Stage 15 check: "{c["anchor"]}" -> {a["target_id"] or "no target"} ({a["mapping_disposition"]}; Stage 14 topic {a["stage14_topic_id"] or "-"})')
    if c['xkey']: notes.append(f'[xkey:{c["xkey"]}]')
    notes.append(f'Journey stage: {c["stage"]}')
    ev_text = evidence_text(t, e, extra)
    cnt = e['kw'] + e['serp'] + e['paa'] + e['rel'] + (extra[1] if extra else 0)
    GAPS.append(dict(target_page_id=t, cluster_id=REG15[t]['cluster_ids'], gap_type=c['gap_type'], concept=c['concept'],
                     concept_type=c['ctype'], source_evidence=ev_text, evidence_count=cnt, evidence_strength=st,
                     searcher_need=c['need'], current_coverage=cov_txt, coverage_status=cov, gap_severity=sev,
                     owner_status=os_, owner_page_id=c['owner'] or t, recommended_treatment=c['treat'],
                     stage19_relevance=rel19, business_dependency=c['biz'], confidence=conf, notes=' | '.join(notes),
                     _xkey=c['xkey'], _anchor=c['anchor'], _rx=c['rx'], _stage=c['stage'], _e=e))
for i, g in enumerate(GAPS, 1):
    g['gap_id'] = f'G18-{i:04d}'

GAP_COLS = ['target_page_id', 'cluster_id', 'gap_id', 'gap_type', 'concept', 'concept_type', 'source_evidence', 'evidence_count',
            'evidence_strength', 'searcher_need', 'current_coverage', 'coverage_status', 'gap_severity', 'owner_status', 'owner_page_id',
            'recommended_treatment', 'stage19_relevance', 'business_dependency', 'confidence', 'notes']
wr('18_semantic_gap_register.csv', GAP_COLS, GAPS)

# ---------------------------------------------------------------- cross-page ownership
CP_TREAT = {'OWNED_ELSEWHERE': ('Answer only the aspect relevant to this page in 1-3 sentences; link to the owner.',
                                'Do not build a full section, table or FAQ set that duplicates the owner; do not target the owner\'s keywords in headings.'),
            'INTERIM_HOME_HERE': ('Cover as a section here until the conditional topic is approved; keep it self-contained so it can move.',
                                  'Do not create a separate URL; do not expand beyond the interim keywords Stage 15 assigned.'),
            'CONDITIONAL_OWNER_NOT_BUILT': ('Mention briefly only if the searcher need requires it; no link until the conditional page exists.',
                                            'Do not pre-build the conditional topic inside this page.'),
            'COMMERCIAL_PAGE_OWNER': ('Link or hand off to the commercial/support page once business facts are confirmed.',
                                      'Do not add product claims, prices or policies to Education content.')}
CP = []
for g in GAPS:
    if g['owner_status'] == 'OWNED_HERE':
        continue
    cur, avoid = CP_TREAT[g['owner_status']]
    if g['recommended_treatment'] == 'INLINE_ANSWER' and g['owner_status'] == 'OWNED_ELSEWHERE':
        cur = 'Give a one-line direct answer in context; link to the owner for depth.'
    ev = f'{g["gap_id"]}: {g["source_evidence"]}'
    if g['_anchor']:
        a = BYKW[g['_anchor']]
        ev = f'Stage 15: "{g["_anchor"]}" -> {a["target_id"] or "-"} / {a["mapping_disposition"]} / Stage 14 {a["stage14_topic_id"] or "-"}. ' + ev
    CP.append(dict(concept=g['concept'], current_target_page_id=g['target_page_id'], actual_owner_page_id=g['owner_page_id'],
                   relationship=g['owner_status'], current_page_treatment=cur, avoid_treatment=avoid, evidence=ev,
                   confidence=g['confidence'], notes=(f'[xkey:{g["_xkey"]}] ' if g['_xkey'] else '') + f'Gap severity at this page: {g["gap_severity"]}'))
wr('18_cross_page_semantic_ownership.csv', ['concept', 'current_target_page_id', 'actual_owner_page_id', 'relationship',
                                            'current_page_treatment', 'avoid_treatment', 'evidence', 'confidence', 'notes'], CP)

# ---------------------------------------------------------------- entities
E = []


def EN(name, etype, rx, owner=None):
    E.append(dict(name=name, etype=etype, rx=rx, owner=owner))


for n, rx, o in [('CVD (chemical vapour deposition)', r'\bcvd\b|chemical vapou?r', 'EDU-LG-03'), ('HPHT (high pressure, high temperature)', r'\bhpht\b|high pressure', 'EDU-LG-03'),
                 ('Post-growth treatment', r'treat(ed|ment)|anneal|irradiat', 'EDU-LG-08'), ('Kimberlite', r'kimberlite', 'EDU-NAT-00'),
                 ('Mining', r'\bmin(ed|ing)\b', 'EDU-NAT-00'), ('Laser inscription', r'inscri', 'EDU-CERT-00'),
                 ('Spectroscopy / lab screening', r'spectro|screener|id100', 'EDU-LG-09'), ('Thermal / electrical diamond tester', r'thermal|tester', 'EDU-LG-09'),
                 ('Rhodium plating', r'rhodium', 'EDU-MET-02')]:
    EN(n, 'PROCESS_ENTITY', rx, o)
for n, rx, o in [('Carbon', r'\bcarbon\b', 'EDU-GEN-01'), ('Graphite', r'graphite', 'EDU-GEN-01'), ('Lonsdaleite', r'lonsdaleite', 'EDU-GEN-01'),
                 ('Type IIa', r'\biia\b|type ii', 'EDU-GEN-01'), ('10k gold', r'\b10 ?k\b|10 karat|10-karat', 'EDU-MET-01'), ('14k gold', r'\b14 ?k\b', 'EDU-MET-01'),
                 ('18k gold', r'\b18 ?k\b', 'EDU-MET-01'), ('22k / 24k gold', r'\b2[24] ?k\b', 'EDU-MET-01'), ('Yellow gold', r'yellow gold', 'EDU-MET-00'),
                 ('White gold', r'white gold', 'EDU-MET-00'), ('Rose gold', r'rose gold', 'EDU-MET-00'), ('Platinum', r'platinum', 'EDU-MET-00'),
                 ('Sterling silver (925)', r'sterling|\b925\b|\bsilver\b', 'EDU-MET-00'), ('Tungsten', r'tungsten', 'EDU-MET-00'),
                 ('Titanium', r'titanium', 'EDU-MET-00'), ('Stainless steel', r'stainless', 'EDU-MET-00'), ('Nickel (allergen)', r'nickel', 'EDU-MET-00')]:
    EN(n, 'MATERIAL_ENTITY', rx, o)
for n, rx, o in [('Natural (mined) diamond', r'natural|mined', 'EDU-LG-02'), ('Lab-grown diamond', r'lab[- ]?(grown|created|made)|lab diamond|synthetic', 'EDU-LG-00'),
                 ('Moissanite', r'moissanite', 'EDU-GEM-01'), ('Cubic zirconia', r'cubic zirconia|\bcz\b', 'EDU-GEM-00'),
                 ('Simulant', r'simulant|simulated', 'EDU-GEM-00')]:
    EN(n, 'COMPARISON_ENTITY', rx, o)
for n, rx in [('GIA', r'\bgia\b'), ('IGI', r'\bigi\b'), ('GCAL', r'gcal'), ('AGS', r'\bags\b|american gem society'), ('EGL', r'\begl\b'), ('GSI', r'\bgsi\b'),
              ('Grading report / certificate', r'grading report|certificate|\breport\b'), ('FTC', r'\bftc\b')]:
    EN(n, 'CERTIFICATION_ENTITY', rx, 'EDU-LG-00' if n == 'FTC' else 'EDU-CERT-00')
for n, rx, o in [('The 4Cs', r'4 ?cs\b|four cs|4 c\'s', 'EDU-4C-00'), ('Cut grade scale (Excellent/Ideal to Poor)', r'excellent|ideal cut|\bideal\b|cut grade', 'EDU-4C-06'),
                 ('Colour grades D-Z', r'd[- ]to[- ]z|colou?rless|near[- ]colou?rless|\bg[- ]?h\b', 'EDU-4C-05'),
                 ('FL / IF (flawless)', r'flawless|\bif\b|\bfl\b', 'EDU-4C-03'), ('VVS1 / VVS2', r'vvs', 'EDU-4C-03'),
                 ('VS1 / VS2', r'\bvs ?[12]\b|vs clarity|very slightly included', 'EDU-4C-04'), ('SI1 / SI2 / SI3', r'\bsi ?[123]\b|slightly included', 'EDU-4C-02'),
                 ('I1 / I2 / I3', r'\bi[123]\b', 'EDU-4C-01'), ('Inclusions and blemishes', r'inclusion|blemish', 'EDU-4C-01'),
                 ('Eye-clean', r'eye[- ]clean', 'EDU-4C-01'), ('Fluorescence', r'fluoresc', None),
                 ('Brilliance / fire / scintillation', r'brillian|\bfire\b|scintillat|brightness', 'EDU-4C-06'),
                 ('Polish and symmetry', r'polish|symmetr', 'EDU-4C-06'), ('Facets', r'facet', 'EDU-4C-06'),
                 ('Carat weight', r'carat|\bct\b', 'EDU-4C-07'), ('Total carat weight (ctw)', r'total carat|ctw', 'EDU-4C-07'),
                 ('Mohs hardness scale', r'mohs|hardness', 'EDU-GEN-01'), ('Karat (gold purity)', r'karat', 'EDU-MET-01'),
                 ('US ring size', r'ring size', 'EDU-RJG-02'), ('Ring sizer', r'sizer', 'EDU-RJG-05')]:
    EN(n, 'SUPPORTING_ENTITY', rx, o)
for n, rx in [('Round brilliant', r'\bround\b'), ('Oval', r'\boval\b'), ('Princess', r'princess'), ('Cushion', r'cushion'), ('Emerald cut', r'emerald'),
              ('Pear', r'\bpear\b'), ('Marquise', r'marquise'), ('Radiant', r'radiant'), ('Asscher', r'asscher'), ('Heart', r'\bheart\b')]:
    EN(n + ' shape', 'SUPPORTING_ENTITY', rx, 'EDU-SHP-00')
for n, rx in [('Prong setting', r'prong'), ('Bezel setting', r'bezel'), ('Pavé setting', r'pav[eé]'), ('Halo setting', r'\bhalo\b'), ('Channel setting', r'channel'),
              ('Tension setting', r'tension'), ('Three-stone / trilogy', r'three[- ]stone|trilogy'), ('Solitaire', r'solitaire'), ('Milgrain', r'milgrain'),
              ('Baguette side stones', r'baguette')]:
    EN(n, 'PRODUCT_ENTITY', rx, 'EDU-RJG-01')
EN('Side stones (accent stones)', 'PRODUCT_ENTITY', r'side stone|side diamond|accent stone', 'COM-ER-SIDESTONE')

PRIMARY_ENT = {
    'EDU-LG-00': ['Lab-grown diamond'], 'EDU-LG-01': ['Lab-grown diamond'], 'EDU-LG-02': ['Lab-grown diamond', 'Natural (mined) diamond'],
    'EDU-LG-03': ['CVD (chemical vapour deposition)', 'HPHT (high pressure, high temperature)'], 'EDU-LG-05': ['Lab-grown diamond'],
    'EDU-LG-07': ['Lab-grown diamond'], 'EDU-LG-08': ['Fluorescence', 'Lab-grown diamond'], 'EDU-LG-09': ['Thermal / electrical diamond tester'],
    'EDU-LG-10': ['Lab-grown diamond', 'The 4Cs'], 'EDU-NAT-00': ['Natural (mined) diamond', 'Kimberlite'], 'EDU-4C-00': ['The 4Cs'],
    'EDU-4C-01': ['Inclusions and blemishes', 'FL / IF (flawless)', 'VVS1 / VVS2', 'VS1 / VS2', 'SI1 / SI2 / SI3', 'I1 / I2 / I3'],
    'EDU-4C-02': ['SI1 / SI2 / SI3'], 'EDU-4C-03': ['VVS1 / VVS2', 'FL / IF (flawless)'], 'EDU-4C-05': ['Colour grades D-Z'],
    'EDU-4C-06': ['Cut grade scale (Excellent/Ideal to Poor)'], 'EDU-4C-07': ['Carat weight'], 'EDU-SHP-00': [],
    'EDU-CERT-00': ['Grading report / certificate', 'GIA', 'IGI'], 'EDU-CERT-01': ['GIA', 'IGI'],
    'EDU-MET-00': ['Platinum', 'White gold', 'Yellow gold'], 'EDU-MET-01': ['14k gold', '18k gold', '10k gold', 'Karat (gold purity)'],
    'EDU-RJG-01': ['Prong setting', 'Bezel setting', 'Halo setting', 'Pavé setting'], 'EDU-RJG-02': ['US ring size'],
    'EDU-GEN-01': ['Carbon', 'Mohs hardness scale'], 'COM-ER-SIDESTONE': ['Side stones (accent stones)'], 'COM-PDP-OVAL-FLORAL': ['Oval shape', 'Marquise shape'],
}
ENT = []
for t in TARGETS:
    for en in E:
        e = evidence(t, en['rx'])
        own = e['aio'] + e['org'] + e['paa'] + e['rel']
        prim = en['name'] in PRIMARY_ENT.get(t, [])
        if own + e['kw'] == 0 and not prim:
            continue
        if not prim and own == 0 and e['kw'] < 2:
            continue           # single stray keyword mention is not enough for a non-primary entity
        if prim and own + e['kw'] + e['adj'] == 0:
            continue
        owner = en['owner'] or t
        if prim:
            role, etype = 'REQUIRED', 'PRIMARY_ENTITY'
        else:
            etype = en['etype']
            role = 'SUPPORTING' if (e['aio'] >= 1 and own >= 2) or e['paa'] >= 2 or own >= 3 else 'MENTION_IF_RELEVANT'
        if owner != t and not prim:
            role = 'MENTION_IF_RELEVANT' if role == 'MENTION_IF_RELEVANT' else 'SUPPORTING'
        cov, _ = coverage(t, en['rx'])
        if owner != t and not prim:
            cov_status = 'OWNED_ELSEWHERE'
        else:
            cov_status = cov
        st = strength(e)
        conf = {'STRONG': 'HIGH', 'MODERATE': 'MEDIUM', 'WEAK': 'LOW'}[st]
        if conf == 'HIGH' and not OWN_SERPS.get(t):
            conf = 'MEDIUM'
        is_gap = role in ('REQUIRED', 'SUPPORTING') and cov_status in ('FUTURE_PAGE', 'TITLE/H1_NOT_EVIDENT')
        ENT.append(dict(target_page_id=t, entity=en['name'], entity_type=etype, evidence_source=evidence_text(t, e, None) or 'Primary entity of the target (Stage 15/17)',
                        evidence_count=own + e['kw'], coverage_status=cov_status, owner_page_id=owner, required_or_supporting=role,
                        confidence=conf, notes=('ENTITY_GAP' if is_gap else 'not a gap') + ('' if owner == t else f'; depth owned by {owner}')))
wr('18_entity_coverage.csv', ['target_page_id', 'entity', 'entity_type', 'evidence_source', 'evidence_count', 'coverage_status', 'owner_page_id',
                              'required_or_supporting', 'confidence', 'notes'], ENT)

# ---------------------------------------------------------------- questions
QTREAT = {'CORE_ANSWER': 'CORE_SECTION', 'SECTION_QUESTION': 'SUPPORTING_SECTION', 'FAQ_CANDIDATE': 'FAQ',
          'CATEGORY_COPY_CANDIDATE': 'CATEGORY_COPY', 'EXCLUDE_OFF_TOPIC': 'NOT_NEEDED'}
Q_OVERRIDE = {  # evidence-based adjustments of Stage 17 roles (reason in notes)
    'Are lab diamonds as good as real diamonds?': ('INLINE_ANSWER', 'Answered in one line inside the similarities section.'),
    'Is a lab-grown diamond really a diamond?': ('INLINE_ANSWER', 'Same need as the core authenticity answer; one-line restatement, not a new section.'),
    'Is a lab diamond a real diamond?': ('INLINE_ANSWER', 'Near-duplicate of the core authenticity answer.'),
    'What does VVS mean in a diamond?': ('CORE_SECTION', 'Definition is the page\'s primary need.'),
    'Can I add side stones to an engagement ring?': ('NOT_NEEDED', 'Service question; BUSINESS_DEPENDENT (bespoke/enhancer offer unknown). Held until HOD confirms.'),
    'Is diamond color grade GH good?': ('CORE_SECTION', 'Stage 17 CORE_ANSWER retained.'),
}
INTERIM_GROUP = [(r'VS1 / VS2', 'EDU-4C-04'), (r'Rhodium', 'EDU-MET-02'), (r'Pros and cons|Worth it', 'EDU-LG-06')]
STOP = set('what which is are the a an of to do does can in for or and how why when will diamond diamonds you your it be'.split())


def q_cov(t, q):
    txt = existing_text(t)
    if txt is None:
        return 'FUTURE_PAGE'
    words = [w for w in re.findall(r'[a-z0-9]+', q.lower()) if w not in STOP and len(w) > 2]
    hit = sum(1 for w in words if w in txt)
    return 'BODY_UNKNOWN' if words and hit / len(words) >= 0.6 else 'TITLE/H1_NOT_EVIDENT'


QROWS = []
for q in Q17:
    t = q['target_page_id']
    treat = QTREAT[q['recommended_role']]
    note = []
    if q['question'] in Q_OVERRIDE:
        treat, why = Q_OVERRIDE[q['question']]
        note.append('Override of Stage 17 role: ' + why)
    owner = t
    if not t.startswith('NO_TARGET'):
        for rx, o in INTERIM_GROUP:
            if re.search(rx, q['need_group']) and t in ('EDU-4C-01', 'EDU-MET-00', 'EDU-LG-02'):
                owner = o
        if q['source_type'] == 'STAGE15_KEYWORD':
            a = BYKW.get(q['source_keyword'], {})
            if a.get('mapping_disposition') == 'MAP_INTERIM_HOME' and a.get('stage14_topic_id'):
                owner = a['stage14_topic_id']
    if owner != t:
        note.append(f'Interim home here; conditional owner {owner} (Stage 14/15).')
    src = (f'STAGE8_PAA (SERP: "{q["source_keyword"]}")' if q['source_type'] == 'STAGE8_PAA'
           else f'STAGE15_KEYWORD ({q["variant_count"]} variant(s); lead "{q["source_keyword"]}")')
    cov = 'NOT_APPLICABLE' if treat == 'NOT_NEEDED' else q_cov(t, q['question'])
    conf = q['confidence']
    if q['source_type'] == 'STAGE8_PAA' and q['surfaced_on_target']:
        note.append(f'Surfaced on: {q["surfaced_on_target"]}')
    QROWS.append(dict(target_page_id=t, question=q['question'], question_type=q['question_type'], source=src, coverage_status=cov,
                      recommended_treatment=treat, owner_page_id=owner, confidence=conf,
                      notes=' | '.join(note + [f'Stage 17 need group: {q["need_group"]}; Stage 17 role: {q["recommended_role"]}'])))
    # cross rows: PAA surfaced on another Stage 15 target's SERP than its owner
    if q['source_type'] == 'STAGE8_PAA' and treat != 'NOT_NEEDED':
        for s in [x.strip() for x in q['surfaced_on_target'].split(';')]:
            if s in REG15 and s != t:
                QROWS.append(dict(target_page_id=s, question=q['question'], question_type=q['question_type'], source=src,
                                  coverage_status='OWNED_ELSEWHERE', recommended_treatment='INLINE_ANSWER', owner_page_id=t, confidence=conf,
                                  notes=f'PAA appeared on this page\'s SERP but Stage 17 routed it to {t}. One-line answer in context + link; no FAQ duplicate.'))
wr('18_question_coverage.csv', ['target_page_id', 'question', 'question_type', 'source', 'coverage_status', 'recommended_treatment',
                                'owner_page_id', 'confidence', 'notes'], QROWS)

# ---------------------------------------------------------------- related searches
REL_ROWS = collections.OrderedDict()
for kw, t in SERP_TARGET.items():
    for r in SERP[kw]['rel']:
        REL_ROWS.setdefault(r, dict(serps=[], targets=set()))
        REL_ROWS[r]['serps'].append(kw)
        REL_ROWS[r]['targets'].add(t)
QW = re.compile(r'^(what|whats|how|why|when|where|which|who|is|are|do|does|can|will|should)\b')
REL_OVERRIDE = {
    'diamond shape pictures': 'AMBIGUOUS', 'diamond shape ring': 'BUSINESS_DEPENDENT', 'diamond shape jewelry': 'BUSINESS_DEPENDENT',
    'cvd diamond full form': 'NEW_SEMANTIC_CONCEPT', 'hpht vs cvd vs iia': 'NEW_SEMANTIC_CONCEPT', 'cvd hpht': 'CLOSE_VARIANT', 'hpht diamond': 'CLOSE_VARIANT',
    'igi diamond': 'NEW_SEMANTIC_CONCEPT', 'igi natural diamond': 'NEW_SEMANTIC_CONCEPT', 'marquise diamond': 'NEW_SEMANTIC_CONCEPT',
    'lab grown diamonds': 'BUSINESS_DEPENDENT', 'if lab grown diamond': 'NEW_ATTRIBUTE', 'types of diamond cuts brilliant': 'NEW_SEMANTIC_CONCEPT',
    'how many cuts in diamond': 'NEW_QUESTION', 'side stone ring enhancer': 'BUSINESS_DEPENDENT', 'diamond color chart': 'NEW_SEMANTIC_CONCEPT',
    'rhodium ring meaning': 'NEW_QUESTION', 'solid rhodium ring': 'NEW_SEMANTIC_CONCEPT', 'black rhodium ring': 'NEW_ATTRIBUTE',
    'types of diamond settings for engagement rings': 'NEW_MODIFIER', 'types of ring settings and mountings': 'NEW_SEMANTIC_CONCEPT',
    'diamond setting types for necklace': 'NEW_MODIFIER', 'how to buy a lab grown diamond': 'CLOSE_VARIANT',
    'best diamond cut for sparkle': 'NEW_SEMANTIC_CONCEPT', 'color g diamond good or bad': 'NEW_QUESTION', 'gh color diamond': 'CLOSE_VARIANT',
    'gh diamond quality': 'CLOSE_VARIANT', 'g-h si diamond quality': 'NEW_SEMANTIC_CONCEPT', 'g si2 diamond': 'NEW_SEMANTIC_CONCEPT',
    'round diamond cut grade': 'NEW_ATTRIBUTE', 'si2 i1 diamond clarity': 'NEW_SEMANTIC_CONCEPT', 'vvs diamonds real': 'NEW_QUESTION',
    'oval diamond with marquise halo': 'BUSINESS_DEPENDENT', 'tungsten ring pros and cons': 'BUSINESS_DEPENDENT',
}


def classify_rel(s, serps, t):
    sl = s.lower()
    if sl in {k.lower() for k in S7}:
        return 'DUPLICATE', 'Already in the Stage 7 universe; no new evidence.'
    if sl in REL_OVERRIDE:
        return REL_OVERRIDE[sl], 'Manual classification.'
    if t == 'EDU-SHP-00' and re.search(r'face|drawing|meaning|name|colour|color', sl):
        return 'IRRELEVANT', 'Geometric/non-jewellery sense of "diamond shape".'
    if re.search(r'astrolog|bad luck|health benefit|benefits of wearing', sl):
        return 'IRRELEVANT', 'Belief/astrology claim; not trust-safe for HOD.'
    if t == 'EDU-LG-09' and re.search(r'amazon|for sale|near me|price|cost|best|professional|machine', sl):
        return 'IRRELEVANT', 'Tester-device shopping; not HOD business (Stage 12 D-16).'
    if re.search(r'reddit', sl):
        return 'NEW_MODIFIER', 'Forum modifier: discussion/experience demand.'
    if re.search(r'\b20[12]\d\b', sl):
        return 'CLOSE_VARIANT', 'Dated variant of the SERP query.'
    if re.search(r'pawn|per gram', sl):
        return 'NEW_ATTRIBUTE', 'Scrap/melt value attribute (PRICE/RESALE).'
    if re.search(r'for sale|near me|\bbuy\b|amazon', sl):
        return 'BUSINESS_DEPENDENT', 'Transactional modifier; depends on HOD catalogue.'
    if QW.match(sl):
        if any(sl.startswith(k.lower()) for k in serps):
            return 'NEW_MODIFIER', 'Question SERP query extended with a use-case modifier.'
        return 'NEW_QUESTION', 'Question not in Stage 7.'
    if re.search(r'price|cost|value|worth|expensive|cheap', sl):
        return 'NEW_ATTRIBUTE', 'PRICE/VALUE attribute.'
    if re.search(r'chart|scale|pictures|pdf|side by side|before and after', sl):
        return 'NEW_SEMANTIC_CONCEPT', 'Visual/reference format signal (chart, pictures, side-by-side).'
    if re.search(r'\bvs\b|versus', sl):
        return 'NEW_SEMANTIC_CONCEPT', 'Additional comparison entity or dimension.'
    if re.search(r'\bring\b|rings\b|earrings|chain|necklace|jewelry|women|\bmen\b|mens|men\'s|gold\b', sl):
        return 'BUSINESS_DEPENDENT', 'Product/jewellery modifier; relevance depends on HOD catalogue.'
    if any(sl.startswith(k.lower()) for k in serps):
        return 'NEW_MODIFIER', 'SERP query extended with a modifier.'
    if re.search(r'process|pros and cons|gia|igi|lab grown|natural|meaning|machine', sl):
        return 'NEW_SEMANTIC_CONCEPT', 'Adds a concept/entity to the SERP topic.'
    return 'AMBIGUOUS', 'Intent unclear from the string alone.'


RELC, seen_lower = [], {}
GAP_BY_T = collections.defaultdict(list)
for g in GAPS:
    GAP_BY_T[g['target_page_id']].append(g)
for s, v in REL_ROWS.items():
    t = sorted(v['targets'])[0]
    cls, why = classify_rel(s, v['serps'], t)
    if s.lower() in seen_lower and cls != 'DUPLICATE':
        cls, why = 'DUPLICATE', f'Case variant of "{seen_lower[s.lower()]}".'
    seen_lower.setdefault(s.lower(), s)
    feeds = [g['gap_id'] for tt in v['targets'] for g in GAP_BY_T[tt] if g['_rx'] and m(g['_rx'], s)][:6]
    RELC.append(dict(related_search=s, occurrences=len(v['serps']), serp_keywords='; '.join(sorted(set(v['serps']))),
                     serp_target_page_id='; '.join(sorted(v['targets'])), in_stage7='YES' if s.lower() in {k.lower() for k in S7} else 'NO',
                     classification=cls, feeds_gap_ids='; '.join(feeds), ownership_effect='NONE (evidence only; Stage 15 ownership unchanged)', notes=why))
wr('18_related_search_classification.csv', ['related_search', 'occurrences', 'serp_keywords', 'serp_target_page_id', 'in_stage7', 'classification',
                                             'feeds_gap_ids', 'ownership_effect', 'notes'], RELC)

# ---------------------------------------------------------------- SERP patterns
ATTR = [('QUALITY', r'quality|grade'), ('CLARITY', r'clarity|inclusion'), ('COLOUR', r'colou?r'), ('CUT', r'\bcut\b|brillian|scintillation'),
        ('CARAT', r'carat'), ('SHAPE', r'\bshape'), ('CERTIFICATION', r'certif|\bgia\b|\bigi\b|report'), ('ORIGIN', r'natural|mined|origin'),
        ('PROCESS', r'process|\bcvd\b|\bhpht\b|grown|formed'), ('DURABILITY', r'durab|hardness|scratch|soft|strength'),
        ('PRICE', r'price|cost|afford|cheap|expensive|\$'), ('VALUE', r'value|worth|invest'), ('RESALE', r'resale|resell|melt'),
        ('ETHICS', r'ethic|environment|sustainab'), ('CARE', r'clean|care|maintenance|re-?plat'), ('SIZE', r'\bsize'),
        ('MATERIAL', r'gold|platinum|silver|metal|tungsten|titanium|rhodium'), ('STYLE', r'style|design'), ('SETTING', r'setting|prong|bezel|halo'),
        ('OCCASION', r'engagement|wedding')]


def aio_pattern(aio, ptype):
    h = ' '.join(re.findall(r'^#+ (.+)$', aio, re.M)).lower()
    pats = []
    if re.search(r'differen|similarit|\bvs\b|compar|at a glance|which one|better', h): pats.append('COMPARISON_STRUCTURE')
    if re.search(r'pros|cons', h): pats.append('PROS_CONS')
    if re.search(r'grade|scale', h): pats.append('GRADE_SCALE')
    if re.search(r'popular|types|main|options', h): pats.append('TYPE_LIST')
    if re.search(r'how .*work|process|how it works', h): pats.append('PROCESS_EXPLAINER')
    if re.search(r'calculat', h): pats.append('CALCULATION_STEPS')
    if re.search(r'what (is|vvs)|definition|means', h): pats.append('DEFINITION_FIRST')
    if re.search(r'tips|consider|choose|buying', h): pats.append('BUYING_CONSIDERATIONS')
    if not aio.strip(): pats.append('NO_AI_OVERVIEW_TEXT')
    return f'{ptype}; AIO: ' + ('+'.join(pats) if pats else 'UNSTRUCTURED')


def aio_topics(aio):
    heads = [x.strip() for x in re.findall(r'^#+ (.+)$', aio, re.M)]
    bold = [x.strip(' :') for x in re.findall(r'\*\*([^*]{2,60})\*\*', aio)]
    out = []
    for x in heads + bold:
        if x and x.lower() not in [o.lower() for o in out] and not re.search(r'\$\d', x):
            out.append(x)
    return out


SP = []
for t in TARGETS:
    own = sorted(OWN_SERPS.get(t, []))
    agg_topics, agg_ent, agg_attr = collections.Counter(), collections.Counter(), collections.Counter()
    for kw in own:
        s8, raw = S8[kw], SERP[kw]
        txt = raw['aio'] + '\n' + '\n'.join(raw['org']) + '\n' + '\n'.join(raw['paa'])
        ents = [en['name'] for en in E if m(en['rx'], txt)]
        attrs = [a for a, rx in ATTR if m(rx, txt)]
        tops = aio_topics(raw['aio'])
        agg_topics.update({x.lower() for x in tops}); agg_ent.update(ents); agg_attr.update(attrs)
        SP.append(dict(target_page_id=t, serp_keyword=kw, serp_page_type=s8['dominant_serp_page_type'], ai_overview=s8['ai_overview_presence'],
                       paa=s8['paa_presence'], shopping=s8['shopping_presence'], images=s8['image_presence'], video=s8['video_presence'],
                       dominant_pattern=aio_pattern(raw['aio'], s8['dominant_serp_page_type']), recurring_topics='; '.join(tops[:14]),
                       recurring_questions='; '.join(raw['paa']), recurring_entities='; '.join(ents[:18]), recurring_attributes='; '.join(attrs),
                       confidence=s8['validation_confidence'],
                       notes=f'Stage 8 validated intent {s8["validated_intent"]}; raw file {raw["file"]}. AIO topics = AI Overview headings and bolded terms (trailing personalisation prompts such as budget/carat size included as decision attributes).'))
    if len(own) >= 2:
        n = len(own)
        f = lambda c: '; '.join(f'{k} ({v}/{n})' for k, v in c.most_common() if v >= 2)[:1500]
        feats = {c: sum(S8[k][col] == 'YES' for k in own) for c, col in
                 [('ai', 'ai_overview_presence'), ('paa', 'paa_presence'), ('shop', 'shopping_presence'), ('img', 'image_presence'), ('vid', 'video_presence')]}
        paa_c = collections.Counter(q for k in own for q in SERP[k]['paa'])
        SP.append(dict(target_page_id=t, serp_keyword=f'AGGREGATE ({n} SERPs)', serp_page_type='; '.join(f'{k}:{v}' for k, v in collections.Counter(S8[k]['dominant_serp_page_type'] for k in own).most_common()),
                       ai_overview=f'{feats["ai"]}/{n}', paa=f'{feats["paa"]}/{n}', shopping=f'{feats["shop"]}/{n}', images=f'{feats["img"]}/{n}', video=f'{feats["vid"]}/{n}',
                       dominant_pattern='Recurring across SERPs (count/n)', recurring_topics=f(agg_topics), recurring_questions='; '.join(f'{q} ({v}/{n})' for q, v in paa_c.most_common() if v >= 2)[:1500],
                       recurring_entities=f(agg_ent), recurring_attributes=f(agg_attr), confidence='HIGH' if n >= 4 else 'MEDIUM',
                       notes='Only items recurring on 2+ independent SERPs are listed (stronger evidence than a single SERP).'))
    if not own:
        adj = sorted(k for u in linked(t) for k in OWN_SERPS.get(u, []))
        SP.append(dict(target_page_id=t, serp_keyword='NO_STAGE8_SERP', serp_page_type='NOT_VALIDATED', ai_overview='n/a', paa='n/a', shopping='n/a', images='n/a',
                       video='n/a', dominant_pattern='INSUFFICIENT_EVIDENCE', recurring_topics='', recurring_questions='', recurring_entities='',
                       recurring_attributes='', confidence='INSUFFICIENT_EVIDENCE',
                       notes=NO_SERP_NOTE + (f' Adjacent (Stage 16-linked) validated SERPs used only as weak context: {len(adj)}.' if adj else ' No adjacent validated SERP.')))
wr('18_serp_semantic_patterns.csv', ['target_page_id', 'serp_keyword', 'serp_page_type', 'ai_overview', 'paa', 'shopping', 'images', 'video',
                                     'dominant_pattern', 'recurring_topics', 'recurring_questions', 'recurring_entities', 'recurring_attributes',
                                     'confidence', 'notes'], SP)

# ---------------------------------------------------------------- stats
cnt = lambda rows, k: dict(collections.Counter(r[k] for r in rows))
stats = dict(
    targets=len({g['target_page_id'] for g in GAPS}), gaps=len(GAPS), dropped_no_evidence=DROPPED,
    severity=cnt(GAPS, 'gap_severity'), gap_type=cnt(GAPS, 'gap_type'), owner_status=cnt(GAPS, 'owner_status'),
    coverage=cnt(GAPS, 'coverage_status'), confidence=cnt(GAPS, 'confidence'), treatment=cnt(GAPS, 'recommended_treatment'),
    per_target={t: dict(collections.Counter(g['gap_severity'] for g in GAPS if g['target_page_id'] == t)) for t in TARGETS},
    entities=len(ENT), entity_gaps=sum(1 for r in ENT if r['notes'].startswith('ENTITY_GAP')),
    entity_gaps_by_target=dict(collections.Counter(r['target_page_id'] for r in ENT if r['notes'].startswith('ENTITY_GAP'))),
    questions=len(QROWS), question_rows_by_treatment=cnt(QROWS, 'recommended_treatment'),
    question_gaps=sum(1 for r in QROWS if r['recommended_treatment'] != 'NOT_NEEDED' and r['coverage_status'] in ('FUTURE_PAGE', 'TITLE/H1_NOT_EVIDENT')),
    paa_rows=sum(1 for r in QROWS if r['source'].startswith('STAGE8_PAA') and r['coverage_status'] != 'OWNED_ELSEWHERE'),
    paa_treatment=dict(collections.Counter(r['recommended_treatment'] for r in QROWS if r['source'].startswith('STAGE8_PAA') and r['coverage_status'] != 'OWNED_ELSEWHERE')),
    related_unique=len(RELC), related_not_in_s7=sum(1 for r in RELC if r['in_stage7'] == 'NO'),
    related_rows_not_in_s7=sum(r['occurrences'] for r in RELC if r['in_stage7'] == 'NO'),
    related_class=cnt(RELC, 'classification'), serp_rows=len(SP), cross_page=len(CP), cross_rel=cnt(CP, 'relationship'),
    serps_used=len(SERP_TARGET),
)
json.dump(stats, open(os.path.join(OUT, 'scripts', '18_build_stats.json'), 'w'), indent=1)
print(json.dumps({k: v for k, v in stats.items() if k not in ('per_target', 'dropped_no_evidence')}, indent=1))
print('dropped', len(DROPPED), DROPPED)
