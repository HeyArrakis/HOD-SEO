"""Commercial category hubs, subcategories, curated collections, legacy/redirect URLs, PDP rows."""
import re, json, collections
import lib_research as L
from mm_core import *
import mm_helpers as H
from mm_live import base_row, finish, kwc, link_gap_text, SRC_COMMON, D19

SRC_CAT = SRC_COMMON + "; architecture/12_ia_decision_log.md D-03/D-04/D-07/D-13/D-14; blog_keyword_research.csv (RESERVED_COMMERCIAL_PAGE candidates)"


def nprod(path):
    r = cr(path)
    if not r or "internal_links" not in r:
        return None
    n = len([l for l in r["internal_links"] if l.startswith("/shop/")])
    return n


def prod_txt(path):
    n = nprod(path)
    if n is None:
        return UNK
    if n == 0:
        return "0 product links in initial HTML (page text shows '0 pieces' where checked)"
    if n >= 24:
        return "≥24 (listing paginated 24 per page)"
    return str(n)


# ------------------------------------------------------------------ hubs
HUBS = [
    dict(path="/engagement-rings", pid="COM-ER", name="Engagement Rings (category hub)", ptype="CATEGORY_HUB", cluster="Engagement Rings (commercial)",
         cands=("engagement ring", "engagement rings for women", "lab grown diamond engagement rings"),
         conflict="REVIEW — D-19 gap; 'lab grown diamond engagement rings' (90,500) is an origin × type head that Stage 12 D-05 defers as a facet/landing page and that borders the CL-001 commercial lab-grown hub. Needs an explicit ownership decision (COM-ER vs COM-LG-HUB).",
         cannib="MEDIUM — homepage title overlap (OV-13); /engagement-rings/by-design group page duplicates the hub listing (identical 61-piece grid and boilerplate FAQ).",
         title="Diamond Engagement Rings: Halo, Solitaire & More | House of Diams",
         meta="Shop diamond engagement rings in halo, solitaire, pavé, three-stone, bezel and side-stone styles. Lab-grown diamonds with free insured worldwide delivery; bespoke available.",
         h1="Diamond Engagement Rings",
         content="Page is a product grid + generic 'Engagement Rings FAQ' (sitewide boilerplate, e.g. 'How is House of Diams different…'). Add unique intro (2–3 short paragraphs: styles, how to choose, lab-grown positioning) with required links to the 4Cs, shapes, ring-size and side-stone pages (Stage 16 REQUIRED). Remove duplicated boilerplate FAQ or make it category-specific. Resolve duplicate grouping page /engagement-rings/by-design (see its row).",
         action="OPTIMIZE", prio="HIGH", role="Commercial (category hub)", intent="TRANSACTIONAL / COMMERCIAL (DataForSEO label; SERP not validated for these heads)", edu="EDU-SHP-00; EDU-4C-00; EDU-RJG-02; EDU-LG-10; EDU-LG-02"),
    dict(path="/wedding-bands", pid="COM-WB", name="Wedding Bands (category hub)", ptype="CATEGORY_HUB", cluster="Wedding Bands (commercial)",
         cands=("wedding bands for women", "gold wedding bands", "eternity band"),
         conflict="REVIEW — D-19 gap. Calendar BLOG-WR-TYPES / EDU-WB-GUIDE reference COM-WB as owner of commercial heads ('matching wedding band' 6,600, curved/contour/ring enhancer); no Stage 15 mapping exists.",
         cannib="LOW–MEDIUM — informational wedding-band content (BC-036, BC-037, BC-007, BLOG-WR-TYPES, EDU-WB-GUIDE) must stay out of this URL.",
         title="Diamond Wedding Bands for Her: Eternity, Pavé & Solid | House of Diams",
         meta="Shop diamond wedding bands for her, including eternity, anniversary, pavé and solid styles, with free insured worldwide delivery.",
         h1="Diamond Wedding Bands",
         content="Only 7 products are linked; 'for him' branch is empty. Add unique intro + links to the metals guides (EDU-MET-00/01) and ring-size guide (Stage 16 REQUIRED/RECOMMENDED). Do not publish a men's-band proposition in metadata until the 'for him' range is populated.",
         action="OPTIMIZE", prio="HIGH", role="Commercial (category hub)", intent="TRANSACTIONAL / COMMERCIAL (DFS label)", edu="EDU-MET-00; EDU-MET-01; EDU-RJG-02"),
    dict(path="/fine-jewellery", pid="COM-FJ", name="Fine Jewellery (umbrella hub)", ptype="CATEGORY_HUB (umbrella)", cluster="Fine Jewellery (commercial)",
         cands=("fine jewelry", "diamond jewelry", "luxury jewelry"),
         conflict="REVIEW — label/spelling open (Stage 12 D-15): 'fine jewelry' is not measured in any project dataset; 'fine jewelry retailers/brands' (12,100/9,900) are commercial-investigation/brand queries, not a category head.",
         cannib="LOW",
         title="Fine Diamond Jewellery: Earrings, Necklaces & Bracelets | House of Diams",
         meta="Explore House of Diams fine jewellery: diamond earrings, necklaces, pendants and bracelets crafted in Surat, with free insured worldwide delivery.",
         h1="Fine Diamond Jewellery",
         content="Umbrella page: should route to Earrings / Necklaces & Pendants / Bracelets (Stage 16 REQUIRED outgoing) and the 4Cs guide. Currently a product grid with boilerplate FAQ. Measure 'fine jewelry' demand (D-19) before settling label and slug spelling (jewelry vs jewellery).",
         action="OPTIMIZE", prio="MEDIUM", role="Commercial (umbrella hub)", intent="COMMERCIAL / navigational", edu="EDU-4C-00"),
    dict(path="/fine-jewellery/earrings", pid="COM-FJ-EARRINGS", name="Earrings (category)", ptype="CATEGORY", cluster="Fine Jewellery > Earrings",
         cands=("diamond earrings", "diamond stud earrings", "earrings"),
         conflict="REVIEW — D-19 gap; BC-025 'different types of earrings' (blog) shares topic words — boundary: BC-025 informational, this URL transactional.",
         cannib="MEDIUM — sub-pages /stud-earrings, /hoops-huggies, /drop-dangle each have a stronger single-type head ('stud earrings' 60,500; 'diamond stud earrings' 49,500) than the hub; hub vs child split must be set by ownership decision.",
         title="Diamond Earrings: Studs, Hoops, Huggies & Drops | House of Diams",
         meta="Shop diamond earrings: stud, hoop, huggie and drop styles in 10K and 14K gold, with free insured worldwide delivery.",
         h1="Diamond Earrings",
         content="Product grid (24 per page, 5 child types listed as tabs) + boilerplate FAQ. Add short buying guidance with links to the 4Cs and metals pages (Stage 16 recommended) and to BC-025 when live. 'Tennis' and 'Personalized & Charm' child tabs are empty.",
         action="OPTIMIZE", prio="HIGH", role="Commercial (category)", intent="TRANSACTIONAL (DFS label)", edu="EDU-MET-00; EDU-4C-00"),
    dict(path="/fine-jewellery/necklaces", pid="COM-FJ-NECKLACES", name="Necklaces & Pendants (category)", ptype="CATEGORY", cluster="Fine Jewellery > Necklaces & Pendants",
         cands=("diamond necklace", "diamond pendant necklace", "necklace"),
         conflict="REVIEW — D-19 gap; BC-006 'necklace layering' and the planned EDU-RJG-NL 'necklace length chart' are informational siblings (boundary).",
         cannib="MEDIUM — eight child type pages plus /t-bar overlap the hub (OV-16 T-Bar vs pendant necklaces).",
         title="Diamond Necklaces & Pendants | House of Diams",
         meta="Shop diamond necklaces and pendants: solitaire, toi et moi, multi-stone, charm and lariat styles, with free insured worldwide delivery.",
         h1="Diamond Necklaces & Pendants",
         content="Add unique intro + link to the planned necklace-length chart (EDU-RJG-NL) and BC-006 when live. Hub currently lists 8 child types; 2 are empty (tennis necklace, initials).",
         action="OPTIMIZE", prio="HIGH", role="Commercial (category)", intent="TRANSACTIONAL (DFS label)", edu="EDU-4C-00; EDU-RJG-NL (planned)"),
    dict(path="/fine-jewellery/bracelet", pid="COM-FJ-BRACELETS", name="Bracelets (category)", ptype="CATEGORY", cluster="Fine Jewellery > Bracelets",
         cands=("diamond bracelet", "diamond tennis bracelet", "tennis bracelet"),
         conflict="REVIEW — D-19 gap; tennis-bracelet heads (135,000 / 90,500) map more naturally to the /bracelet/tennis child; BC-021 'what is a tennis bracelet' (3,600) is informational.",
         cannib="MEDIUM — hub vs /bracelet/tennis for 'tennis bracelet' intent.",
         title="Diamond Bracelets: Tennis, Bangle & Chain | House of Diams",
         meta="Shop diamond bracelets: tennis, bangle and chain-and-link designs in 10K gold, with free insured worldwide delivery.",
         h1="Diamond Bracelets",
         content="11 products linked. Singular 'bracelet' slug (D-15 related). Add unique intro, bracelet-size link (planned EDU-RJG-BR 'bracelet size chart') and BC-021 link when live.",
         action="OPTIMIZE", prio="MEDIUM", role="Commercial (category)", intent="TRANSACTIONAL (DFS label)", edu="EDU-4C-00; EDU-RJG-BR (planned)"),
    dict(path="/fine-jewellery/rings", pid="COM-FJ-RINGS", name="Fine Jewellery > Rings (non-bridal)", ptype="CATEGORY (conditional)", cluster="Fine Jewellery > Rings",
         cands=("eternity ring", "anniversary ring", "diamond ring"),
         conflict="REVIEW — Stage 12: 'INSUFFICIENT EVIDENCE — DEFER'. Scope overlaps /engagement-rings and /wedding-bands (e.g. eternity/anniversary bands).",
         cannib="MEDIUM — overlaps COM-WB (eternity/anniversary) and COM-ER; one-home principle (P-ONE-HOME).",
         title="No change recommended until scope decision", meta="—", h1="—",
         content="Only 2 products linked; child 'eternity-rings' is empty. Decide scope (non-bridal fashion rings?) or fold into existing categories; until then treat as non-indexable candidate.",
         action="REVIEW", prio="MEDIUM", role="Commercial (conditional)", intent="TRANSACTIONAL (DFS label)", edu="—"),
    dict(path="/t-bar", pid="COM-CURATED-TBAR", name="T-Bar (curated collection)", ptype="CURATED_COLLECTION", cluster="Necklaces & Pendants (conceptual)",
         cands=("t bar necklace",),
         conflict="REVIEW — Stage 12 D-14: placement deferred (OV-16 overlap with pendant necklaces).",
         cannib="MEDIUM — overlaps /fine-jewellery/necklaces/pendant-necklace; 4 PDPs only.",
         title="T-Bar Necklaces & Pendants | House of Diams",
         meta="Shop T-bar diamond necklaces and pendants — sculptural knot and linear designs in gold, with free insured worldwide delivery.",
         h1="T-Bar Necklaces",
         content="Title/H1 currently 'T- BAR' (stray space, no descriptor); meta 'Browse T- BAR from the live catalog.' Decide whether T-bar is a curated collection or a necklace subtype before investing in copy (D-14).",
         action="REVIEW", prio="MEDIUM", role="Commercial (curated collection)", intent="TRANSACTIONAL (DFS label; 2,400/mo)", edu="—"),
]


def hub_rows():
    rows = []
    for h in HUBS:
        p = h["path"]
        r = base_row(p, "COMMERCIAL CATEGORY", h["pid"], h["name"], h["ptype"], h["cluster"], h["role"])
        r["Primary Keyword"] = "NO RATIFIED PRIMARY (D-19 data gap). Candidate head-term evidence from existing datasets (NOT ownership): " + kwc(*h["cands"])
        r["Secondary Keywords"] = "—"
        r["Related/Semantic Concepts"] = "child subcategories; metals; diamond shapes; 4Cs; lab-grown positioning"
        r["Search Intent"] = h["intent"]
        r["Keyword Owner"] = f"{h['pid']} — no Stage 15 keyword"
        r["Existing Keyword Ownership Conflict?"] = h["conflict"]
        r["Cannibalization Risk"] = h["cannib"]
        r["Recommended SEO Title"] = h["title"]; r["Recommended Meta Description"] = h["meta"]; r["Recommended H1"] = h["h1"]
        r["Recommended Content/Section Changes"] = h["content"] + f" Products shown: {prod_txt(p)}."
        c = cr(p)
        r["Recommended Image/Alt-Text Changes"] = f"Product-card alt text = product name + key attribute. Initial HTML: {c.get('img_count','?')} <img>, {c.get('img_no_alt','?')} without alt (incl. UI icons — VERIFY)." if c and 'img_count' in c else UNK
        r["Recommended Internal Links IN"] = H.link_summary(h["pid"], "in")
        r["Recommended Internal Links OUT"] = H.link_summary(h["pid"], "out") + " || " + link_gap_text(h["pid"], p)
        r["Recommended Anchor Context"] = "Use category/child names; Education links use 16_anchor_strategy descriptive anchors (≤5 Education links per category, Stage 16)."
        r["Internal-Link Priority"] = "HIGH" if h["prio"] == "HIGH" else "MEDIUM"
        r["Recommended Schema"] = "BreadcrumbList (present). Remove reliance on template FAQPage (FAQ rich results deprecated 2026-05-08; boilerplate Q&A repeats across pages). ItemList/CollectionPage optional, no search feature."
        r["Schema Validation/Review Needed?"] = "YES — decide FAQPage keep/remove; validate BreadcrumbList."
        r["AEO Opportunity"] = "LOW (commercial listing). Buying questions are owned by Education pages; link to them instead of duplicating."
        r["Primary Questions to Answer"] = "Which style/type should I choose? (answered by linked Education owners)"
        r["Answer-First Opportunity"] = "Optional 2-sentence category definition above the grid."
        r["PAA/Question Coverage Needed?"] = "NO — Stage 14/15: category pages hold no informational keywords"
        r["GEO/AI Search Opportunity"] = "Clear category definition + attributes (metal, stone origin, certification) helps AI shopping answers; keep consistent with PDP Product schema."
        r["Important Entities"] = "House of Diams; " + h["name"].split(" (")[0] + "; lab-grown diamond; metals (10K gold); " + ("diamond shapes" if "ER" in h["pid"] else "diamond 4Cs")
        r["Entity Clarity Needed?"] = "YES — state stone origin and certification facts once confirmed."
        r["Brand/Expertise/Trust Signal Opportunity"] = "Link to certification guide, returns and bespoke service; show real policy facts."
        r["Recommended Action"] = h["action"]; r["Priority"] = h["prio"]
        r["Implementation Dependency"] = "Commercial keyword ratification (D-19, needs approval for any paid check; existing datasets reused here); CMS/code access; business facts"
        r["Status"] = "LIVE — NEEDS OPTIMIZATION" if h["action"] == "OPTIMIZE" else "LIVE — DECISION NEEDED"
        r["Evidence / Source"] = SRC_CAT; r["Notes"] = D19 + " Title/meta drafts are provisional until a keyword is ratified."
        rows.append(finish(r, dict(meta=h["action"] == "OPTIMIZE", h1=h["action"] == "OPTIMIZE", links=1, schema=1, conflict=1, cannib=1),
                           a=["metadata + intro-copy drafts", "link plan", "keyword-ratification memo (reuse existing data)"], b=["schema/template changes"], c=["canonical, indexability, sitemap membership, status, CWV baseline"]))
    return rows


# ------------------------------------------------------------------ subcategories
S = []  # (path, clean name, parent label, pid, cands, ia_status, extra note, rec title, rec h1, rec meta)


def sub(path, clean, parent_pid, cands, ia, note, title, meta, role_conflict=""):
    S.append(dict(path=path, clean=clean, parent=parent_pid, cands=cands, ia=ia, note=note, title=title, meta=meta, conflict=role_conflict))


ERP = "COM-ER"
sub("/engagement-rings/by-design/side-stone-rings", "Side-Stone Engagement Rings", ERP, ("side stones engagement rings",), "INDEXABLE_PERMANENT (only subcategory that passes the D-07 gate: ranking + CATEGORY SERP)",
    "KEYWORD OWNER (Stage 15: COM-ER-SIDESTONE). Moved from /engagement-rings/by-desgin/… (old URL now 404 — see legacy row).",
    "Side-Stone Engagement Rings | House of Diams", "Shop side-stone engagement rings: a center diamond flanked by smaller stones, in 10K gold with free insured worldwide delivery.")
sub("/engagement-rings/by-design/solitare-rings", "Solitaire Engagement Rings", ERP, ("solitaire engagement rings for women",), "INDEXABLE_CONDITIONAL (D-07 gate)", "Slug misspelled ('solitare'); changing it needs a migration plan.",
    "Solitaire Engagement Rings | House of Diams", "Shop solitaire engagement rings: a single center diamond in classic and sculptural settings, with free insured worldwide delivery.")
sub("/engagement-rings/by-design/halo-ring", "Halo Engagement Rings", ERP, ("halo engagement rings",), "INDEXABLE_CONDITIONAL (D-07 gate)", "Singular slug 'halo-ring'.",
    "Halo Engagement Rings | House of Diams", "Shop halo engagement rings: a center diamond framed by a ring of smaller stones, in round, oval, pear and more shapes, with free insured delivery.")
sub("/engagement-rings/by-design/toi-moi-rings", "Toi et Moi Rings", ERP, ("toi et moi ring", "toi et moi engagement ring"), "INDEXABLE_CONDITIONAL (D-07 gate)", "Slug 'toi-moi' differs from the necklace child 'toi-et-moi'. Calendar BC-031 reserves 'toi et moi' style heads for COM-ER style subcategories. DFS labels 'toi et moi ring' informational — SERP must be checked.",
    "Toi et Moi Rings | House of Diams", "Shop toi et moi rings: two diamonds side by side on one band, in modern and classic designs, with free insured worldwide delivery.")
sub("/engagement-rings/by-design/pave", "Pavé Engagement Rings", ERP, (), "INDEXABLE_CONDITIONAL (D-07 gate)", "Page title 'Pavé Rings'; no matching keyword measured. 24+ products.",
    "Pavé Engagement Rings | House of Diams", "Shop pavé engagement rings with diamonds set along the band for continuous sparkle, with free insured worldwide delivery.")
sub("/engagement-rings/by-design/nature-inspired-rings", "Nature-Inspired Engagement Rings", ERP, (), "INDEXABLE_CONDITIONAL (D-07 gate)", "No matching keyword measured; 3 products — thin inventory.",
    "Nature-Inspired Engagement Rings | House of Diams", "Shop nature-inspired engagement rings with vine, leaf and floral designs, with free insured worldwide delivery.")
sub("/engagement-rings/by-design/three-stone-rings", "Three-Stone Engagement Rings", ERP, ("three stone engagement ring",), "INDEXABLE_CONDITIONAL (D-07 gate)", "BC-031 reserves 'three stone engagement ring' for COM-ER style subcategories.",
    "Three-Stone Engagement Rings | House of Diams", "Shop three-stone engagement rings, symbolising past, present and future, in 10K gold with free insured worldwide delivery.")
sub("/engagement-rings/by-design/bezel-rings", "Bezel Engagement Rings", ERP, ("bezel engagement ring",), "INDEXABLE_CONDITIONAL (D-07 gate)", "BC-031 reserves 'bezel' heads for COM-ER style subcategories. 2 products.",
    "Bezel Engagement Rings | House of Diams", "Shop bezel engagement rings with the center diamond held in a smooth metal rim, with free insured worldwide delivery.")
sub("/engagement-rings/round-rings", "Round Engagement Rings (shape landing)", ERP, ("round engagement rings", "round diamond engagement ring"), "NOT IN IA — Stage 12 treats shape as a FILTER_STATE (landing pages deferred, INSUFFICIENT EVIDENCE)", "NEW since Stage 1; 0 products; new URL pattern outside /by-design.",
    "No change — review first", "—", role_conflict="Conflicts with Stage 12 D-05/D-07 (shape landing pages deferred) and D-13 (no empty pages in the indexable IA).")
sub("/wedding-bands/for-her", "Women's Wedding Bands", "COM-WB", ("wedding bands for women",), "INDEXABLE_CONDITIONAL (populated: 7 products)", "L2 gender split is conditional (D-04).",
    "Women's Diamond Wedding Bands | House of Diams", "Shop women's diamond wedding bands: eternity, anniversary, pavé and solid designs, with free insured worldwide delivery.")
sub("/wedding-bands/for-him", "Men's Wedding Bands", "COM-WB", ("mens diamond wedding band",), "INDEXABLE_CONDITIONAL only when populated — currently EMPTY", "Empty branch (Stage 10 also observed empty).",
    "No change — review first", "—")
for nm, slug, cands, nt in (("Nature", "nature", (), "empty"), ("Solid", "solid", (), "empty"), ("Cigar Band", "cigar-band", (), "empty"), ("Eternity", "eternity", ("eternity band", "eternity rings for women"), "6 products"),
                           ("Anniversary", "anniversay", (), "slug misspelled 'anniversay'; 1 product"), ("Pavé", "pavee", (), "slug 'pavee'; empty")):
    sub(f"/wedding-bands/for-her/{slug}", f"{nm} Wedding Bands (women's)", "COM-WB", cands, "INSUFFICIENT EVIDENCE — DEFER (Stage 12 D-04: band styles deferred)", nt,
        f"{nm} Diamond Wedding Bands | House of Diams", f"Shop {nm.lower()} diamond wedding bands for her, with free insured worldwide delivery.")
for nm, slug in (("Classic", "classic"), ("Diamonds", "diamonds"), ("Designer", "designer")):
    sub(f"/wedding-bands/for-him/{slug}", f"{nm} Men's Wedding Bands", "COM-WB", (), "INSUFFICIENT EVIDENCE — DEFER; EMPTY", "empty",
        "No change — review first", "—")
# fine jewellery children
EAR = "COM-FJ-EARRINGS"; NEC = "COM-FJ-NECKLACES"; BRA = "COM-FJ-BRACELETS"
sub("/fine-jewellery/earrings/stud-earrings", "Diamond Stud Earrings", EAR, ("diamond stud earrings", "stud earrings"), "INDEXABLE_CONDITIONAL (D-07 gate; strong inventory ≥24)", "Shows 28 pieces vs 50 on the earrings hub; strongest earrings child; CL-125 'Diamond Stud Earrings' sits as CONDITIONAL_NOT_MAPPED/REVIEW in Stage 15 (informational stud queries → EDU-4C-07 carat guide).",
    "Diamond Stud Earrings | House of Diams", "Shop diamond stud earrings in round, princess, oval, cushion and more shapes, in 10K gold with free insured worldwide delivery.",
    role_conflict="REVIEW — Stage 15 CL-125 (Diamond Stud Earrings) has 1 REVIEW_REQUIRED + 1 CONDITIONAL_NOT_MAPPED keyword; commercial head 'diamond stud earrings' (49,500) is unowned.")
sub("/fine-jewellery/earrings/hoops-huggies", "Hoop & Huggie Earrings", EAR, ("diamond hoop earrings", "huggie earrings"), "INDEXABLE_CONDITIONAL (D-07 gate)", "14 products.",
    "Diamond Hoop & Huggie Earrings | House of Diams", "Shop diamond hoop and huggie earrings, from slim huggies to statement hoops, with free insured worldwide delivery.")
sub("/fine-jewellery/earrings/drop-dangle", "Drop & Dangle Earrings", EAR, ("diamond drop earrings",), "INDEXABLE_CONDITIONAL (D-07 gate)", "8 products.",
    "Diamond Drop & Dangle Earrings | House of Diams", "Shop diamond drop and dangle earrings with movement and sparkle, with free insured worldwide delivery.")
sub("/fine-jewellery/earrings/tennis-earrings", "Tennis Earrings", EAR, (), "NON_INDEXABLE_BY_DEFAULT (Stage 12) — EMPTY", "empty", "No change — review first", "—")
sub("/fine-jewellery/earrings/personalized-charm", "Personalized & Charm Earrings", EAR, ("personalized jewelry",), "NON_INDEXABLE_BY_DEFAULT (Stage 12) — EMPTY", "empty", "No change — review first", "—")
sub("/fine-jewellery/necklaces/solitare", "Diamond Solitaire Necklaces", NEC, ("solitaire necklace", "diamond solitaire necklace"), "INDEXABLE_CONDITIONAL (D-07 gate; ≥24 listed)", "Slug misspelled ('solitare'). Page shows 28 pieces vs 49 on the necklaces hub — confirm the 28 are solitaire-only (distinctness).",
    "Diamond Solitaire Necklaces | House of Diams", "Shop diamond solitaire necklaces and pendants, a single stone on a fine chain, with free insured worldwide delivery.")
sub("/fine-jewellery/necklaces/pendant-necklace", "Diamond Pendant Necklaces", NEC, ("diamond pendant necklace", "diamond pendant"), "INDEXABLE_CONDITIONAL (D-07 gate)", "3 products; overlaps hub and /t-bar (OV-16).",
    "Diamond Pendant Necklaces | House of Diams", "Shop diamond pendant necklaces in bezel, marquise and sculptural designs, with free insured worldwide delivery.")
sub("/fine-jewellery/necklaces/charm-necklace", "Charm Necklaces", NEC, ("charm necklace",), "INDEXABLE_CONDITIONAL (D-07 gate)", "8 products.",
    "Diamond Charm Necklaces | House of Diams", "Shop diamond charm necklaces — small, meaningful pendants on a fine chain — with free insured worldwide delivery.")
sub("/fine-jewellery/necklaces/multi-stone", "Multi-Stone Necklaces", NEC, (), "INDEXABLE_CONDITIONAL (D-07 gate)", "6 products; no keyword measured.",
    "Multi-Stone Diamond Necklaces | House of Diams", "Shop multi-stone diamond necklaces combining several cuts in one design, with free insured worldwide delivery.")
sub("/fine-jewellery/necklaces/lariat-necklace", "Lariat Necklaces", NEC, ("lariat necklace",), "INDEXABLE_CONDITIONAL (D-07 gate) — thin (1 product)", "1 product only; 'lariat necklace' 18,100 was BACKLOG_LOW_PRIORITY in blog research.",
    "Diamond Lariat Necklaces | House of Diams", "Shop diamond lariat necklaces with a drop-through design, with free insured worldwide delivery.")
sub("/fine-jewellery/necklaces/toi-et-moi", "Toi et Moi Necklaces", NEC, (), "INDEXABLE_CONDITIONAL (D-07 gate)", "3 products.",
    "Toi et Moi Diamond Necklaces | House of Diams", "Shop toi et moi diamond necklaces pairing two cuts in one pendant, with free insured worldwide delivery.")
sub("/fine-jewellery/necklaces/tennis-necklace", "Tennis Necklaces", NEC, ("tennis necklace",), "INDEXABLE_CONDITIONAL — EMPTY", "empty; 'tennis necklace' 33,100.", "No change — review first", "—")
sub("/fine-jewellery/necklaces/initials", "Initial Necklaces", NEC, ("initial necklace",), "INDEXABLE_CONDITIONAL — EMPTY", "empty; 'initial necklace' 40,500.", "No change — review first", "—")
sub("/fine-jewellery/bracelet/tennis", "Tennis Bracelets", BRA, ("tennis bracelet", "diamond tennis bracelet"), "INDEXABLE_CONDITIONAL (D-07 gate)", "8 products; highest-demand bracelet head in existing data.",
    "Diamond Tennis Bracelets | House of Diams", "Shop diamond tennis bracelets: a continuous line of brilliant stones in 10K gold, with free insured worldwide delivery.")
sub("/fine-jewellery/bracelet/bangles", "Diamond Bangles", BRA, (), "INDEXABLE_CONDITIONAL — thin (2 products)", "2 products.",
    "Diamond Bangle Bracelets | House of Diams", "Shop diamond bangle bracelets, with free insured worldwide delivery.")
sub("/fine-jewellery/bracelet/chain-link", "Chain & Link Bracelets", BRA, ("chain bracelet",), "INDEXABLE_CONDITIONAL — thin (1 product)", "1 product; title shows lower-case 'chain & Link'.",
    "Diamond Chain & Link Bracelets | House of Diams", "Shop diamond chain and link bracelets, with free insured worldwide delivery.")
sub("/fine-jewellery/rings/eternity-rings", "Eternity Rings (non-bridal)", "COM-FJ-RINGS", ("eternity ring", "eternity band"), "INSUFFICIENT EVIDENCE — DEFER; EMPTY", "empty; overlaps /wedding-bands/for-her/eternity.", "No change — review first", "—",
    role_conflict="CANNIBALIZATION REVIEW REQUIRED — same subject as /wedding-bands/for-her/eternity (6 products). One home needed (P-ONE-HOME).")
# hiphop
sub("/hiphop/chains", "Hip Hop Chains", "COM-HIPHOP", ("cuban link chain diamond",), "INDEXABLE_CONDITIONAL (curated collection) — EMPTY", "empty; /hiphop itself now 308-redirects to /shop.", "No change — review first", "—")
sub("/hiphop/chains/cuban-links", "Cuban Link Chains", "COM-HIPHOP", ("cuban link chain diamond", "cuban link bracelet"), "INDEXABLE_CONDITIONAL — EMPTY", "empty.", "No change — review first", "—")
sub("/hiphop/test-subcat", "TEST SUBCATEGORY (artifact)", "COM-HIPHOP", (), "NON_INDEXABLE (D-13: test artifact)", "Dev/test page in the live sitemap.", "REMOVE FROM INDEX", "—")

SUB_BY_PATH = {s["path"]: s for s in S}


def sub_rows():
    rows = []
    for s in S:
        p = s["path"]
        n = nprod(p)
        empty = (n == 0)
        pid = f"SUB:{p}"
        is_side = p.endswith("/side-stone-rings")
        is_test = "test-subcat" in p
        r = base_row(p, "COMMERCIAL SUBCATEGORY", pid, s["clean"], "SUBCATEGORY", f"{s['parent']} child", "Commercial (subcategory)")
        if is_side:
            r["Primary Keyword"] = "side stones engagement rings (1,000/mo) — Stage 15 OWNER (COM-ER-SIDESTONE; existing ranking pos ~104 in Stage 3 snapshot, NOT GSC)"
            r["Keyword Owner"] = "COM-ER-SIDESTONE — RATIFIED (Stage 15)"
            r["Existing Keyword Ownership Conflict?"] = "NO — but the URL changed (by-desgin → by-design) after Stage 15 recorded it; see legacy-URL row."
            r["Cannibalization Risk"] = "LOW (Stage 15) — now MEDIUM until the legacy URL is redirected and the parent group page is resolved."
        elif is_test:
            r["Primary Keyword"] = "NONE — TEST ARTIFACT"; r["Keyword Owner"] = "none"; r["Existing Keyword Ownership Conflict?"] = "NO"; r["Cannibalization Risk"] = "NONE"
        else:
            cands = kwc(*s["cands"]) if s["cands"] else "none measured in project datasets"
            r["Primary Keyword"] = "NO RATIFIED PRIMARY (D-19 gap). Candidate evidence (NOT ownership): " + cands
            r["Keyword Owner"] = "COM-ER-STYLES / parent hub — no Stage 15 keyword" if s["parent"] == ERP else f"{s['parent']} child — no Stage 15 keyword"
            r["Existing Keyword Ownership Conflict?"] = s["conflict"] or "NO documented conflict (no ownership recorded)"
            r["Cannibalization Risk"] = "CANNIBALIZATION REVIEW REQUIRED — " + s["conflict"] if "CANNIBALIZATION" in s["conflict"] else ("MEDIUM — hub vs child for the same head term; one-home decision pending" if s["cands"] else "LOW")
        r["Secondary Keywords"] = "—"
        r["Related/Semantic Concepts"] = s["clean"].lower() + "; metal options; diamond shapes; lab-grown"
        r["Search Intent"] = "TRANSACTIONAL / COMMERCIAL (side-stone: SERP-validated CATEGORY)" if is_side else ("n/a" if is_test else "TRANSACTIONAL (DFS label; SERP not validated)")
        if is_test:
            r["Recommended SEO Title"] = "(remove from index)"; r["Recommended Meta Description"] = "—"; r["Recommended H1"] = "—"
        elif s["title"].startswith("No change"):
            r["Recommended SEO Title"] = "No change until the page is populated and its indexability is decided"; r["Recommended Meta Description"] = "—"; r["Recommended H1"] = "—"
        else:
            r["Recommended SEO Title"] = s["title"]; r["Recommended Meta Description"] = s["meta"]; r["Recommended H1"] = s["clean"]
        gate = f"D-07 gate check — demand: {'measured (candidate) ' if s['cands'] or is_side else 'NOT measured'}; SERP type: {'CATEGORY (validated)' if is_side else 'NOT validated'}; inventory: {prod_txt(p)}; unique intro copy: absent (template page); stable path: {'NO (typo/segment)' if any(t in p for t in ('solitare','anniversay','pavee','by-design')) else 'yes'}."
        r["Recommended Content/Section Changes"] = (
            ("Remove from the sitemap and set noindex (or delete) — a test page must not be indexable (D-13). " if is_test else
             "EMPTY in the sitemap: noindex + sitemap exclusion until populated (Stage 12 D-13), or populate. " if empty else
             "Add 80–150 words of unique intro copy (what this type is, how to choose, link to the Education owner); replace boilerplate meta. ") + gate + ((" " + s["note"]) if s["note"] not in ("empty",) else ""))
        c = cr(p)
        r["Recommended Image/Alt-Text Changes"] = "Product-card alt text = product name + attribute." if not empty else "n/a (no products)"
        r["Recommended Internal Links IN"] = f"Parent hub ({H.disp(s['parent']) if s['parent'] in H.IDMAP_FIXED else s['parent']}); matching PDPs; relevant blog/education posts (calendar internal_link_targets name parent categories, not subcategories)."
        edu = {"halo": "EDU-RJG-01 (planned)", "solit": "EDU-SHP-00; EDU-4C-00", "stud": "EDU-4C-07 (planned carat guide)", "tennis": "BC-021 (planned) / EDU-RJG-BR (planned)"}
        key = next((k for k in edu if k in p), "")
        r["Recommended Internal Links OUT"] = f"Parent hub; 1–2 Education owners ({edu.get(key, 'EDU-4C-00; EDU-SHP-00 as relevant')}); Stage 16: category pages ≤5 Education links."
        if is_side:
            L16 = H.link_summary("COM-ER-SIDESTONE", "in") + " || OUT " + H.link_summary("COM-ER-SIDESTONE", "out")
            r["Recommended Internal Links IN"] = L16
            r["Recommended Internal Links OUT"] = H.link_summary("COM-ER-SIDESTONE", "out") + " || " + link_gap_text("COM-ER-SIDESTONE", p)
        r["Recommended Anchor Context"] = "Anchor = type name (e.g. 'side-stone engagement rings'); avoid keyword-stuffed repeats."
        r["Internal-Link Priority"] = "HIGH" if is_side else ("LOW" if (empty or is_test) else "MEDIUM")
        r["Recommended Schema"] = "REMOVE nothing now; recommended end-state: BreadcrumbList only (present). Template FAQPage is boilerplate shared across pages — gives no rich result (deprecated 2026-05)." if not is_test else "n/a"
        r["Schema Validation/Review Needed?"] = "LOW — validate BreadcrumbList; decide on boilerplate FAQPage" if not is_test else "NO"
        r["AEO Opportunity"] = "NONE (listing); informational questions belong to Education owners."
        r["Primary Questions to Answer"] = "—"; r["Answer-First Opportunity"] = "—"; r["PAA/Question Coverage Needed?"] = "NO"
        r["GEO/AI Search Opportunity"] = "Low; keep attributes in product data consistent with PDP schema."
        r["Important Entities"] = s["clean"] + "; House of Diams"; r["Entity Clarity Needed?"] = "NO"
        r["Brand/Expertise/Trust Signal Opportunity"] = "—"
        if is_test:
            act, pr = "REVIEW", "CRITICAL"
        elif is_side:
            act, pr = "OPTIMIZE", "CRITICAL"
        elif empty:
            act, pr = "REVIEW", "HIGH"
        elif s["title"].startswith("No change"):
            act, pr = "REVIEW", "MEDIUM"
        else:
            act, pr = "OPTIMIZE", "MEDIUM"
        if p.endswith("/round-rings"):
            pr = "HIGH"
        r["Recommended Action"] = act; r["Priority"] = pr
        r["Implementation Dependency"] = "Commercial keyword ratification + SERP check (D-07/D-19); CMS/code access for noindex/sitemap rules; slug fixes need a migration/redirect plan"
        r["Status"] = ("TEST ARTIFACT LIVE" if is_test else "LIVE — EMPTY INDEXABLE PAGE" if empty else "LIVE — NEEDS OPTIMIZATION")
        r["Evidence / Source"] = SRC_CAT + f"; IA status: {s['ia']}"
        r["Notes"] = s["note"] + " Current <title>/meta follow the template 'X | Parent | House of Diams' / 'Browse X in Parent.' (boilerplate)."
        rows.append(finish(r, dict(meta=(act == "OPTIMIZE"), h1=(act == "OPTIMIZE"), links=(act == "OPTIMIZE"), schema=(not is_test), conflict=bool(s["conflict"]) or is_side,
                                   cannib=("CANNIBALIZATION" in s["conflict"]) or bool(s["cands"] and not is_side and not is_test and not empty and False)),
                           a=["metadata/copy drafts" if act == "OPTIMIZE" else "decision memo"], b=["noindex / sitemap rules / slug changes" if (empty or is_test or any(t in p for t in ('solitare', 'anniversay', 'pavee'))) else "template schema change"],
                           c=["status, canonical, indexability, sitemap membership"]))
    return rows
