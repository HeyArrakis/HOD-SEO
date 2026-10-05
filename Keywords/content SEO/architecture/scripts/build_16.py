#!/usr/bin/env python3
"""Stage 16 — Internal linking architecture (build).

Local-only: reads Stage 10-15 project files, writes the four Stage 16 CSVs.
No network access, no DataForSEO, no live-site request.

Page IDs:
  * The 27 Stage 15 target IDs are reused unchanged.
  * Architecture nodes that own no keyword (Stage 15 summary §11-12) get IDs here:
    EDU-ROOT and EDU-RJG-00 follow Stage 14; conditional Stage 14 topics keep their
    Stage 14 topic IDs; commercial/brand/blog nodes use COM-/NAV-/SUP-/BRAND-/BLOG-.
  * TPL-HEADER / TPL-FOOTER are site templates (link sources only).
  * Stage 14 DEFERRED topics and Stage 12 DEFERRED/NOT_PROPOSED nodes get no ID and no link.
"""
import csv, collections, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
P = lambda *a: os.path.join(ROOT, *a)
rd = lambda p: list(csv.DictReader(open(P(p), newline='', encoding='utf-8')))

REG = {r['target_id']: r for r in rd('architecture/15_target_page_registry.csv')}
KMAP = rd('architecture/15_keyword_url_map.csv')
PROT = rd('content-strategy/15_ranking_equity_protection.csv')
ARCH = {r['topic_id']: r for r in rd('architecture/14_education_architecture.csv')}
HIER = rd('architecture/14_education_hierarchy.csv')

# ---------------------------------------------------------------- pages
# (page_type, business_area, url_or_expression, current_or_proposed, notes)
X = 'EXISTING'
NONREG = {
    'TPL-HEADER': ('SITE_TEMPLATE', 'Global', 'TEMPLATE: site header / main navigation (every page)', 'TEMPLATE', 'Link source only.'),
    'TPL-FOOTER': ('SITE_TEMPLATE', 'Global', 'TEMPLATE: site footer (every page)', 'TEMPLATE', 'Link source only.'),
    'NAV-HOME': ('HOMEPAGE', 'Brand', '/', X, 'Stage 12 D-18: targets brand and overall offer, not category subjects (OV-13).'),
    'COM-SHOP': ('ALL_PRODUCTS_LISTING', 'Shop (commercial)', '/shop', X, 'Stage 12: INDEXABLE_CONDITIONAL (indexability not decided here).'),
    'COM-ER': ('CATEGORY_HUB', 'Engagement Rings (commercial)', '/engagement-rings', X, 'Stage 12 L1. Owns no Stage 15 keyword (commercial keyword gap, D-19).'),
    'COM-ER-STYLES': ('SUBCATEGORY_GROUP', 'Engagement Rings (commercial)', '/engagement-rings/by-desgin/{bezel-rings, halo-ring, nature-inspired-rings, pave, solitare-rings, three-stone-rings, toi-moi-rings}', 'EXISTING_CONDITIONAL', 'Stage 12 D-03: indexable only if each passes the D-07 gate. Live and in nav today.'),
    'COM-WB': ('CATEGORY_HUB', 'Wedding Bands (commercial)', '/wedding-bands', X, 'Stage 12 L1.'),
    'COM-WB-GENDER': ('SUBCATEGORY_GROUP', 'Wedding Bands (commercial)', '/wedding-bands/for-her, /wedding-bands/for-him', 'EXISTING_CONDITIONAL', 'Stage 12 D-04: allowed L2 only when populated; /for-him and children observed empty (Stage 10).'),
    'COM-FJ': ('CATEGORY_HUB', 'Fine Jewellery (commercial)', '/fine-jewellery', X, 'Umbrella; label/slug spelling open (D-15).'),
    'COM-FJ-EARRINGS': ('CATEGORY', 'Fine Jewellery > Earrings', '/fine-jewellery/earrings', X, 'Stage 12 D-02: first-class in navigation.'),
    'COM-FJ-NECKLACES': ('CATEGORY', 'Fine Jewellery > Necklaces & Pendants', '/fine-jewellery/necklaces', X, 'Stage 12 D-02.'),
    'COM-FJ-BRACELETS': ('CATEGORY', 'Fine Jewellery > Bracelets', '/fine-jewellery/bracelet', X, 'Stage 12 D-02.'),
    'COM-FJ-TYPE-SUBCATS': ('SUBCATEGORY_GROUP', 'Fine Jewellery (commercial)', '/fine-jewellery/{earrings,necklaces,bracelet}/<type>', 'EXISTING_CONDITIONAL', 'Stage 12: type subcategories PROPOSED_CONDITIONAL (D-07 gate); some observed empty (Stage 10).'),
    'COM-FJ-RINGS': ('CATEGORY', 'Fine Jewellery > Rings', '/fine-jewellery/rings', 'EXISTING_CONDITIONAL', 'Stage 12: INSUFFICIENT EVIDENCE - DEFER. Live; eternity-rings child observed empty.'),
    'COM-CURATED-TBAR': ('CURATED_COLLECTION', 'Necklaces & Pendants (conceptual)', '/t-bar', 'EXISTING_CONDITIONAL', 'Stage 12 D-14: placement deferred (OV-16 overlap with pendant necklaces).'),
    'COM-LG-HUB': ('ORIGIN_HUB', 'Lab-Grown Diamonds (commercial)', 'NO_URL (CONDITIONAL - Stage 12 D-05)', 'CONDITIONAL', 'Conditional owner of CL-001 head terms (lab grown diamonds / lab diamonds). Needs business confirmation.'),
    'COM-BESPOKE': ('SERVICE_PAGE', 'Bespoke / Custom', '/bespoke', X, 'Bespoke sub-pages deferred (Stage 12).'),
    'COM-PDP': ('PRODUCT_DETAIL_PAGE', 'Shop (commercial)', 'TEMPLATE: /shop/<product-slug> (all live PDPs)', 'EXISTING_GROUP', 'One row represents the PDP template; COM-PDP-OVAL-FLORAL is listed separately because it ranks.'),
    'EDU-ROOT': ('EDUCATION_HUB', 'Education', '/education', X, 'Existing hub becomes the Education root index (Stage 14 D14-26). Lists 1 article today (Stage 10).'),
    'EDU-RJG-00': ('EDUCATION_TOPIC_HUB_INDEX', 'Ring & Jewellery Guides', 'URL_PENDING', 'PROPOSED', 'Index only; owns no keyword (Stage 14 N-RJG-00). Slug blocked by D-15.'),
    'EXIST-BLOG-ER-ONLINE': ('EXISTING_ARTICLE_DEFERRED', 'Engagement Rings / Diamond Buying', '/blog/how-to-choose-a-lab-grown-diamond-engagement-ring-online-house-of-diams', X, 'Stage 13 DEFER; intended destination EDU-RJG-04 (DEFERRED). Owns no Stage 15 keyword.'),
    'BLOG-HUB': ('BLOG_HUB', 'Blog / Journal', '/blog', X, 'Stage 13 KEEP_BLOG. Lists the 10 current articles (Stage 10).'),
    'BLOG-CRAFT': ('BLOG_POST_TEMPLATE', 'Blog: Craft & Making', 'TEMPLATE: future Blog post (Craft & Making)', 'PROPOSED_TEMPLATE', 'Stage 13 §5 category. No posts exist yet.'),
    'BLOG-STYLE': ('BLOG_POST_TEMPLATE', 'Blog: Style & Trends', 'TEMPLATE: future Blog post (Style & Trends)', 'PROPOSED_TEMPLATE', 'Stage 13 §5 category. No posts exist yet.'),
    'BLOG-GIFTS': ('BLOG_POST_TEMPLATE', 'Blog: Gifts & Occasions', 'TEMPLATE: future Blog post (Gifts & Occasions)', 'PROPOSED_TEMPLATE', 'Stage 13 §5; one URL per recurring occasion.'),
    'BLOG-LAUNCH': ('BLOG_POST_TEMPLATE', 'Blog: Collections & Launches', 'TEMPLATE: future Blog post (Collections & Launches)', 'PROPOSED_TEMPLATE', 'Stage 13 §5; never replaces the category page.'),
    'BLOG-STORIES': ('BLOG_POST_TEMPLATE', 'Blog: Stories', 'TEMPLATE: future Blog post (Stories / client commissions)', 'CONDITIONAL', 'Stage 13: client stories are a FUTURE POSSIBILITY (need real commissions and consent).'),
    'BLOG-INDUSTRY': ('BLOG_POST_TEMPLATE', 'Blog: Industry Notes', 'TEMPLATE: future Blog post (Industry Notes)', 'PROPOSED_TEMPLATE', 'Stage 13 §5; dated lab-grown market notes (CL-014).'),
    'SUP-FAQ': ('FAQ_HELP', 'Brand & Support', '/faq', X, 'Stage 12 D-18 / Stage 14 D14-30: one-line answers + link to the Education owner.'),
    'SUP-POLICIES': ('POLICY_PAGE_GROUP', 'Brand & Support', '/shipping, /returns, /privacy-policy, /terms', X, ''),
    'BRAND-ABOUT': ('BRAND_PAGE', 'Brand & Support', '/about', X, 'Brand story (workshop, founders).'),
    'BRAND-CONTACT': ('BRAND_PAGE', 'Brand & Support', '/contact', X, ''),
}
# Stage 14 CONDITIONAL topics (not DEFERRED): get IDs, links only as CONDITIONAL
COND_EDU = ['EDU-LG-04', 'EDU-LG-06', 'EDU-NAT-01', 'EDU-NAT-02', 'EDU-4C-04', 'EDU-4C-08', 'EDU-CERT-02',
            'EDU-MET-02', 'EDU-GEM-00', 'EDU-GEM-01', 'EDU-GEM-02', 'EDU-RJG-03', 'EDU-GEN-02']
for t in COND_EDU:
    a = ARCH[t]
    assert a['architecture_status'] == 'CONDITIONAL', t
    NONREG[t] = (a['proposed_page_type'], a['education_hub'], 'NO_URL (CONDITIONAL - Stage 14)', 'CONDITIONAL',
                 f"Stage 14 CONDITIONAL. {a['business_dependency']}".strip())
# Deferred / not proposed: never linked (listed in 16_linking_rules.md)
DEFERRED = [t for t, a in ARCH.items() if a['architecture_status'] == 'DEFERRED'] + ['COM-NAT-HUB', 'COM-LOOSE-CARAT', 'COM-WHOLESALE', 'COM-HIPHOP']

PAGES = {}
for tid, r in REG.items():
    ex = r['existing_or_proposed'] == 'EXISTING'
    url = r['existing_url'] if ex else r['proposed_url']
    cop = 'EXISTING' if ex else r['status']  # PROPOSED / PROPOSED_PROVISIONAL
    PAGES[tid] = dict(page_type=r['page_type'], area=r['hub'], url=url, cop=cop, registry=True, notes=r['notes'])
for pid, (pt, area, url, cop, n) in NONREG.items():
    PAGES[pid] = dict(page_type=pt, area=area, url=url, cop=cop, registry=False, notes=n)

def is_cond(pid):
    return PAGES[pid]['cop'] in ('CONDITIONAL', 'EXISTING_CONDITIONAL')

def is_template(pid):
    return PAGES[pid]['cop'] == 'TEMPLATE'

# ---------------------------------------------------------------- Education parents (Stage 14)
H2PILLAR = {h['hierarchy_id']: h['topic_or_pillar_id'] for h in HIER if h['node_type'] == 'HUB' and h['topic_or_pillar_id']}
PARENT = {}
for h in HIER:
    t = h['topic_or_pillar_id']
    if h['node_type'] != 'TOPIC' or not t:
        continue
    if h['level'] == 'L1_PILLAR' or h['parent_id'] == 'H-00':
        PARENT[t] = 'EDU-ROOT'
    elif h['parent_id'] in H2PILLAR:
        PARENT[t] = H2PILLAR[h['parent_id']]
EDU_PAGES = [p for p in PAGES if p.startswith('EDU-') and p != 'EDU-ROOT']
for p in EDU_PAGES:
    assert p in PARENT, p

# ---------------------------------------------------------------- labels (navigational anchors)
LABEL = {
    'EDU-ROOT': 'Education', 'EDU-LG-00': 'Lab-Grown Diamond Guide', 'EDU-NAT-00': 'Natural Diamond Guide',
    'EDU-4C-00': 'Diamond Quality (4Cs)', 'EDU-SHP-00': 'Diamond Shapes', 'EDU-CERT-00': 'Certification & Grading Reports',
    'EDU-MET-00': 'Metals & Materials', 'EDU-RJG-00': 'Ring & Jewellery Guides', 'EDU-GEM-00': 'Gemstones & Diamond Alternatives',
    'EDU-LG-01': 'Are lab-grown diamonds real?', 'EDU-LG-02': 'Lab-grown vs natural', 'EDU-LG-03': 'CVD vs HPHT',
    'EDU-LG-04': 'How they are grown', 'EDU-LG-05': 'Price, value & resale', 'EDU-LG-06': 'Pros & cons',
    'EDU-LG-07': 'Ethics & sustainability', 'EDU-LG-08': 'Appearance & durability', 'EDU-LG-09': 'Testing & identification',
    'EDU-LG-10': 'How to choose a lab-grown diamond', 'EDU-NAT-01': 'Value & rarity', 'EDU-NAT-02': 'Conflict-free sourcing',
    'EDU-4C-01': 'Clarity guide', 'EDU-4C-02': 'SI clarity', 'EDU-4C-03': 'VVS & flawless clarity', 'EDU-4C-04': 'VS clarity',
    'EDU-4C-05': 'Color guide', 'EDU-4C-06': 'Cut grade guide', 'EDU-4C-07': 'Carat guide', 'EDU-4C-08': 'Fancy-colored diamonds',
    'EDU-CERT-01': 'GIA vs IGI', 'EDU-CERT-02': 'Reading a grading report', 'EDU-MET-01': '14k vs 18k gold',
    'EDU-MET-02': 'Rhodium plating', 'EDU-GEM-01': 'Moissanite vs lab-grown', 'EDU-GEM-02': 'Moissanite vs diamond',
    'EDU-RJG-01': 'Ring settings guide', 'EDU-RJG-02': 'Ring size guide', 'EDU-RJG-03': 'Care & everyday wear',
    'EDU-GEN-01': 'Diamond properties', 'EDU-GEN-02': 'Types of diamonds (guide)',
    'BLOG-HUB': 'Journal', 'COM-ER': 'Engagement Rings', 'COM-WB': 'Wedding Bands', 'COM-FJ': 'Fine Jewellery',
    'COM-FJ-EARRINGS': 'Earrings', 'COM-FJ-NECKLACES': 'Necklaces & Pendants', 'COM-FJ-BRACELETS': 'Bracelets',
}

# ---------------------------------------------------------------- links
LINKS = collections.OrderedDict()
CTX = {'CONTEXTUAL', 'RELATED_CONTENT', 'EDITORIAL', 'EDUCATIONAL_CTA', 'COMMERCIAL_CTA', 'PRODUCT_RECOMMENDATION'}
STRUCT = {'GLOBAL_NAV', 'PRIMARY_NAV', 'CATEGORY_NAV', 'BREADCRUMB', 'FOOTER'}


def L(src, tgt, lt, rel, pri, at, anchor, variants='', reason='', notes=''):
    assert src in PAGES and tgt in PAGES, (src, tgt)
    if is_cond(src) or is_cond(tgt):
        pri = 'CONDITIONAL'
    LINKS[(src, tgt)] = dict(link_type=lt, relationship_type=rel, priority=pri, anchor_type=at, recommended_anchor=anchor,
                             anchor_variants=variants, context_reason=reason, notes=notes)


# --- auto: Education hierarchy (Stage 14) -------------------------------------------------
for p in EDU_PAGES:
    par = PARENT[p]
    pri = 'REQUIRED'
    L(par, p, 'CATEGORY_NAV', 'HUB_TO_CHILD', pri, 'NAVIGATIONAL', LABEL[p], '',
      f'Stage 14 hierarchy: {par} is the parent of {p}; hub topic list.')
    L(p, par, 'BREADCRUMB', 'CHILD_TO_HUB', pri, 'NAVIGATIONAL', LABEL[par], '',
      f'Stage 14 hierarchy breadcrumb ({p} -> {par}).',
      'Transitional Education-owned /blog URLs carry the Education breadcrumb too (Stage 13 §6).' if PAGES[p]['url'].startswith('/blog/') else '')

# --- global templates ---------------------------------------------------------------------
NAVR = 'Stage 12 D-01/D-02 top-level navigation.'
L('TPL-HEADER', 'NAV-HOME', 'GLOBAL_NAV', 'SITE_NAV', 'REQUIRED', 'BRANDED', 'House of Diams (logo)', '', 'Global home link.')
L('TPL-HEADER', 'COM-ER', 'PRIMARY_NAV', 'SITE_NAV', 'REQUIRED', 'NAVIGATIONAL', 'Engagement Rings', '', NAVR)
L('TPL-HEADER', 'COM-ER-SIDESTONE', 'PRIMARY_NAV', 'SITE_NAV', 'REQUIRED', 'NAVIGATIONAL', 'Side-Stone', '',
  'Mega-menu style entry under Engagement Rings; the only style subcategory confirmed by Stage 12 D-03. Already linked in live nav (Stage 10).',
  'Nav alone is not counted as contextual support (see contextual rows).')
L('TPL-HEADER', 'COM-ER-STYLES', 'PRIMARY_NAV', 'SITE_NAV', 'CONDITIONAL', 'NAVIGATIONAL', 'Solitaire / Halo / Pave / Three-Stone / Bezel / Toi-et-Moi / Nature-Inspired', '',
  'Style entries only while each style listing is populated (Stage 12 P-EMPTY). Indexability is not decided by Stage 16.')
L('TPL-HEADER', 'COM-WB', 'PRIMARY_NAV', 'SITE_NAV', 'REQUIRED', 'NAVIGATIONAL', 'Wedding Bands', '', NAVR)
L('TPL-HEADER', 'COM-FJ', 'PRIMARY_NAV', 'SITE_NAV', 'REQUIRED', 'NAVIGATIONAL', 'Fine Jewellery', '', NAVR, 'Label spelling (jewellery/jewelry) is open (Stage 12 D-15).')
L('TPL-HEADER', 'COM-FJ-EARRINGS', 'PRIMARY_NAV', 'SITE_NAV', 'REQUIRED', 'NAVIGATIONAL', 'Earrings', '', 'Stage 12 D-02: first-class in navigation.')
L('TPL-HEADER', 'COM-FJ-NECKLACES', 'PRIMARY_NAV', 'SITE_NAV', 'REQUIRED', 'NAVIGATIONAL', 'Necklaces & Pendants', '', 'Stage 12 D-02.')
L('TPL-HEADER', 'COM-FJ-BRACELETS', 'PRIMARY_NAV', 'SITE_NAV', 'REQUIRED', 'NAVIGATIONAL', 'Bracelets', '', 'Stage 12 D-02.')
L('TPL-HEADER', 'COM-BESPOKE', 'PRIMARY_NAV', 'SITE_NAV', 'REQUIRED', 'NAVIGATIONAL', 'Bespoke', '', NAVR)
L('TPL-HEADER', 'COM-LG-HUB', 'PRIMARY_NAV', 'SITE_NAV', 'CONDITIONAL', 'NAVIGATIONAL', 'Lab-Grown Diamonds', '',
  'Only if the commercial Lab-Grown hub is approved (Stage 12 D-05). This is the only page that may carry the bare head-term label.')
L('TPL-HEADER', 'EDU-ROOT', 'PRIMARY_NAV', 'SITE_NAV', 'REQUIRED', 'NAVIGATIONAL', 'Education', 'Diamond & Jewellery Guide', 'Resources grouping (Stage 12 D-01).')
L('TPL-HEADER', 'BLOG-HUB', 'PRIMARY_NAV', 'SITE_NAV', 'REQUIRED', 'NAVIGATIONAL', 'Journal', 'Blog', 'Resources grouping (Stage 12 D-01); Blog vs Journal naming is a brand choice (Stage 13 §14).')
L('TPL-HEADER', 'COM-SHOP', 'PRIMARY_NAV', 'SITE_NAV', 'RECOMMENDED', 'NAVIGATIONAL', 'Shop All', '', 'All-products listing (Stage 12 L1).')
L('TPL-FOOTER', 'SUP-FAQ', 'FOOTER', 'SITE_NAV', 'REQUIRED', 'NAVIGATIONAL', 'FAQ', '', 'Stage 12: FAQ in footer.')
L('TPL-FOOTER', 'SUP-POLICIES', 'FOOTER', 'SITE_NAV', 'REQUIRED', 'NAVIGATIONAL', 'Shipping / Returns / Privacy / Terms', '', 'Stage 12: policies in footer.')
L('TPL-FOOTER', 'BRAND-ABOUT', 'FOOTER', 'SITE_NAV', 'REQUIRED', 'NAVIGATIONAL', 'About', '', '')
L('TPL-FOOTER', 'BRAND-CONTACT', 'FOOTER', 'SITE_NAV', 'REQUIRED', 'NAVIGATIONAL', 'Contact', '', '')
L('TPL-FOOTER', 'EDU-RJG-02', 'FOOTER', 'SITE_NAV', 'RECOMMENDED', 'NAVIGATIONAL', 'Ring Size Guide', '',
  'Utility guide used across every ring purchase (Stage 14 N-RJG-02).', 'Points at the current /blog URL until the Stage 13 move executes.')
L('TPL-FOOTER', 'EDU-ROOT', 'FOOTER', 'SITE_NAV', 'OPTIONAL', 'NAVIGATIONAL', 'Education', '', 'Secondary path to the Education root.')

# --- homepage -----------------------------------------------------------------------------
L('NAV-HOME', 'COM-ER', 'COMMERCIAL_CTA', 'HOME_TO_CATEGORY', 'REQUIRED', 'BRANDED', 'House of Diams engagement rings', 'Explore engagement rings',
  'Stage 12 D-18: the homepage hands the engagement-ring subject to its category page (OV-13).')
L('NAV-HOME', 'COM-FJ', 'COMMERCIAL_CTA', 'HOME_TO_CATEGORY', 'RECOMMENDED', 'DESCRIPTIVE', 'Earrings, necklaces and bracelets', 'Fine jewellery', 'Second product family.')
L('NAV-HOME', 'COM-WB', 'COMMERCIAL_CTA', 'HOME_TO_CATEGORY', 'RECOMMENDED', 'DESCRIPTIVE', 'Wedding bands', '', 'Product family.')
L('NAV-HOME', 'COM-BESPOKE', 'COMMERCIAL_CTA', 'HOME_TO_CATEGORY', 'RECOMMENDED', 'NATURAL_LANGUAGE', 'Design a bespoke piece', '', 'Service entry.')
L('NAV-HOME', 'EDU-ROOT', 'EDUCATIONAL_CTA', 'HOME_TO_EDUCATION', 'RECOMMENDED', 'DESCRIPTIVE', 'Diamond and jewellery guides', '', 'Entry to the evergreen system.')
L('NAV-HOME', 'EDU-LG-02', 'EDUCATIONAL_CTA', 'HOME_TO_EDUCATION', 'OPTIONAL', 'NATURAL_LANGUAGE', 'Lab-grown or natural? See how they compare', '',
  'Protected ranking URL; supports the decision most lab-grown shoppers face.', 'Homepage must not host the comparison itself.')
L('NAV-HOME', 'COM-LG-HUB', 'COMMERCIAL_CTA', 'HOME_TO_CATEGORY', 'CONDITIONAL', 'NAVIGATIONAL', 'Lab-grown diamonds', '', 'Only if the commercial hub exists (D-05).')
L('NAV-HOME', 'BLOG-CRAFT', 'EDITORIAL', 'HOME_TO_BLOG', 'CONDITIONAL', 'BRANDED', 'Inside our Surat workshop', '',
  'Brand evidence (Stage 13 §1).', 'CONDITIONAL on craft posts existing; the Blog has no qualifying posts today (Stage 13).')

# --- engagement rings ---------------------------------------------------------------------
L('COM-ER', 'COM-ER-SIDESTONE', 'CATEGORY_NAV', 'CATEGORY_TO_SUBCATEGORY', 'REQUIRED', 'PARTIAL_MATCH', 'Side-stone engagement rings', 'Side-stone',
  'Stage 12 D-03: confirmed L2 style; its query SERP is CATEGORY (Stage 8).', 'Link the style URL directly; never the /by-desgin/ grouping page.')
L('COM-ER', 'COM-ER-STYLES', 'CATEGORY_NAV', 'CATEGORY_TO_SUBCATEGORY', 'CONDITIONAL', 'NAVIGATIONAL', 'Solitaire / Halo / Pave / Three-Stone / Bezel / Toi-et-Moi / Nature-Inspired', '',
  'Style tiles for populated styles only (Stage 12 D-03, D-07).')
L('COM-ER', 'COM-PDP', 'CATEGORY_NAV', 'CATEGORY_TO_PRODUCT', 'REQUIRED', 'NAVIGATIONAL', '(product name in grid)', '', 'Product grid.')
L('COM-ER', 'COM-PDP-OVAL-FLORAL', 'CATEGORY_NAV', 'CATEGORY_TO_PRODUCT', 'REQUIRED', 'NAVIGATIONAL', 'Oval Marquise Side-Stone Engagement Ring', '',
  'Ranking PDP stays in the engagement-ring grid while live.', 'Product name as shown on the PDP (Stage 10 title).')
L('COM-ER', 'EDU-SHP-00', 'CONTEXTUAL', 'CATEGORY_TO_EDUCATION', 'REQUIRED', 'DESCRIPTIVE', 'compare diamond shapes', 'which diamond shape suits you',
  'Shape is the first engagement-ring decision; the Shapes pillar includes engagement-ring shape choice (D14-17).')
L('COM-ER', 'EDU-4C-00', 'CONTEXTUAL', 'CATEGORY_TO_EDUCATION', 'REQUIRED', 'DESCRIPTIVE', 'how diamonds are graded (the 4Cs)', '',
  'Buyers compare grades; category copy links rather than re-explains (Stage 12 D-06).')
L('COM-ER', 'EDU-RJG-02', 'EDUCATIONAL_CTA', 'CATEGORY_TO_EDUCATION', 'REQUIRED', 'NATURAL_LANGUAGE', 'work out your ring size', '', 'Sizing is needed for every ring purchase (Stage 14 N-RJG-02).')
L('COM-ER', 'EDU-LG-02', 'CONTEXTUAL', 'CATEGORY_TO_EDUCATION', 'RECOMMENDED', 'NATURAL_LANGUAGE', 'how lab-grown and natural diamonds compare', '',
  'Protected ranking URL; origin is a common pre-purchase question.', 'One sentence + link; the category page must not host the comparison.')
L('COM-ER', 'EDU-LG-10', 'CONTEXTUAL', 'CATEGORY_TO_EDUCATION', 'OPTIONAL', 'DESCRIPTIVE', 'choosing a lab-grown diamond', '',
  'Protected ranking URL (pos 35).', 'Optional to respect the 5-link Education cap on category pages.')
L('COM-ER', 'COM-BESPOKE', 'COMMERCIAL_CTA', 'CATEGORY_TO_SERVICE', 'RECOMMENDED', 'NATURAL_LANGUAGE', 'create a custom engagement ring', '',
  'Bespoke is the commercial alternative for shoppers who do not find a design.', 'Links /bespoke; bespoke sub-pages are deferred (Stage 12).')
L('COM-ER', 'EXIST-BLOG-ER-ONLINE', 'RELATED_CONTENT', 'CATEGORY_TO_EDUCATION', 'OPTIONAL', 'NATURAL_LANGUAGE', 'tips for buying an engagement ring online', '',
  'Existing article on the ring-buying process.', 'Its destination (EDU-RJG-04) is DEFERRED pending D-19; do not promote it as a buying-guide owner.')
L('COM-ER-SIDESTONE', 'COM-ER', 'BREADCRUMB', 'CHILD_TO_HUB', 'REQUIRED', 'NAVIGATIONAL', 'Engagement Rings', '', 'Stage 12 hierarchy.')
L('COM-ER-SIDESTONE', 'COM-PDP', 'CATEGORY_NAV', 'CATEGORY_TO_PRODUCT', 'REQUIRED', 'NAVIGATIONAL', '(product name in grid)', '', 'Product grid.')
L('COM-ER-SIDESTONE', 'COM-PDP-OVAL-FLORAL', 'CATEGORY_NAV', 'CATEGORY_TO_PRODUCT', 'REQUIRED', 'NAVIGATIONAL', 'Oval Marquise Side-Stone Engagement Ring', '',
  'The ranking PDP is a side-stone design (Stage 10 title).')
L('COM-ER-SIDESTONE', 'EDU-RJG-01', 'CONTEXTUAL', 'CATEGORY_TO_EDUCATION', 'RECOMMENDED', 'DESCRIPTIVE', 'how different ring settings hold side stones', '',
  'Settings guide explains styles; the subcategory keeps the shopping query (Stage 13 row for side-stone).')
L('COM-ER-SIDESTONE', 'EDU-SHP-00', 'CONTEXTUAL', 'CATEGORY_TO_EDUCATION', 'OPTIONAL', 'DESCRIPTIVE', 'choosing a centre-stone shape', '', 'Shape choice for the centre stone.')
L('COM-ER-STYLES', 'COM-ER', 'BREADCRUMB', 'CHILD_TO_HUB', 'CONDITIONAL', 'NAVIGATIONAL', 'Engagement Rings', '', 'Stage 12 hierarchy.')
L('COM-ER-STYLES', 'COM-PDP', 'CATEGORY_NAV', 'CATEGORY_TO_PRODUCT', 'CONDITIONAL', 'NAVIGATIONAL', '(product name in grid)', '', 'Product grid.')
L('COM-ER-STYLES', 'EDU-RJG-01', 'CONTEXTUAL', 'CATEGORY_TO_EDUCATION', 'CONDITIONAL', 'DESCRIPTIVE', 'how this setting style works', '', 'Same pattern as side-stone.')

# --- wedding bands ------------------------------------------------------------------------
L('COM-WB', 'COM-WB-GENDER', 'CATEGORY_NAV', 'CATEGORY_TO_SUBCATEGORY', 'CONDITIONAL', 'NAVIGATIONAL', "Women's / Men's", '',
  'Stage 12 D-04: only populated splits; /for-him observed empty.')
L('COM-WB', 'COM-PDP', 'CATEGORY_NAV', 'CATEGORY_TO_PRODUCT', 'REQUIRED', 'NAVIGATIONAL', '(product name in grid)', '', 'Product grid.')
L('COM-WB', 'EDU-RJG-02', 'EDUCATIONAL_CTA', 'CATEGORY_TO_EDUCATION', 'REQUIRED', 'NATURAL_LANGUAGE', 'measure your band size', '', 'Sizing is needed for every band.')
L('COM-WB', 'EDU-MET-01', 'CONTEXTUAL', 'CATEGORY_TO_EDUCATION', 'RECOMMENDED', 'NATURAL_LANGUAGE', '14k or 18k gold for your band?', '',
  'Protected ranking URL; the validated band keywords are metal questions (Stage 12 D-04, CL-113).')
L('COM-WB', 'EDU-MET-00', 'CONTEXTUAL', 'CATEGORY_TO_EDUCATION', 'RECOMMENDED', 'DESCRIPTIVE', 'choosing a metal for your wedding band', '',
  'Metal is the main band decision.', 'Add when EDU-MET-00 launches (provisional).')
L('COM-WB', 'COM-ER', 'RELATED_CONTENT', 'CATEGORY_TO_CATEGORY', 'OPTIONAL', 'NATURAL_LANGUAGE', 'pair it with an engagement ring', '', 'Cross-sell between families.')
L('COM-WB-GENDER', 'COM-WB', 'BREADCRUMB', 'CHILD_TO_HUB', 'CONDITIONAL', 'NAVIGATIONAL', 'Wedding Bands', '', 'Stage 12 hierarchy.')
L('COM-WB-GENDER', 'COM-PDP', 'CATEGORY_NAV', 'CATEGORY_TO_PRODUCT', 'CONDITIONAL', 'NAVIGATIONAL', '(product name in grid)', '', 'Product grid.')

# --- fine jewellery -----------------------------------------------------------------------
for c, lab in [('COM-FJ-EARRINGS', 'Earrings'), ('COM-FJ-NECKLACES', 'Necklaces & Pendants'), ('COM-FJ-BRACELETS', 'Bracelets')]:
    L('COM-FJ', c, 'CATEGORY_NAV', 'CATEGORY_TO_SUBCATEGORY', 'REQUIRED', 'NAVIGATIONAL', lab, '', 'Stage 12 D-02: L2 under the umbrella.')
    L(c, 'COM-FJ', 'BREADCRUMB', 'CHILD_TO_HUB', 'REQUIRED', 'NAVIGATIONAL', 'Fine Jewellery', '', 'Stage 12 hierarchy.')
    L(c, 'COM-PDP', 'CATEGORY_NAV', 'CATEGORY_TO_PRODUCT', 'REQUIRED', 'NAVIGATIONAL', '(product name in grid)', '', 'Product grid.')
    L(c, 'COM-FJ-TYPE-SUBCATS', 'CATEGORY_NAV', 'CATEGORY_TO_SUBCATEGORY', 'CONDITIONAL', 'NAVIGATIONAL', '(type labels, e.g. Studs / Hoops & Huggies / Drop & Dangle)', '',
      'Populated type subcategories only (Stage 12 D-07).')
    L('COM-FJ-TYPE-SUBCATS', c, 'BREADCRUMB', 'CHILD_TO_HUB', 'CONDITIONAL', 'NAVIGATIONAL', lab, '', 'Breadcrumb for type subcategories of this parent.')
L('COM-FJ', 'COM-FJ-RINGS', 'CATEGORY_NAV', 'CATEGORY_TO_SUBCATEGORY', 'CONDITIONAL', 'NAVIGATIONAL', 'Rings', '', 'Stage 12: INSUFFICIENT EVIDENCE - DEFER.')
L('COM-FJ', 'EDU-4C-00', 'CONTEXTUAL', 'CATEGORY_TO_EDUCATION', 'OPTIONAL', 'DESCRIPTIVE', 'understanding diamond quality', '', 'One supporting link only.')
L('COM-FJ-EARRINGS', 'EDU-MET-00', 'CONTEXTUAL', 'CATEGORY_TO_EDUCATION', 'RECOMMENDED', 'NATURAL_LANGUAGE', 'which metals suit sensitive ears', '',
  'EDU-MET-00 owns hypoallergenic-metal questions (Stage 15).', 'Add when EDU-MET-00 launches. No earring-specific guide exists (keyword-data gap, D-19).')
L('COM-FJ-NECKLACES', 'COM-CURATED-TBAR', 'CATEGORY_NAV', 'CATEGORY_TO_SUBCATEGORY', 'CONDITIONAL', 'NAVIGATIONAL', 'T-Bar', '', 'Stage 12 D-14: placement deferred.')
L('COM-FJ-NECKLACES', 'EDU-4C-00', 'CONTEXTUAL', 'CATEGORY_TO_EDUCATION', 'OPTIONAL', 'DESCRIPTIVE', 'what diamond grades mean', '', 'One supporting link only.')
L('COM-FJ-BRACELETS', 'EDU-4C-00', 'CONTEXTUAL', 'CATEGORY_TO_EDUCATION', 'OPTIONAL', 'DESCRIPTIVE', 'how diamond quality is graded', '', 'One supporting link only.')
L('COM-FJ-TYPE-SUBCATS', 'COM-PDP', 'CATEGORY_NAV', 'CATEGORY_TO_PRODUCT', 'CONDITIONAL', 'NAVIGATIONAL', '(product name in grid)', '', 'Product grid.')
L('COM-FJ-RINGS', 'COM-FJ', 'BREADCRUMB', 'CHILD_TO_HUB', 'CONDITIONAL', 'NAVIGATIONAL', 'Fine Jewellery', '', 'Stage 12 hierarchy.')
L('COM-FJ-RINGS', 'COM-PDP', 'CATEGORY_NAV', 'CATEGORY_TO_PRODUCT', 'CONDITIONAL', 'NAVIGATIONAL', '(product name in grid)', '', 'Product grid.')
L('COM-CURATED-TBAR', 'COM-FJ-NECKLACES', 'BREADCRUMB', 'CHILD_TO_HUB', 'CONDITIONAL', 'NAVIGATIONAL', 'Necklaces & Pendants', '', 'Only if placed under necklaces (D-14).')
L('COM-CURATED-TBAR', 'COM-PDP', 'CATEGORY_NAV', 'CATEGORY_TO_PRODUCT', 'CONDITIONAL', 'NAVIGATIONAL', '(product name in grid)', '', 'Product grid.')

# --- shop all / lab-grown commercial hub / bespoke ----------------------------------------
L('COM-SHOP', 'COM-PDP', 'CATEGORY_NAV', 'CATEGORY_TO_PRODUCT', 'REQUIRED', 'NAVIGATIONAL', '(product name in grid)', '', 'All-products grid.')
L('COM-SHOP', 'COM-PDP-OVAL-FLORAL', 'CATEGORY_NAV', 'CATEGORY_TO_PRODUCT', 'REQUIRED', 'NAVIGATIONAL', 'Oval Marquise Side-Stone Engagement Ring', '', 'All-products grid.')
for c, lab in [('COM-ER', 'Engagement Rings'), ('COM-WB', 'Wedding Bands'), ('COM-FJ', 'Fine Jewellery')]:
    L('COM-SHOP', c, 'CATEGORY_NAV', 'CATEGORY_TO_SUBCATEGORY', 'RECOMMENDED', 'NAVIGATIONAL', lab, '', 'Shop-by-category entry points.')
L('COM-LG-HUB', 'EDU-LG-00', 'EDUCATIONAL_CTA', 'CATEGORY_TO_EDUCATION', 'CONDITIONAL', 'NATURAL_LANGUAGE', 'learn what a lab-grown diamond is', '',
  'Stage 12 D-05: commercial and Education pages for the same entity cross-link.')
L('COM-LG-HUB', 'EDU-LG-02', 'EDUCATIONAL_CTA', 'CATEGORY_TO_EDUCATION', 'CONDITIONAL', 'NATURAL_LANGUAGE', 'compare lab-grown and natural diamonds', '', 'Decision support.')
L('COM-LG-HUB', 'EDU-CERT-00', 'EDUCATIONAL_CTA', 'CATEGORY_TO_EDUCATION', 'CONDITIONAL', 'DESCRIPTIVE', 'how lab-grown diamonds are certified', '', 'Trust question.')
L('COM-LG-HUB', 'COM-ER', 'CATEGORY_NAV', 'CATEGORY_TO_SUBCATEGORY', 'CONDITIONAL', 'NAVIGATIONAL', 'Engagement rings', '',
  'Route to the product family.', "Do not label as 'lab-grown engagement rings': that landing page is deferred (D-05).")
L('COM-LG-HUB', 'COM-FJ', 'CATEGORY_NAV', 'CATEGORY_TO_SUBCATEGORY', 'CONDITIONAL', 'NAVIGATIONAL', 'Fine jewellery', '', 'Route to the product family.')
L('COM-BESPOKE', 'BRAND-CONTACT', 'COMMERCIAL_CTA', 'SERVICE_TO_CONTACT', 'REQUIRED', 'NATURAL_LANGUAGE', 'talk to our design team', '', 'Conversion step for the service.')
L('COM-BESPOKE', 'COM-ER', 'RELATED_CONTENT', 'SERVICE_TO_CATEGORY', 'RECOMMENDED', 'NATURAL_LANGUAGE', 'see our engagement ring designs', '', 'Design reference for commissions.')
L('COM-BESPOKE', 'BLOG-CRAFT', 'EDITORIAL', 'SERVICE_TO_BLOG', 'CONDITIONAL', 'BRANDED', 'how our Surat workshop makes each piece', '',
  'Stage 13 §12: Bespoke is the natural commercial partner of craft content.', 'CONDITIONAL on craft posts existing.')
L('COM-BESPOKE', 'BLOG-STORIES', 'EDITORIAL', 'SERVICE_TO_BLOG', 'CONDITIONAL', 'DESCRIPTIVE', 'recent client commissions', '', 'Stage 13: FUTURE POSSIBILITY (consent needed).')
L('COM-BESPOKE', 'EDU-SHP-00', 'CONTEXTUAL', 'CATEGORY_TO_EDUCATION', 'OPTIONAL', 'NATURAL_LANGUAGE', 'explore diamond shapes before your consultation', '', 'Helps the brief.')

# --- product template ----------------------------------------------------------------------
for c, lab, when in [('COM-ER', 'Engagement Rings', 'engagement-ring PDPs'), ('COM-WB', 'Wedding Bands', 'band PDPs'),
                     ('COM-FJ-EARRINGS', 'Earrings', 'earring PDPs'), ('COM-FJ-NECKLACES', 'Necklaces & Pendants', 'necklace/pendant PDPs'),
                     ('COM-FJ-BRACELETS', 'Bracelets', 'bracelet PDPs')]:
    L('COM-PDP', c, 'BREADCRUMB', 'PRODUCT_TO_CATEGORY', 'REQUIRED', 'NAVIGATIONAL', lab, '', f'Breadcrumb to the primary category ({when}).',
      'Product URLs stay flat; the category relationship is carried by breadcrumb and links (Stage 12 D-11).')
L('COM-PDP', 'COM-ER-SIDESTONE', 'BREADCRUMB', 'PRODUCT_TO_CATEGORY', 'REQUIRED', 'NAVIGATIONAL', 'Side-Stone', '', 'Breadcrumb for side-stone PDPs.')
L('COM-PDP', 'COM-ER-STYLES', 'BREADCRUMB', 'PRODUCT_TO_CATEGORY', 'CONDITIONAL', 'NAVIGATIONAL', '(style label)', '', 'Breadcrumb for other style PDPs, if the style listing is kept.')
L('COM-PDP', 'EDU-RJG-02', 'EDUCATIONAL_CTA', 'PRODUCT_TO_EDUCATION', 'REQUIRED', 'NAVIGATIONAL', 'Find your ring size', '',
  'Next to the size selector on ring and band PDPs only.', 'Template UI label; not an exact-match keyword.')
L('COM-PDP', 'EDU-4C-00', 'EDUCATIONAL_CTA', 'PRODUCT_TO_EDUCATION', 'RECOMMENDED', 'NAVIGATIONAL', 'What do these diamond grades mean?', '',
  'Beside the diamond spec table, only on PDPs that list grades.')
L('COM-PDP', 'EDU-CERT-00', 'EDUCATIONAL_CTA', 'PRODUCT_TO_EDUCATION', 'CONDITIONAL', 'NAVIGATIONAL', 'About diamond certification', '',
  'Only where the piece ships with a grading report.', 'Business fact not in project files: which products carry IGI/GIA reports.')
L('COM-PDP', 'EDU-MET-01', 'EDUCATIONAL_CTA', 'PRODUCT_TO_EDUCATION', 'CONDITIONAL', 'NAVIGATIONAL', '14k or 18k? How to choose', '',
  'Only on PDPs that offer both karats (protected ranking URL).', 'Business fact not in project files: karat options per product.')
L('COM-PDP', 'COM-PDP', 'PRODUCT_RECOMMENDATION', 'PRODUCT_TO_PRODUCT', 'RECOMMENDED', 'NAVIGATIONAL', '(related product names)', '',
  'Related products module.', 'SELF_TEMPLATE_JUSTIFIED: template-level relationship between different PDPs; a product never links to itself.')
L('COM-PDP', 'COM-PDP-OVAL-FLORAL', 'PRODUCT_RECOMMENDATION', 'PRODUCT_TO_PRODUCT', 'OPTIONAL', 'NAVIGATIONAL', 'Oval Marquise Side-Stone Engagement Ring', '',
  'Shown as a related product on other side-stone / oval designs.')
L('COM-PDP', 'COM-BESPOKE', 'COMMERCIAL_CTA', 'PRODUCT_TO_SERVICE', 'OPTIONAL', 'NATURAL_LANGUAGE', 'Commission a bespoke piece', '', 'Alternative path for custom requests.')
L('COM-PDP-OVAL-FLORAL', 'COM-ER-SIDESTONE', 'BREADCRUMB', 'PRODUCT_TO_CATEGORY', 'REQUIRED', 'NAVIGATIONAL', 'Side-Stone', '', 'Breadcrumb: Engagement Rings > Side-Stone.')
L('COM-PDP-OVAL-FLORAL', 'COM-ER', 'BREADCRUMB', 'PRODUCT_TO_CATEGORY', 'REQUIRED', 'NAVIGATIONAL', 'Engagement Rings', '', 'Breadcrumb.')
L('COM-PDP-OVAL-FLORAL', 'EDU-RJG-02', 'EDUCATIONAL_CTA', 'PRODUCT_TO_EDUCATION', 'REQUIRED', 'NAVIGATIONAL', 'Find your ring size', '', 'Same template link as all ring PDPs.')
L('COM-PDP-OVAL-FLORAL', 'EDU-SHP-00', 'EDUCATIONAL_CTA', 'PRODUCT_TO_EDUCATION', 'RECOMMENDED', 'DESCRIPTIVE', 'Compare diamond shapes', '',
  'The piece combines two shapes; the shapes pillar explains them.', "Never use 'marquise oval diamond' (this PDP's own ranking query) as the anchor to Education.")
L('COM-PDP-OVAL-FLORAL', 'EDU-4C-00', 'EDUCATIONAL_CTA', 'PRODUCT_TO_EDUCATION', 'OPTIONAL', 'NAVIGATIONAL', 'What do these diamond grades mean?', '', 'Same template link as other PDPs.')
L('COM-PDP-OVAL-FLORAL', 'COM-PDP', 'PRODUCT_RECOMMENDATION', 'PRODUCT_TO_PRODUCT', 'RECOMMENDED', 'NAVIGATIONAL', '(related side-stone ring names)', '', 'Related products.')

# --- Education: Lab-Grown ------------------------------------------------------------------
L('EDU-LG-00', 'EDU-LG-02', 'CONTEXTUAL', 'HUB_TO_CHILD', 'REQUIRED', 'EXACT_MATCH_ALLOWED', 'lab-grown vs natural diamonds', 'how lab-grown and natural diamonds differ',
  'Pillar sends the comparison question to its owner (protected ranking URL).', 'Also listed in the hub topic list.')
L('EDU-LG-00', 'EDU-LG-03', 'CONTEXTUAL', 'HUB_TO_CHILD', 'REQUIRED', 'EXACT_MATCH_ALLOWED', 'HPHT vs CVD', 'the two lab-growing methods compared',
  'Pillar mentions the two growth methods in one short section and hands depth to the single CVD/HPHT owner (D14-06; Stage 15 HIGH pair).',
  'Pillar must not carry its own CVD/HPHT sections. Also listed in the hub topic list.')
L('EDU-LG-00', 'EDU-LG-01', 'CONTEXTUAL', 'HUB_TO_CHILD', 'REQUIRED', 'EXACT_MATCH_ALLOWED', 'are lab-grown diamonds real', '',
  'Authenticity question goes to its owner.', 'Also listed in the hub topic list.')
L('EDU-LG-00', 'EDU-LG-10', 'CONTEXTUAL', 'HUB_TO_CHILD', 'REQUIRED', 'EXACT_MATCH_ALLOWED', 'how to choose a lab-grown diamond', '',
  'Buying-decision exit from the pillar (protected ranking URL).', 'Also listed in the hub topic list.')
L('EDU-LG-00', 'COM-LG-HUB', 'COMMERCIAL_CTA', 'EDUCATION_TO_CATEGORY', 'CONDITIONAL', 'PARTIAL_MATCH', 'shop lab-grown diamonds', '',
  'The commercial head term belongs to the conditional commercial hub (D-05, D14-05).')
L('EDU-LG-00', 'COM-ER', 'COMMERCIAL_CTA', 'EDUCATION_TO_CATEGORY', 'RECOMMENDED', 'DESCRIPTIVE', 'browse our engagement rings', '',
  'Decision-point exit while no commercial Lab-Grown hub exists.', "Anchor must not be 'lab-grown diamonds' (held for COM-LG-HUB).")
L('EDU-LG-00', 'EDU-NAT-00', 'RELATED_CONTENT', 'EDUCATION_CROSS_HUB', 'RECOMMENDED', 'NATURAL_LANGUAGE', 'how natural diamonds form', '', 'Origin contrast (cross-hub).')
L('EDU-LG-00', 'EDU-4C-00', 'RELATED_CONTENT', 'EDUCATION_CROSS_HUB', 'RECOMMENDED', 'DESCRIPTIVE', 'how lab-grown diamonds are graded', '',
  'Lab-grown grading lives in the general 4Cs pillar (D14-15).')
L('EDU-LG-00', 'EDU-CERT-00', 'RELATED_CONTENT', 'EDUCATION_CROSS_HUB', 'RECOMMENDED', 'DESCRIPTIVE', 'how lab-grown diamonds are certified', '', 'Certification pillar (cross-hub).')
L('EDU-LG-01', 'EDU-LG-02', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'REQUIRED', 'NATURAL_LANGUAGE', 'how lab-grown and natural diamonds differ', '',
  'D14-07: authenticity and comparison each link to the other.')
L('EDU-LG-01', 'EDU-LG-03', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'REQUIRED', 'DESCRIPTIVE', 'how CVD and HPHT diamonds are grown', '',
  "Protected ranking URL: 'are cvd diamonds real' ranks on EDU-LG-03 (pos 27).", 'EDU-LG-01 answers CVD authenticity in one sentence and links; no CVD section.')
L('EDU-LG-01', 'EDU-LG-09', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'RECOMMENDED', 'NATURAL_LANGUAGE', 'whether a lab-grown diamond passes a diamond tester', '',
  'Tester questions belong to EDU-LG-09 (D14-13).')
L('EDU-LG-01', 'EDU-LG-08', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'RECOMMENDED', 'NATURAL_LANGUAGE', 'whether lab-grown diamonds change over time', '',
  'Appearance/durability belongs to EDU-LG-08.', "Avoid 'look real' wording in this anchor.")
L('EDU-LG-01', 'EDU-CERT-00', 'CONTEXTUAL', 'EDUCATION_CROSS_HUB', 'RECOMMENDED', 'DESCRIPTIVE', 'how grading reports identify lab-grown diamonds', '', 'Proof of origin.')
L('EDU-LG-01', 'EDU-GEM-00', 'CONTEXTUAL', 'EDUCATION_CROSS_HUB', 'CONDITIONAL', 'NATURAL_LANGUAGE', 'the difference between a lab-grown diamond and a simulant', '',
  'Only if the Gemstones & Alternatives hub is approved (D14-20).')
L('EDU-LG-01', 'COM-ER', 'COMMERCIAL_CTA', 'EDUCATION_TO_CATEGORY', 'OPTIONAL', 'DESCRIPTIVE', 'see our engagement rings', '', 'Single commercial exit.')
L('EDU-LG-02', 'EDU-LG-01', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'REQUIRED', 'NATURAL_LANGUAGE', 'why lab-grown diamonds are real diamonds', '', 'D14-07 reciprocal link.')
L('EDU-LG-02', 'EDU-LG-05', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'REQUIRED', 'PARTIAL_MATCH', 'whether lab-grown diamonds hold their value', '',
  'Price/resale depth belongs to EDU-LG-05 (D14-10).')
L('EDU-LG-02', 'EDU-LG-07', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'RECOMMENDED', 'DESCRIPTIVE', 'the ethics and environmental footprint of lab-grown diamonds', '', 'Ethics depth.')
L('EDU-LG-02', 'EDU-NAT-00', 'CONTEXTUAL', 'EDUCATION_CROSS_HUB', 'REQUIRED', 'NATURAL_LANGUAGE', 'how natural diamonds form underground', '', 'Natural formation depth.')
L('EDU-LG-02', 'EDU-LG-03', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'RECOMMENDED', 'DESCRIPTIVE', 'the two ways lab diamonds are grown', '', 'Links two protected URLs.')
L('EDU-LG-02', 'EDU-LG-10', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'RECOMMENDED', 'NATURAL_LANGUAGE', 'choosing a lab-grown diamond step by step', '', 'Next step after deciding on origin.')
L('EDU-LG-02', 'EDU-LG-06', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'CONDITIONAL', 'DESCRIPTIVE', 'pros and cons of lab-grown diamonds', '',
  'If EDU-LG-06 is created, the interim worth-it section is reduced to a summary plus this link (D14-27 rule 7).')
L('EDU-LG-02', 'EDU-4C-00', 'RELATED_CONTENT', 'EDUCATION_CROSS_HUB', 'OPTIONAL', 'NATURAL_LANGUAGE', 'both are graded on the same 4Cs', '', 'Shared grading.')
L('EDU-LG-02', 'COM-ER', 'COMMERCIAL_CTA', 'EDUCATION_TO_CATEGORY', 'RECOMMENDED', 'BRANDED', 'browse House of Diams engagement rings', '', 'Comparison is COMMERCIAL_RESEARCH; decision-point exit.')
L('EDU-LG-02', 'COM-LG-HUB', 'COMMERCIAL_CTA', 'EDUCATION_TO_CATEGORY', 'CONDITIONAL', 'PARTIAL_MATCH', 'explore lab-grown diamond jewellery', '', 'If the commercial hub exists.')
L('EDU-LG-03', 'EDU-LG-09', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'RECOMMENDED', 'DESCRIPTIVE', 'how gemologists identify lab-grown diamonds', '',
  'Detection belongs to EDU-LG-09.', "The excluded query 'cvd/hpht diamond tester' is never used as an anchor.")
L('EDU-LG-03', 'EDU-LG-08', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'OPTIONAL', 'DESCRIPTIVE', 'post-growth treatments and colour', '', 'Treatment effects on appearance.')
L('EDU-LG-03', 'EDU-LG-10', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'RECOMMENDED', 'NATURAL_LANGUAGE', 'whether growth method should affect your choice', '', 'Buying next step.')
L('EDU-LG-03', 'EDU-LG-02', 'RELATED_CONTENT', 'CHILD_TO_RELATED_CHILD', 'OPTIONAL', 'NATURAL_LANGUAGE', 'how lab-grown diamonds compare with natural ones', '', 'Related comparison.')
L('EDU-LG-03', 'EDU-LG-04', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'CONDITIONAL', 'DESCRIPTIVE', 'the growing process step by step', '',
  'Only if EDU-LG-04 is created (D14-08).', 'EDU-LG-04 must not target CVD/HPHT method queries (Stage 15 HIGH pair).')
L('EDU-LG-03', 'COM-ER', 'COMMERCIAL_CTA', 'EDUCATION_TO_CATEGORY', 'OPTIONAL', 'DESCRIPTIVE', 'browse finished engagement rings', '', 'Single commercial exit.')
L('EDU-LG-04', 'EDU-LG-03', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'CONDITIONAL', 'DESCRIPTIVE', 'how CVD and HPHT compare', '', 'Method comparison stays on EDU-LG-03.')
L('EDU-LG-05', 'EDU-LG-02', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'REQUIRED', 'NATURAL_LANGUAGE', 'whether a lab-grown diamond is worth it compared with natural', '',
  "EDU-LG-02 is the interim home for 'worth it' (CL-012) while EDU-LG-06 is conditional.")
L('EDU-LG-05', 'EDU-LG-06', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'CONDITIONAL', 'DESCRIPTIVE', 'the full pros and cons', '', 'Only if EDU-LG-06 is created.')
L('EDU-LG-05', 'EDU-NAT-01', 'CONTEXTUAL', 'EDUCATION_CROSS_HUB', 'CONDITIONAL', 'DESCRIPTIVE', 'natural diamond value and rarity', '', "Depends on HOD's natural offering (Stage 12 Q1).")
L('EDU-LG-05', 'COM-ER', 'COMMERCIAL_CTA', 'EDUCATION_TO_CATEGORY', 'OPTIONAL', 'DESCRIPTIVE', 'see current engagement ring designs', '', 'No price figures in Education (Stage 13).')
L('EDU-LG-05', 'COM-LG-HUB', 'COMMERCIAL_CTA', 'EDUCATION_TO_CATEGORY', 'CONDITIONAL', 'PARTIAL_MATCH', 'browse lab-grown diamond jewellery', '', 'If the commercial hub exists.')
L('EDU-LG-06', 'EDU-LG-02', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'CONDITIONAL', 'DESCRIPTIVE', 'the head-to-head comparison', '', 'If created.')
L('EDU-LG-06', 'EDU-LG-05', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'CONDITIONAL', 'DESCRIPTIVE', 'resale value explained', '', 'If created.')
L('EDU-LG-07', 'EDU-LG-02', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'RECOMMENDED', 'NATURAL_LANGUAGE', 'how lab-grown and natural diamonds compare on ethics', '', 'Protected ranking URL.')
L('EDU-LG-07', 'EDU-NAT-02', 'CONTEXTUAL', 'EDUCATION_CROSS_HUB', 'CONDITIONAL', 'DESCRIPTIVE', 'conflict-free natural diamond sourcing', '', 'Only if EDU-NAT-02 is created (sourcing policy needed).')
L('EDU-LG-07', 'BLOG-CRAFT', 'EDITORIAL', 'EDUCATION_TO_BLOG', 'CONDITIONAL', 'BRANDED', 'how House of Diams makes its jewellery', '',
  'Stage 13 §11: Education may cite Blog as first-hand evidence.', 'Only substantiated claims (trust principle).')
L('EDU-LG-08', 'EDU-LG-01', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'RECOMMENDED', 'NATURAL_LANGUAGE', 'why lab-grown diamonds are chemically real diamonds', '',
  "Boundary: 'look real' is appearance (here), authenticity is EDU-LG-01.")
L('EDU-LG-08', 'EDU-4C-05', 'CONTEXTUAL', 'EDUCATION_CROSS_HUB', 'RECOMMENDED', 'DESCRIPTIVE', 'how diamond color is graded', '', 'Colour tints link to colour grading.')
L('EDU-LG-08', 'EDU-GEN-01', 'CONTEXTUAL', 'EDUCATION_CROSS_HUB', 'RECOMMENDED', 'DESCRIPTIVE', 'how hard and durable diamonds are', '', 'Durability science.')
L('EDU-LG-08', 'EDU-LG-03', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'OPTIONAL', 'DESCRIPTIVE', 'post-growth treatment and growth methods', '', 'Treatments relate to growth method.')
L('EDU-LG-09', 'EDU-LG-01', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'RECOMMENDED', 'NATURAL_LANGUAGE', 'what makes a lab-grown diamond a real diamond', '', 'LOW pair (Stage 15): detection vs authenticity.')
L('EDU-LG-09', 'EDU-CERT-00', 'CONTEXTUAL', 'EDUCATION_CROSS_HUB', 'RECOMMENDED', 'DESCRIPTIVE', 'how a grading lab confirms origin', '', 'Lab identification.')
L('EDU-LG-09', 'EDU-LG-03', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'OPTIONAL', 'DESCRIPTIVE', 'CVD and HPHT growth methods', '', 'Method context for identification.')
L('EDU-LG-09', 'EDU-GEM-00', 'CONTEXTUAL', 'EDUCATION_CROSS_HUB', 'CONDITIONAL', 'DESCRIPTIVE', 'how testers treat simulants', '', 'Only if the Gemstones hub is approved; moissanite tester detail deferred (D14-13).')
L('EDU-LG-10', 'EDU-4C-00', 'CONTEXTUAL', 'EDUCATION_CROSS_HUB', 'REQUIRED', 'DESCRIPTIVE', 'the 4Cs of diamond quality', '', 'Stone selection starts with grades.')
L('EDU-LG-10', 'EDU-CERT-00', 'CONTEXTUAL', 'EDUCATION_CROSS_HUB', 'REQUIRED', 'NATURAL_LANGUAGE', 'why certification matters', '', 'Certificate check is a selection step.')
L('EDU-LG-10', 'EDU-LG-03', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'REQUIRED', 'NATURAL_LANGUAGE', 'CVD or HPHT: does it matter?', '', 'Links two protected URLs.')
L('EDU-LG-10', 'EDU-SHP-00', 'CONTEXTUAL', 'EDUCATION_CROSS_HUB', 'RECOMMENDED', 'DESCRIPTIVE', 'choosing a diamond shape', '', 'Shape selection.')
L('EDU-LG-10', 'EDU-LG-02', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'RECOMMENDED', 'NATURAL_LANGUAGE', 'deciding between lab-grown and natural first', '', 'Origin decision.')
L('EDU-LG-10', 'COM-ER', 'COMMERCIAL_CTA', 'EDUCATION_TO_CATEGORY', 'REQUIRED', 'NATURAL_LANGUAGE', 'shop engagement rings', '', 'Buying guide -> category at the decision point (Stage 13 §9).')
L('EDU-LG-10', 'COM-LG-HUB', 'COMMERCIAL_CTA', 'EDUCATION_TO_CATEGORY', 'CONDITIONAL', 'PARTIAL_MATCH', 'see lab-grown diamond pieces', '', 'If the commercial hub exists.')
L('EDU-LG-10', 'EXIST-BLOG-ER-ONLINE', 'RELATED_CONTENT', 'CHILD_TO_RELATED_CHILD', 'OPTIONAL', 'NATURAL_LANGUAGE', 'buying the finished ring online', '',
  'Different step (ring purchase logistics).', 'Boundary INSUFFICIENT_EVIDENCE (OV-06, D-19): keep anchors on stone choice vs ring purchase.')

# --- Education: Natural / 4Cs / Shapes / Certification / Metals / RJG / GEN -----------------
L('EDU-NAT-00', 'EDU-LG-02', 'CONTEXTUAL', 'EDUCATION_CROSS_HUB', 'REQUIRED', 'NATURAL_LANGUAGE', 'comparing natural and lab-grown diamonds', '', 'Protected ranking URL; cross-hub.',
  'No commercial link: the natural commercial hub is deferred (Stage 12 D-05).')
L('EDU-NAT-00', 'EDU-GEN-01', 'CONTEXTUAL', 'EDUCATION_CROSS_HUB', 'RECOMMENDED', 'PARTIAL_MATCH', 'what diamonds are made of', '', 'Composition belongs to EDU-GEN-01.')
L('EDU-NAT-00', 'EDU-LG-00', 'RELATED_CONTENT', 'EDUCATION_CROSS_HUB', 'RECOMMENDED', 'NATURAL_LANGUAGE', 'how lab-grown diamonds are made instead', '', 'Process vs formation contrast.')
L('EDU-NAT-02', 'EDU-LG-07', 'CONTEXTUAL', 'EDUCATION_CROSS_HUB', 'CONDITIONAL', 'DESCRIPTIVE', 'lab-grown ethics and sustainability', '', 'MEDIUM boundary (D14-11).')
L('EDU-4C-00', 'EDU-4C-01', 'CONTEXTUAL', 'HUB_TO_CHILD', 'REQUIRED', 'DESCRIPTIVE', 'our diamond clarity guide', '', 'Clarity section -> clarity owner.', 'Also listed in the hub topic list.')
L('EDU-4C-00', 'EDU-4C-05', 'CONTEXTUAL', 'HUB_TO_CHILD', 'REQUIRED', 'DESCRIPTIVE', 'how diamond color is graded from D to Z', '', 'Colour section -> colour owner.', 'Also listed in the hub topic list.')
L('EDU-4C-00', 'EDU-4C-06', 'CONTEXTUAL', 'HUB_TO_CHILD', 'REQUIRED', 'DESCRIPTIVE', 'what makes a good cut grade', '', 'Cut section -> cut owner.', 'Also listed in the hub topic list.')
L('EDU-4C-00', 'EDU-4C-07', 'CONTEXTUAL', 'HUB_TO_CHILD', 'REQUIRED', 'DESCRIPTIVE', 'how carat weight relates to size', '', 'Carat section -> carat owner.', 'Also listed in the hub topic list.')
L('EDU-4C-00', 'EDU-LG-10', 'CONTEXTUAL', 'EDUCATION_CROSS_HUB', 'REQUIRED', 'NATURAL_LANGUAGE', 'using the 4Cs to choose a lab-grown diamond', '', 'Protected ranking URL.')
L('EDU-4C-00', 'EDU-CERT-00', 'CONTEXTUAL', 'EDUCATION_CROSS_HUB', 'RECOMMENDED', 'DESCRIPTIVE', 'where grades come from: diamond certification', '', 'Grades come from reports.')
L('EDU-4C-00', 'COM-ER', 'COMMERCIAL_CTA', 'EDUCATION_TO_CATEGORY', 'RECOMMENDED', 'DESCRIPTIVE', 'explore engagement rings', '', 'Decision-point exit (H1 of existing article is a choosing guide).')
L('EDU-4C-01', 'EDU-4C-02', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'REQUIRED', 'DESCRIPTIVE', 'SI1 and SI2 clarity explained', '', 'Grade explainer (D14-14).')
L('EDU-4C-01', 'EDU-4C-03', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'REQUIRED', 'DESCRIPTIVE', 'VVS and flawless clarity explained', '', 'Grade explainer (D14-14).')
L('EDU-4C-01', 'EDU-4C-04', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'CONDITIONAL', 'DESCRIPTIVE', 'VS1 and VS2 clarity explained', '', 'VS stays a section of EDU-4C-01 until EDU-4C-04 is justified.')
L('EDU-4C-02', 'EDU-4C-01', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'REQUIRED', 'PARTIAL_MATCH', 'the full diamond clarity scale', '', 'LOW pair: grade page -> scale owner.')
L('EDU-4C-02', 'EDU-4C-03', 'RELATED_CONTENT', 'CHILD_TO_RELATED_CHILD', 'RECOMMENDED', 'NATURAL_LANGUAGE', 'how SI compares with VVS', '', 'Sibling grade.')
L('EDU-4C-03', 'EDU-4C-01', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'REQUIRED', 'NATURAL_LANGUAGE', 'where VVS sits on the clarity scale', '', 'LOW pair: grade page -> scale owner.')
L('EDU-4C-03', 'EDU-4C-02', 'RELATED_CONTENT', 'CHILD_TO_RELATED_CHILD', 'RECOMMENDED', 'NATURAL_LANGUAGE', 'SI clarity as a value alternative', '', 'Sibling grade.')
L('EDU-4C-05', 'EDU-MET-00', 'CONTEXTUAL', 'EDUCATION_CROSS_HUB', 'RECOMMENDED', 'NATURAL_LANGUAGE', 'how metal colour affects diamond colour', '', 'Colour vs metal (Stage 14 N-4C-05).')
L('EDU-4C-05', 'EDU-4C-08', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'CONDITIONAL', 'DESCRIPTIVE', 'fancy-colored diamonds', '', "Depends on HOD's fancy-colour offering.")
L('EDU-4C-06', 'EDU-SHP-00', 'CONTEXTUAL', 'EDUCATION_CROSS_HUB', 'REQUIRED', 'DESCRIPTIVE', 'diamond shapes, which are different from cut grade', '', 'Cut vs shape disambiguation (D14-02 SPLIT).')
L('EDU-4C-07', 'EDU-SHP-00', 'RELATED_CONTENT', 'EDUCATION_CROSS_HUB', 'OPTIONAL', 'NATURAL_LANGUAGE', 'how shape changes apparent size', '', 'Size perception.')
L('EDU-4C-07', 'COM-ER', 'COMMERCIAL_CTA', 'EDUCATION_TO_CATEGORY', 'OPTIONAL', 'DESCRIPTIVE', 'view engagement ring designs', '', "'Is it big enough' is a decision point.")
L('EDU-4C-08', 'EDU-4C-05', 'CONTEXTUAL', 'CHILD_TO_RELATED_CHILD', 'CONDITIONAL', 'DESCRIPTIVE', 'D-to-Z colour grading', '', 'If created.')
L('EDU-SHP-00', 'EDU-4C-06', 'CONTEXTUAL', 'EDUCATION_CROSS_HUB', 'REQUIRED', 'DESCRIPTIVE', 'cut grade, which is different from shape', '', 'Cut vs shape disambiguation (D14-02).')
L('EDU-SHP-00', 'EDU-RJG-01', 'CONTEXTUAL', 'EDUCATION_CROSS_HUB', 'RECOMMENDED', 'DESCRIPTIVE', 'settings that suit each shape', '', 'Shape by setting.')
L('EDU-SHP-00', 'COM-ER', 'COMMERCIAL_CTA', 'EDUCATION_TO_CATEGORY', 'REQUIRED', 'DESCRIPTIVE', 'explore engagement ring designs', '', 'Pillar includes engagement-ring shape choice (D14-17).',
  'Per-shape shopping pages are deferred; do not link shape names to filter URLs.')
L('EDU-SHP-00', 'COM-PDP-OVAL-FLORAL', 'CONTEXTUAL', 'EDUCATION_TO_PRODUCT', 'RECOMMENDED', 'DESCRIPTIVE', 'an oval centre stone with marquise side stones', '',
  'Illustrative example in the oval/marquise section (Stage 13 §9: Education -> Product sparingly).', 'Only while the product is live; product name/description anchor, never its ranking query.')
L('EDU-SHP-00', 'EDU-4C-07', 'RELATED_CONTENT', 'EDUCATION_CROSS_HUB', 'RECOMMENDED', 'NATURAL_LANGUAGE', 'how carat weight looks across shapes', '', 'Size perception.')
L('EDU-CERT-00', 'EDU-CERT-01', 'CONTEXTUAL', 'HUB_TO_CHILD', 'REQUIRED', 'PARTIAL_MATCH', 'GIA vs IGI compared', '',
  'The retarget and the GIA-vs-IGI narrowing ship together (Stage 13); OV-01 persists otherwise.', 'Also listed in the hub topic list.')
L('EDU-CERT-00', 'EDU-4C-00', 'CONTEXTUAL', 'EDUCATION_CROSS_HUB', 'RECOMMENDED', 'DESCRIPTIVE', 'what the grades on a report mean', '', 'Grade definitions are Diamond Quality.')
L('EDU-CERT-00', 'EDU-LG-10', 'CONTEXTUAL', 'EDUCATION_CROSS_HUB', 'RECOMMENDED', 'NATURAL_LANGUAGE', 'using a certificate to choose a lab-grown diamond', '', 'Protected ranking URL.')
L('EDU-CERT-00', 'COM-ER', 'COMMERCIAL_CTA', 'EDUCATION_TO_CATEGORY', 'CONDITIONAL', 'DESCRIPTIVE', 'engagement rings with certified diamonds', '',
  'Only if HOD pieces ship with grading reports (business fact not in project files).')
L('EDU-CERT-01', 'EDU-LG-10', 'CONTEXTUAL', 'EDUCATION_CROSS_HUB', 'RECOMMENDED', 'NATURAL_LANGUAGE', 'choosing a lab-grown diamond with confidence', '', 'Protected ranking URL.')
L('EDU-CERT-01', 'COM-ER', 'COMMERCIAL_CTA', 'EDUCATION_TO_CATEGORY', 'CONDITIONAL', 'DESCRIPTIVE', 'see which report comes with our rings', '', 'Only if report type per product is confirmed.')
L('EDU-CERT-02', 'EDU-4C-00', 'CONTEXTUAL', 'EDUCATION_CROSS_HUB', 'CONDITIONAL', 'DESCRIPTIVE', 'grade definitions', '', 'If created.')
L('EDU-MET-00', 'EDU-MET-01', 'CONTEXTUAL', 'HUB_TO_CHILD', 'REQUIRED', 'PARTIAL_MATCH', '14k vs 18k gold compared', '', 'Protected ranking URL; karat depth.', 'Also listed in the hub topic list.')
L('EDU-MET-00', 'COM-WB', 'COMMERCIAL_CTA', 'EDUCATION_TO_CATEGORY', 'RECOMMENDED', 'DESCRIPTIVE', 'browse wedding bands', '', 'Metal choice is the main band decision.')
L('EDU-MET-00', 'COM-ER', 'COMMERCIAL_CTA', 'EDUCATION_TO_CATEGORY', 'RECOMMENDED', 'DESCRIPTIVE', 'explore our engagement rings', '', 'Decision-point exit.')
L('EDU-MET-00', 'EDU-4C-05', 'RELATED_CONTENT', 'EDUCATION_CROSS_HUB', 'OPTIONAL', 'NATURAL_LANGUAGE', 'how metal colour changes how a diamond looks', '', 'Colour vs metal.')
L('EDU-MET-00', 'EDU-RJG-03', 'RELATED_CONTENT', 'EDUCATION_CROSS_HUB', 'CONDITIONAL', 'DESCRIPTIVE', 'caring for gold and platinum', '', 'If the care guide is created.')
L('EDU-MET-01', 'COM-ER', 'COMMERCIAL_CTA', 'EDUCATION_TO_CATEGORY', 'REQUIRED', 'DESCRIPTIVE', 'see engagement ring designs', '', "Existing H1 frames the choice for an engagement ring (Stage 10).")
L('EDU-MET-01', 'COM-WB', 'COMMERCIAL_CTA', 'EDUCATION_TO_CATEGORY', 'RECOMMENDED', 'DESCRIPTIVE', 'explore wedding bands', '', 'Karat choice for bands.')
L('EDU-MET-01', 'EDU-4C-05', 'RELATED_CONTENT', 'EDUCATION_CROSS_HUB', 'OPTIONAL', 'NATURAL_LANGUAGE', 'how gold colour affects diamond colour', '', 'Colour vs metal.')
L('EDU-MET-02', 'EDU-RJG-03', 'RELATED_CONTENT', 'EDUCATION_CROSS_HUB', 'CONDITIONAL', 'DESCRIPTIVE', 'everyday care', '', 'If both are created.')
L('EDU-RJG-01', 'COM-ER-SIDESTONE', 'COMMERCIAL_CTA', 'EDUCATION_TO_CATEGORY', 'REQUIRED', 'PARTIAL_MATCH', 'side-stone engagement rings', '',
  'Protected ranking URL: the side-stone section hands the shopping query to its commercial owner.', 'The guide explains settings; it never targets the style shopping query.')
L('EDU-RJG-01', 'COM-ER', 'COMMERCIAL_CTA', 'EDUCATION_TO_CATEGORY', 'REQUIRED', 'DESCRIPTIVE', 'engagement rings by setting style', '', 'Decision-point exit.')
L('EDU-RJG-01', 'COM-ER-STYLES', 'COMMERCIAL_CTA', 'EDUCATION_TO_CATEGORY', 'CONDITIONAL', 'DESCRIPTIVE', 'halo, pave, bezel and solitaire designs', '', 'Only to populated style listings.')
L('EDU-RJG-01', 'EDU-SHP-00', 'CONTEXTUAL', 'EDUCATION_CROSS_HUB', 'RECOMMENDED', 'DESCRIPTIVE', 'which diamond shapes suit each setting', '', 'Shape by setting.')
L('EDU-RJG-01', 'BLOG-CRAFT', 'EDITORIAL', 'EDUCATION_TO_BLOG', 'CONDITIONAL', 'BRANDED', 'see how our setters work', '', 'Stage 13 §9: optional first-hand evidence link.')
L('EDU-RJG-02', 'SUP-FAQ', 'CONTEXTUAL', 'EDUCATION_TO_SUPPORT', 'REQUIRED', 'BRANDED', 'our resizing policy', '', 'D14-30: HOD resizing policy stays on the FAQ.')
L('EDU-RJG-02', 'COM-ER', 'COMMERCIAL_CTA', 'EDUCATION_TO_CATEGORY', 'REQUIRED', 'DESCRIPTIVE', 'shop engagement rings in your size', '', 'Tool/guide -> category (D14-23).')
L('EDU-RJG-02', 'COM-WB', 'COMMERCIAL_CTA', 'EDUCATION_TO_CATEGORY', 'RECOMMENDED', 'DESCRIPTIVE', 'shop wedding bands', '', 'Tool/guide -> category (D14-23).')
L('EDU-RJG-03', 'EDU-MET-02', 'RELATED_CONTENT', 'EDUCATION_CROSS_HUB', 'CONDITIONAL', 'DESCRIPTIVE', 'rhodium replating', '', 'If both are created.')
L('EDU-GEN-01', 'EDU-LG-08', 'CONTEXTUAL', 'EDUCATION_CROSS_HUB', 'RECOMMENDED', 'NATURAL_LANGUAGE', 'how lab-grown diamonds hold up over time', '', 'Durability for lab-grown.')
L('EDU-GEN-01', 'EDU-NAT-00', 'CONTEXTUAL', 'EDUCATION_CROSS_HUB', 'RECOMMENDED', 'DESCRIPTIVE', 'how diamonds form in nature', '', 'Formation belongs to EDU-NAT-00.')
L('EDU-GEN-01', 'EDU-RJG-03', 'CONTEXTUAL', 'EDUCATION_CROSS_HUB', 'CONDITIONAL', 'DESCRIPTIVE', 'caring for diamond jewellery every day', '', 'If the care guide is created.')
L('EDU-GEM-00', 'EDU-LG-01', 'CONTEXTUAL', 'EDUCATION_CROSS_HUB', 'CONDITIONAL', 'DESCRIPTIVE', 'lab-grown diamonds are real diamonds, not simulants', '', 'MEDIUM boundary simulants vs authenticity.')
L('EDU-GEM-01', 'EDU-LG-00', 'CONTEXTUAL', 'EDUCATION_CROSS_HUB', 'CONDITIONAL', 'DESCRIPTIVE', 'what a lab-grown diamond is', '', 'If the hub is approved. No moissanite commercial link (HOD sale unconfirmed).')
L('EDU-GEM-02', 'EDU-GEM-01', 'RELATED_CONTENT', 'CHILD_TO_RELATED_CHILD', 'CONDITIONAL', 'DESCRIPTIVE', 'moissanite compared with lab-grown diamond', '', 'If both are created.')

# --- existing deferred article ------------------------------------------------------------
L('EXIST-BLOG-ER-ONLINE', 'BLOG-HUB', 'BREADCRUMB', 'CHILD_TO_HUB', 'REQUIRED', 'NAVIGATIONAL', 'Journal', '', 'Stays a /blog article until Stage 13 DEFER is resolved.')
L('EXIST-BLOG-ER-ONLINE', 'EDU-LG-10', 'CONTEXTUAL', 'BLOG_TO_EDUCATION', 'RECOMMENDED', 'NATURAL_LANGUAGE', 'choosing the lab-grown diamond itself', '',
  'Protected ranking URL; stone selection belongs to EDU-LG-10 (presumed survivor, Stage 13).', 'INSUFFICIENT_EVIDENCE boundary (OV-06, D-19).')
L('EXIST-BLOG-ER-ONLINE', 'COM-ER', 'COMMERCIAL_CTA', 'BLOG_TO_CATEGORY', 'REQUIRED', 'NATURAL_LANGUAGE', 'browse engagement rings online', '', 'Ring-buying article -> category.')
L('EXIST-BLOG-ER-ONLINE', 'EDU-RJG-02', 'CONTEXTUAL', 'BLOG_TO_EDUCATION', 'RECOMMENDED', 'NATURAL_LANGUAGE', 'measure your ring size at home', '', 'Sizing step.')
L('EXIST-BLOG-ER-ONLINE', 'EDU-SHP-00', 'CONTEXTUAL', 'BLOG_TO_EDUCATION', 'RECOMMENDED', 'NATURAL_LANGUAGE', 'pick a diamond shape', '', 'Shape step.')
L('EXIST-BLOG-ER-ONLINE', 'EDU-MET-01', 'CONTEXTUAL', 'BLOG_TO_EDUCATION', 'RECOMMENDED', 'NATURAL_LANGUAGE', 'choosing between 14k and 18k gold', '', 'Metal step (protected ranking URL).')
L('EXIST-BLOG-ER-ONLINE', 'EDU-4C-00', 'CONTEXTUAL', 'BLOG_TO_EDUCATION', 'OPTIONAL', 'DESCRIPTIVE', 'the 4Cs explained', '', '4Cs step.')

# --- Blog ----------------------------------------------------------------------------------
BLOGC = [('BLOG-CRAFT', 'Craft & Making'), ('BLOG-STYLE', 'Style & Trends'), ('BLOG-GIFTS', 'Gifts & Occasions'),
         ('BLOG-LAUNCH', 'Collections & Launches'), ('BLOG-STORIES', 'Stories'), ('BLOG-INDUSTRY', 'Industry Notes')]
for b, lab in BLOGC:
    L('BLOG-HUB', b, 'CATEGORY_NAV', 'HUB_TO_CHILD', 'REQUIRED', 'NAVIGATIONAL', '(post title)', '',
      'Blog hub lists posts chronologically (Stage 13 §5).', f"'{lab}' category label only once the category holds posts; no empty category pages.")
    L(b, 'BLOG-HUB', 'BREADCRUMB', 'CHILD_TO_HUB', 'REQUIRED', 'NAVIGATIONAL', 'Journal', '', 'Blog breadcrumb.')
L('BLOG-HUB', 'EXIST-BLOG-ER-ONLINE', 'CATEGORY_NAV', 'HUB_TO_CHILD', 'REQUIRED', 'NAVIGATIONAL', '(article title)', '',
  'Current and only path: the Blog hub listing (Stage 10). Its Education destination (EDU-RJG-04) is DEFERRED, so the listing stays.',
  'Not boosted with extra contextual links while the D-19 / OV-06 boundary is unresolved.')
L('BLOG-HUB', 'EDU-ROOT', 'EDUCATIONAL_CTA', 'BLOG_TO_EDUCATION', 'RECOMMENDED', 'DESCRIPTIVE', 'diamond and jewellery buying guides', '', 'Routes evergreen needs to Education (Stage 13 §4).')
for t in ['EDU-LG-01', 'EDU-LG-02', 'EDU-LG-03', 'EDU-LG-10', 'EDU-4C-00', 'EDU-SHP-00', 'EDU-CERT-00', 'EDU-MET-01', 'EDU-RJG-02']:
    L('BLOG-HUB', t, 'CATEGORY_NAV', 'HUB_TO_CHILD_TRANSITIONAL', 'CONDITIONAL', 'NAVIGATIONAL', '(article title)', '',
      'Current observed path: the Blog hub lists all 10 existing articles (Stage 10).',
      'TRANSITIONAL: keep this listing until the Education path to the article is live; removal after that is a UX choice (Stage 13 §14 Q2). Never remove before a replacement path exists.')
L('BLOG-CRAFT', 'COM-BESPOKE', 'COMMERCIAL_CTA', 'BLOG_TO_CATEGORY', 'REQUIRED', 'NATURAL_LANGUAGE', 'commission your own piece', '', 'Stage 13 §12: Bespoke is the natural commercial link for craft content.')
L('BLOG-CRAFT', 'EDU-RJG-01', 'CONTEXTUAL', 'BLOG_TO_EDUCATION', 'RECOMMENDED', 'DESCRIPTIVE', 'ring setting styles explained', '', 'Concept owner for setting techniques.')
L('BLOG-CRAFT', 'EDU-MET-00', 'CONTEXTUAL', 'BLOG_TO_EDUCATION', 'OPTIONAL', 'DESCRIPTIVE', 'a guide to jewellery metals', '', 'Concept owner for metals.')
L('BLOG-CRAFT', 'COM-PDP', 'EDITORIAL', 'BLOG_TO_PRODUCT', 'OPTIONAL', 'NAVIGATIONAL', '(name of the featured piece)', '', 'Live products only; review when retired.')
L('BLOG-CRAFT', 'BRAND-ABOUT', 'EDITORIAL', 'BLOG_TO_BRAND', 'RECOMMENDED', 'BRANDED', 'the House of Diams story', '', 'Brand context.')
L('BLOG-CRAFT', 'BLOG-STORIES', 'RELATED_CONTENT', 'BLOG_TO_RELATED_BLOG', 'CONDITIONAL', 'DESCRIPTIVE', 'a finished commission', '', 'Only where both posts exist and the story continues.')
L('BLOG-STYLE', 'COM-ER', 'EDITORIAL', 'BLOG_TO_CATEGORY', 'RECOMMENDED', 'BRANDED', 'our engagement ring collection', '', 'Featured family (Stage 13 §9).')
L('BLOG-STYLE', 'COM-FJ', 'EDITORIAL', 'BLOG_TO_CATEGORY', 'RECOMMENDED', 'BRANDED', 'our fine jewellery', '', 'Featured family.')
L('BLOG-STYLE', 'COM-WB', 'EDITORIAL', 'BLOG_TO_CATEGORY', 'OPTIONAL', 'DESCRIPTIVE', 'wedding bands to pair with it', '', 'Featured family.')
L('BLOG-STYLE', 'COM-ER-SIDESTONE', 'EDITORIAL', 'BLOG_TO_CATEGORY', 'OPTIONAL', 'DESCRIPTIVE', 'side-stone designs', '', 'When a trend features side stones (protected ranking URL).')
L('BLOG-STYLE', 'EDU-SHP-00', 'CONTEXTUAL', 'BLOG_TO_EDUCATION', 'RECOMMENDED', 'DESCRIPTIVE', 'compare every diamond shape', '', 'Stage 13 framework: dated shape-trend pieces link to the shapes owner.')
L('BLOG-STYLE', 'EDU-RJG-01', 'CONTEXTUAL', 'BLOG_TO_EDUCATION', 'OPTIONAL', 'DESCRIPTIVE', 'how each setting style works', '', 'Concept owner.')
L('BLOG-STYLE', 'COM-PDP', 'EDITORIAL', 'BLOG_TO_PRODUCT', 'OPTIONAL', 'NAVIGATIONAL', '(name of the featured piece)', '', 'Live products only.')
for c, a in [('COM-FJ-EARRINGS', 'earrings to give'), ('COM-FJ-NECKLACES', 'necklaces and pendants'), ('COM-FJ-BRACELETS', 'bracelets for every occasion')]:
    L('BLOG-GIFTS', c, 'EDITORIAL', 'BLOG_TO_CATEGORY', 'REQUIRED', 'DESCRIPTIVE', a, '',
      'Stage 13 §12: gift guides link to categories rather than long product lists.', 'Required when the guide features this family.')
L('BLOG-GIFTS', 'EDU-RJG-02', 'CONTEXTUAL', 'BLOG_TO_EDUCATION', 'RECOMMENDED', 'NATURAL_LANGUAGE', 'how to find out a ring size discreetly', '', 'Ring gifts need a size.')
L('BLOG-GIFTS', 'COM-PDP', 'EDITORIAL', 'BLOG_TO_PRODUCT', 'OPTIONAL', 'NAVIGATIONAL', '(name of the featured piece)', '', 'A few featured pieces; live only.')
L('BLOG-GIFTS', 'COM-BESPOKE', 'COMMERCIAL_CTA', 'BLOG_TO_CATEGORY', 'OPTIONAL', 'NATURAL_LANGUAGE', 'commission something one of a kind', '', 'Custom gift route.')
L('BLOG-LAUNCH', 'COM-PDP', 'EDITORIAL', 'BLOG_TO_PRODUCT', 'REQUIRED', 'NAVIGATIONAL', '(names of the launched pieces)', '', 'Launch posts link the live pieces (Stage 13 §9).')
L('BLOG-LAUNCH', 'COM-FJ', 'EDITORIAL', 'BLOG_TO_CATEGORY', 'REQUIRED', 'DESCRIPTIVE', 'the full fine jewellery collection', '',
  'A launch post never replaces the category page (Stage 13 rule 7).', 'Required when the launch is a fine-jewellery family; use COM-ER for bridal launches.')
L('BLOG-LAUNCH', 'COM-ER', 'EDITORIAL', 'BLOG_TO_CATEGORY', 'REQUIRED', 'DESCRIPTIVE', 'the engagement ring collection', '', 'Required when the launch is bridal.')
L('BLOG-LAUNCH', 'COM-CURATED-TBAR', 'EDITORIAL', 'BLOG_TO_CATEGORY', 'CONDITIONAL', 'DESCRIPTIVE', 'the T-Bar collection', '', 'Only if T-Bar is kept as a curated collection (D-14).')
L('BLOG-LAUNCH', 'BLOG-CRAFT', 'RELATED_CONTENT', 'BLOG_TO_RELATED_BLOG', 'OPTIONAL', 'NATURAL_LANGUAGE', 'how the collection was made', '', 'Editorially useful continuation.')
L('BLOG-LAUNCH', 'EDU-4C-00', 'CONTEXTUAL', 'BLOG_TO_EDUCATION', 'OPTIONAL', 'DESCRIPTIVE', 'diamond grades explained', '', 'Concept owner when grades are mentioned.')
L('BLOG-STORIES', 'COM-BESPOKE', 'COMMERCIAL_CTA', 'BLOG_TO_CATEGORY', 'CONDITIONAL', 'NATURAL_LANGUAGE', 'start your own commission', '', 'Stage 13: client stories support Bespoke.')
L('BLOG-STORIES', 'BRAND-ABOUT', 'EDITORIAL', 'BLOG_TO_BRAND', 'CONDITIONAL', 'BRANDED', 'who we are', '', 'Brand context.')
L('BLOG-STORIES', 'BLOG-CRAFT', 'RELATED_CONTENT', 'BLOG_TO_RELATED_BLOG', 'CONDITIONAL', 'DESCRIPTIVE', 'how the piece was made', '', 'Only where both exist.')
L('BLOG-INDUSTRY', 'EDU-LG-00', 'CONTEXTUAL', 'BLOG_TO_EDUCATION', 'REQUIRED', 'NATURAL_LANGUAGE', 'what lab-grown diamonds are', '', 'Evergreen concept owner (Stage 13 framework).')
L('BLOG-INDUSTRY', 'EDU-LG-05', 'CONTEXTUAL', 'BLOG_TO_EDUCATION', 'REQUIRED', 'NATURAL_LANGUAGE', 'how lab-grown diamond value works', '',
  'Dated price commentary is Blog; evergreen value principles are EDU-LG-05 (Stage 13 framework).')
L('BLOG-INDUSTRY', 'EDU-LG-02', 'CONTEXTUAL', 'BLOG_TO_EDUCATION', 'RECOMMENDED', 'NATURAL_LANGUAGE', 'lab-grown and natural, compared in depth', '', 'Protected ranking URL.')
L('BLOG-INDUSTRY', 'EDU-LG-03', 'CONTEXTUAL', 'BLOG_TO_EDUCATION', 'RECOMMENDED', 'DESCRIPTIVE', 'how CVD and HPHT production differ', '', 'Protected ranking URL.')
L('BLOG-INDUSTRY', 'EDU-LG-07', 'CONTEXTUAL', 'BLOG_TO_EDUCATION', 'RECOMMENDED', 'DESCRIPTIVE', 'lab-grown sustainability explained', '', 'Concept owner.')
L('BLOG-INDUSTRY', 'COM-LG-HUB', 'COMMERCIAL_CTA', 'BLOG_TO_CATEGORY', 'CONDITIONAL', 'PARTIAL_MATCH', 'our lab-grown diamond collection', '', 'If the commercial hub exists.')

# --- FAQ / brand / Education root extras ------------------------------------------------
L('SUP-FAQ', 'EDU-LG-01', 'CONTEXTUAL', 'FAQ_TO_EDUCATION', 'REQUIRED', 'NATURAL_LANGUAGE', 'more on whether lab-grown diamonds are real', '', 'D14-30: legitimacy -> EDU-LG-01.')
L('SUP-FAQ', 'EDU-LG-02', 'CONTEXTUAL', 'FAQ_TO_EDUCATION', 'REQUIRED', 'NATURAL_LANGUAGE', 'our full lab-grown vs natural comparison', '', 'D14-30: lab vs natural -> EDU-LG-02 (protected ranking URL).',
  'FAQ keeps a one-line answer; no full comparison on the FAQ (OV-10).')
L('SUP-FAQ', 'EDU-CERT-00', 'CONTEXTUAL', 'FAQ_TO_EDUCATION', 'REQUIRED', 'DESCRIPTIVE', 'how diamond certification works', '', 'D14-30: certification -> EDU-CERT-00.')
L('SUP-FAQ', 'EDU-CERT-01', 'CONTEXTUAL', 'FAQ_TO_EDUCATION', 'RECOMMENDED', 'NATURAL_LANGUAGE', 'GIA or IGI: which report?', '', 'D14-30: certification -> EDU-CERT-01.')
L('SUP-FAQ', 'EDU-RJG-02', 'CONTEXTUAL', 'FAQ_TO_EDUCATION', 'REQUIRED', 'NATURAL_LANGUAGE', 'how to measure your ring size', '', 'D14-30: resizing -> EDU-RJG-02 for the general explanation.')
L('SUP-FAQ', 'EDU-LG-09', 'CONTEXTUAL', 'FAQ_TO_EDUCATION', 'OPTIONAL', 'NATURAL_LANGUAGE', "can a jeweller tell it's lab-grown?", '', 'Only if the FAQ carries a tester question.')
L('SUP-FAQ', 'SUP-POLICIES', 'CONTEXTUAL', 'FAQ_TO_SUPPORT', 'REQUIRED', 'DESCRIPTIVE', 'shipping and returns policies', '', 'Service answers.')
L('SUP-FAQ', 'BRAND-CONTACT', 'CONTEXTUAL', 'FAQ_TO_SUPPORT', 'REQUIRED', 'NAVIGATIONAL', 'contact us', '', 'Service answers.')
L('SUP-FAQ', 'COM-BESPOKE', 'CONTEXTUAL', 'FAQ_TO_CATEGORY', 'RECOMMENDED', 'BRANDED', 'our bespoke service', '', 'Custom-order question.')
L('SUP-FAQ', 'COM-ER', 'CONTEXTUAL', 'FAQ_TO_CATEGORY', 'OPTIONAL', 'DESCRIPTIVE', 'browse engagement rings', '', 'Where an answer ends in a shopping step.')
L('SUP-POLICIES', 'SUP-FAQ', 'CONTEXTUAL', 'SUPPORT_TO_SUPPORT', 'RECOMMENDED', 'NAVIGATIONAL', 'FAQ', '', 'Support path.')
L('BRAND-ABOUT', 'BLOG-CRAFT', 'EDITORIAL', 'BRAND_TO_BLOG', 'CONDITIONAL', 'BRANDED', 'stories from our Surat workshop', '', 'CONDITIONAL on craft posts existing.')
L('BRAND-ABOUT', 'COM-BESPOKE', 'COMMERCIAL_CTA', 'BRAND_TO_CATEGORY', 'RECOMMENDED', 'BRANDED', 'our bespoke service', '', 'Brand -> service.')
L('BRAND-ABOUT', 'COM-ER', 'COMMERCIAL_CTA', 'BRAND_TO_CATEGORY', 'OPTIONAL', 'DESCRIPTIVE', 'see our engagement rings', '', 'Brand -> category.')
L('BRAND-CONTACT', 'COM-BESPOKE', 'CONTEXTUAL', 'BRAND_TO_CATEGORY', 'OPTIONAL', 'BRANDED', 'about our bespoke service', '', 'Visitors contacting HOD are often commission enquiries.')
L('EDU-ROOT', 'BLOG-HUB', 'RELATED_CONTENT', 'EDUCATION_TO_BLOG', 'OPTIONAL', 'BRANDED', 'stories from the House of Diams journal', '', 'Stage 13 §9: Education -> Blog optional.')
for t in ['EDU-LG-01', 'EDU-LG-02', 'EDU-LG-03', 'EDU-LG-10', 'EDU-MET-01', 'EDU-RJG-02', 'EDU-CERT-01']:
    L('EDU-ROOT', t, 'CATEGORY_NAV', 'HUB_TO_CHILD_TRANSITIONAL', 'CONDITIONAL', 'NAVIGATIONAL', LABEL[t], '',
      f'Interim Education path until the parent hub ({PARENT[t]}) is live.',
      'TRANSITIONAL: replace with the hub listing once the parent hub launches. Gives the Education-owned /blog articles an Education path now.')

# ---------------------------------------------------------------- cannibalization pairs
PAIRS = {
    frozenset(['EDU-LG-01', 'EDU-LG-02']): ('MEDIUM', 'Authenticity vs comparison (D14-07): anchors name the other page\'s distinct question.'),
    frozenset(['EDU-LG-02', 'EDU-LG-05']): ('MEDIUM', "Money-worry overlap: worth-it stays on EDU-LG-02 (interim), value/resale on EDU-LG-05."),
    frozenset(['EDU-LG-00', 'EDU-LG-03']): ('HIGH', 'Pillar keeps a one-paragraph mention of methods and links; all CVD/HPHT depth stays on EDU-LG-03.'),
    frozenset(['EDU-4C-00', 'EDU-4C-01']): ('MEDIUM', 'Pillar clarity section is a summary + link; clarity-scale depth stays on EDU-4C-01.'),
    frozenset(['EDU-CERT-00', 'EDU-CERT-01']): ('MEDIUM', 'General certification vs GIA-vs-IGI: ship together; comparison anchors only to EDU-CERT-01.'),
    frozenset(['EDU-4C-06', 'EDU-SHP-00']): ('MEDIUM', "'Cut' is ambiguous: cut-grade anchors -> EDU-4C-06, shape anchors -> EDU-SHP-00."),
    frozenset(['EDU-LG-08', 'EDU-LG-01']): ('MEDIUM', "'Look real' is appearance (EDU-LG-08); anchor to EDU-LG-01 avoids that wording."),
    frozenset(['EDU-LG-09', 'EDU-LG-01']): ('LOW', 'Detection owns tester questions; authenticity anchors avoid tester wording.'),
    frozenset(['EDU-LG-00', 'COM-LG-HUB']): ('MEDIUM', 'Head terms stay with the commercial hub; the Education pillar never takes the bare head-term anchor.'),
    frozenset(['EDU-LG-10', 'EXIST-BLOG-ER-ONLINE']): ('INSUFFICIENT_EVIDENCE', 'OV-06/D-19 unresolved: stone choice (EDU-LG-10) vs ring purchase (online article).'),
    frozenset(['EDU-4C-02', 'EDU-4C-01']): ('LOW', 'SI SERP shares 0 URLs with the clarity scale.'),
    frozenset(['EDU-4C-03', 'EDU-4C-01']): ('LOW', 'VVS SERP shares 1 URL with the clarity scale.'),
    frozenset(['EDU-LG-03', 'EDU-LG-04']): ('HIGH', 'D14-27: process page (if created) must not target CVD/HPHT method queries.'),
    frozenset(['EDU-LG-07', 'EDU-NAT-02']): ('MEDIUM', 'Lab-grown ethics vs natural conflict-free sourcing (D14-11).'),
    frozenset(['EDU-LG-05', 'EDU-LG-06']): ('MEDIUM', 'Price/resale vs worth-it (D14-27).'),
    frozenset(['EDU-LG-02', 'EDU-LG-06']): ('MEDIUM', 'Interim worth-it section on EDU-LG-02 shrinks to summary + link if EDU-LG-06 is created.'),
    frozenset(['EDU-LG-09', 'EDU-GEM-00']): ('MEDIUM', 'Lab-grown detection vs simulant/moissanite testing (D14-27).'),
    frozenset(['EDU-GEM-00', 'EDU-LG-01']): ('MEDIUM', 'Simulants vs authenticity (D14-27).'),
    frozenset(['COM-ER-SIDESTONE', 'EDU-RJG-01']): ('LOW', 'Settings guide explains styles; the subcategory owns the shopping query (Stage 13).'),
    frozenset(['COM-PDP-OVAL-FLORAL', 'EDU-SHP-00']): ('LOW', "Shape pillar must not take the PDP's PRODUCT-SERP query 'marquise oval diamond' (CL-063 excluded from Education)."),
}

# ---------------------------------------------------------------- protection
PROT_BY_URL = collections.Counter(p['ranking_url'] for p in PROT)
URL2PID = {PAGES[p]['url']: p for p in PAGES if PAGES[p]['cop'] == 'EXISTING'}
PROT_PAGE = {}
for u, n in PROT_BY_URL.items():
    PROT_PAGE[URL2PID[u]] = n
TARGETED = collections.Counter(URL2PID[p['ranking_url']] for p in PROT if p['mapped_target_id'].startswith('EDU') or p['mapped_target_id'].startswith('COM'))


def prot_label(pid):
    if pid not in PROT_PAGE:
        return 'NONE'
    n, t = PROT_PAGE[pid], TARGETED[pid]
    s = f'SUPPORTS_PROTECTED_RANKING_URL ({t} targeted Stage 3 kw'
    if n != t:
        s += f'; {n - t} ranking kw not targeted'
    return s + '; URL unchanged)'


# ---------------------------------------------------------------- write link map
def url_of(pid):
    return PAGES[pid]['url']


rows = []
for (s, t), d in LINKS.items():
    pair = frozenset([s, t])
    cann, guard = PAIRS.get(pair, ('NONE_IDENTIFIED', ''))
    if d['link_type'] in STRUCT and cann == 'NONE_IDENTIFIED':
        cann = 'NONE (structural)'
    req = {'REQUIRED': 'YES', 'RECOMMENDED': 'NO', 'OPTIONAL': 'NO', 'CONDITIONAL': 'CONDITIONAL'}[d['priority']]
    notes = ' '.join(x for x in [d['notes'], f'Guard: {guard}' if guard else ''] if x)
    rows.append(dict(
        source_page_id=s, source_page_type=PAGES[s]['page_type'], source_url_or_expression=url_of(s), source_business_area=PAGES[s]['area'],
        target_page_id=t, target_page_type=PAGES[t]['page_type'], target_url_or_expression=url_of(t), target_business_area=PAGES[t]['area'],
        link_type=d['link_type'], relationship_type=d['relationship_type'], priority=d['priority'], required_at_launch=req,
        anchor_type=d['anchor_type'], recommended_anchor=d['recommended_anchor'], anchor_variants=d['anchor_variants'],
        context_reason=d['context_reason'], ranking_equity_protection=prot_label(t), cannibalization_risk=cann, notes=notes))
LCOLS = ['source_page_id', 'source_page_type', 'source_url_or_expression', 'source_business_area', 'target_page_id', 'target_page_type',
         'target_url_or_expression', 'target_business_area', 'link_type', 'relationship_type', 'priority', 'required_at_launch', 'anchor_type',
         'recommended_anchor', 'anchor_variants', 'context_reason', 'ranking_equity_protection', 'cannibalization_risk', 'notes']


def write(path, cols, data):
    with open(P(path), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(data)


write('architecture/16_internal_link_map.csv', LCOLS, rows)

# ---------------------------------------------------------------- connectivity
inc = collections.defaultdict(list)
out = collections.defaultdict(list)
for r in rows:
    inc[r['target_page_id']].append(r)
    out[r['source_page_id']].append(r)

# Current observed state for existing pages (Stage 1/10 facts only; no crawl/link-count data exists)
OBSERVED = {
    'NAV-HOME': ('WELL_CONNECTED', 'Site root; global logo link on every page (Stage 1).'),
    'COM-SHOP': ('NAV_ONLY', 'In sitemap; apparent parent of product nav (Stage 1). No contextual links recorded.'),
    'COM-ER': ('NAV_ONLY', 'In sitemap and main nav (Stage 1/10). Contextual incoming links not measured.'),
    'COM-WB': ('NAV_ONLY', 'In sitemap and main nav (Stage 1/10).'),
    'COM-FJ': ('NAV_ONLY', 'In sitemap and main nav (Stage 1/10).'),
    'COM-FJ-EARRINGS': ('NAV_ONLY', 'Linked from category nav; NOT in sitemap (Stage 10 §1a).'),
    'COM-FJ-NECKLACES': ('NAV_ONLY', 'Linked from category nav; NOT in sitemap (Stage 10 §1a).'),
    'COM-FJ-BRACELETS': ('NAV_ONLY', 'Linked from category nav; NOT in sitemap (Stage 10 §1a).'),
    'COM-ER-SIDESTONE': ('NAV_ONLY', 'Linked from engagement-ring nav under /by-desgin/; NOT in sitemap (Stage 10 §1a). Ranks pos 104.'),
    'COM-ER-STYLES': ('NAV_ONLY', 'Nav-linked; NOT in sitemap (Stage 10 §1a).'),
    'COM-WB-GENDER': ('NAV_ONLY', 'Nav-linked; NOT in sitemap; /for-him branch empty (Stage 10 §1a).'),
    'COM-FJ-TYPE-SUBCATS': ('NAV_ONLY', 'Nav-linked; NOT in sitemap; several observed empty (Stage 10 §1a).'),
    'COM-FJ-RINGS': ('NAV_ONLY', 'Nav-linked; NOT in sitemap (Stage 10 §1a).'),
    'COM-CURATED-TBAR': ('NAV_ONLY', 'In sitemap; top-level style collection (Stage 1).'),
    'COM-BESPOKE': ('NAV_ONLY', 'In sitemap and nav (Stage 1). No supporting editorial content (Stage 13 §13).'),
    'COM-PDP': ('NAV_ONLY', 'Reached through product grids (/shop, categories) only; no contextual links recorded (Stage 1).'),
    'COM-PDP-OVAL-FLORAL': ('NAV_ONLY', 'In sitemap; reached through product grids only. Ranks pos 90.'),
    'EDU-ROOT': ('WEAKLY_CONNECTED', 'In sitemap; nav placement not recorded; lists 1 article (Stage 10 §7).'),
    'BLOG-HUB': ('WEAKLY_CONNECTED', 'In sitemap; nav placement not recorded; lists 10 articles (Stage 10).'),
    'SUP-FAQ': ('NAV_ONLY', 'In sitemap (footer/utility); no H1 (Stage 1).'),
    'SUP-POLICIES': ('NAV_ONLY', 'In sitemap (footer).'),
    'BRAND-ABOUT': ('NAV_ONLY', 'In sitemap; no H1 (Stage 1).'),
    'BRAND-CONTACT': ('NAV_ONLY', 'In sitemap.'),
    'EDU-CERT-01': ('WEAKLY_CONNECTED', 'In sitemap; the only article listed on /education (Stage 10 §7). Contextual links not measured.'),
    'EXIST-BLOG-ER-ONLINE': ('WEAKLY_CONNECTED', 'In sitemap; listed on /blog hub only (Stage 10). Contextual links not measured.'),
}
for p in PAGES:
    if PAGES[p]['url'].startswith('/blog/') and p not in OBSERVED:
        OBSERVED[p] = ('WEAKLY_CONNECTED', 'In sitemap; listed on /blog hub only; not listed on /education (Stage 10). Contextual links not measured.')

HUBLIKE = {'CATEGORY_HUB', 'EDUCATION_HUB', 'EDUCATION_TOPIC_HUB_INDEX', 'BLOG_HUB', 'HOMEPAGE', 'ALL_PRODUCTS_LISTING', 'FAQ_HELP',
           'POLICY_PAGE_GROUP', 'BRAND_PAGE', 'SITE_TEMPLATE', 'SERVICE_PAGE', 'ORIGIN_HUB'}


def is_struct(r):
    # a hub topic list exists even when the hub->child row is recorded as a contextual body link
    return r['link_type'] in STRUCT or r['relationship_type'].startswith('HUB_TO_CHILD')


def planned(pid):
    live = [r for r in inc[pid] if r['priority'] != 'CONDITIONAL' and r['source_page_id'] != pid]
    st = [r for r in live if is_struct(r)]
    cx = [r for r in live if r['link_type'] in CTX and r['priority'] in ('REQUIRED', 'RECOMMENDED')]
    pt = PAGES[pid]['page_type']
    if pt in ('HOMEPAGE', 'ALL_PRODUCTS_LISTING'):
        ok = len(st) >= 1
    elif pt in HUBLIKE:
        ok = len(st) >= 2 or (len(st) >= 1 and len(cx) >= 1)
    elif pid.startswith('COM') or pid.startswith('BLOG'):
        ok = len(st) >= 1 and (len(cx) >= 1 or pt in ('SUBCATEGORY', 'SUBCATEGORY_GROUP', 'CATEGORY', 'BLOG_POST_TEMPLATE', 'CURATED_COLLECTION'))
    else:
        ok = len(st) >= 1 and len(cx) >= 2
    return ok, len(st), len(cx)


conn = []
req_rows = []
for pid in PAGES:
    pg = PAGES[pid]
    if is_template(pid):
        continue
    ic = [r for r in inc[pid] if r['source_page_id'] != pid]
    oc = [r for r in out[pid] if r['target_page_id'] != pid]
    ic_ctx = [r for r in ic if r['link_type'] in CTX]
    ic_st = [r for r in ic if is_struct(r)]
    ok, nst, ncx = planned(pid)
    cond = is_cond(pid)
    existing = pg['cop'] in ('EXISTING', 'EXISTING_GROUP', 'EXISTING_CONDITIONAL')
    if existing:
        status, obs = OBSERVED[pid]
    else:
        status, obs = 'LINKING_REQUIREMENT_AT_LAUNCH', 'Page does not exist yet; counts are required/expected relationships, not live links.'
    reqin = sorted({r['source_page_id'] for r in ic if r['priority'] == 'REQUIRED'})
    if cond:
        risk = 'CONDITIONAL'
        fix = 'Only if the condition is met: add the CONDITIONAL rows in 16_internal_link_map.csv at the same release as the page.'
    elif pid in PROT_PAGE:
        risk = 'HIGH' if pid in ('EDU-LG-03', 'EDU-LG-02') else 'MEDIUM'
        fix = f"Protected ranking URL (unchanged). Add the {len([r for r in ic_ctx if r['priority'] in ('REQUIRED', 'RECOMMENDED')])} REQUIRED/RECOMMENDED contextual links; keep the /blog hub listing until an Education path is live."
    elif status in ('NAV_ONLY', 'WEAKLY_CONNECTED'):
        risk = 'MEDIUM' if ncx else 'LOW'
        fix = 'Add the REQUIRED incoming rows' + (' and the contextual rows' if ncx else '') + ' from 16_internal_link_map.csv.'
    elif status == 'LINKING_REQUIREMENT_AT_LAUNCH':
        risk = 'LAUNCH_BLOCKER_IF_MISSING'
        fix = f"Launch only with the {len(reqin)} REQUIRED incoming links in place (sources: {'; '.join(reqin)})."
    else:
        risk = 'LOW'
        fix = 'None beyond the REQUIRED rows.'
    plan = f"Planned at launch: {nst} structural + {ncx} contextual (REQUIRED/RECOMMENDED, non-conditional) incoming -> {'meets' if ok else 'BELOW'} the connectivity bar."
    conn.append(dict(page_id=pid, page_type=pg['page_type'], current_or_proposed=pg['cop'], incoming_link_count=len(ic),
                     contextual_incoming_count=len(ic_ctx), structural_incoming_count=len(ic_st), outgoing_link_count=len(oc),
                     status=status, risk=risk, required_fix=fix, notes=f'Current: {obs} {plan}'))

    # requirements
    def fmt(rs):
        ids = sorted({r for r in rs})
        return f"{len(ids)}: {'; '.join(ids)}" if ids else '0'
    inc_req = [r['source_page_id'] for r in ic if r['priority'] == 'REQUIRED']
    inc_rec = [r['source_page_id'] for r in ic if r['priority'] in ('RECOMMENDED', 'OPTIONAL')]
    out_req = [r['target_page_id'] for r in oc if r['priority'] == 'REQUIRED']
    out_rec = [r['target_page_id'] for r in oc if r['priority'] in ('RECOMMENDED', 'OPTIONAL')]
    parent = PARENT.get(pid, '')
    if not parent:
        bc = [r['target_page_id'] for r in oc if r['link_type'] == 'BREADCRUMB']
        parent = '; '.join(sorted(set(bc)))
    children = sorted({r['target_page_id'] for r in oc if r['relationship_type'] in ('HUB_TO_CHILD', 'CATEGORY_TO_SUBCATEGORY', 'CATEGORY_TO_PRODUCT')})
    related = sorted({r['target_page_id'] for r in oc if r['relationship_type'] in ('CHILD_TO_RELATED_CHILD', 'EDUCATION_CROSS_HUB', 'BLOG_TO_RELATED_BLOG')})
    if existing:
        launch = f"Existing page: keep current paths; add REQUIRED rows ({len(set(inc_req))} incoming / {len(set(out_req))} outgoing)."
    elif cond:
        launch = 'IF_ACTIVATED: publish with its CONDITIONAL rows (parent hub listing, breadcrumb, named related links). Not linked before it exists.'
    else:
        launch = f"LINKING_REQUIREMENT_AT_LAUNCH: {len(set(inc_req))} REQUIRED incoming and {len(set(out_req))} REQUIRED outgoing links must ship with the page."
    rp = f'YES ({PROT_PAGE[pid]} Stage 3 kw; URL preserved)' if pid in PROT_PAGE else 'NO'
    req_rows.append(dict(page_id=pid, page_type=pg['page_type'], business_area=pg['area'], current_or_proposed=pg['cop'],
                         incoming_required=fmt(inc_req), incoming_recommended=fmt(inc_rec), outgoing_required=fmt(out_req),
                         outgoing_recommended=fmt(out_rec), parent_page_id=parent, child_page_ids='; '.join(children),
                         related_page_ids='; '.join(related), ranking_protected=rp, orphan_status=status,
                         launch_linking_requirement=launch,
                         notes=('Stage 15 keyword owner. ' if pg['registry'] else 'Owns no Stage 15 keyword. ') + pg['notes']))
for pid in ['TPL-HEADER', 'TPL-FOOTER']:
    oc = out[pid]
    req_rows.append(dict(page_id=pid, page_type='SITE_TEMPLATE', business_area='Global', current_or_proposed='TEMPLATE', incoming_required='0',
                         incoming_recommended='0', outgoing_required=f"{len([r for r in oc if r['priority'] == 'REQUIRED'])}: " + '; '.join(r['target_page_id'] for r in oc if r['priority'] == 'REQUIRED'),
                         outgoing_recommended='; '.join(r['target_page_id'] for r in oc if r['priority'] in ('RECOMMENDED', 'OPTIONAL')),
                         parent_page_id='', child_page_ids='', related_page_ids='', ranking_protected='NO',
                         orphan_status='NOT_APPLICABLE (site template, not a page)',
                         launch_linking_requirement='Global links are counted as structural only; never as the only support for an important page.',
                         notes='Link source only.'))
write('architecture/16_page_link_requirements.csv', ['page_id', 'page_type', 'business_area', 'current_or_proposed', 'incoming_required',
      'incoming_recommended', 'outgoing_required', 'outgoing_recommended', 'parent_page_id', 'child_page_ids', 'related_page_ids',
      'ranking_protected', 'orphan_status', 'launch_linking_requirement', 'notes'], req_rows)
write('architecture/16_orphan_and_connectivity.csv', ['page_id', 'page_type', 'current_or_proposed', 'incoming_link_count',
      'contextual_incoming_count', 'structural_incoming_count', 'outgoing_link_count', 'status', 'risk', 'required_fix', 'notes'], conn)

# ---------------------------------------------------------------- anchor strategy
AVOID = {
    'EDU-LG-00': "'lab-grown diamonds' / 'lab diamonds' as bare anchors (CL-001 head terms held for the conditional commercial hub COM-LG-HUB); CVD/HPHT method phrases as section anchors",
    'EDU-LG-01': "'do lab-grown diamonds look real' (EDU-LG-08); 'do lab grown diamonds test real' (EDU-LG-09); 'lab-grown vs natural' (EDU-LG-02)",
    'EDU-LG-02': "'are lab-grown diamonds real' (EDU-LG-01); 'lab grown diamonds' head term; price/resale phrases (EDU-LG-05)",
    'EDU-LG-03': "'cvd/hpht diamond tester' (excluded transactional query); 'lab grown diamonds' head term; the same exact HPHT/CVD phrase repeated from many pages",
    'EDU-LG-05': "'are lab grown diamonds worth it' (interim owner EDU-LG-02 until EDU-LG-06 exists); dated price claims ('prices in 2026')",
    'EDU-LG-07': "'conflict-free diamonds' (EDU-NAT-02, conditional)",
    'EDU-LG-08': "'are lab-grown diamonds real' (EDU-LG-01)",
    'EDU-LG-09': "'cvd/hpht diamond tester', 'buy a diamond tester' or any tester-shopping phrase (not HOD's business, Stage 12 D-16)",
    'EDU-LG-10': "'how to choose a lab-grown diamond engagement ring online' (deferred EDU-RJG-04 boundary); 'lab-grown engagement rings' (deferred commercial landing)",
    'EDU-NAT-00': "'natural diamonds' (commercial head term, deferred natural hub); 'buy natural diamonds'",
    'EDU-4C-00': "'diamond clarity grading scale' (EDU-4C-01); 'lab-grown 4Cs' as if a separate page",
    'EDU-4C-01': "'grading system for diamonds' / 'diamond grading chart' (EDU-4C-00)",
    'EDU-4C-06': "shape names such as 'emerald cut' or 'asscher cut' (EDU-SHP-00)",
    'EDU-SHP-00': "cut-grade phrases such as 'best cut' (EDU-4C-06); 'oval engagement rings' or other per-shape shopping phrases (deferred); 'marquise oval diamond' (PDP query)",
    'EDU-CERT-00': "'GIA vs IGI' (EDU-CERT-01); 'IGI report explained' (deferred IGI-only page)",
    'EDU-CERT-01': "'lab-grown diamond certification' / 'diamond certification' (EDU-CERT-00)",
    'EDU-MET-00': "'14k vs 18k' (EDU-MET-01)",
    'EDU-MET-01': "'best metal for rings' / hypoallergenic phrases (EDU-MET-00); 'shop 14k gold rings'",
    'EDU-RJG-01': "'side stones engagement rings' and other style shopping phrases (commercial subcategories)",
    'EDU-RJG-02': "'our resizing policy' (FAQ owns HOD policy)",
    'EDU-GEN-01': "'types of diamonds' (conditional EDU-GEN-02); 'how are diamonds formed' (EDU-NAT-00)",
    'COM-ER-SIDESTONE': "the '/by-desgin/' grouping label; 'ring settings' / 'types of settings' (EDU-RJG-01)",
    'COM-PDP-OVAL-FLORAL': "'marquise oval diamond' from Education pages; 'oval engagement rings' (shape landing pages deferred)",
    'COM-ER': "'lab-grown diamond engagement rings' on both homepage and category (OV-13); 'lab-grown diamonds' (COM-LG-HUB)",
    'COM-LG-HUB': "Education-style anchors ('what are lab-grown diamonds')",
    'EXIST-BLOG-ER-ONLINE': "'how to choose a lab-grown diamond' (EDU-LG-10)",
}
TYPE_GUIDE = {
    'EXACT_MATCH_ALLOWED': 'At most once per source page, in body copy, from a parent hub or one closely related page. Never in templates, nav or footers.',
    'PARTIAL_MATCH': 'Contextual body copy; vary wording between pages.',
    'DESCRIPTIVE': 'Default for contextual links: describes what the reader gets on the target.',
    'NATURAL_LANGUAGE': 'Question- or sentence-style anchor for FAQ, comparison and Blog links.',
    'BRANDED': 'Brand/possessive anchors for commercial, bespoke and craft links.',
    'NAVIGATIONAL': 'Nav, breadcrumb, hub lists and template UI labels; short page labels, never keyword strings.',
}
anc = []
for pid in PAGES:
    if is_template(pid):
        continue
    rs = [r for r in inc[pid] if r['source_page_id'] != pid]
    reg = REG.get(pid)
    topic = (reg['primary_searcher_need'] if reg else PAGES[pid]['page_type'] + ': ' + PAGES[pid]['area'])
    if not reg:
        topic = 'No keyword ownership (Stage 15). ' + topic
    by = collections.defaultdict(list)
    for r in rs:
        by[r['anchor_type']].append(r)
    if not by:
        continue
    for at in ['EXACT_MATCH_ALLOWED', 'PARTIAL_MATCH', 'DESCRIPTIVE', 'NATURAL_LANGUAGE', 'BRANDED', 'NAVIGATIONAL']:
        if at not in by:
            continue
        anchors = []
        for r in by[at]:
            if r['recommended_anchor'] not in anchors:
                anchors.append(r['recommended_anchor'])
        srcs = sorted({r['source_page_id'] for r in by[at]})
        anc.append(dict(target_page_id=pid, target_page_type=PAGES[pid]['page_type'], primary_topic=topic, anchor_type=at,
                        recommended_anchor=' | '.join(anchors[:6]),
                        usage_guidance=f"{TYPE_GUIDE[at]} Used from: {'; '.join(srcs)}.",
                        avoid_anchor=AVOID.get(pid, 'Any keyword phrase owned by another page in Stage 15; identical wording repeated from many pages.'),
                        reason=('Reinforces the Stage 15 owner without assigning new keywords.' if reg else 'Page owns no Stage 15 keyword; anchors describe it without targeting keywords.')
                        + (' Protected ranking URL: vary anchors; no sitewide exact match.' if pid in PROT_PAGE else '')))
write('architecture/16_anchor_strategy.csv', ['target_page_id', 'target_page_type', 'primary_topic', 'anchor_type', 'recommended_anchor',
      'usage_guidance', 'avoid_anchor', 'reason'], anc)

print(f'links={len(rows)} pages={len(req_rows)} connectivity={len(conn)} anchors={len(anc)}')
print(collections.Counter(r['priority'] for r in rows))
print(collections.Counter(r['link_type'] for r in rows))
print(collections.Counter(c['status'] for c in conn))
for c in conn:
    if 'BELOW' in c['notes'] and c['current_or_proposed'] not in ('CONDITIONAL', 'EXISTING_CONDITIONAL'):
        print('BELOW BAR:', c['page_id'], c['notes'][-120:])
