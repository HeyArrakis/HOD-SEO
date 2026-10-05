#!/usr/bin/env python3
"""Stage 18.5 — targeted SERP validation supplement (17 approved queries).

Reads ONLY the 17 raw task_get responses saved in dataforseo/raw/18_5_stage_serp/ (paid for in the
single approved task_post, $0.0102) plus the Stage 18 outputs (read-only). No API call is made here.

Outputs:
  dataforseo/raw/18_5_stage_serp/manifest.csv
  serp/analysis/18_5_targeted_serp_validation.csv
  serp/analysis/18_5_stage18_change_log.csv
  scripts/18_5_build_stats.json

Stage 18 files are NOT edited. Every change-log row carries an evidence token [ev:"..."] that must
appear verbatim (case-insensitive) in that query's raw SERP; qc_18_5.py verifies this.
"""
import collections
import csv
import glob
import json
import os
import re

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
P = lambda *a: os.path.join(BASE, *a)
RAW = P('dataforseo', 'raw', '18_5_stage_serp')

QUERIES = ['what are lab grown diamonds', 'do lab grown diamonds hold their value', 'are lab grown diamonds ethical',
           'do lab grown diamonds get cloudy', 'how are diamonds formed', '4cs of diamonds', 'diamond color chart',
           'diamond carat size chart', 'diamond cut', 'diamond shapes', 'diamond certificate', '14k vs 18k gold',
           'white gold vs platinum', 'engagement ring settings', 'ring size chart', 'how to measure ring size',
           'what are diamonds made of']
TARGET = {'what are lab grown diamonds': 'EDU-LG-00', 'do lab grown diamonds hold their value': 'EDU-LG-05',
          'are lab grown diamonds ethical': 'EDU-LG-07', 'do lab grown diamonds get cloudy': 'EDU-LG-08',
          'how are diamonds formed': 'EDU-NAT-00', '4cs of diamonds': 'EDU-4C-00', 'diamond color chart': 'EDU-4C-05',
          'diamond carat size chart': 'EDU-4C-07', 'diamond cut': 'EDU-4C-06', 'diamond shapes': 'EDU-SHP-00',
          'diamond certificate': 'EDU-CERT-00', '14k vs 18k gold': 'EDU-MET-01', 'white gold vs platinum': 'EDU-MET-00',
          'engagement ring settings': 'EDU-RJG-01', 'ring size chart': 'EDU-RJG-02', 'how to measure ring size': 'EDU-RJG-02',
          'what are diamonds made of': 'EDU-GEN-01'}


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)


# ---------------------------------------------------------------- load raw
S = {}
for f in sorted(glob.glob(os.path.join(RAW, '09242103-*.json'))):
    d = json.load(open(f, encoding='utf-8'))
    t = d['tasks'][0]
    res = t['result'][0]
    items = res['items']
    kw = res['keyword']
    S[kw] = dict(task_id=t['id'], status=t['status_code'], status_message=t['status_message'], cost=t['cost'],
                 result_count=t['result_count'], data=t['data'], item_types=res['item_types'], items=items, file=os.path.basename(f),
                 text=' \n'.join(strings(res)).lower(), datetime=res['datetime'])
assert sorted(S) == sorted(QUERIES), sorted(set(QUERIES) ^ set(S))
POST = json.load(open(os.path.join(RAW, '00_task_post_response.json'), encoding='utf-8'))


def of(kw, typ):
    return [it for it in S[kw]['items'] if it['type'] == typ]


def clean_md(md):
    md = re.sub(r'\[\[\d+\]\]\([^)]*\)', '', md or '')
    md = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', md)
    return re.sub(r'\]\([^)]*\)', ']', md)


def aio_topics(kw):
    out = []
    for it in of(kw, 'ai_overview'):
        md = clean_md(it.get('markdown'))
        for x in re.findall(r'^#+ (.+)$', md, re.M) + re.findall(r'\*\*([^*]{2,60})\*\*', md):
            x = x.strip(' :')
            if x and x.lower() not in [o.lower() for o in out] and not re.search(r'\$\d|\d+ ?kwh', x.lower()):
                out.append(x)
    return out


ENT = [('Lab-grown diamond', r'lab[- ]grown|lab diamond|laboratory'), ('Natural / mined diamond', r'natural|mined'),
       ('HPHT', r'\bhpht\b'), ('CVD', r'\bcvd\b|chemical vapor'), ('Moissanite', r'moissanite'), ('Cubic zirconia', r'cubic zirconia'),
       ('GIA', r'\bgia\b|gemological institute of america'), ('IGI', r'\bigi\b|international gemological'), ('AGS', r'\bags\b|american gem society'),
       ('GCAL', r'gcal'), ('Laser inscription', r'inscri'), ('Carbon', r'\bcarbon\b'), ('Graphite', r'graphite'), ('Kimberlite', r'kimberlite'),
       ('Mantle', r'mantle'), ('Mohs / hardness', r'mohs|hardness|hardest'), ('Rhodium', r'rhodium'), ('Platinum', r'platinum'),
       ('White gold', r'white gold'), ('Yellow gold', r'yellow gold'), ('Rose gold', r'rose gold'), ('Nickel', r'nickel'),
       ('Palladium', r'palladium'), ('14k gold', r'\b14 ?k\b'), ('18k gold', r'\b18 ?k\b'), ('24k gold', r'\b24 ?k\b'),
       ('D-Z colour scale', r'\bd\b.{0,20}\bz\b|colorless'), ('Fancy colour', r'fancy'), ('VS1/VS2', r'\bvs ?[12]\b'),
       ('FL-I3 clarity', r'flawless|\bi3\b'), ('Eye-clean', r'eye-clean|eye clean'), ('Brilliance/fire/scintillation', r'brilliance|scintillation|\bfire\b'),
       ('Proportions/polish/symmetry', r'proportion|polish|symmetr'), ('Carat (0.2 g)', r'0\.2 grams|carat'), ('Millimetres', r'\bmm\b|millimet'),
       ('Round', r'\bround\b'), ('Oval', r'\boval\b'), ('Princess', r'princess'), ('Cushion', r'cushion'), ('Emerald cut', r'emerald'),
       ('Pear', r'\bpear\b'), ('Marquise', r'marquise'), ('Radiant', r'radiant'), ('Asscher', r'asscher'), ('Heart', r'\bheart\b'),
       ('Solitaire', r'solitaire'), ('Prong', r'prong'), ('Bezel', r'bezel'), ('Pavé', r'pav[eé]'), ('Halo', r'\bhalo\b'),
       ('Three-stone', r'three-stone|three stone'), ('Cathedral', r'cathedral'), ('Channel', r'channel'), ('Tension', r'tension'),
       ('US ring size', r'us size|us ring size'), ('Ring sizer', r'ring sizer'), ('Coal', r'\bcoal\b'), ('Energy / renewables', r'kwh|renewable|carbon-neutral|carbon neutral'),
       ('India / China production', r'india and china'), ('Conflict / blood diamonds', r'conflict|blood diamond')]
ATTR = [('QUALITY', r'quality|grade'), ('CLARITY', r'clarity|inclusion'), ('COLOUR', r'\bcolou?r'), ('CUT', r'\bcut\b'), ('CARAT', r'carat'),
        ('SHAPE', r'\bshape'), ('CERTIFICATION', r'certif|grading report|\breport\b'), ('ORIGIN', r'natural|mined|origin'),
        ('PROCESS', r'\bprocess|formed|\bgrow|made'), ('DURABILITY', r'durab|scratch|hardness|softer|harder|wear'),
        ('PRICE', r'price|cost|afford|expensive'), ('VALUE', r'\bvalue|worth|invest'), ('RESALE', r'resale|resell|buy them back|secondary'),
        ('ETHICS', r'ethic|conflict|labor|labour'), ('CARE', r'clean|maintenance|re-plat|replat'), ('SIZE', r'\bsize'),
        ('MATERIAL', r'gold|platinum|metal|alloy'), ('STYLE', r'style|design|look'), ('SETTING', r'setting|prong|bezel'),
        ('OCCASION', r'engagement|wedding')]

# curated reading of each SERP (evidence summarised in notes; see 18_5_semantic_supplement.md)
CUR = {
    'what are lab grown diamonds': ('INFORMATIONAL', 'EDITORIAL_GUIDE', 'DEFINITION_BLOCK; TYPE_LIST (growth methods); COMPARISON (key differences from mined)',
        'AIO: definition -> composition & properties (identical carbon lattice, same 4Cs, IGI certifies) -> how they are made (HPHT, CVD) -> key differences from mined (origin, cost, not fakes). Organic #1-#2 are lab-vs-natural comparison pages.', 'HIGH'),
    'do lab grown diamonds hold their value': ('INFORMATIONAL', 'EDITORIAL_GUIDE', 'DEFINITION_BLOCK (direct "No" answer); CALCULATION (absolute vs % loss example); PROS_CONS (why buy anyway); FAQ',
        'AIO: direct answer -> resale worth & depreciation (low resale, falling prices, limited secondary market) -> absolute dollar loss vs percentage -> why buy them / not an investment. Reddit #1 + Discussions & forums: experience-led SERP.', 'HIGH'),
    'are lab grown diamonds ethical': ('INFORMATIONAL', 'EDITORIAL_GUIDE', 'DEFINITION_BLOCK (qualified yes); PROS_CONS (benefits vs concerns); BUYING_GUIDE (how to buy responsibly)',
        'AIO: qualified answer -> ethical benefits (no mining risks, conflict-free, labour) -> environmental & ethical concerns (energy use, fossil-fuel grids in India/China, lack of regulation) -> how to buy responsibly (ask origin, green energy). Reddit #1, Guardian, forums.', 'HIGH'),
    'do lab grown diamonds get cloudy': ('INFORMATIONAL', 'EDITORIAL_GUIDE', 'DEFINITION_BLOCK (direct "No"); TYPE_LIST (causes of a cloudy look); STEP_SEQUENCE (cleaning)',
        'AIO: direct answer -> why a lab diamond might look cloudy (surface buildup, cloud inclusions/low clarity, poor cut, simulant confusion) -> how to restore sparkle (clean, professional check). Retailer blogs + Reddit.', 'HIGH'),
    'how are diamonds formed': ('INFORMATIONAL', 'EDUCATIONAL', 'STEP_SEQUENCE / process explainer; COMPARISON (natural vs lab-grown formation)',
        'AIO: natural formation (depth in mantle, heat & pressure, 1-3.3 bn years, kimberlite pipes) -> lab-grown formation (HPHT, CVD). Q&A feature; museum, Wikipedia, naturaldiamonds.com, VRAI.', 'HIGH'),
    '4cs of diamonds': ('INFORMATIONAL', 'EDUCATIONAL', 'DEFINITION_BLOCK; TYPE_LIST (one block per C with meaning + grade range); VISUAL_CHART (images pack at rank 2)',
        'AIO: definition (GIA-established standard) -> Cut -> Color -> Clarity -> Carat (each: what it means + grade range) -> prompt: which C to prioritise for budget/shape. Authority-led (AGS, GIA 4Cs) then retailer guides.', 'HIGH'),
    'diamond color chart': ('INFORMATIONAL', 'EDITORIAL_GUIDE', 'VISUAL_CHART; TYPE_LIST (five grade groups, each with appearance + value); BUYING_GUIDE (metal pairing)',
        'AIO: five chart images -> D-to-Z definition (GIA) -> five groups D-F, G-J, K-M, N-R, S-Z each with appearance and value -> fancy-colour note -> prompt metal type / shape / carat. GIA #1, Tiffany (image result), AGS.', 'HIGH'),
    'diamond carat size chart': ('INFORMATIONAL', 'EDITORIAL_GUIDE', 'VISUAL_CHART (carat -> mm by shape; image-led, no AI Overview); on-hand comparison (short videos); price-by-budget questions',
        'No AI Overview. Images pack at rank 1, PAA, short videos. Organic: carat-to-mm charts by shape (Brilliance, Brilliant Earth, Diamonds Factory, Fascinating Diamonds, Zales, VRAI, Diamond Banc), Pinterest.', 'HIGH'),
    'diamond cut': ('INFORMATIONAL', 'EDITORIAL_GUIDE', 'DEFINITION_BLOCK; COMPARISON (cut vs shape); TYPE_LIST (cut quality factors; popular shapes)',
        'AIO: definition (light performance) -> cut vs shape -> key cut quality factors (brilliance, fire, scintillation, proportions) -> popular shapes. Organic mixes cut-grade pages (GIA cut scale, Tiffany, Blue Nile, VRAI) with shape lists (Hatton Garden "Top 10 Diamond Cuts", Bario Neal). Meaning is MIXED (cut quality + shape).', 'MEDIUM'),
    'diamond shapes': ('INFORMATIONAL', 'EDITORIAL_GUIDE', 'TYPE_LIST (10 shapes with traits); VISUAL_CHART (related: chart with pictures)',
        'AIO: definition (outline viewed from above) -> 10 popular shapes each with a trait -> prompts: jewellery type, brilliant vs step cut, carat/budget. Organic all jewellery guides (Tiffany, GIA, Brilliant Earth, Rare Carat, Kay); popular products present.', 'HIGH'),
    'diamond certificate': ('INFORMATIONAL', 'MIXED', 'DEFINITION_BLOCK; TYPE_LIST (what is included; top labs); STEP_SEQUENCE (check/lookup - PAA + related)',
        'AIO: definition (independent lab grading report) -> what is included (4Cs, measurements, polish, symmetry, fluorescence, origin natural/lab, laser inscription) -> top labs (GIA, IGI, AGS). IGI homepage #1 and GIA service page (lab navigational), then editorial guides; popular products are Etsy certificate listings (irrelevant).', 'MEDIUM'),
    '14k vs 18k gold': ('INFORMATIONAL', 'COMPARISON', 'COMPARISON_TABLE (purity, colour, durability, price/value, hypoallergenic); PROS_CONS',
        'AIO: purity -> colour & appearance -> durability & wear -> price & value -> hypoallergenic properties -> prompt jewellery type / daily wear. Reddit #1 then side-by-side comparison guides.', 'HIGH'),
    'white gold vs platinum': ('INFORMATIONAL', 'COMPARISON', 'COMPARISON_TABLE (composition, price, maintenance, skin sensitivity); PROS_CONS (PAA disadvantages of each)',
        'AIO: key differences: composition (alloy + rhodium vs ~95% platinum) -> price -> maintenance (rhodium re-plating vs platinum patina) -> skin sensitivity (nickel) -> prompt ring type / upfront vs long-term cost.', 'HIGH'),
    'engagement ring settings': ('MIXED', 'MIXED', 'TYPE_LIST (setting types); CATEGORY / PRODUCT listings (settings only); VISUAL_CHART (related chart)',
        'AIO: definition -> popular setting types (solitaire, halo, pave, bezel, three-stone, cathedral) -> shopping for settings (price range, retailers). Organic led by shop pages (Kesslers, Friendly Diamonds, Robbins Brothers "setting only", KayOutlet Design-A-Ring) plus local pack and popular products; editorial guides below (Brilliant Earth, Tiffany, Blue Nile, VRAI).', 'HIGH'),
    'ring size chart': ('INFORMATIONAL', 'EDITORIAL_GUIDE', 'VISUAL_CHART (AI Overview table: US size / circumference mm / diameter mm); STEP_SEQUENCE (measure at home); printable tool (PDF sizers)',
        'AIO: definition -> US ring size chart table -> how to measure at home (string/paper, round up, band width, printable sizer). Organic: Tiffany size guide, printable PDFs (UCF, Macy\'s, James Avery), Brilliant Earth, Wikipedia, Jewlr.', 'HIGH'),
    'how to measure ring size': ('INFORMATIONAL', 'EDITORIAL_GUIDE', 'STEP_SEQUENCE (numbered paper/string steps; existing-ring method); accuracy tips; VIDEO / short videos',
        'AIO: direct answer -> measuring with paper or string (7 numbered steps) -> measuring an existing ring (inside diameter) -> tips for accuracy (time of day, cold, band width). Video and short-video units; at-home methods dominate.', 'HIGH'),
    'what are diamonds made of': ('INFORMATIONAL', 'EDUCATIONAL', 'DEFINITION_BLOCK; COMPARISON (diamond vs graphite/other carbon forms)',
        'AIO: pure carbon -> elemental & atomic structure (99.95% carbon, trace nitrogen/boron, tetrahedral lattice) -> comparison with other carbon forms (graphite). GIA #1, Wikipedia, ASU, university and jeweller explainers.', 'HIGH'),
}

# ---------------------------------------------------------------- validation CSV
VAL = []
for kw in QUERIES:
    s = S[kw]
    it = s['item_types']
    org = of(kw, 'organic')
    paa = [q['title'] for x in of(kw, 'people_also_ask') for q in (x.get('items') or [])]
    rel = [q for x in of(kw, 'related_searches') for q in (x.get('items') or [])]
    txt_core = ' \n'.join([clean_md(x.get('markdown')) for x in of(kw, 'ai_overview')] + [o.get('title', '') + ' ' + (o.get('description') or '') for o in org] + paa).lower()
    ents = [n for n, rx in ENT if re.search(rx, txt_core)]
    attrs = [a for a, rx in ATTR if re.search(rx, txt_core)]
    fs = 'YES' if ('featured_snippet' in it or any(o.get('is_featured_snippet') for o in org)) else 'NO'
    intent, ptype, fmt, pattern, conf = CUR[kw]
    doms = []
    for o in org:
        if o['domain'] not in doms:
            doms.append(o['domain'])
    VAL.append(dict(keyword=kw, task_id=s['task_id'], validated_intent=intent, dominant_page_type=ptype,
                    ai_overview='YES' if 'ai_overview' in it else 'NO', paa='YES' if 'people_also_ask' in it else 'NO',
                    shopping='YES' if ('popular_products' in it or 'product_considerations' in it) else 'NO',
                    video='YES' if ('video' in it or 'short_videos' in it) else 'NO', images='YES' if 'images' in it else 'NO',
                    local_pack='YES' if 'local_pack' in it else 'NO', featured_snippet=fs, top_domains='; '.join(doms[:8]),
                    recurring_topics='; '.join(aio_topics(kw)[:16]), recurring_questions='; '.join(paa),
                    recurring_entities='; '.join(ents), recurring_attributes='; '.join(attrs), content_format_pattern=fmt, confidence=conf,
                    notes=f'{pattern} | Related searches: {"; ".join(rel)} | Top titles: {" / ".join(o["title"] for o in org[:5])} | '
                          f'SERP item types: {", ".join(it)} | Stage 15 owner of this topic: {TARGET[kw]} (unchanged) | raw: {s["file"]}'))
os.makedirs(P('serp', 'analysis'), exist_ok=True)
VCOLS = ['keyword', 'task_id', 'validated_intent', 'dominant_page_type', 'ai_overview', 'paa', 'shopping', 'video', 'images', 'local_pack',
         'featured_snippet', 'top_domains', 'recurring_topics', 'recurring_questions', 'recurring_entities', 'recurring_attributes',
         'content_format_pattern', 'confidence', 'notes']
with open(P('serp', 'analysis', '18_5_targeted_serp_validation.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=VCOLS)
    w.writeheader()
    w.writerows(VAL)

# manifest
with open(os.path.join(RAW, 'manifest.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['task_id', 'keyword', 'status', 'cost', 'result_count', 'raw_file', 'task_post_status', 'location_code', 'language_code', 'depth', 'device', 'priority', 'retrieved_via'])
    post_status = {t['id']: t['status_code'] for t in POST['tasks']}
    for kw in QUERIES:
        s = S[kw]
        d = s['data']
        w.writerow([s['task_id'], kw, f'{s["status"]} {s["status_message"]}', s['cost'], s['result_count'], s['file'], post_status.get(s['task_id']),
                    d['location_code'], d['language_code'], d['depth'], d['device'], d['priority'], 'task_get/advanced (free; cost field echoes the task_post charge)'])

# ---------------------------------------------------------------- change log vs Stage 18
REG = {r['gap_id']: r for r in csv.DictReader(open(P('content-strategy', '18_semantic_gap_register.csv'), encoding='utf-8'))}
CH = []


def ch(kw, gap, ctype, new, ev, conf='HIGH', note='', target=None, ref=None, assumption=None):
    t = target or TARGET[kw]
    if gap:
        g = REG[gap]
        assert g['target_page_id'] == t, (gap, t)
        ref = ref or f'18_semantic_gap_register.csv:{gap}'
        assumption = assumption or f'{g["concept"]} — {g["gap_severity"]} / {g["evidence_strength"]} evidence / {g["owner_status"]} ({g["owner_page_id"]}) / confidence {g["confidence"]}'
    evs = ev if isinstance(ev, list) else [ev]
    for e in evs:
        assert e.lower() in S[kw]['text'], (kw, e)
    CH.append(dict(keyword=kw, stage18_reference=ref, stage18_assumption=assumption, new_evidence=new, change_type=ctype,
                   affected_target_id=t, affected_gap_id=gap or 'NONE (not in Stage 18 register)', confidence=conf,
                   notes=(note + ' ' if note else '') + ' '.join(f'[ev:"{e}"]' for e in evs)))


FMT = 'Stage 18 had no Stage 8 SERP for this target; format recorded INSUFFICIENT_EVIDENCE.'
HEADNOTE = 'Head-term SERP now validated. Search volume is still NOT measured (no volume lookup was run or approved).'

K = 'what are lab grown diamonds'
ch(K, 'G18-0296', 'CHANGED', 'SERP validated: INFORMATIONAL / EDITORIAL_GUIDE with AI Overview, PAA, video, images.', 'Composition and Properties', note='Format no longer unvalidated for this target. ' + FMT)
ch(K, 'G18-0282', 'CHANGED', 'The definition head term has a validated informational SERP.', 'a real diamond produced in a controlled laboratory setting', note=HEADNOTE)
ch(K, 'G18-0001', 'STRENGTHENED', 'AI Overview opens with a one-sentence definition; 5 of 6 organic snippets define the term.', 'A lab-grown diamond is', note='Evidence moves from keyword-only to SERP-validated; DEFINITION_BLOCK format supported.')
ch(K, 'G18-0002', 'STRENGTHENED', 'Wikipedia and Kay snippets list the alternative names (synthetic, laboratory-created, man-made, artificial, cultured).', ['cultured', 'man-made'])
ch(K, 'G18-0005', 'STRENGTHENED', 'AI Overview section "How They Are Made" summarises HPHT and CVD.', 'How They Are Made', note='Interim home for EDU-LG-04 unchanged; summary level only, CVD-vs-HPHT depth stays with EDU-LG-03.')
ch(K, 'G18-0008', 'STRENGTHENED', 'AI Overview bullet "Not Fakes" (not simulants); PAA "Are lab diamonds like real diamonds?" and "Will a diamond tester say a lab-grown diamond is real?".', ['Not Fakes', 'Are lab diamonds like real diamonds?'], note='Implied weight OPTIONAL -> IMPORTANT (brief mention + link to EDU-LG-01; ownership unchanged).')
ch(K, 'G18-0009', 'STRENGTHENED', 'AI Overview section "Key Differences from Mined Diamonds"; organic #1 (Brilliant Earth) and #2 (Kay) are lab-vs-natural comparison pages.', 'Key Differences from Mined Diamonds', note='Definition SERP is partly comparison-led (same pattern as the Stage 8 authenticity SERP). Brief comparison framing + link to EDU-LG-02; no second owner.')
ch(K, 'G18-0010', 'STRENGTHENED', 'AI Overview "Cost" difference; PAA "Is it worth buying lab grown diamonds?"; related "worth", "cost".', ['Is it worth buying lab grown diamonds?', 'What are lab grown diamonds worth'], note='Implied weight OPTIONAL -> SUPPORTING (brief mention + link to EDU-LG-05).')
ch(K, None, 'NEW_EVIDENCE', 'Definition SERP also asks about disadvantages (PAA "What are the disadvantages of lab grown diamonds?"; related "Disadvantages of lab-grown diamonds").', 'What are the disadvantages of lab grown diamonds?', conf='MEDIUM',
   assumption='Not assumed for EDU-LG-00 (owned by EDU-LG-06 conditional; interim home EDU-LG-02).', note='Brief mention + link only; owner EDU-LG-06 (interim EDU-LG-02).')

K = 'do lab grown diamonds hold their value'
ch(K, 'G18-0297', 'CHANGED', 'SERP validated: INFORMATIONAL / EDITORIAL_GUIDE, forum-heavy (Reddit #1, Discussions & forums), answer-first AI Overview.', 'Resale Worth and Depreciation', note=FMT)
ch(K, 'G18-0064', 'CONFIRMED', 'AI Overview gives a direct "No" and a "Resale Worth and Depreciation" section; all 8 organic results address resale/value.', 'do not hold their value well over time', note='Answer-first DEFINITION_BLOCK format supported; SERP evidence suggests a direct answer, no guarantee of AI Overview inclusion.')
ch(K, 'G18-0065', 'CONFIRMED', 'AI Overview bullet "Not an Investment"; Frank Darling snippet "consumer luxury good rather than a financial investment".', 'Not an Investment')
ch(K, 'G18-0063', 'CONFIRMED', 'AI Overview: manufactured at scale; upfront cost far lower than natural.', 'manufactured at scale')
ch(K, 'G18-0066', 'STRENGTHENED', 'AI Overview bullet "Falling Market Prices"; Instagram snippet on price declines since 2020.', 'Falling Market Prices', note='Implied weight SUPPORTING -> IMPORTANT.')
ch(K, 'G18-0071', 'STRENGTHENED', 'Liori snippet compares natural (25-50%) vs lab (10-30%) resale; related "Do natural diamonds hold their value", "Resale value of lab grown diamonds vs natural".', ['Do natural diamonds hold their value', 'Resale value of lab grown diamonds vs natural'], note='Implied weight SUPPORTING -> IMPORTANT.')
ch(K, 'G18-0069', 'STRENGTHENED', 'AI Overview: many traditional jewellers refuse to buy lab diamonds back.', 'refuse to buy them back', note='Remains BUSINESS_DEPENDENT: HOD buy-back/trade-in policy is now a more visible buyer question.')
ch(K, 'G18-0073', 'STRENGTHENED', 'SERP carries dated, conflicting percentage claims (10-30%, 20-40%, 15-20%/yr) from different sources.', ['10% to 30%', '20-40%'], note='Stage 13 rule stands: no hard-coded price or resale figures; any range must be sourced and dated.')
ch(K, None, 'NEW_EVIDENCE', 'AI Overview section "Absolute Dollar Loss vs. Percentage": cash lost can be smaller for lab-grown because the upfront price is lower.', 'Absolute Dollar Loss vs. Percentage',
   assumption='Not in Stage 18 register for EDU-LG-05.', note='New supporting concept for EDU-LG-05 (framing, no live figures).')
ch(K, None, 'NEW_EVIDENCE', 'PAA "What is the lifespan of a lab diamond?" appears on this SERP (and on the cloudiness SERP).', 'What is the lifespan of a lab diamond?', conf='MEDIUM', target='EDU-LG-08',
   assumption='Stage 17 routed this PAA to EDU-LG-08 (FAQ).', note='Cross-page: answer belongs to EDU-LG-08; EDU-LG-05 may link.')

K = 'are lab grown diamonds ethical'
ch(K, 'G18-0298', 'CHANGED', 'SERP validated: INFORMATIONAL / EDITORIAL_GUIDE (Reddit #1, Guardian, jeweller journals, forums).', 'The Ethical Benefits', note=FMT)
ch(K, 'G18-0074', 'CONFIRMED', 'AI Overview qualified "Yes" + "The Ethical Benefits" section.', 'generally considered more ethical than mined diamonds')
ch(K, 'G18-0075', 'CONFIRMED', 'AI Overview "The Environmental and Ethical Concerns": high energy use, fossil-fuel grids.', 'High Energy Use')
ch(K, 'G18-0077', 'STRENGTHENED', 'AI Overview benefits list: no mining risks (land disruption, extraction labour), better labour conditions; Grown Diamond Corp snippet on child labour.', ['No Mining Risks', 'Better Labor Conditions'], note='Implied weight OPTIONAL -> IMPORTANT.')
ch(K, 'G18-0076', 'STRENGTHENED', 'AI Overview: many lab diamonds are produced in India and China on coal-based grids; buyers told to look for renewable energy / certified carbon-neutral stones.', ['India and China', 'carbon-neutral'], note='Remains BUSINESS_DEPENDENT and is now higher-stakes: HOD manufactures in Surat, India, so its energy source and any sustainability claim must be substantiated before Stage 19 uses them.')
ch(K, None, 'NEW_EVIDENCE', 'AI Overview "Lack of Regulation": fewer mandatory standards/transparency in the lab-grown sector; Cushla Whiting snippet "little transparency".', 'Lack of Regulation',
   assumption='Not in Stage 18 register for EDU-LG-07.', note='New supporting concept (trust/transparency).')
ch(K, None, 'NEW_EVIDENCE', 'AI Overview "How to Buy Responsibly": ask for origin (facility) and green energy.', 'How to Buy Responsibly',
   assumption='Not in Stage 18 register for EDU-LG-07.', note='New decision-factor concept; HOD-specific facility disclosure is BUSINESS_DEPENDENT.')
ch(K, None, 'NEW_EVIDENCE', 'AI Overview "Conflict-Free": removes risk of funding blood diamonds.', ['Conflict-Free', 'blood diamonds'],
   assumption='Stage 18 dropped "Natural conflict-free sourcing (EDU-NAT-02 conditional)" for EDU-LG-07 for lack of evidence.', note='Concept now evidenced: brief mention only; conditional owner EDU-NAT-02 unchanged.')
ch(K, None, 'NEW_EVIDENCE', 'PAA "What is the most ethical diamond?"; Cushla Whiting compares lab-grown, natural and antique.', 'What is the most ethical diamond?', conf='MEDIUM',
   assumption='Not in Stage 18 register.', note='FAQ-scale; antique/recycled options are context, not an HOD claim.')

K = 'do lab grown diamonds get cloudy'
ch(K, 'G18-0299', 'CHANGED', 'SERP validated: INFORMATIONAL / EDITORIAL_GUIDE (retailer blogs + Reddit), answer-first AI Overview.', 'Why Your Lab Diamond Might Look Cloudy', note=FMT)
ch(K, 'G18-0078', 'CONFIRMED', 'AI Overview direct "No"; 8 of 9 organic snippets say they do not cloud; PAA lifespan question.', ['do not get cloudy over time', 'What is the lifespan of a lab diamond?'])
ch(K, 'G18-0080', 'STRENGTHENED', 'PAA "Do lab diamonds lose their sparkle?"; related "lose their shine", "sparkle rainbow", "look real".', ['Do lab diamonds lose their sparkle?', 'Do lab grown diamonds lose their shine'])
ch(K, 'G18-0079', 'UNCHANGED', 'Fluorescence does not appear on this SERP.', 'lab-grown', conf='MEDIUM', note='Still keyword-only evidence (8 owned keywords); no SERP support either way.')
ch(K, 'G18-0083', 'STRENGTHENED', 'Do Amore snippet: 10/10 hardness so they never cloud; AI Overview simulant-confusion bullet.', '10/10 hardness', note='Implied weight OPTIONAL -> SUPPORTING (brief mention + link to EDU-GEN-01).')
ch(K, None, 'NEW_EVIDENCE', 'AI Overview lists causes of a cloudy look: surface buildup, cloud inclusions/low clarity, poor cut, simulant confusion.', ['Surface Buildup', 'Poor Cut Quality', 'Simulant Confusion'],
   assumption='Not in Stage 18 register for EDU-LG-08.', note='New core-supporting concept; clarity (EDU-4C-01), cut (EDU-4C-06) and simulants (EDU-LG-01) are mentioned + linked, not duplicated.')
ch(K, None, 'NEW_EVIDENCE', 'AI Overview section "How to Restore the Sparkle" (gentle cleaning, professional check); related "get dirty faster".', ['How to Restore the Sparkle', 'Do lab grown diamonds get dirty faster'],
   assumption='Stage 18 dropped "Care and cleaning to keep sparkle (EDU-RJG-03 conditional)" for lack of evidence.', note='Concept now evidenced: short care block or link; conditional owner EDU-RJG-03 unchanged.')

K = 'how are diamonds formed'
ch(K, 'G18-0300', 'CHANGED', 'SERP validated: INFORMATIONAL / EDUCATIONAL (museum, Wikipedia, naturaldiamonds.com, jeweller explainers) with Q&A feature and video.', 'Natural Formation', note=FMT)
ch(K, 'G18-0104', 'CONFIRMED', 'AI Overview "Natural Formation": depth in the mantle, heat and pressure, 1-3.3 billion years.', ['mantle', 'billion years'])
ch(K, 'G18-0105', 'STRENGTHENED', 'AI Overview "Journey to the Surface" via kimberlite pipes; related "How are diamonds formed in volcanoes".', ['kimberlite pipes', 'How are diamonds formed in volcanoes'], note='Implied weight IMPORTANT -> CRITICAL.')
ch(K, 'G18-0109', 'STRENGTHENED', 'AI Overview devotes a full section to "Lab-Grown Formation" (HPHT, CVD); related "How are diamonds formed artificially".', ['Lab-Grown Formation', 'How are diamonds formed artificially'], note='The formation SERP expects both processes. Implied weight SUPPORTING -> IMPORTANT, still a short section + link to EDU-LG-00/EDU-LG-03 (no second owner).')
ch(K, 'G18-0108', 'STRENGTHENED', 'Related "Where are diamonds found", "Where do diamonds come from country".', ['Where are diamonds found', 'Where do diamonds come from country'], note='Implied weight SUPPORTING -> IMPORTANT.')
ch(K, None, 'NEW_EVIDENCE', 'PAA "Do diamonds start as coal?"; the made-of SERP also asks "Is coal under pressure a diamond?".', 'Do diamonds start as coal?',
   assumption='Not in Stage 18 register.', note='Myth-busting FAQ owned by EDU-NAT-00 (formation); EDU-GEN-01 mentions at composition level.')
ch(K, None, 'NEW_EVIDENCE', 'PAA "How long does a diamond take to form?" and "Is the earth still creating diamonds?"; related "step by step", "for kids".', ['How long does a diamond take to form?', 'Is the earth still creating diamonds?', 'How are diamonds formed step by step'],
   assumption='Not in Stage 18 register.', note='Timescale + ongoing-formation questions; SERP evidence suggests a step sequence.')

K = '4cs of diamonds'
ch(K, 'G18-0301', 'CHANGED', 'SERP validated: INFORMATIONAL / EDUCATIONAL, authority-led (AGS, GIA 4Cs) then retailer guides; images pack at rank 2.', 'Understanding the 4Cs of Diamond Quality', note=FMT)
ch(K, 'G18-0283', 'CHANGED', 'The 4Cs head term has a validated informational SERP.', 'The 4Cs of diamonds are', note=HEADNOTE)
ch(K, 'G18-0114', 'CONFIRMED', 'AI Overview: definition, then one section per C (meaning + grade range).', 'The 4Cs of diamonds are')
ch(K, 'G18-0115', 'STRENGTHENED', 'Images pack at rank 2 (grading charts incl. GIA grading scales); related "4cs of diamonds chart".', ['4cs of diamonds chart', 'GIA Diamond Grading Scales'])
ch(K, 'G18-0117', 'STRENGTHENED', 'Related "4 C\'s of diamonds order of importance"; AI Overview: cut "most important factor for sparkle"; prompt "which of the 4Cs to prioritize".', ["order of importance", 'which of the 4Cs to prioritize'], note='Implied weight OPTIONAL -> IMPORTANT.')
ch(K, 'G18-0123', 'STRENGTHENED', 'AI Overview: universal standard established by GIA; AGS and GIA 4Cs are organic #1-#2.', 'established by the Gemological Institute of America', note='Implied weight OPTIONAL -> SUPPORTING (brief mention + link to EDU-CERT-00).')
ch(K, 'G18-0116', 'WEAKENED', 'The 4Cs head-term SERP does not mention lab-grown grading (only VRAI "created diamond" snippet).', 'created diamond', conf='MEDIUM', note='Still supported by 21 owned keywords; keep as a section, but it is not the head-term expectation. Implied weight CRITICAL -> IMPORTANT.')
for g, c, ev in [('G18-0119', 'Clarity', 'FL** (Flawless) down to **I3'), ('G18-0120', 'Color', 'Scored on a scale from **D**'), ('G18-0121', 'Cut', 'Ranging from Excellent to Poor'), ('G18-0122', 'Carat', 'One carat equals 0.2 grams')]:
    ch(K, g, 'STRENGTHENED', f'AI Overview has a dedicated "{c}" block (meaning + grade range).', ev, note='Hub needs a short per-C block with grade range + link to the owning page. Implied weight -> IMPORTANT (still brief).')
ch(K, None, 'NEW_EVIDENCE', 'PAA "What is the 5th C of diamonds?".', 'What is the 5th C of diamonds?', conf='MEDIUM',
   assumption='Not in Stage 18 register.', note='FAQ-scale; the SERP does not define it here, so Stage 19 must not assume the answer.')
ch(K, None, 'NEW_EVIDENCE', 'Budget-to-size questions: PAA "How big a diamond will $10,000 buy?", "How much is a 4 CT diamond worth?".', ['How big a diamond will $10,000 buy?', 'How much is a 4 CT diamond worth?'], conf='MEDIUM',
   assumption='Not in Stage 18 register for EDU-4C-00.', note='Price questions: no live prices on Education pages (Stage 13); treat as carat/price context (EDU-4C-07, EDU-LG-05) or BUSINESS_DEPENDENT.')

K = 'diamond color chart'
ch(K, 'G18-0287', 'CHANGED', 'The colour-chart head term has a validated informational SERP (GIA #1).', 'GIA 4Cs Color D-to-Z', note=HEADNOTE)
ch(K, 'G18-0157', 'CONFIRMED', 'AI Overview lists five grade groups (D-F, G-J, K-M, N-R, S-Z), each with appearance and value.', 'GIA Diamond Color Scale and Categories')
ch(K, 'G18-0158', 'CONFIRMED', 'AI Overview shows five chart images; Tiffany result is an image; related "Diamond color chart pdf".', ['Diamond Color Chart: The Official GIA Color Scale', 'Diamond color chart pdf'])
ch(K, 'G18-0159', 'CONFIRMED', 'AI Overview: G-J "Great balance of beauty and budget"; PAA "What is the best color of a diamond?".', 'Great balance of beauty and budget')
ch(K, 'G18-0164', 'CONFIRMED', 'Each group carries a value line; related "Diamond color chart price"; PAA "least valuable".', ['Diamond color chart price', 'Which diamond color is the least valuable?'])
ch(K, 'G18-0163', 'STRENGTHENED', 'PAA "Which diamond color is better, D or G?".', 'Which diamond color is better, D or G?')
ch(K, 'G18-0161', 'STRENGTHENED', 'AI Overview: K-M "works well with yellow or rose gold settings"; prompt asks metal type.', 'works well with yellow or rose gold settings', note='Implied weight SUPPORTING -> IMPORTANT.')
ch(K, 'G18-0118', 'STRENGTHENED', 'Related "Diamond color and clarity chart", "Diamond color chart vs1"; PAA "What is better, a VS1 or VS2 diamond?".', ['Diamond color and clarity chart', 'Diamond color chart vs1'], target='EDU-4C-00',
   note='Combined colour+clarity demand shows up on the colour SERP. Owner stays EDU-4C-00 (combos); EDU-4C-05 links. Implied weight SUPPORTING -> IMPORTANT.')
ch(K, None, 'NEW_EVIDENCE', 'AI Overview note: colours past Z or pink/blue are classified separately as "fancy colored diamonds".', 'fancy colored diamonds',
   assumption='Stage 18 dropped "Fancy colours boundary (EDU-4C-08 conditional)" for EDU-4C-05 for lack of evidence.', note='Concept now evidenced: one-line boundary note; conditional owner EDU-4C-08 unchanged.')

K = 'diamond carat size chart'
ch(K, 'G18-0302', 'CHANGED', 'SERP validated: INFORMATIONAL, image-led (images pack at rank 1), NO AI Overview, short videos; all organic results are carat-to-mm size charts.', 'Diamond Size Chart, Size of Diamonds by MM', note=FMT)
ch(K, 'G18-0289', 'CHANGED', 'The carat size-chart head term has a validated SERP.', 'Diamond Carat Size Chart', note=HEADNOTE)
ch(K, 'G18-0177', 'CONFIRMED', 'Diamond Banc snippet: carat weight, millimetre spread, face-up size; Brilliant Earth "what diamond carat weight is".', ['millimeter spread, face-up size', 'Learn what diamond carat weight is'])
ch(K, 'G18-0178', 'CONFIRMED', 'PAA "Is a 2 carat diamond a big diamond?", "What is the perfect diamond carat size?".', ['Is a 2 carat diamond a big diamond?', 'What is the perfect diamond carat size?'])
ch(K, None, 'NEW_EVIDENCE', 'Carat-to-millimetre size chart is the dominant format (Brilliance, Fascinating Diamonds, Zales, VRAI, Diamonds Factory).', ['Carat to MM Guide', 'Diamond Carat Weight Measuring Chart'],
   assumption='Stage 18 dropped "Carat size chart (mm, on hand)" for EDU-4C-07 for lack of evidence; head-term row INSUFFICIENT_EVIDENCE.', note='Now the core SERP-format expectation for EDU-4C-07 (VISUAL_CHART). Implied weight: CRITICAL.')
ch(K, None, 'NEW_EVIDENCE', 'Size in mm varies by shape (VRAI oval dimensions; Brilliance "by diamond shape").', ['by diamond shape and millimeter', 'oval-cut diamond measures'],
   assumption='Not in Stage 18 register for EDU-4C-07.', note='Shape detail stays with EDU-SHP-00; chart shows round + common shapes.')
ch(K, None, 'NEW_EVIDENCE', 'Price-by-carat / budget-to-carat demand: related "Diamond carat size chart and price", "1 carat diamond price"; PAA "How many carats is a $5000 diamond?".', ['Diamond carat size chart and price', 'How many carats is a $5000 diamond?'], conf='MEDIUM',
   assumption='Stage 18 dropped "Price by carat" for EDU-4C-07 for lack of evidence.', note='No live prices (Stage 13); concept-level price context only, or BUSINESS_DEPENDENT.')
ch(K, None, 'NEW_EVIDENCE', 'On-hand visual comparison: short videos ("on hand comparison") and related "Diamond size on hand simulator".', ['On Hand Comparison', 'Diamond size on hand simulator'], conf='MEDIUM',
   assumption='Not in Stage 18 register.', note='Format signal (visual / interactive); any tool is a business/build decision (no URL or ownership change).')

K = 'diamond cut'
ch(K, 'G18-0288', 'CHANGED', 'The cut head term has a validated SERP, but its meaning is MIXED: cut quality and shape lists.', 'Cut vs. Shape', conf='MEDIUM', note=HEADNOTE)
ch(K, 'G18-0169', 'STRENGTHENED', 'AI Overview has a "Cut vs. Shape" section and then lists popular shapes; organic includes "Top 10 Diamond Cuts" and "Diamond Shapes & Cuts"; PAA "What is a diamond cut called?".', ['Cut vs. Shape', 'Top 10 Diamond Cuts', 'What is a diamond cut called?'],
   note='Disambiguation is essential on the head term; shapes overview stays owned by EDU-SHP-00 (link, no duplicate list).')
ch(K, 'G18-0167', 'CONFIRMED', 'AI Overview "Key Cut Quality Factors": brilliance, fire, scintillation.', 'Key Cut Quality Factors')
ch(K, 'G18-0168', 'CONFIRMED', 'AI Overview: proportions; cut describes symmetry, proportions, polish.', 'Proportions')
ch(K, 'G18-0166', 'CONFIRMED', 'Organic cut-grade pages: GIA "Understanding The Cut Scale", Tiffany "Diamond Cut Grades", Blue Nile "Grading Scale".', ['Understanding The Cut Scale', 'Diamond Cut Grades'])
ch(K, 'G18-0175', 'STRENGTHENED', 'PAA "Which diamond cut is the cheapest?" repeats (also on the Stage 8 cut SERP).', 'Which diamond cut is the cheapest?', note='Implied weight OPTIONAL -> SUPPORTING (FAQ).')
ch(K, None, 'NEW_EVIDENCE', 'Non-jewellery senses of "diamond cut" in related searches (grillz, vegetables).', ['Diamond Cuts Grillz', 'Diamond cut vegetables'], conf='MEDIUM',
   assumption='Not in Stage 18 register.', note='AVOID: do not target these senses.')

K = 'diamond shapes'
ch(K, 'G18-0290', 'CHANGED', 'The plural head term has a validated jewellery-led SERP (Tiffany, GIA, Brilliant Earth, Rare Carat, Kay) with popular products.', 'Popular Diamond Shapes', note=HEADNOTE)
ch(K, 'G18-0184', 'CONFIRMED', 'AI Overview lists the same 10 shapes as Stage 8 (round brilliant to heart).', ['Round Brilliant', 'Asscher', 'Heart'])
ch(K, 'G18-0191', 'WEAKENED', 'Geometric intent is weak on the plural: 10/10 organic results are jewellery; only related "drawing", "Shape of diamond in maths", "shape name".', 'Shape of diamond in maths', note='Keep AVOID; dilution risk is lower than Stage 8 showed for the singular "diamond shape".')
ch(K, 'G18-0190', 'STRENGTHENED', 'Related "Diamond shapes chart", "Diamond shapes chart with pictures"; Tiffany "Shape Charts".', ['Diamond shapes chart with pictures', 'Shape Charts'])
ch(K, 'G18-0186', 'CONFIRMED', 'GIA "Guide to Diamond Shapes for Engagement Rings"; related "for engagement ring"; AI Overview prompt asks jewellery type.', 'Guide to Diamond Shapes for Engagement Rings')
ch(K, 'G18-0187', 'STRENGTHENED', 'AI Overview gives each shape a trait (sparkle, elongation/slimming, surface coverage per carat, hall-of-mirrors).', ['slims the finger', 'surface coverage per carat'], note='Implied weight SUPPORTING -> IMPORTANT.')
ch(K, 'G18-0188', 'STRENGTHENED', 'PAA "Which shape of diamond is most expensive?".', 'Which shape of diamond is most expensive?', note='Implied weight SUPPORTING -> IMPORTANT.')
ch(K, 'G18-0194', 'STRENGTHENED', 'Popular products unit on the shapes SERP.', 'popular_products', note='Remains BUSINESS_DEPENDENT (shape filters / catalogue).')
ch(K, None, 'NEW_EVIDENCE', 'AI Overview decision prompt: "maximum sparkle (brilliant cut) or a clear, elegant gleam (step cut)".', 'step cut',
   assumption='Not in Stage 18 register for EDU-SHP-00.', note='New decision factor: brilliant vs step-cut appearance.')

K = 'diamond certificate'
ch(K, 'G18-0291', 'CHANGED', 'SERP validated: MIXED - lab navigational (IGI homepage #1, GIA service page) plus editorial guides; popular products are Etsy certificate listings.', 'IGI: Diamond Certification', conf='MEDIUM', note=HEADNOTE)
ch(K, 'G18-0195', 'CONFIRMED', 'AI Overview definition: official grading report from an independent gemological laboratory.', 'an official grading report issued by an independent gemological laboratory')
ch(K, 'G18-0198', 'CONFIRMED', 'AI Overview "What is Included": 4Cs, measurements, polish, symmetry, fluorescence, origin, laser inscription.', ['What is Included', 'Laser inscription'])
ch(K, 'G18-0197', 'CONFIRMED', 'AI Overview "Top Grading Laboratories": GIA, IGI, AGS.', 'Top Grading Laboratories')
ch(K, 'G18-0196', 'CONFIRMED', 'AI Overview: origin disclosure (natural or laboratory-grown); IGI grades both.', 'natural or laboratory-grown')
ch(K, 'G18-0199', 'STRENGTHENED', 'PAA "How do I check my diamond certificate?"; related "Diamond certificate lookup", "IGI Diamond Certificate check", "GIA diamond Certificate Check".', ['How do I check my diamond certificate?', 'Diamond certificate lookup'])
ch(K, 'G18-0203', 'CONFIRMED', 'PAA "What are the top 5 diamond certifications?".', 'What are the top 5 diamond certifications?', note='Lab-ranking depth stays on EDU-CERT-01 (brief mention + link).')
ch(K, 'G18-0205', 'STRENGTHENED', 'AI Overview prompt: natural or lab-grown; which certification matters for your purchase.', 'which certification matters most for your purchase', note='Remains BUSINESS_DEPENDENT (which labs grade HOD stones).')
ch(K, None, 'NEW_EVIDENCE', 'PAA "How do you get a diamond certificate?" (process of having a stone graded).', 'How do you get a diamond certificate?',
   assumption='Not in Stage 18 register.', note='New process question for EDU-CERT-00.')
ch(K, None, 'NEW_EVIDENCE', 'Lab navigational results (IGI homepage, GIA service page) rank at the top.', ['www.igi.org', 'Natural Diamond Grading Reports & Services'], conf='MEDIUM',
   assumption='Stage 18 expected an editorial certification SERP.', note='SERP-format signal: do not compete with the labs\' own pages; cite and link to official lab verification tools (trust).')
ch(K, None, 'NEW_EVIDENCE', 'Jared snippet: a certificate can serve as identification in case of loss or theft.', 'identification in case of loss or theft', conf='MEDIUM',
   assumption='Not in Stage 18 register.', note='Supporting benefit (insurance/identification).')

K = '14k vs 18k gold'
ch(K, 'G18-0293', 'CHANGED', 'The comparison head term has a validated COMPARISON SERP.', 'The main difference between 14k and 18k gold is purity', note=HEADNOTE)
for g, ev in [('G18-0228', 'Purity and Composition'), ('G18-0230', 'Color and Appearance'), ('G18-0229', 'Durability and Wear'), ('G18-0231', 'Price and Value'),
              ('G18-0233', 'A Side-by-Side Comparison of 14K vs. 18K Gold'), ('G18-0236', 'higher intrinsic metal value')]:
    ch(K, g, 'CONFIRMED', f'AI Overview / organic: "{ev}".', ev)
ch(K, 'G18-0234', 'STRENGTHENED', 'AI Overview section "Hypoallergenic Properties" (14k may contain nickel; 18k more hypoallergenic).', 'Hypoallergenic Properties', note='Dedicated section on the head-term SERP.')
ch(K, None, 'NEW_EVIDENCE', 'PAA "Can gold be fake if it says 14k?" (stamps/hallmarks and authenticity).', 'Can gold be fake if it says 14k?', conf='MEDIUM',
   assumption='Not in Stage 18 register.', note='FAQ-scale for EDU-MET-01.')
ch(K, None, 'NEW_EVIDENCE', 'Related "14k vs 18k white gold", "14k vs 18k gold vs platinum".', ['14k vs 18k white gold', '14k vs 18k gold vs platinum'], conf='MEDIUM', target='EDU-MET-00',
   assumption='Not in Stage 18 register.', note='Cross-page: white gold / platinum comparison owned by EDU-MET-00; EDU-MET-01 links.')

K = 'white gold vs platinum'
ch(K, 'G18-0292', 'CHANGED', 'The comparison head term has a validated COMPARISON SERP.', 'Key Differences', note=HEADNOTE)
ch(K, 'G18-0217', 'CONFIRMED', 'AI Overview "Key Differences": composition, price, maintenance, skin sensitivity; PAA "Which is better, platinum or white gold?".', ['Which is better, platinum or white gold?', 'Composition'])
ch(K, 'G18-0218', 'STRENGTHENED', 'AI Overview: white gold needs rhodium re-plating every few years.', 're-plating with rhodium', note='Rhodium is a core dimension of this comparison; interim home EDU-MET-00 unchanged.')
ch(K, 'G18-0219', 'STRENGTHENED', 'AI Overview "Skin Sensitivity": platinum hypoallergenic, white gold may contain nickel.', 'Skin Sensitivity')
ch(K, 'G18-0227', 'STRENGTHENED', 'AI Overview prompt: engagement ring or wedding band; upfront cost vs long-term maintenance.', 'lower upfront cost', note='Remains BUSINESS_DEPENDENT (HOD metal options).')
ch(K, None, 'NEW_EVIDENCE', 'Platinum patina and scratching vs white gold wear: AI Overview "patina"; related "White gold vs platinum scratch", "durability"; Brilliant Earth "platinum is softer".', ['patina', 'White gold vs platinum scratch'],
   assumption='Not in Stage 18 register.', note='New attribute (DURABILITY/CARE) for the white-gold-vs-platinum comparison.')
ch(K, None, 'NEW_EVIDENCE', 'PAA "What are the disadvantages of platinum?", "What is the disadvantage of white gold?".', ['What are the disadvantages of platinum?', 'What is the disadvantage of white gold?'],
   assumption='Not in Stage 18 register.', note='SERP evidence suggests pros/cons per metal.')

K = 'engagement ring settings'
ch(K, 'G18-0294', 'CONFLICT', 'Head-term SERP is MIXED and commercial-led: shop pages (Kesslers, Friendly Diamonds, Robbins Brothers "setting only", KayOutlet Design-A-Ring), local pack, popular products, AI Overview "Shopping for Settings"; editorial guides rank lower.', ['Shop Engagement Ring Settings', 'Shopping for Settings', 'Engagement ring setting only no stone'],
   note='Stage 18 treated this as an unmeasured Education head term for EDU-RJG-01. It is largely transactional. Stage 15 ownership is NOT changed here; flag for a Stage 15-style review. EDU-RJG-01 keeps its validated editorial query ("types of diamond settings").')
ch(K, 'G18-0241', 'CONFIRMED', 'AI Overview lists setting types: solitaire, halo, pavé, bezel, three-stone, cathedral.', ['Solitaire', 'Cathedral'], note='Adds solitaire and cathedral to the entities evidenced in Stage 8 (prong, bezel, pavé, halo, channel, tension, three-stone).')
ch(K, 'G18-0242', 'CONFIRMED', 'AI Overview: bezel "snag-free profile ideal for active lifestyles"; prompt asks lifestyle; PAA "Which setting is best for an engagement ring?".', ['ideal for active lifestyles', 'Which setting is best for an engagement ring?'])
ch(K, 'G18-0243', 'STRENGTHENED', 'Related "Engagement ring settings chart", "Engagement ring settings types".', 'Engagement ring settings chart')
ch(K, 'G18-0251', 'STRENGTHENED', 'Transactional "setting only / no stone" demand and design-your-own pages.', ['Engagement ring settings only', 'Design-A-Ring'], note='Remains BUSINESS_DEPENDENT: does HOD sell settings without a centre stone or a design-your-own flow?')
ch(K, None, 'NEW_EVIDENCE', 'PAA "What is the most popular setting for an engagement ring?"; related "Engagement ring settings for round diamond".', ['What is the most popular setting for an engagement ring?', 'Engagement ring settings for round diamond'], conf='MEDIUM',
   assumption='Not in Stage 18 register.', note='Popularity + setting-by-shape questions (FAQ / inline).')

for K in ('ring size chart', 'how to measure ring size'):
    first = K == 'ring size chart'
    if first:
        ch(K, 'G18-0303', 'CHANGED', 'SERP validated: INFORMATIONAL / EDITORIAL_GUIDE with printable-PDF sizers; AI Overview includes a US size table.', 'US Ring Size Chart (Circumference & Diameter)', note=FMT)
        ch(K, 'G18-0295', 'CHANGED', 'Ring-size head terms have validated SERPs (chart and measuring).', 'Ring Size Chart & Guide', note=HEADNOTE)
        ch(K, 'G18-0253', 'STRENGTHENED', 'AI Overview is built around a US size / inner circumference / inner diameter (mm) table.', ['Inner Circumference (mm)', 'Inner Diameter (mm)'], note='Implied weight IMPORTANT -> CRITICAL (VISUAL_CHART).')
        ch(K, 'G18-0255', 'STRENGTHENED', 'Related "Ring size chart men", "Ring size chart women"; Jewlr average sizes; AI Overview prompt men\'s/women\'s.', ['Ring size chart men', 'average ring size for women'], note='Implied weight SUPPORTING -> IMPORTANT.')
        ch(K, 'G18-0258', 'STRENGTHENED', 'Related "Ring sizer"; PAA "Is there a virtual ring sizer?", "Can I measure my ring size on my phone?"; printable PDF sizers (Macy\'s, UCF, James Avery).', ['Is there a virtual ring sizer?', 'Print your ring sizer'], note='Implied weight SUPPORTING -> IMPORTANT; tool embedded by default (Stage 14/15), EDU-RJG-05 still conditional.')
        ch(K, None, 'NEW_EVIDENCE', 'International and unit conversions: related "Ring size chart EU", "in cm", "in inches", "in mm".', ['Ring size chart EU', 'Ring size chart in inches'],
           assumption='Not in Stage 18 register.', note='New attribute (SIZE systems/conversions) for EDU-RJG-02.')
    else:
        ch(K, 'G18-0252', 'STRENGTHENED', 'AI Overview: 7 numbered paper/string steps + existing-ring method; video and short-video units; both ring-size SERPs.', ['Measuring with Paper or String', 'Measuring an Existing Ring'], note='Implied weight IMPORTANT -> CRITICAL (STEP_SEQUENCE).')
        ch(K, 'G18-0256', 'STRENGTHENED', 'Both AI Overviews: wide/thick bands fit tighter, go up half a size.', 'Consider band width', note='Implied weight SUPPORTING -> IMPORTANT.')
        ch(K, 'G18-0254', 'WEAKENED', 'Resizing does not appear on either ring-size SERP (AI Overview, PAA, related).', 'ring size', conf='MEDIUM', target='EDU-RJG-02',
           note='Still owned via resizing keywords, so keep a section; but it is not the head-term expectation. Implied weight CRITICAL -> IMPORTANT.')
        ch(K, None, 'NEW_EVIDENCE', 'AI Overview "Tips for Accuracy": measure later in the day, avoid cold, band width; round up between sizes (chart SERP).', 'Tips for Accuracy',
           assumption='Not in Stage 18 register.', note='New supporting concept (accuracy tips).')
        ch(K, None, 'NEW_EVIDENCE', 'Size-to-dimension questions: PAA "How big is a 7 ring size?", "How big is a size 9 ring in inches?".', ['How big is a 7 ring size?', 'How big is a size 9 ring in inches?'],
           assumption='Not in Stage 18 register.', note='Answered by the chart; FAQ/inline.')

K = 'what are diamonds made of'
ch(K, 'G18-0304', 'CHANGED', 'SERP validated: INFORMATIONAL / EDUCATIONAL (GIA #1, Wikipedia, ASU, university and jeweller explainers).', 'Elemental and Atomic Structure', note=FMT)
ch(K, 'G18-0260', 'CONFIRMED', 'AI Overview: made of a single pure element, carbon (about 99.95%).', 'a single pure element')
ch(K, 'G18-0261', 'CONFIRMED', 'AI Overview: crystal lattice, each carbon bonded to four others.', 'Crystal Lattice')
ch(K, 'G18-0262', 'CONFIRMED', 'AI Overview: strong covalent bonding creates the hardest known natural material.', 'hardest known natural material', conf='MEDIUM')
ch(K, 'G18-0270', 'STRENGTHENED', 'AI Overview section "How They Compare to Other Carbon Forms" (graphite); ASU and Greenwich snippets.', ['Graphite Connection', 'How They Compare to Other Carbon Forms'], note='Implied weight OPTIONAL -> SUPPORTING.')
ch(K, None, 'NEW_EVIDENCE', 'Trace elements: remaining ~0.05% nitrogen or boron (GIA, Rare Carat: nitrogen can turn a diamond yellow).', ['nitrogen or boron', 'Nitrogen'],
   assumption='Not in Stage 18 register.', note='Links composition to colour (EDU-4C-05) and diamond types (EDU-GEN-02 conditional).')
ch(K, None, 'NEW_EVIDENCE', 'PAA "Is coal under pressure a diamond?" (coal myth, also on the formation SERP).', 'Is coal under pressure a diamond?', conf='MEDIUM', target='EDU-NAT-00',
   assumption='Not in Stage 18 register.', note='Owner EDU-NAT-00 (formation); EDU-GEN-01 mentions at composition level.')
ch(K, None, 'NEW_EVIDENCE', 'PAA "What is a poor man\'s diamond called?" and "Is a diamond rarer than gold?".', ["What is a poor man's diamond called?", 'Is a diamond rarer than gold?'], conf='LOW',
   assumption='Not in Stage 18 register.', note='Adjacent: simulants (EDU-GEM-00 conditional) and rarity (EDU-NAT-01 conditional); FAQ-scale at most.')

CCOLS = ['keyword', 'stage18_reference', 'stage18_assumption', 'new_evidence', 'change_type', 'affected_target_id', 'affected_gap_id', 'confidence', 'notes']
with open(P('serp', 'analysis', '18_5_stage18_change_log.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=CCOLS)
    w.writeheader()
    w.writerows(CH)

stats = dict(queries=len(S), task_post_cost=POST['cost'], task_post_tasks=POST['tasks_count'], task_post_errors=POST['tasks_error'],
             change_types=dict(collections.Counter(r['change_type'] for r in CH)), change_rows=len(CH),
             targets_touched=sorted({r['affected_target_id'] for r in CH}),
             ai_overview=sum(v['ai_overview'] == 'YES' for v in VAL), paa=sum(v['paa'] == 'YES' for v in VAL),
             shopping=sum(v['shopping'] == 'YES' for v in VAL), video=sum(v['video'] == 'YES' for v in VAL), images=sum(v['images'] == 'YES' for v in VAL),
             local_pack=sum(v['local_pack'] == 'YES' for v in VAL), featured_snippet=sum(v['featured_snippet'] == 'YES' for v in VAL),
             intents=dict(collections.Counter(v['validated_intent'] for v in VAL)), page_types=dict(collections.Counter(v['dominant_page_type'] for v in VAL)))
json.dump(stats, open(P('scripts', '18_5_build_stats.json'), 'w'), indent=1)
print(json.dumps(stats, indent=1))
