#!/usr/bin/env python3
"""Stage 13 builder: existing-content decisions, ranking equity, Blog/Education
framework and migration risk.

Local project files only. No DataForSEO or live-site calls.
Ranking rows are read from Stage 3/10/11 files so every Stage 3 ranking keyword
and position is carried over exactly; judgement fields are written below.
Run from the project root:  python3 content-strategy/scripts/build_13_csvs.py
"""
import csv
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CS = os.path.join(ROOT, "content-strategy")
D = "https://www.houseofdiams.com"


def rd(path):
    with open(os.path.join(ROOT, path), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def wr(name, cols, rows):
    with open(os.path.join(CS, name), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})


# ---------------------------------------------------------------- sources
stage3 = rd("dataforseo/processed/03_hod_ranked_keywords.csv")
align10 = {(r["url"], r["keyword"]): r for r in rd("content-strategy/10_content_serp_alignment.csv")
           if r["basis"] == "STAGE3_RANKING_KEYWORD"}
cmap = {r["keyword"]: r for r in rd("clusters/11_keyword_cluster_map.csv")}
inv = {r["url"]: r for r in rd("content-strategy/10_existing_content_inventory.csv")}

# URL short names
CVD = f"{D}/blog/cvd-vs-hpht-lab-grown-diamonds-what-buyers-should-know-house-of-diams"
LVN = f"{D}/blog/lab-grown-vs-natural-diamonds-the-honest-comparison-house-of-diams"
K14 = f"{D}/blog/14k-vs-18k-gold-for-diamond-jewellery-which-is-better-house-of-diams"
HTC = f"{D}/blog/how-to-choose-a-lab-grown-diamond-the-complete-buyer-s-guide"
REAL = f"{D}/blog/are-lab-grown-diamonds-real-a-complete-buyer-s-guide"
FOURC = f"{D}/blog/the-4cs-of-lab-grown-diamonds-explained-cut-colour-clarity-and-carat-house-of-diams"
ONLINE = f"{D}/blog/how-to-choose-a-lab-grown-diamond-engagement-ring-online-house-of-diams"
SHAPES = f"{D}/blog/the-best-lab-grown-diamond-shapes-for-engagement-rings-house-of-diams"
RSIZE = f"{D}/blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-house-of-diams"
IGI = f"{D}/blog/igi-certification-for-lab-grown-diamonds-what-it-means-house-of-diams"
GIAIGI = f"{D}/education/lab-grown-diamond-certification-explained-gia-vs-igi-house-of-diams"
BLOGHUB = f"{D}/blog"
EDUHUB = f"{D}/education"
FAQ = f"{D}/faq"
PDP = f"{D}/shop/oval-floral-diamond-ring"
SIDE = f"{D}/engagement-rings/by-desgin/side-stone-rings"

PAGE_TYPE = {
    CVD: "BLOG_ARTICLE (evergreen comparison)", LVN: "BLOG_ARTICLE (evergreen comparison)",
    K14: "BLOG_ARTICLE (evergreen comparison)", HTC: "BLOG_ARTICLE (evergreen buying guide)",
    PDP: "PRODUCT_PAGE", SIDE: "SUBCATEGORY (nav-only, not in sitemap)",
}

# ------------------------------------------------ 13_ranking_equity_analysis
# alignment judgement per keyword (position is never the deciding input)
PARTIAL_CL017 = ("PARTIALLY_ALIGNED",
                 "Single-method HPHT query (CL-017), not the CVD-vs-HPHT comparison (CL-016). Stage 11 kept "
                 "CL-016/CL-017 as separate clusters; REL-001 POSSIBLE_OVERLAP (55 SERP pairs, mean 1.9 shared "
                 "top-10 URLs, max 4). The comparison article covers HPHT, so it ranks, but the SERP need is "
                 "'what is HPHT' rather than 'which method'.")
PARTIAL_CL018 = ("PARTIALLY_ALIGNED",
                 "Single-method CVD query (CL-018), not the method comparison (CL-016). REL-002 POSSIBLE_OVERLAP "
                 "(22 SERP pairs, mean 1.5 shared URLs).")
JUDGE = {
    "are cvd diamonds real": ("PARTIALLY_ALIGNED",
        "CVD authenticity question (CL-018). Stage 8 SERP UNCLEAR/OTHER (vrai, queensmith, ritani, growndiamondcorp, "
        "wikipedia); Stage 10 marked INSUFFICIENT_EVIDENCE. OV-03: string-matches the are-lab-grown-real article "
        "but only the CVD article ranks. Best-positioned HOD keyword (27)."),
    "what is cvd lab grown diamond": ("PARTIALLY_ALIGNED",
        "Definitional single-method CVD query (CL-018). Stage 8 SERP MIXED, LOW confidence."),
    "cvd diamond vs lab grown": ("ALIGNED",
        "Moved into CL-016 by Stage 11 QC: its SERP shares 4-5 top-10 URLs with CVD-vs-HPHT SERPs. The query rests on "
        "a misconception (CVD is a lab-grown method), which the comparison article answers."),
    "what is cvd diamond vs lab grown": ("ALIGNED", "CL-016; EDITORIAL_GUIDE SERP. Same misconception pattern as above."),
    "cvd/hpht diamond tester": ("MISALIGNED",
        "Stage 8 SERP TRANSACTIONAL/CATEGORY (tool retailers selling tester devices). Stage 10 PAGE_TYPE_MISMATCH. "
        "HOD does not sell testers (Stage 12: NOT_PROPOSED). Incidental ranking; not equity to protect or chase."),
    "hpht lab grown diamonds": PARTIAL_CL017, "hpht lab grown diamond": PARTIAL_CL017,
    "lab grown hpht diamonds": PARTIAL_CL017, "lab grown diamond hpht": PARTIAL_CL017,
    "lab grown diamonds hpht": PARTIAL_CL017,
    "which diamond is better lab grown or natural": ("ALIGNED",
        "Topic and cluster (CL-011) match the article. Caveat: Stage 8 SERP typed UNCLEAR/OTHER (MEDIUM), so SERP "
        "page-type evidence is inconclusive for this variant; the two sibling variants are COMPARISON SERPs."),
    "is 14k diamond good": ("ALIGNED",
        "CL-110; EDITORIAL_GUIDE SERP (HIGH). Query is about 14k gold settings, which the article covers."),
    "marquise oval diamond": ("ALIGNED",
        "PRODUCT SERP (keyzarjewelry, benzdiamonds PDPs) served by a HOD PDP. CL-063 is a shape cluster "
        "(head 'moval diamond' 4,400); OV-11 DISTINCT from the shapes article."),
    "side stones engagement rings": ("ALIGNED",
        "CATEGORY SERP (sarahojewelry, zales, laurapreshong) served by a HOD category page. Only ranking category "
        "URL; Stage 12 D-03 confirms side-stone as an indexable L2."),
}
DEFAULT_ALIGNED_NOTE = {
    CVD: "Core CVD-vs-HPHT comparison query (CL-016); EDITORIAL_GUIDE SERP; article is an editorial guide.",
    LVN: "Core lab-vs-natural comparison query (CL-011, head 'lab grown vs natural diamonds' 22,200); COMPARISON SERP.",
    K14: "Core 14k-vs-18k query (CL-110 HIGH); EDITORIAL_GUIDE SERP.",
    HTC: "CL-024 buying guidance; EDITORIAL_GUIDE SERP (HIGH). Cluster has 3 keywords, max volume 30.",
}


def equity_risk(pos, alignment, vol):
    # descriptive bands, not a score: what would be at stake if this URL changed
    if alignment == "MISALIGNED":
        return "LOW"
    if pos <= 50:
        return "HIGH"
    if pos <= 100:
        return "MEDIUM"
    return "LOW"


eq_rows = []
for r in sorted(stage3, key=lambda x: (x["ranking_url"], int(x["rank_absolute"]))):
    url, kw = r["ranking_url"], r["keyword"]
    a = align10[(url, kw)]
    c = cmap[kw]
    pos = int(r["rank_absolute"])
    alignment, why = JUDGE.get(kw, ("ALIGNED", DEFAULT_ALIGNED_NOTE.get(url, "")))
    risk = equity_risk(pos, alignment, int(r["search_volume"]))
    note = why
    if kw in ("hpht lab grown diamonds", "hpht lab grown diamond"):
        note += (" These two 8,100-volume variants carry about 34 of the URL's 36.5 Stage 3 ETV, so most of this "
                 "article's estimated value comes from the adjacent single-method HPHT need.")
    if url == SIDE:
        note += " Position 104 is minimal positional equity, but it is HOD's only commercial-category ranking."
    note += " Stage 3 is a single Labs snapshot (all rows is_new=True); not live rank."
    eq_rows.append({
        "url": url, "keyword": kw, "position": pos, "search_volume": r["search_volume"],
        "cluster": f"{c['cluster_id']} {c['cluster_name']}",
        "intent": f"{a['stage8_validated_intent']} (Stage 8, {a['stage8_validation_confidence']}); Stage 11: {c['search_intent']} [{c['intent_source']}]",
        "serp_page_type": a["stage8_dominant_serp_page_type"],
        "current_page_type": PAGE_TYPE[url],
        "alignment": alignment, "equity_risk": risk, "notes": note,
    })

wr("13_ranking_equity_analysis.csv",
   ["url", "keyword", "position", "search_volume", "cluster", "intent", "serp_page_type",
    "current_page_type", "alignment", "equity_risk", "notes"], eq_rows)


def kw_summary(url):
    rows = [r for r in stage3 if r["ranking_url"] == url]
    rows.sort(key=lambda x: int(x["rank_absolute"]))
    return (len(rows), "; ".join(f"{r['keyword']} (pos {r['rank_absolute']}, vol {r['search_volume']})" for r in rows),
            rows[0]["rank_absolute"] if rows else "")


# ------------------------------------------------ 13_existing_content_decisions
DEC = [
    dict(url=CVD, content_type="BLOG_ARTICLE", business_area="8. Lab-Grown Diamonds",
         current_role="Blog article acting as HOD's main evergreen lab-grown reference; holds 19 of 28 Stage 3 rankings",
         important_search_volume="hpht lab grown diamonds / hpht lab grown diamond 8,100 each (pos 49); hpht vs cvd 720 (pos 54); remaining 16 keywords 20-30",
         stage11_clusters="CL-016 (11 kw), CL-017 (5), CL-018 (2), CL-022 (1)",
         validated_intent="INFORMATIONAL (18 of 19 SERP-validated; 1 TRANSACTIONAL tester query)",
         serp_page_type="EDITORIAL_GUIDE dominant (14); COMPARISON (1); OTHER (1); MIXED (1); CATEGORY (1 tester query)",
         overlap_status="POSSIBLE_OVERLAP", overlap_with="are-lab-grown-real blog (OV-03, one query family); DISTINCT from lab-vs-natural blog (OV-04)",
         proposed_role="Education-owned evergreen comparison (Lab-Grown topic), kept at its current URL until the migration conditions are met",
         action="UPDATE_IN_PLACE", migration_risk="HIGH", confidence="MEDIUM",
         evidence="Stage 3: 19 rankings, pos 27-68, ~36.5 ETV. Stage 8: 18/19 informational. Stage 10: 17 ALIGNMENT, 1 PAGE_TYPE_MISMATCH, 1 INSUFFICIENT. Stage 11: CL-016/017/018 HIGH evidence, STRONG_EXISTING_CONTENT_SIGNAL. Stage 9: competitors rank for this topic on /blog(s)/ paths (regalhattongarden, lgdusallc, ritani /blogs/education/).",
         rationale="Topic is evergreen reference, so Education owns it (P-ONE-TOPIC-ONE-HOME). But this URL carries 68% of HOD's ranking keywords and nearly all estimated traffic value, and the Education destination does not exist yet. Stage 8/9 show /blog paths rank for this exact topic, so a path change brings no demonstrated ranking benefit. Ownership moves now; the URL stays. Update in place to serve CL-016 fully and cover the adjacent HPHT/CVD single-method questions it already ranks for.",
         deferred_question="Stage 14: does CL-017 (HPHT, head 8,100) or CL-018 (CVD, head 3,600) need its own Education page, or does this article stay the single home? A separate HPHT page could fragment the equity this URL holds. Physical move only if the conditions in 13_content_migration_risk.csv are met."),
    dict(url=LVN, content_type="BLOG_ARTICLE", business_area="8. Lab-Grown Diamonds / 9. Natural Diamonds",
         current_role="Blog article serving the core origin comparison; 3 Stage 3 rankings including HOD's second-best position",
         important_search_volume="Ranking kw 20-30 each; cluster head 'lab grown vs natural diamonds' 22,200 (HOD not ranking)",
         stage11_clusters="CL-011 (3 kw); Stage 11 also links CL-020 identification and CL-051 fancy colour (signals only)",
         validated_intent="INFORMATIONAL / COMPARISON (2 HIGH); 1 variant UNCLEAR/OTHER",
         serp_page_type="COMPARISON (2); OTHER (1)",
         overlap_status="POSSIBLE_OVERLAP", overlap_with="are-lab-grown-real blog (OV-02: both SERPs COMPARISON-dominant, 1 shared top-10 URL); FAQ (OV-10)",
         proposed_role="Education-owned evergreen comparison (Lab-Grown topic; primary home for CL-011), kept at its current URL until the migration conditions are met",
         action="UPDATE_IN_PLACE", migration_risk="HIGH", confidence="MEDIUM",
         evidence="Stage 3: pos 29/36/40. Stage 8: head term 22,200 COMPARISON SERP (kay, brilliantearth /guides/, diamondmansion /blog/). Stage 11: CL-011 HIGH, STRONG_EXISTING_CONTENT_SIGNAL; REL-020 CL-010 vs CL-011 RELATED_BUT_DISTINCT (HIGH).",
         rationale="Aligned with a high-demand, HIGH-evidence comparison cluster. Equity is small in traffic terms but it is the best-positioned foothold in HOD's most valuable informational cluster. Moving it before an Education lab-grown hub exists would add redirect risk with no demonstrated gain. Update in place to target the head comparison intent.",
         deferred_question="Stage 14: exact scope boundary with the authenticity page (CL-010). Physical move only if migration conditions are met."),
    dict(url=K14, content_type="BLOG_ARTICLE", business_area="15. Jewellery Materials / Metals",
         current_role="Blog article serving an evergreen metal comparison; 3 weak rankings",
         important_search_volume="Ranking kw 20-30 each; cluster head '10 kt rings' 1,000",
         stage11_clusters="CL-110 (3 kw)", validated_intent="INFORMATIONAL (3 of 3, 2 HIGH)",
         serp_page_type="EDITORIAL_GUIDE (3)", overlap_status="DISTINCT",
         overlap_with="Online-ring guide references metal as a step (OV-09 DISTINCT); CL-110 vs CL-112 RELATED_BUT_DISTINCT",
         proposed_role="Education evergreen comparison (Metals & Materials topic)",
         action="MOVE_TO_EDUCATION", migration_risk="MEDIUM", confidence="MEDIUM",
         evidence="Stage 3: pos 81, 84, 95 (~0.17 ETV). Stage 8: all EDITORIAL_GUIDE. Stage 11: CL-110 HIGH, STRONG_EXISTING_CONTENT_SIGNAL. No overlap with another HOD page.",
         rationale="Clearly evergreen reference with no overlap. Rankings at 81-95 carry almost no traffic value, so a 301 move puts little at risk. It should move only with the Education Metals section, not ahead of it, and only with a 1:1 301.",
         deferred_question="Timing: move with the rebuild once the Education metals home exists. Confirm with GSC and backlink data that the URL has no hidden equity beyond Stage 3."),
    dict(url=HTC, content_type="BLOG_ARTICLE", business_area="14. Diamond Buying / Education / 8. Lab-Grown",
         current_role="Blog buying guide for choosing a lab-grown diamond; 1 ranking",
         important_search_volume="how to choose a lab grown diamond 30 (pos 35); CL-024 max volume 30",
         stage11_clusters="CL-024 (MULTIPLE_EXISTING_CONTENT_POSSIBLE_OVERLAP)",
         validated_intent="INFORMATIONAL (HIGH)", serp_page_type="EDITORIAL_GUIDE",
         overlap_status="POSSIBLE_OVERLAP", overlap_with="Online engagement-ring guide (OV-06); 4Cs article (OV-07, shared sub-topic only); DISTINCT from are-real (OV-05)",
         proposed_role="Education buying guide (Lab-Grown / Buying Guides); presumed survivor if the buying-guide overlap is later consolidated, because it holds the ranking",
         action="DEFER", migration_risk="MEDIUM", confidence="LOW",
         evidence="Stage 3: 1 ranking pos 35. Stage 8: SERP mixes reddit, retailer blogs, brilliantearth /guides/, gemsociety. Stage 10: OV-06 POSSIBLE; the ring-buying side has no validated SERP. Stage 11: CL-024 has only 3 keywords (max vol 30).",
         rationale="Belongs in Education by type, but its relationship with the online-ring guide is unresolved and the measured demand is tiny. Merging, differentiating or moving it without SERP evidence for the ring-buying intent would be a guess.",
         deferred_question="Is 'how to choose a lab-grown diamond' (stone) a different buyer decision from 'how to buy an engagement ring online' (ring)? Needs SERPs for engagement-ring buying-guide queries, which are missing from the master DB (commercial keyword gap, Stage 12 D-19)."),
    dict(url=REAL, content_type="BLOG_ARTICLE", business_area="8. Lab-Grown Diamonds",
         current_role="Blog article on lab-grown legitimacy; no rankings",
         important_search_volume="No ranking kw. CL-010 head 'are lab grown diamonds real' 14,800; Stage 10 topic match 21 kw / 29,160 raw volume",
         stage11_clusters="CL-010 (authenticity); CL-008 pricing signal",
         validated_intent="INFORMATIONAL (topic SERP)", serp_page_type="COMPARISON (are lab grown diamonds real)",
         overlap_status="POSSIBLE_OVERLAP", overlap_with="Lab-vs-natural blog (OV-02); CVD-vs-HPHT blog (OV-03); FAQ (OV-10); DISTINCT from how-to-choose (OV-05)",
         proposed_role="Education evergreen explainer (Lab-Grown topic; primary home for CL-010 authenticity)",
         action="MOVE_TO_EDUCATION", migration_risk="LOW", confidence="MEDIUM",
         evidence="Stage 3: 0 rankings. Stage 8: head query 14,800 COMPARISON-dominant (reddit, frankdarling /blog/, brilliantearth, vrai /journal/, kay); HOD absent. Stage 11: REL-020 CL-010 vs CL-011 RELATED_BUT_DISTINCT (HIGH; mean 1.0 shared URLs).",
         rationale="Evergreen trust question with large demand and no ranking equity to lose. Stage 11 SERP evidence keeps authenticity separate from lab-vs-natural, so it stays a distinct Education topic rather than merging. Google answers 'are they real' with comparison-style pages, so the content must address the comparison angle and link to the lab-vs-natural page.",
         deferred_question="Stage 14: final scope versus CL-011 and CL-008 pricing. Check GSC/backlinks before the redirect."),
    dict(url=FOURC, content_type="BLOG_ARTICLE", business_area="12. Diamond Quality / 4Cs / 8. Lab-Grown",
         current_role="Blog article covering the 4Cs for lab-grown diamonds; no rankings; one article stretched across 12 quality clusters",
         important_search_volume="No ranking kw. Linked clusters include CL-040 head 'diamond clarity grading scale' 12,100 and CL-043 'v v s diamond' 18,100",
         stage11_clusters="CL-023, CL-040 to CL-049, CL-089 (EXISTING_CONTENT_SIGNAL); CL-125 possible overlap signal",
         validated_intent="INFORMATIONAL (topic SERPs)", serp_page_type="EDITORIAL_GUIDE dominant on quality SERPs (gia, whiteflash, brilliantearth, bluenile)",
         overlap_status="POSSIBLE_OVERLAP", overlap_with="How-to-choose (OV-07) and online-ring guide (OV-08): shared 4Cs sub-topic, different primary intent; measured SERP pair shares 0 URLs",
         proposed_role="Education reference (Diamond Quality / 4Cs topic)",
         action="MOVE_TO_EDUCATION", migration_risk="LOW", confidence="MEDIUM",
         evidence="Stage 3: 0 rankings. Stage 8: clarity/cut SERPs EDITORIAL_GUIDE (CL-041 HIGH). Stage 12: Education > Diamond Quality hub conceptual; 'one article stretched across 12 clusters'.",
         rationale="Pure evergreen reference with no ranking equity. Education is its home. The overlaps with the buying guides are shared sub-topics, not shared intent, so they do not block the move.",
         deferred_question="Stage 14: is this the general 4Cs overview (CL-040) or a lab-grown-specific quality page (CL-023)? Will the 4Cs be one guide or several?"),
    dict(url=ONLINE, content_type="BLOG_ARTICLE", business_area="1. Engagement Rings / 14. Diamond Buying",
         current_role="Blog step-by-step guide to buying an engagement ring online; no rankings",
         important_search_volume="No ranking kw; 2 weak topic matches in master DB",
         stage11_clusters="CL-024 (possible overlap signal)", validated_intent="Not validated (no ring-buying SERP)",
         serp_page_type="Not validated", overlap_status="POSSIBLE_OVERLAP",
         overlap_with="How-to-choose (OV-06); 4Cs (OV-08); DISTINCT from shapes / 14k / ring-size (OV-09)",
         proposed_role="Education buying guide (engagement-ring purchase decision) OR consolidation into the lab-grown buying guide; undecided",
         action="DEFER", migration_risk="LOW", confidence="LOW",
         evidence="Stage 3: 0 rankings. Stage 10: content-level overlap only (Stage 1 note). Stage 11: no validated keyword for engagement-ring buying guidance. Stage 12 D-19: engagement-ring commercial/research keywords are missing from the universe.",
         rationale="This is the only article that bridges directly to the core commercial category, so its role matters. But there is no keyword or SERP evidence on whether 'buying an engagement ring online' is a distinct intent from choosing a lab-grown stone. Deferring avoids an unsupported merge.",
         deferred_question="Resolve with the commercial keyword/SERP supplement (D-19): validate 'engagement ring buying guide' / 'buy engagement ring online' SERPs, then decide merge vs separate Education guide."),
    dict(url=SHAPES, content_type="BLOG_ARTICLE", business_area="10. Diamond Shapes / 1. Engagement Rings",
         current_role="Blog shape guide for engagement rings; no rankings",
         important_search_volume="No ranking kw. CL-060 'diamond shape' 60,500; CL-061 'asscher cut diamond' 18,100; CL-063 'moval diamond' 4,400",
         stage11_clusters="CL-060 to CL-064 (EXISTING_CONTENT_SIGNAL)", validated_intent="INFORMATIONAL (diamond shape)",
         serp_page_type="EDITORIAL_GUIDE (diamond shape), served by education/guide paths (gia, tiffany, brilliantearth /guides/, bluenile /education/)",
         overlap_status="DISTINCT", overlap_with="PDP for 'marquise oval diamond' (OV-11 DISTINCT); online-ring guide (OV-09 DISTINCT)",
         proposed_role="Education reference (Diamond Shapes & Cuts topic)",
         action="MOVE_TO_EDUCATION", migration_risk="LOW", confidence="MEDIUM",
         evidence="Stage 3: 0 rankings. Stage 8: 'diamond shape' EDITORIAL_GUIDE via education paths. Stage 12 D-06: shapes live in Education; shape shopping stays a filter.",
         rationale="Evergreen decision support with no ranking equity and no demonstrated overlap. A dated 'trending shapes' angle would be Blog, but this article is framed as a permanent guide.",
         deferred_question="Stage 14: is this the shapes overview (CL-060) or an engagement-ring shape chooser (CL-064)? Per-shape pages are Stage 14."),
    dict(url=RSIZE, content_type="BLOG_ARTICLE", business_area="14. Diamond Buying / 1. Engagement Rings",
         current_role="Blog practical utility guide (ring sizing); no rankings",
         important_search_volume="No ranking kw. Master DB has no 'ring size' / 'ring size chart' keywords; CL-124 resizing head 1,000",
         stage11_clusters="CL-124 (INSUFFICIENT_EVIDENCE; resizing, not size-finding)", validated_intent="Not validated",
         serp_page_type="Not validated", overlap_status="DISTINCT", overlap_with="Online-ring guide references sizing as a step (OV-09 DISTINCT)",
         proposed_role="Education practical guide (Ring & Jewellery Guides); possibly a TOOL page",
         action="MOVE_TO_EDUCATION", migration_risk="LOW", confidence="MEDIUM",
         evidence="Stage 3: 0 rankings. Stage 11: only resizing questions measured (keyword-data gap for size-finding). Stage 12: Ring & Jewellery Guides hub; ring-size tool vs article deferred to Stage 14.",
         rationale="Evergreen utility that supports purchase and returns, with no ranking equity and no overlap. Its home is clear even though demand is unmeasured.",
         deferred_question="Stage 14: tool page vs article. Measure 'ring size' / 'ring size chart' demand (not in master DB)."),
    dict(url=IGI, content_type="BLOG_ARTICLE", business_area="13. Diamond Certification / 8. Lab-Grown",
         current_role="Blog explainer on IGI certification; no rankings; topic overlaps the Education GIA-vs-IGI article",
         important_search_volume="No ranking kw. CL-032 head 'igi lab grown diamond' 1,000; CL-033 head 'certified lab diamonds' 590; 'lab-grown diamond certification' 390",
         stage11_clusters="CL-030 to CL-034 (all MULTIPLE_EXISTING_CONTENT_POSSIBLE_OVERLAP)",
         validated_intent="INFORMATIONAL (topic SERPs)", serp_page_type="EDITORIAL_GUIDE ('lab-grown diamond certification': igi.org, gia.edu, retailer guides)",
         overlap_status="CLEAR_OVERLAP", overlap_with="Education GIA-vs-IGI article (OV-01)",
         proposed_role="Education certification explainer for a non-comparison intent (general lab-grown certification or IGI report), no longer competing with the GIA-vs-IGI comparison",
         action="RETARGET", migration_risk="LOW", confidence="MEDIUM",
         evidence="Stage 10 OV-01 CLEAR_OVERLAP at topic level; cannibalization not proven (neither URL ranks). Stage 8: 'gia vs igi lab diamond' and 'lab-grown diamond certification' share 0 top-10 URLs, so Google treats comparison and general certification as different intents. Stage 11: CL-030 vs CL-033 RELATED_BUT_DISTINCT; CL-030 vs CL-032 POSSIBLE_OVERLAP (LOW, no SERP).",
         rationale="SERP evidence supports two certification pages with different jobs, not a merge. The Education article already carries 'GIA vs IGI' and suits the comparison intent. This article should take the non-comparison certification need and move into Education with it. It has no equity, so the retarget and move carry little risk.",
         deferred_question="Retarget to CL-033 (general lab-grown certification) or CL-032 (IGI report-specific)? No IGI-only keyword was SERP-validated. Decide in Stage 14; keyword assignment in Stage 15."),
    dict(url=GIAIGI, content_type="EDUCATION_ARTICLE", business_area="13. Diamond Certification / 8. Lab-Grown",
         current_role="Only Education article; title mixes 'certification explained' and 'GIA vs IGI'",
         important_search_volume="No ranking kw. CL-030 head 'gia vs igi lab diamond' 140",
         stage11_clusters="CL-030 (primary fit); CL-031 to CL-034 (possible overlap signals)",
         validated_intent="INFORMATIONAL (gia vs igi lab diamond, HIGH)", serp_page_type="EDITORIAL_GUIDE (reddit, bluenile /blog/, stienhardt /blogs/education/, plumdiamonds, whiteflash /blog/)",
         overlap_status="CLEAR_OVERLAP", overlap_with="IGI certification blog (OV-01)",
         proposed_role="Education primary home for the GIA-vs-IGI comparison intent (CL-030)",
         action="UPDATE_IN_PLACE", migration_risk="LOW", confidence="MEDIUM",
         evidence="Already in the correct system. Stage 8 comparison SERP validated (HIGH). 0 shared URLs with the general-certification SERP supports narrowing it to the comparison.",
         rationale="Keep in Education and sharpen it to the comparison intent the SERP validates, leaving general certification to the retargeted IGI article. Its URL has the '-house-of-diams' suffix; with no rankings, any slug clean-up is low risk, but that is a Stage 15 URL decision.",
         deferred_question="Stage 15: slug clean-up. Content overlap depth between the two pages is unmeasured (no content audit)."),
    dict(url=BLOGHUB, content_type="BLOG_HUB", business_area="Resources",
         current_role="Lists all 10 articles; no categories or tags",
         important_search_volume="n/a", stage11_clusters="n/a", validated_intent="n/a", serp_page_type="n/a",
         overlap_status="POSSIBLE_OVERLAP", overlap_with="Education hub (OV-12, section-level)",
         proposed_role="Hub for time-bound editorial and brand content, organised by editorial category (13_blog_strategy.md)",
         action="KEEP_BLOG", migration_risk="LOW", confidence="MEDIUM",
         evidence="Stage 12 D-10: Blog stays a distinct system. Stage 13 finding: 0 of the 10 current articles is editorial by type.",
         rationale="Keep the Blog, but under the new role it has no qualifying editorial content yet. Do not relaunch it as an active section until an editorial pipeline exists. Meanwhile it hosts the Education-owned articles that keep their /blog URLs.",
         deferred_question="Should the hub keep listing Education-owned articles that stay at /blog URLs, or link to them only from Education? (Open question in 13_blog_strategy.md.)"),
    dict(url=EDUHUB, content_type="EDUCATION_HUB", business_area="Resources",
         current_role="Hub with 1 article; stated scope (diamonds, craftsmanship, care, buying) unpopulated",
         important_search_volume="n/a", stage11_clusters="n/a", validated_intent="n/a", serp_page_type="n/a",
         overlap_status="POSSIBLE_OVERLAP", overlap_with="Blog hub (OV-12, section-level)",
         proposed_role="Single evergreen home (Stage 12 D-09); structure decided in Stage 14",
         action="NO_ACTION", migration_risk="LOW", confidence="HIGH",
         evidence="Stage 12 D-09.", rationale="Role already decided in Stage 12. 'Craftsmanship' in its stated scope is Blog/brand content under the Stage 13 framework; 'care' stays Education.",
         deferred_question="Stage 14: topic hubs, article inventory, URL depth."),
    dict(url=FAQ, content_type="FAQ", business_area="Brand & Support",
         current_role="Answers legitimacy, lab-vs-natural and certification questions that articles also cover",
         important_search_volume="n/a (no FAQ keyword data)", stage11_clusters="n/a", validated_intent="n/a", serp_page_type="No FAQ-dominant SERP in Stage 8",
         overlap_status="POSSIBLE_OVERLAP", overlap_with="are-real, lab-vs-natural, IGI articles (OV-10)",
         proposed_role="Service/policy answers; one-line topic answers that link to the Education owner (Stage 12 D-18)",
         action="NO_ACTION", migration_risk="LOW", confidence="MEDIUM",
         evidence="Stage 10 OV-10 POSSIBLE; Stage 12 D-18.", rationale="The role was set in Stage 12. Stage 13 adds only that FAQ answers must link to the Education owner of each topic.",
         deferred_question="Stage 15/16: FAQ targeting and links."),
    dict(url=PDP, content_type="PRODUCT_PAGE", business_area="1. Engagement Rings / 10. Diamond Shapes",
         current_role="Only ranking PDP (Oval Marquise Side-Stone Engagement Ring)",
         important_search_volume="marquise oval diamond 390 (pos 90)", stage11_clusters="CL-063",
         validated_intent="TRANSACTIONAL (MEDIUM)", serp_page_type="PRODUCT",
         overlap_status="DISTINCT", overlap_with="Shapes blog article (OV-11 DISTINCT)",
         proposed_role="Commercial PDP (unchanged)", action="NO_ACTION", migration_risk="LOW", confidence="HIGH",
         evidence="Stage 10 ALIGNMENT; Stage 12 D-11 flat PDP URLs.", rationale="Outside the Blog/Education scope. Listed so its ranking is accounted for. Shape content in Education should link to it (Stage 16).",
         deferred_question="None for Stage 13."),
    dict(url=SIDE, content_type="SUBCATEGORY", business_area="1. Engagement Rings",
         current_role="Only ranking category URL; nav-only, misspelled 'by-desgin' segment",
         important_search_volume="side stones engagement rings 1,000 (pos 104)", stage11_clusters="CL-120",
         validated_intent="TRANSACTIONAL (MEDIUM)", serp_page_type="CATEGORY",
         overlap_status="DISTINCT", overlap_with="/engagement-rings parent (OV-17 DISTINCT)",
         proposed_role="Confirmed L2 style subcategory (Stage 12 D-03)", action="NO_ACTION", migration_risk="LOW", confidence="HIGH",
         evidence="Stage 10 ALIGNMENT; Stage 12 D-03.", rationale="Outside the Blog/Education scope. Listed so its ranking is accounted for. Any URL change follows Stage 12/15 migration reasoning.",
         deferred_question="Stage 15: URL (by-desgin segment) with migration reasoning."),
]

for d in DEC:
    i = inv.get(d["url"], {})
    d["title"] = i.get("title", "")
    n, kws, best = kw_summary(d["url"])
    d["ranking_keyword_count"] = n
    d["ranking_keywords"] = kws
    d["best_known_position"] = best

wr("13_existing_content_decisions.csv",
   ["url", "title", "content_type", "business_area", "current_role", "ranking_keyword_count", "ranking_keywords",
    "best_known_position", "important_search_volume", "stage11_clusters", "validated_intent", "serp_page_type",
    "overlap_status", "overlap_with", "proposed_role", "action", "migration_risk", "confidence", "evidence",
    "rationale", "deferred_question"], DEC)

# ------------------------------------------------ 13_content_migration_risk
COMMON_HIGH = ("(1) The Education topic hub that will own the topic is live and indexable; "
               "(2) GSC clicks/impressions and backlink data for this URL have been reviewed; "
               "(3) a 1:1 301 to a single destination that covers the same intent (no merge into a broader page); "
               "(4) the content keeps or improves coverage of every ranking keyword's intent; "
               "(5) internal links, sitemap and canonical updated in the same release; "
               "(6) the move is batched with the rebuild rather than done as a separate change; "
               "(7) rankings for the listed keywords are monitored for 8-12 weeks, with a rollback plan.")
MR = {
    CVD: dict(current_type="BLOG_ARTICLE", proposed_action="UPDATE_IN_PLACE (Education-owned; URL retained)", risk_level="HIGH",
              ranking_equity="19 kw, pos 27-68, ~36.5 ETV (34 of it from two HPHT 8,100 variants at pos 49); 68% of HOD's ranking keywords",
              overlap="POSSIBLE (OV-03 with are-real, one query family); DISTINCT from lab-vs-natural (OV-04)",
              destination_exists="NO (Education lab-grown hub is conceptual; Stage 14)",
              reason="Largest single concentration of HOD equity. Intent aligned. No demonstrated benefit from a path change (competitors rank for this topic on /blog paths). Splitting HPHT/CVD into new pages could fragment the equity.",
              required_conditions=COMMON_HIGH + " (8) Stage 14 has decided whether CL-017/CL-018 get their own pages, so the destination scope is final.",
              decision="DO_NOT_MOVE_NOW — revisit only when all conditions are met"),
    LVN: dict(current_type="BLOG_ARTICLE", proposed_action="UPDATE_IN_PLACE (Education-owned; URL retained)", risk_level="HIGH",
              ranking_equity="3 kw, pos 29-40 (best HOD position after 27); foothold in CL-011 (head 22,200)",
              overlap="POSSIBLE (OV-02 with are-real; OV-10 with FAQ)", destination_exists="NO",
              reason="Aligned with the highest-demand comparison cluster. Equity is small in traffic but strategically placed. Scope boundary with the authenticity page is still open.",
              required_conditions=COMMON_HIGH + " (8) Stage 14 has fixed the boundary between CL-010 and CL-011.",
              decision="DO_NOT_MOVE_NOW — revisit only when all conditions are met"),
    K14: dict(current_type="BLOG_ARTICLE", proposed_action="MOVE_TO_EDUCATION", risk_level="MEDIUM",
              ranking_equity="3 kw, pos 81-95, ~0.17 ETV", overlap="DISTINCT", destination_exists="NO (Education metals home is conceptual)",
              reason="Evergreen, aligned, no overlap, negligible positional equity. Move is justified but must not run ahead of its destination.",
              required_conditions="Education metals home exists; GSC/backlink check shows no hidden equity; 1:1 301; internal links and sitemap updated in the same release; monitor the 3 keywords.",
              decision="PROCEED_WHEN_CONDITIONS_MET"),
    HTC: dict(current_type="BLOG_ARTICLE", proposed_action="DEFER", risk_level="MEDIUM",
              ranking_equity="1 kw, pos 35", overlap="POSSIBLE (OV-06 online-ring guide; OV-07 4Cs sub-topic)", destination_exists="NO",
              reason="Possible overlap with the online-ring guide is unresolved; it holds the only ranking in the buying-guide group.",
              required_conditions="SERP evidence for engagement-ring buying-guide intent (D-19 supplement); Stage 14 buying-guide inventory; if consolidation is chosen, this URL (or its successor via 301) should be the survivor because it holds the ranking.",
              decision="DEFER"),
    REAL: dict(current_type="BLOG_ARTICLE", proposed_action="MOVE_TO_EDUCATION", risk_level="LOW",
               ranking_equity="None in Stage 3", overlap="POSSIBLE (OV-02, OV-03, OV-10)", destination_exists="NO",
               reason="No measured equity; clear Education topic (CL-010) kept distinct from CL-011 by Stage 11 SERP evidence.",
               required_conditions="Education lab-grown hub exists; GSC/backlink check; 301 to the Education authenticity page; link to the lab-vs-natural owner.",
               decision="PROCEED_WHEN_CONDITIONS_MET"),
    FOURC: dict(current_type="BLOG_ARTICLE", proposed_action="MOVE_TO_EDUCATION", risk_level="LOW",
                ranking_equity="None in Stage 3", overlap="POSSIBLE (OV-07, OV-08: shared sub-topic only)", destination_exists="NO",
                reason="No measured equity; evergreen reference.",
                required_conditions="Stage 14 decides overview vs lab-grown-specific scope; Education quality hub exists; GSC/backlink check; 301.",
                decision="PROCEED_WHEN_CONDITIONS_MET"),
    ONLINE: dict(current_type="BLOG_ARTICLE", proposed_action="DEFER", risk_level="LOW",
                 ranking_equity="None in Stage 3", overlap="POSSIBLE (OV-06, OV-08)", destination_exists="NO",
                 reason="Role undecided (separate guide vs consolidation); no SERP evidence for its intent.",
                 required_conditions="D-19 commercial keyword/SERP supplement covering engagement-ring buying queries; Stage 14 buying-guide inventory.",
                 decision="DEFER"),
    SHAPES: dict(current_type="BLOG_ARTICLE", proposed_action="MOVE_TO_EDUCATION", risk_level="LOW",
                 ranking_equity="None in Stage 3", overlap="DISTINCT (OV-09, OV-11)", destination_exists="NO",
                 reason="No measured equity; evergreen shape reference; Stage 8 shows education paths serve 'diamond shape'.",
                 required_conditions="Education shapes hub exists; Stage 14 scope (overview vs engagement-ring chooser); GSC/backlink check; 301.",
                 decision="PROCEED_WHEN_CONDITIONS_MET"),
    RSIZE: dict(current_type="BLOG_ARTICLE", proposed_action="MOVE_TO_EDUCATION", risk_level="LOW",
                ranking_equity="None in Stage 3", overlap="DISTINCT (OV-09)", destination_exists="NO",
                reason="No measured equity; evergreen utility.",
                required_conditions="Stage 14 decides article vs TOOL page; GSC/backlink check; 301.",
                decision="PROCEED_WHEN_CONDITIONS_MET"),
    IGI: dict(current_type="BLOG_ARTICLE", proposed_action="RETARGET (and home in Education)", risk_level="LOW",
              ranking_equity="None in Stage 3", overlap="CLEAR_OVERLAP (OV-01) with the GIA-vs-IGI Education article; cannibalization not demonstrated",
              destination_exists="PARTIAL (/education exists; certification topic hub is conceptual)",
              reason="SERPs separate comparison from general certification (0 shared URLs), so differentiation, not a merge, resolves the overlap.",
              required_conditions="Stage 14 picks the target (CL-033 general vs CL-032 IGI-specific); remove duplicated GIA-vs-IGI comparison content; cross-link both pages; GSC/backlink check; 301 if the URL moves.",
              decision="PROCEED_WHEN_CONDITIONS_MET"),
    GIAIGI: dict(current_type="EDUCATION_ARTICLE", proposed_action="UPDATE_IN_PLACE", risk_level="LOW",
                 ranking_equity="None in Stage 3", overlap="CLEAR_OVERLAP (OV-01)", destination_exists="YES (already in /education)",
                 reason="Already in the correct system; narrow to the validated comparison intent.",
                 required_conditions="IGI article retargeted in the same release so both pages do not keep covering the same ground.",
                 decision="PROCEED"),
    BLOGHUB: dict(current_type="BLOG_HUB", proposed_action="KEEP_BLOG", risk_level="LOW", ranking_equity="None",
                  overlap="POSSIBLE (OV-12)", destination_exists="YES", reason="Hub URL stays; its role changes.",
                  required_conditions="Editorial categories only after editorial content exists (no empty category pages, Stage 12 D-13).",
                  decision="PROCEED"),
    EDUHUB: dict(current_type="EDUCATION_HUB", proposed_action="NO_ACTION", risk_level="LOW", ranking_equity="None",
                 overlap="POSSIBLE (OV-12)", destination_exists="YES", reason="Role set in Stage 12 D-09; structure is Stage 14.",
                 required_conditions="n/a", decision="NOT_APPLICABLE (Stage 14)"),
    FAQ: dict(current_type="FAQ", proposed_action="NO_ACTION", risk_level="LOW", ranking_equity="None",
              overlap="POSSIBLE (OV-10)", destination_exists="YES", reason="Role set in Stage 12 D-18.",
              required_conditions="n/a", decision="NOT_APPLICABLE (Stage 15/16)"),
    PDP: dict(current_type="PRODUCT_PAGE", proposed_action="NO_ACTION", risk_level="LOW",
              ranking_equity="1 kw, pos 90 (390)", overlap="DISTINCT (OV-11)", destination_exists="YES",
              reason="Not content; no Stage 13 migration. Listed for equity completeness.",
              required_conditions="n/a", decision="NOT_APPLICABLE"),
    SIDE: dict(current_type="SUBCATEGORY", proposed_action="NO_ACTION", risk_level="LOW",
               ranking_equity="1 kw, pos 104 (1,000); only ranking category URL", overlap="DISTINCT (OV-17)", destination_exists="YES",
               reason="Not content; URL questions belong to Stage 15 (D-03). Low positional equity but strategically important.",
               required_conditions="Stage 15 migration reasoning for any URL change.", decision="NOT_APPLICABLE (Stage 15)"),
}
mr_rows = [dict(url=d["url"], **MR[d["url"]]) for d in DEC]
wr("13_content_migration_risk.csv",
   ["url", "current_type", "proposed_action", "risk_level", "ranking_equity", "overlap", "destination_exists",
    "reason", "required_conditions", "decision"], mr_rows)

# ------------------------------------------------ 13_blog_education_framework
E, B = "EDUCATION", "BLOG"
FW = [
    ("Lab-grown science & process (what they are, how made)", E, "Blog may cover dated industry/process news and link here", "EVERGREEN", "INFORMATIONAL",
     "what are lab-grown diamonds; how lab diamonds are made", "Reference question with a stable answer", "Stage 11 CL-002, CL-015 INFORMATIONAL; Stage 12 D-06", ""),
    ("Growth-method comparison (CVD vs HPHT; single-method CVD / HPHT)", E, "None", "EVERGREEN", "INFORMATIONAL",
     "CVD vs HPHT; what is an HPHT diamond", "EDITORIAL_GUIDE SERPs; HOD's main ranking equity", "Stage 8 CL-016 EDITORIAL_GUIDE x11; Stage 3 19 rankings", "Existing article stays at its /blog URL for now (HIGH migration risk)."),
    ("Origin comparison (lab-grown vs natural)", E, "Blog may run opinion/market pieces that link here", "EVERGREEN", "INFORMATIONAL / COMMERCIAL_RESEARCH",
     "lab-grown vs natural diamonds", "Decision-support comparison", "Stage 8 COMPARISON SERP (22,200); Stage 11 CL-011 HIGH", "Existing article stays at its /blog URL for now (HIGH migration risk)."),
    ("Authenticity & trust (are lab-grown real, fake, synthetic)", E, "FAQ gives a one-line answer and links here", "EVERGREEN", "INFORMATIONAL",
     "are lab-grown diamonds real", "Trust question with stable answer; high demand", "Stage 8 COMPARISON SERP (14,800); Stage 11 CL-010 vs CL-011 RELATED_BUT_DISTINCT", ""),
    ("Lab-grown value, pricing & resale", E, "Blog for dated market/price-trend commentary", "EVERGREEN (principles) / TIMEBOUND (prices)", "INFORMATIONAL / COMMERCIAL_RESEARCH",
     "do lab-grown diamonds hold value; are lab diamonds cheaper", "Principles are evergreen; price levels date quickly", "Stage 11 CL-008, CL-009 (no validated SERP)", "Education should avoid hard-coded prices that date; dated price commentary goes to Blog."),
    ("Ethics & sustainability explainers", E, "Blog for HOD's own sourcing/making stories", "EVERGREEN", "INFORMATIONAL",
     "are lab-grown diamonds ethical; conflict-free diamonds", "Explainer is reference; brand practice is editorial", "Stage 11 CL-013, CL-073 (POSSIBLE_OVERLAP, no SERP)", "Brand claims need substantiation (trust principle)."),
    ("Industry history & market trends", B, "Evergreen history facts may sit in Education", "TIMEBOUND", "INFORMATIONAL",
     "lab-grown market developments; notable stones", "News/trend framing is time-bound", "Stage 11 CL-014 (13 kw; 'lab grown diamond trends' 20)", "Low measured demand; editorial value, not search-led."),
    ("Diamond certification & grading reports", E, "None; Blog links to it", "EVERGREEN", "INFORMATIONAL / COMMERCIAL_RESEARCH",
     "GIA vs IGI; what an IGI report means", "Reference; OV-01 is the case this rule prevents", "Stage 8 two certification SERPs, 0 shared URLs; Stage 10 OV-01", "One comparison page and one general certification page, both Education."),
    ("4Cs & quality grades", E, "None", "EVERGREEN", "INFORMATIONAL / COMMERCIAL_RESEARCH",
     "clarity grades; colour scale; VS vs SI", "Reference", "Stage 8 EDITORIAL_GUIDE (CL-041 HIGH); Stage 11 12 clusters", ""),
    ("Diamond shapes & cuts reference", E, "Blog for dated shape-trend pieces", "EVERGREEN", "INFORMATIONAL",
     "diamond shapes; asscher vs emerald", "Reference; education paths serve the SERP", "Stage 8 'diamond shape' (60,500) EDITORIAL_GUIDE", "Shape shopping is a commercial filter (Stage 12 D-08)."),
    ("Metals & materials", E, "None", "EVERGREEN", "INFORMATIONAL / COMMERCIAL_RESEARCH",
     "14k vs 18k gold; platinum vs white gold", "Reference comparison", "Stage 8 CL-110 EDITORIAL_GUIDE; Stage 3 3 rankings", ""),
    ("Buying guides (how to choose, what to look for, is it worth it)", E, "Blog seasonal gift guides link to them", "EVERGREEN", "COMMERCIAL_RESEARCH",
     "how to choose a lab-grown diamond", "Decision support; bridge to category pages", "Stage 11 CL-012, CL-024; Stage 10 OV-06/07/08", "One guide per distinct buyer decision; count set in Stage 14."),
    ("Ring sizing & practical tools", E, "None", "EVERGREEN", "INFORMATIONAL",
     "find your ring size; resizing", "Utility reference", "Stage 11 CL-124; Stage 12 TOOL page type (conditional)", "Size-finding demand not in master DB."),
    ("Jewellery care & maintenance", E, "Blog for seasonal care reminders that link here", "EVERGREEN", "INFORMATIONAL",
     "how to clean a diamond ring", "Reference", "Stage 10: Education hub states 'care' in scope; Stage 11 CL-115 wear/tarnish", "Keyword coverage thin; confirm in Stage 14."),
    ("Testing & identification", E, "None", "EVERGREEN", "INFORMATIONAL",
     "do lab diamonds pass a tester", "Reference question", "Stage 11 CL-020, CL-021, CL-022", "Tester shopping (TRANSACTIONAL) is not HOD's business; do not target it."),
    ("Gemstones & diamond alternatives", E, "None", "EVERGREEN", "INFORMATIONAL",
     "moissanite vs diamond", "Reference comparison", "Stage 11 13 clusters; Stage 12 INDEXABLE_CONDITIONAL", "CONDITIONAL: business relevance unconfirmed."),
    ("Jewellery trends & seasonal style", B, "Links to Education for concepts and to categories for products", "TIMEBOUND", "INFORMATIONAL (editorial)",
     "this season's engagement-ring trends", "Dated by nature", "Stage 12 D-10; business catalogue (Stage 1)", "Demand unmeasured in the keyword universe."),
    ("Styling & how to wear", B, "If a styling question proves evergreen with a stable SERP, it moves to Education Ring & Jewellery Guides", "TIMEBOUND or EVERGREEN (case by case)", "INFORMATIONAL",
     "stacking bands; pairing earrings", "Mostly editorial and visual", "Catalogue: rings, earrings, necklaces, bracelets, bands (Stage 1)", "Decide per topic using the tests in 13_blog_strategy.md."),
    ("Gift guides & occasions", B, "Links to categories/products", "TIMEBOUND (seasonal)", "COMMERCIAL_RESEARCH (seasonal)",
     "anniversary gift ideas; holiday gifts", "Seasonal, refreshed each year", "Business context; no seasonal keywords measured", "Reuse one URL per recurring occasion, updated each year, rather than a new URL per year."),
    ("Craftsmanship & making-of (Surat workshop)", B, "Bespoke page links to it; Education may cite it", "EVERGREEN-ISH brand", "INFORMATIONAL (brand)",
     "how a HOD ring is made", "Brand differentiation, trust and experience signals", "CLAUDE.md business context (Surat manufacturing); Education hub scope lists 'craftsmanship' (Stage 10)", "Stage 13 moves 'craftsmanship' from Education scope to Blog/brand."),
    ("Brand stories & behind the scenes", B, "About page may link", "TIMEBOUND", "NAVIGATIONAL / brand",
     "founder story; studio news", "Brand, not search-led", "Stage 12 D-10", ""),
    ("Product launches & collection stories", B, "Must link to the live category/collection", "TIMEBOUND", "INFORMATIONAL / COMMERCIAL",
     "new collection launch", "Dated announcements", "Stage 12 D-10; D-14 curated collections (T-Bar, Hip Hop)", "The launch post never replaces the category page."),
    ("Bespoke client stories / case studies", B, "Bespoke service page links to them", "TIMEBOUND", "COMMERCIAL_RESEARCH",
     "a custom ring commission", "Experience evidence for the Bespoke service", "Stage 1 /bespoke exists; Stage 11 no bespoke keywords", "FUTURE POSSIBILITY: needs client consent and real commissions."),
    ("Commercial product/category shopping", "COMMERCIAL PAGES", "Blog and Education link in; never host", "PERMANENT", "TRANSACTIONAL / COMMERCIAL",
     "side stone engagement rings; lab-grown diamonds (head)", "SERPs are category/product pages", "Stage 8 CATEGORY/PRODUCT SERPs; Stage 12 D-05, D-03", "Neither Blog nor Education targets shopping queries."),
    ("Service & policy questions", "FAQ / SUPPORT", "Links to Education for topic depth", "PERMANENT", "INFORMATIONAL (support)",
     "shipping, returns, resizing policy", "Support content", "Stage 12 D-18; Stage 10 OV-10", ""),
]
wr("13_blog_education_framework.csv",
   ["topic_type", "primary_home", "secondary_role", "evergreen_or_timebound", "search_intent", "example_topics",
    "reason", "evidence", "notes"],
   [dict(zip(["topic_type", "primary_home", "secondary_role", "evergreen_or_timebound", "search_intent",
              "example_topics", "reason", "evidence", "notes"], r)) for r in FW])

print("written:", len(DEC), "decisions;", len(eq_rows), "equity rows;", len(mr_rows), "risk rows;", len(FW), "framework rows")
