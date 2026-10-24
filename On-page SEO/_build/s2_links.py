# -*- coding: utf-8 -*-
"""Internal-link specification rows (resolved to real URLs) + PDP priority rows."""
import re, collections, csv
from s2_load import *
from s2_build import us, blogname

LINK_COLS = ["Link ID", "Source ID", "Source URL", "Source Status", "Destination ID", "Destination URL", "Destination Status",
             "Link Type", "Relationship", "Recommended Anchor", "Anchor Variants", "Avoid Anchor", "Placement / Context", "Purpose",
             "Stage 16 Priority", "Step 2 Priority", "Required At Launch", "Present In Live HTML?", "Destination Ownership Flag",
             "Ranking-Equity Note", "AWS Class", "Origin", "Notes"]


def id_maps(rows):
    by = {}
    for r in rows:
        by[r["Row ID"]] = r
    # Stage 16 ids that differ from master Row IDs
    alias = {"COM-ER-SIDESTONE": "SUB:/engagement-rings/by-design/side-stone-rings", "EDU-WB-TYPES": "BLOG-WR-TYPES"}
    return by, alias


GROUPS = {
    "COM-ER-STYLES": ("/engagement-rings/by-design/<style> (8 style subcategories)", "GROUP"),
    "COM-FJ-TYPE-SUBCATS": ("/fine-jewellery/<category>/<type> (earrings, necklaces, bracelet type pages)", "GROUP"),
    "COM-WB-GENDER": ("/wedding-bands/for-her and /wedding-bands/for-him", "GROUP"),
    "SUP-POLICIES": ("/shipping and /returns", "GROUP"),
    "COM-PDP": ("/shop/<product-slug> (184 PDPs)", "TEMPLATE"),
    "TPL-HEADER": ("site header / main menu", "TEMPLATE"), "TPL-FOOTER": ("site footer", "TEMPLATE"),
    "BLOG-HUB": ("/blog", "LIVE"),
    "BLOG-CRAFT": ("Blog category: Craft (posts under /blog)", "GROUP"), "BLOG-GIFTS": ("Blog category: Gifts & Occasions (posts under /blog)", "GROUP"),
    "BLOG-INDUSTRY": ("Blog category: Industry Notes (posts under /blog)", "GROUP"), "BLOG-LAUNCH": ("Blog category: Collections & Launches (posts under /blog)", "GROUP"),
    "BLOG-STORIES": ("Blog category: Stories / Ring culture (posts under /blog)", "GROUP"), "BLOG-STYLE": ("Blog category: Style & Trends (posts under /blog)", "GROUP"),
}


def resolve(pid, by, alias):
    """-> (url_text, status, row_or_None)"""
    if pid in GROUPS:
        u, st = GROUPS[pid]
        return u, st, by.get(pid)
    rid = alias.get(pid, pid)
    r = by.get(rid)
    if not r:
        return "UNRESOLVED (%s)" % pid, "UNRESOLVED", None
    u = r["URL"]
    grp = r["Row Group"]
    if u.startswith("http"):
        p = path_of(u)
        c = CRAWL.get(p)
        if grp in ("PLANNED EDUCATION", "PLANNED BLOG", "CONDITIONAL EDUCATION"):
            return p, "PLANNED — URL proposed/fixed, not live", r
        stt = "LIVE (200)" if c and str(c["status"]) == "200" else ("LIVE URL BUT NOT 200 / %s" % (c["status"] if c else "not in crawl"))
        return p, stt, r
    if "URL PENDING" in u:
        return "URL PENDING (slug not decided) — " + r["Page Name"][:60], "PLANNED — URL PENDING", r
    if "/blog/<slug>" in u:
        return "/blog/<slug generated from Article Title> — " + r["Page Name"][:50], "PLANNED — URL PENDING", r
    if "NOT PLANNED" in u or "NOT BUILT" in u:
        return "NO URL (conditional) — " + r["Page Name"][:60], "CONDITIONAL — NO URL", r
    return u, "PLANNED", r


def unresolved_flag(row):
    """Destination ownership still not a settled single owner after Step 2A (HELD / NOT BUILT)."""
    if not row:
        return ""
    o = row["Ownership Status"]
    if o.startswith("HELD") or o.startswith("NOT BUILT"):
        why = "OD-02 — no hub built"
        if o.startswith("HELD — TAXONOMY"):
            why = "OD-01 held — category contents vs label need HOD confirmation (F-E7)"
        elif o.startswith("HELD"):
            why = "OD-01 held — ambiguous head"
        return "DESTINATION OWNERSHIP NOT SETTLED (%s)" % why
    return ""


def s2_priority(p16, req, dest_status, link_type):
    if link_type in ("BREADCRUMB", "GLOBAL_NAV", "PRIMARY_NAV", "FOOTER"):
        return "MEDIUM" if p16 == "REQUIRED" else "LOW"
    if p16 == "REQUIRED":
        return "HIGH"
    if p16 == "RECOMMENDED":
        return "MEDIUM"
    return "LOW"


def build_links(rows):
    by, alias = id_maps(rows)
    l19 = {}
    for x in rd(KW + "/content-strategy/19_internal_link_requirements.csv"):
        l19[(x["source_page_id"], x["target_page_id"])] = x
    out = []
    n = 0
    for x in LINKMAP:
        n += 1
        su, ss, sr = resolve(x["source_page_id"], by, alias)
        du, ds, dr = resolve(x["target_page_id"], by, alias)
        l = l19.get((x["source_page_id"], x["target_page_id"]))
        ctx = (l["placement_context"] if l and l.get("placement_context") else "") or x["context_reason"]
        present = ""
        if ss.startswith("LIVE") and ds.startswith("LIVE") and su.startswith("/") and du.startswith("/"):
            il = live_links(su)
            if il is not None:
                present = "YES (initial HTML, any position incl. global nav)" if du in il else "NOT FOUND in initial HTML"
        elif ss == "TEMPLATE" or ds == "TEMPLATE":
            present = "template-level"
        notes = []
        if x["target_page_id"] == "COM-ER-SIDESTONE" or x["source_page_id"] == "COM-ER-SIDESTONE":
            notes.append("Stage 16 records the stale /by-desgin/ URL; use /by-design/ (OD-06)")
        if ds.startswith("PLANNED") or ds.startswith("CONDITIONAL"):
            notes.append("destination not live yet — link ships with the destination page")
        anchor = x["recommended_anchor"]
        if x["target_page_id"] == "COM-PDP-OVAL-FLORAL":
            anchor = "Oval Marquise Diamond Engagement Ring"
            notes.append("Stage 16 anchor used the current PDP name ('…Side-Stone…'); aligned to the recommended H1 (OD-15)")
        out.append({
            "Link ID": "L2-%03d" % n, "Source ID": x["source_page_id"], "Source URL": su, "Source Status": ss,
            "Destination ID": x["target_page_id"], "Destination URL": du, "Destination Status": ds,
            "Link Type": x["link_type"], "Relationship": x["relationship_type"], "Recommended Anchor": blogname(us(anchor)),
            "Anchor Variants": blogname(us(x["anchor_variants"])), "Avoid Anchor": blogname(us(l["avoid_anchor"] if l else "")),
            "Placement / Context": blogname(us(ctx[:300])), "Purpose": blogname(us(x["context_reason"][:200])),
            "Stage 16 Priority": x["priority"], "Step 2 Priority": s2_priority(x["priority"], x["required_at_launch"], ds, x["link_type"]),
            "Required At Launch": x["required_at_launch"], "Present In Live HTML?": present, "Destination Ownership Flag": unresolved_flag(dr),
            "Ranking-Equity Note": x["ranking_equity_protection"][:160],
            "AWS Class": "B" if ss.startswith("LIVE") else "A", "Origin": "Stage 16 link map (resolved)", "Notes": "; ".join(notes)})
    # --- Step 2 additions: planned Blog posts -> calendar internal_link_targets
    anchors = collections.defaultdict(list)
    for a in ANCHORS:
        anchors[a["target_page_id"]].append(a)
    k = 0
    for r in rows:
        if r["Row Group"] != "PLANNED BLOG":
            continue
        cal = CAL.get(r["Row ID"])
        if not cal:
            continue
        su, ss, sr = resolve(r["Row ID"], by, alias)
        if r["Row ID"] in ("BC-001", "BC-004", "BC-035", "BC-018", "BC-036", "BC-006", "BC-008", "BC-009", "BC-003", "BC-007"):
            su = r["URL"].replace("https://www.houseofdiams.com", "")
            ss = "PLANNED — URL fixed by approved package"
        for tid in dict.fromkeys(re.findall(r"[A-Z]+(?:-[A-Z0-9]+)+", cal["internal_link_targets"])):
            if tid == r["Row ID"] or (r["Row ID"] == "BLOG-WR-TYPES" and tid == "EDU-WB-TYPES"):
                continue
            du, ds, dr = resolve(tid, by, alias)
            if tid == "BLOG-WR-TYPES":
                tid = "EDU-WB-TYPES"
            an = anchors.get(tid)
            anc = ""
            if an:
                d = [a for a in an if a["anchor_type"] == "DESCRIPTIVE"] or an
                anc = d[0]["recommended_anchor"].split("|")[0].strip()
            else:
                m = re.search(re.escape(tid) + r": “([^”]+)”", r["Anchor Context"])
                anc = m.group(1) if m else (dr["Page Name"] if dr else tid)
            k += 1
            conf = unresolved_flag(dr)
            out.append({
                "Link ID": "L2-B%03d" % k, "Source ID": ("EDU-WB-TYPES" if r["Row ID"] == "BLOG-WR-TYPES" else r["Row ID"]), "Source URL": su, "Source Status": ss, "Destination ID": tid, "Destination URL": du,
                "Destination Status": ds, "Link Type": "CONTEXTUAL", "Relationship": "BLOG_POST_TO_TARGET", "Recommended Anchor": blogname(us(anc)), "Anchor Variants": "",
                "Avoid Anchor": blogname(us(an[0]["avoid_anchor"][:160] if an else "")), "Placement / Context": "Natural in-body mention where the topic arises; CTA targets per calendar CTA_direction",
                "Purpose": "Calendar internal_link_targets for " + r["Row ID"], "Stage 16 Priority": "n/a (calendar)", "Step 2 Priority": "MEDIUM" if tid.startswith(("EDU", "COM")) else "LOW",
                "Required At Launch": "BLOG-HUB: YES" if tid == "BLOG-HUB" else "NO", "Present In Live HTML?": "n/a (post not live)", "Destination Ownership Flag": conf,
                "Ranking-Equity Note": "", "AWS Class": "A", "Origin": "STEP 2 — final calendar internal_link_targets",
                "Notes": "do not invent URLs: destination URL as resolved" + ("; destination not live yet — conditional link" if ds.startswith(("PLANNED", "CONDITIONAL")) else "")})

    # --- Step 2A additions: links created by the resolutions (new/re-homed Education pages; OD-04, OD-12, OD-13)
    ADD = [
     ("EDU-ROOT", "EDU-WB-TYPES", "types of wedding rings, explained", "HUB_TO_CHILD", "RECOMMENDED", "Education index lists the re-homed style catalog (OD-04)."),
     ("EDU-ROOT", "EDU-WB-GUIDE", "how to choose a wedding band", "HUB_TO_CHILD", "RECOMMENDED", "Education index lists the buying guide."),
     ("EDU-ROOT", "EDU-RJG-BR", "bracelet size chart", "HUB_TO_CHILD", "RECOMMENDED", "Sizing reference listed under Ring & Jewelry Guides."),
     ("EDU-ROOT", "EDU-RJG-NL", "necklace length chart", "HUB_TO_CHILD", "RECOMMENDED", "Sizing reference listed under Ring & Jewelry Guides."),
     ("EDU-WB-TYPES", "EDU-WB-GUIDE", "how to choose a wedding band", "CHILD_TO_RELATED_CHILD", "REQUIRED", "Boundary: styles here, buying decision there; ship together."),
     ("EDU-WB-GUIDE", "EDU-WB-TYPES", "the main wedding band styles", "CHILD_TO_RELATED_CHILD", "REQUIRED", "Boundary link; ship together."),
     ("EDU-WB-TYPES", "COM-WB", "browse diamond wedding bands", "EDUCATION_TO_CATEGORY", "RECOMMENDED", "Decision-point exit (Stage 16 §3.1)."),
     ("EDU-WB-TYPES", "SUB:/wedding-bands/for-her/eternity", "eternity bands", "EDUCATION_TO_CATEGORY", "OPTIONAL", "One-home for eternity commercial intent (OD-16)."),
     ("EDU-WB-GUIDE", "COM-WB", "browse diamond wedding bands", "EDUCATION_TO_CATEGORY", "RECOMMENDED", "Decision-point exit."),
     ("COM-WB", "EDU-WB-GUIDE", "how to choose a wedding band", "CATEGORY_TO_EDUCATION", "RECOMMENDED", "Category copy: one sentence + link; counts toward the ≤5 Education links."),
     ("BC-037", "EDU-WB-TYPES", "the types of wedding rings", "BLOG_TO_EDUCATION", "RECOMMENDED", "Blog posts link to the single Education owner."),
     ("BC-007", "EDU-WB-TYPES", "wedding band styles", "BLOG_TO_EDUCATION", "RECOMMENDED", "Blog posts link to the single Education owner."),
     ("BC-022", "EDU-WB-TYPES", "wedding band styles", "BLOG_TO_EDUCATION", "RECOMMENDED", "Blog posts link to the single Education owner."),
     ("BC-023", "EDU-WB-TYPES", "eternity and other band styles", "BLOG_TO_EDUCATION", "OPTIONAL", "Eternity meaning stays Blog; styles live in Education."),
     ("EDU-RJG-BR", "COM-FJ-BRACELETS", "browse diamond bracelets", "EDUCATION_TO_CATEGORY", "RECOMMENDED", "Decision-point exit."),
     ("EDU-RJG-BR", "SUB:/fine-jewellery/bracelet/tennis", "tennis bracelets", "EDUCATION_TO_CATEGORY", "RECOMMENDED", "Sizing page for tennis bracelets (calendar title)."),
     ("COM-FJ-BRACELETS", "EDU-RJG-BR", "how to measure your wrist", "CATEGORY_TO_EDUCATION", "RECOMMENDED", "Category intro link."),
     ("SUB:/fine-jewellery/bracelet/tennis", "EDU-RJG-BR", "bracelet size chart", "CATEGORY_TO_EDUCATION", "RECOMMENDED", "Subcategory intro link."),
     ("EDU-RJG-NL", "COM-FJ-NECKLACES", "browse diamond necklaces and pendants", "EDUCATION_TO_CATEGORY", "RECOMMENDED", "Decision-point exit."),
     ("COM-FJ-NECKLACES", "EDU-RJG-NL", "necklace length chart", "CATEGORY_TO_EDUCATION", "RECOMMENDED", "Category intro link."),
     ("BC-006", "EDU-RJG-NL", "necklace length chart", "BLOG_TO_EDUCATION", "RECOMMENDED", "Layering = styling (Blog); lengths = sizing reference (Education)."),
     ("EDU-INS", "BC-024", "how much an engagement ring costs", "EDUCATION_TO_BLOG", "OPTIONAL", "Cost PAA is owned by BC-024."),
     ("EDU-INS", "COM-ER", "browse engagement rings", "EDUCATION_TO_CATEGORY", "OPTIONAL", "Single optional exit; no HOD insurance/appraisal service claim (F-E5)."),
     ("EDU-RJG-03", "EDU-RJG-02", "ring size guide", "CHILD_TO_RELATED_CHILD", "OPTIONAL", "Related ring guide."),
     ("EDU-RJG-03", "COM-ER", "browse engagement rings", "EDUCATION_TO_CATEGORY", "OPTIONAL", "Single optional exit; no cleaning-service claim (F-E5)."),
     ("EDU-ROOT", "EXIST-BLOG-ER-ONLINE", "buying a lab-grown engagement ring online", "HUB_TO_CHILD_TRANSITIONAL", "OPTIONAL", "OD-13: transitional listing; article retained unchanged."),
     ("SUB:/wedding-bands/for-her", "COM-WB", "wedding bands", "CHILD_TO_HUB", "REQUIRED", "Canonical target; breadcrumb parent."),
     ("COM-ER-STYLES-GROUP", "COM-ER", "engagement rings", "CHILD_TO_HUB", "REQUIRED", "Canonical target (OD-06)."),
    ]
    k2 = 0
    for src, dst, anc_, rel, pr, why in ADD:
        su, ss, sr = resolve(src, by, alias)
        du, ds, dr = resolve(dst, by, alias)
        if src in ("BC-037", "BC-007", "BC-022", "BC-023", "BC-006"):
            pass
        k2 += 1
        sid = "EDU-WB-TYPES" if src == "BLOG-WR-TYPES" else src
        out.append({
            "Link ID": "L2A-%03d" % k2, "Source ID": sid, "Source URL": su, "Source Status": ss, "Destination ID": dst, "Destination URL": du, "Destination Status": ds,
            "Link Type": "CONTEXTUAL", "Relationship": rel, "Recommended Anchor": anc_, "Anchor Variants": "", "Avoid Anchor": "",
            "Placement / Context": "Natural in-body/intro placement; descriptive anchor", "Purpose": why, "Stage 16 Priority": "n/a (Step 2A addition)",
            "Step 2 Priority": {"REQUIRED": "HIGH", "RECOMMENDED": "MEDIUM", "OPTIONAL": "LOW"}[pr], "Required At Launch": "YES" if pr == "REQUIRED" else "NO",
            "Present In Live HTML?": "n/a (new link)", "Destination Ownership Flag": unresolved_flag(dr), "Ranking-Equity Note": "",
            "AWS Class": "A" if not ss.startswith("LIVE") else "B", "Origin": "STEP 2A — resolution addition (2026-10-10)",
            "Notes": "destination not live yet — conditional link" if ds.startswith(("PLANNED", "CONDITIONAL")) else ""})

    return out


def pdp_rows():
    prods = {x["URL"]: x for x in PDP}
    spec = {
     "cushion-solitaire-studs": ("Cushion Solitaire Stud Earrings, 3.00 ct", "Cushion cut solitaire stud earrings, each with a 1.50 ct diamond in an eight-prong setting (3.00 ct total). Available in 10K or 14K gold."),
     "princess-halo-stud-earrings": ("Princess Halo Diamond Stud Earrings, 2.32 ct", "Princess cut diamond stud earrings with a round pavé halo: about 1 ct per center stone and 2.32 ct total weight. Available in 10K or 14K gold."),
     "radiant-halo-drops": ("Radiant Halo Diamond Drop Earrings, 2.52 ct", "Radiant cut diamond drop earrings with a pavé halo and a pavé lever back, 2.52 ct total weight. Available in 10K or 14K gold."),
     "round-hoop-drops": ("Round Diamond Hoop Drop Earrings, 4.00 ct", "Round brilliant diamond drops hanging from a slim hoop, 4.00 ct total weight (2.00 ct per ear). Available in 10K or 14K gold."),
     "round-radiant-drops": ("Round & Radiant Diamond Drop Earrings, 3.66 ct", "Drop earrings pairing a round brilliant top stone with a radiant cut drop diamond, 3.66 ct total weight. Available in 10K or 14K gold."),
     "round-solitaire-studs": ("Round Solitaire Diamond Stud Earrings, 4.00 ct", "Round brilliant solitaire stud earrings, 4.00 ct total weight (2.00 ct per ear), in an eight-prong black rhodium finish. Available in 10K or 14K gold."),
     "aurelia-round-solitaire-diamond-pendant": ("2.00 ct Round Diamond Solitaire Pendant, Circular Bail", "A 2.00 ct round diamond solitaire pendant in an open four-prong setting with a polished circular bail and open gallery. Available in 10K or 14K gold."),
     "elyra-round-solitaire-diamond-pendant": ("2.00 ct Round Diamond Solitaire Pendant, Split Bail", "A 2.00 ct round diamond solitaire pendant in a classic four-prong setting with a polished split bail. Available in 10K or 14K gold."),
    }
    out = []
    seen = set()
    for u, p in prods.items():
        slug = u.split("/shop/")[1]
        fl = p["Flags"]
        if not any(k in fl for k in ("placeholder", "duplicate", "numeric", "Vermil", "meta>160")) and slug != "oval-floral-diamond-ring":
            continue
        issues = [f.strip() for f in fl.split(";") if f.strip() and f.strip() not in ("title>60",)]
        if "title>60" in fl:
            issues.append("title>60 (rendered)")
        rt, rm = spec.get(slug, ("", ""))
        if "numeric-ID/copy slug" in fl:
            act = "KEEP URL; unique carat-specific title/meta already; decide variant consolidation (OD-14); never delete without 301"
            pr = "MEDIUM"
        elif "placeholder-style meta" in fl:
            act = "REPLACE title + meta from the product record (fact-check specs); H1/name unchanged"
            pr = "HIGH"
        elif "duplicate title" in fl:
            act = "DIFFERENTIATE title (bail style) — two products share one title"
            pr = "HIGH"
        elif "Vermil" in fl:
            act = "FIX material label in product data ('18K Gold Vermil' → verify; likely vermeil); correct schema material; add carat/stone specs to title if available"
            pr = "MEDIUM"
        elif "meta>160" in fl:
            act = "TRIM meta to ≤155 chars at a sentence boundary"
            pr = "LOW"
        else:
            act = "see COM-PDP-OVAL-FLORAL row in 01"
            pr = "MEDIUM"
        out.append({"URL": u.replace(SITE, ""), "Product (H1)": p["H1"], "Category": p["Schema category"], "Material (schema)": p["Material (schema)"], "Price (schema, USD)": p["Price (schema)"],
                    "Issues (QA/06 flags)": "; ".join(issues), "Current Title": p["Title"], "Recommended Title (pre-suffix)": rt, "Current Meta": p["Meta description"],
                    "Recommended Meta (DRAFT — fact-check vs product record)": rm, "Action": act, "Priority": pr, "AWS Class": "B",
                    "Notes": ("Product description on the page says 'IGI certified GH / VVS' — claim unverified (OD-08); NOT repeated in the draft meta." if slug in spec else "")})
    # oval floral
    for o in out:
        if o["URL"].endswith("oval-floral-diamond-ring"):
            o["Recommended Title (pre-suffix)"] = "2.5 ct Oval Marquise Diamond Engagement Ring"
            o["Recommended Meta (DRAFT — fact-check vs product record)"] = "Oval engagement ring with a 2.5 ct oval lab-grown center diamond and 16 marquise side stones in a raised four-prong setting, available in 10K and 14K gold."
            o["Issues (QA/06 flags)"] = "Stage 15 ranking PDP; JSON-LD name ≠ H1; sku UUID ≠ visible SKU; title lead term 'Side-Stone'"
            o["Priority"] = "MEDIUM"
    if not any(o["URL"].endswith("oval-floral-diamond-ring") for o in out):
        out.append({"URL": "/shop/oval-floral-diamond-ring", "Product (H1)": "Oval Marquise Side-Stone Engagement Ring", "Category": "Engagement Rings", "Material (schema)": "10K Yellow Gold (+ other metals listed)",
                    "Price (schema, USD)": "1675", "Issues (QA/06 flags)": "Stage 15 ranking PDP; JSON-LD name 'Oval Floral Diamond Ring' ≠ H1; sku UUID ≠ visible SKU RG038993; title lead term 'Side-Stone'",
                    "Current Title": "Oval Marquise Side-Stone Engagement Ring | House of Diams", "Recommended Title (pre-suffix)": "2.5 ct Oval Marquise Diamond Engagement Ring",
                    "Current Meta": "Shop an oval side-stone engagement ring with a 2.500 ct center diamond, 16 marquise accents, and a raised four-prong setting.",
                    "Recommended Meta (DRAFT — fact-check vs product record)": "Oval engagement ring with a 2.5 ct oval lab-grown center diamond and 16 marquise side stones in a raised four-prong setting, available in 10K and 14K gold.",
                    "Action": "Replace title/meta (GSC baseline first); align H1 and schema name; keep slug", "Priority": "MEDIUM", "AWS Class": "B", "Notes": "OD-15"})
    order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    out.sort(key=lambda o: (order[o["Priority"]], o["URL"]))
    return out
