"""Helpers: ID→display mapping, link lists, entity/question presence checks, article text."""
import json, re
import lib_research as L
from mm_core import *

IDMAP_FIXED = {
    "NAV-HOME": "Homepage (/)",
    "COM-SHOP": "/shop",
    "COM-ER": "/engagement-rings",
    "COM-ER-SIDESTONE": "/engagement-rings/by-design/side-stone-rings",
    "COM-ER-STYLES": "ER style subcategories (/engagement-rings/by-design/*)",
    "COM-WB": "/wedding-bands",
    "COM-WB-GENDER": "WB gender subcategories (/wedding-bands/for-her, /for-him)",
    "COM-FJ": "/fine-jewellery",
    "COM-FJ-EARRINGS": "/fine-jewellery/earrings",
    "COM-FJ-NECKLACES": "/fine-jewellery/necklaces",
    "COM-FJ-BRACELETS": "/fine-jewellery/bracelet",
    "COM-FJ-RINGS": "/fine-jewellery/rings",
    "COM-FJ-TYPE-SUBCATS": "FJ type subcategories",
    "COM-CURATED-TBAR": "/t-bar",
    "COM-LG-HUB": "COM-LG-HUB (conditional commercial lab-grown hub — not built)",
    "COM-BESPOKE": "/bespoke",
    "COM-PDP": "PDPs (/shop/<slug>)",
    "COM-PDP-OVAL-FLORAL": "/shop/oval-floral-diamond-ring",
    "EDU-ROOT": "/education",
    "BLOG-HUB": "/blog",
    "BLOG-CRAFT": "Blog: Craft & Making posts",
    "BLOG-STYLE": "Blog: Style & Trends posts",
    "BLOG-GIFTS": "Blog: Gifts & Occasions posts",
    "BLOG-LAUNCH": "Blog: Collections & Launches posts",
    "BLOG-INDUSTRY": "Blog: Industry Notes posts",
    "BLOG-STORIES": "Blog: Stories posts (conditional)",
    "BRAND-ABOUT": "/about",
    "BRAND-CONTACT": "Contact (currently a modal: /contact → /?contact=open)",
    "SUP-FAQ": "/faq",
    "SUP-POLICIES": "/shipping, /returns, /privacy-policy, /terms",
    "TPL-HEADER": "global header",
    "TPL-FOOTER": "global footer",
    "EXIST-BLOG-ER-ONLINE": "/blog/how-to-choose-a-lab-grown-diamond-engagement-ring-online-house-of-diams",
    "EDU-RJG-00": "Ring & Jewellery Guides index (EDU-RJG-00; URL pending)",
}

# live path for IDs that exist today (for link-presence checks)
LIVE_PATH = {
    "NAV-HOME": "/", "COM-SHOP": "/shop", "COM-ER": "/engagement-rings",
    "COM-ER-SIDESTONE": "/engagement-rings/by-design/side-stone-rings", "COM-WB": "/wedding-bands",
    "COM-FJ": "/fine-jewellery", "COM-FJ-EARRINGS": "/fine-jewellery/earrings",
    "COM-FJ-NECKLACES": "/fine-jewellery/necklaces", "COM-FJ-BRACELETS": "/fine-jewellery/bracelet",
    "COM-FJ-RINGS": "/fine-jewellery/rings", "COM-CURATED-TBAR": "/t-bar", "COM-BESPOKE": "/bespoke",
    "COM-PDP-OVAL-FLORAL": "/shop/oval-floral-diamond-ring", "EDU-ROOT": "/education", "BLOG-HUB": "/blog",
    "BRAND-ABOUT": "/about", "SUP-FAQ": "/faq",
    "EXIST-BLOG-ER-ONLINE": "/blog/how-to-choose-a-lab-grown-diamond-engagement-ring-online-house-of-diams",
}
for tid, r in L.registry.items():
    eu = r["existing_url"]
    if eu and tid not in LIVE_PATH and not tid.startswith("COM-ER-SIDESTONE"):
        LIVE_PATH[tid] = eu


def disp(i):
    i = i.strip()
    if i in IDMAP_FIXED:
        return f"{i} → {IDMAP_FIXED[i]}" if not IDMAP_FIXED[i].startswith("/") and i not in ("NAV-HOME",) else f"{IDMAP_FIXED[i]}"
    r = L.registry.get(i)
    if r:
        u = r["existing_url"] or r["proposed_url"]
        return f"{i} ({u})" if u and u != "URL_PENDING" else f"{i} (URL pending: {r['target_page_name'][:50]})"
    lr = L.links_req.get(i)
    if lr:
        return f"{i} (planned/conditional)"
    c = L.cal_by_id.get(i)
    if c:
        return f"{i} (planned blog/edu: {c['primary_keyword']})"
    return i


def parse_ids(s):
    """'3: A; B; C' -> ['A','B','C']"""
    if not s or s.strip() in ("0", ""):
        return []
    s = re.sub(r"^\d+:\s*", "", s.strip())
    return [p.strip() for p in s.split(";") if p.strip()]


def link_summary(pid, which):
    lr = L.links_req.get(pid)
    if not lr:
        return ""
    if which == "in":
        req = parse_ids(lr["incoming_required"]); rec = parse_ids(lr["incoming_recommended"])
    else:
        req = parse_ids(lr["outgoing_required"]); rec = parse_ids(lr["outgoing_recommended"])
    req = [x for x in req if not x.startswith("TPL-")] or req
    out = []
    if req:
        out.append("REQUIRED: " + "; ".join(disp(x) for x in req))
    if rec:
        out.append("RECOMMENDED: " + "; ".join(disp(x) for x in rec))
    return " || ".join(out)


def anchor_ctx(tid, n=3):
    """Recommended anchors OTHER pages should use to link TO this target (Stage 16 anchor strategy)."""
    rows = L.anchors.get(tid, [])
    out = []
    for r in rows[:n]:
        out.append(f"{r['anchor_type']}: “{r['recommended_anchor'][:110]}”")
    av = rows[0]["avoid_anchor"][:140] if rows else ""
    s = " | ".join(out)
    if av:
        s += f" || AVOID: {av}"
    return s


ART = json.load(open(L.SCR + "articles/articles.json"))


def missing_required_out(pid, live_links, page_path):
    """Return REQUIRED outgoing link targets that have a live URL but are NOT linked from the crawled page."""
    lr = L.links_req.get(pid)
    if not lr:
        return [], []
    miss, ok = [], []
    for x in parse_ids(lr["outgoing_required"]):
        p = LIVE_PATH.get(x)
        if not p or x.startswith("TPL-"):
            continue
        if p == page_path:
            continue
        norm_l = {l.rstrip("/") or "/" for l in live_links}
        (ok if (p.rstrip("/") or "/") in norm_l else miss).append(x)
    return miss, ok


def present(text, term):
    t = text.lower()
    term = re.sub(r"\(.*?\)", "", term).strip().lower()
    toks = [w for w in re.split(r"[\s/\-–,]+", term) if len(w) > 2]
    if not toks:
        return True
    if term in t:
        return True
    return all(w in t for w in toks[:3]) if len(toks) <= 3 else sum(w in t for w in toks) >= max(2, len(toks) - 1)


def entity_presence(tid, path):
    a = ART.get(path)
    if not a:
        return None
    txt = a["text"]
    req = [x for x in L.ecov.get(tid, []) if x["required_or_supporting"] == "REQUIRED"]
    seen, miss = [], []
    for e in req:
        nm = e["entity"]
        (seen if present(txt, nm) else miss).append(nm)
    return seen, miss


def question_presence(tid, path, n=40):
    a = ART.get(path)
    if not a:
        return None
    heads = " ".join(a["heads"]).lower()
    txt = a["text"].lower()
    stop = set("what is the are a an of to do does can how which why for in or and vs with your you it be".split())
    core = [q for q in L.qcov.get(tid, []) if q["recommended_treatment"] in ("CORE_SECTION", "FAQ", "SUPPORTING_SECTION") and q["coverage_status"] in ("BODY_UNKNOWN", "TITLE/H1_NOT_EVIDENT")]
    seen_q, missing_q = [], []
    done = set()
    for q in core:
        qq = q["question"]
        if qq.lower() in done:
            continue
        done.add(qq.lower())
        toks = [w for w in re.findall(r"[a-z0-9]+", qq.lower()) if w not in stop and len(w) > 2]
        if not toks:
            continue
        hit_h = sum(w in heads for w in toks) / len(toks)
        hit_t = sum(w in txt for w in toks) / len(toks)
        if hit_h >= 0.6:
            seen_q.append((qq, "heading"))
        elif hit_t >= 0.8:
            seen_q.append((qq, "body"))
        else:
            missing_q.append(qq)
    return seen_q, missing_q


def pairs_for(tid):
    out = []
    for x in L.cannib:
        if x["check"] == "E_PROPOSED_OVERLAPPING_INTENT" and tid in x["subject"]:
            out.append(f"{x['severity']}: {x['subject']}")
    return out


def ranking_equity(path):
    rows = L.equity.get(path, [])
    if not rows:
        return ""
    best = min(int(r["ranking_position"]) for r in rows)
    return f"{len(rows)} DataForSEO Labs ranked keyword(s) (Stage 3 snapshot, NOT GSC; best est. pos {best})"
