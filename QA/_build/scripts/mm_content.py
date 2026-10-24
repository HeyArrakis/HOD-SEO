"""Hubs (/blog, /education), existing Education-owned articles, planned/conditional Education pages, calendar blog rows."""
import re, json, collections, csv
import lib_research as L
from mm_core import *
import mm_helpers as H
from mm_live import base_row, finish, kwc, link_gap_text, SRC_COMMON, D19

SRC_EDU = ("Live crawl 2026-10-09; architecture/15_keyword_url_map.csv + 15_target_page_registry.csv; content-strategy/17_topic_intelligence.csv; 18_question_coverage.csv; 18_entity_coverage.csv; "
           "19_brief_registry.csv; architecture/16_page_link_requirements.csv; 16_anchor_strategy.csv; FINAL-BLOG-CALENDAR/BLOG_CALENDAR_FINAL.csv")
edu_arch = {x["topic_id"]: x for x in L.rd("architecture/14_education_architecture.csv")}

PRIO_CAL = {"MUST_PUBLISH": "CRITICAL", "HIGH": "HIGH", "NORMAL": "MEDIUM", "FLEXIBLE": "LOW"}
TODAY = "2026-10-09"


# ---------------------------------------------------------------- hubs
def hub_rows():
    rows = []
    # /blog
    r = base_row("/blog", "HUBS", "BLOG-HUB", "Blog hub (live label: Blog / Stories / Journal)", "BLOG_HUB", "Blog / Journal", "Hub (editorial index)")
    r["Primary Keyword"] = "NO PRIMARY KEYWORD — HUB INDEX (owns no Stage 15 keyword)"; r["Search Intent"] = "NAVIGATIONAL / browse"; r["Keyword Owner"] = "BLOG-HUB — none"
    r["Existing Keyword Ownership Conflict?"] = "NO"; r["Cannibalization Risk"] = "LOW"
    r["Recommended SEO Title"] = "Journal | Diamond Jewellery Guides, Gift Ideas & Style | House of Diams"
    r["Recommended Meta Description"] = "Guides, gift ideas and style advice from House of Diams: engagement rings, anniversary gifts, jewellery care and the craft behind diamond jewellery."
    r["Recommended H1"] = "The House of Diams Journal"
    r["Recommended Content/Section Changes"] = ("Naming is inconsistent (nav 'Blog', H1 'Stories from House of Diams', blog drafts say 'Back to Journal', IA says 'Blog / Journal') — pick one. "
        "Pagination: /blog?page=2 canonicalises to /blog (not self-canonical), so posts beyond page 1 may be discoverable only via the sitemap/in-content links; with ~34 Blog + ~28 Education posts planned, confirm the pagination/canonical policy (or add category hub pages per Stage 13 §5: Craft, Style, Gifts, Launches, Industry). "
        "Education-owned articles currently sit under /blog (10 of 11 live articles) — the hub must stay the index for them until the Education migration conditions are met.")
    r["Recommended Image/Alt-Text Changes"] = "Card images: alt text = article topic, not 'Featured Projects'."
    r["Recommended Internal Links IN"] = H.link_summary("BLOG-HUB", "in"); r["Recommended Internal Links OUT"] = H.link_summary("BLOG-HUB", "out")
    r["Recommended Anchor Context"] = "Article titles as card anchors."; r["Internal-Link Priority"] = "HIGH (every post must be linked from the hub — Stage 16 REQUIRED)"
    r["Recommended Schema"] = "Blog (optional) + BreadcrumbList; ItemList not needed."; r["Schema Validation/Review Needed?"] = "LOW"
    r["AEO Opportunity"] = "NONE"; r["GEO/AI Search Opportunity"] = "Author/publisher consistency: bylines vary ('House of Diams Jewellery Team', 'Krish Babriya, Co-founder') — define an author policy."
    r["Important Entities"] = "House of Diams Journal; article categories"; r["Entity Clarity Needed?"] = "YES (author naming)"
    r["Recommended Action"] = "OPTIMIZE"; r["Priority"] = "MEDIUM"; r["Implementation Dependency"] = "Template/code (pagination, category pages)"
    r["Status"] = "LIVE — NEEDS OPTIMIZATION"; r["Evidence / Source"] = SRC_COMMON + "; 13_blog_strategy.md"; r["Notes"] = "Lists the 10 current /blog articles + 1 Education article cross-listed? — VERIFY. No new calendar posts are live as of 2026-10-09."
    rows.append(finish(r, dict(meta=1, h1=1, links=1, geo=1), a=["naming decision", "metadata drafts"], b=["pagination canonical / category pages"], c=["canonical on ?page=N, sitemap, status"]))

    # /education
    r = base_row("/education", "HUBS", "EDU-ROOT", "Education hub (root index)", "EDUCATION_HUB", "Education", "Hub/Cornerstone (root index)")
    r["Primary Keyword"] = "NO PRIMARY KEYWORD — ROOT INDEX (owns no Stage 15 keyword)"; r["Search Intent"] = "NAVIGATIONAL / informational browse"; r["Keyword Owner"] = "EDU-ROOT — none"
    r["Existing Keyword Ownership Conflict?"] = "NO"; r["Cannibalization Risk"] = "LOW"
    r["Recommended SEO Title"] = "Diamond & Jewellery Guide: Lab-Grown Diamonds, 4Cs, Metals & More | House of Diams"
    r["Recommended Meta Description"] = "Plain-English guides to lab-grown diamonds, the 4Cs, certification, metals and ring care from House of Diams."
    r["Recommended H1"] = "Diamond & Jewellery Education"
    r["Recommended Content/Section Changes"] = ("Hub lists 1 article today (GIA vs IGI) although 10 more Education-owned articles live at /blog. Per Stage 14 the root index should list the eight topic hubs (Lab-Grown, Natural, 4Cs, Shapes, Certification, Metals, Ring & Jewellery Guides, root-level Diamond properties). "
        "H2 on the page is the article's own <title> string including '| House of Diams' — template bug. Do NOT move existing /blog URLs without the Stage 13 migration conditions.")
    r["Recommended Internal Links IN"] = H.link_summary("EDU-ROOT", "in"); r["Recommended Internal Links OUT"] = H.link_summary("EDU-ROOT", "out") + " || " + link_gap_text("EDU-ROOT", "/education")
    r["Recommended Anchor Context"] = "Hub names per 16_anchor_strategy (e.g. 'Lab-Grown Diamond Guide')."; r["Internal-Link Priority"] = "HIGH"
    r["Recommended Schema"] = "CollectionPage/WebPage + BreadcrumbList; optional."; r["Schema Validation/Review Needed?"] = "LOW"
    r["AEO Opportunity"] = "NONE (index)"; r["GEO/AI Search Opportunity"] = "Strong topical-structure signal for AI systems once the eight hubs exist."
    r["Important Entities"] = "Lab-grown diamond; natural diamond; 4Cs; certification (IGI/GIA); metals"; r["Entity Clarity Needed?"] = "NO"
    r["Recommended Action"] = "EXPAND"; r["Priority"] = "HIGH"; r["Implementation Dependency"] = "Education hubs/pillars must exist (calendar: EDU-LG-00 on 2026-10-21, etc.)"
    r["Status"] = "LIVE — THIN INDEX"; r["Evidence / Source"] = SRC_COMMON + "; 14_education_hierarchy.csv"; r["Notes"] = "Stage 1/10 also saw 1 article."
    rows.append(finish(r, dict(meta=1, links=1), a=["hub listing plan"], b=["template: hub listing logic, H2 bug"], c=["canonical, links to hubs, sitemap"]))
    return rows


# ---------------------------------------------------------------- existing articles
EXIST = {
    "/blog/cvd-vs-hpht-lab-grown-diamonds-what-buyers-should-know-house-of-diams": dict(tid="EDU-LG-03", action="OPTIMIZE", prio="HIGH", status="LIVE — PROTECT (19 ranked keywords)",
        title="CVD vs HPHT Lab-Grown Diamonds: Which Is Better?", h1="CVD vs HPHT Lab-Grown Diamonds: How They Differ and Which Is Better",
        meta="CVD and HPHT are the two main ways lab-grown diamonds are made. Both produce real diamonds — here is how the methods differ and what matters when you buy."),
    "/blog/lab-grown-vs-natural-diamonds-the-honest-comparison-house-of-diams": dict(tid="EDU-LG-02", action="OPTIMIZE", prio="HIGH", status="LIVE — PROTECT (3 ranked keywords)",
        title="Lab-Grown vs Natural Diamonds: The Honest Comparison", h1="Lab-Grown vs Natural Diamonds: The Honest Comparison",
        meta="Lab-grown and natural diamonds are both real diamonds. Compare origin, price, quality and long-term value before you choose."),
    "/blog/14k-vs-18k-gold-for-diamond-jewellery-which-is-better-house-of-diams": dict(tid="EDU-MET-01", action="OPTIMIZE", prio="MEDIUM", status="LIVE — PROTECT (3 ranked keywords)",
        title="14K vs 18K Gold (and 10K): Which Is Better?", h1="14K vs 18K Gold (and 10K) for Diamond Jewelry: Which Is Better?",
        meta="14K gold is about 58% pure gold and 18K about 75%. Compare colour, durability and value to choose the right gold for diamond jewelry."),
    "/blog/how-to-choose-a-lab-grown-diamond-the-complete-buyer-s-guide": dict(tid="EDU-LG-10", action="OPTIMIZE", prio="MEDIUM", status="LIVE — KEEP (migration deferred)",
        title="How to Choose a Lab-Grown Diamond: Buyer's Guide", h1="How to Choose a Lab-Grown Diamond: The Complete Buyer's Guide",
        meta="How to choose a lab-grown diamond: which of cut, colour, clarity and carat matter most, why certification matters and the mistakes to avoid."),
    "/blog/are-lab-grown-diamonds-real-a-complete-buyer-s-guide": dict(tid="EDU-LG-01", action="OPTIMIZE", prio="HIGH", status="LIVE — NEEDS OPTIMIZATION",
        title="Are Lab-Grown Diamonds Real? The Short Answer", h1="Are Lab-Grown Diamonds Real? The Short Answer and How to Verify One",
        meta="Yes — lab-grown diamonds are real diamonds with the same carbon crystal structure as mined stones. How they differ from simulants and how to verify one."),
    "/blog/the-4cs-of-lab-grown-diamonds-explained-cut-colour-clarity-and-carat-house-of-diams": dict(tid="EDU-4C-00", action="OPTIMIZE", prio="HIGH", status="LIVE — NEEDS OPTIMIZATION (pillar refresh scheduled)",
        title="The 4Cs of Diamonds: Cut, Color, Clarity & Carat", h1="The 4Cs of Diamonds Explained: Cut, Color, Clarity and Carat",
        meta="The 4Cs — cut, color, clarity and carat — explained, including how lab-grown diamonds are graded and which C matters most for how a diamond looks."),
    "/blog/how-to-choose-a-lab-grown-diamond-engagement-ring-online-house-of-diams": dict(tid="EXIST-BLOG-ER-ONLINE", action="REVIEW", prio="MEDIUM", status="LIVE — DEFERRED (overlap with LG-10 / 4Cs)",
        title="No change until the DEFER decision (EDU-RJG-04) is made", h1="—",
        meta="—"),
    "/blog/the-best-lab-grown-diamond-shapes-for-engagement-rings-house-of-diams": dict(tid="EDU-SHP-00", action="OPTIMIZE", prio="HIGH", status="LIVE — NEEDS OPTIMIZATION (pillar refresh scheduled)",
        title="Diamond Shapes Guide: 10 Shapes and How to Choose", h1="Diamond Shapes Guide: The 10 Main Shapes and How to Choose One",
        meta="Compare the main diamond shapes — round, oval, pear, emerald, cushion and more — and how shape affects sparkle, apparent size and price in a ring."),
    "/blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-house-of-diams": dict(tid="EDU-RJG-02", action="OPTIMIZE", prio="HIGH", status="LIVE — NEEDS OPTIMIZATION (refresh scheduled; 165,000/mo head)",
        title="Ring Size Guide: Chart and How to Measure at Home", h1="Ring Size Guide: Ring Size Chart and How to Measure Your Size at Home",
        meta="Find your ring size at home: measure an existing ring or your finger, use our ring size chart, and learn when to size up or down."),
    "/blog/igi-certification-for-lab-grown-diamonds-what-it-means-house-of-diams": dict(tid="EDU-CERT-00", action="OPTIMIZE", prio="HIGH", status="LIVE — RETARGET (OV-01 overlap)",
        title="Lab-Grown Diamond Certification: What the Report Shows", h1="Lab-Grown Diamond Certification Explained: What an IGI or GIA Report Shows",
        meta="What a lab-grown diamond certificate (IGI or GIA report) shows, why it matters and how to verify it before you buy."),
    "/education/lab-grown-diamond-certification-explained-gia-vs-igi-house-of-diams": dict(tid="EDU-CERT-01", action="OPTIMIZE", prio="MEDIUM", status="LIVE — KEEP (OV-01 partner)",
        title="GIA vs IGI Lab-Grown Diamond Certification", h1="GIA vs IGI: What Your Lab-Grown Diamond Report Means",
        meta="GIA vs IGI for lab-grown diamonds: what each report shows, how their grading approaches differ and how to verify a report number."),
}


def gap_text(tid, n=4):
    out = []
    for g in L.gaps.get(tid, []):
        if g["gap_severity"] == "CRITICAL_COVERAGE":
            out.append(f"{g['concept']} [{g['recommended_treatment']}]")
    return "; ".join(out[:n])


def existing_rows():
    rows = []
    for path, d in EXIST.items():
        tid = d["tid"]
        reg = L.registry.get(tid)
        is_er_online = tid == "EXIST-BLOG-ER-ONLINE"
        t = L.topic.get(tid, {}); b = L.brief.get(tid, {})
        dec = L.existing_decisions.get(path, {}); a = H.ART.get(path, {})
        r = base_row(path, "EXISTING ARTICLES (Education-owned)", tid, (reg["target_page_name"] if reg else "How to choose a lab-grown diamond engagement ring online (existing, deferred)"),
                     "BLOG_ARTICLE (Education-owned)" if path.startswith("/blog") else "EDUCATION_ARTICLE", (reg["hub"] if reg else "Engagement Rings / Diamond Buying"),
                     "Informational (Education evergreen)" if not is_er_online else "Informational / commercial-research (deferred)")
        if reg:
            r["Primary Keyword"] = (b.get("primary_keyword") or t.get("primary_keyword") or "") + f"  [Stage 19 brief primary; Stage 15 owner of {reg['keyword_count']} keywords, highest-volume: {reg['highest_search_volume']}]"
            r["Secondary Keywords"] = "; ".join(L.split_list(b.get("secondary_keywords", ""))[:8])
        else:
            r["Primary Keyword"] = "NO STAGE 15 OWNER (existing article, Stage 13 DEFER; intended destination EDU-RJG-04 is DEFERRED)"
            r["Secondary Keywords"] = "—"
        r["Related/Semantic Concepts"] = "; ".join(H.L.req_concepts(tid, 8)) or "—"
        r["Search Intent"] = (t.get("primary_intent", "INFORMATIONAL") + " | SERP: " + t.get("dominant_serp_type", "n/a")) if t else "INFORMATIONAL (buying guidance)"
        r["Keyword Owner"] = f"{tid} (Stage 15)" if reg else "none (deferred)"
        pairs = H.pairs_for(tid)
        cal = L.cal_by_id.get(tid)
        conflict = []
        if cal and b and cal["primary_keyword"].strip().lower() != b.get("primary_keyword", "").split(";")[0].replace("co-primary:", "").strip().lower():
            conflict.append(f"Primary keyword differs by source: Stage 17/19 = '{b.get('primary_keyword','').split(' | ')[0]}'; final calendar = '{cal['primary_keyword']}' ({cal['primary_search_volume']}/mo). Both map to the same page; calendar primary is {'in Stage 15 map' if cal['primary_keyword'].strip().lower() in L.kmap else 'NOT in the Stage 15 keyword map (new research)'}.")
        r["Existing Keyword Ownership Conflict?"] = ("YES — " + " ".join(conflict)) if conflict else ("NO" if reg else "REVIEW — overlap with EDU-LG-10/EDU-4C-00 (Stage 10: buying-guide intent covered 3×)")
        r["Cannibalization Risk"] = (reg["cannibalization_risk"] if reg else "MEDIUM") + ((" — pairs: " + "; ".join(pairs)) if pairs else "")
        r.update({k: v for k, v in cur_fields(path).items()})
        r["Recommended SEO Title"] = d["title"]; r["Recommended Meta Description"] = d["meta"]; r["Recommended H1"] = d["h1"]
        # content changes
        ent = H.entity_presence(tid, path) if reg else None
        qp = H.question_presence(tid, path) if reg else None
        parts = []
        if dec:
            parts.append(f"Stage 13 decision: {dec['action']} — {dec['proposed_role'][:140]}.")
        if cal:
            parts.append(f"Calendar refresh {cal['publish_date']} ({cal['status']}): {cal['working_title'][:140]}")
        if ent and ent[1]:
            parts.append("Required entities NOT found in page text (heuristic match, VERIFY): " + "; ".join(ent[1][:8]))
        if qp and qp[1]:
            parts.append(f"Stage 17/18 questions likely NOT covered by headings/body (heuristic, VERIFY; {len(qp[1])} of {len(qp[0])+len(qp[1])} checked): " + "; ".join(qp[1][:5]))
        g = gap_text(tid)
        if g:
            parts.append("Stage 18 CRITICAL gaps to confirm in body: " + g)
        if not reg:
            parts.append("Overlaps the lab-grown buying guide and the 4Cs article; decide survivor/consolidation under EDU-RJG-04 before editing. Do not consolidate automatically.")
        parts.append(f"Do NOT change URL; keep H1 core keywords; baseline GSC before editing. Page word count ≈ {a.get('words','?')}.")
        r["Recommended Content/Section Changes"] = " ".join(parts)
        r["Recommended Image/Alt-Text Changes"] = "Add alt text describing each diagram/image; replace generic 'Featured Projects' module labels. Add comparison/table visuals where Stage 19 brief specifies."
        r["Recommended Internal Links IN"] = H.link_summary(tid, "in")
        r["Recommended Internal Links OUT"] = H.link_summary(tid, "out") + " || " + (("Stage 16 REQUIRED outgoing links to live pages not found in page HTML: " + ", ".join(H.disp(x) for x in H.missing_required_out(tid, a.get("links_all", []), path)[0])) if a and H.missing_required_out(tid, a.get("links_all", []), path)[0] else "required live outgoing links present or n/a")
        r["Recommended Anchor Context"] = H.anchor_ctx(tid) if reg else "Descriptive anchors; follow 16_anchor_strategy for related targets."
        r["Internal-Link Priority"] = "HIGH" if reg and tid in ("EDU-LG-03", "EDU-LG-02", "EDU-4C-00", "EDU-CERT-00", "EDU-SHP-00", "EDU-RJG-02") else "MEDIUM"
        r["Recommended Schema"] = "Article/BlogPosting (current) + BreadcrumbList (missing); named Person author with real credentials OR Organization; keep ISO dates; NO FAQPage/HowTo (no rich results)."
        au = re.findall(r'"name":"([^"]+)"', (a.get("author") or [""])[0]) if a else []
        r["Current Schema"] = r["Current Schema"] + f" | author in schema: {au[0] if au else '?'}; datePublished {a['ld_dates'][0][1][:10] if a.get('ld_dates') else '?'}, dateModified {a['ld_dates'][1][1][:10] if a.get('ld_dates') and len(a['ld_dates'])>1 else '?'}"
        r["Schema Validation/Review Needed?"] = "YES — add BreadcrumbList; reconcile author entity (names vary); validate after AWS."
        qs = H.L.top_questions(tid, 5) if reg else []
        r["AEO Opportunity"] = "HIGH" if reg and tid in ("EDU-LG-01", "EDU-LG-02", "EDU-LG-03", "EDU-4C-00", "EDU-SHP-00", "EDU-RJG-02", "EDU-MET-01") else "MEDIUM"
        r["Primary Questions to Answer"] = "; ".join(qs) or "Which route to buy online? (deferred)"
        r["Answer-First Opportunity"] = (b.get("serp_format") or "Direct answer in first paragraph, then comparison table/steps per Stage 19 brief")[:200]
        qc = H.L.q_status_counts(tid) if reg else {}
        r["PAA/Question Coverage Needed?"] = ("YES — Stage 18 statuses: " + ", ".join(f"{k}={v}" for k, v in qc.items())) if qc else "REVIEW"
        r["GEO/AI Search Opportunity"] = "Entity-clear definitions + comparison table + dated update + cited authority (GIA/IGI) make the page quotable by AI answers."
        r["Important Entities"] = "; ".join(H.L.entities(tid, 8)) or "lab-grown diamond; natural diamond; certification"
        r["Entity Clarity Needed?"] = ("YES — " + str(len(ent[1])) + " required entities not detected in page text (heuristic)") if ent and ent[1] else (f"LOW — all {len(ent[0])} required entities detected in page text (heuristic; clarity of definitions not assessed)" if ent else "VERIFY")
        r["Brand/Expertise/Trust Signal Opportunity"] = "Add a reviewer/author with verifiable trade experience (About: family-run manufacturer, in trade since 2014 — confirm), 'last updated' date and sources; avoid unverifiable claims."
        r["Recommended Action"] = d["action"]; r["Priority"] = d["prio"]
        r["Implementation Dependency"] = "CMS access; Stage 19 brief; business facts " + ("(" + "; ".join(x["fact"][:60] for x in L.bizfacts.get(tid, [])[:2]) + ")" if L.bizfacts.get(tid) else "(none)")
        r["Status"] = d["status"]
        eq = H.ranking_equity(path)
        r["Evidence / Source"] = SRC_EDU + "; content-strategy/13_existing_content_decisions.csv; 15_ranking_equity_protection.csv"
        r["Notes"] = (f"Ranking equity: {eq}. " if eq else "No Stage 3 ranking keywords. ") + (f"Planned destination: {reg['proposed_url']}  (move only when Stage 13 conditions are met; 1:1 301)." if reg and reg['proposed_url'] and reg['proposed_url'] not in ('(stays at existing URL)', 'URL_PENDING') else "") + " CMS content store (Supabase) is in the AWS migration — publish/edit timing must follow the migration content-freeze plan (UNKNOWN — VERIFY)."
        gsc_na(r)
        rows.append(finish(r, dict(meta=d["action"] == "OPTIMIZE", h1=d["action"] == "OPTIMIZE", links=1, schema=1, aeo=1, geo=1, conflict=bool(conflict), cannib=bool(pairs) or not reg),
                           a=["metadata + content update drafts (Stage 19 brief)", "link additions"], b=["BreadcrumbList/author schema template", "any URL move"], c=["canonical, indexability, schema, CWV, internal links render"]))
    return rows


# ---------------------------------------------------------------- planned / conditional education rows
def pretty_title(wt):
    s = re.sub(r"\s*\([^)]*\)", "", wt).strip()
    head = s.split("?")[0] + "?" if "?" in s.split(":")[0] else s.split(":")[0]
    head = head.strip().rstrip(".")
    words = head.split()
    small = {"a", "an", "the", "and", "or", "of", "to", "in", "for", "vs", "on", "is", "at"}
    out = []
    for i, w in enumerate(words):
        out.append(w if (w.lower() in small and i) else (w[0].upper() + w[1:] if w[0].isalpha() else w))
    return " ".join(out)


def planned_edu_rows():
    rows = []
    existing_ids = {d["tid"] for d in EXIST.values()}
    calendar_edu_extra = {"EDU-RJG-BR": ("Bracelet size chart (planned Education practical guide)", "EDUCATION_PRACTICAL_GUIDE", "Ring & Jewellery Guides"),
                          "EDU-RJG-NL": ("Necklace length chart (planned Education practical guide)", "EDUCATION_PRACTICAL_GUIDE", "Ring & Jewellery Guides"),
                          "EDU-INS": ("Engagement ring insurance (planned Education guide)", "EDUCATION_PRACTICAL_GUIDE", "Ring & Jewellery Guides"),
                          "EDU-WB-GUIDE": ("How to choose a wedding band (planned Education buying guide)", "EDUCATION_BUYING_GUIDE", "Ring & Jewellery Guides")}
    ids = []
    for tid, rg in L.registry.items():
        if tid.startswith("EDU-") and tid not in existing_ids and tid not in ("EDU-CERT-01",):
            ids.append(tid)
    for tid in ("EDU-RJG-00", "EDU-RJG-03", "EDU-LG-04", "EDU-LG-06", "EDU-NAT-01", "EDU-NAT-02", "EDU-4C-04", "EDU-4C-08", "EDU-CERT-02", "EDU-MET-02", "EDU-GEM-00", "EDU-GEM-01", "EDU-GEM-02", "EDU-GEN-02"):
        if tid not in ids:
            ids.append(tid)
    ids += list(calendar_edu_extra)
    for tid in ids:
        reg = L.registry.get(tid); ea = edu_arch.get(tid); cal = L.cal_by_id.get(tid); b = L.brief.get(tid, {}); t = L.topic.get(tid, {})
        if reg:
            name, ptype, hub = reg["target_page_name"], reg["page_type"], reg["hub"]
            url = reg["proposed_url"] if reg["proposed_url"] and reg["proposed_url"] != "URL_PENDING" else "PLANNED — URL PENDING (slug not decided)"
            status_arch = reg["status"]
        elif ea:
            name, ptype, hub = ea["topic_name"], ea["proposed_page_type"], ea["education_hub"]; url = "NOT PLANNED — conditional/deferred (no URL)"; status_arch = ea["architecture_status"]
        else:
            name, ptype, hub = calendar_edu_extra[tid]; url = "PLANNED — URL PENDING (proposed under Ring & Jewellery Guides)"; status_arch = "NEW (calendar-added; no Stage 14/15 owner)"
        conditional = (not cal)
        r = new_row()
        r["URL"] = (url + f" [{tid}]") if (url.startswith("http") or url.startswith("/") is False) else BASE + url
        r["Page Type"] = ptype; r["Page/Content Name"] = name; r["SEO Cluster / Topic"] = hub
        r["Page Role"] = "Hub/Cornerstone" if "HUB" in ptype else ("Informational (conditional — not active)" if conditional else "Informational")
        # keywords
        if b:
            pk = b.get("primary_keyword", ""); r["Primary Keyword"] = pk.split(" | ")[0] + "  [Stage 19 brief primary]"
            r["Secondary Keywords"] = "; ".join(L.split_list(b.get("secondary_keywords", ""))[:8])
        elif cal:
            r["Primary Keyword"] = cal["primary_keyword"] + f"  [calendar primary; {cal['primary_search_volume']}/mo]"
            r["Secondary Keywords"] = "; ".join(L.split_list(cal["secondary_keywords"])[:8])
        else:
            r["Primary Keyword"] = "NONE ASSIGNED — conditional/deferred owner (no Stage 15 keywords mapped; see 15_keyword_url_map.csv CONDITIONAL_NOT_MAPPED/DEFERRED_NOT_MAPPED)"
            r["Secondary Keywords"] = "—"
        if reg and b and cal:
            bp = b.get("primary_keyword", "").split(" | ")[0].replace("co-primary:", "").strip().lower()
            cp = cal["primary_keyword"].strip().lower()
            if bp and bp.split(";")[0].strip() != cp:
                r["Primary Keyword"] += f"  ||  CALENDAR PRIMARY: '{cal['primary_keyword']}' ({cal['primary_search_volume']}/mo)" + ("" if cp in L.kmap else " — NOT in Stage 15 keyword map (new research)")
        r["Related/Semantic Concepts"] = "; ".join(L.req_concepts(tid, 8)) or "—"
        r["Search Intent"] = (t.get("primary_intent", "") + (" | SERP: " + t.get("dominant_serp_type", "") if t.get("dominant_serp_type") else "")) if t else (cal["search_intent"] if cal else (ea["primary_intent"] if ea else "INFORMATIONAL"))
        if cal and cal["serp_page_type"]:
            r["Search Intent"] += " | calendar SERP: " + cal["serp_page_type"][:80]
        r["Keyword Owner"] = (tid + (" (Stage 15)" if reg else " (Stage 14 topic)")) if (reg or ea) else f"{tid} — NEW; no Stage 14/15 owner (ownership confirmation required)"
        conflicts = []
        if cal and "OWNERSHIP_CONFIRMATION" in cal["production_status"]:
            conflicts.append("Calendar flags OWNERSHIP_CONFIRMATION: " + cal["notes"][:0] + cal["cannibalization_status"][:260])
        if cal and reg and (cal["primary_keyword"].strip().lower() not in L.kmap):
            conflicts.append("Calendar primary keyword not in Stage 15 map (additive, not conflicting; ratify)")
        r["Existing Keyword Ownership Conflict?"] = " | ".join(conflicts) if conflicts else "NO"
        pairs = H.pairs_for(tid)
        r["Cannibalization Risk"] = ((reg["cannibalization_risk"] if reg else (cal["cannibalization_status"][:120] if cal else "n/a")) + (" — pairs: " + "; ".join(pairs) if pairs else ""))
        # current state (not live)
        for k in ("Current SEO Title", "Current Meta Description", "Current H1", "Current Canonical", "Current Indexability", "Current Schema"):
            r[k] = "NOT LIVE — page does not exist"
        r["Current URL Status"] = "NOT LIVE (no matching URL in live sitemap or crawl, 2026-10-09)"
        if cal:
            wt = cal["working_title"]
            r["Recommended SEO Title"] = pretty_title(wt) + "  (site template appends ' | House of Diams'; DRAFT)"
            r["Recommended H1"] = re.sub(r"\s*\((?:refresh|Lab-Grown Diamond Guide pillar)[^)]*\)", "", wt)
            r["Recommended Meta Description"] = f"DIRECTION (write with the article): answer the primary query in ≤155 chars, answer-first. Format hint: {cal['ae_o_answer_format'][:150]}"
        else:
            r["Recommended SEO Title"] = "DRAFT AT ACTIVATION — conditional page; no title until the activation condition is met"
            r["Recommended H1"] = name; r["Recommended Meta Description"] = "n/a until activated"
        if b:
            r["Recommended Content/Section Changes"] = f"Build per Stage 19 brief (19_content_briefs.csv; {len(L.gaps.get(tid, []))} Stage 18 gaps). Critical: {b.get('critical_requirements','')[:260]}"
        elif cal:
            r["Recommended Content/Section Changes"] = "No Stage 19 brief — create content brief first. Calendar notes: " + cal["cannibalization_status"][:200]
        else:
            r["Recommended Content/Section Changes"] = "Conditional/deferred: do not build. Activation condition per Stage 14/15: " + ((ea["business_dependency"][:200] if ea else "") or "business confirmation")
        r["Recommended Image/Alt-Text Changes"] = "Diagrams/charts/tables specified in the Stage 19 brief or SERP pattern; alt text describes the visual." if cal else "n/a"
        r["Recommended Internal Links IN"] = H.link_summary(tid, "in") or "Per Stage 16 when activated"
        r["Recommended Internal Links OUT"] = H.link_summary(tid, "out") or "Per Stage 16 when activated"
        r["Recommended Anchor Context"] = H.anchor_ctx(tid) or "Descriptive anchors (16_anchor_strategy)"
        r["Internal-Link Priority"] = ("REQUIRED at launch (Stage 16 LINKING_REQUIREMENT_AT_LAUNCH)" if cal else "n/a until activated")
        r["Recommended Schema"] = "Article (or BlogPosting per template) + BreadcrumbList; no FAQPage/HowTo rich-result markup; Organization author unless a real named expert is credited."
        r["Schema Validation/Review Needed?"] = "YES at launch"
        qs = L.top_questions(tid, 5)
        r["AEO Opportunity"] = ("HIGH — AI Overview present on the calendar SERP" if cal and "PRESENT" in cal.get("ai_overview", "") else ("MEDIUM" if cal else "n/a"))
        r["Primary Questions to Answer"] = "; ".join(qs) or (" ; ".join(L.paa_r2.get(cal["primary_keyword"].lower(), [])[:5]) if cal else "—")
        r["Answer-First Opportunity"] = (cal["ae_o_answer_format"][:220] if cal else "—")
        qn = len(L.qcov.get(tid, []))
        r["PAA/Question Coverage Needed?"] = (f"YES — {qn} Stage 18 questions mapped (FUTURE_PAGE); {cal['paa_questions_count']} live PAA captured" if qn else ("YES — PAA captured in calendar research" if cal else "n/a"))
        r["GEO/AI Search Opportunity"] = "Define the primary entity precisely, include a short quotable definition + table, cite GIA/IGI/industry sources where relevant, and show HOD first-hand context only where confirmed." if cal else "n/a"
        r["Important Entities"] = "; ".join(L.entities(tid, 8)) or "—"
        gaps_e = [e for e in L.ecov.get(tid, []) if e["coverage_status"] == "FUTURE_PAGE"]
        r["Entity Clarity Needed?"] = f"YES — {len(gaps_e)} required entities to introduce at launch" if gaps_e else ("YES" if cal else "n/a")
        r["Brand/Expertise/Trust Signal Opportunity"] = "Author/reviewer credential, last-updated date, sources; HOD workshop evidence only if confirmed (see business-fact list)." if cal else "n/a"
        gsc_na(r)
        # action/prio/status
        if cal:
            ps = cal["production_status"]
            if "BUSINESS_FACT_REQUIRED" in ps:
                act = "BLOCKED"
            elif "OWNERSHIP_CONFIRMATION" in ps:
                act = "REVIEW"
            else:
                act = "CREATE"
            prio = PRIO_CAL.get(cal["publishing_priority"], "MEDIUM")
            st = f"PLANNED — {cal['status']}; calendar date {cal['publish_date']}; production: {ps}"
            if cal["publish_date"] <= TODAY and not ps.startswith("DONE"):
                st += " — DATE REACHED/PASSED, NOT LIVE"
        else:
            act, prio, st = "REVIEW", "LOW", f"CONDITIONAL/DEFERRED — {status_arch}; not scheduled"
        if tid == "EDU-RJG-00":
            act, prio, st = "CREATE", "MEDIUM", "PLANNED — hub index required at launch of first RJG page (Stage 14/16)"
        r["Recommended Action"] = act; r["Priority"] = prio; r["Status"] = st
        r["Implementation Dependency"] = ("Stage 19 brief" if b else "Content brief needed") + "; " + ("business facts: " + "; ".join(x["fact"][:70] for x in L.bizfacts.get(tid, [])[:2]) if L.bizfacts.get(tid) else "no business fact flagged") + ("; ownership confirmation" if act == "REVIEW" and cal else "") + "; CMS publishing window vs AWS migration"
        r["Evidence / Source"] = SRC_EDU
        note = []
        if cal:
            note.append(f"Calendar {cal['content_id']} | {cal['publish_date']} | priority {cal['publishing_priority']} | {cal['existing_or_new']}.")
        note.append("Page is planned only. Prepare brief/draft now (A); publishing depends on migration content-freeze window (UNKNOWN — VERIFY).")
        r["Notes"] = " ".join(note)
        r["Row ID"] = tid; r["Registry/Calendar ID"] = tid; r["Row Group"] = "PLANNED EDUCATION" if cal else "CONDITIONAL EDUCATION"
        rows.append(finish(r, dict(meta=bool(cal), h1=bool(cal), links=bool(cal), schema=bool(cal), aeo=bool(cal), geo=bool(cal), conflict=("OWNERSHIP_CONFIRMATION" in r["Existing Keyword Ownership Conflict?"] or "CALENDAR PRIMARY" in r["Primary Keyword"]) , cannib=("HIGH" in r["Cannibalization Risk"] or "MEDIUM" in r["Cannibalization Risk"]), blocked=(act == "BLOCKED")),
                           a=["brief, draft, metadata, link plan"] if cal else ["none"], b=["publish into CMS inside the migration-safe window (content-freeze plan UNKNOWN — VERIFY)"] if cal else [], c=["URL live, canonical, indexability, schema, internal links, CWV"] if cal else []))
    return rows


# ---------------------------------------------------------------- calendar blog rows
def parse_seo_meta(bid):
    p = L.R + f"blogs/{bid.lower()}/seo-metadata.md"
    try:
        t = open(p, encoding="utf-8").read()
    except Exception:
        return None
    def g(label):
        m = re.search(r"\| \*\*" + label + r"\*\* \| (.*?) \|", t)
        return m.group(1).strip() if m else ""
    return dict(title=re.sub(r"\s*\(\d+ characters\).*", "", g("SEO title")), h1=g("H1"), meta=g("Meta description"), slug=g("URL slug").strip("`"))


CAT_ENT = {"BESPOKE": "bespoke jewellery; CAD design; Surat workshop; custom engagement ring", "CHRISTMAS": "Christmas / Hanukkah gift occasion; diamond studs; pendants; tennis bracelet",
           "ANNIVERSARY": "anniversary gift traditions by year; diamond jewellery", "PROPOSAL": "proposal planning; engagement ring; proposal timing",
           "RING_CULTURE": "ring finger/hand meaning; engagement ring; wedding band", "STYLE": "jewellery styling; layering/stacking; ring types",
           "GIFTS": "recipient-based gift ideas; diamond jewellery", "WEDDING": "wedding band; engagement ring; wedding etiquette",
           "RING_GUIDE": "ring sizing/guides", "JEWELLERY_GUIDE": "jewellery sizing/length", "METALS": "gold/platinum metals", "4CS": "4Cs", "LAB_GROWN": "lab-grown diamond"}


def blog_rows():
    rows = []
    cal_blog = [c for c in L.cal if c["education_or_blog"] == "BLOG" and c["content_id"] != "BC-004-DEC-REFRESH"]
    ref_in = collections.defaultdict(list)
    for c in L.cal:
        for t in L.split_list(c["internal_link_targets"]):
            ref_in[t].append(c["content_id"])
    for c in cal_blog:
        cid = c["content_id"]
        sm = parse_seo_meta(cid)
        r = new_row()
        slug = sm["slug"] if sm and sm["slug"] else "PLANNED — /blog/<slug> generated from the Article Title at first save"
        r["URL"] = (BASE + slug) if slug.startswith("/") else slug + f" [{cid}]"
        r["Page Type"] = "BLOG_POST (" + (c["target_owner"].split("BLOG-")[-1].strip(")") if "BLOG-" in c["target_owner"] else c["target_owner"][:40]) + ")"
        r["Page/Content Name"] = c["working_title"]; r["SEO Cluster / Topic"] = f"{c['content_category']} / {c['content_type']}"
        r["Page Role"] = "Supporting (Blog editorial)" if c["content_type"] != "HIGH_INTENT" else "Supporting (high-intent Blog)"
        r["Primary Keyword"] = f"{c['primary_keyword']} ({c['primary_search_volume']}/mo; KD {c['keyword_difficulty']})"
        r["Secondary Keywords"] = "; ".join(L.split_list(c["secondary_keywords"])[:8])
        r["Related/Semantic Concepts"] = CAT_ENT.get(c["content_category"], c["content_category"].lower()) + ("; " + c["occasion"] if c["occasion"] not in ("NONE", "") else "")
        r["Search Intent"] = c["search_intent"] + " | SERP: " + c["serp_page_type"][:90]
        r["Keyword Owner"] = c["target_owner"]
        conf = []
        if "OWNERSHIP_CONFIRMATION" in c["production_status"]:
            conf.append("OWNERSHIP_CONFIRMATION flagged in calendar (Blog vs Education ownership of this topic is unconfirmed)")
        additive = c["primary_keyword"].strip().lower() not in L.kmap
        r["Existing Keyword Ownership Conflict?"] = "; ".join(conf) if conf else ("NO CONFLICT — primary keyword is outside the Stage 15 map (new calendar research; 'no Stage 15 owner'); no secondary keyword maps to another Stage 15 target" if additive else "NO")
        r["Cannibalization Risk"] = c["cannibalization_status"][:260]
        for k in ("Current SEO Title", "Current Meta Description", "Current H1", "Current Canonical", "Current Indexability", "Current Schema"):
            r[k] = "NOT LIVE — page does not exist"
        r["Current URL Status"] = f"NOT LIVE (no matching URL in live sitemap/crawl, {CRAWL_DATE})" + ("; draft package exists in blogs/" + cid.lower() if sm else "")
        if sm:
            r["Recommended SEO Title"] = sm["title"] + "  (approved; template appends ' | House of Diams')"; r["Recommended H1"] = sm["h1"]; r["Recommended Meta Description"] = sm["meta"]
        else:
            r["Recommended SEO Title"] = pretty_title(c["working_title"]) + "  (DRAFT; template appends ' | House of Diams')"
            r["Recommended H1"] = c["working_title"]
            r["Recommended Meta Description"] = f"DIRECTION (write with the article): answer-first, ≤155 chars. Format hint: {c['ae_o_answer_format'][:150]}"
        r["Recommended Content/Section Changes"] = ("Draft package READY (approved article, cms-entry, seo-metadata, internal-links, QA)" if sm else "Write per calendar row + SERP/PAA data (no Stage 19 brief for Blog items)") + f". Boundary: {c['cannibalization_status'][:200]} Business facts: {('see calendar notes' if 'BUSINESS_FACT' in c['production_status'] else 'none flagged')}."
        r["Recommended Image/Alt-Text Changes"] = "Real HOD photography where possible; alt text describes the image; see blogs/…/image-requirements.md" if sm else "Charts/diagrams only where the SERP pattern supports them; descriptive alt text."
        ins = ["BLOG-HUB (REQUIRED)"] + [f"{x} (calendar link)" for x in ref_in.get(cid, [])[:6]]
        r["Recommended Internal Links IN"] = "; ".join(ins)
        tg = L.split_list(c["internal_link_targets"])
        r["Recommended Internal Links OUT"] = "; ".join(H.disp(x) for x in tg)
        ac = []
        for x in tg[:4]:
            if x in L.anchors and L.anchors[x]:
                ac.append(f"{x}: “{L.anchors[x][0]['recommended_anchor'][:70]}”")
        r["Recommended Anchor Context"] = "; ".join(ac) or "Descriptive anchors per 16_anchor_strategy; CTA: " + c["CTA_direction"][:100]
        r["Internal-Link Priority"] = "REQUIRED at launch (Stage 16 BLOG-* rows: hub ↔ post; Education owners)"
        r["Recommended Schema"] = "BlogPosting + BreadcrumbList; ISO 8601 dates; author = Organization 'House of Diams' (or a named real expert). NO FAQPage/HowTo (no rich results; QAPage invalid)."
        r["Schema Validation/Review Needed?"] = "YES — current template emits author as Person and no BreadcrumbList on blog posts (crawl of live posts, 2026-10-09)"
        s2 = L.r2serp.get(c["primary_keyword"].strip().lower())
        paa = L.paa_r2.get(c["primary_keyword"].strip().lower(), [])
        r["AEO Opportunity"] = ("HIGH — AI Overview present" if "PRESENT" in c["ai_overview"] or "AIO" in c["ai_overview"] else "MEDIUM") + f"; PAA {c['paa_questions_count']}"
        if cid == "BC-001":
            paa = [q for q in paa if not re.search(r"spend|\$|cheap|lot for|afford|budget|month rule|big", q, re.I)]
        r["Primary Questions to Answer"] = ("; ".join(dict.fromkeys(paa))[:500] or c["working_title"]) + (" (budget PAA excluded: routed to BC-024 per calendar)" if cid == "BC-001" else "")
        r["Answer-First Opportunity"] = c["ae_o_answer_format"][:240]
        r["PAA/Question Coverage Needed?"] = f"YES — {c['paa_questions_count']} PAA captured in calendar research (map into H2/H3 or answer blocks; no FAQ padding)"
        r["GEO/AI Search Opportunity"] = "Answer-first block + dated facts + clear entities; HOD-specific first-hand context only where confirmed (" + c["HOD_relevance"][:60] + ")."
        r["Important Entities"] = CAT_ENT.get(c["content_category"], "") + "; House of Diams (publisher)"
        r["Entity Clarity Needed?"] = "YES — define the primary entity in the first paragraph" if c["content_type"] in ("INFORMATIONAL", "EDUCATION") else "MODERATE"
        r["Brand/Expertise/Trust Signal Opportunity"] = "Byline policy (Organization vs named person), sources, last-updated date; confirmed bespoke facts only ('typically', never a guarantee)."
        gsc_na(r)
        ps = c["production_status"]
        act = "BLOCKED" if "BUSINESS_FACT_REQUIRED" in ps else ("REVIEW" if "OWNERSHIP_CONFIRMATION" in ps else "CREATE")
        prio = PRIO_CAL.get(c["publishing_priority"], "MEDIUM")
        r["Recommended Action"] = act; r["Priority"] = prio
        late = c["publish_date"] <= TODAY
        r["Status"] = f"PLANNED — {c['status']}; calendar date {c['publish_date']}; production: {ps}" + (" — SCHEDULED DATE REACHED/PASSED, NOT LIVE" if late else "") + ("; DRAFT PACKAGE READY" if sm else "")
        r["Implementation Dependency"] = "CMS publishing (human review); " + ("business fact confirmation" if act == "BLOCKED" else "ownership confirmation" if act == "REVIEW" else "none blocking") + "; publishing window vs AWS migration"
        r["Evidence / Source"] = f"FINAL-BLOG-CALENDAR/BLOG_CALENDAR_FINAL.csv ({cid}); content-strategy/blog-calendar/revision/round2_paa_questions.csv; " + (f"blogs/{cid.lower()}/ (draft package); " if sm else "") + "live sitemap check 2026-10-09"
        r["Notes"] = f"Seasonal: {c['season']}/{c['festival']}; lead time {c['lead_time_days']} days. " + ("Date has passed without a live URL — confirm whether publishing is paused for the AWS migration (UNKNOWN — VERIFY). " if late else "") + ("BC-004 also has a December refresh row (BC-004-DEC-REFRESH, 2026-12-07, BUSINESS_FACT_REQUIRED: shipping cut-offs). " if cid == "BC-004" else "")
        r["Row ID"] = cid; r["Registry/Calendar ID"] = cid; r["Row Group"] = "PLANNED BLOG"
        rows.append(finish(r, dict(meta=1, h1=1, links=1, schema=1, aeo=1, geo=1, conflict=bool(conf), cannib=("MEDIUM" in c["cannibalization_status"][:12] or "HIGH" in c["cannibalization_status"][:12]), blocked=(act == "BLOCKED")),
                           a=["draft/approve content, metadata, link plan"], b=["publish into CMS inside the migration-safe window (content-freeze plan UNKNOWN — VERIFY)"], c=["URL live, canonical, indexability, schema, links, CWV"]))
    return rows
