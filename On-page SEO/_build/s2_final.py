# -*- coding: utf-8 -*-
"""Step 2A/2B — resolved decisions (2026-10-10). Authoritative source for the final disposition of OD-01…OD-19.
Everything here is a RECOMMENDATION/SPECIFICATION under the user's delegation of 2026-10-10; nothing is implemented.
Volumes/KD/intent labels are looked up from existing project evidence (QA/_build/evidence/kwlookup.json) — no new research, no paid calls."""
import json, re, os

DEC_DATE = "2026-10-10"
_KW = json.load(open("/Users/manavdesai/Desktop/HOD SEO/QA/_build/evidence/kwlookup.json"))


_DB = None


def _db():
    global _DB
    if _DB is None:
        import csv
        _DB = {}
        for r in csv.DictReader(open("/Users/manavdesai/Desktop/HOD SEO/Keywords/content SEO/dataforseo/processed/07_hod_master_keyword_database.csv", encoding="utf-8-sig")):
            _DB[r["keyword"].lower()] = r
    return _DB


def kwi(k):
    """-> (volume_int|None, kd_str, intent_str) from existing project data (kwlookup.json, then the master keyword DB)."""
    x = _KW.get(k.lower())
    if x and x.get("vol") is not None:
        return x.get("vol"), str(x.get("kd", "")), x.get("intent", "")
    r = _db().get(k.lower())
    if r and r.get("search_volume"):
        try:
            return int(float(r["search_volume"])), str(r.get("keyword_difficulty", "")), r.get("intent", "")
        except Exception:
            pass
    return None, "", ""


def fmt(k):
    v, kd, it = kwi(k)
    if v is None:
        return "%s (volume not measured in project datasets)" % k
    return "%s (%s/mo; KD %s; DFS %s)" % (k, format(int(v), ","), kd if kd != "" else "n/a", it or "n/a")


# ------------------------------------------------------------------------------------------------------------
# Dispositions of the 19 decisions
# ------------------------------------------------------------------------------------------------------------
DISP = {
 "OD-01": "ADOPTED", "OD-02": "ADOPTED — NO SEPARATE HUB NOW; HOD FACT PENDING", "OD-03": "ADOPTED", "OD-04": "ADOPTED",
 "OD-05": "ADOPTED (CONFIRMED PROJECT RULE)", "OD-06": "ADOPTED", "OD-07": "ADOPTED", "OD-08": "PARTLY ADOPTED — HOD INPUT PENDING",
 "OD-09": "ADOPTED — HOD CONTACT FACTS PENDING", "OD-10": "ADOPTED", "OD-11": "ADOPTED", "OD-12": "ADOPTED", "OD-13": "ADOPTED",
 "OD-14": "ADOPTED (KEEP; REVIEW DEFERRED)", "OD-15": "ADOPTED — GSC BASELINE BEFORE LIVE CHANGE", "OD-16": "ADOPTED (REVERSIBLE DEFAULTS)",
 "OD-17": "INTAKE PREPARED — ENGINEERING INPUT PENDING (NON-BLOCKING FOR SPEC)", "OD-18": "REQUEST PREPARED — GSC DATA PENDING (BLOCKS EQUITY-PAGE EDITS ONLY)",
 "OD-19": "BUNDLED WITH OD-08 — HOD INPUT PENDING; NEUTRAL FRAMING ADOPTED",
}
SHORT = {k: v.split(" — ")[0].split(" (")[0] for k, v in DISP.items()}


def dec_ref(ids):
    out = []
    for i in re.findall(r"OD-\d+", ids or ""):
        out.append("%s %s" % (i, SHORT.get(i, "")))
    return "; ".join(dict.fromkeys(out))


# ------------------------------------------------------------------------------------------------------------
# OD-01 / OD-16 — commercial keyword assignments (one primary per URL)
# state: ASSIGNED | ASSIGNED — INVENTORY WATCH | RESERVED — INACTIVE UNTIL POPULATED | NO KEYWORD BY DESIGN |
#        NO KEYWORD — NO MEASURED DEMAND | HELD — AMBIGUOUS | NOT BUILT
# ------------------------------------------------------------------------------------------------------------
A = {}
def a(rid, primary, sec=(), state="ASSIGNED", conf="MEDIUM", why="", boundary="", caveat="", serp="NOT VALIDATED (volume + DFS intent label only)", proxy=False):
    A[rid] = dict(primary=primary, sec=list(sec), state=state, conf=conf, why=why, boundary=boundary, caveat=caveat, serp=serp, proxy=proxy)

a("COM-ER", "engagement ring", ["engagement rings for women", "lab grown diamond engagement rings*", "lab grown diamond rings*"], conf="HIGH",
  why="Broad head term → parent hub (Stage 12 D-03/D-18: category subjects live on category hubs, not the homepage). Only engagement-ring listing with full inventory.",
  boundary="Must not target style heads (child pages), custom/bespoke heads (/bespoke), or informational 'how to choose' queries (Education). * Origin-qualified variants become active only when HOD confirms all catalog stones are lab-grown (F-E1) — no separate URL (D-05).",
  caveat="SERP type not validated; Stage 8 validated only the side-stone head (CATEGORY-dominant), which supports the category-page pattern for this family.")
a("COM-WB", "diamond wedding bands", ["wedding bands for women*"], conf="MEDIUM",
  why="Hub and /wedding-bands/for-her list the identical 7 products (initial-HTML check), so one URL must own the intent. Hub owns it while the range is women's-only; no unmeasured 'wedding bands' head exists in the datasets.",
  boundary="'eternity' and 'anniversary' heads belong to their children; metal-led head 'gold wedding bands' (40,500) is not targeted (catalog is diamond-led; metal is a filter). * 'wedding bands for women' stays on the hub until a distinct men's range exists (F-E3), then moves to /for-her.",
  caveat="Reversible: if men's bands are added, restore /for-her as a distinct indexable child and move 'wedding bands for women' there.")
a("COM-FJ", None, state="NO KEYWORD — NO MEASURED DEMAND", conf="MEDIUM",
  why="'fine jewelry' and 'diamond jewelry' are not measured in project datasets; 'luxury jewelry' (450,000) is dominated by luxury houses and is not a fit. Umbrella page is navigational (routes to earrings/necklaces/bracelets/rings).",
  boundary="Must not repeat child-category heads (earrings, necklace, bracelet).", caveat="Revisit with GSC Queries after cut-over.")
a("COM-FJ-EARRINGS", "diamond earrings", ["earrings"], conf="HIGH", why="Broad product-type head → hub; children own the specific types (stud, hoop/huggie, drop).",
  boundary="Must not lead with 'stud' (child) — stud queries go to /stud-earrings; informational stud/carat questions stay with EDU-4C-07.", caveat="SERP not validated.")
a("COM-FJ-NECKLACES", "diamond necklace", ["necklace"], conf="HIGH", why="Broad head → hub; children own pendant/solitaire/charm/lariat types.",
  boundary="Layering/length questions belong to BC-006 / EDU-RJG-NL.", caveat="SERP not validated.")
a("COM-FJ-BRACELETS", "diamond bracelet", ["bracelet"], conf="HIGH", why="Broad head → hub; 'tennis bracelet' (135,000) belongs to the tennis child.",
  boundary="Hub title must not lead with 'tennis'; 'what is a tennis bracelet' stays Blog (BC-021); sizing → EDU-RJG-BR.", caveat="SERP not validated.")
a("COM-FJ-RINGS", None, ["diamond ring*"], state="HELD — AMBIGUOUS", conf="LOW",
  why="'diamond ring' (110,000) spans engagement, wedding and fashion intent; the page holds 2 products and its only child is empty; Stage 12 marks FJ rings DEFER. No safe single-intent assignment exists without SERP/GSC evidence.",
  boundary="Must not target engagement- or wedding-ring heads or eternity terms (one-home: /wedding-bands/for-her/eternity).",
  caveat="HELD — specific reason: ambiguous head + 2-product inventory. Reversible default: keep descriptive title; revisit with GSC Queries.")
a("COM-CURATED-TBAR", "t bar necklace", state="ASSIGNED — INVENTORY WATCH", conf="MEDIUM",
  why="The 4 T-bar pieces are pendants/necklaces with zero overlap with /pendant-necklace (initial-HTML check), so /t-bar is the only home for the term; no merge (D-14).",
  boundary="Must not target 'diamond pendant necklace' (child owner).", caveat="Curated-collection placement stays deferred; naming typo 'T- BAR' fixed in the visible name only.")
a("COM-ER-STYLES-GROUP", None, state="NO KEYWORD BY DESIGN", conf="HIGH",
  why="Grouping-only segment; identical listing to /engagement-rings (24 = 24 initial-HTML products). Canonical to /engagement-rings; child style URLs preserved.",
  boundary="No keyword may be assigned.", caveat="Redirect is the alternative once breadcrumbs stop linking the group page.")
a("COM-BESPOKE", "custom engagement ring", ["design your own engagement ring", "bespoke engagement ring", "custom jewelry"], conf="MEDIUM",
  why="Calendar boundary notes already reserve the custom heads for COM-BESPOKE; /bespoke is the only service/commission page. Distinct intent from the engagement-rings catalog (user-confirmed default).",
  boundary="BC-001 owns the informational timeline question; BC-024 owns cost; /engagement-rings must not target 'custom' heads.",
  caveat="SERP type not validated (may mix retailer category and service pages).")
# --- subcategories
a("SUB:/engagement-rings/by-design/side-stone-rings", "side stones engagement rings", conf="HIGH", serp="SERP-VALIDATED (Stage 8: TRANSACTIONAL, CATEGORY-dominant)",
  why="Existing Stage 15 owner (COM-ER-SIDESTONE); ratification unchanged.", boundary="PDP /shop/oval-floral-diamond-ring keeps 'oval/marquise' as lead terms.", caveat="Registry URL record must move to /by-design/ once the 301 exists.")
a("SUB:/engagement-rings/by-design/solitare-rings", "solitaire engagement rings for women", ["solitaire engagement ring"], conf="MEDIUM", proxy=True,
  why="Only measured solitaire-ring head; the page itself is not gendered, so the unmodified form is used in title/H1 and the measured phrase is a volume proxy.",
  boundary="Necklace solitaire terms belong to /fine-jewellery/necklaces/solitare.", caveat="Volume is a proxy for the unmodified head (DFS groups variants).")
a("SUB:/engagement-rings/by-design/halo-ring", "halo engagement rings", conf="MEDIUM", why="Specific style head with measured demand; populated (11 products).", boundary="Settings explanation → EDU-RJG-01.")
a("SUB:/engagement-rings/by-design/toi-moi-rings", "toi et moi engagement ring", ["toi et moi ring*"], state="ASSIGNED — INVENTORY WATCH", conf="MEDIUM",
  why="Transactional-labelled variant chosen as primary; 'toi et moi ring' (27,100) is DFS-informational → kept as secondary on the same page (one home) pending SERP evidence.",
  boundary="Necklace page must not use ring-intent 'toi et moi' heads; BC-031 trends post links here.", caveat="1 product only — inventory watch; * secondary needs SERP check (GSC Queries after cut-over).")
a("SUB:/engagement-rings/by-design/pave", None, state="NO KEYWORD — NO MEASURED DEMAND", conf="MEDIUM",
  why="No measured pavé-ring head in project datasets; page stays indexable as a populated style listing (current state), not promoted.", boundary="Settings explanation → EDU-RJG-01.", caveat="D-07 gate #1 unmet → GSC review trigger.")
a("SUB:/engagement-rings/by-design/nature-inspired-rings", None, state="NO KEYWORD — NO MEASURED DEMAND", conf="MEDIUM",
  why="No measured head; 3 products; keep as navigational style listing.", boundary="—", caveat="D-07 gate #1 unmet → GSC review trigger.")
a("SUB:/engagement-rings/by-design/three-stone-rings", "three stone engagement ring", conf="MEDIUM", why="Measured style head; 4 products.", boundary="BC-031 reserves this head for the commercial page.")
a("SUB:/engagement-rings/by-design/bezel-rings", "bezel engagement ring", state="ASSIGNED — INVENTORY WATCH", conf="MEDIUM",
  why="Measured style head (22,200; calendar RESERVED_COMMERCIAL_PAGE); 2 products.", boundary="Settings explanation → EDU-RJG-01.", caveat="Thin inventory — merchandising to add products or GSC review at 90 days.")
a("SUB:/engagement-rings/round-rings", None, ["round engagement rings*"], state="NO KEYWORD — NO MEASURED DEMAND", conf="MEDIUM",
  why="Shape stays a filter (Stage 12 D-08, D-07): empty page, noindex. Shape+ring heads are now measured (round engagement rings 22,200; oval engagement ring 60,500) but SERP type is unvalidated; per-shape landing pages are not created from volume alone.",
  boundary="Shape guide → EDU-SHP-00.", caveat="OPPORTUNITY LOGGED, NOT ADOPTED: re-evaluate shape landings with GSC Queries.")
a("SUB:/wedding-bands/for-her", None, ["wedding bands for women* (held on hub)"], state="NO KEYWORD BY DESIGN", conf="MEDIUM",
  why="Identical product set to the hub (7 = 7) → duplicate; canonical to /wedding-bands, out of sitemap, until a distinct men's range exists.", boundary="—", caveat="Reversible (see COM-WB).")
a("SUB:/wedding-bands/for-her/eternity", "eternity rings for women", ["eternity band*", "eternity ring*"], conf="MEDIUM",
  why="One home for eternity commercial intent (populated, 6 products). Transactional-labelled variant is primary; 'eternity band'/'eternity ring' are DFS-informational and kept here pending SERP evidence.",
  boundary="/fine-jewellery/rings/eternity-rings (empty) must not target eternity terms; 'eternity ring meaning' stays Blog (BC-023).", caveat="* informational-labelled heads: SERP check via GSC Queries.")
a("SUB:/wedding-bands/for-her/anniversay", "anniversary ring", state="ASSIGNED — INVENTORY WATCH", conf="LOW",
  why="Only home with a matching product (1 product); 'anniversary band' (5,400) is DFS-informational.", boundary="Gift lists → BC-018/BC-035.", caveat="Thin inventory + intent may be gift-led; review with GSC.")
a("SUB:/wedding-bands/for-her/nature", None, state="NO KEYWORD — NO MEASURED DEMAND", why="Empty page.")
a("SUB:/wedding-bands/for-her/solid", None, state="NO KEYWORD — NO MEASURED DEMAND", why="Empty page.")
a("SUB:/wedding-bands/for-her/cigar-band", None, state="NO KEYWORD — NO MEASURED DEMAND", why="Empty page.")
a("SUB:/wedding-bands/for-her/pavee", None, state="NO KEYWORD — NO MEASURED DEMAND", why="Empty page; slug typo 'pavee' (URL change = migration).")
a("SUB:/wedding-bands/for-him", None, state="NO KEYWORD — NO MEASURED DEMAND", why="Empty; men's range is an unconfirmed offer (F-E3).")
a("SUB:/wedding-bands/for-him/classic", None, state="NO KEYWORD — NO MEASURED DEMAND", why="Empty; men's range unconfirmed.")
a("SUB:/wedding-bands/for-him/diamonds", None, state="NO KEYWORD — NO MEASURED DEMAND", why="Empty; men's range unconfirmed.")
a("SUB:/wedding-bands/for-him/designer", None, state="NO KEYWORD — NO MEASURED DEMAND", why="Empty; men's range unconfirmed.")
a("SUB:/fine-jewellery/earrings/stud-earrings", "diamond stud earrings", ["stud earrings"], conf="HIGH",
  why="Specific type; strongest earrings child (QA/04 R7, Stage 15 CL-125). Hub keeps the broad head.", boundary="Informational stud/carat questions → EDU-4C-07.")
a("SUB:/fine-jewellery/earrings/hoops-huggies", "huggie earrings", ["diamond hoop earrings"], conf="MEDIUM",
  why="One page serves both types; the higher-volume, lower-competition head is primary and the hoop head is a same-page secondary.", boundary="BC-025 informational.")
a("SUB:/fine-jewellery/earrings/drop-dangle", "diamond drop earrings", ["dangle earrings"], conf="MEDIUM", why="Specific type; populated (8 products).", boundary="BC-025 informational.")
a("SUB:/fine-jewellery/earrings/tennis-earrings", None, state="NO KEYWORD — NO MEASURED DEMAND", why="Empty page; no measured head.")
a("SUB:/fine-jewellery/earrings/personalized-charm", None, ["personalized jewelry (too broad)"], state="NO KEYWORD — NO MEASURED DEMAND", why="Empty; 'personalized jewelry' (60,500) is too broad for an earrings child and personalization is an unconfirmed service (F-E5).")
a("SUB:/fine-jewellery/necklaces/solitare", "diamond solitaire necklace", ["solitaire necklace"], conf="MEDIUM",
  why="Solitaire-qualified heads; product set is disjoint from /pendant-necklace (0 overlap), so each product has one home.", boundary="Ring solitaire heads → /engagement-rings/by-design/solitare-rings.")
a("SUB:/fine-jewellery/necklaces/pendant-necklace", "diamond pendant necklace", ["diamond pendant"], state="ASSIGNED — INVENTORY WATCH", conf="MEDIUM",
  why="Generic pendant heads; 3 products, disjoint from solitaire and T-bar sets.", boundary="'solitaire' qualified terms → solitaire child; T-bar → /t-bar.")
a("SUB:/fine-jewellery/necklaces/charm-necklace", "charm necklace", conf="MEDIUM", why="Measured head (33,100); populated (8 products).")
a("SUB:/fine-jewellery/necklaces/multi-stone", None, state="NO KEYWORD — NO MEASURED DEMAND", why="No measured head; 6 products; navigational listing.", caveat="GSC review trigger.")
a("SUB:/fine-jewellery/necklaces/lariat-necklace", "lariat necklace", state="ASSIGNED — INVENTORY WATCH", conf="MEDIUM", why="Measured head (18,100); 1 product.", caveat="Thin inventory — merchandising/GSC review.")
a("SUB:/fine-jewellery/necklaces/toi-et-moi", None, state="NO KEYWORD — NO MEASURED DEMAND", conf="MEDIUM",
  why="'toi et moi necklace' is not measured; ring-intent 'toi et moi' heads belong to the ring child (disjoint product sets, 1 vs 3). Keeps 'necklace' in title/H1.", boundary="Must not use ring-intent toi et moi heads.")
a("SUB:/fine-jewellery/necklaces/tennis-necklace", "tennis necklace", state="RESERVED — INACTIVE UNTIL POPULATED", conf="MEDIUM", why="Measured head (33,100) but 0 products: noindex now; assignment activates on population.", caveat="Merchandising opportunity — F-E5 (do they make it?).")
a("SUB:/fine-jewellery/necklaces/initials", "initial necklace", state="RESERVED — INACTIVE UNTIL POPULATED", conf="LOW", why="Measured head (40,500) but 0 products and personalization is an unconfirmed service (F-E5).")
a("SUB:/fine-jewellery/bracelet/tennis", "tennis bracelet", ["diamond tennis bracelet"], conf="MEDIUM",
  why="Child owns the commercial head; hub keeps 'diamond bracelet'; 8 products.", boundary="BC-021 informational; EDU-RJG-BR sizing.", caveat="Largest commercial head in the project (135,000); SERP not validated.")
a("SUB:/fine-jewellery/bracelet/bangles", None, ["gold bangles"], state="HELD — TAXONOMY CONFIRMATION", conf="LOW",
  why="Label/contents mismatch: the category is named 'Bangles' but its 2 products are both named link bracelets (Celeste Pavé Circle Diamond Link Bracelet; Lattice Rose Gold Geometric Diamond Link Bracelet); no product in the catalog is described as a bangle (the only 'bangle' mentions are styling suggestions inside two bracelet descriptions). The only measured bangle head, 'gold bangles' (27,100; DFS transactional), is metal-led and needs actual bangle products, so it is not adopted. The product sets of /bangles (2), /chain-link (1) and /tennis (8) are disjoint (crawl 2026-10-09).",
  boundary="Must not use 'bangle', 'cuff' or 'bangle bracelet' in title, H1, intro or anchors while the contents are link bracelets; must not duplicate /chain-link ('chain bracelet').",
  caveat="HELD until HOD answers F-E7 (are bangles sold or planned; should 'Bangles' be kept, renamed or folded into 'Chain & Link'). Reversible default: interim copy scoped to link bracelets. If real bangles are added, re-run the D-07 gate and consider 'gold bangles'/'diamond bangle' with GSC Queries.")
a("SUB:/fine-jewellery/bracelet/chain-link", "chain bracelet", state="ASSIGNED — INVENTORY WATCH", conf="LOW",
  why="Measured head (8,100); 1 product (Rosette Five-Flower Bracelet, described as a chain bracelet). No product overlap with /bracelet/bangles (2) or /bracelet/tennis (8) — verified in the 2026-10-09 crawl.",
  boundary="Must not borrow 'bangle' wording from /bracelet/bangles; link-bracelet wording stays on that page until F-E7 is answered.", caveat="Thin inventory — merchandising/GSC review; taxonomy shared with /bangles (F-E7).")
a("SUB:/fine-jewellery/rings/eternity-rings", None, state="NO KEYWORD BY DESIGN", conf="MEDIUM",
  why="One home for eternity intent is /wedding-bands/for-her/eternity; page is empty (noindex).", boundary="If populated with non-bridal pieces it must differentiate (e.g. 'diamond eternity ring' only after SERP/GSC evidence).")
a("SUB:/hiphop/chains", None, state="NO KEYWORD — NO MEASURED DEMAND", why="Empty; Hip Hop range unconfirmed (F-E3).")
a("SUB:/hiphop/chains/cuban-links", "cuban link chain diamond", state="RESERVED — INACTIVE UNTIL POPULATED", conf="LOW", why="Measured (720); empty page; range unconfirmed (F-E3).")
a("SUB:/hiphop/test-subcat", None, state="NO KEYWORD BY DESIGN", why="Test artifact — remove.")
a("COM-LG-HUB", None, ["lab grown diamonds*", "lab diamonds*", "lab created diamonds*", "lab grown diamond engagement rings → /engagement-rings"], state="NOT BUILT", conf="MEDIUM",
  why="No separate commercial hub now (OD-02): (1) the catalog is finished jewelry — a 'lab-grown diamonds' hub would duplicate /shop (every product is lab-grown), failing D-07 distinctness and one-home; (2) the SERP for the head terms is retailer loose-stone/collection pages (Stage 8) that HOD cannot match without loose stones; (3) EDU-LG-00 must stay informational.",
  boundary="Education pillar must not target the head terms; bare anchor 'lab-grown diamonds' reserved for a future hub only.",
  caveat="Reverses if HOD confirms it sells (or will sell) loose lab-grown diamonds (F-E2). Origin-qualified ring heads move to /engagement-rings once F-E1 is confirmed.",
  serp="SERP-VALIDATED for head terms (Stage 8: 'lab grown diamonds' NAVIGATIONAL; 'lab diamonds' TRANSACTIONAL, retailer collection pages)")
# keywords by design (single rows)
for rid in ("NAV-HOME", "COM-SHOP", "COM-COLLECTION", "BRAND-ABOUT", "BRAND-CONTACT", "SUP-FAQ", "SUP-POLICIES-SHIP", "SUP-POLICIES-RET", "SUP-POLICIES-PRIV", "SUP-POLICIES-TERMS", "BLOG-HUB", "EDU-ROOT", "COM-PDP"):
    a(rid, None, state="NO KEYWORD BY DESIGN", conf="HIGH", why="Brand / utility / index / policy / template page (Stage 12 D-18).")

# ------------------------------------------------------------------------------------------------------------
# OD-03 — the 12 Education primary-keyword resolutions (R2). id: (final primary, co-primary/secondary treatment, rationale note)
# ------------------------------------------------------------------------------------------------------------
EDU3 = {
 "EDU-MET-01": ("14k vs 18k gold", "co-primary: 'is 18k gold or 14k gold better' (Stage 17/19) — answered in the first section", "Existing ranking-equity URL: title/H1 change waits for the GSC baseline"),
 "EDU-4C-00": ("4 cs of diamonds", "co-primary: 'diamond grading scale' (Stage 17/19)", "Pillar; depth handed to 4C-01/05/06/07"),
 "EDU-SHP-00": ("diamond shapes", "co-primary: 'diamond shape' (same volume 60,500 — wording variant)", "Single page; no new page"),
 "EDU-RJG-02": ("ring size chart", "'are mens and womens ring sizes the same' (Stage 17/19, 1,000) becomes an H2 answer block, not a co-primary", "Largest volume in the plan; tool optional"),
 "EDU-LG-00": ("what are lab grown diamonds", "co-primary: 'synthetic diamonds' (2,900) via the 'other names' section", "Must not take commercial head terms"),
 "EDU-LG-09": ("how to tell if a diamond is real", "co-primary: 'do lab grown diamonds pass a diamond tester' (720)", "Generic testing intent with lab-grown tester section; boundary with EDU-LG-01/08"),
 "EDU-4C-01": ("diamond clarity chart", "co-primary: 'diamond clarity grading scale' (12,100)", "General scale here; lab-grown clarity-chart queries stay on the pillar (MEDIUM pair)"),
 "EDU-4C-03": ("vvs diamonds", "co-primary: 'v v s diamond' (same volume — spacing variant)", "Title identical either way"),
 "EDU-4C-05": ("diamond color scale", "co-primary: 'color grade diamond'", "—"),
 "EDU-4C-06": ("diamond cut", "co-primary: 'diamond cut grade'", "Cut-grade here; shape queries → EDU-SHP-00"),
 "EDU-4C-07": ("diamond carat size chart", "'is 1 carat diamond good' (320) becomes a section question, not a co-primary", "Informational stud queries land here"),
 "EDU-MET-00": ("white gold vs platinum", "co-primary: 'types of jewelry metals'", "No claim that HOD offers platinum (F-E4)"),
}
# OD-04 — the 8 ownership confirmations. id: (final owner, treatment)
EDU4 = {
 "EDU-RJG-BR": ("EDU-RJG-BR — Education (Ring & Jewelry Guides)", "Sizing reference = Education (Stage 13 §3 'ring sizing…reference'). Owns 'bracelet size chart' only; BC-021 keeps tennis-bracelet meaning/wear.", "Stage 13 §3, tests 1–2; calendar boundary note"),
 "EDU-RJG-NL": ("EDU-RJG-NL — Education (Ring & Jewelry Guides)", "Sizing reference = Education. BC-006 keeps layering/styling.", "Stage 13 §3; D-BC-14 gap note"),
 "EDU-INS": ("EDU-INS — Education (Ring & Jewelry Guides)", "Permanent 'is it worth it / what does it cover' buying question = Education; no personalized financial advice; no HOD insurance/appraisal service claims (F-E5).", "Stage 13 §3 permanent buying guides, tests 1–2"),
 "EDU-WB-GUIDE": ("EDU-WB-GUIDE — Education (Ring & Jewelry Guides)", "Permanent 'how to choose' buying guide = Education; owns the buying decision (metal, width, fit, pairing).", "Stage 13 §3; boundary BC-007/BC-022/EDU-WB-TYPES"),
 "EDU-LG-09": ("EDU-LG-09 — Education (Lab-Grown)", "Co-primary adopted (see OD-03). Testing/identification reference is Education.", "Stage 13 §3 'testing/identification reference'; Stage 14 EDU-LG-09"),
 "EDU-RJG-01": ("EDU-RJG-01 — Education (Ring & Jewelry Guides)", "Targets 'types of diamond settings' (720). 'engagement ring settings' stays off (S18.5 commercial-led CONFLICT); style heads stay on commercial child pages, which this guide links to.", "Stage 19 ownership review carried; S18.5"),
 "EDU-RJG-03": ("EDU-RJG-03 — Education (Ring & Jewelry Guides) — ACTIVATED", "Care is Education (Stage 13 keeps care in Education); no Blog post targets care. Activation condition met (≥2 child guides in the hub). No HOD cleaning/appraisal service claims (F-E5).", "Stage 13 §3; Stage 14 EDU-RJG-03; calendar note"),
 "BLOG-WR-TYPES": ("EDU-WB-TYPES — Education (Ring & Jewelry Guides); calendar ID BLOG-WR-TYPES retained as alias", "Stage 13 §4 tests: shelf-life ✓ (permanent), question ✓ ('types of …' stable query), ownership ✓ (no Blog owner), brand test ✗ → Education; 'if tests disagree Education wins'. One page only: owns the style catalog ('types of wedding rings' 12,100); EDU-WB-GUIDE owns the buying decision; BC-037/007/022/023 stay Blog and link here. Calendar date/slot unchanged.", "Stage 13 §3–4; calendar cannibalization note (merged phrasings)"),
}

# ------------------------------------------------------------------------------------------------------------
# OD-06 / OD-07 — redirect and index-control specification
# ------------------------------------------------------------------------------------------------------------
STYLE_SLUGS = ["solitare-rings", "halo-ring", "toi-moi-rings", "pave", "nature-inspired-rings", "three-stone-rings", "bezel-rings", "side-stone-rings"]
REDIR = []
for s in STYLE_SLUGS:
    REDIR.append(("R-%02d" % (len(REDIR) + 1), "/engagement-rings/by-desgin/" + s, "/engagement-rings/by-design/" + s, "301",
                  "Typo path (404, re-verified 2026-10-10). Target confirmed live 2026-10-10 (200, self-canonical; in the 2026-10-09 sitemap).", "CRITICAL" if s.startswith("side-stone") else "HIGH",
                  "Stage 15 keyword-owner URL" if s.startswith("side-stone") else "Live at the old path per Stage 10; may be indexed — GSC check is non-blocking"))
REDIR.append(("R-%02d" % (len(REDIR) + 1), "/engagement-rings/by-desgin", "/engagement-rings/by-design", "301", "1:1 to the corresponding valid group URL (which itself canonicalises to /engagement-rings).", "LOW", "Old grouping URL"))
GROUP = ("C-01", "/engagement-rings/by-design", "canonical → /engagement-rings; remove from sitemap; stop internal links to the group page (breadcrumbs, nav) ; child pages untouched",
         "Identical 24 = 24 initial-HTML products and the same boilerplate FAQ as /engagement-rings; D-03/P-DEPTH. Redirect remains the alternative once no internal link points here and GSC shows no standalone demand.")
EMPTY = [  # (path, treatment, redirect?, note)
 ("/collection", "noindex,follow; out of sitemap, nav and /llms.txt", "No redirect (empty, no equity; /shop is the all-products listing but a redirect would hide a template defect)", "Revisit if engineering confirms /collection is a retired route → 301 /shop"),
 ("/engagement-rings/round-rings", "noindex,follow; out of sitemap/nav; shape stays a filter (D-08)", "No redirect — shape filter URLs already canonicalise to the parent", "Shape landing pages: opportunity logged, not adopted"),
 ("/wedding-bands/for-him", "noindex,follow; out of sitemap/nav", "No redirect (irrelevant destinations)", "CONDITIONAL on men's range (F-E3)"),
 ("/wedding-bands/for-him/classic", "noindex,follow; out of sitemap/nav", "No redirect", "CONDITIONAL on men's range (F-E3)"),
 ("/wedding-bands/for-him/diamonds", "noindex,follow; out of sitemap/nav", "No redirect", "CONDITIONAL on men's range (F-E3)"),
 ("/wedding-bands/for-him/designer", "noindex,follow; out of sitemap/nav", "No redirect", "CONDITIONAL on men's range (F-E3)"),
 ("/wedding-bands/for-her/nature", "noindex,follow; out of sitemap/nav until populated", "No redirect", "Populate or retire — merchandising"),
 ("/wedding-bands/for-her/solid", "noindex,follow; out of sitemap/nav until populated", "No redirect", "Populate or retire — merchandising"),
 ("/wedding-bands/for-her/cigar-band", "noindex,follow; out of sitemap/nav until populated", "No redirect", "Populate or retire — merchandising"),
 ("/wedding-bands/for-her/pavee", "noindex,follow; out of sitemap/nav until populated", "No redirect", "Slug typo 'pavee' — fix only with a migration plan if populated"),
 ("/fine-jewellery/earrings/tennis-earrings", "noindex,follow; out of sitemap/nav until populated", "No redirect", "Remove the empty tab from the earrings hub"),
 ("/fine-jewellery/earrings/personalized-charm", "noindex,follow; out of sitemap/nav until populated", "No redirect", "Personalization service unconfirmed (F-E5)"),
 ("/fine-jewellery/necklaces/tennis-necklace", "noindex,follow; out of sitemap/nav until populated", "No redirect", "Reserved head 'tennis necklace' (33,100) activates on population"),
 ("/fine-jewellery/necklaces/initials", "noindex,follow; out of sitemap/nav until populated", "No redirect", "Reserved head 'initial necklace' (40,500); personalization unconfirmed (F-E5)"),
 ("/fine-jewellery/rings/eternity-rings", "noindex,follow; out of sitemap/nav until populated", "No redirect (one-home is /wedding-bands/for-her/eternity)", "Do not redirect to a populated page that serves a different (bridal) intent"),
 ("/hiphop/chains", "noindex,follow; out of sitemap/nav", "No redirect (parent /hiphop already 308 → /shop)", "CONDITIONAL on Hip Hop range (F-E3)"),
 ("/hiphop/chains/cuban-links", "noindex,follow; out of sitemap/nav", "No redirect", "CONDITIONAL on Hip Hop range (F-E3)"),
 ("/hiphop/test-subcat", "REMOVE: return 404/410; delete the record; out of sitemap", "No redirect (test artifact has no equity)", "Stage 12 D-13 / P-NO-TEST"),
]
OTHER_PATHS = [
 ("/contact", "Replace the 307-to-modal with a real indexable /contact page (200, self-canonical, in sitemap); /?contact=open canonicalises to /contact", "OD-09; HOD contact facts F-C2; engineering E-12"),
 ("/hiphop", "Keep 308 → /shop (range unconfirmed)", "OD-07; F-E3"),
 ("/shop/marquise-floral-diamond-engagement-ring", "404 today; 301 to nearest equivalent ONLY if the GSC Pages export shows impressions/links; otherwise leave 404/410", "GSC G-01"),
 ("/shop/fine-jewellery-test-product", "Keep 404/410", "—"),
 ("Slug typos (solitare ×2, anniversay, pavee, singular /bracelet, toi-moi vs toi-et-moi)", "NO URL change; fix visible category names to US spelling/correct words only", "OD-05; CLAUDE.md rule 12"),
 ("/blog?page=N", "Self-referencing canonical per distinct page; title 'Blog – Page N'", "OD-12; E-06"),
 ("/shop?page=N and /engagement-rings?page=N", "Self-referencing canonical; add 'Page N' to title/H1 for N>1", "E-06"),
]

# ------------------------------------------------------------------------------------------------------------
# HOD facts (OD-08, OD-19) — single consolidated questionnaire.  tier: 1 = blocks page copy/trust claims now,
# 2 = changes architecture/offer, 3 = completes copy/schema
# ------------------------------------------------------------------------------------------------------------
FACTS = [
 # id, tier, group, fact asked, where it appears today, what we do until answered, what it unblocks
 ("F-A1", 1, "A. Policies", "Shipping: regions served; processing vs transit time (in-stock vs made-to-order); carrier(s); insurance/signature; order tracking (is a tracking link sent by email/SMS? does the account 'Orders' tab show order status?); US duties & taxes; any free-shipping terms; holiday order-by dates.",
  "/shipping (placeholder text), header badge 'Complimentary Insured Shipping', home 'Complimentary Overnight Shipping', every PDP shipping block, FAQ, and the approved BC-001 article ('6–9 days of insured shipping'); /returns has a 'Track My Order' button to /profile?tab=orders (login-gated, not verified) and /shipping mentions a tracking link by email/SMS", "Remove 'overnight/free worldwide' claims; /shipping carries no promises; PDP block links to /shipping", "/shipping copy; shipping details in product listings; the shipping block on every product page; holiday gift guides; whether BC-001 can be published as approved ('insured shipping' wording) or needs a separate content revision (SR-02)"),
 ("F-A2", 1, "A. Policies", "Returns/exchanges: window (days), condition, exclusions (bespoke/made-to-order/engraved), refund method and timing, who pays return shipping, how to start a return.",
  "/returns (no terms), header badge '15-Day Returns', FAQ", "No window stated anywhere; page links to contact", "/returns copy; return details in product listings"),
 ("F-A3", 2, "A. Policies", "Warranty: does one exist? If yes, exact terms and duration. Same for 'Care' guidance HOD wants to stand behind.", "Home badge 'Lifetime Warranty'; every PDP 'Care & Warranty' block", "Remove 'Lifetime Warranty'; PDP block reduced to neutral care text", "Home page trust strip; product page template"),
 ("F-B1", 1, "B. Certification", "Which grading labs (IGI, GIA, other) report on which products? Is a report issued for every diamond piece, only some, or on request? Is it supplied with the order?",
  "Home 'IGI Certified', /bespoke 'Full IGI / GIA certification included', PDP descriptions 'IGI certified GH / VVS', FAQ", "Remove blanket 'IGI/GIA certified' claims; no lab named in titles/descriptions; guides explain labs generically", "Home page, /bespoke, product descriptions and listings, certification guides (statements about HOD stones)"),
 ("F-C1", 1, "C. Company & contact", "Company identity: trading name, founders' names and roles, founding year, locations (Surat workshop? New York office?), whether 'family-run' and 'in the trade since 2014' are accurate.",
  "/about, /faq, /returns, blog bylines ('Akshar korat co founder' vs 'Krish Babriya, Co-founder')", "Remove unverifiable claims; organization-level byline; no Person schema", "/about; company details in search listings; whether named authors can be shown"),
 ("F-C2", 1, "C. Company & contact", "Public contact details: one email, phone/WhatsApp, address to publish; reply-time statement (if any); which enquiry topics are really offered (modal lists Product, Bespoke, B2B Wholesale, Press, General).",
  "Footer, /returns (Admin@ vs info@), enquiry modal", "Use the footer details only; no reply-time promise", "/contact page; contact details in search listings; FAQ"),
 ("F-D1", 1, "D. Bespoke", "What a bespoke commission includes (consultation, CAD sketch/rendering, certification, insured delivery, countries served, reply time) and its steps. The timeline itself is already confirmed.",
  "/bespoke page list: 'Free design consultation — CAD sketch', 'Full IGI/GIA', 'insured delivery to 40+ countries', '4-6 week' (not the confirmed timeline)", "Keep only the confirmed timeline and the page's own enquiry description; remove the other claims", "/bespoke process copy, FAQ and the wording of the bespoke timeline article"),
 ("F-E1", 2, "E. Offer & availability", "Is every diamond in the catalog lab-grown? (PDP spec tables say 'Lab Grown Diamond'.)", "Home page tagline/title, product titles", "Origin stated at product level only; hub titles origin-neutral", "Whether the engagement-rings page can say its diamonds are lab-grown in its title and intro"),
 ("F-E2", 2, "E. Offer & availability", "Does House of Diams sell, or plan to sell, loose diamonds (lab-grown or natural) or natural-diamond jewelry?", "Not offered according to the current catalog; guides discuss natural diamonds educationally only", "No commercial hub; education framing neutral; no claim HOD sells natural/loose stones", "Whether a separate 'Lab-Grown Diamonds' shopping page makes sense"),
 ("F-E3", 2, "E. Offer & availability", "Men's wedding bands and the Hip Hop range: do they exist now or are they planned? When?", "Nav 'For Him', 'Hip Hop' (empty pages, test item)", "noindex + out of nav until populated", "Whether men's wedding band and Hip Hop pages are shown on the site"),
 ("F-E4", 3, "E. Offer & availability", "Metals actually offered: platinum? 14K and 18K options? '18K Gold Vermeil' product (label shows 'Vermil')?", "PDP metal lists (10K/14K), 'Gold Vermil' label, EDU-MET pages", "Education neutral; no metal availability claims", "Metal guides and product material labels"),
 ("F-E5", 3, "E. Offer & availability", "Services: cleaning, appraisal, insurance help, resizing, personalization/engraving, wholesale/B2B enquiries, bridal sets, ready-to-ship inventory?", "Planned articles, the enquiry-form topics, the 'Personalized & Charm' pages", "No service mentioned in copy", "Wording of care and insurance guides; personalized pages; holiday gift guide refresh"),
 ("F-E6", 3, "E. Offer & availability", "Workshop/sourcing statements HOD may publish (e.g. a Surat cutting workshop, manufacturing chain).", "Two planned articles (diamond cutting; where lab-grown diamonds are made)", "Posts held", "Those two articles; the bespoke 'how it is made' copy"),
 ("F-E7", 2, "E. Offer & availability", "Bracelet categories: does House of Diams sell, or plan to sell, bangles (rigid circular bracelets)? Today the 'Bangles' category holds 2 pieces that are named link bracelets. Should that category be kept as 'Bangles', renamed to link bracelets, or folded into 'Chain & Link' (1 piece)? Also confirm the category placement of 'Solara Loop … Link Bracelet' and 'Luminelle Cadence … Bracelet', which are listed under Tennis.",
  "/fine-jewellery/bracelet/bangles (2 link bracelets), /bracelet/chain-link (1 chain bracelet), /bracelet/tennis (8)", "Interim copy scoped to 'link bracelets' with no bangle claim; page copy held; no keyword assigned", "The title, meta description, H1 and intro for the Bangles page; whether the two link-style categories stay separate"),
]

# ------------------------------------------------------------------------------------------------------------
# Engineering inputs (OD-17)
# ------------------------------------------------------------------------------------------------------------
ENG = [
 ("E-01", "Cut-over date and content-freeze/DB-sync window?", "Dating every Class B item; whether copy fixes can go earlier", "All B rows; publishing of the 9 publish-ready packaged posts (BC-001 is held for F-A1)"),
 ("E-02", "Where are page titles, meta descriptions, H1s, category names and article bodies edited — Supabase-backed CMS or in code — and does that store move to AWS?", "Who applies metadata/copy and how", "All metadata/copy rows"),
 ("E-03", "Will every current URL stay identical on AWS (incl. /by-design/ paths, /blog, /education, /shop/<slug>)?", "Whether the redirect map needs extra rows", "Redirect map R-01…R-09; Stage 13 transitional URLs"),
 ("E-04", "Who owns/implements the redirect map; can 1:1 301s preserve query strings and avoid chains?", "R-01…R-09 delivery", "Redirect rows"),
 ("E-05", "Can sitemap.xml and robots/meta-robots be set per page (exclude empty/test pages; noindex,follow; add lastmod)? Can empty categories be auto-excluded at 0 products?", "Index-control rule for 18 pages", "/collection + 17 subcategories; group page C-01"),
 ("E-06", "Does the listing template support self-referencing canonical on ?page=N and 'Page N' in title/H1 (shop, engagement-rings, blog)?", "Pagination spec", "/shop, /engagement-rings, /blog"),
 ("E-07", "Can article templates output BreadcrumbList, an Organization author, and a visible breadcrumb (Blog › Post; Education › Hub › Page)?", "Article schema + byline policy", "All articles (11 live + planned)"),
 ("E-08", "Can the boilerplate FAQPage (35 pages) be removed and the FAQ block made category-specific or optional?", "Schema clean-up", "Category/subcategory/shop pages; /returns"),
 ("E-09", "PDP data model: how are variants/metals represented (default variant price)? Can JSON-LD name/sku/breadcrumb be aligned with the visible page? Image host/URL plan after the Supabase/R2 move?", "PDP schema + image URLs", "184 PDPs; Product/OG image fields"),
 ("E-10", "How is USD pricing/schema guaranteed for US users and Googlebot when currency cookies are IP-based?", "Offer currency", "PDP Offer schema"),
 ("E-11", "What replaces the current no-store HTML caching (CDN/cache policy)?", "CWV/TTFB baseline comparison", "Sitewide Class C"),
 ("E-12", "Can a real /contact page be added and /?contact=open canonicalised to it? Can header/footer Contact link to it?", "OD-09 implementation", "/contact; nav"),
 ("E-13", "Can internal links be repointed: PDP breadcrumbs 'By Design' → /engagement-rings; header menu empty children removed; Education index listing the transitional articles?", "Group-page canonical and nav clean-up", "C-01; header menu; /education"),
]

# ------------------------------------------------------------------------------------------------------------
# GSC data request (OD-18)
# ------------------------------------------------------------------------------------------------------------
GSC = [
 ("G-01", "Pages report — clicks, impressions, CTR, position; 16 months; Web; all countries and United States", "Baseline for every ranking-equity edit; /by-desgin/* and /shop/marquise-floral-* legacy URLs; thin-inventory review",
  "EDU-LG-03, EDU-LG-02, EDU-LG-10, EDU-MET-01, COM-PDP-OVAL-FLORAL, LEG-marquise-floral…"),
 ("G-02", "Queries report and Page×Query export for the URLs in G-01 plus /blog, /education, /faq, /engagement-rings, /shop, home and the 23 live subcategories", "Confirms (or overturns) the volume-only keyword assignments; informational-labelled heads (toi et moi, eternity); shape-landing opportunity", "OD-01/OD-16 reviews"),
 ("G-03", "Page indexing report (indexed vs excluded + reasons), incl. URL inspection of the 8 /by-desgin/ URLs and the 18 empty pages", "Whether legacy/empty URLs are indexed", "Redirect and index-control rows"),
 ("G-04", "Sitemaps report (submitted vs indexed)", "Sitemap exclusion verification baseline", "Index-control rows"),
 ("G-05", "Core Web Vitals report + PageSpeed/CrUX for 10 template URLs (home, category, subcategory, 2 PDPs, article, /bespoke, /shipping, /faq, /blog)", "Pre-cut-over performance baseline", "Class C verification"),
 ("G-06", "Property settings: 'Search generative AI' option and property type (domain vs URL-prefix)", "Confirms the property is not excluding AI surfaces", "Measurement"),
]
