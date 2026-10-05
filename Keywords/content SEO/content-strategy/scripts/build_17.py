#!/usr/bin/env python3
"""Stage 17 — keyword deep dives (keyword intelligence layer).

LOCAL ONLY. Reads the accepted Stage 3/7/8/10/11/13/14/15/16 files and the raw Stage 8
SERP JSON already on disk (paid for in Stage 8). No DataForSEO or other API call.

Stage 15 is authoritative for keyword ownership, Stage 11 for clusters, Stage 8 for SERP
evidence, Stage 16 for link relationships. Nothing here changes any of those. The curated
knowledge below (primary-term choices, concept lexicons, gap notes) is interpretation that
sits on top of the upstream decisions; every concept and question must be matched to a
real keyword, PAA question or related search before it is written out.

Outputs (content-strategy/):
  17_keyword_deep_dive.csv, 17_topic_intelligence.csv, 17_semantic_concepts.csv,
  17_question_map.csv, 17_keyword_relationships.csv, 17_gap_register.csv
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


def vol(x):
    s = x.get('search_volume', '')
    return int(s) if str(s).isdigit() else -1


# ---------------------------------------------------------------- load upstream
M15 = rd('architecture/15_keyword_url_map.csv')
REG15 = {r['target_id']: r for r in rd('architecture/15_target_page_registry.csv')}
REP15 = rd('content-strategy/15_ranking_equity_protection.csv')
REG11 = {r['cluster_id']: r for r in rd('clusters/11_cluster_registry.csv')}
KCM11 = {r['keyword']: r for r in rd('clusters/11_keyword_cluster_map.csv')}
REL11 = rd('clusters/11_cluster_relationships.csv')
S8 = {r['keyword']: r for r in rd('serp/analysis/08_hod_serp_validation.csv')}
S7 = {r['keyword']: r for r in rd('dataforseo/processed/07_hod_master_keyword_database.csv')}
INV10 = {r['url']: r for r in rd('content-strategy/10_existing_content_inventory.csv')}
PLR16 = {r['page_id']: r for r in rd('architecture/16_page_link_requirements.csv')}
ARCH14 = {r['topic_id']: r for r in rd('architecture/14_education_architecture.csv')}
BYKW = {r['keyword']: r for r in M15}

# raw Stage 8 SERPs: PAA questions and related searches per SERP keyword
PAA, RELATED = {}, {}
for f in sorted(glob.glob(P('serp/raw/08_stage8_by_id/*.json'))):
    d = json.load(open(f, encoding='utf-8'))
    for t in d.get('tasks') or []:
        for res in t.get('result') or []:
            kw = res.get('keyword')
            items = res.get('items') or []
            PAA[kw] = [q.get('title') for it in items if it.get('type') == 'people_also_ask'
                       for q in (it.get('items') or []) if q.get('title')]
            RELATED[kw] = [(q if isinstance(q, str) else q.get('title')) for it in items
                           if it.get('type') == 'related_searches' for q in (it.get('items') or [])]
            RELATED[kw] = [q for q in RELATED[kw] if q]

EXCLUDED_TESTER_KW = 'cvd/hpht diamond tester'   # never used as evidence (Stage 15/16 special rule)

# ---------------------------------------------------------------- text helpers
QWORD = re.compile(r"^(what|whats|what's|how|why|when|where|which|who|is|are|do|does|did|can|could|will|would|should)\b")
SYN = [(r'lab[- ]grown|lab[- ]created|lab[- ]made|lab', 'lab'), (r'diamonds', 'diamond'),
       (r'\bdoes\b|\bwill\b|\bcan\b', 'do'), (r'\bis\b|\bare\b', 'be'), (r'testers?|tests?', 'test'),
       (r'\bthe\b|\ba\b|\ban\b|\btheir\b', ' '), (r'-', ' ')]


def canon(k, numbers=False):
    s = k.lower().replace('-', ' ')
    for a, b in SYN:
        s = re.sub(a, b, s)
    if numbers:
        s = re.sub(r'\b\d+(\.\d+)?(/\d+)?\b|\bhalf\b', 'N', s)
        s = re.sub(r'\bN( N)+\b', 'N', s)
        s = re.sub(r'\bct\b|\bct tw\b', 'carat', s)
    return ' '.join(s.split())


def is_question(k):
    return bool(QWORD.match(k.lower()))


VS_AMBIG = re.compile(r'^([d-k](-[d-k])?|[d-k]{2}) vs diamond$')   # "f vs diamond" = F colour + VS clarity?


def is_comparison(k):
    kl = k.lower()
    if VS_AMBIG.match(kl):
        return False
    return bool(re.search(r'\bvs\b|versus|difference|\bor\b|better|compare|comparison', kl)) and not \
        re.search(r'^(vs|diamond clarity vs$)', kl) and not re.search(r'\bvs (clarity|diamond clarity|diamond quality|diamond chart)\b', kl)


MODS = [
    ('LOCATION', r'near me|\busa\b|united states|\bindia\b|\bsurat\b|\bnyc\b|new york|london|dubai'),
    ('BUYING', r'\bbuy\b|\bshop\b|for sale|online|\bchoose\b|should i (buy|get)|what .* should i get'),
    ('PRICE', r'price|cost|cheap|expensive|worth|value|invest|resale|per carat|pawn|\bsell\b|trade in|waste of money'),
    ('COMPARISON', r'\bvs\b|versus|difference|\bor\b|better|comparison|compare'),
    ('CERTIFICATION', r'certif|\bgia\b|\bigi\b|\bags\b|\begl\b|\bgsi\b|report|grading lab|appraisal|graded'),
    ('CARAT', r'carat|\bct\b|ctw'),
    ('SHAPE', r'shape|\boval\b|marquise|radiant|asscher|emerald cut|princess|cushion|\bpear\b'),
    ('ORIGIN', r'\blab\b|natural|synthetic|mined|man[- ]made|artificial|rough|\braw\b|unpolished|untreated'),
    ('PROCESS', r'\bcvd\b|\bhpht\b|process|\bmade\b|formed|form\b|created|grow|method|manufactur|extract|mining|treatment|irradiat'),
    ('QUALITY', r'quality|\bgood\b|\bbest\b|grade|grading|rating|\bok\b|okay|tacky|flawless|scale|chart'),
    ('ATTRIBUTE', r'clarity|colou?r|colorless|\bcut\b|facet|inclusion|fluoresc|cloudy|hardness|vvs|\bvs[12]?\b|\bsi[123]?\b|\bif\b|\bfl\b|sparkle|refraction|lattice|crystal|melting'),
    ('STYLE', r'side stone|halo|milgrain|setting|pav[eé]|solitaire|stud'),
    ('OCCASION', r'engagement|wedding|anniversary'),
    ('GENDER', r"\bmens?\b|men's|womens?\b|women's"),
    ('MATERIAL', r'gold|\b1[048]k\b|platinum|silver|tungsten|titanium|rhodium|metal|stainless|iridium|alloy'),
    ('SIZE', r'\bsize|too big|too small|big enough|thickness|largest'),
    ('CARE', r'clean|\bcare\b|cloudy|fade|tarnish|scratch|shower|replate|chip|crack|break'),
    ('AUTHENTICITY', r'\breal\b|fake|tester|\btest|detect|\btell\b|authentic|serial number|microscope|x ray'),
    ('ETHICS', r'ethical|environment|sustainab|eco|carbon neutral|conflict'),
]
TRANS_MOD = re.compile(r'\bbuy\b|\bshop\b|for sale|near me|online|\bstore\b|jewell?ers?\b|wholesale|supplier|'
                       r'\brings?\b|earrings|necklace|bracelet|\bbands?\b|collection|custom|bespoke|\bsale\b')
COMM_MOD = re.compile(r'price|cost|\bbest\b|\bvs\b|versus|review|worth|value|cheap|expensive|certified|certificate|'
                      r'per carat|invest|better')


def modifiers(k):
    kl = k.lower()
    found = [n for n, p in MODS if re.search(p, kl)]
    if VS_AMBIG.match(kl) and 'COMPARISON' in found:
        found.remove('COMPARISON')
    return found


def modifier_changes_intent(mods, k):
    kl = k.lower()
    if 'LOCATION' in mods or re.search(r'\bbuy\b|\bshop\b|for sale|near me', kl):
        return 'YES (toward transactional)'
    if 'COMPARISON' in mods:
        return 'FORMAT_ONLY (comparison angle; same owner per Stage 15)'
    if 'PRICE' in mods:
        return 'UNCLEAR (price wording in an informational question)' if is_question(k) else 'UNCLEAR'
    return 'NO' if mods else ''


def commercial_signal(k, validated_intent):
    kl = k.lower()
    t, c = bool(TRANS_MOD.search(kl)), bool(COMM_MOD.search(kl))
    if not (t or c):
        return 'NONE'
    if validated_intent == 'TRANSACTIONAL':
        return 'TRANSACTIONAL (Stage 8)'
    if is_question(k) or validated_intent in ('INFORMATIONAL',):
        return 'INFORMATIONAL_WITH_COMMERCIAL_WORD'
    return 'TRANSACTIONAL_MODIFIER' if t else 'COMMERCIAL_RESEARCH_MODIFIER'


FEAT = [('ai_overview_presence', 'AI Overview'), ('paa_presence', 'PAA'),
        ('featured_snippet_presence', 'Featured Snippet'), ('video_presence', 'Video'),
        ('image_presence', 'Images'), ('shopping_presence', 'Shopping'), ('local_presence', 'Local Pack')]


def s8_features(kw):
    s = S8.get(kw)
    if not s:
        return ''
    out = [n for c, n in FEAT if s[c] == 'YES']
    if 'discussions_and_forums' in s['serp_features']:
        out.append('Forums')
    return '; '.join(out)


# ---------------------------------------------------------------- curated target profiles
# primary: the chosen primary keyword(s) (first = main). variants: close variants.
# covered: regex describing what the EXISTING page's title/H1/Stage 10 topic addresses (None = future page).
# concepts: (concept, type, relationship, regex).  gaps: (gap_type, clusters, description, kw_regex, confidence, stage18, notes)
T = {}

T['EDU-LG-00'] = dict(
    topic='What lab-grown diamonds are: definition, names/terminology, types, short history (process summary pending EDU-LG-04)',
    primary=['synthetic diamonds'], variants=['lab grown diamond definition', 'lab grown diamonds definition', 'lab grown diamonds wiki', 'lab grown diamonds wikipedia', 'man made diamonds wiki'],
    head='lab grown diamonds (135,000; CONDITIONAL_NOT_MAPPED — held for the conditional commercial Lab-Grown hub, not owned here)',
    pconf='LOW', core=['CL-002', 'CL-003', 'CL-004'],
    why='Highest-demand informational definition/terminology term the pillar owns. Not validated; the SERP may be science/Wikipedia-led, so fit is unconfirmed. The commercial head term is held for the conditional commercial hub (Stage 12 D-05), so the pillar is led by definition and terminology rather than the head term.',
    status='FUTURE_PAGE', covered=None,
    content_note='No existing page. The existing /blog/are-lab-grown-diamonds-real article topic string includes "what they are, how made" (Stage 10), so definition content partly exists there under a different owner (EDU-LG-01).',
    concepts=[
        ('Lab-grown diamond definition', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'definition|information|wiki|article|lab grown diamonds how'),
        ('Terminology: synthetic / man-made / lab-created / lab-grown names', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'synthetic|man[- ]made|name|called|lab created|artificial'),
        ('Types of lab-grown diamonds', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'types?\b'),
        ('Growth process overview (CVD and HPHT at summary level)', 'SUPPORTING_CONCEPT', 'PROCESS', r'process|how are|^how lab|lab grown diamonds how|made|making|manufactur|methods?|can you make|can we make'),
        ('History of lab-grown diamonds (first synthesis)', 'SUPPORTING_CONCEPT', 'CONTEXT', r'history|first'),
        ('General Electric (first reproducible synthesis)', 'RELATED_ENTITY', 'ENTITY', r'general electric'),
        ('FTC Jewelry Guides (labelling of lab-grown diamonds)', 'RELATED_ENTITY', 'ENTITY', r'\bftc\b'),
        ('Lab-grown vs lab-created (terminology equivalence)', 'SUPPORTING_CONCEPT', 'COMPARISON_PARTNER', r'lab grown vs lab created'),
        ('Largest synthetic diamond', 'OPTIONAL_CONTEXT', 'CONTEXT', r'largest'),
        ('Growth time-lapse / visual demonstration', 'OPTIONAL_CONTEXT', 'FORMAT', r'time lapse'),
        ('Moissanite (not a lab-grown diamond)', 'OPTIONAL_CONTEXT', 'COMPARISON_PARTNER', r'moissanite'),
    ],
    gaps=[
        ('NO_CONTENT', 'CL-002; CL-003; CL-004', 'Pillar does not exist. Definition, terminology and type demand (synthetic diamonds 2,900; name/called variants 590) has no HOD owner page today.', r'.', 'MEDIUM', 'HIGH', 'Proposed URL /education/lab-grown-diamonds. Education label "Lab-Grown Diamond Guide" awaits Stage 16 sign-off.'),
        ('MISSING_ENTITY', 'CL-003', 'Terminology and labelling concepts (FTC guidance; "lab-created" vs "lab-grown" vs "synthetic") appear in owned keywords and no existing HOD page title addresses them.', r'ftc|called|name|synthetic|lab grown vs lab created', 'MEDIUM', 'HIGH', ''),
        ('MISSING_SUBTOPIC', 'CL-015', 'Process queries (how are synthetic diamonds made 880; lab grown diamond process 480) are interim-homed here. Their owner topic EDU-LG-04 is CONDITIONAL, so the pillar needs a process summary that links to EDU-LG-03 rather than a full process guide.', r'process|made|how', 'MEDIUM', 'MEDIUM', 'Stage 15 HIGH-risk pair: the process split matters only if EDU-LG-04 is created.'),
        ('MISSING_SUBTOPIC', 'CL-014', 'History queries (history/first lab-grown diamond, General Electric) have no existing HOD coverage.', r'history|first|general electric|largest', 'LOW', 'LOW', 'Low-volume subtopic.'),
    ])

T['EDU-LG-01'] = dict(
    topic='Authenticity: are lab-grown diamonds real diamonds (real vs fake)',
    primary=['are lab grown diamonds real'], variants=['is lab grown diamond real', 'are lab diamonds real', 'are lab created diamonds real', 'is a lab grown diamond a real diamond', 'is a lab diamond a real diamond', 'is lab created diamonds real', 'lab created diamond real', 'lab created diamonds real', 'is lab grown diamonds real diamonds', 'is lab diamond real diamond', 'is lab diamonds real diamonds'],
    head='are lab grown diamonds real (14,800)', pconf='HIGH', core=['CL-010'],
    why='Highest-demand, Stage 8 validated INFORMATIONAL owner of CL-010, with an exact match to the existing article title. The Stage 8 SERP is COMPARISON-led, which is why Stage 14 recorded MEDIUM risk against EDU-LG-02.',
    status='WEAK_EXISTING_CONTENT', covered=r'\breal\b|lab',
    content_note='Existing /blog/are-lab-grown-diamonds-real-a-complete-buyer-s-guide. Its H1 matches the primary query, but Stage 3 shows no ranking despite 14,800 monthly searches. Body not audited (no Stage 1/10 body extract).',
    concepts=[
        ('What makes a diamond "real" (same material vs different origin)', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'\breal\b'),
        ('"Fake" vs simulant: lab-grown diamond is not a simulant', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'fake'),
        ('Lab-created / lab-grown / lab diamond as equivalent terms', 'SUPPORTING_CONCEPT', 'CONTEXT', r'lab created|lab diamond'),
        ('Tester and jeweller identification (link to EDU-LG-09)', 'SUPPORTING_CONCEPT', 'LINKED_TOPIC', r'test'),
        ('Downsides / worth buying (link to EDU-LG-02)', 'OPTIONAL_CONTEXT', 'LINKED_TOPIC', r'downside|worth|disadvantage'),
        ('Price vs natural (link to EDU-LG-05)', 'OPTIONAL_CONTEXT', 'LINKED_TOPIC', r'cheaper|cost|price|expensive'),
    ],
    gaps=[
        ('MISSING_SERP_FORMAT', 'CL-010', 'Stage 8 validated the primary as INFORMATIONAL with a COMPARISON-dominant SERP (Reddit, Kay comparison pages). A pure authenticity explainer may under-serve that format. The page has to set out the real-vs-natural framing without taking over EDU-LG-02 comparison ownership.', r'real', 'MEDIUM', 'HIGH', 'Stage 14 MEDIUM cannibalization risk with EDU-LG-02 (max 2 shared URLs).'),
        ('MISSING_QUESTION', 'CL-010', 'The "fake" and "real or fake" variants (880 + 390 + 390 + 260 + 110) are not reflected in the existing title/H1. Body coverage is unknown.', r'fake', 'LOW', 'MEDIUM', 'Title-level evidence only.'),
        ('MISSING_AEO_COVERAGE', 'CL-010', 'The primary SERP shows AI Overview + PAA (Stage 8). HOD has no ranking position, so there is no evidence the existing page is eligible for these features.', r'real', 'MEDIUM', 'HIGH', 'Performance evidence (no Stage 3 rank) and not a content audit.'),
    ])

T['EDU-LG-02'] = dict(
    topic='Lab-grown vs natural diamonds: differences, which is better, pros & cons, worth it',
    primary=['lab grown vs natural diamonds'], variants=['lab diamonds vs natural diamonds', 'natural vs lab grown diamonds', 'lab created vs natural diamonds', 'difference between lab grown and natural diamonds', 'difference between lab grown diamonds and natural diamonds', 'natural vs synthetic diamonds', 'lab made vs natural diamonds', 'natural diamonds vs lab', 'diamonds lab vs natural', 'natural versus lab diamonds', 'lab diamonds vs diamonds'],
    head='lab grown vs natural diamonds (22,200)', pconf='HIGH', core=['CL-011'],
    why='Highest-demand, validated INFORMATIONAL/COMPARISON term. Exact match to the page type (COMPARISON_GUIDE) and to the existing page. The Stage 3 rankings are low-volume "which is better" variants (positions 29–40), so ranking equity and head demand point to the same page.',
    status='PARTIAL_EXISTING_CONTENT', covered=r'\bvs\b|versus|difference|natural|better|which|right',
    content_note='Existing /blog/lab-grown-vs-natural-diamonds-the-honest-comparison (H1 "Lab-Grown vs Natural Diamonds: Which One Is Right for You?"). Ranks 29/36/40 for three "which is better" variants and has no ranking for the 22,200 head term. Body not audited.',
    concepts=[
        ('Differences between lab-grown and natural diamonds', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'\bvs\b|versus|difference|natural and lab'),
        ('Which is better / decision framing', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'better|which|should i|or natural|or lab|natural or'),
        ('Pros and cons / disadvantages of lab-grown', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'pros|cons\b|disadvantage|downside'),
        ('Worth it / value for money', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'worth|waste of money'),
        ('Perception and social acceptance (tacky, popular, jeweller attitudes)', 'SUPPORTING_CONCEPT', 'CONTEXT', r'tacky|popular|\bok\b|okay|rich people|hate|avoid'),
        ('Natural (mined) diamonds', 'RELATED_ENTITY', 'COMPARISON_PARTNER', r'natural|mined'),
        ('Synthetic / lab-made terminology', 'SUPPORTING_CONCEPT', 'CONTEXT', r'synthetic|lab made|lab created'),
        ('Price difference (link to EDU-LG-05)', 'SUPPORTING_CONCEPT', 'LINKED_TOPIC', r'price|cost'),
        ('Can you tell them apart (link to EDU-LG-09)', 'SUPPORTING_CONCEPT', 'LINKED_TOPIC', r'tell the difference|side by side|identify|jeweler tell'),
        ('Sparkle / appearance parity (link to EDU-LG-08)', 'SUPPORTING_CONCEPT', 'LINKED_TOPIC', r'sparkle|as good as'),
        ('Moissanite and cubic zirconia as third options (owners conditional)', 'OPTIONAL_CONTEXT', 'COMPARISON_PARTNER', r'moissanite|cubic zirconia'),
        ('Clarity differences between origins', 'OPTIONAL_CONTEXT', 'ATTRIBUTE', r'clarity'),
    ],
    gaps=[
        ('MISSING_SUBTOPIC', 'CL-012', 'The CL-012 worth-it/pros-cons family is interim-homed here: are lab grown diamonds worth it 1,900; are lab grown diamonds good 1,300 ×2; disadvantages 880; cons 140. The existing title frames a decision ("Which One Is Right for You?") but does not name pros/cons or worth-it. Body coverage unknown.', r'worth|good|cons\b|disadvantage|pros|better|should i', 'MEDIUM', 'HIGH', 'Owner topic EDU-LG-06 is CONDITIONAL (Stage 14). Interim home is this page.'),
        ('MISSING_QUESTION', 'CL-012', 'Perception questions (tacky, popular, "ok", PAA "why do jewelers hate", "do rich people buy") are present in keywords and PAA.', r'tacky|popular|\bok\b|okay', 'LOW', 'MEDIUM', 'FAQ-level. Avoid FAQ spam.'),
        ('MISSING_AEO_COVERAGE', 'CL-011', 'All four validated SERPs show AI Overview + PAA. HOD ranks only 29–40 for low-volume variants and has no position for the 22,200 head.', r'\bvs\b|better', 'MEDIUM', 'HIGH', ''),
        ('MISSING_COMPARISON', 'CL-011', 'Related searches pair the comparison with moissanite and cubic zirconia ("lab-grown vs natural vs moissanite"). Those comparisons are owned by CONDITIONAL Gemstones topics, so this is a linking/mention need and not an ownership change.', r'moissanite|zirconia', 'LOW', 'LOW', 'Do not expand ownership. EDU-GEM-* are conditional.'),
    ])

T['EDU-LG-03'] = dict(
    topic='CVD vs HPHT: the single home for both growth methods (comparison + single-method explainers)',
    primary=['hpht vs cvd'], variants=['cvd vs hpht diamonds', 'hpht vs cvd diamond', 'cvd or hpht', 'cvd vs hpht lab diamond', 'cvd vs hpht lab diamonds', 'lab diamond cvd vs hpht', 'lab grown diamonds cvd vs hpht', 'lab-grown diamond cvd vs hpht', 'cvd vs hpht which is better', 'which is better cvd or hpht diamond'],
    head='hpht lab grown diamond (8,100) and cvd diamond (3,600): single-method heads owned by this page (Stage 14 D14: no separate CVD/HPHT pages)',
    pconf='HIGH', core=['CL-016'],
    why='The page is a COMPARISON_GUIDE. The validated comparison terms are EDITORIAL_GUIDE SERPs, and 11 of the 18 protected Stage 3 rankings are CL-016 comparison variants (5 HPHT, 2 CVD). Higher-volume single-method heads (HPHT 8,100; CVD 3,600) are secondary heads on the same page, not the primary, because of the page type and ranking equity.',
    status='PARTIAL_EXISTING_CONTENT', covered=r'cvd|hpht',
    content_note='Existing /blog/cvd-vs-hpht-lab-grown-diamonds-what-buyers-should-know (H1 "CVD vs HPHT Lab-Grown Diamonds: What\'s the Difference?"). Holds 18 protected rankings (positions 27–54) plus the excluded tester keyword (68). No Stage 3 ranking for "cvd diamond" (3,600) or "cvd lab grown diamonds" (720).',
    concepts=[
        ('CVD (chemical vapor deposition)', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'\bcvd\b'),
        ('HPHT (high pressure, high temperature)', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'hpht'),
        ('Which growth method is better', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'better|best|\bvs\b|\bor\b'),
        ('Growth methods in general', 'SUPPORTING_CONCEPT', 'PROCESS', r'method|process|machine'),
        ('CVD acronym / full form', 'SUPPORTING_CONCEPT', 'CONTEXT', r'full form'),
        ('Pros and cons / disadvantages by method', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'pros and cons|disadvantage|downside'),
        ('Are CVD/HPHT diamonds real (link to EDU-LG-01)', 'SUPPORTING_CONCEPT', 'LINKED_TOPIC', r'\breal\b|fake'),
        ('Price/value by method (link to EDU-LG-05 for value)', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'price|cost|worth|value'),
        ('Tester behaviour by method (link to EDU-LG-09)', 'SUPPORTING_CONCEPT', 'LINKED_TOPIC', r'tester'),
        ('Type IIa diamonds', 'RELATED_ENTITY', 'ENTITY', r'\biia\b'),
        ('HPHT treatment vs HPHT growth (disambiguation)', 'SUPPORTING_CONCEPT', 'CONTEXT', r'treated'),
        ('GIA (research on growth methods)', 'RELATED_ENTITY', 'ENTITY', r'\bgia\b'),
        ('Comparison with natural diamonds / moissanite', 'OPTIONAL_CONTEXT', 'COMPARISON_PARTNER', r'natural|moissanite'),
    ],
    gaps=[
        ('MISSING_SUBTOPIC', 'CL-018', 'Single-method CVD demand ("cvd diamond" 3,600; "cvd lab grown diamonds" 720) has no Stage 3 ranking, while HPHT single-method variants rank 44–49. The page is the only home (Stage 14), so CVD needs explainer depth equal to HPHT.', r'^cvd diamond$|cvd lab grown|lab grown cvd|lab grown diamond cvd|cvd method|full form', 'MEDIUM', 'HIGH', 'Not validated: "cvd diamond" (DataForSEO TRANSACTIONAL label). "what is cvd lab grown diamond" validated MIXED (LOW).'),
        ('MISSING_QUESTION', 'CL-016; CL-017; CL-018', 'Recurring PAA across the 18 validated CVD/HPHT SERPs: disadvantages of CVD, price difference CVD vs HPHT, "are CVD diamonds worth buying", "are HPHT diamonds worth anything", "will CVD pass a diamond tester".', r'better|real', 'HIGH', 'HIGH', 'Stage 8 PAA repeated across many SERPs is strong AEO evidence.'),
        ('MISSING_ENTITY', 'CL-017', 'Related searches name "HPHT vs CVD vs IIa" (Type IIa) and PAA name "HPHT treated diamond". These entities are not visible in the title/topic.', r'hpht', 'MEDIUM', 'MEDIUM', ''),
        ('MISSING_AEO_COVERAGE', 'CL-016', 'AI Overview appears on 17 of 18 validated SERPs, and PAA on all 18. HOD positions are 27–54, below the AI Overview-cited range (Stage 8 citations not measured).', r'\bvs\b|\bor\b', 'MEDIUM', 'HIGH', 'Do not move the URL (DO_NOT_MOVE_NOW; 18 protected rankings).'),
    ])

T['EDU-LG-05'] = dict(
    topic='Lab-grown diamond price, value, resale & investment (no hard-coded prices)',
    primary=['do lab grown diamonds hold their value', 'are lab grown diamonds cheaper'],
    variants=['do lab grown diamonds hold value', 'does lab grown diamonds hold value', 'are lab grown diamonds less expensive', 'are lab-grown diamonds less expensive', 'is lab grown diamond cheaper'],
    head='are lab grown diamonds cheaper (2,400) / do lab grown diamonds hold their value (1,900)', pconf='MEDIUM', core=['CL-008', 'CL-009'],
    why='Two co-primaries: price (CL-008) and value retention (CL-009) form one searcher need (what it costs and what it is worth later), per Stage 14. Value retention leads because Stage 13 forbids dated price levels on Education pages. Neither is validated.',
    status='FUTURE_PAGE', covered=None, content_note='No existing page (PROPOSED_PROVISIONAL, URL_PENDING).',
    concepts=[
        ('Price of lab-grown vs natural', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'cheap|expensive|less expensive|price|cost'),
        ('Resale value / holding value', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'resale|hold (their )?value|worth anything|worthless|worth less|have value|increase in value'),
        ('Investment suitability', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'invest'),
        ('Price trend over time (getting cheaper)', 'SUPPORTING_CONCEPT', 'CONTEXT', r'get cheaper'),
        ('Selling, pawning and trade-in', 'SUPPORTING_CONCEPT', 'SUBTOPIC', r'pawn|\bsell\b|trade in'),
        ('Price per carat (concept only; no live figures)', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'per carat|carat'),
        ('Role of a certificate in resale', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'certificate'),
        ('Natural diamond value retention (comparison)', 'SUPPORTING_CONCEPT', 'COMPARISON_PARTNER', r'natural'),
        ('Production cost of growing a diamond', 'OPTIONAL_CONTEXT', 'CONTEXT', r'cost to grow'),
    ],
    gaps=[
        ('NO_CONTENT', 'CL-008; CL-009; CL-086', 'No HOD page covers price, value or resale, the lab-grown buyer\'s main value questions (2,400 + 1,900 + 590 heads).', r'.', 'MEDIUM', 'HIGH', 'Provisional topic.'),
        ('MISSING_COMMERCIAL_CONTEXT', 'CL-008', 'Price questions sit next to a commercial decision. Stage 13 bars dated price levels on Education pages, so commercial context must come from links to the (conditional) commercial Lab-Grown hub, not from embedded prices.', r'cheap|price|per carat|expensive', 'MEDIUM', 'MEDIUM', 'The commercial hub (COM-LG-HUB) is CONDITIONAL.'),
        ('MISSING_SUBTOPIC', 'CL-086', 'Selling, pawning and trade-in questions (CL-086) are grouped here. HOD\'s own buy-back/trade-in policy is unknown (business question).', r'pawn|sell|trade', 'LOW', 'MEDIUM', 'Needs a business input before any HOD claim.'),
    ])

T['EDU-LG-07'] = dict(
    topic='Lab-grown diamond ethics & environmental impact',
    primary=['are lab grown diamonds ethical'], variants=['are lab grown diamonds more ethical', 'lab grown diamond ethical', 'lab grown diamonds ethical', 'ethical lab grown diamonds'],
    head='are lab grown diamonds more ethical (320)', pconf='LOW', core=['CL-013'],
    why='The generic ethics question is the cluster head need. "more ethical" (320) is a close variant with a comparative angle. Not validated, and the environmental keywords are a separate facet of the same topic.',
    status='FUTURE_PAGE', covered=None, content_note='No existing page (PROPOSED_PROVISIONAL, URL_PENDING).',
    concepts=[
        ('Ethical sourcing (vs mined supply chain)', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'ethical'),
        ('Environmental impact (energy, footprint)', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'environment|sustainab|eco'),
        ('Carbon-neutral claims and their substantiation', 'SUPPORTING_CONCEPT', 'CONTEXT', r'carbon neutral'),
    ],
    gaps=[
        ('NO_CONTENT', 'CL-013', 'No HOD page covers ethics or sustainability questions.', r'.', 'MEDIUM', 'MEDIUM', ''),
        ('MISSING_ENTITY', 'CL-013', 'Carbon-neutral and "eco" claims need evidence (certifications, energy source). The trust principle requires any HOD-specific claim to be substantiated.', r'carbon|eco|sustainab', 'LOW', 'MEDIUM', 'Business/trust input required. No SERP validation.'),
    ])

T['EDU-LG-08'] = dict(
    topic='Lab-grown appearance & durability over time: cloudiness, fluorescence, fading, treatments',
    primary=['do lab grown diamonds get cloudy', 'do lab grown diamonds have fluorescence'],
    variants=['do lab-grown diamonds get cloudy', 'do lab grown diamonds fluoresce', 'do lab-grown diamonds fluoresce', 'lab grown diamond fluorescence', 'lab grown diamonds fluorescence'],
    head='irradiated diamonds (260; CL-089 treatments subtopic)', pconf='LOW', core=['CL-019'],
    why='CL-019 is the core cluster. Cloudiness and fluorescence are its two main questions. "irradiated diamonds" is higher volume but belongs to the treatments subtopic (CL-089). No validation.',
    status='FUTURE_PAGE', covered=None, content_note='No existing page (PROPOSED_PROVISIONAL, URL_PENDING).',
    concepts=[
        ('Cloudiness over time', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'cloudy'),
        ('Fluorescence / UV reaction', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'fluoresc|\buv\b|glow'),
        ('Looks and sparkle vs natural', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'look real|sparkle'),
        ('Fading / colour stability / lifespan', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'fade|lifespan'),
        ('Treatments: irradiation, post-growth treatment, clarity enhancement', 'SUPPORTING_CONCEPT', 'SUBTOPIC', r'irradiat|treatment|enhanced'),
    ],
    gaps=[
        ('NO_CONTENT', 'CL-019; CL-089', 'No HOD page answers appearance/durability-over-time questions (cloudy, fluorescence, glow, fade).', r'.', 'MEDIUM', 'MEDIUM', ''),
        ('MISSING_ENTITY', 'CL-089', 'Treatment concepts (irradiated, post-growth treatment, clarity enhanced) appear only in keywords. HOD disclosure practice for treated stones is unknown.', r'irradiat|treatment|enhanced', 'LOW', 'MEDIUM', 'Business input: does HOD sell treated stones?'),
    ])

T['EDU-LG-09'] = dict(
    topic='Detecting lab-grown diamonds: diamond testers, jeweller/lab identification',
    primary=['do lab grown diamonds pass a diamond tester', 'can a jeweler tell a lab grown diamond'],
    variants=['does lab grown diamonds pass diamond tester', 'does lab-grown diamonds pass diamond tester', 'do lab grown diamonds pass the diamond tester', 'will a lab grown diamond pass a diamond tester', 'do lab diamonds pass diamond tester', 'can lab grown diamonds pass a diamond tester', 'will lab grown diamonds pass diamond tester', 'does lab grown diamond pass diamond tester'],
    head='does lab grown diamonds pass diamond tester (880; grammatical variant of the primary)', pconf='MEDIUM', core=['CL-021', 'CL-020'],
    why='Natural-language form of the CL-021 head family. CL-021 is 28 near-identical variants, so the group demand is large even though each variant is small. "can a jeweler tell" carries the identification (CL-020) need. The only validated members are CL-022 tester-device SERPs (OTHER / EDITORIAL_GUIDE), which include marketplace results.',
    status='FUTURE_PAGE', covered=None, content_note='No existing page. The CVD vs HPHT article ranks 68 for the excluded "cvd/hpht diamond tester". That keyword is not used as evidence here (Stage 15/16 rule).',
    concepts=[
        ('Diamond tester results for lab-grown diamonds', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'tester|\btest'),
        ('Jeweller and gemological-lab identification', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'jeweler|detect|\btell\b'),
        ('Thermal conductivity testers (how they work)', 'SUPPORTING_CONCEPT', 'PROCESS', r'thermal|heat test|beeps'),
        ('Microscope inspection', 'SUPPORTING_CONCEPT', 'PROCESS', r'microscope'),
        ('Laser inscription / serial numbers', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'serial'),
        ('X-ray and home tests (sparkle/light test)', 'OPTIONAL_CONTEXT', 'PROCESS', r'x ray|sparkle test|light test'),
        ('Where to get a diamond tested', 'SUPPORTING_CONCEPT', 'CONTEXT', r'where can i get'),
        ('Which gems pass a diamond tester (moissanite false positives)', 'RELATED_ENTITY', 'COMPARISON_PARTNER', r'gems|moissanite'),
        ('Clarity grade and tester results', 'OPTIONAL_CONTEXT', 'ATTRIBUTE', r'\bsi\b'),
        ('Reliability of testers', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'testers real|tester real|actually work|really work|tester work'),
    ],
    gaps=[
        ('NO_CONTENT', 'CL-020; CL-021', 'No HOD page covers the tester/identification question family (CL-021: 28 variants).', r'.', 'MEDIUM', 'HIGH', ''),
        ('MISSING_SERP_FORMAT', 'CL-022', 'The validated tester SERPs are OTHER/EDITORIAL with Amazon/marketplace and device brands. Device-shopping intent is not HOD business (Stage 12 D-16), so the page must stay on the question intent (CL-021), not on devices.', r'tester', 'MEDIUM', 'MEDIUM', '"cvd/hpht diamond tester" remains excluded and was not used.'),
    ])

T['EDU-LG-10'] = dict(
    topic='How to choose a lab-grown diamond (stone buying guide)',
    primary=['how to choose a lab grown diamond'], variants=[], head='how to choose a lab grown diamond (30)', pconf='HIGH', core=['CL-024'],
    why='The only owned term with a direct title match. Stage 8 validated INFORMATIONAL/EDITORIAL_GUIDE (HIGH). Ranks 35 (protected). Demand is small. The page\'s value is commercial-research proximity, not volume.',
    status='PARTIAL_EXISTING_CONTENT', covered=r'choose|buy',
    content_note='Existing /blog/how-to-choose-a-lab-grown-diamond-the-complete-buyer-s-guide ranks 35. Stage 1/10 records heavy overlap with the 4Cs article and the engagement-ring-online article (3 articles, one buying intent). Migration deferred (D-19).',
    concepts=[
        ('Choosing a lab-grown diamond (decision steps)', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'choose|buy'),
        ('Engagement-ring purchase decision (boundary with deferred EDU-RJG-04)', 'SUPPORTING_CONCEPT', 'SUBTOPIC', r'engagement|ring'),
        ('4Cs priorities for lab-grown (link to EDU-4C-00)', 'SUPPORTING_CONCEPT', 'LINKED_TOPIC', r'vs1|vs2|clarity|\bif\b'),
        ('Budget / price per carat (link to EDU-LG-05)', 'SUPPORTING_CONCEPT', 'LINKED_TOPIC', r'pay|price'),
        ('Is it worth it (link to EDU-LG-02)', 'OPTIONAL_CONTEXT', 'LINKED_TOPIC', r'worth'),
        ('Lifespan / durability (link to EDU-LG-08)', 'OPTIONAL_CONTEXT', 'LINKED_TOPIC', r'lifespan'),
    ],
    gaps=[
        ('MISSING_COMMERCIAL_CONTEXT', 'CL-024', '"should i buy a lab grown diamond engagement ring" (30 ×2) mixes stone choice and ring purchase. The boundary with the deferred engagement-ring buying guide (EDU-RJG-04) depends on the unapproved D-19 SERP supplement.', r'should i buy', 'LOW', 'MEDIUM', 'D-19 remains unapproved.'),
        ('POSSIBLE_OVERLAP_NOTE', 'CL-024; CL-040', 'Stage 1/10 overlap: three existing articles cover the same buying intent. Stage 13 DEFER decision stands. Recorded here only so Stage 18 can assess scope.', r'choose', 'MEDIUM', 'MEDIUM', 'Not a gap type. Kept as context (gap_type mapped to NO_CLEAR_GAP in output).'),
    ])

T['EDU-NAT-00'] = dict(
    topic='Natural diamonds: how they form, where they come from, mining & processing',
    primary=['how are diamonds formed'], variants=['how are diamonds created', 'how are diamonds made', 'how diamond created', 'how diamond made', 'how is diamond formed', 'how do diamonds form', 'how does diamond form', 'diamond formation', 'natural diamond formation'],
    head='how are diamonds formed / made / created (12,100 each; same need)', pconf='MEDIUM', core=['CL-075', 'CL-074'],
    why='The formation question family is the clear head need of CL-075, with an unambiguous informational question form. "how are diamonds made" may also draw lab-grown process intent. That is a POSSIBLE_OVERLAP with EDU-LG-00/LG-04 and is not validated.',
    status='FUTURE_PAGE', covered=None, content_note='No existing page (PROPOSED_PROVISIONAL, URL_PENDING).',
    concepts=[
        ('Natural formation: carbon under heat and pressure in the mantle', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'form|created|made|pressure|makes'),
        ('Kimberlite pipes (volcanic transport)', 'PRIMARY_CONCEPT', 'PROCESS', r'pipe'),
        ('Mining and extraction', 'SUPPORTING_CONCEPT', 'PROCESS', r'extract|mining'),
        ('Processing stages (rough to polished)', 'SUPPORTING_CONCEPT', 'PROCESS', r'processed|processing'),
        ('Rough / raw / unpolished diamonds', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'rough|\braw\b|unpolished'),
        ('Natural untreated diamonds', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'untreated'),
        ('Diamond sources / origin', 'SUPPORTING_CONCEPT', 'CONTEXT', r'source'),
        ('Controlled metamorphosis (term)', 'OPTIONAL_CONTEXT', 'CONTEXT', r'metamorphosis'),
        ('Are white diamonds real', 'OPTIONAL_CONTEXT', 'CONTEXT', r'white diamonds'),
    ],
    gaps=[
        ('NO_CONTENT', 'CL-074; CL-075', 'No HOD page covers natural formation or origin (6 × 12,100 variants, plus pipes/mining).', r'.', 'MEDIUM', 'MEDIUM', 'Commercial natural hub deferred (Stage 12 business question 1).'),
        ('MISSING_COMPARISON', 'CL-075; CL-015', '"how are diamonds made" (12,100) can mean natural formation or lab growth. The page should state the natural/lab distinction and link to lab-grown process content.', r'made|created', 'LOW', 'MEDIUM', 'Not SERP-validated. POSSIBLE_OVERLAP recorded in relationships.'),
    ])

T['EDU-4C-00'] = dict(
    topic='The 4Cs / diamond grading scales overview (incl. how lab-grown diamonds are graded)',
    primary=['diamond grading scale'], variants=['diamond grading chart', 'grading system for diamonds', 'diamond classification chart', 'diamond quality scale', '4cs of diamond grading'],
    head='grading system for diamonds (8,100). A "4cs" head term is absent from the Stage 7 universe; "4cs of diamond grading" = 10.', pconf='LOW', core=['CL-040', 'CL-023'],
    why='The grading-scale/chart family is the head need of the pillar (4 × 4,400–8,100) and matches its function. The "4Cs" head term is missing from Stage 7, so the most obvious candidate cannot be evaluated. None validated. Possible overlap with EDU-4C-01 "diamond clarity grading scale" (validated UNCLEAR).',
    status='WEAK_EXISTING_CONTENT', covered=r'4cs|clarity|\blab\b|quality of lab|lab grown diamonds quality',
    content_note='Existing /blog/the-4cs-of-lab-grown-diamonds-explained (H1 "The 4Cs of Lab-Grown Diamonds Explained: How to Choose the Perfect Diamond"). No Stage 3 ranking. Framed for lab-grown, while the owned head terms are general grading scales. Body not audited.',
    concepts=[
        ('The 4Cs framework (cut, colour, clarity, carat)', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'4cs|characteristics|categories|classification|grading system|quality measurement'),
        ('Diamond grading charts and scales', 'PRIMARY_CONCEPT', 'FORMAT', r'chart|scale|grades|ratings'),
        ('How lab-grown diamonds are graded (same scales)', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'\blab\b'),
        ('Colour–clarity grade combinations (e.g. G/VS, F VS2)', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', ('cluster', 'CL-048')),
        ('Flawless lab-grown diamonds', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'flawless'),
        ('Grading laboratories (GIA, IGI)', 'RELATED_ENTITY', 'ENTITY', r'\bgia\b|\bigi\b'),
    ],
    gaps=[
        ('MISSING_SUBTOPIC', 'CL-040', 'Owned head terms are general (grading system for diamonds 8,100; diamond grading chart/scale 4,400 each; classification chart 4,400), but the existing article is framed as "4Cs of lab-grown diamonds". The general grading-scale framing is not evident from the title.', r'grading|chart|scale|classification|characteristics|categories', 'MEDIUM', 'HIGH', 'Stage 14 decided the pillar integrates lab-grown grading.'),
        ('MISSING_ENTITY', 'CL-048', 'Colour–clarity combination queries (is f vs2 a good diamond 140; g/vs; gh si …) have no dedicated treatment. They are FAQ-scale and sit here per Stage 15.', ('cluster', 'CL-048'), 'LOW', 'MEDIUM', 'Grouping in the question map avoids FAQ spam.'),
        ('KEYWORD_UNIVERSE_GAP', 'CL-040', '"4cs of diamonds" / "diamond 4cs" style head terms are absent from the Stage 7 master DB (only "4cs of diamond grading" = 10), so the pillar\'s most natural primary cannot be measured.', r'4cs', 'HIGH', 'HIGH', 'Data gap, not a content gap. Mapped to MISSING_SUBTOPIC in output with this note. Optional paid supplement listed in the Stage 17 summary.'),
    ])

T['EDU-4C-01'] = dict(
    topic='Diamond clarity guide: scale, inclusions, eye-clean, grade comparisons, best clarity to buy',
    primary=['diamond clarity grading scale', 'what is the best clarity for a diamond'],
    variants=['diamond grading and clarity', 'diamond clarity types', 'diamond clarity comparison', 'which is the best diamond clarity'],
    head='diamond clarity grading scale (12,100)', pconf='MEDIUM', core=['CL-044', 'CL-045', 'CL-046'],
    why='The highest-demand member directly names the page subject. Stage 8 validated it, but as UNCLEAR/OTHER (GIA 4cs site, Tiffany, Wikipedia), so the SERP format is reference/chart-led rather than a clear editorial pattern. Co-primary "best clarity" (1,900) carries the buying-decision need.',
    status='FUTURE_PAGE', covered=None, content_note='No dedicated page. The existing 4Cs-of-lab-grown article covers clarity at overview level (Stage 10 topic string).',
    concepts=[
        ('Clarity grading scale (FL to I3)', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'clarity (grading )?scale|clarity types|grading and clarity|chart|clarity comparison'),
        ('Inclusions and blemishes', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'inclusion|imperfection|graining|clarity characteristics'),
        ('Best clarity to buy / does clarity matter', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'best clarity|best diamond clarity|what clarity|clarity matter|clarity really matter|good clarity'),
        ('Eye-clean', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'eye.?clean'),
        ('VS1 / VS2 grades (interim home; VS page conditional)', 'SUPPORTING_CONCEPT', 'SUBTOPIC', r'\bvs1\b|\bvs2\b|vs clarity|vs diamond clarity|vs diamond quality|vs diamond chart'),
        ('Clarity grade comparisons (VS vs SI, VVS vs VS)', 'PRIMARY_CONCEPT', 'COMPARISON_PARTNER', r'si vs vs|vs and vvs|vvs vs|vvs.vs|vs or|diamond vs si|difference between|si diamond vs|better vs|clarity vs'),
        ('Lab-grown diamond clarity and inclusions', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'\blab'),
        ('GIA clarity chart', 'RELATED_ENTITY', 'ENTITY', r'\bgia\b'),
        ('Clarity vs carat trade-off', 'SUPPORTING_CONCEPT', 'CONTEXT', r'bigger diamond or more clarity'),
        ('Lowest clarity grades (I1–I3)', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'lowest quality|best to worst'),
    ],
    gaps=[
        ('NO_CONTENT', 'CL-040; CL-042; CL-044; CL-045; CL-046', 'No dedicated clarity page. The clarity family (12,100 head plus comparisons and inclusions) is proposed only.', r'.', 'MEDIUM', 'HIGH', ''),
        ('MISSING_SERP_FORMAT', 'CL-040', 'The validated head SERP is UNCLEAR/OTHER, led by reference/chart pages (4cs.gia.edu, Wikipedia, Tiffany). A visual clarity chart is likely part of the expected format. This is an inference from page types, not a measured feature.', r'scale|chart', 'MEDIUM', 'HIGH', 'Images feature not present on this SERP (Stage 8), so the chart inference is LOW-MEDIUM.'),
        ('MISSING_COMPARISON', 'CL-044', 'Grade comparison queries (VS vs SI, VVS vs VS, VS1 vs VS2) are numerous (14 in CL-044) and each small.', r'\bvs\b|\bor\b|difference', 'MEDIUM', 'MEDIUM', 'Keyword "vs" is ambiguous (the VS grade vs "versus"). See keyword_relationships.'),
    ])

T['EDU-4C-02'] = dict(
    topic='SI clarity grades (SI1, SI2, SI3): what they mean, are they good',
    primary=['si2 diamond clarity'], variants=['si2 diamond', 'si2 diamond quality'], head='si2 diamond clarity (1,300)', pconf='HIGH', core=['CL-041'],
    why='Both heads are validated INFORMATIONAL/EDITORIAL_GUIDE (HIGH and MEDIUM). "si clarity diamonds" style generic head is not in Stage 7, so SI2 leads.',
    status='FUTURE_PAGE', covered=None, content_note='No existing page.',
    concepts=[
        ('SI1, SI2, SI3 grades', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'\bsi[123]?\b'),
        ('Is an SI diamond good / eye-clean SI', 'PRIMARY_CONCEPT', 'ATTRIBUTE', r'good|quality'),
        ('SI vs VS comparisons', 'SUPPORTING_CONCEPT', 'COMPARISON_PARTNER', r'\bvs\b|\bvs1\b|vvs'),
        ('SI value / price context (no live prices)', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'worth|price|value'),
        ('SI3 (non-GIA grade)', 'RELATED_ENTITY', 'ENTITY', r'si3'),
        ('I1 boundary', 'OPTIONAL_CONTEXT', 'CONTEXT', r'\bi1\b|lowest quality'),
    ],
    gaps=[
        ('NO_CONTENT', 'CL-041', 'No HOD page covers SI grades. Both validated SERPs are editorial guides with AI Overview + PAA + Shopping.', r'.', 'HIGH', 'HIGH', 'Validated evidence.'),
    ])

T['EDU-4C-03'] = dict(
    topic='VVS, IF & flawless clarity grades (incl. VVS in lab-grown)',
    primary=['v v s diamond'], variants=['vvs diamonds vs regular'], head='v v s diamond (18,100; DataForSEO\'s spacing of "vvs diamond")', pconf='HIGH', core=['CL-043'],
    why='Validated INFORMATIONAL/EDITORIAL_GUIDE (HIGH). This is how Stage 7 records the VVS head term.',
    status='FUTURE_PAGE', covered=None, content_note='No existing page.',
    concepts=[
        ('VVS1 / VVS2 grades', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'vvs|v v s'),
        ('IF and FL (flawless) grades', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'\bif\b|flawless|\bfl\b'),
        ('VVS lab-grown diamonds', 'PRIMARY_CONCEPT', 'SUBTOPIC', r'\blab'),
        ('VVS vs regular / VS diamonds', 'SUPPORTING_CONCEPT', 'COMPARISON_PARTNER', r'regular|better, vvs or vs|vvs diamonds vs diamonds'),
        ('What VVS means', 'SUPPORTING_CONCEPT', 'CONTEXT', r'mean'),
        ('VVS price context (no live prices)', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'price|expensive|how much'),
        ('VVS in jewellery (chains, earrings, rings)', 'OPTIONAL_CONTEXT', 'CONTEXT', r'chain|earring|ring'),
    ],
    gaps=[
        ('NO_CONTENT', 'CL-043; CL-023', 'No HOD page covers VVS/IF/FL (18,100 head, validated editorial SERP with AI Overview + PAA + Shopping).', r'.', 'HIGH', 'HIGH', ''),
        ('MISSING_SUBTOPIC', 'CL-023', 'VVS in lab-grown (vvs lab diamonds 320; are vvs diamonds lab grown 90 ×2) is a distinct sub-need. Related searches also show "Vvs diamonds lab grown".', r'\blab', 'MEDIUM', 'MEDIUM', 'DataForSEO TRANSACTIONAL labels on "vvs lab diamonds" are unvalidated.'),
    ])

T['EDU-4C-05'] = dict(
    topic='Diamond colour guide: D-to-Z scale, colourless / near-colourless, grade comparisons',
    primary=['color grade diamond', 'colorless diamond'], variants=['d-f diamond', 'ef quality diamond'],
    head='colorless diamond (3,600). "diamond color chart" appears only as a Stage 8 related search and is not in Stage 7.', pconf='LOW', core=['CL-047'],
    why='"color grade diamond" names the page need but has no volume (NOT_AVAILABLE). "colorless diamond" is the highest-demand member but covers only D–F. Only a 10-volume member is validated. The general colour head terms are missing from Stage 7.',
    status='FUTURE_PAGE', covered=None, content_note='No dedicated page. The 4Cs-of-lab-grown article covers colour at overview level.',
    concepts=[
        ('D-to-Z colour scale', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'colou?r grade|letter|colou?r chart|best to worst'),
        ('Colourless grades (D–F)', 'PRIMARY_CONCEPT', 'ATTRIBUTE', r'colorless|d-f|^d diamond|ef quality|\bd vs\b|\be vs f\b|\bd vs e\b'),
        ('Near-colourless grades (G–J)', 'PRIMARY_CONCEPT', 'ATTRIBUTE', r'g.?h|diamond j|\bh vs i\b'),
        ('Faint colour (K and below)', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'diamond k|k-diamonds'),
        ('Colour grade comparisons (D vs E, G vs H …)', 'SUPPORTING_CONCEPT', 'COMPARISON_PARTNER', r'^[d-k] vs [d-k] diamond$|fg vs gh|which diamond is better, gh or fg'),
        ('Best colour to buy / is G-H good', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'good|best'),
    ],
    gaps=[
        ('NO_CONTENT', 'CL-047', 'No dedicated colour page. The D-to-Z scale family is proposed only.', r'.', 'MEDIUM', 'HIGH', ''),
        ('KEYWORD_UNIVERSE_GAP', 'CL-047', 'The general colour heads ("diamond color chart", "diamond color scale") are absent from Stage 7. "Diamond color chart" appears only as a related search on the clarity SERP. The primary has no volume.', r'colou?r', 'HIGH', 'HIGH', 'Data gap. Mapped to MISSING_SUBTOPIC in output with this note.'),
        ('MISSING_COMPARISON', 'CL-047; CL-048', 'Several CL-047 keywords ("f vs diamond", "g vs diamond", "g-h vs diamond", "f-g vs diamond", "d vs diamond") may mean colour + VS clarity combinations, not "versus". The interpretation is ambiguous. Possible overlap with CL-048 at EDU-4C-00.', r'^([d-k](-[d-k])?|[d-k]{2}) vs diamond$', 'LOW', 'MEDIUM', 'Ownership unchanged (Stage 15). Flagged only.'),
    ])

T['EDU-4C-06'] = dict(
    topic='Diamond cut guide: cut grades, facets, light performance',
    primary=['diamond cut grade'], variants=['what is a good cut for a diamond', 'is ideal cut diamond good'], head='diamond facet (1,000; DataForSEO TRANSACTIONAL label, unvalidated)', pconf='MEDIUM', core=['CL-050'],
    why='"diamond cut grade" is validated INFORMATIONAL/EDITORIAL_GUIDE (HIGH) and names the page need exactly, but Stage 7 has no volume for it. "diamond facet" has more volume but is a CL-088 optics subtopic with a doubtful TRANSACTIONAL label.',
    status='FUTURE_PAGE', covered=None, content_note='No dedicated page. The 4Cs-of-lab-grown article covers cut at overview level.',
    concepts=[
        ('Cut grade scale (Excellent/Ideal, Very Good, Good …)', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'cut grade|ideal|very good|standard cut|good cut|poor cut|super ideal'),
        ('Facets and diamond surfaces', 'PRIMARY_CONCEPT', 'ATTRIBUTE', r'facet|surfaces'),
        ('Light performance: refraction and sparkle', 'PRIMARY_CONCEPT', 'ATTRIBUTE', r'refraction|sparkle'),
        ('Brilliant cut', 'SUPPORTING_CONCEPT', 'ENTITY', r'brilliant'),
        ('Cut grade vs shape (disambiguation)', 'SUPPORTING_CONCEPT', 'CONTEXT', r'best cut for a diamond ring|cheapest|types of diamond cuts'),
        ('Does cut matter', 'SUPPORTING_CONCEPT', 'CONTEXT', r'matter'),
        ('Cut grading by GIA / IGI', 'RELATED_ENTITY', 'ENTITY', r'\bgia\b|\bigi\b'),
    ],
    gaps=[
        ('NO_CONTENT', 'CL-050; CL-088', 'No dedicated cut page. The validated editorial SERP has AI Overview + PAA.', r'.', 'MEDIUM', 'HIGH', ''),
        ('MISSING_ENTITY', 'CL-050', 'Queries mix cut grade and shape ("best cut for a diamond ring", PAA "which diamond cut is the cheapest", related "types of diamond cuts brilliant"). The page needs a cut-vs-shape disambiguation that links to EDU-SHP-00.', r'best cut|cheapest', 'MEDIUM', 'MEDIUM', 'Stage 14 split Shapes & Cuts. Cut grade belongs here.'),
        ('KEYWORD_UNIVERSE_GAP', 'CL-050', 'The primary "diamond cut grade" has no volume in Stage 7 (NOT_AVAILABLE), and "diamond cut" is absent.', r'cut grade', 'HIGH', 'MEDIUM', 'Data gap. Mapped to MISSING_SUBTOPIC in output with this note.'),
    ])

T['EDU-4C-07'] = dict(
    topic='Diamond carat guide: weight vs size, "is X carat good / big enough", ct vs ctw',
    primary=['is 1 carat diamond good'], variants=['is a 1 carat diamond a good size'], head='No carat head term in Stage 7 ("diamond carat" / "carat weight" absent)', pconf='LOW', core=['CL-049'],
    why='CL-049 is a long list of "is N carat good / too big" questions. The 1-carat form is the largest and most representative. The real head terms are missing from Stage 7, and nothing is validated.',
    status='FUTURE_PAGE', covered=None, content_note='No dedicated page.',
    concepts=[
        ('Carat weight (and weight vs visual size)', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'carat|\bct\b'),
        ('Is N carat good / big enough (size perception)', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'too big|too small|big enough|good size|good\b'),
        ('Carat (ct) vs total carat weight (ctw)', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'ctw|ct tw'),
        ('Carat sizes for stud earrings', 'SUPPORTING_CONCEPT', 'SUBTOPIC', r'earring'),
        ('Fractional carat weights (1/2, 1/3, 1/4 …)', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'\d/\d|half'),
        ('Flashiness / social perception of large stones', 'OPTIONAL_CONTEXT', 'CONTEXT', r'flashy'),
    ],
    gaps=[
        ('NO_CONTENT', 'CL-049', 'No carat page exists.', r'.', 'MEDIUM', 'MEDIUM', 'Provisional topic.'),
        ('KEYWORD_UNIVERSE_GAP', 'CL-049', 'Carat head terms ("diamond carat", "carat size chart", "carat weight") are absent from Stage 7, which holds only question-form long tail.', r'carat', 'HIGH', 'HIGH', 'Data gap. Mapped to MISSING_SUBTOPIC in output with this note.'),
        ('MISSING_QUESTION', 'CL-049', 'About 36 "is N carat good/too big/too small" variants collapse to 3 question patterns. They should be answered as one size-perception section, not as 36 FAQs.', r'^is ', 'MEDIUM', 'MEDIUM', 'Anti-FAQ-spam grouping applied in 17_question_map.'),
    ])

T['EDU-SHP-00'] = dict(
    topic='Diamond shapes guide (overview + choosing a shape for an engagement ring)',
    primary=['diamond shape', 'what shape diamond should i get'], variants=[], head='diamond shape (60,500)', pconf='MEDIUM', core=['CL-060', 'CL-064'],
    why='"diamond shape" is validated INFORMATIONAL/EDITORIAL_GUIDE (HIGH; GIA 4cs, Brilliant Earth). However, its PAA questions are about the geometric shape ("rhombus or kite", "another word for a diamond shape"), so part of the 60,500 demand is not jewellery. Co-primary "what shape diamond should i get" carries the engagement-ring choice need.',
    status='WEAK_EXISTING_CONTENT', covered=r'shape|should i get',
    content_note='Existing /blog/the-best-lab-grown-diamond-shapes-for-engagement-rings (H1 "Diamond Shapes Guide: Which Lab-Grown Diamond Shape Is Right for You?"). No Stage 3 ranking. Framed for engagement rings and lab-grown.',
    concepts=[
        ('Diamond shapes overview (round, oval, princess, emerald, radiant, asscher, marquise …)', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'shape'),
        ('Choosing a shape for an engagement ring', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'should i get|engagement|ring'),
        ('Radiant cut', 'SUPPORTING_CONCEPT', 'ENTITY', r'radiant'),
        ('Asscher vs emerald cut', 'SUPPORTING_CONCEPT', 'COMPARISON_PARTNER', r'asscher|emerald'),
        ('Princess cut', 'SUPPORTING_CONCEPT', 'ENTITY', r'princess'),
        ('Length-to-width ratio', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'ratio'),
        ('Sparkle by shape', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'sparkle'),
        ('Price differences by shape', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'expensive'),
        ('Marquise vs oval', 'OPTIONAL_CONTEXT', 'COMPARISON_PARTNER', r'marquise'),
        ('Geometric "diamond shape" meaning (non-jewellery intent in the SERP)', 'OPTIONAL_CONTEXT', 'DISAMBIGUATION', r'rhombus|kite|another word|drawing|shape face|shape called|what is the diamond shape'),
    ],
    gaps=[
        ('MISSING_SUBTOPIC', 'CL-060; CL-061; CL-062', 'Owned keywords include a general shapes overview (diamond shape 60,500) and specific shapes (radiant 3,600; asscher vs emerald 390). The existing article is framed as engagement-ring shape choice for lab-grown. Radiant/asscher/emerald coverage is not evident from the title.', r'radiant|asscher|emerald|princess', 'MEDIUM', 'HIGH', 'Per-shape pages DEFERRED (Stage 14). Shape detail stays in the pillar.'),
        ('MISSING_SERP_FORMAT', 'CL-060', 'The head SERP mixes jewellery guides (GIA, Brilliant Earth) with geometric intent (PAA "Is a diamond a rhombus or a kite?"; related "Diamond shape face", "Diamond shapes drawing"). Realistic demand for the page is below the raw 60,500.', r'^diamond shape$', 'HIGH', 'HIGH', 'Direct Stage 8 PAA/related evidence.'),
        ('KEYWORD_UNIVERSE_GAP', 'CL-060', '"diamond shapes" (plural) and "diamond shapes chart" are absent from Stage 7.', r'shape', 'MEDIUM', 'MEDIUM', 'Data gap. Mapped to MISSING_SUBTOPIC in output with this note.'),
    ])

T['EDU-CERT-00'] = dict(
    topic='Diamond certification explained (lab-grown focus; GIA, IGI, grading reports, verification)',
    primary=['lab-grown diamond certification'], variants=['lab grown diamond certification', 'lab grown diamond grading', 'lab grown diamonds grading', 'lab-grown diamond grading', 'lab diamond grading', 'grading lab grown diamonds'],
    head='gia lab diamonds (2,400; DataForSEO TRANSACTIONAL, unvalidated) and diamond grading report (1,600; interim home)', pconf='HIGH', core=['CL-033', 'CL-031', 'CL-032'],
    why='"lab-grown diamond certification" (hyphenated form; the unhyphenated twin has the same 390 volume) is validated INFORMATIONAL/EDITORIAL_GUIDE (HIGH), with IGI and GIA pages in the top 5. It matches the retarget decision (Stage 13 RETARGET to CL-033). Higher-volume entity heads (gia lab diamonds) carry unvalidated TRANSACTIONAL labels.',
    status='WEAK_EXISTING_CONTENT', covered=r'\bigi\b',
    content_note='Existing /blog/igi-certification-for-lab-grown-diamonds (H1 "IGI Certification Explained …"). Stage 13 RETARGET then move. No Stage 3 ranking. IGI-only framing today.',
    concepts=[
        ('Diamond certification / grading reports', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'certif|report|certificate'),
        ('Lab-grown grading reports', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'\blab'),
        ('GIA (incl. its lab-grown reports)', 'RELATED_ENTITY', 'ENTITY', r'\bgia\b'),
        ('IGI', 'RELATED_ENTITY', 'ENTITY', r'\bigi\b'),
        ('Grading laboratories in general', 'SUPPORTING_CONCEPT', 'ENTITY', r'grading lab|laboratory'),
        ('Report verification / lookup / serial number', 'SUPPORTING_CONCEPT', 'PROCESS', r'check|lookup|serial'),
        ('Appraisal vs grading report', 'SUPPORTING_CONCEPT', 'COMPARISON_PARTNER', r'appraisal'),
        ('Grading scales on reports', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'scale|chart'),
        ('GIA natural diamond reports', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'natural'),
        ('Certification cost', 'OPTIONAL_CONTEXT', 'ATTRIBUTE', r'price'),
    ],
    gaps=[
        ('MISSING_SUBTOPIC', 'CL-031', 'GIA lab-grown questions (gia lab diamonds 2,400; does gia certify lab grown diamonds 320; are lab grown diamonds gia certified 140 ×2) are owned here. The existing IGI-framed article title does not address GIA.', r'\bgia\b', 'MEDIUM', 'HIGH', 'Retarget to CL-033 general certification (Stage 13/14).'),
        ('MISSING_QUESTION', 'CL-033', 'Certification basics questions (are lab grown diamonds certified; do lab-grown diamonds come with a certificate; report check) plus validated PAA ("Do lab-grown diamonds get a certificate?", "Does GIA still certify lab-grown diamonds?").', r'certified|certificate|graded|check', 'HIGH', 'HIGH', 'Validated SERP + PAA.'),
        ('MISSING_SUBTOPIC', 'CL-034', 'Generic report queries (diamond grading report 1,600; diamond grading lab 170) are interim-homed here while EDU-CERT-02 (how to read a report) is CONDITIONAL.', r'report|grading lab', 'MEDIUM', 'MEDIUM', ''),
    ])

T['EDU-CERT-01'] = dict(
    topic='GIA vs IGI (and other labs) certificate comparison',
    primary=['gia vs igi lab diamond'], variants=['gia vs igi diamond', 'igi certified diamonds vs gia'], head='gia vs igi lab diamond (140)', pconf='HIGH', core=['CL-030'],
    why='Validated INFORMATIONAL/EDITORIAL_GUIDE (HIGH). Exact match to the existing Education article.',
    status='WEAK_EXISTING_CONTENT', covered=r'\bgia\b|\bigi\b|report',
    content_note='Existing /education/lab-grown-diamond-certification-explained-gia-vs-igi (H1 "GIA vs IGI: What Your Lab-Grown Diamond Report Actually Tells You"). Kept in place. No Stage 3 ranking.',
    concepts=[
        ('GIA vs IGI', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'\bgia\b|\bigi\b'),
        ('Which certificate is best', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'best|better'),
        ('Other labs: AGS, EGL, GSI, GCAL', 'RELATED_ENTITY', 'ENTITY', r'\bags\b|\begl\b|\bgsi\b|gcal'),
        ('Why IGI costs less than GIA', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'cheaper|cost'),
        ('Different diamond certifications', 'SUPPORTING_CONCEPT', 'CONTEXT', r'different'),
    ],
    gaps=[
        ('MISSING_COMPARISON', 'CL-030', 'Other-lab comparisons (gia vs ags, gia vs gsi, is egl a good certificate; related "GIA vs IGI vs GCAL") are not evident from the GIA-vs-IGI title.', r'\bags\b|\begl\b|\bgsi\b|different|best', 'MEDIUM', 'MEDIUM', 'Low volume (10–30 each).'),
        ('MISSING_AEO_COVERAGE', 'CL-030', 'The validated SERP has AI Overview + PAA ("Why is IGI so much cheaper than GIA?", "Which is best, IGI or GIA?"). HOD has no ranking.', r'\bgia\b', 'MEDIUM', 'HIGH', ''),
    ])

T['EDU-MET-00'] = dict(
    topic='Jewellery metals guide: types, best metal for rings/wedding bands, hypoallergenic, mixing, plating',
    primary=['types of jewelry metals', 'best metal for rings'], variants=['types of metals for rings', 'jewelry alloys', 'diamond metals'],
    head='rhodium ring (1,000; interim home, validated UNCLEAR/OTHER)', pconf='MEDIUM', core=['CL-112', 'CL-113'],
    why='The pillar need (metal types, best metal) is expressed by CL-112 terms (590 / 210), which are unvalidated. Validated members are sub-questions (tungsten/titanium wedding bands, rhodium plating, mixing metals) with EDITORIAL_GUIDE SERPs.',
    status='FUTURE_PAGE', covered=None, content_note='No existing page (PROPOSED_PROVISIONAL, URL_PENDING). The 14k-vs-18k article (EDU-MET-01) covers gold karat only.',
    concepts=[
        ('Types of jewellery metals and alloys', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'types?|metals|alloys'),
        ('Best metal for rings / wedding bands', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'best metal|good for wedding|metal is best'),
        ('Hypoallergenic metals', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'hypoallergenic'),
        ('Rhodium plating and replating (interim; EDU-MET-02 conditional)', 'SUPPORTING_CONCEPT', 'SUBTOPIC', r'rhodium|replat|dip'),
        ('Tungsten', 'RELATED_ENTITY', 'ENTITY', r'tungsten'),
        ('Titanium', 'RELATED_ENTITY', 'ENTITY', r'titanium'),
        ('Sterling silver (925)', 'RELATED_ENTITY', 'ENTITY', r'silver|925'),
        ('Rose gold', 'RELATED_ENTITY', 'ENTITY', r'rose gold'),
        ('Mixing metals (gold with silver)', 'SUPPORTING_CONCEPT', 'CONTEXT', r'with gold|mix|together'),
        ('White gold / yellow gold conversion', 'SUPPORTING_CONCEPT', 'CONTEXT', r'white gold'),
        ('Iridium', 'OPTIONAL_CONTEXT', 'ENTITY', r'iridium'),
    ],
    gaps=[
        ('NO_CONTENT', 'CL-111; CL-112; CL-113', 'No metals pillar. Five validated sub-questions (tungsten, titanium, rhodium plating, silver-with-gold: EDITORIAL_GUIDE; rhodium ring: OTHER).', r'.', 'MEDIUM', 'HIGH', ''),
        ('MISSING_COMMERCIAL_CONTEXT', 'CL-113', 'Tungsten/titanium wedding-band questions are validated editorial, but there is no catalogue evidence that HOD sells these metals (Stage 15 business dependency). The guide can explain them, but cannot point to HOD products.', r'tungsten|titanium|iridium', 'MEDIUM', 'MEDIUM', 'Business input required.'),
        ('KEYWORD_UNIVERSE_GAP', 'CL-112', 'Platinum and white-gold head terms ("platinum vs white gold", "white gold") are absent from Stage 7 (only noise/review "platinum" rows).', r'gold|platinum', 'HIGH', 'MEDIUM', 'Data gap. Mapped to MISSING_SUBTOPIC in output with this note.'),
    ])

T['EDU-MET-01'] = dict(
    topic='14k vs 18k gold (and 10k): karat comparison for diamond jewellery',
    primary=['is 18k gold or 14k gold better'], variants=['which one is better 14k or 18k gold'], head='"14k vs 18k gold" is absent from Stage 7. Largest owned = is a 10k gold ring worth anything (50).', pconf='MEDIUM', core=['CL-110'],
    why='Validated INFORMATIONAL/EDITORIAL_GUIDE (HIGH). Protected ranking (95). Closest owned expression of the page\'s comparison need, since the real head "14k vs 18k gold" is missing from Stage 7.',
    status='WEAK_EXISTING_CONTENT', covered=r'14k|18k',
    content_note='Existing /blog/14k-vs-18k-gold-for-diamond-jewellery (H1 "14K vs 18K Gold: Which Gold Is Best for Your Engagement Ring?"). Ranks 81, 84 and 95 (protected). Stage 13 MOVE_TO_EDUCATION when conditions are met.',
    concepts=[
        ('Gold karat: 10k, 14k, 18k (purity)', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'\b1[048]k\b|karat'),
        ('Which karat is better', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'better|best|worth getting'),
        ('Durability for daily wear (softness)', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'daily|soft|lasts'),
        ('Value / resale of gold by karat', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'worth|value|selling'),
        ('Karat vs carat confusion ("14k diamond")', 'SUPPORTING_CONCEPT', 'DISAMBIGUATION', r'14k diamond|14 carat|14k diamonds'),
        ('Engagement ring metal choice', 'SUPPORTING_CONCEPT', 'CONTEXT', r'engagement'),
        ('22k / 24k context', 'OPTIONAL_CONTEXT', 'CONTEXT', r'24k|22k'),
    ],
    gaps=[
        ('MISSING_SUBTOPIC', 'CL-110', '10k gold ("is a 10k gold ring worth anything", validated HIGH; PAA "Is 10K gold considered cheap?") is owned here, but the title covers only 14K vs 18K.', r'10k', 'MEDIUM', 'MEDIUM', ''),
        ('MISSING_QUESTION', 'CL-110', 'Validated PAA across four SERPs: daily-wear durability, "is 18K too soft", resale value by karat, "is 14k gold worth buying".', r'better|good', 'HIGH', 'HIGH', 'Direct Stage 8 PAA.'),
        ('MISSING_ENTITY', 'CL-110', '"is 14k diamond good" (ranking 84) plus PAA "Are 14k diamonds real?" and "How much is a 14 carat diamond worth?" show karat/carat confusion. A clarifying section would serve this ranking keyword.', r'14k diamond', 'MEDIUM', 'MEDIUM', ''),
        ('KEYWORD_UNIVERSE_GAP', 'CL-110', 'The head term "14k vs 18k gold" is absent from Stage 7. Demand for the page\'s main topic is unmeasured.', r'14k|18k', 'HIGH', 'HIGH', 'Data gap. Mapped to MISSING_SUBTOPIC in output with this note.'),
    ])

T['EDU-RJG-01'] = dict(
    topic='Ring settings guide: setting types (prong, bezel, halo, pavé, milgrain …) and choosing one',
    primary=['types of diamond settings'], variants=['different types of diamond settings'], head='types of diamond settings (720)', pconf='HIGH', core=['CL-121'],
    why='Validated INFORMATIONAL/EDITORIAL_GUIDE (HIGH). Exact match to the page need. "milgrain ring" has the same volume but is a detail term with a doubtful TRANSACTIONAL label.',
    status='FUTURE_PAGE', covered=None, content_note='No existing page.',
    concepts=[
        ('Setting types (prong, bezel, halo, pavé, tension/pressure …)', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'setting'),
        ('Milgrain detailing', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'milgrain'),
        ('Halo effect on apparent size', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'halo'),
        ('Pressure / tension setting', 'SUPPORTING_CONCEPT', 'ENTITY', r'pressure'),
        ('High vs low setting profile', 'SUPPORTING_CONCEPT', 'COMPARISON_PARTNER', r'high vs low'),
        ('"Do diamonds need breathing holes" myth', 'SUPPORTING_CONCEPT', 'CONTEXT', r'breathe|breathing'),
        ('Stud earring settings', 'SUPPORTING_CONCEPT', 'SUBTOPIC', r'stud'),
        ('Best setting to show off a diamond', 'SUPPORTING_CONCEPT', 'CONTEXT', r'best setting|setting is best|show off'),
    ],
    gaps=[
        ('NO_CONTENT', 'CL-121; CL-125', 'No settings guide exists. The validated SERP is editorial with AI Overview + PAA.', r'.', 'HIGH', 'HIGH', ''),
        ('KEYWORD_UNIVERSE_GAP', 'CL-121', 'Setting head terms ("engagement ring settings", "prong setting", "bezel setting") are absent from Stage 7.', r'setting', 'HIGH', 'MEDIUM', 'Data gap. Mapped to MISSING_SUBTOPIC in output with this note.'),
    ])

T['EDU-RJG-02'] = dict(
    topic='Ring size guide: finding your size, men\'s vs women\'s sizes, resizing',
    primary=['are mens and womens ring sizes the same'], variants=[], head='No "ring size" head term in Stage 7 (Stage 13 noted "ring size / ring size chart" demand as unmeasured)', pconf='LOW', core=['CL-124'],
    why='All six owned terms are resizing/sizing-difference questions. None is the page\'s natural head ("ring size chart"), which is missing from Stage 7. The selected term has the highest volume among the owned terms and is closest to the sizing need. Nothing is validated.',
    status='WEAK_EXISTING_CONTENT', covered=r'ring size|sizing',
    content_note='Existing /blog/how-to-find-your-ring-size-at-home (H1 "How to Find Your Ring Size at Home: The Complete Ring Sizing Guide"). No Stage 3 ranking. Owned keywords are mostly about resizing, which the title does not name.',
    concepts=[
        ('Men\'s vs women\'s ring sizes', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'mens and womens'),
        ('Ring resizing (up/down; where)', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'resiz|smaller'),
        ('Band thickness and fit', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'thickness'),
        ('Metals that cannot be resized (titanium, stainless steel)', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'titanium|stainless'),
        ('Where to get a ring resized', 'SUPPORTING_CONCEPT', 'CONTEXT', r'where can i'),
    ],
    gaps=[
        ('MISSING_SUBTOPIC', 'CL-124', 'Resizing questions (where can i get my ring resized 1,000; can you make a ring smaller 590; titanium/stainless resizing) are owned here, but the existing title covers measuring at home only.', r'resiz|smaller|cut off', 'MEDIUM', 'MEDIUM', 'HOD resizing policy belongs on FAQ/policy (Stage 15).'),
        ('KEYWORD_UNIVERSE_GAP', 'CL-124', '"ring size chart", "ring size guide" and "how to measure ring size" are absent from Stage 7, so the page\'s main demand is unmeasured (Stage 13 open question).', r'size', 'HIGH', 'HIGH', 'Data gap. Mapped to MISSING_SUBTOPIC in output with this note.'),
    ])

T['EDU-GEN-01'] = dict(
    topic='Diamond properties: composition, crystal structure, hardness & durability, melting point',
    primary=['what are diamonds made of', 'diamond hardness'], variants=['what element are diamonds made of'], head='what are diamonds made of (3,600)', pconf='MEDIUM', core=['CL-080', 'CL-082'],
    why='Composition (3,600) is the largest clear informational head. "diamond hardness" (1,600) is co-primary because durability is the commercially relevant facet (Stage 15 business note). Neither is validated.',
    status='FUTURE_PAGE', covered=None, content_note='No existing page (PROPOSED_PROVISIONAL, URL_PENDING).',
    concepts=[
        ('Carbon composition (element, chemistry)', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'made of|carbon|element|chemical|atomic|molecule|periodic'),
        ('Crystal structure / lattice', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'lattice|crystal|cube|hexagonal'),
        ('Mineral classification', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'mineral'),
        ('Hardness (Mohs) and what is harder than diamond', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'hard|stronger|strong'),
        ('Toughness: chipping, cracking, breaking', 'PRIMARY_CONCEPT', 'ATTRIBUTE', r'break|chip|crack|brittle|smash|destroy|unbreakable'),
        ('Scratching', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'scratch|cut glass'),
        ('Melting / burning point', 'SUPPORTING_CONCEPT', 'ATTRIBUTE', r'melt|boiling|burn|heating'),
        ('Lab-grown durability parity', 'SUPPORTING_CONCEPT', 'COMPARISON_PARTNER', r'\blab'),
        ('Cutting and recutting diamonds', 'SUPPORTING_CONCEPT', 'PROCESS', r'\bcut\b|recut|reshape'),
        ('Lonsdaleite (hexagonal diamond)', 'RELATED_ENTITY', 'ENTITY', r'lonsdaleite|hexagonal'),
        ('Type IIa diamonds', 'RELATED_ENTITY', 'ENTITY', r'\biia\b'),
        ('Graphite (same element, different structure)', 'RELATED_ENTITY', 'COMPARISON_PARTNER', r'graphite'),
        ('Uses of diamonds and general facts', 'OPTIONAL_CONTEXT', 'CONTEXT', r'uses|facts|wiki'),
        ('Engagement-ring stone hardness', 'SUPPORTING_CONCEPT', 'CONTEXT', r'engagement ring stone'),
    ],
    gaps=[
        ('NO_CONTENT', 'CL-080; CL-081; CL-082; CL-083; CL-087', 'No HOD page covers diamond properties (74 owned keywords). The durability questions are the commercially relevant part.', r'.', 'MEDIUM', 'MEDIUM', 'Provisional topic.'),
        ('MISSING_COMPARISON', 'CL-082', 'Lab-grown durability parity questions (are lab grown diamonds as hard as natural 210 ×2; durable; stronger) sit here. They are adjacent to EDU-LG-08 (appearance and durability over time).', r'\blab', 'MEDIUM', 'MEDIUM', 'POSSIBLE_OVERLAP recorded in relationships. Ownership unchanged.'),
    ])

T['COM-ER-SIDESTONE'] = dict(
    topic='Side-stone engagement rings (commercial style subcategory)',
    primary=['side stones engagement rings'], variants=[], head='side stones engagement rings (1,000)', pconf='HIGH', core=['CL-120'],
    why='The only owned term. Validated TRANSACTIONAL/CATEGORY. Protected ranking (104).',
    status='WEAK_EXISTING_CONTENT', covered=r'side stone',
    content_note='Existing /engagement-rings/by-desgin/side-stone-rings. Ranks 104. Template meta description. About 4 product links in server HTML at the Stage 10 check.',
    concepts=[
        ('Side-stone engagement ring style', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'side stone'),
        ('What side stones are called (accent stones)', 'SUPPORTING_CONCEPT', 'CONTEXT', r'called'),
        ('Benefits of side stones / adding side stones', 'SUPPORTING_CONCEPT', 'CONTEXT', r'benefits|add side'),
        ('Centre-shape combinations (oval, round, emerald-cut side stones)', 'OPTIONAL_CONTEXT', 'ATTRIBUTE', r'oval|round|emerald'),
        ('Metal (gold)', 'OPTIONAL_CONTEXT', 'ATTRIBUTE', r'gold'),
        ('Ring enhancer', 'OPTIONAL_CONTEXT', 'ENTITY', r'enhancer'),
    ],
    gaps=[
        ('MISSING_COMMERCIAL_CONTEXT', 'CL-120', 'The SERP is CATEGORY-led (Stage 8) and the HOD page is a category, so the format is aligned. Evidence of thin category content: template meta, about 4 products, position 104.', r'side stone', 'MEDIUM', 'MEDIUM', 'Catalogue depth is a business dependency.'),
        ('MISSING_QUESTION', 'CL-120', 'Validated PAA are definitional ("What is a side stone engagement ring?", "What are the side stones called?"). They are candidates for short category copy, not an FAQ block.', r'side stone', 'MEDIUM', 'LOW', ''),
    ])

T['COM-PDP-OVAL-FLORAL'] = dict(
    topic='Oval marquise side-stone engagement ring (product page)',
    primary=['marquise oval diamond'], variants=[], head='marquise oval diamond (390)', pconf='HIGH', core=['CL-063'],
    why='The only owned term. Validated TRANSACTIONAL/PRODUCT. Protected ranking (90).',
    status='WEAK_EXISTING_CONTENT', covered=r'marquise|oval',
    content_note='Existing /shop/oval-floral-diamond-ring (title "Oval Marquise Side-Stone Engagement Ring"). Ranks 90. Page type aligned with a PRODUCT SERP.',
    concepts=[
        ('Oval centre with marquise side stones', 'PRIMARY_CONCEPT', 'CORE_TOPIC', r'marquise|oval'),
        ('Marquise halo / band variants', 'OPTIONAL_CONTEXT', 'ATTRIBUTE', r'halo|band'),
    ],
    gaps=[
        ('NO_CLEAR_GAP', 'CL-063', 'The PRODUCT SERP format is aligned with the HOD PDP. Aside from the weak position (90), no content gap is evidenced from local data. The URL slug ("oval-floral") differs from the title terms. That is not a URL recommendation.', r'marquise', 'MEDIUM', 'LOW', 'Do not move the URL.'),
    ])

# gap types outside the allowed vocabulary are mapped for output, with the original kept in notes
GAP_ALIAS = {'KEYWORD_UNIVERSE_GAP': 'MISSING_SUBTOPIC', 'POSSIBLE_OVERLAP_NOTE': 'NO_CLEAR_GAP'}
GAP_TYPES = {'NO_CONTENT', 'MISSING_SUBTOPIC', 'MISSING_QUESTION', 'MISSING_COMPARISON', 'MISSING_ENTITY',
             'MISSING_COMMERCIAL_CONTEXT', 'MISSING_AEO_COVERAGE', 'MISSING_SERP_FORMAT', 'NO_CLEAR_GAP'}

# ---------------------------------------------------------------- PAA routing (Stage 8 raw questions)
# question -> (owner target, role, note). role in CORE_ANSWER / SECTION_QUESTION / FAQ_CANDIDATE /
# CATEGORY_COPY_CANDIDATE / EXCLUDE_OFF_TOPIC. Questions not listed and not on a target SERP are not used.
PAA_ROUTE = {
    # lab-grown generic (surfaced on held CL-001 SERPs and on target SERPs)
    'Are lab-grown diamonds actually real diamonds?': ('EDU-LG-01', 'SECTION_QUESTION', ''),
    'Is a lab-grown diamond really a diamond?': ('EDU-LG-01', 'SECTION_QUESTION', ''),
    'Is a lab diamond a real diamond?': ('EDU-LG-01', 'SECTION_QUESTION', ''),
    'Are lab grown diamonds considered fake?': ('EDU-LG-01', 'SECTION_QUESTION', ''),
    'Is it worth buying lab-grown diamonds?': ('EDU-LG-02', 'SECTION_QUESTION', 'Worth-it family (CL-012 interim home).'),
    'Is a lab-grown diamond worth buying?': ('EDU-LG-02', 'SECTION_QUESTION', 'Worth-it family (CL-012 interim home).'),
    'What is the downside of a lab-grown diamond?': ('EDU-LG-02', 'SECTION_QUESTION', 'Downsides family.'),
    'What is the downside of a lab grown diamond?': ('EDU-LG-02', 'SECTION_QUESTION', 'Downsides family.'),
    'What are the downsides of lab grown diamonds?': ('EDU-LG-02', 'SECTION_QUESTION', 'Downsides family.'),
    'What are the downsides of lab-grown diamonds?': ('EDU-LG-02', 'SECTION_QUESTION', 'Downsides family.'),
    'What is the downside of lab diamonds?': ('EDU-LG-02', 'SECTION_QUESTION', 'Downsides family.'),
    'Why avoid lab-grown diamonds?': ('EDU-LG-02', 'FAQ_CANDIDATE', 'Downsides family.'),
    'Are lab diamonds better quality?': ('EDU-LG-02', 'FAQ_CANDIDATE', ''),
    'Are lab diamonds as good as real diamonds?': ('EDU-LG-02', 'SECTION_QUESTION', ''),
    'Is it better to buy a real diamond or a lab-grown diamond?': ('EDU-LG-02', 'CORE_ANSWER', ''),
    'Why do jewelers hate lab-grown diamonds?': ('EDU-LG-02', 'FAQ_CANDIDATE', 'Perception question. Answer factually, without disparaging others.'),
    'Why do jewelers hate lab grown diamonds?': ('EDU-LG-02', 'FAQ_CANDIDATE', 'Perception question. Answer factually, without disparaging others.'),
    'Do rich people buy lab diamonds?': ('EDU-LG-02', 'FAQ_CANDIDATE', 'Perception question. LOW value.'),
    'Do lab diamonds sparkle like real diamonds?': ('EDU-LG-08', 'SECTION_QUESTION', 'Appearance (look/sparkle) owned by EDU-LG-08.'),
    'What is the lifespan of a lab diamond?': ('EDU-LG-08', 'FAQ_CANDIDATE', 'Durability over time.'),
    'Can a jeweler tell if a diamond is lab or natural?': ('EDU-LG-09', 'CORE_ANSWER', 'Identification owner.'),
    'Are lab diamonds worth anything?': ('EDU-LG-05', 'SECTION_QUESTION', 'Value/resale owner.'),
    'How much does it cost to grow a lab-grown diamond?': ('EDU-LG-05', 'FAQ_CANDIDATE', 'Production-cost context. No live figures.'),
    'What is the average price of a 1 carat lab-grown diamond?': ('EDU-LG-05', 'FAQ_CANDIDATE', 'No hard-coded prices (Stage 13).'),
    'How much should I pay for a 1 carat lab diamond?': ('EDU-LG-05', 'FAQ_CANDIDATE', 'No hard-coded prices (Stage 13).'),
    'How much is a 2 carat lab grown diamond worth?': ('EDU-LG-05', 'FAQ_CANDIDATE', 'Surfaced on a deferred CL-006 SERP. No live prices.'),
    'What is the price of a 2 carat lab grown diamond?': ('EDU-LG-05', 'FAQ_CANDIDATE', 'Surfaced on a deferred CL-006 SERP. No live prices.'),
    'Is 2ct lab grown diamond good?': ('EDU-4C-07', 'FAQ_CANDIDATE', 'Carat size-perception family.'),
    'Is 2 carat too flashy?': ('EDU-4C-07', 'FAQ_CANDIDATE', 'Carat size-perception family.'),
    'Is Meghan Markle\'s diamond Lab grown?': ('EDU-LG-02', 'EXCLUDE_OFF_TOPIC', 'Celebrity question.'),
    'Are Costco diamonds natural or lab grown?': ('EDU-LG-02', 'EXCLUDE_OFF_TOPIC', 'Third-party retailer question.'),
    'Who has the highest quality of lab-grown diamonds?': ('EDU-LG-03', 'EXCLUDE_OFF_TOPIC', 'Brand/retailer comparison.'),
    # CVD / HPHT
    'What are the disadvantages of CVD diamonds?': ('EDU-LG-03', 'SECTION_QUESTION', 'Recurs on 8 SERPs.'),
    'Which lab-grown diamond method is best?': ('EDU-LG-03', 'CORE_ANSWER', ''),
    'Which lab grown diamond method is best?': ('EDU-LG-03', 'CORE_ANSWER', ''),
    'Which is better, lab grown diamond, CVD or HPHt?': ('EDU-LG-03', 'CORE_ANSWER', ''),
    'Which is better, lab-grown diamond, CVD or HPHt?': ('EDU-LG-03', 'CORE_ANSWER', ''),
    'Which one is better, CVD or HPHt?': ('EDU-LG-03', 'CORE_ANSWER', ''),
    'Which is better, CVD or HPHT?': ('EDU-LG-03', 'CORE_ANSWER', ''),
    'Which lab diamond is better, CVD or HPHt?': ('EDU-LG-03', 'CORE_ANSWER', ''),
    'Are HPHt or CVD lab diamonds better?': ('EDU-LG-03', 'CORE_ANSWER', ''),
    'Is CVD or HPHT better for lab-grown diamonds?': ('EDU-LG-03', 'CORE_ANSWER', ''),
    'What is the difference in price between CVD and HPHT diamonds?': ('EDU-LG-03', 'SECTION_QUESTION', 'Method-level price comparison. Link to EDU-LG-05 for value.'),
    'Are CVD diamonds worth buying?': ('EDU-LG-03', 'SECTION_QUESTION', ''),
    'Are Hpht diamonds worth anything?': ('EDU-LG-03', 'FAQ_CANDIDATE', 'Method-specific value. Link to EDU-LG-05.'),
    'How much is a 1 carat CVD diamond worth?': ('EDU-LG-03', 'FAQ_CANDIDATE', 'Method-specific value. No live prices. Link to EDU-LG-05.'),
    'Is a CVD diamond a real diamond?': ('EDU-LG-03', 'SECTION_QUESTION', '"are cvd diamonds real" ranks 27 on this URL.'),
    'Are CVD diamonds real or fake?': ('EDU-LG-03', 'SECTION_QUESTION', ''),
    'Are Hpht diamonds real or fake?': ('EDU-LG-03', 'SECTION_QUESTION', ''),
    'Is Hpht a real diamond?': ('EDU-LG-03', 'SECTION_QUESTION', ''),
    'What does "HPHT treated diamond" mean?': ('EDU-LG-03', 'FAQ_CANDIDATE', 'Disambiguate HPHT growth from HPHT treatment. Treatments are at EDU-LG-08.'),
    'Can you tell an Hpht diamond?': ('EDU-LG-03', 'FAQ_CANDIDATE', 'Method identification. Link to EDU-LG-09.'),
    'Will CVD pass a diamond tester?': ('EDU-LG-09', 'SECTION_QUESTION', 'Tester behaviour owned by EDU-LG-09. Surfaced on CVD/HPHT SERPs, so EDU-LG-03 should link to it.'),
    'Can a CVD pass a diamond tester?': ('EDU-LG-09', 'SECTION_QUESTION', 'Tester behaviour owned by EDU-LG-09.'),
    'Will a CVD diamond pass a diamond tester?': ('EDU-LG-09', 'SECTION_QUESTION', 'Tester behaviour owned by EDU-LG-09.'),
    # testers
    'Will a diamond tester work on lab diamonds?': ('EDU-LG-09', 'CORE_ANSWER', ''),
    'What gems will pass a diamond tester?': ('EDU-LG-09', 'SECTION_QUESTION', ''),
    'Do those diamond testers actually work?': ('EDU-LG-09', 'SECTION_QUESTION', ''),
    'Do those diamond testers really work?': ('EDU-LG-09', 'SECTION_QUESTION', ''),
    'Is a diamond tester a real diamond if it beeps?': ('EDU-LG-09', 'FAQ_CANDIDATE', ''),
    'How to do the heat test on a diamond?': ('EDU-LG-09', 'FAQ_CANDIDATE', ''),
    'What is the most reliable lab diamond tester available?': ('EDU-LG-09', 'EXCLUDE_OFF_TOPIC', 'Device shopping. Not HOD business (Stage 12 D-16).'),
    'What is the most accurate diamond tester?': ('EDU-LG-09', 'EXCLUDE_OFF_TOPIC', 'Device shopping. Not HOD business (Stage 12 D-16).'),
    # 4Cs
    'Which is clearer, VS1 or VS2?': ('EDU-4C-01', 'SECTION_QUESTION', 'VS grades interim-homed at EDU-4C-01 (EDU-4C-04 conditional).'),
    'Is VS1 or VS2 better diamond?': ('EDU-4C-01', 'SECTION_QUESTION', 'Surfaced on the cut-grade SERP.'),
    'Is VS1 or VS2 better quality?': ('EDU-4C-01', 'SECTION_QUESTION', 'Surfaced on the settings SERP.'),
    'What is a good clarity grade on a diamond?': ('EDU-4C-01', 'CORE_ANSWER', ''),
    'Is it better to have a bigger diamond or more clarity?': ('EDU-4C-01', 'SECTION_QUESTION', 'Clarity vs carat trade-off. Link to EDU-4C-07.'),
    'What is the lowest quality diamond?': ('EDU-4C-01', 'FAQ_CANDIDATE', ''),
    'What are the worst clarity characteristics of diamonds to avoid?': ('EDU-4C-01', 'SECTION_QUESTION', 'Surfaced on the colour SERP.'),
    'Which diamond is better, VVS or VS?': ('EDU-4C-01', 'SECTION_QUESTION', 'VS-vs-VVS comparisons owned by EDU-4C-01 (Stage 15). Surfaced on the VVS SERP.'),
    'Is F VS1 a good diamond?': ('EDU-4C-00', 'FAQ_CANDIDATE', 'Colour–clarity combinations (CL-048) owned by EDU-4C-00.'),
    'Is SI2 a good diamond?': ('EDU-4C-02', 'CORE_ANSWER', ''),
    'Is SI2 better than VS1?': ('EDU-4C-02', 'SECTION_QUESTION', 'Grade-specific comparison.'),
    'How much is a SI2 diamond worth?': ('EDU-4C-02', 'FAQ_CANDIDATE', 'No live prices.'),
    'Will an SI2 diamond increase in value?': ('EDU-4C-02', 'FAQ_CANDIDATE', ''),
    'What does VVS mean in a diamond?': ('EDU-4C-03', 'CORE_ANSWER', ''),
    'Are VVS diamonds expensive?': ('EDU-4C-03', 'FAQ_CANDIDATE', 'No live prices.'),
    'How much is 1 carat of VVS?': ('EDU-4C-03', 'FAQ_CANDIDATE', 'No live prices.'),
    'Which diamond is better, GH or FG?': ('EDU-4C-05', 'SECTION_QUESTION', ''),
    'Is diamond color grade GH good?': ('EDU-4C-05', 'CORE_ANSWER', ''),
    'What is the best to worst diamond color chart?': ('EDU-4C-05', 'SECTION_QUESTION', 'Chart format signal.'),
    'What is the best cut grade for diamonds?': ('EDU-4C-06', 'CORE_ANSWER', ''),
    'What is a poor cut diamond?': ('EDU-4C-06', 'FAQ_CANDIDATE', ''),
    'Which diamond cut is the cheapest?': ('EDU-4C-06', 'FAQ_CANDIDATE', 'Ambiguous: cut grade or shape. Disambiguate and link to EDU-SHP-00.'),
    # certification
    'Do lab-grown diamonds get a certificate?': ('EDU-CERT-00', 'SECTION_QUESTION', ''),
    'Does GIA still certify lab-grown diamonds?': ('EDU-CERT-00', 'SECTION_QUESTION', 'Time-sensitive fact. Verify at writing time.'),
    'Does GIA still grade lab diamonds?': ('EDU-CERT-00', 'SECTION_QUESTION', 'Time-sensitive fact. Surfaced on the GIA-vs-IGI SERP.'),
    'What is the best certificate for lab-grown diamonds?': ('EDU-CERT-01', 'SECTION_QUESTION', '"which diamond certificate is the best" owned by EDU-CERT-01.'),
    'Is GIA or IGI certification better?': ('EDU-CERT-01', 'CORE_ANSWER', 'Surfaced on the CERT-00 SERP.'),
    'Which is best, IGI or GIA?': ('EDU-CERT-01', 'CORE_ANSWER', ''),
    'Why is IGI so much cheaper than GIA?': ('EDU-CERT-01', 'SECTION_QUESTION', ''),
    'What is the most reputable lab-grown diamond company?': ('EDU-CERT-01', 'EXCLUDE_OFF_TOPIC', 'Brand/retailer question.'),
    # metals
    'Is a rhodium plated ring good?': ('EDU-MET-00', 'SECTION_QUESTION', 'Rhodium interim-homed (EDU-MET-02 conditional).'),
    'How much does it cost to rhodium plate a ring?': ('EDU-MET-00', 'FAQ_CANDIDATE', 'HOD service pricing is policy, not Education.'),
    'How long will a rhodium plated ring last?': ('EDU-MET-00', 'SECTION_QUESTION', ''),
    'What are the downsides of rhodium plating on jewelry?': ('EDU-MET-00', 'FAQ_CANDIDATE', ''),
    'Are rhodium rings good quality?': ('EDU-MET-00', 'FAQ_CANDIDATE', ''),
    'Can you get a solid rhodium ring?': ('EDU-MET-00', 'FAQ_CANDIDATE', ''),
    'Is rhodium expensive jewelry?': ('EDU-MET-00', 'FAQ_CANDIDATE', ''),
    'Is rhodium fake silver?': ('EDU-MET-00', 'FAQ_CANDIDATE', ''),
    'Is there a downside to Tungsten rings?': ('EDU-MET-00', 'SECTION_QUESTION', 'Catalogue dependency (tungsten not evidenced in the catalogue).'),
    'What are the downsides of tungsten?': ('EDU-MET-00', 'SECTION_QUESTION', 'Catalogue dependency.'),
    'Is tungsten better than 925 silver?': ('EDU-MET-00', 'FAQ_CANDIDATE', ''),
    'Can I shower with my tungsten ring on?': ('EDU-MET-00', 'FAQ_CANDIDATE', 'Care topic (EDU-RJG-03 conditional).'),
    'What are the downsides of using titanium wedding bands?': ('EDU-MET-00', 'SECTION_QUESTION', 'Catalogue dependency.'),
    'What type of metal is best for wedding bands?': ('EDU-MET-00', 'CORE_ANSWER', ''),
    'Which is better, 925 silver or titanium?': ('EDU-MET-00', 'FAQ_CANDIDATE', ''),
    'How long will a titanium ring last?': ('EDU-MET-00', 'FAQ_CANDIDATE', ''),
    'Is it okay to wear gold and silver necklaces together?': ('EDU-MET-00', 'SECTION_QUESTION', 'Mixing metals.'),
    'Why are gold and silver not worn together?': ('EDU-MET-00', 'FAQ_CANDIDATE', 'Mixing metals.'),
    'Is it tacky to wear gold and silver at the same time?': ('EDU-MET-00', 'FAQ_CANDIDATE', 'Mixing metals.'),
    'What is the 2:1:1 rule for wearing jewelry?': ('EDU-MET-00', 'EXCLUDE_OFF_TOPIC', 'Styling rule. Blog style territory, not the metals guide.'),
    'Which karat gold is best?': ('EDU-MET-01', 'CORE_ANSWER', ''),
    'Is 18k gold worth more than 14k when selling?': ('EDU-MET-01', 'SECTION_QUESTION', ''),
    'Is 14k gold worth buying?': ('EDU-MET-01', 'SECTION_QUESTION', ''),
    'Is it better to buy 18k or 24k gold?': ('EDU-MET-01', 'FAQ_CANDIDATE', '24k context.'),
    'Is it worth getting 18K gold over 14K?': ('EDU-MET-01', 'CORE_ANSWER', ''),
    'Is 14K gold better for daily wear than 18K gold?': ('EDU-MET-01', 'SECTION_QUESTION', ''),
    'Which lasts longer, 14K or 18K gold?': ('EDU-MET-01', 'SECTION_QUESTION', ''),
    'Is 18K gold too soft for everyday wear?': ('EDU-MET-01', 'SECTION_QUESTION', ''),
    'Are 14k diamonds real?': ('EDU-MET-01', 'SECTION_QUESTION', 'Karat/carat confusion. Serves ranking keyword "is 14k diamond good".'),
    'Is 14k high quality?': ('EDU-MET-01', 'FAQ_CANDIDATE', ''),
    'Which is better, 10k or 14k or 18K?': ('EDU-MET-01', 'SECTION_QUESTION', '10k subtopic.'),
    'Is 10K gold considered cheap?': ('EDU-MET-01', 'FAQ_CANDIDATE', '10k subtopic.'),
    'How much is a 10K gold ring worth today?': ('EDU-MET-01', 'FAQ_CANDIDATE', 'No live metal prices.'),
    'How much is a 14 carat diamond worth?': ('EDU-MET-01', 'EXCLUDE_OFF_TOPIC', 'Karat/carat confusion evidence only. Price question.'),
    'How much does a pawn shop pay for 10K gold?': ('EDU-MET-01', 'EXCLUDE_OFF_TOPIC', 'Scrap/pawn transaction.'),
    'Can I pawn 10K gold?': ('EDU-MET-01', 'EXCLUDE_OFF_TOPIC', 'Scrap/pawn transaction.'),
    # settings
    'What are the different diamond settings?': ('EDU-RJG-01', 'CORE_ANSWER', ''),
    'Which diamond setting is best?': ('EDU-RJG-01', 'SECTION_QUESTION', ''),
    'What is the best setting to show off a diamond?': ('EDU-RJG-01', 'SECTION_QUESTION', ''),
    # shapes
    'Is a marquise diamond more expensive than an oval?': ('EDU-SHP-00', 'FAQ_CANDIDATE', 'Surfaced on the PDP SERP. Shape comparison belongs to the shapes pillar.'),
    'What is a diamond shape called?': ('EDU-SHP-00', 'EXCLUDE_OFF_TOPIC', 'Geometric-shape intent (non-jewellery). Evidence for the SERP-format gap.'),
    'What is the diamond shape?': ('EDU-SHP-00', 'EXCLUDE_OFF_TOPIC', 'Geometric-shape intent (non-jewellery).'),
    "What's another word for a diamond shape?": ('EDU-SHP-00', 'EXCLUDE_OFF_TOPIC', 'Geometric-shape intent (non-jewellery).'),
    'Is a diamond a rhombus or a kite?': ('EDU-SHP-00', 'EXCLUDE_OFF_TOPIC', 'Geometric-shape intent (non-jewellery).'),
    'What cut is Taylor Swift\'s diamond?': ('COM-PDP-OVAL-FLORAL', 'EXCLUDE_OFF_TOPIC', 'Celebrity question.'),
    'What is a divorce ring?': ('COM-PDP-OVAL-FLORAL', 'EXCLUDE_OFF_TOPIC', 'Unrelated.'),
    'What cut is Hailey Bieber\'s engagement ring?': ('COM-PDP-OVAL-FLORAL', 'EXCLUDE_OFF_TOPIC', 'Celebrity question.'),
    # side stones
    'What is a side stone engagement ring?': ('COM-ER-SIDESTONE', 'CATEGORY_COPY_CANDIDATE', 'Short category intro copy. Not an Education article.'),
    'What are the side stones on an engagement ring called?': ('COM-ER-SIDESTONE', 'CATEGORY_COPY_CANDIDATE', ''),
    'What are the benefits of having side stones on an engagement ring?': ('COM-ER-SIDESTONE', 'CATEGORY_COPY_CANDIDATE', ''),
    'Can I add side stones to an engagement ring?': ('COM-ER-SIDESTONE', 'FAQ_CANDIDATE', 'Service question. Depends on HOD bespoke capability (business input).'),
    # natural
    'Is a rough diamond a real diamond?': ('EDU-NAT-00', 'FAQ_CANDIDATE', 'Surfaced on an excluded commercial SERP. Rough/unpolished concept owned here.'),
    'How to identify a raw diamond?': ('EDU-NAT-00', 'FAQ_CANDIDATE', 'Surfaced on an excluded commercial SERP. "raw diamond testing" owned here.'),
}
# Explicitly unused: every PAA from the 'cvd/hpht diamond tester' SERP (special exclusion rule).

# ---------------------------------------------------------------- build deep-dive rows
rank_by_kw = {r['keyword']: r for r in REP15}
target_rows = collections.defaultdict(list)
for r in M15:
    if r['target_id']:
        target_rows[r['target_id']].append(r)

assert set(T) == set(REG15), (set(REG15) ^ set(T))


def held_group(r):
    if r['stage14_topic_id']:
        return r['stage14_topic_id']
    return r['cluster_id']


def row_confidence(r, conflict):
    kw = r['keyword']
    if kw in S8:
        return S8[kw]['validation_confidence']
    if r['mapping_disposition'] == 'REVIEW_REQUIRED':
        return 'INSUFFICIENT_EVIDENCE'
    if r['mapping_disposition'] in ('CONDITIONAL_NOT_MAPPED', 'DEFERRED_NOT_MAPPED'):
        return 'LOW'
    if r['mapping_disposition'].startswith('EXCLUDE'):
        return r['mapping_confidence'] if r['mapping_confidence'] in ('HIGH', 'MEDIUM', 'LOW') else 'LOW'
    if conflict or r['mapping_confidence'] == 'LOW':
        return 'LOW'
    return 'MEDIUM'   # unvalidated keywords are capped at MEDIUM


def intent_reading(r):
    """(reading, basis, conflict_flag). Stage 8 controls where it exists."""
    kw, lab = r['keyword'], r['keyword_intent']
    if kw in S8:
        v = S8[kw]['validated_intent']
        return v, 'STAGE8_SERP_VALIDATED', (v != lab and v != 'UNCLEAR')
    if r['mapping_disposition'].startswith('EXCLUDE') or r['mapping_disposition'] == 'REVIEW_REQUIRED':
        return lab or 'UNCLEAR', 'DATAFORSEO_LABEL_UNVALIDATED', False
    if lab in ('INFORMATIONAL', 'COMMERCIAL_RESEARCH'):
        return lab, 'DATAFORSEO_LABEL_UNVALIDATED', False
    if is_question(kw):
        return 'INFORMATIONAL', f'QUERY_FORM (unvalidated; DataForSEO label {lab} conflicts with question form)', True
    if lab == 'TRANSACTIONAL' and not TRANS_MOD.search(kw.lower()):
        return 'UNCLEAR', 'DATAFORSEO_TRANSACTIONAL_WITHOUT_COMMERCIAL_MODIFIER (unvalidated)', True
    return lab or 'UNCLEAR', 'DATAFORSEO_LABEL_UNVALIDATED', False


def role_for(r, t):
    kw = r['keyword']
    cfg = T[t]
    if kw in cfg['primary']:
        return 'PRIMARY'
    if kw in cfg['variants'] or any(canon(kw) == canon(p) for p in cfg['primary']):
        return 'CLOSE_VARIANT'
    if VS_AMBIG.match(kw.lower()):
        return 'POSSIBLE_OVERLAP'
    if r['mapping_disposition'] == 'MAP_INTERIM_HOME' or r['cluster_id'] not in cfg['core']:
        return 'SUBTOPIC'
    if is_question(kw):
        return 'QUESTION'
    if is_comparison(kw):
        return 'COMPARISON'
    if len(kw.split()) >= 5:
        return 'LONG_TAIL'
    mods = modifiers(kw)
    if set(mods) & {'ATTRIBUTE', 'CARAT', 'SHAPE', 'MATERIAL', 'CERTIFICATION', 'STYLE'}:
        return 'ATTRIBUTE'
    return 'SUPPORTING'


def coverage_for(r, t, role):
    cfg = T[t]
    if cfg['status'] == 'FUTURE_PAGE':
        return 'MISSING', 'NO_CONTENT'
    if t == 'COM-ER-SIDESTONE':
        return 'THIN', 'MISSING_COMMERCIAL_CONTEXT'
    if re.search(cfg['covered'], r['keyword'].lower()):
        return 'PARTIAL', 'NO_CLEAR_GAP'
    g = {'QUESTION': 'MISSING_QUESTION', 'COMPARISON': 'MISSING_COMPARISON', 'ATTRIBUTE': 'MISSING_ENTITY'}.get(role, 'MISSING_SUBTOPIC')
    return 'UNKNOWN', g


DD_COLS = ['target_page_id', 'topic_group_id', 'cluster_id', 'keyword', 'keyword_normalized', 'search_volume', 'intent',
           'validated_intent', 'stage17_intent_reading', 'intent_basis', 'serp_page_type', 'serp_confidence', 'serp_features',
           'stage7_labs_serp_items_unvalidated', 'keyword_role', 'modifier_type', 'modifier_changes_intent', 'commercial_signal',
           'primary_or_secondary', 'current_rank', 'ranking_url', 'existing_content_status', 'content_coverage', 'gap_type',
           'business_area', 'stage15_disposition', 'stage15_target_url', 'analysis_tier', 'evidence_source', 'evidence_confidence', 'notes']
dd = []
for r in M15:
    kw, t, disp = r['keyword'], r['target_id'], r['mapping_disposition']
    reading, basis, conflict = intent_reading(r)
    mods = modifiers(kw)
    s8 = S8.get(kw)
    notes = []
    if t:
        tier = 'DEEP'
        group = t
        role = role_for(r, t)
        pos = 'PRIMARY' if role in ('PRIMARY', 'CLOSE_VARIANT') else 'SECONDARY'
        ecs = T[t]['status']
        cov, gap = coverage_for(r, t, role)
        if disp == 'MAP_INTERIM_HOME':
            notes.append(f"Interim home. Owner topic {r['stage14_topic_id']} is CONDITIONAL (Stage 14/15).")
        if role == 'POSSIBLE_OVERLAP':
            notes.append('"vs" may be the VS clarity grade (colour + clarity combination, CL-048 at EDU-4C-00) rather than "versus". Ownership unchanged.')
        if cov == 'UNKNOWN':
            notes.append('Existing page exists, but its title/H1/topic does not evidence this concept. Body not audited.')
    else:
        pos = {'CONDITIONAL_NOT_MAPPED': 'HELD', 'DEFERRED_NOT_MAPPED': 'HELD', 'REVIEW_REQUIRED': 'REVIEW'}.get(disp, 'EXCLUDED')
        if pos == 'HELD':
            tier, group, role = 'HELD', 'NO_TARGET::' + held_group(r), 'RELATED_BUT_DISTINCT'
            notes.append(f'{disp}: no Stage 15 owner; not analysed as a page opportunity.')
        elif pos == 'REVIEW':
            tier, group, role = 'REVIEW', 'NO_TARGET::REVIEW_REQUIRED', 'REVIEW_REQUIRED'
            notes.append('REVIEW_REQUIRED kept in the review section; not promoted.')
        else:
            tier = 'EXCLUDED_NO_ANALYSIS' if disp in ('EXCLUDE_NOISE', 'EXCLUDE_COMPETITOR_BRAND') else 'EXCLUDED_LIGHT'
            group, role = 'NO_TARGET::' + disp, 'EXCLUDE'
        ecs, cov, gap = 'NOT_ASSESSED', 'NOT_ASSESSED', 'NOT_ASSESSED'
    if kw == EXCLUDED_TESTER_KW:
        notes.append('Special rule: remains excluded from SEO ownership; ranking URL untouched; not used as evidence for tester targeting.')
    if conflict:
        notes.append('Intent label conflict (see intent_basis).')
    rank = rank_by_kw.get(kw)
    ev = ['Stage 15 map', 'Stage 11 cluster', 'Stage 7 metrics']
    if s8:
        ev.append('Stage 8 SERP')
    if rank:
        ev.append('Stage 3 ranking (via Stage 15 equity)')
    if t and T[t]['status'] != 'FUTURE_PAGE':
        ev.append('Stage 10/13 existing content')
    dd.append(dict(
        target_page_id=t, topic_group_id=group, cluster_id=r['cluster_id'], keyword=kw,
        keyword_normalized=r['normalized_keyword'], search_volume=r['search_volume'], intent=r['keyword_intent'],
        validated_intent=s8['validated_intent'] if s8 else '', stage17_intent_reading=reading, intent_basis=basis,
        serp_page_type=s8['dominant_serp_page_type'] if s8 else 'NOT_VALIDATED',
        serp_confidence=s8['validation_confidence'] if s8 else 'INSUFFICIENT_EVIDENCE',
        serp_features=s8_features(kw), stage7_labs_serp_items_unvalidated=S7[kw]['serp_summary'] if kw in S7 else '',
        keyword_role=role, modifier_type='; '.join(mods), modifier_changes_intent=modifier_changes_intent(mods, kw),
        commercial_signal=commercial_signal(kw, s8['validated_intent'] if s8 else ''),
        primary_or_secondary=pos, current_rank=r['existing_ranking_position'], ranking_url=r['existing_ranking_url'],
        existing_content_status=ecs, content_coverage=cov, gap_type=gap,
        business_area=KCM11[kw]['business_area'] if kw in KCM11 else '', stage15_disposition=disp,
        stage15_target_url=r['target_url'], analysis_tier=tier, evidence_source='; '.join(ev),
        evidence_confidence=row_confidence(r, conflict), notes=' '.join(notes)))

DD_BY_KW = {d['keyword']: d for d in dd}

# ---------------------------------------------------------------- questions
Q_COLS = ['target_page_id', 'cluster_id', 'need_group', 'question', 'question_type', 'intent', 'source_keyword', 'source_type',
          'serp_validated', 'surfaced_on_target', 'variant_count', 'variant_keywords', 'max_search_volume',
          'recommended_role', 'confidence', 'notes']
QTYPES = [
    ('IDENTIFICATION_TESTING', r'tester|\btest\b|beeps|tell if|tell a|detect|microscope|x ray|identify|serial'),
    ('AUTHENTICITY', r'\breal\b|fake|considered fake|really a diamond'),
    ('COMPARISON', r'\bvs\b|versus|difference|better|\bor\b|same as'),
    ('VALUE_PRICE', r'worth|value|cheap|expensive|price|cost|invest|pawn|\bsell\b|how much|pay'),
    ('ETHICS_ENVIRONMENT', r'ethical|environment|sustainab|carbon'),
    ('DURABILITY_CARE', r'cloudy|fade|scratch|break|chip|crack|melt|burn|hard|strong|durable|last|soft|shower|lifespan|destroy|smash|brittle|unbreakable|cut glass'),
    ('SIZE_SUITABILITY', r'too big|too small|big enough|good size|carat diamond good|flashy|ring size|resiz|smaller'),
    ('CERTIFICATION', r'certif|graded|\bgia\b|\bigi\b|certificate'),
    ('PROCESS_ORIGIN', r'how (are|is|do|does)|made|formed|form\b|created|process|grow|extract'),
    ('SELECTION', r'best|should i|which|what .* (get|choose)|how to choose'),
    ('QUALITY_JUDGEMENT', r'good|quality|\bok\b|okay|tacky|popular|matter'),
    ('DEFINITION', r'^what (is|are|does)|mean|called|^is .* (an element|a mineral|a crystal)'),
]


def qtype(q):
    ql = q.lower()
    for n, p in QTYPES:
        if re.search(p, ql):
            return n
    return 'OTHER'


def as_question(k):
    s = k.strip()
    return s[0].upper() + s[1:] + ('' if s.endswith('?') else '?')


def need_matcher(t):
    """Concept regexes for target t, most specific (fewest owned-keyword matches) first."""
    out = []
    for name, _ct, _rel, pat in T[t]['concepts']:
        if isinstance(pat, tuple):
            continue
        n = sum(1 for r in target_rows[t] if re.search(pat, r['keyword'].lower()))
        out.append((n if n else 10 ** 6, name, pat))
    return sorted(out)


# broad concepts that would swallow narrower needs are not used as question groups
NO_GROUP = {'Carat weight (and weight vs visual size)', 'Fractional carat weights (1/2, 1/3, 1/4 …)',
            'Lab-created / lab-grown / lab diamond as equivalent terms',
            'Terminology: synthetic / man-made / lab-created / lab-grown names'}


def need_group(t, text, cluster=None):
    tl = text.lower()
    for name, _ct, _rel, pat in T[t]['concepts']:
        if isinstance(pat, tuple) and cluster == pat[1]:
            return name
    for _n, name, pat in NEED[t]:
        if name in NO_GROUP:
            continue
        if re.search(pat, tl):
            lab = ' [lab-grown]' if re.search(r'\blab\b|lab[- ]grown|lab[- ]created', tl) and not re.search(r'lab', name.lower()) and not t.startswith('EDU-LG') else ''
            return name + lab
    return ''


NEED = {t: need_matcher(t) for t in T}

questions = []
for t, rows in target_rows.items():
    groups = collections.OrderedDict()
    for r in sorted(rows, key=lambda x: -vol(x)):
        if not is_question(r['keyword']):
            continue
        g = need_group(t, r['keyword'], r['cluster_id']) or ('~' + canon(r['keyword'], numbers=(t == 'EDU-4C-07')))
        groups.setdefault(g, []).append(r)
    for g, members in groups.items():
        prim = [m for m in members if m['keyword'] in T[t]['primary']]
        top = prim[0] if prim else members[0]
        names = [m['keyword'] for m in members]
        role_set = {DD_BY_KW[n]['keyword_role'] for n in names}
        validated = any(n in S8 for n in names)
        if 'PRIMARY' in role_set or 'CLOSE_VARIANT' in role_set:
            rec = 'CORE_ANSWER'
        elif 'SUBTOPIC' in role_set or validated or len(members) >= 3:
            rec = 'SECTION_QUESTION'
        else:
            rec = 'FAQ_CANDIDATE'
        qtext = as_question(top['keyword'])
        note = ''
        if len(members) > 1:
            note = f'{len(members)} keyword questions collapsed into one searcher need (anti-FAQ-spam).'
        if t == 'EDU-4C-07' and len(members) > 1:
            qtext = as_question(re.sub(r'\b\d+(\.\d+)?(/\d+)?( \d+)?\b|\bhalf\b|\b1/\d+\b', 'N', top['keyword']).replace('N N', 'N'))
            note += ' Numeric carat variants shown as "N".'
        confs = [DD_BY_KW[n]['evidence_confidence'] for n in names]
        conf = 'HIGH' if 'HIGH' in confs else ('MEDIUM' if 'MEDIUM' in confs else 'LOW')
        questions.append(dict(
            target_page_id=t, cluster_id=top['cluster_id'], need_group=g.lstrip('~') if not g.startswith('~') else 'UNGROUPED (canonical: %s)' % g[1:], question=qtext, question_type=qtype(top['keyword']),
            intent=DD_BY_KW[top['keyword']]['stage17_intent_reading'], source_keyword=top['keyword'],
            source_type='STAGE15_KEYWORD', serp_validated='YES' if validated else 'NO', surfaced_on_target=t,
            variant_count=len(members), variant_keywords=' | '.join(names), max_search_volume=top['search_volume'],
            recommended_role=rec, confidence=conf, notes=note))

# PAA
paa_used, paa_unrouted, paa_skipped_tester = set(), [], 0
seen_q = set()
for serp_kw, qs in PAA.items():
    r = BYKW.get(serp_kw)
    if serp_kw == EXCLUDED_TESTER_KW:
        paa_skipped_tester += len(qs)
        continue
    for q in qs:
        q = q.replace('\u2019', "'").replace('\u2018', "'")
        route = PAA_ROUTE.get(q)
        if not route:
            paa_unrouted.append((serp_kw, q, r['mapping_disposition'] if r else 'NOT_IN_15'))
            continue
        tgt, rec, note = route
        key = (tgt, q)
        surf = (r['target_id'] or ('NO_TARGET::' + r['mapping_disposition'])) if r else 'NOT_IN_15'
        if key in seen_q:
            for qq in questions:
                if qq['target_page_id'] == tgt and qq['question'] == q:
                    qq['variant_count'] += 1
                    if serp_kw not in qq['variant_keywords'].split(' | '):
                        qq['variant_keywords'] += ' | ' + serp_kw
                    if surf not in qq['surfaced_on_target'].split('; '):
                        qq['surfaced_on_target'] += '; ' + surf
            continue
        seen_q.add(key)
        paa_used.add(q)
        questions.append(dict(
            target_page_id=tgt, cluster_id=(r['cluster_id'] if r else ''),
            need_group=(need_group(tgt, q) or 'UNGROUPED') if rec != 'EXCLUDE_OFF_TOPIC' else 'OFF_TOPIC', question=q, question_type=qtype(q), intent='INFORMATIONAL' if rec != 'CATEGORY_COPY_CANDIDATE' else 'TRANSACTIONAL',
            source_keyword=serp_kw, source_type='STAGE8_PAA', serp_validated='YES', surfaced_on_target=surf,
            variant_count=1, variant_keywords=serp_kw, max_search_volume='',
            recommended_role=rec, confidence='MEDIUM' if rec != 'EXCLUDE_OFF_TOPIC' else 'HIGH',
            notes=('PAA observed on the Stage 8 SERP for "%s". ' % serp_kw) + note))
for q in questions:
    if q['source_type'] == 'STAGE8_PAA':
        n = q['variant_count']
        q['notes'] += f' Seen on {n} SERP(s).' if n > 1 else ''
        if n >= 3 and q['recommended_role'] != 'EXCLUDE_OFF_TOPIC':
            q['confidence'] = 'HIGH'
        # cluster_id for PAA: the owner target's cluster that the SERP keyword belongs to, else the target's first Stage 15 cluster
        if not q['cluster_id'] or BYKW.get(q['source_keyword'], {}).get('target_id') != q['target_page_id']:
            q['cluster_id'] = REG15[q['target_page_id']]['cluster_ids'].split(';')[0].strip()
            q['notes'] += ' cluster_id = owner target\'s lead Stage 15 cluster (PAA surfaced on another SERP).'

# ---------------------------------------------------------------- semantic concepts
C_COLS = ['target_page_id', 'cluster_id', 'concept', 'concept_type', 'source_keyword', 'relationship', 'required_or_supporting',
          'evidence_source', 'evidence_count', 'confidence', 'notes']
concepts = []
dropped_concepts = []
for t, cfg in T.items():
    rows = target_rows[t]
    tq = [q['question'] for q in questions if q['target_page_id'] == t and q['source_type'] == 'STAGE8_PAA' and q['recommended_role'] != 'EXCLUDE_OFF_TOPIC']
    tq_all = [q['question'] for q in questions if q['target_page_id'] == t and q['source_type'] == 'STAGE8_PAA']
    rel = [x for r in rows for x in RELATED.get(r['keyword'], [])]
    for name, ctype, relation, pat in cfg['concepts']:
        if isinstance(pat, tuple):
            kws = [r for r in rows if r['cluster_id'] == pat[1]]
            paa_hits, rel_hits = [], []
        else:
            kws = [r for r in rows if re.search(pat, r['keyword'].lower())]
            pool = tq_all if ctype == 'OPTIONAL_CONTEXT' else tq
            paa_hits = [q for q in pool if re.search(pat, q.lower())]
            rel_hits = [x for x in rel if re.search(pat, x.lower())]
        if not (kws or paa_hits or rel_hits):
            dropped_concepts.append((t, name))
            continue
        kws = sorted(kws, key=lambda x: -vol(x))
        src = kws[0]['keyword'] if kws else (paa_hits[0] if paa_hits else rel_hits[0])
        parts = []
        if kws:
            parts.append(f'Stage 15 keywords ({len(kws)})')
        if paa_hits:
            parts.append(f'Stage 8 PAA ({len(paa_hits)})')
        if rel_hits:
            parts.append(f'Stage 8 related searches ({len(set(rel_hits))})')
        s8_backed = bool(paa_hits or rel_hits or any(k['keyword'] in S8 for k in kws))
        if kws and s8_backed:
            conf = 'HIGH' if len(kws) >= 2 or any(k['keyword'] in S8 for k in kws) else 'MEDIUM'
        elif len(kws) >= 3 or (s8_backed and not kws and (len(paa_hits) + len(set(rel_hits))) >= 2):
            conf = 'MEDIUM'
        else:
            conf = 'LOW'
        req = {'PRIMARY_CONCEPT': 'REQUIRED', 'OPTIONAL_CONTEXT': 'OPTIONAL'}.get(ctype, 'SUPPORTING')
        cl = kws[0]['cluster_id'] if kws else REG15[t]['cluster_ids'].split(';')[0].strip()
        n_ = ''
        if not kws:
            n_ = 'Evidence from Stage 8 SERP text only (no owned keyword names it).'
        concepts.append(dict(target_page_id=t, cluster_id=cl, concept=name, concept_type=ctype, source_keyword=src,
                             relationship=relation, required_or_supporting=req, evidence_source='; '.join(parts),
                             evidence_count=len(kws) + len(paa_hits) + len(set(rel_hits)), confidence=conf, notes=n_))

# ---------------------------------------------------------------- relationships
R_COLS = ['keyword', 'cluster_id', 'target_page_id', 'related_keyword', 'related_cluster_id', 'related_target_page_id',
          'relationship_type', 'relationship_source', 'evidence', 'confidence', 'notes']
rels = []
for t, rows in target_rows.items():
    main = T[t]['primary'][0]
    for r in rows:
        d = DD_BY_KW[r['keyword']]
        if r['keyword'] == main:
            continue
        rels.append(dict(keyword=r['keyword'], cluster_id=r['cluster_id'], target_page_id=t, related_keyword=main,
                         related_cluster_id=BYKW[main]['cluster_id'], related_target_page_id=t,
                         relationship_type=d['keyword_role'], relationship_source='STAGE17_KEYWORD_ROLE',
                         evidence=f"Same Stage 15 owner {t}; role derived from query form, cluster and primary choice.",
                         confidence=d['evidence_confidence'], notes=d['notes'][:200]))
# Stage 11 cluster relationships (head keyword to head keyword)
head_of = {}
for cid, reg in REG11.items():
    members = [r for r in M15 if r['cluster_id'] == cid]
    if members:
        head_of[cid] = sorted(members, key=lambda x: -vol(x))[0]
for x in REL11:
    a, b = x['cluster_a'], x['cluster_b']
    if a not in head_of or b not in head_of:
        continue
    ha, hb = head_of[a], head_of[b]
    rt = x['relationship_type'] if x['relationship_type'] in ('RELATED_BUT_DISTINCT', 'POSSIBLE_OVERLAP') else 'RELATED_BUT_DISTINCT'
    rels.append(dict(keyword=ha['keyword'], cluster_id=a, target_page_id=ha['target_id'], related_keyword=hb['keyword'],
                     related_cluster_id=b, related_target_page_id=hb['target_id'], relationship_type=rt,
                     relationship_source='STAGE11_' + x['relationship_id'], evidence=x['evidence'][:300],
                     confidence=x['confidence'],
                     notes=('Stage 11 type DISTINCT_INTENT mapped to RELATED_BUT_DISTINCT. ' if x['relationship_type'] == 'DISTINCT_INTENT' else '') +
                     'Cluster-level relationship shown via each cluster\'s highest-volume Stage 15 member. Clusters not merged.'))
# Stage 17 flagged overlaps (no ownership change)
FLAGS = [
    ('how are diamonds made', 'how are synthetic diamonds made', 'POSSIBLE_OVERLAP', 'LOW', 'Ambiguous "made": natural formation (EDU-NAT-00) vs lab process (interim EDU-LG-00). Not SERP-validated.'),
    ('diamond clarity grading scale', 'diamond grading scale', 'POSSIBLE_OVERLAP', 'MEDIUM', 'Clarity scale (EDU-4C-01, validated UNCLEAR/OTHER) vs general grading scale (EDU-4C-00). The pillar should summarise the clarity scale and link to it.'),
    ('are lab grown diamonds real', 'lab grown vs natural diamonds', 'POSSIBLE_OVERLAP', 'MEDIUM', 'Stage 14 MEDIUM risk: the authenticity SERP is COMPARISON-dominant. Stage 8: max 2 shared top-10 URLs.'),
    ('are cvd diamonds real', 'are lab grown diamonds real', 'RELATED_BUT_DISTINCT', 'MEDIUM', 'Method-specific authenticity stays at EDU-LG-03 (ranking 27). Generic authenticity stays at EDU-LG-01.'),
    ('are lab grown diamonds as hard as natural diamonds', 'do lab grown diamonds get cloudy', 'POSSIBLE_OVERLAP', 'LOW', 'Durability parity (EDU-GEN-01) vs appearance and durability over time (EDU-LG-08).'),
    ('is 14k diamond good', 'is 1 carat diamond good', 'RELATED_BUT_DISTINCT', 'MEDIUM', 'Karat vs carat confusion (Stage 8 PAA "Are 14k diamonds real?"). Different owners; clarify, do not merge.'),
    ('vvs lab diamonds', 'lab grown diamond clarity chart', 'RELATED_BUT_DISTINCT', 'LOW', 'VVS in lab-grown (EDU-4C-03) vs lab-grown grading overview (EDU-4C-00).'),
    ('types of diamond settings', 'types of diamond stud settings', 'SUBTOPIC', 'MEDIUM', 'Stud settings are a subtopic of the settings guide (same owner).'),
    ('diamond facet', 'diamond shape', 'RELATED_BUT_DISTINCT', 'MEDIUM', 'Cut grade/facets (EDU-4C-06) vs shape (EDU-SHP-00). PAA shows cut/shape confusion.'),
]
for vs in ['f vs diamond', 'g vs diamond', 'd vs diamond', 'g-h vs diamond', 'f-g vs diamond']:
    FLAGS.append((vs, 'is f vs2 a good diamond', 'POSSIBLE_OVERLAP', 'LOW', '"vs" may be the VS clarity grade: a colour + clarity combination (CL-048, EDU-4C-00), not a colour comparison. Ownership unchanged (Stage 15).'))
for a, b, rt, cf, note in FLAGS:
    ra, rb = BYKW[a], BYKW[b]
    rels.append(dict(keyword=a, cluster_id=ra['cluster_id'], target_page_id=ra['target_id'], related_keyword=b,
                     related_cluster_id=rb['cluster_id'], related_target_page_id=rb['target_id'], relationship_type=rt,
                     relationship_source='STAGE17_FLAG', evidence=note, confidence=cf, notes='Flag only. No merge, no ownership change.'))
# Stage 8 related searches (only for SERPs of target-owned keywords)
for t, rows in target_rows.items():
    for r in rows:
        for rs in RELATED.get(r['keyword'], []):
            rsl = rs.lower()
            in7 = BYKW.get(rsl)
            if in7:
                rc, rt_ = in7['cluster_id'], in7['target_id']
                if rt_ == t:
                    typ = 'CLOSE_VARIANT' if canon(rsl) == canon(r['keyword']) else 'SUPPORTING'
                elif rt_:
                    typ = 'RELATED_BUT_DISTINCT'
                else:
                    typ = 'RELATED_BUT_DISTINCT' if not in7['mapping_disposition'].startswith('EXCLUDE') else 'EXCLUDE'
                note = f"In Stage 7 ({in7['mapping_disposition']})."
            else:
                rc, rt_ = 'NOT_IN_STAGE7', ''
                if re.search(r'reddit|quora', rsl):
                    typ, note = 'SUPPORTING', 'Forum modifier. Signals discussion/experience demand. Not in Stage 7.'
                elif TRANS_MOD.search(rsl) or re.search(r'amazon|price|cost', rsl):
                    typ, note = 'RELATED_BUT_DISTINCT', 'Commercial/price modifier. Not in Stage 7. No ownership implied.'
                elif rsl.startswith(r['keyword'].lower()):
                    typ, note = 'LONG_TAIL', 'Extends the SERP keyword. Not in Stage 7.'
                else:
                    typ, note = 'SUPPORTING', 'Not in Stage 7. Candidate semantic signal for Stage 18.'
            rels.append(dict(keyword=r['keyword'], cluster_id=r['cluster_id'], target_page_id=t, related_keyword=rs,
                             related_cluster_id=rc, related_target_page_id=rt_, relationship_type=typ,
                             relationship_source='STAGE8_RELATED_SEARCHES', evidence=f'Google related search on the Stage 8 SERP for "{r["keyword"]}".',
                             confidence='MEDIUM', notes=note))

# ---------------------------------------------------------------- gap register
G_COLS = ['target_page_id', 'cluster_id', 'gap_type', 'gap_description', 'supporting_keywords', 'serp_evidence',
          'existing_content_evidence', 'confidence', 'stage18_relevance', 'notes']


def serp_summary_for(t):
    vk = [r['keyword'] for r in target_rows[t] if r['keyword'] in S8]
    if not vk:
        return 'No Stage 8 validated keyword for this target (INSUFFICIENT_EVIDENCE).'
    types = collections.Counter(S8[k]['dominant_serp_page_type'] for k in vk)
    feats = collections.Counter(f for k in vk for f in s8_features(k).split('; ') if f)
    return (f'{len(vk)} validated: ' + ', '.join(f'{a}:{b}' for a, b in types.most_common()) + ' | features: ' +
            ', '.join(f'{a} {b}/{len(vk)}' for a, b in feats.most_common()))


def content_evidence_for(t):
    reg = REG15[t]
    if T[t]['status'] == 'FUTURE_PAGE':
        return 'No existing page (' + reg['status'] + '). ' + T[t]['content_note']
    return f"{reg['existing_url']} | Stage 15 status {reg['status']} | equity: {reg['existing_equity']} | " + T[t]['content_note']


gaps = []
for t, cfg in T.items():
    rows = target_rows[t]
    for gtype, cls, desc, pat, conf, s18, note in cfg['gaps']:
        if isinstance(pat, tuple):
            sup = [r for r in rows if r['cluster_id'] == pat[1]]
        else:
            sup = [r for r in rows if re.search(pat, r['keyword'].lower())]
        sup = sorted(sup, key=lambda x: -vol(x))[:6]
        out_type = GAP_ALIAS.get(gtype, gtype)
        assert out_type in GAP_TYPES, gtype
        n = (f'[{gtype}] ' if gtype != out_type else '') + note
        gaps.append(dict(target_page_id=t, cluster_id=cls, gap_type=out_type, gap_description=desc,
                         supporting_keywords=' | '.join(f"{r['keyword']} ({r['search_volume']})" for r in sup),
                         serp_evidence=serp_summary_for(t), existing_content_evidence=content_evidence_for(t),
                         confidence=conf, stage18_relevance=s18, notes=n.strip()))

# ---------------------------------------------------------------- topic intelligence
TI_COLS = ['target_page_id', 'target_page_type', 'business_area', 'stage15_status', 'target_url', 'primary_topic',
           'primary_keyword', 'primary_keyword_volume', 'co_primary_keywords', 'primary_keyword_variants', 'head_term_note',
           'primary_selection_rationale', 'primary_intent', 'keyword_count', 'secondary_keyword_count', 'question_count',
           'comparison_count', 'commercial_modifier_count', 'semantic_concept_count', 'existing_content_status',
           'content_gap_status', 'gap_types', 'dominant_serp_type', 'serp_confidence', 'serp_features_observed',
           'ranking_equity_status', 'stage16_linking_context', 'evidence_confidence', 'notes']
ti = []
for t, cfg in T.items():
    reg = REG15[t]
    rows = [DD_BY_KW[r['keyword']] for r in target_rows[t]]
    p = cfg['primary'][0]
    vk = [r['keyword'] for r in rows if r['keyword'] in S8]
    types = collections.Counter(S8[k]['dominant_serp_page_type'] for k in vk)
    if not vk:
        dom, sc = 'NOT_VALIDATED', 'INSUFFICIENT_EVIDENCE'
    else:
        dom = types.most_common(1)[0][0] if len(types) == 1 or types.most_common(1)[0][1] > len(vk) / 2 else 'MIXED (' + ', '.join(f'{a}:{b}' for a, b in types.most_common()) + ')'
        sc = 'HIGH' if len(vk) >= 3 and types.most_common(1)[0][1] >= 0.75 * len(vk) else 'MEDIUM' if len(vk) >= 1 and 'UNCLEAR' not in S8[vk[0]]['validated_intent'] else 'LOW'
    feats = collections.Counter(f for k in vk for f in s8_features(k).split('; ') if f)
    eq = [x for x in REP15 if x['mapped_target_id'] == t]
    eqs = (f"PROTECTED: {len(eq)} Stage 3 ranking keyword(s), positions {min(int(x['ranking_position']) for x in eq)}–{max(int(x['ranking_position']) for x in eq)}, URL kept ({eq[0]['ranking_url'].split('.com')[-1]})" if eq else 'NONE (no Stage 3 ranking keyword)')
    lk = PLR16.get(t, {})
    link = (f"parent={lk.get('parent_page_id') or '-'}; children={lk.get('child_page_ids') or '-'}; related={lk.get('related_page_ids') or '-'}; "
            f"incoming_required={lk.get('incoming_required') or '0'}; outgoing_required={lk.get('outgoing_required') or '0'}; orphan_status={lk.get('orphan_status')}")
    covs = collections.Counter(r['content_coverage'] for r in rows)
    gap_status = 'MISSING' if cfg['status'] == 'FUTURE_PAGE' else ('THIN' if covs.get('THIN') else ('PARTIAL' if covs.get('PARTIAL') else 'UNKNOWN'))
    gts = sorted({g['gap_type'] for g in gaps if g['target_page_id'] == t})
    tq = [q for q in questions if q['target_page_id'] == t and q['recommended_role'] != 'EXCLUDE_OFF_TOPIC']
    ti.append(dict(
        target_page_id=t, target_page_type=reg['page_type'], business_area=reg['hub'], stage15_status=reg['status'],
        target_url=reg['existing_url'] or reg['proposed_url'], primary_topic=cfg['topic'], primary_keyword=p,
        primary_keyword_volume=BYKW[p]['search_volume'], co_primary_keywords=' | '.join(cfg['primary'][1:]),
        primary_keyword_variants=' | '.join(cfg['variants']), head_term_note=cfg['head'], primary_selection_rationale=cfg['why'],
        primary_intent=DD_BY_KW[p]['stage17_intent_reading'] + (' (Stage 8)' if p in S8 else ' (unvalidated)'),
        keyword_count=len(rows), secondary_keyword_count=sum(1 for r in rows if r['primary_or_secondary'] == 'SECONDARY'),
        question_count=len(tq), comparison_count=sum(1 for r in rows if r['keyword_role'] == 'COMPARISON' or 'COMPARISON' in r['modifier_type'].split('; ')),
        commercial_modifier_count=sum(1 for r in rows if r['commercial_signal'] != 'NONE'),
        semantic_concept_count=sum(1 for c in concepts if c['target_page_id'] == t),
        existing_content_status=cfg['status'], content_gap_status=gap_status, gap_types='; '.join(gts),
        dominant_serp_type=dom, serp_confidence=sc,
        serp_features_observed=', '.join(f'{a} {b}/{len(vk)}' for a, b in feats.most_common()) if vk else '',
        ranking_equity_status=eqs, stage16_linking_context=link, evidence_confidence=cfg['pconf'],
        notes=cfg['content_note']))
# held / review groups (visible, not targets)
hg = collections.defaultdict(list)
for d in dd:
    if d['analysis_tier'] in ('HELD', 'REVIEW'):
        hg[d['topic_group_id']].append(d)
for g, rows in sorted(hg.items()):
    rows = sorted(rows, key=lambda x: -vol(x))
    key = g.split('::')[1]
    a14 = ARCH14.get(key)
    disp = collections.Counter(r['stage15_disposition'] for r in rows)
    name = a14['topic_name'] if a14 else (REG11[key]['cluster_name'] if key in REG11 else 'Stage 11 UNCLUSTERED_REVIEW and Stage 15 review additions')
    vk = [r['keyword'] for r in rows if r['keyword'] in S8]
    ti.append(dict(
        target_page_id=g, target_page_type='NO_TARGET (' + '/'.join(disp) + ')', business_area=rows[0]['business_area'],
        stage15_status=(a14['architecture_status'] if a14 else '/'.join(disp)), target_url='NONE (no Stage 15 owner)',
        primary_topic=name, primary_keyword='', primary_keyword_volume='',
        head_term_note=f"Highest-volume member (reference only, not a primary): {rows[0]['keyword']} ({rows[0]['search_volume']})",
        primary_selection_rationale='Not selected: no Stage 15 owner. Held/review keywords are not deep-dived as page opportunities.',
        primary_intent='', keyword_count=len(rows), secondary_keyword_count=0,
        question_count=0, comparison_count=sum(1 for r in rows if 'COMPARISON' in r['modifier_type'].split('; ')),
        commercial_modifier_count=sum(1 for r in rows if r['commercial_signal'] != 'NONE'), semantic_concept_count=0,
        existing_content_status='NOT_ASSESSED', content_gap_status='NOT_ASSESSED', gap_types='',
        dominant_serp_type=(', '.join(f'{k}:{v}' for k, v in collections.Counter(S8[k]['dominant_serp_page_type'] for k in vk).most_common()) if vk else 'NOT_VALIDATED'),
        serp_confidence='LOW' if vk else 'INSUFFICIENT_EVIDENCE', ranking_equity_status='NONE',
        stage16_linking_context=('Stage 16 conditional page: ' + PLR16[key]['orphan_status']) if key in PLR16 else '',
        evidence_confidence='INSUFFICIENT_EVIDENCE' if g.endswith('REVIEW_REQUIRED') else 'LOW',
        notes='Kept visible so held demand is not lost. No page, URL or ownership implied.'))

# ---------------------------------------------------------------- write
wr('17_keyword_deep_dive.csv', DD_COLS, dd)
wr('17_topic_intelligence.csv', TI_COLS, ti)
wr('17_semantic_concepts.csv', C_COLS, concepts)
wr('17_question_map.csv', Q_COLS, questions)
wr('17_keyword_relationships.csv', R_COLS, rels)
wr('17_gap_register.csv', G_COLS, gaps)

stats = dict(
    keywords=len(dd), tiers=dict(collections.Counter(d['analysis_tier'] for d in dd)), targets=len(T),
    topic_rows=len(ti), clusters_on_targets=len({r['cluster_id'] for t in target_rows for r in target_rows[t]}),
    clusters_all=len({d['cluster_id'] for d in dd}),
    questions=len(questions), questions_active=sum(1 for q in questions if q['recommended_role'] != 'EXCLUDE_OFF_TOPIC'),
    q_roles=dict(collections.Counter(q['recommended_role'] for q in questions)),
    q_sources=dict(collections.Counter(q['source_type'] for q in questions)),
    concepts=len(concepts), concept_types=dict(collections.Counter(c['concept_type'] for c in concepts)),
    concept_conf=dict(collections.Counter(c['confidence'] for c in concepts)), dropped_concepts=dropped_concepts,
    rels=len(rels), rel_types=dict(collections.Counter(r['relationship_type'] for r in rels)),
    rel_sources=dict(collections.Counter(r['relationship_source'].split('_R')[0] if r['relationship_source'].startswith('STAGE11') else r['relationship_source'] for r in rels)),
    gaps=len(gaps), gap_types=dict(collections.Counter(g['gap_type'] for g in gaps)),
    gap_conf=dict(collections.Counter(g['confidence'] for g in gaps)),
    paa_total=sum(len(v) for v in PAA.values()), paa_unique_used=len(paa_used), paa_unrouted=len(paa_unrouted),
    paa_skipped_tester=paa_skipped_tester, roles=dict(collections.Counter(d['keyword_role'] for d in dd if d['analysis_tier'] == 'DEEP')),
    coverage=dict(collections.Counter(d['content_coverage'] for d in dd if d['analysis_tier'] == 'DEEP')),
    conflicts=sum(1 for d in dd if 'conflict' in d['intent_basis'].lower() or 'WITHOUT_COMMERCIAL' in d['intent_basis']),
)
json.dump(stats, open(os.path.join(OUT, 'scripts', '17_build_stats.json'), 'w'), indent=1)
print(json.dumps({k: v for k, v in stats.items() if k != 'dropped_concepts'}, indent=1))
print('dropped concepts (no evidence):', dropped_concepts)
print('unrouted PAA sample:', paa_unrouted[:5])
