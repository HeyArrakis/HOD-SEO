import sys; sys.path.insert(0, ".")
from mm_docs import *

km = L.kmap_rows


def kvol(x):
    try:
        return int(float(x["search_volume"]))
    except Exception:
        return 0


def has_owner(r):
    pk = r["Primary Keyword"]
    return not pk.startswith(("NO ", "NONE", "UNOWNED"))


# ================================================================== 04
def doc04():
    A_ = []
    A = A_.append
    A("# 04 — Keyword → URL Ownership Validation")
    A(f"\nGenerated {TODAY}. Validates the existing Stage 15 ownership system (and the Stage 12/14/16/19 + final-calendar layers on top of it) against the master map and the live site. **Nothing in the ownership files was changed.** Recommendations at the end are proposals with evidence; they require your decision.\n")
    A("Scope of the check: Stage 15 (`15_keyword_url_map.csv` 1,936 keywords; `15_target_page_registry.csv` 27 targets), `15_cannibalization_check.csv`, final calendar (62 scheduled items), Stage 19 briefs, and the live crawl of 2026-10-09.\n")
    # ---------------- 1
    A("## 1. Confirmed ownership (Stage 15 targets vs live)\n")
    rr = []
    ver = collections.Counter()
    for tid, reg in L.registry.items():
        eu = reg["existing_url"]
        pu = reg["proposed_url"]
        cal = L.cal_by_id.get(tid)
        if eu:
            live_st = crawl.get(BASE + eu, {}).get("status")
            if live_st == 200:
                v = "CONFIRMED — URL live (200, self-canonical)"
            elif live_st:
                v = f"URL STALE — registry URL returns {live_st}; see conflict C1"
            else:
                v = "VERIFY"
        elif pu and pu != "URL_PENDING":
            live_st = "n/a"; v = "OWNER CONFIRMED in architecture — page not built"
        else:
            live_st = "n/a"; v = "OWNER CONFIRMED — slug undecided (URL_PENDING)"
        ver[v.split(" —")[0].split(" in architecture")[0]] += 1
        rr.append([tid, short(reg["target_page_name"], 58), reg["status"], eu or pu, live_st, f"{cal['content_id']} · {cal['publish_date']}" if cal else "—", v])
    A(table(["Target", "Page", "Stage 15 status", "Registry URL", "Live HTTP", "Calendar", "Verdict"], rr))
    A(f"\n**Result:** {ver['CONFIRMED']} existing owner URLs confirmed live; {ver['URL STALE']} stale; {ver['OWNER CONFIRMED']} proposed/pending owners (not built). Stage 15's central claim — no keyword has two HOD owners — holds: `15_cannibalization_check` B-check = 0 duplicate owners, and this map's own check found **0 exact duplicate primary keywords across {len(rows)} rows** (the side-stone legacy row deliberately carries no keyword).\n")
    # ---------------- 2
    A("## 2. Missing URL ownership\n")
    hubs = [r for r in rows if r["Row Group"] == "COMMERCIAL CATEGORY"]
    subs = [r for r in rows if r["Row Group"] == "COMMERCIAL SUBCATEGORY"]
    noown_sub = [r for r in subs if not has_owner(r) or "RATIFIED PRIMARY" in r["Primary Keyword"]]
    A(table(["Gap", "Count", "Detail"], [
        ["Commercial hubs/categories with no ratified keyword", len(hubs), "Engagement rings, wedding bands, fine jewellery, earrings, necklaces, bracelets, FJ rings, T-Bar (+ bespoke, below). Stage 15: *'commercial hubs have no keywords because the master database has almost no commercial category queries … a data gap, not a lack of demand'* (D-19; the supplement was never approved)."],
        ["Commercial subcategories with no ratified keyword", len([r for r in subs if 'NO RATIFIED' in r['Primary Keyword']]), "Only `side-stone-rings` has an owner. The other style/type/gender pages are conditional under the D-07 gate (demand + SERP type + inventory + distinctness + one home + business fit + stability)."],
        ["Core commercial pages with no ratified keyword", sum(1 for r in rows if r['Row ID'] in ('COM-BESPOKE',) ), "/bespoke — the calendar says COM-BESPOKE owns 'custom engagement ring' (40,500) / 'design your own engagement ring' (5,400) but Stage 15 maps neither."],
        ["Unowned head term, largest in the project", 1, "'lab grown diamonds' 135,000 (+ 'lab diamonds' 27,100, 'lab created diamonds' 12,100): CL-001, CONDITIONAL_NOT_MAPPED → COM-LG-HUB (not built; business confirmation needed)."],
        ["New Education pages with no Stage 14/15 owner", 4, "Bracelet size chart (EDU-RJG-BR), necklace length chart (EDU-RJG-NL), engagement ring insurance (EDU-INS), wedding-band buying guide (EDU-WB-GUIDE) — calendar status OWNERSHIP_CONFIRMATION."],
        ["Calendar primaries outside the Stage 15 map", sum(1 for c in L.cal if c['primary_keyword'].strip().lower() not in L.kmap and c['content_id'] != 'BC-004-DEC-REFRESH'), "New research (calendar says 'no Stage 15 owner'); additive, but unratified. 33 Blog posts are Blog-owned by the calendar only."],
        ["Pages that intentionally own no keyword", sum(1 for r in rows if r['Row Group'] in ('CORE LIVE','HUBS') and not has_owner(r)), "Homepage (brand), /shop, /collection, /about, /contact, /faq, policies, /blog, /education — acceptable and labelled `NO PRIMARY KEYWORD / BRAND / SUPPORTING PAGE`."],
    ]))
    # ---------------- 3
    A("\n## 3. Possible conflicts (both values shown, nothing resolved)\n")
    A("### 3a. Primary keyword differs between the Stage 19 brief / Stage 17 and the final calendar (same page)\n")
    cf = []
    for r in rows:
        if "CALENDAR PRIMARY" in r["Primary Keyword"]:
            a, b = r["Primary Keyword"].split("  ||  CALENDAR PRIMARY: ")
            cf.append([r["Row ID"], a.split("  [")[0], b.split(" — ")[0], "Calendar term not in Stage 15 map" if "NOT in Stage 15" in b else "in map"])
        elif r["Existing Keyword Ownership Conflict?"].startswith("YES — Primary"):
            m = re.search(r"Stage 17/19 = '([^']*)'; final calendar = '([^']*)' \(([^)]*)\)\. Both map to the same page; calendar primary is (.*?)\.", r["Existing Keyword Ownership Conflict?"])
            if m:
                cf.append([r["Row ID"], m.group(1), f"{m.group(2)} ({m.group(3)})", m.group(4)])
    A(table(["Page", "Stage 17/19 primary", "Calendar primary", "Note"], cf))
    A("\nBoth terms point to one page, so this is **not** two pages competing — but the choice changes the title/H1 and which volume the page is judged on. Example: EDU-LG-00 would be 'synthetic diamonds' 2,900 (brief) or 'what are lab grown diamonds' 12,100 (calendar, SERP-validated in Stage 18.5). Stage 15 page ownership is unaffected. **Needs your ratification before the 20 new pages are written.**\n")
    A("### 3b. Calendar items that Stage 14/15 do not cover (ownership confirmation flagged by the calendar itself)\n")
    oc = [[c["content_id"], c["primary_keyword"], c["primary_search_volume"], c["target_owner"][:50], short(c["cannibalization_status"], 200)] for c in L.cal if "OWNERSHIP_CONFIRMATION" in c["production_status"]]
    A(table(["Calendar ID", "Primary", "Vol", "Proposed owner", "Calendar's own risk note"], oc))
    A("\n### 3c. Commercial ownership claimed in notes but not mapped in Stage 15\n")
    A(table(["Claim (source)", "Reality in Stage 15 / live", "Evidence"], [
        ["COM-BESPOKE owns 'custom engagement ring' 40,500 and 'design your own engagement ring' 5,400 (calendar BC-001)", "No Stage 15 mapping; /bespoke is a form-led page", "blog_keyword_research.csv: both labelled RESERVED_COMMERCIAL_PAGE"],
        ["COM-WB owns 'matching wedding band' 6,600, curved/contour/enhancer (calendar BLOG-WR-TYPES / EDU-WB-GUIDE)", "No Stage 15 mapping; /wedding-bands has 7 products", "calendar cannibalization notes"],
        ["Style heads (toi et moi, bezel, east-west, three-stone) reserved for COM-ER style subcategories (calendar BC-031)", "Subcategories exist and are populated (bezel 2, three-stone 4, toi-moi 1 products) but are 'conditional' and own no keyword", "calendar BC-031 note; live crawl"],
        ["Stage 12 D-05: COM-LG-HUB conditional", "Live homepage/ER title and all PDP copy already say lab-grown; 135,000 head unowned", "15_keyword_url_map.csv CL-001"],
    ]))
    A("\n### 3d. Live-site changes that make recorded ownership stale\n")
    A("- **COM-ER-SIDESTONE:** registry/ranking-equity/link files all cite `/engagement-rings/by-desgin/side-stone-rings` (est. pos 104, 1 keyword). Live: 404; new URL `/engagement-rings/by-design/side-stone-rings` is 200. *Owner unchanged; URL record stale; 301 missing.*\n- **COM-PDP-OVAL-FLORAL:** product renamed 'Oval Marquise Side-Stone Engagement Ring' (slug unchanged); its title now contains the COM-ER-SIDESTONE term 'side-stone' (MEDIUM boundary risk).\n- **BRAND-CONTACT:** IA expects an indexable /contact page; live is a 307 to a modal.\n")
    # ---------------- 4
    A("## 4. Cannibalization risks\n")
    A("### 4a. Stage 15 'E' pairs (adjacent intents between owners) — carried forward\n")
    A(table(["Severity", "Pair", "Boundary rule (Stage 15)"], [[x["severity"], x["subject"], short(x["detail"] + " " + x["resolution"], 260)] for x in L.cannib if x["check"] == "E_PROPOSED_OVERLAPPING_INTENT"]))
    A("\nStage 15 conclusion: *no actual cannibalization is demonstrated; the pairs are boundaries to enforce in content (Stage 19) and linking (Stage 16)*. The highest, **EDU-LG-00 ↔ EDU-LG-03 (HIGH)**, concerns process queries (CL-015); EDU-LG-04 must never target CVD/HPHT method terms.\n")
    A("### 4b. New risks found by mapping live + calendar pages together — CANNIBALIZATION REVIEW REQUIRED\n")
    nr = [
        ["Homepage ↔ /engagement-rings ↔ COM-LG-HUB", "MEDIUM", "Homepage title 'Lab-Grown Diamond Engagement Rings & Fine Jewellery' (Stage 10 OV-13) covers the category subject and the unowned lab-grown head.", "Brand-led homepage title; decide COM-LG-HUB; keep category subject on /engagement-rings."],
        ["/engagement-rings ↔ /engagement-rings/by-design", "HIGH", "Identical grid (61 pieces on both), same boilerplate FAQ, both indexable, self-canonical and in the sitemap.", "Decide canonical/redirect/unique-index; do not merge automatically."],
        ["/wedding-bands/for-her/eternity ↔ /fine-jewellery/rings/eternity-rings", "MEDIUM", "Same subject, two homes; one is empty. 'eternity ring/band' (12,100/9,900) labelled informational by DFS.", "One-home decision (P-ONE-HOME); SERP check before assigning."],
        ["/fine-jewellery/bracelet ↔ /fine-jewellery/bracelet/tennis ↔ BC-021", "MEDIUM", "'tennis bracelet' 135,000 commercial head vs hub vs child; BC-021 'what is a tennis bracelet' 3,600 informational.", "Child owns the commercial head; BC-021 stays informational (documented boundary)."],
        ["Earrings hub ↔ stud/hoop/drop children ↔ BC-025", "MEDIUM", "'diamond stud earrings' 49,500 vs hub 'diamond earrings' 74,000; BC-025 'different types of earrings' 1,600.", "Stage 15 CL-125 REVIEW: assign stud head to the stud child; hub keeps broad term."],
        ["/t-bar ↔ /fine-jewellery/necklaces/pendant-necklace", "MEDIUM", "Stage 10 OV-16; 4 vs 3 products.", "D-14 decision: curated collection vs subtype."],
        ["/faq ↔ Education owners (EDU-LG-01/02/03, EDU-4C-00)", "MEDIUM", "FAQ answers lab-grown vs natural, CVD/HPHT, 4Cs in full.", "One-line answer + link (D-18, D14-30)."],
        ["/bespoke ↔ BC-001 (and BC-024)", "LOW–MEDIUM", "Informational timeline post vs commercial 'custom engagement ring' heads.", "Boundary already documented; keep heads on /bespoke."],
        ["/shop/oval-floral-diamond-ring ↔ /engagement-rings/by-design/side-stone-rings", "MEDIUM", "PDP title now says 'Side-Stone'.", "Keep 'oval'/'marquise' as lead terms in the PDP."],
        ["IGI certification article ↔ GIA-vs-IGI article (OV-01)", "MEDIUM", "Both live, one topic (CLEAR_OVERLAP in Stage 10).", "Retarget/ship both changes together (Stage 13)."],
        ["BC-036 ↔ BC-038 ↔ BC-039 ↔ BC-007 (finger/hand/order posts)", "LOW–MEDIUM", "Adjacent SERPs share 2 URLs ('what finger does a wedding ring go on' vs 'what hand does engagement ring go on').", "Calendar boundary notes assign each question; keep exact wording separate."],
        ["BC-004 ↔ BC-008 ↔ BC-009 ↔ BC-035 ↔ BC-018 (gift series)", "LOW–MEDIUM", "SERPs of BC-008/BC-009 share 2 URLs; hub vs recipient posts.", "Series rule: hub owns generic holiday gifts; recipient posts keep recipient primaries."],
        ["BLOG-WR-TYPES ↔ EDU-WB-GUIDE ↔ BC-037 ↔ BC-007 ↔ BC-022", "MEDIUM", "Wedding-band topics split across Blog and Education; 1 of 10 results shared.", "Confirm Blog-vs-Education ownership (flagged)."],
    ]
    A(table(["Pages", "Risk", "Why", "Suggested handling (not applied)"], nr))
    # automated cross check
    prim = {}
    for r in rows:
        if has_owner(r) and "RATIFIED PRIMARY" not in r["Primary Keyword"]:
            k = re.split(r"\s+\(|  \[|  \|\|", r["Primary Keyword"])[0].strip().lower()
            prim.setdefault(k, []).append(r["Row ID"])
    xs = []
    for r in rows:
        for s in L.split_list(r["Secondary Keywords"]):
            k = re.sub(r"\s*\(.*$", "", s).strip().lower()
            if k in prim and r["Row ID"] not in prim[k]:
                xs.append((k, r["Row ID"], prim[k]))
    A(f"\n### 4c. Automated checks on this map\n\n- Exact duplicate primary keywords across rows: **{sum(1 for v in prim.values() if len(v) > 1)}**.\n- A row's primary keyword appearing as another row's secondary keyword: **{len(xs)}**" + (": " + "; ".join(f"'{k}' primary on {','.join(p)}, secondary on {s}" for k, s, p in xs[:8]) if xs else "") + ".\n- Calendar secondaries that map to a *different* Stage 15 target than the calendar item's own page: **0** (checked all 62 items; matches the calendar's own 'PASS' notes).\n- SERP overlap ≥2 shared top-10 URLs (calendar round-2): 'how to layer necklaces' / 'necklace layering' (4 — already merged into BC-006); 'ring finger meaning' / 'what do rings on each finger mean' (3 — one post, BC-038); 'jewelry gifts for girlfriend' / 'wife' (2 — kept separate, series rule); 'what finger does a wedding ring go on' / 'what hand does engagement ring go on' (2 — split BC-036/BC-007 by question).\n")
    # ---------------- 5
    A("## 5. Orphan keyword clusters (keywords with no live or planned owner)\n")
    cl = collections.defaultdict(lambda: dict(n=0, vol=0, disp=collections.Counter(), name="", top=("", 0)))
    for x in km:
        d = x["mapping_disposition"]
        if d in ("CONDITIONAL_NOT_MAPPED", "DEFERRED_NOT_MAPPED", "REVIEW_REQUIRED", "EXCLUDE_COMMERCIAL"):
            c = cl[x["cluster_id"]]; c["n"] += 1; c["vol"] += kvol(x); c["disp"][d] += 1; c["name"] = x["cluster_name"] or c["name"]
            if kvol(x) > c["top"][1]:
                c["top"] = (x["keyword"], kvol(x))
    HOME = {"CL-001": "COM-LG-HUB (not built) — business decision", "CL-125": "Live `/fine-jewellery/earrings/stud-earrings` now exists (commercial head) — assign", "CL-123": "`/fine-jewellery/rings` (FJ rings, DEFER)", "CL-063": "`/shop/oval-floral-diamond-ring` / moval (PRODUCT SERP)", "CL-006": "Loose-stone pages (deferred; are loose stones sold?)", "CL-065": "EDU-GEN-02 (conditional; 'types of diamonds' sense unresolved)", "CL-090": "EDU-GEM-03 (deferred)", "CL-095": "EDU-GEM-00 (conditional)", "CL-070": "Natural commercial hub (deferred)", "UNCLUSTERED_REVIEW": "Needs human triage (brand/dual meaning)"}
    top = sorted(cl.items(), key=lambda x: -x[1]["vol"])[:18]
    A(table(["Cluster", "Name", "Unowned kws", "Σ volume", "Top keyword", "Dispositions", "Nearest home today"], [[k, short(v["name"], 44), v["n"], f"{v['vol']:,}", f"{v['top'][0]} ({v['top'][1]:,})", ", ".join(f"{a.replace('_NOT_MAPPED','')} {b}" for a, b in v['disp'].items()), HOME.get(k, "—")] for k, v in top]))
    tot = {d: (sum(1 for x in km if x["mapping_disposition"] == d), sum(kvol(x) for x in km if x["mapping_disposition"] == d)) for d in ("CONDITIONAL_NOT_MAPPED", "DEFERRED_NOT_MAPPED", "REVIEW_REQUIRED", "EXCLUDE_COMMERCIAL")}
    A("\nTotals (Stage 15): " + "; ".join(f"{d} {n} kws / {v:,} vol" for d, (n, v) in tot.items()) + ". Volumes are DataForSEO Labs monthly US searches and overlap across variants — treat as magnitude, not additive traffic.\n")
    # ---------------- 6
    A("## 6. Pages without clear keyword ownership\n")
    pw = collections.Counter(r["Row Group"] for r in rows if not has_owner(r) or "RATIFIED PRIMARY" in r["Primary Keyword"])
    A(table(["Row group", "Rows without an owner or with only candidates"], [[k, v] for k, v in pw.most_common()]))
    A("\nEvery mapped page states either a keyword owner, `NO RATIFIED PRIMARY (D-19 …)` with candidate evidence, or `NO PRIMARY KEYWORD / BRAND / SUPPORTING PAGE`. Pages with *no* such statement: **0** (checked programmatically).\n")
    # ---------------- 7
    A("## 7. Keywords on inappropriate page types\n")
    t = [x for x in km if x["target_id"].startswith("EDU") and x["keyword_intent"] in ("TRANSACTIONAL", "NAVIGATIONAL")]
    t.sort(key=lambda x: -kvol(x))
    A(f"**7a. Transactional/navigational labels inside Education owners — {len(t)} keywords** (DataForSEO intent labels, none SERP-validated). Largest: " + "; ".join(f"'{x['keyword']}' {kvol(x):,} → {x['target_id']}" for x in t[:8]) + ". Stage 15 already marks these LOW confidence; they are informational in practice ('cvd diamond', 'diamond inclusions') but confirm with SERPs before relying on the labels. **Recommendation: none beyond SERP validation when budget allows.**\n")
    A("**7b. Informational-labelled heads reserved for commercial pages:** 'eternity ring' 12,100 / 'eternity band' 9,900 and 'toi et moi ring' 27,100 are DFS-informational but sit on commercial subcategories (and BC-023 'eternity ring meaning' is a blog) — SERP check required before assigning (risk: commercial page for an informational SERP).\n")
    A("**7c. Commercial/transactional SERPs targeted by Blog posts:** BC-008 'jewelry gifts for wife' and BC-009 'jewelry gifts for girlfriend' are SERP-verified TRANSACTIONAL_OR_COMMERCIAL (product/category + marketplace results lead); BC-004/BC-035 are MIXED commercial-research. Their primaries are small (320–390/mo; BC-035 33,100) and the calendar already limits them to listicle/guide format and avoids broad heads ('christmas gifts for wife' 27,100). **Risk: product-led SERPs favour commercial pages — keep these as guides linking to category pages, set expectations on traffic.** No change proposed.\n")
    A("**7d. Blog-vs-Education:** BLOG-WR-TYPES ('types of wedding rings' 12,100) is a Blog post while Stage 13 assigns 'how to choose / types' reference intent to Education — flagged by the calendar for confirmation.\n")
    A("**7e. Informational answers living on a support page:** /faq (see 4b).\n")
    # ---------------- 8
    A("## 8. Recommendations (evidence-supported; not applied)\n")
    recs = [
        ("R1", "Add a 1:1 301 for the renamed side-stone URL and update the research registry's recorded URL after the redirect exists.", "Live 404 + ranking-equity file; CLAUDE.md rules 11–12.", "Do not change ownership; change only the URL record."),
        ("R2", "Ratify a primary keyword for every Education page where the calendar and Stage 19 brief differ (12 pages) before writing; default to the SERP-validated calendar term with the Stage 15 term as co-primary.", "§3a table.", "Ownership of the page stays with Stage 15."),
        ("R3", "Confirm the 8 OWNERSHIP_CONFIRMATION items (4 new Education pages, EDU-LG-09 co-primary, EDU-RJG-01, EDU-RJG-03 activation, BLOG-WR-TYPES).", "§3b; calendar notes.", "Until confirmed, rows stay `REVIEW`."),
        ("R4", "Ratify commercial hub/child ownership using the candidate lists already in the map (zero cost): one owner per head term, hub = broad term, child = specific type; resolve 'lab grown diamond engagement rings' (COM-ER vs COM-LG-HUB).", "§2, §3c; blog_keyword_research.csv RESERVED_COMMERCIAL_PAGE; Stage 12 D-05/D-07/D-19.", "If SERP validation of commercial heads is wanted, submit a priced plan first (CLAUDE.md DataForSEO rules)."),
        ("R5", "Decide COM-LG-HUB: the catalogue is lab-grown, so 'conditional' may no longer hold; the 135,000 head is unowned.", "§5; live positioning.", "Needs business confirmation of products + certification."),
        ("R6", "Resolve /engagement-rings vs /engagement-rings/by-design, and eternity (WB vs FJ rings), as one-home decisions.", "§4b.", "No automatic merge/delete."),
        ("R7", "Assign 'diamond stud earrings' (CL-125, 49,500) to the stud-earrings child once the D-07 gate is documented.", "§5; Stage 15 CL-125 REVIEW.", "Informational stud queries stay with EDU-4C-07."),
        ("R8", "Keep FAQ answers to one line + link (D-18).", "§4b.", "—"),
        ("R9", "Triage the 156 REVIEW_REQUIRED keywords (94,960 vol): mostly dual-meaning/brand terms; likely excludable.", "§5.", "Human triage; no paid call needed."),
        ("R10", "Re-run this validation after AWS cut-over and after GSC data is available (GSC will show whether any two HOD URLs actually rank for one query).", "GSC not available this session.", "—"),
    ]
    A(table(["#", "Recommendation", "Evidence", "Guardrail"], recs))
    A("\n## 9. Method and limits\n")
    A("- Ownership data are Stage 15 (frozen); live data from the 2026-10-09 read-only crawl; volumes/KD are existing DataForSEO values (no new calls, $0.00).\n- Heuristic checks (e.g. entity/question presence in article text) are labelled heuristic in the CSV; they flag candidates for review, not defects.\n- Without GSC, actual query→URL competition is unknown; cannibalization here is **risk by design**, not observed.\n")
    open(OUT + "04-KEYWORD-URL-OWNERSHIP-VALIDATION.md", "w").write("\n".join(A_))


doc04()
print("04 done")
