# -*- coding: utf-8 -*-
"""Builds the Step 2 master rows (list of dicts) from Step 1 + authored specs + the Step 2A resolutions (s2_final)."""
import re, collections
from s2_load import *
import s2_core, s2_subs, s2_edu, s2_blog, s2_final as FN

SUFFIX = " | House of Diams"

COLS = ["Row ID", "Row Group", "URL", "Page Name", "Page Type", "SEO Cluster", "Page Role",
        "Primary Keyword", "Secondary Keywords", "Related Terms", "Search Intent", "Keyword Owner", "Ownership Status", "Cannibalization Risk",
        "Current URL Status", "Current Canonical", "Current Indexability", "Current Content State",
        "Current Title", "Recommended Title (pre-suffix value)", "Rendered Title Preview", "Rendered Length", "Title Action",
        "Current Meta", "Recommended Meta", "Meta Length", "Meta Action",
        "Current H1", "Recommended H1", "H1 Action",
        "Content Action", "Section Recommendations",
        "Internal Links In", "Internal Links Out", "Anchor Context",
        "Current Schema", "Recommended Schema", "Schema Action",
        "AEO Opportunity", "Primary Questions", "GEO Opportunity", "Entity/Trust Opportunity", "Image/Alt Action",
        "Recommended Action", "Priority", "AWS Class", "Implementation Dependency", "Decision Resolution", "Remaining Dependencies",
        "HOD Facts Needed", "GSC Data Needed", "Engineering Input Needed", "Status", "Evidence/Source", "Notes"]

STATUSES = ["READY FOR IMPLEMENTATION POST-AWS", "PRE-AWS PREPARATION", "HOD INPUT REQUIRED", "ENGINEERING INPUT REQUIRED", "GSC BASELINE REQUIRED",
            "CONDITIONAL — PRODUCT/OFFER CONFIRMATION", "NO CHANGE REQUIRED", "NOT PLANNED — CONDITIONAL"]

# ---- US English normalizer (recommended / customer-facing text only) ----
# Corrected 2026-10-10: the earlier list replaced the prefix "jeweller" before "jewellery", producing the misspelling "jewelery";
# verb stems also matched "symbolism"/"organism" ("symbolizm"). Rules now: longest forms first, verb stems need an inflection
# suffix, matching is case-preserving, URL/slug-like chunks (contain "/" or 2+ hyphens) are left alone, and text wrapped in
# \u27e6 \u27e7 is quoted current-site/historical text that must stay verbatim.
_UK_STEMS = [("jewellery", "jewelry"), ("jewellers", "jewelers"), ("jeweller", "jeweler"), ("enquir", "inquir"), ("labelled", "labeled"), ("colour", "color"),
             ("centred", "centered"), ("centre", "center"), ("catalogue", "catalog"), ("aluminium", "aluminum"), ("favour", "favor"), ("behaviour", "behavior")]
_UK_VERB = ("canonicalis", "normalis", "standardis", "prioritis", "optimis", "finalis", "customis", "organis", "recognis", "symbolis", "personalis",
            "itemis", "summaris", "utilis", "emphasis", "categoris", "specialis", "authoris", "minimis", "maximis", "visualis", "realis", "characteris")
_UK_SIMPLE_RE = [(re.compile(r"(?<![A-Za-z])" + a, re.I), b) for a, b in _UK_STEMS]
_UK_VERB_RE = re.compile(r"(?<![A-Za-z])(" + "|".join(_UK_VERB) + r")(e|es|ed|ing|ation|ations)\b", re.I)
_UK_ANALYSE_RE = re.compile(r"(?<![A-Za-z])analys(e|es|ed|ing)\b", re.I)
_QUOTE = re.compile("\u27e6(.*?)\u27e7", re.S)
_CHUNK = re.compile(r"[\w\-/.:%?=&#]+")


def _case(src, rep):
    if src.isupper() and len(src) > 1:
        return rep.upper()
    if src[:1].isupper():
        return rep[:1].upper() + rep[1:]
    return rep


def _us_chunk(m):
    c = m.group(0)
    if "/" in c or "://" in c or c.count("-") >= 2 or "fine-jewellery" in c.lower():
        return c
    for r, b in _UK_SIMPLE_RE:
        c = r.sub(lambda x, b=b: _case(x.group(0), b), c)
    c = _UK_VERB_RE.sub(lambda x: _case(x.group(1)[:-2], x.group(1)[:-2] + "iz") + x.group(2), c)
    c = _UK_ANALYSE_RE.sub(lambda x: "analyz" + x.group(1), c)
    return c


def _us_plain(s):
    return _CHUNK.sub(_us_chunk, s)


def us(s):
    """US spelling for recommended text. Segments wrapped in U+27E6/U+27E7 are quoted current-site/historical text: kept verbatim, markers removed."""
    if not s:
        return s
    out, pos = [], 0
    for m in _QUOTE.finditer(s):
        out.append(_us_plain(s[pos:m.start()]))
        out.append(m.group(1))
        pos = m.end()
    out.append(_us_plain(s[pos:]))
    return "".join(out)


# Narrative documents (md): conservative variant. 'jewellery', 'colour', 'centre' and 'catalogue' are NOT touched because the docs quote current-site
# text, URLs and research terms verbatim; only unambiguous prose spellings are normalized.
_DOC_STEMS = [("jewellers?\\b", "jeweler"), ("enquir", "inquir"), ("labelled", "labeled"), ("favour", "favor"), ("behaviour", "behavior")]
_DOC_STEMS_RE = [(re.compile(r"(?<![A-Za-z])" + a, re.I), b) for a, b in _DOC_STEMS]


def _usdoc_chunk(m):
    c = m.group(0)
    if "/" in c or "://" in c or c.count("-") >= 2 or "fine-jewellery" in c.lower():
        return c
    for r, b in _DOC_STEMS_RE:
        c = r.sub(lambda x, b=b: _case(x.group(0), b + ("s" if x.group(0).lower().endswith("s") and b == "jeweler" else "")), c)
    c = _UK_VERB_RE.sub(lambda x: _case(x.group(1)[:-2], x.group(1)[:-2] + "iz") + x.group(2), c)
    c = _UK_ANALYSE_RE.sub(lambda x: "analyz" + x.group(1), c)
    return c


def us_doc(t):
    out, pos = [], 0
    for m in _QUOTE.finditer(t):
        out.append(_CHUNK.sub(_usdoc_chunk, t[pos:m.start()]))
        out.append(m.group(1))
        pos = m.end()
    out.append(_CHUNK.sub(_usdoc_chunk, t[pos:]))
    return "".join(out)


def blogname(s):
    """OD-12: public section name is 'Blog'."""
    s = re.sub(r"House of Diams journal", "House of Diams blog", s)
    s = re.sub(r"\bBack to Journal\b", "Back to Blog", s)
    s = re.sub(r"\bJournal\b", "Blog", s)
    s = re.sub(r"\bjournal\b", "blog", s)
    return s


def clean(s, n=None):
    s = (s or "").replace("\n", " ").strip()
    s = re.sub(r"\s+", " ", s)
    return s[:n] if n else s


def cand_text(pk):
    m = re.search(r"Candidate[^:]*:\s*(.*)", pk or "")
    return clean(m.group(1)) if m else clean(pk, 400)


def vol_of(term):
    t = term.lower().strip()
    for x in KMAP:
        if x["keyword"].lower() == t:
            return x["search_volume"]
    return None


def find_core(rid, group):
    if rid in s2_core.CORE:
        return s2_core.CORE[rid]
    for k, v in s2_core.CORE.items():
        if rid.startswith(k[:34]) or k.startswith(rid):
            return v
    return None


def stage15_str(tid):
    top, n = stage15_top(tid, 3)
    if not n:
        return "Stage 15: 0 keywords mapped"
    return "Stage 15: %d keywords mapped; top: %s" % (n, "; ".join("%s (%s)" % (k, v) for k, v in top))


def n_products(path):
    il = live_links(path)
    if il is None:
        return None
    return len([l for l in il if l.startswith("/shop/")])


def rendered(title, rid):
    if not title or title.startswith("—") or title.startswith("(") or title.startswith("{"):
        return "—", ""
    return (title if rid == "NAV-HOME" else title + SUFFIX), len(title if rid == "NAV-HOME" else title + SUFFIX)


# ---- dependency defaults for article rows ----
EDU_HOD = {"EDU-LG-02": "F-E2 (keeps natural-diamond framing neutral)", "EDU-MET-00": "F-E4 (platinum/karat availability — not claimed)", "EDU-MET-01": "F-E4",
           "EDU-RJG-03": "F-E5 (services — not claimed)", "EDU-INS": "F-E5 (services — not claimed)", "EDU-NAT-00": "F-E2", "EDU-CERT-00": "F-B1 (HOD-specific statements only)",
           "EDU-CERT-01": "F-B1 (HOD-specific statements only)", "EDU-LG-07": "F-E6 (sourcing claims — not made)", "BC-005": "F-E6", "BC-015": "F-E6",
           "BC-017": "F-A1 (holiday timing statements)", "BC-034": "F-A1 (holiday timing statements)", "BC-019": "F-A1"}
GSC_EQ = {"EDU-LG-03", "EDU-LG-02", "EDU-LG-10", "EDU-MET-01"}


def deps_str(d):
    parts = []
    if d.get("hod"):
        parts.append("HOD: " + d["hod"])
    if d.get("eng"):
        parts.append("ENG: " + d["eng"])
    if d.get("gsc"):
        parts.append("GSC: " + d["gsc"])
    return " | ".join(parts) if parts else "None beyond the AWS cut-over"


# ---- keyword / ownership text ----
def assignment_text(rid):
    a = FN.A[rid]
    st = a["state"]
    sec = []
    for s in a["sec"]:
        base = s.rstrip("*")
        cond = s.endswith("*")
        if "→" in base or "(" in base:
            sec.append(base + (" [conditional]" if cond else ""))
        else:
            sec.append(FN.fmt(base) + (" [conditional]" if cond else ""))
    secs = ("; secondary: " + "; ".join(sec)) if sec else ""
    if st.startswith("ASSIGNED"):
        txt = "ASSIGNED 2026-10-10 (OD-01/OD-16, delegated): %s%s | evidence: volume + DFS intent label; SERP %s | confidence %s" % (
            FN.fmt(a["primary"]), secs, a["serp"].split(" (")[0].lower() if a["serp"].startswith("NOT") else a["serp"], a["conf"])
        if a["proxy"]:
            txt += " | volume is a PROXY (measured phrase differs from the unmodified head)"
        own = "RATIFIED 2026-10-10 (delegated, OD-01) — confidence %s%s" % (a["conf"], "; INVENTORY WATCH" if "WATCH" in st else "")
        if "side stones" in a["primary"]:
            own = "RATIFIED — Stage 15 owner (unchanged); SERP-validated (Stage 8)"
        return txt, own
    if st.startswith("RESERVED"):
        return ("RESERVED — inactive until the page is populated (noindex now): %s | confidence %s" % (FN.fmt(a["primary"]), a["conf"]),
                "RESERVED — INACTIVE UNTIL POPULATED (OD-01)")
    if st.startswith("HELD — TAXONOMY"):
        return ("HELD — TAXONOMY (F-E7): no keyword assigned%s | reason: %s" % (secs.replace("; secondary:", "; considered:"), a["why"]),
                "HELD — TAXONOMY CONFIRMATION (F-E7); no keyword until the category contents match the label (reversible default: scoped link-bracelet wording)")
    if st.startswith("HELD"):
        return ("HELD — AMBIGUOUS (OD-01): no primary assigned%s | reason: %s" % (secs.replace("; secondary:", "; held candidate:"), a["why"]),
                "HELD — AMBIGUOUS (specific reason recorded; reversible default: descriptive title)")
    if st.startswith("NOT BUILT"):
        return ("NOT BUILT (OD-02): head terms deliberately unowned%s | %s" % (secs, a["why"][:260]), "NOT BUILT — no separate commercial hub (OD-02 adopted)")
    if st == "NO KEYWORD BY DESIGN":
        return ("NONE BY DESIGN — " + a["why"], "NO KEYWORD BY DESIGN")
    return ("NONE — no measured demand in project datasets%s | %s" % (secs, a["why"]), "NO KEYWORD — NO MEASURED DEMAND (page not promoted; GSC review trigger)")


def build():
    rows = []
    for s1 in S1:
        rid = s1["Row ID"]
        grp = s1["Row Group"]
        url = s1["URL"]
        path = path_of(url) if url.startswith("http") else None
        ov = {}
        if grp in ("CORE LIVE", "HUBS", "COMMERCIAL CATEGORY", "PRODUCT PAGES", "LEGACY / REDIRECT"):
            ov = find_core(rid, grp) or {}
        elif grp == "COMMERCIAL SUBCATEGORY":
            ov = s2_subs.sub_row(path, s1)
        elif grp == "EXISTING ARTICLES (Education-owned)":
            ov = s2_edu.EXIST[rid]
        elif grp == "CONDITIONAL COMMERCIAL":
            ov = s2_edu.LG_HUB
        if grp == "PLANNED EDUCATION":
            ov = planned_edu(rid, s1)
        elif grp == "CONDITIONAL EDUCATION":
            ov = cond_edu(rid, s1)
        elif grp == "PLANNED BLOG":
            ov = s2_blog.blog_override(rid, CAL.get(rid, {}))
        if not ov:
            raise SystemExit("NO OVERRIDE for %s (%s)" % (rid, grp))
        rows.append(make_row(s1, ov, path))
    return rows


def planned_edu(rid, s1):
    t, m, h, pr, note = s2_edu.PLANNED[rid]
    mm = s2_edu.MISMATCH.get(rid)
    conf = rid in s2_edu.CONFIRM
    secs = brief_sections(rid)
    if secs:
        sect = "Stage 19 brief sections: " + "; ".join("[%s] %s" % (i[:4], h_) for i, h_ in secs[:14]) + " | Note: " + note
    else:
        sect = "No Stage 19 brief exists for this page — create the brief at writing time from the calendar row (PAA, AEO format hint, link targets) and the boundary in the note. | Note: " + note
    dec = ("OD-03; OD-04" if (mm and conf) else "OD-03" if mm else "OD-04" if conf else "OD-05")
    return dict(
        title=t, tact="FINAL — primary ratified 2026-10-10 (%s); adjust only if the written article changes the answer" % ("OD-03" if mm else "OD-04" if conf else "owner confirmed"),
        meta=m, mact="FINAL DRAFT (answer-first; adjust only if the written article changes the answer)",
        h1=h, hact="FINAL DRAFT",
        cact="WRITE (Stage 19 brief)" if secs else "BRIEF THEN WRITE",
        sect=sect, sch=s2_edu.SCH_ART, sact="TEMPLATE (Class B) — at launch",
        prio=pr, aws="A", status="PRE-AWS PREPARATION", bf="N", gsc="N", dec=dec,
        dep="Write now (Class A); publish inside the migration-safe window (Class B, E-01); Stage 16 launch links must ship with the page.",
        notes=note, deps=dict(hod=EDU_HOD.get(rid, ""), eng="E-01, E-02, E-07"))


def cond_edu(rid, s1):
    extra = " Hub-index condition (≥2 child guides) is satisfied once EDU-RJG-BR/NL launch — activation is a documented follow-up, no calendar slot." if rid == "EDU-RJG-00" else ""
    return dict(
        title="— (not planned)", tact="N/A — conditional", meta="—", mact="N/A", h1="—", hact="N/A", cact="NOT PLANNED",
        sect=s2_edu.COND_NOTE + extra, sch="At activation: BlogPosting/Article + BreadcrumbList.", sact="N/A", aeo="N/A", qs="—", geo="—", trust="—", img="N/A",
        prio="LOW", aws="A", dep="Stage 14 activation conditions.", dec="OD-04", status="NOT PLANNED — CONDITIONAL", bf="N", gsc="N",
        notes="Documented so that Step 1 coverage is complete; not an on-page task.", deps=dict())


def action_for(grp, ov, rid):
    st = ov.get("status", "")
    if rid == "BRAND-CONTACT":
        return "CREATE PAGE"
    if grp == "LEGACY / REDIRECT":
        return "REDIRECT" if "301" in ov.get("cact", "") and "REDIRECT" in ov.get("cact", "") else ("NO ACTION" if "NO CHANGE" in st else "REVIEW")
    if "NO CHANGE" in st:
        return "NO ACTION"
    if grp == "CONDITIONAL EDUCATION":
        return "NOT PLANNED"
    if grp == "CONDITIONAL COMMERCIAL":
        return "DO NOT BUILD (reversible)"
    if grp == "PLANNED BLOG":
        if ov.get("action"):
            return ov["action"]
        return "PUBLISH (packaged)" if rid in s2_blog.PACKAGED else ("HOLD (HOD facts)" if st == "HOD INPUT REQUIRED" else "WRITE")
    if grp == "PLANNED EDUCATION":
        return "WRITE"
    if grp == "EXISTING ARTICLES (Education-owned)":
        return "RETARGET + REFRESH" if "RETARGET" in ov.get("cact", "") else "REFRESH IN PLACE"
    if grp == "COMMERCIAL SUBCATEGORY":
        c = ov.get("cact", "")
        if c.startswith("REMOVE"):
            return "REMOVE"
        if c.startswith("CANONICAL"):
            return "CANONICAL + EXCLUDE"
        return "NOINDEX + EXCLUDE" if c.startswith("NOINDEX") else "OPTIMIZE"
    if rid in ("COM-COLLECTION",):
        return "NOINDEX + EXCLUDE"
    if rid == "COM-ER-STYLES-GROUP":
        return "CANONICAL + EXCLUDE"
    return "OPTIMIZE" if grp != "PRODUCT PAGES" else "OPTIMIZE (template)"


EV_EXTRA = {"CORE LIVE": "Step 2: title-suffix behavior re-verified live 2026-10-09 (og:title vs <title>); trust-page text re-read live 2026-10-09",
            "COMMERCIAL SUBCATEGORY": "Step 2: architecture/12_ia_decision_log.md D-03, D-07, D-13, D-15, D-19; 16_page_link_requirements.csv; initial-HTML product-set comparison (crawl 2026-10-09)",
            "COMMERCIAL CATEGORY": "Step 2: architecture/12_ia_decision_log.md D-02, D-05, D-07, D-13, D-14, D-18, D-19; initial-HTML product-set comparison",
            "EXISTING ARTICLES (Education-owned)": "Step 2: content-strategy/13_existing_content_decisions.csv, 15_ranking_equity_protection.csv, 17_/18_ question & entity files, calendar",
            "PLANNED EDUCATION": "Step 2: content-strategy/19_brief_registry.csv, 19_content_briefs.csv, 19_internal_link_requirements.csv, 17_question_map.csv; calendar; 13_blog_strategy.md §3–4",
            "PLANNED BLOG": "Step 2: calendar + blogs/ packages (read-only)",
            "PRODUCT PAGES": "Step 2: QA/06 PDP audit; live PDP re-read 2026-10-09"}


def make_row(s1, ov, path):
    rid, grp = s1["Row ID"], s1["Row Group"]
    url = s1["URL"]
    if url.startswith("PLANNED — /blog/<slug"):
        url = "PLANNED — /blog/<slug> generated from the Article Title at first save"
    elif url.startswith("PLANNED — URL PENDING (slug not decided)"):
        url = "PLANNED — URL PENDING (slug not decided)"
    # ---- re-homed item: BLOG-WR-TYPES is an Education page (OD-04)
    ptype, role = clean(s1["Page Type"]), clean(s1["Page Role"], 120)
    owner = clean(s1["Keyword Owner"], 200)
    if rid == "BLOG-WR-TYPES":
        url = "PLANNED — URL PENDING (proposed under Ring & Jewelry Guides; slug not decided; re-homed from Blog)"
        grp = "PLANNED EDUCATION"
        ptype, role = "EDUCATION_ARTICLE", "Informational (Education — re-homed from Blog, OD-04)"
    # ---- keyword / ownership
    pk, own = None, None
    if rid in FN.A:
        pk, own = assignment_text(rid)
        owner = owner + " | assigned 2026-10-10 (see 10-DECISIONS-RESOLUTION-LOG.md §OD-01)"
    elif rid in s2_edu.MISMATCH:
        s19, calp, vol, _, _ = s2_edu.MISMATCH[rid]
        fp, cop, why = FN.EDU3[rid]
        v19 = vol_of(s19)
        pk = ("FINAL 2026-10-10 (OD-03, R2): '%s' (%s/mo; calendar primary, SERP-validated in the calendar rounds) | %s | Stage 17/19 primary was '%s' (%s) | %s | %s"
              % (fp, vol, cop, s19, (v19 + "/mo") if v19 else "volume not in Stage 15 map", stage15_str(rid), why))
        own = "RATIFIED — page owner Stage 14/15 (unchanged); primary resolved 2026-10-10 (OD-03)" + ("; owner confirmed (OD-04)" if rid in s2_edu.CONFIRM else "")
        owner = owner + " | primary resolved 2026-10-10 (see 10-DECISIONS-RESOLUTION-LOG.md §OD-03)"
    elif rid in s2_edu.CONFIRM:
        c = CAL[rid]
        o, treat, src = s2_edu.EDU4_ROWS[rid] if hasattr(s2_edu, "EDU4_ROWS") else FN.EDU4[rid]
        pk = "FINAL 2026-10-10 (OD-04): '%s' (%s/mo; calendar primary) | %s | %s" % (c["primary_keyword"], format(int(c["primary_search_volume"]), ","), treat, stage15_str(rid) if rid != "BLOG-WR-TYPES" else "new Education page; no Stage 15 mapping")
        own = "RATIFIED 2026-10-10 (delegated, OD-04) — " + o
        owner = o + " | ratified 2026-10-10 (see 10-DECISIONS-RESOLUTION-LOG.md §OD-04)"
    elif rid == "EXIST-BLOG-ER-ONLINE":
        pk = "NO STAGE 15 OWNER — retained as is (OD-13); must not target 'how to choose a lab grown diamond' (EDU-LG-10)"
        own = "NO STAGE 15 OWNER — RETAINED UNCHANGED (OD-13 adopted); consolidation deferred to GSC"
    elif grp == "EXISTING ARTICLES (Education-owned)" or grp == "PLANNED EDUCATION":
        pk = clean(s1["Primary Keyword"], 420)
        own = "RATIFIED — Stage 15 page owner; calendar and Stage 19 primary agree"
    elif grp == "PLANNED BLOG":
        pk = clean(s1["Primary Keyword"], 260)
        own = "BLOG-OWNED (final calendar; outside Stage 15 — no conflict found, QA/04 §4c)"
    elif grp == "CONDITIONAL EDUCATION":
        pk = "NONE ASSIGNED — conditional/deferred owner; not planned"
        own = "CONDITIONAL — NOT PLANNED"
    elif grp in ("LEGACY / REDIRECT",):
        pk = "NONE (legacy URL)" if rid != "LEG-ER-SIDESTONE" else "NONE of its own (the owned keyword 'side stones engagement rings' lives on the /by-design/ URL)"
        own = "NOT APPLICABLE (legacy URL)"
    pk = pk or clean(s1["Primary Keyword"], 420)
    own = own or "NO KEYWORD BY DESIGN"
    # ---- current state
    if path and path in CRAWL and grp not in ("PLANNED EDUCATION", "PLANNED BLOG"):
        cstate = content_state(path)
        npd = n_products(path)
        if npd is not None and (grp in ("COMMERCIAL CATEGORY", "COMMERCIAL SUBCATEGORY", "CORE LIVE") and npd):
            cstate += "; %d product links in initial HTML (listing paginated 24/page)" % npd
        if grp == "COMMERCIAL SUBCATEGORY" and npd == 0:
            cstate += "; 0 product links — EMPTY"
    elif grp in ("PLANNED EDUCATION", "PLANNED BLOG", "CONDITIONAL EDUCATION", "CONDITIONAL COMMERCIAL"):
        cstate = "NOT LIVE (planned/conditional; no matching URL in live sitemap or crawl, 2026-10-09)"
    else:
        cstate = clean(s1["Current URL Status"], 200)
    cur = lambda k: clean(s1[k], 400)
    # ---- title/meta
    t = us(ov.get("title", ""))
    rt, rl = rendered(t, rid)
    m = us(ov.get("meta", ""))
    ml = len(m) if m and not m.startswith("(") and not m.startswith("—") else ""
    # ---- links (US spelling; OD-12 'Blog' naming)
    lin = clean(s1["Recommended Internal Links IN"], 1400)
    if " || OUT REQUIRED" in lin:
        lin = lin.split(" || OUT REQUIRED")[0]
    lin = blogname(us(lin[:900]))
    lout = blogname(us(clean(s1["Recommended Internal Links OUT"], 900)))
    anc = blogname(us(clean(s1["Recommended Anchor Context"], 700)))
    # ---- schema/AEO fields
    aeo = ov.get("aeo") or clean(s1["AEO Opportunity"], 300)
    qs = ov.get("qs") or clean(s1["Primary Questions to Answer"], 500)
    if grp in ("PLANNED EDUCATION", "EXISTING ARTICLES (Education-owned)") and qs.count("?") < 3:
        qq = [x for x in QMAP if x["target_page_id"] == rid and x["recommended_role"] in ("SECTION_QUESTION", "PRIMARY", "H2_QUESTION", "CORE_QUESTION")] or [x for x in QMAP if x["target_page_id"] == rid]
        def mv(x):
            try:
                return -int(float(x["max_search_volume"]))
            except Exception:
                return 0
        qq.sort(key=mv)
        extra = []
        for x in qq:
            if x["question"] not in qs and x["question"] not in extra:
                extra.append(x["question"])
            if len(extra) >= 5:
                break
        if extra:
            qs = (qs + " | " if qs and qs != "—" else "") + " | ".join(extra) + "  [Stage 17 question map]"
    if grp in ("PLANNED EDUCATION", "PLANNED BLOG") and qs.count("?") < 3 and CAL.get(rid):
        pq = [q for q in paa_for(CAL[rid]["primary_keyword"]) if q not in qs][:5]
        if pq:
            qs = (qs + " | " if qs and qs != "—" else "") + " | ".join(pq) + "  [PAA captured in calendar research]"
    geo = ov.get("geo") or clean(s1["GEO/AI Search Opportunity"], 400)
    trust = ov.get("trust") or clean(s1["Brand/Expertise/Trust Signal Opportunity"], 400)
    img = ov.get("img") or clean(s1["Recommended Image/Alt-Text Changes"], 300)
    # ---- dependencies / decisions / status
    d = dict(ov.get("deps") or {})
    if (grp in ("EXISTING ARTICLES (Education-owned)", "PLANNED BLOG") or rid == "BLOG-WR-TYPES") and not d:
        d = dict(hod=EDU_HOD.get(rid, ""), eng="E-01, E-02, E-07")
    if rid in GSC_EQ:
        d["gsc"] = "G-01, G-02 (blocking before title/H1/body edits)"
        d["gscblock"] = True
    if grp == "EXISTING ARTICLES (Education-owned)" and rid not in GSC_EQ and rid in EDU_HOD and not d.get("hod"):
        d["hod"] = EDU_HOD[rid]
    if rid in EDU_HOD and not d.get("hod"):
        d["hod"] = EDU_HOD[rid]
    if not d.get("hod") and not d.get("eng") and not d.get("gsc"):
        d = dict(d)
    prio, aws, status = ov["prio"], ov["aws"], ov["status"]
    action = ov.get("action") or action_for(grp, ov, rid)
    ta = us(ov.get("tact", ""))
    if ta.startswith("KEEP") and isinstance(rl, int) and rl > 60:
        ta += " [rendered %d chars: key terms are front-loaded; SERP truncation is cosmetic]" % rl
    dec_res = FN.dec_ref(ov.get("dec", ""))
    row = {
        "Row ID": rid, "Row Group": grp, "URL": url,
        "Page Name": us(ov.get("name") or clean(s1["Page/Content Name"], 160)),
        "Page Type": ptype, "SEO Cluster": us(clean(s1["SEO Cluster / Topic"], 200)), "Page Role": us(role),
        "Primary Keyword": clean(pk, 760), "Secondary Keywords": clean(s1["Secondary Keywords"], 500), "Related Terms": us(clean(ov.get("related") or s1["Related/Semantic Concepts"], 300)),
        "Search Intent": us(clean(s1["Search Intent"], 220)), "Keyword Owner": owner, "Ownership Status": clean(own, 400),
        "Cannibalization Risk": us(clean(ov.get("cann") or s1["Cannibalization Risk"], 420)),
        "Current URL Status": cur("Current URL Status"), "Current Canonical": cur("Current Canonical"), "Current Indexability": cur("Current Indexability"), "Current Content State": cstate,
        "Current Title": cur("Current SEO Title"), "Recommended Title (pre-suffix value)": t, "Rendered Title Preview": rt, "Rendered Length": rl, "Title Action": ta,
        "Current Meta": cur("Current Meta Description"), "Recommended Meta": m, "Meta Length": ml, "Meta Action": us(ov.get("mact", "")),
        "Current H1": cur("Current H1"), "Recommended H1": us(ov.get("h1", "")), "H1 Action": us(ov.get("hact", "")),
        "Content Action": us(ov.get("cact", "")), "Section Recommendations": us(ov.get("sect", "")),
        "Internal Links In": lin, "Internal Links Out": lout, "Anchor Context": anc,
        "Current Schema": cur("Current Schema"), "Recommended Schema": us(ov.get("sch", "")), "Schema Action": us(ov.get("sact", "")),
        "AEO Opportunity": us(aeo), "Primary Questions": us(qs), "GEO Opportunity": us(geo), "Entity/Trust Opportunity": us(trust), "Image/Alt Action": us(img),
        "Recommended Action": action, "Priority": prio, "AWS Class": aws, "Implementation Dependency": us(ov.get("dep", "")),
        "Decision Resolution": dec_res, "Remaining Dependencies": deps_str(d),
        "HOD Facts Needed": "Y" if d.get("hod") else "N", "GSC Data Needed": "Y" if d.get("gsc") else "N", "Engineering Input Needed": "Y" if d.get("eng") else "N",
        "Status": status,
        "Evidence/Source": clean(s1["Evidence / Source"], 330) + " || " + EV_EXTRA.get(grp, "Step 2: QA/01, QA/04, QA/05 and the source files named in Evidence") + " || Resolutions: 10-DECISIONS-RESOLUTION-LOG.md",
        "Notes": us(ov.get("notes", "")),
    }
    return row


if __name__ == "__main__":
    rows = build()
    print(len(rows))
    print(collections.Counter(r["Priority"] for r in rows))
    print(collections.Counter(r["Status"] for r in rows))
    print(collections.Counter(r["AWS Class"] for r in rows))
