#!/usr/bin/env python3
"""Stage 15 — keyword → URL mapping (local files only; no API calls).

Builds:
  architecture/15_keyword_url_map.csv            one row per Stage 7 keyword (1,936)
  architecture/15_target_page_registry.csv       one row per target page that owns keywords
  architecture/15_cluster_page_map.csv           one row per Stage 11 cluster (89)
  architecture/15_cannibalization_check.csv      systematic checks A-E + special checks
  content-strategy/15_ranking_equity_protection.csv   all 28 Stage 3 ranking keywords
  architecture/15_keyword_url_mapping_summary.md

Inputs (read-only): Stage 7 master DB, Stage 8 validation, Stage 10 keyword coverage,
Stage 11 cluster map/registry, Stage 12 IA, Stage 13 decisions/equity, Stage 14 architecture
and consolidation.

Order of precedence used for every keyword:
  1. Stage 11 status (NOISE / COMPETITOR_BRAND / UNCLUSTERED_REVIEW)
  2. Explicit keyword-level override (KW_RULES below) — each carries its reason
  3. Stage 14 PRIMARY decision for the keyword's cluster, with Stage 14 SECONDARY
     rows used for interim homes and sub-topic splits (CLUSTER_RULES below)
"""
import csv, collections, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
P = lambda *a: os.path.join(ROOT, *a)
SITE = 'https://www.houseofdiams.com'


def rd(path):
    with open(P(path), newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def wr(path, cols, rows):
    with open(P(path), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, '') for c in cols})


def vol(x):
    try:
        return int(float(x))
    except (TypeError, ValueError):
        return 0


rel = lambda u: u.replace(SITE, '') if u else u

# ---------------------------------------------------------------- inputs
master = rd('dataforseo/processed/07_hod_master_keyword_database.csv')
cmap = {r['keyword']: r for r in rd('clusters/11_keyword_cluster_map.csv')}
creg = {r['cluster_id']: r for r in rd('clusters/11_cluster_registry.csv')}
serp = {r['keyword']: r for r in rd('serp/analysis/08_hod_serp_validation.csv')}
arch = {r['topic_id']: r for r in rd('architecture/14_education_architecture.csv')}
cons = rd('architecture/14_education_cluster_consolidation.csv')
cons_primary = {r['cluster_id']: r for r in cons if r['assignment_role'] == 'PRIMARY'}
cons_secondary = collections.defaultdict(list)
for r in cons:
    if r['assignment_role'] == 'SECONDARY':
        cons_secondary[r['cluster_id']].append(r)
equity = rd('content-strategy/13_ranking_equity_analysis.csv')
cov = collections.defaultdict(list)
for r in rd('content-strategy/10_content_keyword_coverage.csv'):
    if r['url']:
        cov[r['keyword']].append(rel(r['url']))

# ---------------------------------------------------------------- target pages
# Existing URLs (Stage 10/13 inventory) and proposed URL expressions (Stage 15, from Stage 12 D-12
# principles). Proposed expressions are NOT implemented; the path prefix depends on the platform
# (Stage 12 D-17). URL_PENDING = slug not settled (provisional topic, or hub label/spelling open).
U_CVD = '/blog/cvd-vs-hpht-lab-grown-diamonds-what-buyers-should-know-house-of-diams'
U_LVN = '/blog/lab-grown-vs-natural-diamonds-the-honest-comparison-house-of-diams'
U_REAL = '/blog/are-lab-grown-diamonds-real-a-complete-buyer-s-guide'
U_4CS = '/blog/the-4cs-of-lab-grown-diamonds-explained-cut-colour-clarity-and-carat-house-of-diams'
U_SHP = '/blog/the-best-lab-grown-diamond-shapes-for-engagement-rings-house-of-diams'
U_IGI = '/blog/igi-certification-for-lab-grown-diamonds-what-it-means-house-of-diams'
U_GVI = '/education/lab-grown-diamond-certification-explained-gia-vs-igi-house-of-diams'
U_14K = '/blog/14k-vs-18k-gold-for-diamond-jewellery-which-is-better-house-of-diams'
U_CHO = '/blog/how-to-choose-a-lab-grown-diamond-the-complete-buyer-s-guide'
U_RSZ = '/blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-house-of-diams'
U_SIDE = '/engagement-rings/by-desgin/side-stone-rings'
U_PDP = '/shop/oval-floral-diamond-ring'

PENDING = 'URL_PENDING'
# target_id: (name, page_type, hub, status, existing_url, proposed_url, url_status, stage14_source, notes)
TARGETS = {
    'EDU-LG-00': ('Lab-grown diamonds explained (Lab-Grown Education hub pillar)', 'EDUCATION_TOPIC_HUB_PILLAR', 'Lab-Grown Diamonds', 'PROPOSED', '', '/education/lab-grown-diamonds', 'PROPOSED_URL', 'D14-03; D14-05', 'Must not target the commercial head terms (CL-001). Slug is the hub name; Education hub name is firm (D14-02).'),
    'EDU-LG-01': ('Are lab-grown diamonds real? (authenticity)', 'EDUCATION_ARTICLE', 'Lab-Grown Diamonds', 'EXISTING_MOVE_WHEN_CONDITIONS_MET', U_REAL, '/education/lab-grown-diamonds/are-lab-grown-diamonds-real', 'EXISTING_MOVE_WHEN_CONDITIONS_MET', 'D14-07; D14-26', 'Existing blog URL owns the topic now. Move only under Stage 13 conditions (Lab-Grown hub live; 1:1 301). Proposed URL is the future destination expression.'),
    'EDU-LG-02': ('Lab-grown vs natural diamonds (comparison)', 'COMPARISON_GUIDE', 'Lab-Grown Diamonds', 'EXISTING_KEEP', U_LVN, '', 'EXISTING_KEEP', 'D14-07; D14-09; D14-26', 'Stage 13 DO_NOT_MOVE_NOW (HIGH risk). Also the interim home for CL-012 (worth-it pros/cons).'),
    'EDU-LG-03': ('CVD vs HPHT (single home for CVD and HPHT)', 'COMPARISON_GUIDE', 'Lab-Grown Diamonds', 'EXISTING_KEEP', U_CVD, '', 'EXISTING_KEEP', 'D14-06; D14-26', 'Stage 13 DO_NOT_MOVE_NOW (HIGH risk). Single home for CL-016/017/018. No separate CVD or HPHT page.'),
    'EDU-LG-05': ('Lab-grown diamond price, value & resale', 'EDUCATION_ARTICLE', 'Lab-Grown Diamonds', 'PROPOSED_PROVISIONAL', '', PENDING, PENDING, 'D14-10', 'Provisional topic (LOW evidence). Candidate slug: /education/lab-grown-diamonds/lab-grown-diamond-value.'),
    'EDU-LG-07': ('Lab-grown diamond ethics & sustainability', 'EDUCATION_ARTICLE', 'Lab-Grown Diamonds', 'PROPOSED_PROVISIONAL', '', PENDING, PENDING, 'D14-11', 'Provisional topic. Candidate slug: /education/lab-grown-diamonds/are-lab-grown-diamonds-ethical.'),
    'EDU-LG-08': ('Lab-grown diamond appearance & durability', 'EDUCATION_ARTICLE', 'Lab-Grown Diamonds', 'PROPOSED_PROVISIONAL', '', PENDING, PENDING, 'D14-16', 'Provisional topic. Candidate slug: /education/lab-grown-diamonds/lab-grown-diamond-appearance.'),
    'EDU-LG-09': ('Detecting lab-grown diamonds (testers & identification)', 'EDUCATION_ARTICLE', 'Lab-Grown Diamonds', 'PROPOSED_PROVISIONAL', '', PENDING, PENDING, 'D14-13', 'Provisional topic. Candidate slug: /education/lab-grown-diamonds/do-lab-grown-diamonds-pass-a-diamond-tester.'),
    'EDU-LG-10': ('How to choose a lab-grown diamond (buying guide)', 'BUYING_GUIDE', 'Lab-Grown Diamonds', 'EXISTING_KEEP_MIGRATION_DEFERRED', U_CHO, PENDING, 'EXISTING_KEEP', 'D14-24; D14-26', 'Topic PROPOSED in Stage 14; the existing article ranks (pos 35). Migration DEFERRED by Stage 13 pending D-19 (boundary with EDU-RJG-04).'),
    'EDU-NAT-00': ('Natural diamonds: formation & origin (Natural Education hub pillar)', 'EDUCATION_TOPIC_HUB_PILLAR', 'Natural Diamonds', 'PROPOSED_PROVISIONAL', '', PENDING, PENDING, 'D14-19', 'Provisional hub (LOW evidence). Candidate slug: /education/natural-diamonds. Must not target natural commercial head terms (CL-070/071).'),
    'EDU-4C-00': ('The 4Cs of diamond quality (4Cs hub pillar, incl. lab-grown grading)', 'EDUCATION_TOPIC_HUB_PILLAR', 'Diamond Quality (4Cs)', 'EXISTING_MOVE_WHEN_CONDITIONS_MET', U_4CS, '/education/diamond-4cs', 'EXISTING_MOVE_WHEN_CONDITIONS_MET', 'D14-14; D14-15', 'Existing 4Cs-of-lab-grown article becomes the general 4Cs pillar; no separate lab-grown 4Cs page.'),
    'EDU-4C-01': ('Diamond clarity guide', 'EDUCATION_ARTICLE', 'Diamond Quality (4Cs)', 'PROPOSED', '', '/education/diamond-4cs/diamond-clarity', 'PROPOSED_URL', 'D14-14', 'Owns the clarity scale, best clarity, inclusions, cross-grade comparisons; interim home for VS (CL-042).'),
    'EDU-4C-02': ('SI clarity diamonds (SI1, SI2, SI3)', 'GRADE_EXPLAINER', 'Diamond Quality (4Cs)', 'PROPOSED', '', '/education/diamond-4cs/si-clarity-diamonds', 'PROPOSED_URL', 'D14-14', 'HIGH evidence (two SI2 SERPs share 7 URLs; 0 with clarity scale).'),
    'EDU-4C-03': ('VVS, IF & flawless clarity diamonds', 'GRADE_EXPLAINER', 'Diamond Quality (4Cs)', 'PROPOSED', '', '/education/diamond-4cs/vvs-diamonds', 'PROPOSED_URL', 'D14-14; D14-15', "Head 'v v s diamond' 18,100 (EDITORIAL_GUIDE)."),
    'EDU-4C-05': ('Diamond color guide (D to Z)', 'EDUCATION_ARTICLE', 'Diamond Quality (4Cs)', 'PROPOSED', '', '/education/diamond-4cs/diamond-color', 'PROPOSED_URL', 'D14-14', "US spelling 'color' in the slug (US market; D-15 inference; keywords use 'color')."),
    'EDU-4C-06': ('Diamond cut guide (cut grade, facets, light performance)', 'EDUCATION_ARTICLE', 'Diamond Quality (4Cs)', 'PROPOSED', '', '/education/diamond-4cs/diamond-cut', 'PROPOSED_URL', 'D14-02; D14-14', 'Cut grade split from Shapes (D14-02). Shapes pillar must not target cut-grade queries.'),
    'EDU-4C-07': ('Diamond carat guide', 'EDUCATION_ARTICLE', 'Diamond Quality (4Cs)', 'PROPOSED_PROVISIONAL', '', PENDING, PENDING, 'D14-14', 'Provisional (LOW evidence; page type untested, D14-29 #12). Candidate slug: /education/diamond-4cs/diamond-carat.'),
    'EDU-SHP-00': ('Diamond shapes guide (Shapes hub pillar, incl. engagement-ring shape choice)', 'DIAMOND_SHAPE_GUIDE', 'Diamond Shapes', 'EXISTING_MOVE_WHEN_CONDITIONS_MET', U_SHP, '/education/diamond-shapes', 'EXISTING_MOVE_WHEN_CONDITIONS_MET', 'D14-17', 'Per-shape pages DEFERRED (EDU-SHP-01). Inventory/brand-led shape SERPs are not targeted here.'),
    'EDU-CERT-00': ('Diamond certification explained (Certification hub pillar)', 'CERTIFICATION_GUIDE', 'Certification & Grading Reports', 'EXISTING_RETARGET_THEN_MOVE', U_IGI, '/education/diamond-certification', 'EXISTING_RETARGET_THEN_MOVE', 'D14-18', 'IGI blog retargeted to general certification (CL-033); GIA and IGI report questions are sections. Ships together with the GIA-vs-IGI narrowing (Stage 13). No IGI-only page.'),
    'EDU-CERT-01': ('GIA vs IGI (comparison)', 'COMPARISON_GUIDE', 'Certification & Grading Reports', 'EXISTING_KEEP', U_GVI, '', 'EXISTING_KEEP', 'D14-18', 'Already in /education; update in place, narrowed to comparison intent. Slug contains a brand suffix (D-12) but has 0 rankings; any slug change is an implementation-stage choice with a 1:1 301, not recommended here.'),
    'EDU-MET-00': ('Jewelry metals guide (Metals hub pillar)', 'EDUCATION_TOPIC_HUB_PILLAR', 'Metals & Materials', 'PROPOSED_PROVISIONAL', '', PENDING, PENDING, 'D14-21', 'Provisional hub. Candidate slug: /education/jewelry-metals (spelling per D-15). Interim home for rhodium (CL-111).'),
    'EDU-MET-01': ('14k vs 18k gold (and 10k)', 'COMPARISON_GUIDE', 'Metals & Materials', 'EXISTING_MOVE_WHEN_CONDITIONS_MET', U_14K, PENDING, 'EXISTING_MOVE_WHEN_CONDITIONS_MET', 'D14-21; D14-26', 'Moves only once the Metals section exists (Stage 13). Future slug pending because the Metals hub slug is provisional. Candidate: /education/{metals-hub}/14k-vs-18k-gold.'),
    'EDU-RJG-01': ('Ring settings guide', 'EDUCATION_ARTICLE', 'Ring & Jewellery Guides', 'PROPOSED', '', PENDING, PENDING, 'D14-22', 'Topic PROPOSED; slug pending because the hub label/spelling is open (Stage 12 D-15). Candidate: /education/{ring-guides-hub}/ring-settings.'),
    'EDU-RJG-02': ('Ring size guide (tool embedded by default)', 'PRACTICAL_GUIDE', 'Ring & Jewellery Guides', 'EXISTING_MOVE_WHEN_CONDITIONS_MET', U_RSZ, PENDING, 'EXISTING_MOVE_WHEN_CONDITIONS_MET', 'D14-22; D14-23', 'Future slug pending (hub label, D-15). Candidate: /education/{ring-guides-hub}/ring-size-guide. Tool (EDU-RJG-05) is not a separate target.'),
    'EDU-GEN-01': ('Diamond properties: composition, hardness & durability', 'EDUCATION_ARTICLE', 'Education root (no hub)', 'PROPOSED_PROVISIONAL', '', PENDING, PENDING, 'D14-25', 'Provisional root-level article; none of its clusters is SERP-validated. Candidate slug: /education/diamond-properties.'),
    'COM-ER-SIDESTONE': ('Engagement rings: side-stone (style subcategory)', 'SUBCATEGORY', 'Engagement Rings (commercial)', 'EXISTING_KEEP', U_SIDE, PENDING, 'EXISTING_KEEP', 'Stage 12 D-03; Stage 14 D14-22', 'Only style subcategory that passes the D-07 gate. Stage 12 D-03 removes the grouping segment in the future hierarchy; that path change is implementation (1:1 301), not recommended as a stand-alone change here.'),
    'COM-PDP-OVAL-FLORAL': ('Oval floral diamond ring (product page)', 'PRODUCT_DETAIL_PAGE', 'Shop (commercial)', 'EXISTING_KEEP', U_PDP, '', 'EXISTING_KEEP', 'Stage 12 (PDP); Stage 14 D14-17', "Ranks for 'marquise oval diamond' (PRODUCT SERP). Commercial; not an Education target."),
}

# Stage 14 topic → owning target when the topic is mapped directly
TOPIC_TARGET = {t: t for t in TARGETS if t.startswith('EDU-')}

# ---------------------------------------------------------------- dispositions
D_EX, D_PROP, D_KEEP, D_INT = 'MAP_EXISTING_URL', 'MAP_PROPOSED_URL', 'MAP_EXISTING_URL_KEEP', 'MAP_INTERIM_HOME'
D_COND, D_DEF = 'CONDITIONAL_NOT_MAPPED', 'DEFERRED_NOT_MAPPED'
D_XCOM, D_XNOISE, D_XBRAND, D_XOFF, D_REV = 'EXCLUDE_COMMERCIAL', 'EXCLUDE_NOISE', 'EXCLUDE_COMPETITOR_BRAND', 'EXCLUDE_OFF_SCOPE', 'REVIEW_REQUIRED'
DISPOSITIONS = [D_EX, D_PROP, D_KEEP, D_INT, D_COND, D_DEF, D_XCOM, D_XNOISE, D_XBRAND, D_XOFF, D_REV]


def disp_for_target(tid, interim=False):
    if interim:
        return D_INT
    st = TARGETS[tid][6]
    if st == 'EXISTING_KEEP':
        return D_KEEP
    if st.startswith('EXISTING'):
        return D_EX
    return D_PROP


# Cluster-level rules derived from Stage 14 consolidation (PRIMARY/SECONDARY).
# Values: ('TARGET', tid) | ('INTERIM', tid) | (disposition, note)
CLUSTER_RULES = {
    # commercial / non-Education clusters (Stage 14 EXCLUDE_NOT_EDUCATION / EXCLUDE_OFF_SCOPE)
    'CL-001': (D_COND, 'Commercial head terms; owner is the CONDITIONAL commercial Lab-Grown hub (Stage 12 D-05; Stage 14 D14-05). Not Education.'),
    'CL-005': (D_XCOM, 'Location-modified commercial queries; location pages NOT_PROPOSED (Stage 12 D-16; Stage 14).'),
    'CL-006': (D_DEF, 'Carat-led loose-stone shopping (CATEGORY SERP); loose-diamond/carat pages INSUFFICIENT EVIDENCE — DEFER (Stage 12).'),
    'CL-007': (D_DEF, 'Wholesale/trade; Stage 12 wholesale section INSUFFICIENT EVIDENCE — DEFER (business question 4).'),
    'CL-014': (D_DEF, 'History & market trends are time-bound: Blog is primary (Stage 13 framework; Stage 14 D14-12). No Blog article is planned yet.'),
    'CL-026': (D_DEF, 'Industry/factory/business terms: Blog/brand content (Surat manufacturing story), Stage 14 D14-12. No Blog article planned yet.'),
    'CL-063': (D_DEF, 'Elongated-cut (moval / marquise-oval) shopping: PRODUCT SERP; shape landing pages deferred (Stage 12 D-08; Stage 14 D14-17).'),
    'CL-070': (D_DEF, 'Natural head terms: BRAND/retailer SERPs; commercial Natural hub INSUFFICIENT EVIDENCE — DEFER (Stage 12 D-05; Stage 14 D14-19).'),
    'CL-071': (D_XCOM, 'Raw/rough diamond selling: CATEGORY SERPs of rough-diamond sellers; not an HOD product line (Stage 14 D14-19).'),
    'CL-084': (D_XOFF, 'Synonym/thesaurus queries; no jewelry need (Stage 14 EXCLUDE_OFF_SCOPE).'),
    'CL-104': (D_XCOM, 'Morganite rings: CATEGORY SERP; gemstone categories NOT_PROPOSED (Stage 12 D-16; Stage 14).'),
    'CL-105': (D_XCOM, 'Coloured-gemstone ring shopping; not in catalogue; NOT_PROPOSED (Stage 12 D-16; Stage 14).'),
    'CL-114': (D_XOFF, 'Novelty/alternative-material rings; outside a luxury diamond business (Stage 14 EXCLUDE_OFF_SCOPE).'),
    'CL-120': ('TARGET', 'COM-ER-SIDESTONE'),
    'CL-123': (D_DEF, 'Mixed-metal ring shopping: CATEGORY SERP; Fine Jewellery > Rings (incl. mixed-metal) INSUFFICIENT EVIDENCE — DEFER (Stage 12).'),
    'CL-125': (D_COND, 'Stud-earring shopping; Earrings > Studs subcategory is PROPOSED_CONDITIONAL (Stage 12 D-07 gate). Not Education (Stage 14).'),
    # Education: conditional topics with an explicit Stage 14 interim home
    'CL-012': ('INTERIM', 'EDU-LG-02'),
    'CL-015': ('INTERIM', 'EDU-LG-00'),   # method-specific members → EDU-LG-03 via KW rule
    'CL-034': ('INTERIM', 'EDU-CERT-00'),
    'CL-042': ('INTERIM', 'EDU-4C-01'),
    'CL-111': ('INTERIM', 'EDU-MET-00'),
    # Education: conditional without interim home
    'CL-051': (D_COND, 'Fancy-coloured diamonds: EDU-4C-08 CONDITIONAL (business value depends on a fancy-colour offering).'),
    'CL-065': (D_COND, "'Types of diamonds' sense unresolved: EDU-GEN-02 CONDITIONAL (D14-25; D14-29 #13)."),
    'CL-073': (D_COND, 'Conflict-free sourcing: EDU-NAT-02 CONDITIONAL (needs a substantiated HOD sourcing policy; D14-11).'),
    'CL-076': (D_COND, 'Natural value/rarity: EDU-NAT-01 CONDITIONAL (D14-19).'),
    'CL-085': (D_COND, 'General diamond investment: EDU-NAT-01 CONDITIONAL (D14-19).'),
    'CL-091': (D_COND, 'Moissanite vs diamond: EDU-GEM-02 CONDITIONAL (business dependency; D14-20).'),
    'CL-092': (D_COND, 'Moissanite vs lab-grown: EDU-GEM-01 CONDITIONAL (business dependency; first to build if any moissanite page is approved, D14-20).'),
    'CL-094': (D_COND, 'CZ vs diamond: section of EDU-GEM-00 CONDITIONAL hub pillar (D14-20).'),
    'CL-095': (D_COND, 'Simulants: EDU-GEM-00 CONDITIONAL hub pillar (D14-20).'),
    'CL-115': (D_COND, 'Care & everyday wear: EDU-RJG-03 CONDITIONAL (demand mostly stainless/plated jewelry; D14-22).'),
    # Education: deferred
    'CL-090': (D_DEF, 'Moissanite head terms: EDU-GEM-03 DEFERRED (MIXED retailer-led SERP; business dependency; D14-20).'),
    'CL-093': (D_DEF, 'Moissanite tester questions: EDU-GEM-03 DEFERRED; only a brief mention in EDU-LG-09 (D14-13), which is not a home.'),
    'CL-096': (D_DEF, 'Moissanite vs other stones: EDU-GEM-03 DEFERRED (D14-20).'),
    'CL-100': (D_DEF, 'Sapphire: EDU-GEM-04 DEFERRED (no gemstone catalogue evidence; D14-20).'),
    'CL-101': (D_DEF, 'Emerald: EDU-GEM-04 DEFERRED (D14-20).'),
    'CL-102': (D_DEF, 'Lab-created gemstones: EDU-GEM-04 DEFERRED (D14-20).'),
    'CL-103': (D_DEF, 'Natural gemstones: EDU-GEM-04 DEFERRED (D14-20).'),
    'CL-122': (D_DEF, 'Engagement-ring buying questions: EDU-RJG-04 DEFERRED pending the unapproved D-19 supplement (D14-22).'),
}

# Keyword-level overrides: keyword -> (kind, value, reason)
KW = {}


def kw(keys, kind, value, reason):
    for k in keys:
        KW[k] = (kind, value, reason)


# CL-014: evergreen history facts → pillar section (Stage 14 SECONDARY EDU-LG-00)
kw(['largest synthetic diamond', 'first lab grown diamond', 'first lab-grown diamond', 'history of lab grown diamonds',
    'history of lab-grown diamonds', 'lab grown diamonds history', 'lab-grown diamonds history', 'general electric man-made diamond'],
   'TARGET', 'EDU-LG-00', 'Evergreen history fact: short history section of the Lab-Grown pillar (Stage 14 CL-014 SECONDARY → EDU-LG-00). Trend/future members stay Blog (deferred).')
# CL-015: method-specific process members → method detail in CVD vs HPHT (Stage 14 SECONDARY EDU-LG-03)
kw(['lab grown diamond methods', 'lab grown diamonds methods'], 'INTERIM', 'EDU-LG-03',
   'Growth-method wording: interim method detail in CVD vs HPHT (Stage 14 CL-015 SECONDARY → EDU-LG-03). EDU-LG-04 stays CONDITIONAL (D14-08).')
# CL-008: shopping modifiers inside the price cluster → commercial (conditional Lab-Grown hub)
kw(['affordable lab created diamonds', 'lab grown diamonds clearance', 'lab-grown diamonds clearance'], 'DISP', D_COND,
   'Shopping modifier (affordable/clearance) inside the price cluster: commercial intent, owner is the CONDITIONAL commercial Lab-Grown hub (Stage 12 D-05). Education does not absorb commercial intent (Stage 14 rule 9).')
# CL-022: tester shopping / tester product queries → excluded
kw(['cvd/hpht diamond tester'], 'DISP', D_XCOM,
   'Validated CATEGORY SERP (tester shopping); diamond-tester products NOT_PROPOSED (Stage 12 D-16). Stage 13: MISALIGNED ranking on the CVD article. Informational pages must not target it (Stage 14 rule 3). Existing incidental ranking is left untouched.')
kw(['hde diamond tester'], 'DISP', D_XCOM, 'Tester product/brand query; tester shopping is not HOD business (Stage 14 D14-13; Stage 12 D-16).')
# CL-023: VVS members → VVS explainer (Stage 14 SECONDARY EDU-4C-03)
kw(['vvs lab diamonds', 'vvs lab grown diamonds', 'vvs lab-grown diamonds', 'are vvs diamonds lab grown', 'are vvs diamonds lab-grown'],
   'TARGET', 'EDU-4C-03', "VVS member of the lab-grown grade cluster: Stage 14 CL-023 SECONDARY → EDU-4C-03 ('vvs lab diamonds').")
# CL-034: third-party lab navigation / lookup → not an HOD target; commercial natural → deferred
kw(['ags diamond grading', 'national diamond lab', 'gcal lab grown diamond', 'gcal lab grown diamonds', 'gsl diamond lookup',
    'ags diamond lab', 'ags lab grown diamonds', 'egl diamond report lookup', 'gel diamond certification'], 'DISP', D_XOFF,
   "Navigation to / lookup on a third-party grading lab ('ags diamond grading' validated BRAND SERP). Stage 14: only the informational part of CL-034 is Education's.")
kw(['diamond grading kit'], 'DISP', D_XCOM, 'Product (grading kit) query; not an HOD product and not an Education need.')
kw(['certified natural diamonds'], 'DISP', D_DEF, 'Commercial natural-diamond shopping; commercial Natural hub deferred (Stage 12 D-05).')
# CL-040: clarity-scale members → clarity guide (Stage 14 CL-040 SECONDARY EDU-4C-01 and EDU-4C-00 note)
kw(['diamond clarity grading scale', 'diamond grading and clarity', 'diamond clarity comparison', 'diamond clarity types'], 'TARGET', 'EDU-4C-01',
   "Clarity-scale query: Stage 14 flags that 'diamond clarity grading scale' (12,100) returns clarity pages (4cs.gia.edu clarity, tiffany clarity), so clarity-scale members belong to the clarity guide (CL-040 SECONDARY → EDU-4C-01).")
# CL-044 / CL-048: clarity-grade comparisons (Stage 14 D14-14: comparisons fold into grade pages whose SERPs contain them)
kw(['if vs fl diamond', 'flawless diamonds vs vvs', 'difference between vvs and flawless diamonds'], 'TARGET', 'EDU-4C-03',
   'Comparison within the VVS/IF/FL family: the VVS SERP contains grade-comparison pages (D14-14; CL-044 SECONDARY → EDU-4C-03).')
kw(['which diamond is better vs1 or vs2'], 'INTERIM', 'EDU-4C-01',
   'Comparison within the VS family: EDU-4C-04 is CONDITIONAL, so its interim home is the clarity guide (CL-042/CL-044 SECONDARY).')
kw(['vs and vvs diamond', 'vvs vs diamond'], 'TARGET', 'EDU-4C-01',
   "Clarity-only cross-grade comparison (VS vs VVS) inside the colour+clarity cluster (CL-048): no colour grade in the query, so it follows the CL-044 rule (cross-grade → clarity guide, D14-14).")
# CL-061 / CL-062: inventory/brand-led or commercial shape queries → commercial shape landing (deferred)
kw(['asscher cut diamond'], 'DISP', D_DEF,
   "SERP is inventory-led (Stage 14 D14-17: 1 of 7 results is an education page). The Shapes pillar covers asscher as a section but does not target this query; commercial shape landing pages are deferred (Stage 12 D-08).")
kw(['asscher diamond'], 'DISP', D_DEF, 'Validated BRAND SERP (Stage 8). Not an Education target (Stage 14 rule 3); commercial shape landing pages deferred (Stage 12 D-08).')
kw(['asscher cut lab diamond', 'radiant cut lab diamond'], 'DISP', D_DEF,
   'Shape × origin shopping query; shape and origin are filters by default and multi-attribute landings are never indexable by default (Stage 12 D-07/D-08).')
kw(['asscher cut moissanite'], 'DISP', D_DEF, 'Moissanite: EDU-GEM-03 DEFERRED (D14-20); moissanite commercial NOT_PROPOSED.')
# CL-063: comparison wording inside a cluster Stage 14 excluded as commercial
kw(['moval vs oval diamond'], 'DISP', D_REV,
   'Shape-comparison wording (COMMERCIAL_RESEARCH label, unvalidated) inside CL-063, which Stage 14 excluded as commercial (PRODUCT SERP). Could be a Shapes-pillar section or commercial; needs SERP evidence.')
kw(['marquise oval diamond'], 'TARGET', 'COM-PDP-OVAL-FLORAL',
   'Stage 3 ranking (pos 90) on the PDP; validated PRODUCT SERP. Existing ranking URL keeps its keyword (Stage 13 NO_ACTION; Stage 14 rule 7).')
# CL-070 / CL-071: informational members → Natural pillar (Stage 14 SECONDARY EDU-NAT-00)
kw(['natural diamond stone', 'natural untreated diamond', 'natural untreated diamonds', 'are white diamonds real'], 'TARGET', 'EDU-NAT-00',
   "Informational framing of natural diamonds (Stage 14 CL-070 SECONDARY → EDU-NAT-00, e.g. 'natural untreated diamond').")
kw(['unpolished diamond', 'raw diamond testing', 'how raw diamond look like', 'rough diamond grading'], 'TARGET', 'EDU-NAT-00',
   "Raw-diamond identification is a section of the Natural pillar (Stage 14 CL-071 SECONDARY → EDU-NAT-00, 'how raw diamond look like').")
kw(['raw lab grown diamond', 'rough lab grown diamonds', 'lab grown rough diamonds'], 'DISP', D_DEF,
   'Rough lab-grown material is a trade/wholesale query; wholesale section deferred (Stage 12 business question 4). Not a Natural-pillar need.')
kw(['natural diamond wholesale'], 'DISP', D_DEF, 'Validated BRAND SERP; wholesale/trade deferred (Stage 12).')
# CL-110: metal-filter shopping
kw(['10 kt rings'], 'DISP', D_XCOM,
   'Metal-karat ring shopping (TRANSACTIONAL); metal is a non-indexable filter (Stage 12 D-08). Not an Education comparison query.')
# CL-112: competitor brand inside metals cluster
kw(['is 6 ice jewelry real'], 'DISP', D_XBRAND, "'6 ice' is a jewelry retailer brand; brand-legitimacy query about a competitor.")
# CL-113: product shopping for metals HOD does not sell
kw(['tungsten promise ring', 'tungsten promise rings', 'iridium bands'], 'DISP', D_XCOM,
   'Tungsten/iridium ring shopping; no evidence HOD sells these metals (Stage 14 D14-21: tungsten is a section, not a product line).')
# CL-121: ring-enhancer products
kw(['cathedral ring enhancers', 'cz ring enhancers'], 'DISP', D_XCOM, 'Ring-enhancer product query (MIXED label); not in the Stage 12 catalogue structure; not a settings-guide need.')
# CL-125: informational members of the stud cluster → nearest Stage 14 owners
kw(['is 1 2 carat diamond good for earrings', 'is 1 3 carat diamond earrings too small'], 'TARGET', 'EDU-4C-07',
   "Keyword-level INFORMATIONAL 'is X carat good/too small' pattern (the CL-049 need) inside the commercial stud cluster; carat guide owns the need (D14-14).")
kw(['types of diamond stud settings', 'what setting is best for diamond stud earrings'], 'TARGET', 'EDU-RJG-01',
   'Keyword-level INFORMATIONAL setting question inside the commercial stud cluster; settings guide owns setting types (D14-22).')
kw(['can you turn diamond earring into ring'], 'DISP', D_REV,
   'Remodelling question (validated OTHER SERP): could belong to Bespoke (service) or a FAQ; no Stage 12/14 owner defined.')

# Stage 14 topic that owns the need for INTERIM keyword overrides (the conditional page they wait for)
KW_TOPIC = {'which diamond is better vs1 or vs2': 'EDU-4C-04', 'lab grown diamond methods': 'EDU-LG-04', 'lab grown diamonds methods': 'EDU-LG-04'}

# ---------------------------------------------------------------- mapping
def topic_hub(tid):
    return arch[tid]['education_hub'] if tid in arch else ''


rows = []
for m in master:
    k = m['keyword']
    c = cmap[k]
    cid = c['cluster_id'] if c['cluster_id'].startswith('CL-') else ''
    atype = c['cluster_assignment_type']
    s = serp.get(k)
    reg = creg.get(cid, {})
    prim = cons_primary.get(cid)
    s14_topic = prim['education_topic_id'] if prim and prim['education_topic_id'] != 'NONE' else ''
    out = dict(
        keyword=k, normalized_keyword=m['normalized_keyword'], cluster_id=cid or atype,
        cluster_name=c['cluster_name'] if cid else '', cluster_primary_intent=reg.get('primary_intent', ''),
        keyword_intent=c['search_intent'], search_volume=m['search_volume'], cpc=m['cpc'], competition=m['competition'],
        keyword_difficulty=m['keyword_difficulty'], serp_validated='YES' if s else 'NO',
        serp_page_type=s['dominant_serp_page_type'] if s else '', serp_intent=s['validated_intent'] if s else '',
        existing_ranking_url=rel(m['stage3_ranking_url']) if m['stage3_current_rank'] not in ('NOT_APPLICABLE', '') else '',
        existing_ranking_position=m['stage3_current_rank'] if m['stage3_current_rank'] not in ('NOT_APPLICABLE', '') else '',
        existing_content_url=';'.join(sorted(set(cov.get(k, [])))),
        stage14_topic_id=s14_topic, stage14_topic_name=arch[s14_topic]['topic_name'] if s14_topic else '',
        stage14_hub=topic_hub(s14_topic),
    )
    ev = ['Stage 7']
    if s: ev.append('Stage 8')
    if out['existing_content_url']: ev.append('Stage 10')
    if cid: ev += ['Stage 11', 'Stage 14']
    if out['existing_ranking_url']: ev.insert(1, 'Stage 3/13')

    kind = val = reason = None
    if atype == 'NOISE':
        kind, val, reason = 'DISP', D_XNOISE, 'Stage 11 NOISE' + (f" (override: {c['stage11_status_override']})" if c['stage11_status_override'] not in ('NO', '') else ' (Stage 7 status preserved)') + '.'
    elif atype == 'COMPETITOR_BRAND':
        kind, val, reason = 'DISP', D_XBRAND, 'Stage 11 COMPETITOR_BRAND' + (f" (override: {c['stage11_status_override']})" if c['stage11_status_override'] not in ('NO', '') else ' (Stage 7 status preserved)') + '.'
    elif atype == 'UNCLUSTERED_REVIEW':
        kind, val, reason = 'DISP', D_REV, f"Stage 11 UNCLUSTERED_REVIEW: {c['clustering_reason'][:220]}"
    elif k in KW:
        kind, val, reason = KW[k]
        # Keyword-level Stage 14 topic: record the topic that owns this keyword's need when it differs
        # from the cluster PRIMARY (the cluster decision stays visible in 15_cluster_page_map.csv).
        kt = KW_TOPIC.get(k) or (val if kind == 'TARGET' and val.startswith('EDU-') else None)
        if kt and kt != s14_topic:
            out['notes_pre'] = f'Cluster PRIMARY Stage 14 topic is {s14_topic or "NONE"}; this keyword follows {kt} (keyword-level rule).'
            s14_topic = kt
            out.update(stage14_topic_id=kt, stage14_topic_name=arch[kt]['topic_name'], stage14_hub=topic_hub(kt))
    elif cid in CLUSTER_RULES:
        kind, val = CLUSTER_RULES[cid][0], CLUSTER_RULES[cid][1]
        if kind in ('TARGET', 'INTERIM'):
            reason = None
        else:
            reason = val
            kind, val = 'DISP', kind
    elif s14_topic and s14_topic in TOPIC_TARGET:
        kind, val = 'TARGET', TOPIC_TARGET[s14_topic]
    else:
        raise SystemExit(f'Unmapped keyword with no rule: {k} {cid} {s14_topic}')

    if kind in ('TARGET', 'INTERIM'):
        tid = val
        t = TARGETS[tid]
        interim = kind == 'INTERIM'
        disp = disp_for_target(tid, interim)
        if reason is None:
            if interim:
                sec = [r for r in cons_secondary.get(cid, []) if r['education_topic_id'] == tid]
                reason = (f"{s14_topic} is {arch[s14_topic]['architecture_status']}; Stage 14 names {tid} as the interim home"
                          f" ({sec[0]['reason'] if sec else 'SECONDARY row'}). No production URL for {s14_topic}.")
            else:
                reason = f"Stage 14 {prim['decision']} → {tid}: {prim['reason']}"
        out.update(mapping_disposition=disp, target_id=tid, target_page_type=t[1], target_url_status=t[6],
                   target_url=(t[4] if t[4] else (t[5] if t[5] != PENDING else '')),
                   target_url_source=('EXISTING_URL (Stage 10/13 inventory)' if t[4] else
                                      ('PROPOSED_URL_EXPRESSION (Stage 15, D-12 principles; not implemented; platform per D-17)' if t[5] != PENDING else f'{tid} (URL_PENDING)')))
    else:
        out.update(mapping_disposition=val, target_id='', target_page_type='', target_url_status='NONE', target_url='', target_url_source='')
    out['reason'] = reason
    out['evidence_source'] = '; '.join(dict.fromkeys(ev))
    rows.append(out)

# ---------------------------------------------------------------- confidence, risk, notes
HIGH_RISK_TOPICS = {'EDU-LG-03'}
for r in rows:
    d, tid = r['mapping_disposition'], r['target_id']
    notes = []
    kwi = r['keyword_intent']
    s14 = r['stage14_topic_id']
    if d in (D_XNOISE, D_XBRAND):
        conf = 'HIGH' if 'Stage 7 status preserved' in r['reason'] else 'MEDIUM'
        risk = 'NOT_APPLICABLE'
    elif d == D_REV:
        conf, risk = 'LOW', 'NOT_APPLICABLE'
    elif d in (D_XCOM, D_XOFF, D_COND, D_DEF):
        conf = 'HIGH' if r['serp_validated'] == 'YES' else 'MEDIUM'
        risk = 'NOT_APPLICABLE'
    else:
        # mapped
        if r['existing_ranking_url'] and r['existing_ranking_url'] == r['target_url']:
            conf = 'HIGH'
            notes.append(f"Stage 3 ranking pos {r['existing_ranking_position']} on this URL.")
        elif r['serp_validated'] == 'YES' and r['serp_page_type'] in ('EDITORIAL_GUIDE', 'COMPARISON', 'EDUCATIONAL'):
            conf = 'HIGH'
        else:
            ev = arch[s14]['evidence_level'] if s14 in arch else ''
            tstat = TARGETS[tid][3]
            if d == D_INT or 'PROVISIONAL' in tstat or ev in ('LOW', 'INSUFFICIENT_EVIDENCE'):
                conf = 'LOW'
            elif ev == 'HIGH':
                conf = 'HIGH'
            else:
                conf = 'MEDIUM'
            if kwi in ('TRANSACTIONAL', 'NAVIGATIONAL') and r['serp_validated'] == 'NO':
                conf = 'LOW'
                notes.append(f'Keyword intent label {kwi} (DataForSEO label, not SERP-validated) sits in an informational owner; kept with the Stage 14 owner, a SERP check would confirm.')
            if r['serp_validated'] == 'YES' and r['serp_page_type'] in ('OTHER', 'MIXED'):
                notes.append(f"Validated SERP page type {r['serp_page_type']} (not commercial-led).")
        top = arch.get(tid, {}).get('cannibalization_risk') if tid in arch else None
        risk = top or 'LOW'
        if tid in HIGH_RISK_TOPICS:
            risk = 'HIGH'
        if d == D_INT:
            risk = 'MEDIUM' if risk in ('LOW', 'NOT_APPLICABLE') else risk
            notes.append(f'Interim home only: if {s14} is later approved, this keyword moves to it and the interim section shrinks to a summary + link (D14-27 rule 7).')
        if tid == 'EDU-LG-03' and r['cluster_id'] in ('CL-017', 'CL-018'):
            notes.append('Single-method query consolidated into the comparison article (D14-06). CVD-only split may be revisited only under the D14-06 two-part condition; HPHT split not recommended.')
        if tid == 'EDU-4C-00' and r['cluster_id'] == 'CL-023':
            notes.append("Lab-grown chart query on the general 4Cs pillar (D14-15). Whether Google separates 'lab grown diamond clarity chart' from general clarity SERPs is INSUFFICIENT_EVIDENCE (D14-29 #3).")
    if s14 and s14 in arch and d in (D_COND, D_DEF, D_XCOM, D_XOFF, D_XBRAND, D_REV) and r['cluster_id'].startswith('CL-'):
        st = arch[s14]['architecture_status']
        if st in ('CONDITIONAL', 'DEFERRED'):
            notes.append(f"Stage 14 topic {s14} status {st}; no production URL.")
        else:
            notes.append(f"The cluster's Stage 14 owner {s14} ({st}) deliberately does not target this keyword (keyword-level intent differs).")
    if d == D_REV and r['serp_validated'] == 'YES':
        notes.append(f"Validated SERP page type {r['serp_page_type']}.")
    if r['existing_ranking_url'] and r['existing_ranking_url'] != r['target_url']:
        notes.append(f"Existing ranking URL {r['existing_ranking_url']} (pos {r['existing_ranking_position']}) is NOT the target; see 15_ranking_equity_protection.csv (URL itself is preserved).")
    r['mapping_confidence'] = conf
    r['cannibalization_risk'] = risk
    if r.get('notes_pre'):
        notes.insert(0, r.pop('notes_pre'))
    r['notes'] = ' '.join(notes)

def canon(k):
    k = k.lower().replace('-', ' ').replace('lab created', 'lab grown').replace('laboratory grown', 'lab grown')
    k = re.sub(r'[^a-z0-9 ]', ' ', k)
    return ' '.join(w[:-1] if w.endswith('s') and len(w) > 3 else w for w in k.split())


# Variant consistency: flag (do not silently change) variants whose upstream status differs.
_var = collections.defaultdict(list)
for r in rows:
    _var[canon(r['keyword'])].append(r)
for _rs in _var.values():
    if len(set(r['mapping_disposition'] for r in _rs)) > 1:
        for r in _rs:
            others = [f"'{o['keyword']}' = {o['mapping_disposition']}" for o in _rs if o is not r]
            r['notes'] = (r['notes'] + ' ' if r['notes'] else '') + (
                'VARIANT INCONSISTENCY (inherited from Stage 7/11 status, not changed here): ' + '; '.join(others) + '. Neither variant is mapped to a URL, so no ownership conflict results.')

COLS = ['keyword', 'normalized_keyword', 'cluster_id', 'cluster_name', 'cluster_primary_intent', 'keyword_intent', 'search_volume', 'cpc',
        'competition', 'keyword_difficulty', 'serp_validated', 'serp_page_type', 'serp_intent', 'existing_ranking_url',
        'existing_ranking_position', 'existing_content_url', 'stage14_topic_id', 'stage14_topic_name', 'stage14_hub',
        'mapping_disposition', 'target_id', 'target_page_type', 'target_url_status', 'target_url', 'target_url_source',
        'mapping_confidence', 'cannibalization_risk', 'reason', 'evidence_source', 'notes']
rows.sort(key=lambda r: (r['cluster_id'], -vol(r['search_volume']), r['keyword']))
wr('architecture/15_keyword_url_map.csv', COLS, rows)

# ---------------------------------------------------------------- registry
by_t = collections.defaultdict(list)
for r in rows:
    if r['target_id']:
        by_t[r['target_id']].append(r)
reg_rows = []
for tid, t in TARGETS.items():
    ks = by_t.get(tid, [])
    if not ks:
        continue
    top = max(ks, key=lambda r: vol(r['search_volume']))
    clusters = sorted(set(r['cluster_id'] for r in ks))
    val = [r for r in ks if r['serp_validated'] == 'YES']
    pt = collections.Counter(r['serp_page_type'] for r in val)
    ranking = [r for r in ks if r['existing_ranking_url'] == t[4] and t[4]]
    a = arch.get(tid, {})
    interim_n = sum(1 for r in ks if r['mapping_disposition'] == D_INT)
    reg_rows.append(dict(
        target_id=tid, target_page_name=t[0], page_type=t[1], hub=t[2], status=t[3],
        existing_or_proposed='EXISTING' if t[4] else 'PROPOSED', existing_url=t[4],
        proposed_url=t[5] if t[5] else ('(stays at existing URL)' if t[4] else ''),
        primary_intent=a.get('primary_intent', 'TRANSACTIONAL' if tid.startswith('COM') else ''),
        primary_searcher_need=a.get('primary_searcher_need', 'Shop side-stone engagement rings' if tid == 'COM-ER-SIDESTONE' else ('Buy this specific ring' if tid.startswith('COM-PDP') else '')),
        cluster_ids='; '.join(clusters), keyword_count=len(ks),
        highest_search_volume=f"{top['keyword']} ({top['search_volume']})",
        serp_evidence=(f"{len(val)} validated: " + '; '.join(f'{k}:{v}' for k, v in pt.most_common())) if val else 'No validated keyword',
        existing_equity=(f"{len(ranking)} Stage 3 ranking kw (best pos {min(int(r['existing_ranking_position']) for r in ranking)})" if ranking else ('None (no Stage 3 ranking)' if t[4] else 'n/a (new page)')),
        cannibalization_risk=('HIGH' if tid in HIGH_RISK_TOPICS else a.get('cannibalization_risk', 'LOW')),
        business_dependency=a.get('business_dependency', 'None') if a else 'Catalogue (Stage 12)',
        stage14_source=t[7],
        notes=t[8] + (f' Includes {interim_n} interim-home keyword(s).' if interim_n else ''),
    ))
RCOLS = ['target_id', 'target_page_name', 'page_type', 'hub', 'status', 'existing_or_proposed', 'existing_url', 'proposed_url', 'primary_intent',
         'primary_searcher_need', 'cluster_ids', 'keyword_count', 'highest_search_volume', 'serp_evidence', 'existing_equity',
         'cannibalization_risk', 'business_dependency', 'stage14_source', 'notes']
wr('architecture/15_target_page_registry.csv', RCOLS, reg_rows)

# ---------------------------------------------------------------- cluster → page map
cp_rows = []
by_c = collections.defaultdict(list)
for r in rows:
    if r['cluster_id'].startswith('CL-'):
        by_c[r['cluster_id']].append(r)
STATUS = {D_EX: 'MAPPED_EXISTING_URL', D_KEEP: 'MAPPED_EXISTING_URL_KEEP', D_PROP: 'MAPPED_PROPOSED_URL', D_INT: 'MAPPED_INTERIM_HOME',
          D_COND: 'CONDITIONAL_NOT_MAPPED', D_DEF: 'DEFERRED_NOT_MAPPED', D_XCOM: 'EXCLUDED_COMMERCIAL', D_XOFF: 'EXCLUDED_OFF_SCOPE',
          D_XBRAND: 'EXCLUDED_COMPETITOR_BRAND', D_REV: 'REVIEW_REQUIRED'}
for cid in sorted(creg):
    ks = by_c[cid]
    prim = cons_primary[cid]
    tcount = collections.Counter(r['target_id'] for r in ks if r['target_id'])
    dcount = collections.Counter(r['mapping_disposition'] for r in ks)
    main_t = tcount.most_common(1)[0][0] if tcount else ''
    main_d = dcount.most_common(1)[0][0]
    sec_topics = [r['education_topic_id'] for r in cons_secondary.get(cid, [])]
    others = [t for t in tcount if t != main_t]
    split = len(dcount) > 1 or len(tcount) > 1
    notes = 'Keyword dispositions: ' + '; '.join(f'{STATUS[k]}={v}' for k, v in dcount.most_common())
    if others:
        notes += '. Secondary targets used at keyword level: ' + '; '.join(f'{t} ({tcount[t]} kw)' for t in others)
    cp_rows.append(dict(
        cluster_id=cid, cluster_name=creg[cid]['cluster_name'], primary_topic_id=prim['education_topic_id'],
        primary_topic_name=prim['education_topic'], target_id=main_t, target_page_name=TARGETS[main_t][0] if main_t else '',
        mapping_status=STATUS[main_d] + ('_WITH_KEYWORD_SPLIT' if split else ''),
        secondary_topic_id='; '.join(sec_topics), secondary_target_id='; '.join(others),
        reason=(CLUSTER_RULES[cid][1] if cid in CLUSTER_RULES and CLUSTER_RULES[cid][0] not in ('TARGET', 'INTERIM')
                else f"Stage 14 {prim['decision']}: {prim['reason']}"),
        evidence_level=prim['evidence_level'], serp_evidence=prim['serp_evidence'], notes=notes))
CCOLS = ['cluster_id', 'cluster_name', 'primary_topic_id', 'primary_topic_name', 'target_id', 'target_page_name', 'mapping_status',
         'secondary_topic_id', 'secondary_target_id', 'reason', 'evidence_level', 'serp_evidence', 'notes']
wr('architecture/15_cluster_page_map.csv', CCOLS, cp_rows)

# ---------------------------------------------------------------- ranking equity protection
kmap = {r['keyword']: r for r in rows}
mig = {rel(r['existing_url']): r for r in rd('content-strategy/14_education_existing_content_mapping.csv')}
pr_rows = []
for e in equity:
    r = kmap[e['keyword']]
    u = rel(e['url'])
    same = r['target_url'] == u
    if same:
        action = 'KEEP_EXISTING_URL'
        reason = 'Existing ranking URL is the mapped owner. No new page targets this keyword.'
    else:
        action = 'KEEP_EXISTING_URL_NOT_TARGETED'
        reason = 'URL is untouched and keeps whatever ranking it has; the keyword itself is not targeted because its SERP is commercial (CATEGORY) and the page is informational (Stage 14 rule 3; Stage 13 MISALIGNED).'
    ms = mig.get(u, {}).get('stage14_migration_status', '')
    if u in (U_SIDE, U_PDP):
        ms = 'NO_MIGRATION_RECOMMENDED (commercial URL; Stage 13 NO_ACTION)'
    note = ''
    if u == U_CVD:
        note = 'Stage 13 DO_NOT_MOVE_NOW + 9 conditions preserved. No CVD or HPHT page is created (D14-06).'
    elif u == U_LVN:
        note = 'Stage 13 DO_NOT_MOVE_NOW preserved. No competing lab-vs-natural page assigned.'
    elif u == U_14K:
        note = 'Stays at the /blog URL now. Move only when the Metals section exists (Stage 13 conditions; 1:1 301). Migration is not triggered by Stage 15.'
    elif u == U_CHO:
        note = 'Migration DEFERRED (Stage 13) pending D-19; URL stays.'
    elif u == U_SIDE:
        note = "Stage 12 D-03/D-12 flag the 'by-desgin' segment; any path change is an implementation migration with a 1:1 301, not recommended as a stand-alone change. Equity is LOW (pos 104)."
    elif u == U_PDP:
        note = 'PDP keeps its keyword; CL-063 excluded from Education.'
    pr_rows.append(dict(keyword=e['keyword'], ranking_url=u, ranking_position=e['position'], cluster_id=r['cluster_id'],
                        current_intent=e['intent'], mapped_target_id=r['target_id'] or '(none — excluded)', mapped_target_url=r['target_url'],
                        action=action, equity_risk=e['equity_risk'], reason=reason, migration_status=ms, notes=note))
PCOLS = ['keyword', 'ranking_url', 'ranking_position', 'cluster_id', 'current_intent', 'mapped_target_id', 'mapped_target_url', 'action',
         'equity_risk', 'reason', 'migration_status', 'notes']
wr('content-strategy/15_ranking_equity_protection.csv', PCOLS, pr_rows)

# ---------------------------------------------------------------- cannibalization checks
cz = []


def add(check, severity, subject, finding, detail, resolution):
    cz.append(dict(check=check, severity=severity, subject=subject, finding=finding, detail=detail, resolution=resolution))


# A. many keywords → one URL (inventory, informational)
for rr in sorted(reg_rows, key=lambda x: -x['keyword_count']):
    add('A_MANY_KEYWORDS_ONE_URL', 'INFO', rr['target_id'], f"{rr['keyword_count']} keywords", rr['cluster_ids'], 'Expected: one owner per searcher need.')
# B. same keyword → multiple URLs (by construction impossible; check normalized variants too)
seen = collections.defaultdict(set)
for r in rows:
    seen[r['keyword']].add(r['target_id'])
dupes = [k for k, v in seen.items() if len(v) > 1]
add('B_SAME_KEYWORD_MULTIPLE_URLS', 'PASS' if not dupes else 'FAIL', 'all keywords', f'{len(dupes)} keywords with >1 target', ', '.join(dupes), 'One row per keyword, one target_id per row.')


var = collections.defaultdict(list)
for r in rows:
    if r['target_id']:
        var[canon(r['keyword'])].append(r)
for ck, rs in var.items():
    ts = set(r['target_id'] for r in rs)
    if len(ts) > 1:
        add('B_NEAR_DUPLICATE_VARIANTS_SPLIT', 'WARNING', ck, 'Spelling/plural variants map to different targets',
            '; '.join(f"{r['keyword']}→{r['target_id']}" for r in rs), 'Review: variants of one query should share an owner.')
for ck, rs in _var.items():
    if len(set(r['mapping_disposition'] for r in rs)) > 1 and not any(r['target_id'] for r in rs):
        add('B_VARIANT_STATUS_INCONSISTENCY', 'INFO', ck, 'Variants carry different non-mapping dispositions (inherited upstream status)',
            '; '.join(f"{r['keyword']}={r['mapping_disposition']}" for r in rs), 'No URL conflict; recorded for a future Stage 7/11 clean-up.')
# C. same cluster → multiple targets
for cid, ks in sorted(by_c.items()):
    ts = collections.Counter(r['target_id'] for r in ks if r['target_id'])
    if len(ts) > 1:
        sec = set(r['education_topic_id'] for r in cons_secondary.get(cid, [])) | {cons_primary[cid]['education_topic_id']}
        unexplained = [t for t in ts if t not in sec]
        add('C_SAME_CLUSTER_MULTIPLE_TARGETS', 'INFO' if not unexplained else 'REVIEW', cid,
            f"{len(ts)} targets: " + '; '.join(f'{t}={n}' for t, n in ts.items()),
            ('All targets are Stage 14 PRIMARY/SECONDARY topics for this cluster.' if not unexplained else
             f"Targets outside Stage 14 PRIMARY/SECONDARY for this cluster: {', '.join(unexplained)} (keyword-level intent rule; see reason column)."),
            'Allowed: Stage 14 SECONDARY rows or documented keyword-level intent rules.')
# D. existing ranking URL vs proposed URL
for p in pr_rows:
    sev = 'PASS' if p['action'] == 'KEEP_EXISTING_URL' else 'FLAG'
    add('D_EXISTING_RANKING_VS_PROPOSED', sev, p['keyword'], f"ranking {p['ranking_url']} (pos {p['ranking_position']}) → mapped {p['mapped_target_id']}",
        p['reason'], 'Existing ranking URL wins by default.' if sev == 'PASS' else 'URL preserved; keyword not targeted by any page.')
# E. overlapping intent between targets (Stage 14 D14-27 register, restricted to targets that own keywords)
PAIRS = [
    ('EDU-LG-01', 'EDU-LG-02', 'MEDIUM', 'Authenticity vs comparison: REL-020 max 2 shared URLs, both SERPs COMPARISON-dominant (D14-07). Enforce the boundary in content.'),
    ('EDU-LG-02', 'EDU-LG-05', 'MEDIUM', 'Worth-it pros/cons (interim on LG-02) vs price/value/resale: money-worry overlap (D14-10; D14-27).'),
    ('EDU-LG-00', 'EDU-LG-03', 'HIGH', "CL-015 process queries are split between the pillar (general) and CVD vs HPHT (methods). If EDU-LG-04 is ever created, it must not target CVD/HPHT method queries (D14-08)."),
    ('EDU-4C-00', 'EDU-4C-01', 'MEDIUM', "Lab-grown clarity-chart queries (CL-023) sit on the 4Cs pillar while general clarity-scale queries sit on the clarity guide. Separation is INSUFFICIENT_EVIDENCE (D14-15; D14-29 #3)."),
    ('EDU-CERT-00', 'EDU-CERT-01', 'MEDIUM', "General certification vs GIA-vs-IGI: 0 shared URLs (D14-18). Both changes must ship together (Stage 13) or OV-01 persists."),
    ('EDU-4C-06', 'EDU-SHP-00', 'MEDIUM', "Cut grade vs shape: 'cut' is ambiguous (grade vs shape). Cut-grade queries → EDU-4C-06; shape queries → EDU-SHP-00 (D14-02 SPLIT)."),
    ('EDU-LG-08', 'EDU-LG-01', 'MEDIUM', "'do lab-grown diamonds look real' is appearance (EDU-LG-08), not authenticity (D14-07)."),
    ('EDU-LG-09', 'EDU-LG-01', 'LOW', "'do lab grown diamonds test real' wording mixes detection and authenticity; detection owns tester questions (D14-13)."),
    ('EDU-LG-00', 'CL-001 commercial Lab-Grown hub (conditional)', 'MEDIUM', 'Pillar must not target the head terms; REL-004 DISTINCT_INTENT (D14-05).'),
    ('EDU-LG-10', 'EDU-RJG-04 (deferred)', 'INSUFFICIENT_EVIDENCE', "'should i buy a lab grown diamond engagement ring' sits on the lab-grown buying guide; boundary with the deferred engagement-ring guide is unresolved (OV-06; D-19)."),
    ('EDU-4C-02', 'EDU-4C-01', 'LOW', 'SI SERP shares 0 URLs with the clarity scale (D14-14).'),
    ('EDU-4C-03', 'EDU-4C-01', 'LOW', 'VVS SERP shares 1 URL with the clarity scale (D14-14).'),
]
for a_, b_, sev, why in PAIRS:
    add('E_PROPOSED_OVERLAPPING_INTENT', sev, f'{a_} ↔ {b_}', 'Adjacent intents between owners', why, 'Flagged for Stage 16 linking and briefs; no mapping change.')
# Special checks
def spec(name, ok, detail):
    add('SPECIAL_' + name, 'PASS' if ok else 'FAIL', name, 'PASS' if ok else 'FAIL', detail, '')

cvd_rows = [r for r in rows if re.search(r'\b(cvd|hpht)\b', r['keyword']) and r['target_id']]
spec('CVD_HPHT_NO_NEW_PAGE', all(r['target_id'] == 'EDU-LG-03' for r in cvd_rows),
     f"{len(cvd_rows)} mapped CVD/HPHT keywords; targets: {dict(collections.Counter(r['target_id'] for r in cvd_rows))}")
lvn = [r for r in rows if r['cluster_id'] == 'CL-011']
spec('LAB_VS_NATURAL_EXISTING_URL', all(r['target_url'] == U_LVN for r in lvn), f'{len(lvn)} CL-011 keywords → {U_LVN}')
real_cmp = [r['keyword'] for r in rows if r['target_id'] == 'EDU-LG-01' and re.search(r'\bvs\b|differen|better|compare', r['keyword'])]
spec('ARE_REAL_NO_COMPARISON_KEYWORDS', not real_cmp, f'comparison-worded keywords on EDU-LG-01: {real_cmp}')
spec('NO_LAB_GROWN_4CS_TARGET', not any('4C' in t and 'LG' in t for t in TARGETS), 'No lab-grown-only 4Cs target exists; CL-023 → EDU-4C-00 / EDU-4C-03.')
clar = collections.Counter(r['target_id'] for r in rows if r['cluster_id'] in ('CL-040', 'CL-041', 'CL-042', 'CL-043', 'CL-044', 'CL-045', 'CL-046') and r['target_id'])
spec('CLARITY_FOLLOWS_STAGE14', set(clar) <= {'EDU-4C-00', 'EDU-4C-01', 'EDU-4C-02', 'EDU-4C-03'}, f'clarity cluster targets: {dict(clar)}')
shape_t = [t for t in TARGETS if 'SHP' in t]
spec('NO_PER_SHAPE_PAGES', shape_t == ['EDU-SHP-00'], f'shape targets: {shape_t}')
spec('NO_IGI_ONLY_PAGE', 'EDU-CERT-03' not in by_t, 'EDU-CERT-03 receives 0 keywords (deferred).')
bad = [r['keyword'] for r in rows if r['target_id'].startswith('EDU') and r['serp_page_type'] in ('CATEGORY', 'PRODUCT', 'BRAND')]
spec('NO_COMMERCIAL_SERP_ON_EDUCATION', not bad, f'validated CATEGORY/PRODUCT/BRAND keywords on Education targets: {bad}')

ZCOLS = ['check', 'severity', 'subject', 'finding', 'detail', 'resolution']
wr('architecture/15_cannibalization_check.csv', ZCOLS, cz)

print('keywords', len(rows))
print(collections.Counter(r['mapping_disposition'] for r in rows))
print('targets', len(reg_rows))
