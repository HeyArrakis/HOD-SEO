# -*- coding: utf-8 -*-
"""Disk-based QC for the Step 2 package (2A/2B + correction pass 2026-10-10). Read-only. Prints PASS/FAIL; exit code 1 on any FAIL."""
import csv, re, collections, os, glob, json, sys, subprocess, time, datetime
ROOT = "/Users/manavdesai/Desktop/HOD SEO"
OUT = ROOT + "/On-page SEO"
KW = ROOT + "/Keywords/content SEO"
rows = list(csv.DictReader(open(OUT + "/01-ON-PAGE-SEO-MASTER.csv", encoding="utf-8-sig")))
s1 = list(csv.DictReader(open(ROOT + "/QA/01-MASTER-SEO-IMPLEMENTATION-MAP.csv", encoding="utf-8-sig")))
L = list(csv.DictReader(open(OUT + "/05-INTERNAL-LINK-IMPLEMENTATION.csv", encoding="utf-8-sig")))
K = list(csv.DictReader(open(OUT + "/10-COMMERCIAL-KEYWORD-ASSIGNMENTS.csv", encoding="utf-8-sig")))
res = []


def ck(name, ok, detail=""):
    res.append(ok)
    print(("PASS " if ok else "FAIL ") + name + ((" — " + str(detail)[:400]) if detail else ""))


real = lambda s: bool(s) and not s.startswith(("—", "(", "{"))
STAT = {"READY FOR IMPLEMENTATION POST-AWS", "PRE-AWS PREPARATION", "HOD INPUT REQUIRED", "ENGINEERING INPUT REQUIRED", "GSC BASELINE REQUIRED",
        "CONDITIONAL — PRODUCT/OFFER CONFIRMATION", "NO CHANGE REQUIRED", "NOT PLANNED — CONDITIONAL"}

# 1 structure / slugs
ck("147 rows, same Row IDs/order as Step 1", [r["Row ID"] for r in rows] == [r["Row ID"] for r in s1], len(rows))
bad = [r["Row ID"] for r, b in zip(rows, s1) if b["URL"].startswith("http") and r["URL"] != b["URL"]]
ck("URL column identical to Step 1 for every live/proposed URL (no slug changed by spelling cleanup)", not bad, bad[:5])
ck("every Status is in the final vocabulary", all(r["Status"] in STAT for r in rows), collections.Counter(r["Status"] for r in rows if r["Status"] not in STAT))
ck("no row awaits an ownership decision (no OWNER DECISION / OWNERSHIP CONFIRMATION in Ownership Status)", not [r["Row ID"] for r in rows if re.search(r"OWNER DECISION|CONFIRMATION REQUIRED|MISMATCH", r["Ownership Status"])])

# 2 decisions
log = open(OUT + "/10-DECISIONS-RESOLUTION-LOG.md", encoding="utf-8").read()
ck("all 19 decisions have an explicit disposition in 10", all(re.search(r"### OD-%02d — .*\n\n\*\*Disposition: [A-Z]" % i, log) for i in range(1, 20)))
ids = set(re.findall(r"OD-\d+", " ".join(r["Decision Resolution"] + r["Implementation Dependency"] + r["Notes"] + r["Section Recommendations"] for r in rows)))
ck("every OD id used in the CSV is defined in 10 (OD-01..OD-19)", all(("### %s —" % i) in log and 1 <= int(i[3:]) <= 19 for i in ids), sorted(ids))
ck("Decision Resolution carries dispositions (no bare 'Required')", not [r["Row ID"] for r in rows if "Required" in r["Decision Resolution"]])

# 3 uniqueness / claims / spelling
def dups(col, rs):
    c = collections.Counter(r[col].lower() for r in rs if real(r[col])); return [k for k, v in c.items() if v > 1]
ck("recommended rendered titles unique", not dups("Rendered Title Preview", rows), dups("Rendered Title Preview", rows))
ck("recommended metas unique", not dups("Recommended Meta", rows), dups("Recommended Meta", rows))
ck("recommended H1s unique", not dups("Recommended H1", rows), dups("Recommended H1", rows))
forb = re.compile(r"\b(free|insured|overnight|lifetime|warranty|guarantee[d]?|15-day|igi certified|cheapest|best price)\b", re.I)
hits = [(r["Row ID"], f) for r in rows if r["Row ID"] != "BC-001" for f in ("Recommended Title (pre-suffix value)", "Recommended Meta", "Recommended H1") if real(r[f]) and forb.search(r[f])]
ck("no shipping/returns/warranty/certification/'free' wording in recommended title/meta/H1 (BC-001 approved package excluded)", not hits, hits)
VERBS = r"(?:customis|optimis|finalis|prioritis|symbolis|personalis|organis|canonicalis|normalis|recognis|standardis|summaris|utilis|categoris)(?:e|es|ed|ing|ation|ations)\b"
UK = re.compile(r"(?<![\w/\-])(jewellery|jewellers?|enquir\w+|labelled|colour|colours|centre|catalogue|" + VERBS + r"|aluminium|favour\w*|behaviour|grey)", re.I)
def strip_quotes(t):
    return re.sub(r"'[^']{0,120}'|\"[^\"]{0,120}\"|“[^”]{0,120}”", " ", t)
bad = [(r["Row ID"], f, UK.search(r[f]).group(0)) for r in rows for f in ("Recommended Title (pre-suffix value)", "Recommended Meta", "Recommended H1") if UK.search(r[f] or "")]
ck("American English in recommended titles, metas and H1s", not bad, bad)
bad = [(l["Link ID"], f, UK.search(l[f]).group(0)) for l in L for f in ("Recommended Anchor", "Anchor Variants") if UK.search(l[f] or "")]
ck("American English in link anchors", not bad, bad[:5])
bad = [(r["Row ID"], f, UK.search(strip_quotes(r[f])).group(0)) for r in rows for f in ("Section Recommendations", "Recommended Schema", "Page Name", "Implementation Dependency", "Notes", "AEO Opportunity") if UK.search(strip_quotes(r[f] or ""))]
ck("American English in recommended copy outside quoted current text", not bad, bad[:6])
bad = [r["Row ID"] for r in rows for f in ("Recommended Title (pre-suffix value)", "Recommended Meta", "Recommended H1", "Anchor Context", "Internal Links Out") if re.search(r"\bjournal\b", r[f] or "", re.I)]
ck("public section name is 'Blog' (no 'Journal' in recommended text/anchors)", not bad and not [l["Link ID"] for l in L if re.search(r"journal", l["Recommended Anchor"] + l["Placement / Context"], re.I)], bad[:5])

# 4 keyword ownership
assigned = [x for x in K if x["Assignment State"].startswith("ASSIGNED") or x["Assignment State"].startswith("RESERVED")]
pc = collections.Counter(x["Primary Keyword"].lower() for x in assigned if x["Primary Keyword"] not in ("—", ""))
ck("each primary keyword is assigned to at most one URL", not [k for k, v in pc.items() if v > 1], [k for k, v in pc.items() if v > 1])
cal = {r["primary_keyword"].lower() for r in csv.DictReader(open(KW + "/FINAL-BLOG-CALENDAR/BLOG_CALENDAR_FINAL.csv", encoding="utf-8-sig")) if r["status"] != "UNUSED_SLOT"}
km = [r for r in csv.DictReader(open(KW + "/architecture/15_keyword_url_map.csv", encoding="utf-8-sig"))]
s15 = {r["keyword"].lower(): r["target_id"] for r in km if r["target_id"]}
coll = [(p, s15[p]) for p in pc if p in s15 and not s15[p].startswith("COM-")] + [(p, "calendar") for p in pc if p in cal]
ck("no assigned commercial primary collides with a Stage 15 Education owner or a calendar primary", not coll, coll)
STOP = {"for", "and", "the", "a", "of", "s", "et"}
def toks(t):
    return {w.rstrip("s") for w in re.split(r"[^a-z0-9]+", t.lower()) if w and w not in STOP}
by = {r["Row ID"]: r for r in rows}
miss = []
for x in assigned:
    if x["Assignment State"].startswith("ASSIGNED") and "PROXY" not in x["SERP Evidence"] and x["Row ID"] in by:
        r = by[x["Row ID"]]
        tt = toks(r["Recommended Title (pre-suffix value)"] + " " + r["Recommended H1"])
        need = toks(x["Primary Keyword"]) - {"et", "moi"} if "toi et moi" not in x["Primary Keyword"] else toks("toi moi engagement ring")
        if real(r["Recommended Title (pre-suffix value)"]) and not need <= tt:
            miss.append((x["Row ID"], sorted(need - tt)))
ck("every ASSIGNED commercial title/H1 contains its assigned head", not miss, miss)
ck("commercial rows with an assignment show it in the master (Primary Keyword starts ASSIGNED/RESERVED/NONE/HELD/NOT BUILT)",
   all(re.match(r"(ASSIGNED|RESERVED|NONE|HELD|NOT BUILT|FINAL|NO STAGE|side stones)", by[x["Row ID"]]["Primary Keyword"]) for x in K if x["Row ID"] in by))

# 5 cross-field consistency
oval = by["COM-PDP-OVAL-FLORAL"]
ck("oval PDP: H1 = final name, schema name = H1, link anchors = H1",
   oval["Recommended H1"] == "Oval Marquise Diamond Engagement Ring" and "name = H1" in oval["Recommended Schema"]
   and all(l["Recommended Anchor"] == "Oval Marquise Diamond Engagement Ring" for l in L if l["Destination ID"] == "COM-PDP-OVAL-FLORAL" and not l["Origin"].startswith("STEP 2A")))
ck("bespoke row preserves the confirmed timeline with its hedging", all(k in by["COM-BESPOKE"]["Section Recommendations"] for k in ["2–3 weeks", "6–9 days", "3–4 weeks", "design approval", "not a guaranteed delivery date", "typically"]))
ck("BC-001 row carries the approved package values unchanged", by["BC-001"]["Recommended Title (pre-suffix value)"] == "How Long Does a Custom Engagement Ring Take?")
ck("FAQPage never recommended (retire/remove/harmless-on-/faq only)", not [r["Row ID"] for r in rows if "FAQPage" in r["Recommended Schema"] and not re.search(r"retire|remove|harmless|no faqpage|without|not extend|do not", r["Recommended Schema"], re.I)])
ck("no GSC numbers in any cell", not [r["Row ID"] for r in rows if re.search(r"\d[\d,]*\s*(clicks|impressions)", " ".join(r.values()), re.I)])

# 6 status gating
bad = []
for r in rows:
    st, dep = r["Status"], r["Remaining Dependencies"]
    if st == "READY FOR IMPLEMENTATION POST-AWS" and re.search(r"(?<!non-)blocking", dep):
        bad.append((r["Row ID"], "READY but blocking dependency"))
    if st == "GSC BASELINE REQUIRED" and "GSC:" not in dep:
        bad.append((r["Row ID"], "GSC status without GSC dep"))
    if st == "HOD INPUT REQUIRED" and "HOD:" not in dep:
        bad.append((r["Row ID"], "HOD status without HOD dep"))
    if st == "CONDITIONAL — PRODUCT/OFFER CONFIRMATION" and "F-E" not in (dep + r["Implementation Dependency"]):
        bad.append((r["Row ID"], "conditional without F-E"))
ck("no row claims readiness while a blocking HOD/GSC/offer dependency remains; blocked rows name their dependency", not bad, bad)
ck("empty/test pages are individually dispositioned (18 rows with HOLD/REMOVE noindex handling)",
   len([r for r in rows if r["Row Group"] == "COMMERCIAL SUBCATEGORY" and r["Recommended Action"] in ("NOINDEX + EXCLUDE", "REMOVE")]) + (1 if by["COM-COLLECTION"]["Recommended Action"] == "NOINDEX + EXCLUDE" else 0) == 18)

# 7 links
crawl = json.load(open(ROOT + "/QA/_build/evidence/crawl/crawl.json"))
paths = {c["url"].replace("https://www.houseofdiams.com", "") or "/" for c in crawl}
planned = {r["URL"].replace("https://www.houseofdiams.com", "") for r in rows}
ck("%d link specs: every LIVE destination exists in the 2026-10-09 crawl" % len(L), not [l["Link ID"] for l in L if l["Destination Status"].startswith("LIVE (200)") and l["Destination URL"] not in paths])
ck("every proposed destination URL comes from the Step 1/Stage 15 map", not [l["Link ID"] for l in L if l["Destination Status"].startswith("PLANNED — URL proposed") and l["Destination URL"] not in planned])
docs = {f: open(f, encoding="utf-8").read() for f in glob.glob(OUT + "/*.md")}
ck("no leftover template tokens in any .md", not [os.path.basename(f) for f, t in docs.items() if re.search(r"%s|%d|OD-20|\(reserved\)", t)])
ck("required new deliverables exist", all(os.path.exists(OUT + "/" + n) for n in ("10-DECISIONS-RESOLUTION-LOG.md", "10-COMMERCIAL-KEYWORD-ASSIGNMENTS.csv", "11-HOD-CLIENT-FACTS-REQUEST.md", "12-ENGINEERING-INPUTS.md", "13-GSC-DATA-REQUEST.md", "README.md")))

# 9 correction-pass checks (2026-10-10): spelling defects, bangles contradiction, timeline/shipping consistency, README counts
PDPCSV = list(csv.DictReader(open(OUT + "/07-PDP-PRIORITY-ACTIONS.csv", encoding="utf-8-sig")))
MIS = re.compile(r"jewelery|symbolizm|organizm|optimizm|realizm|finalizt|\bjeler(?:y|s)\b", re.I)
LIVE_OK = re.compile(r"Certified Jewelery|'Jewelery' (typo|misspelling)")
mis_hits = []
for name, rs in (("01", rows), ("05", L), ("07", PDPCSV), ("10", K)):
    for r in rs:
        for f, v in r.items():
            if v and MIS.search(v) and not (name == "01" and r["Row ID"] == "BRAND-ABOUT" and LIVE_OK.search(v)):
                mis_hits.append((name, list(r.values())[0], f, MIS.search(v).group(0)))
for f, t in docs.items():
    b = os.path.basename(f)
    for i, line in enumerate(t.splitlines(), 1):
        if MIS.search(line):
            ok = bool(LIVE_OK.search(line)) or (b in ("10-DECISIONS-RESOLUTION-LOG.md", "README.md") and re.search(r"misspelling|Root cause", line))
            if not ok:
                mis_hits.append((b, i, MIS.search(line).group(0)))
ck("no 'jewelery'-type misspelling (or 'symbolizm'-type collateral) in any active recommendation, anchor, label or doc; only live About-tile text and the root-cause note are allow-listed", not mis_hits, mis_hits[:8])

UKH = re.compile(r"(?<![\w/])(?:[\w]+-)?(jewellery|jeweller\w*|enquir\w+|labelled|colour\w*|centre\w*|centred|catalogue\w*|" + VERBS + r"|aluminium|favour\w*|behaviour\w*)", re.I)
def uk_outside_quotes(t):
    t = strip_quotes(t)
    t = " ".join(w for w in t.split() if "/" not in w and w.count("-") < 2 and "houseofdiams" not in w)
    m = UKH.search(t)
    return m.group(0) if m else None
FLDS = ("Page Name", "Page Role", "Search Intent", "Related Terms", "Section Recommendations", "Primary Questions", "Anchor Context", "Cannibalization Risk",
        "Notes", "Implementation Dependency", "Recommended Schema", "AEO Opportunity", "GEO Opportunity", "Entity/Trust Opportunity", "Recommended Title (pre-suffix value)", "Recommended Meta", "Recommended H1")
LFLDS = ("Source URL", "Destination URL", "Recommended Anchor", "Anchor Variants", "Placement / Context", "Purpose", "Notes")
bad = [(r["Row ID"], f, uk_outside_quotes(r[f])) for r in rows for f in FLDS if r[f] and uk_outside_quotes(r[f])]
bad += [(l["Link ID"], f, uk_outside_quotes(l[f])) for l in L for f in LFLDS if l[f] and uk_outside_quotes(l[f])]
ck("no UK spelling (incl. hyphenated words such as ring-centred / near-colourless) in active recommendations or link labels outside quoted current text", not bad, bad[:8])

STALE = re.compile(r"spelling pending|pending OD-05|OD-05[^.\n|]{0,40}\b(pending|open|undecided)\b|awaits? OD-05", re.I)
stale = [(n, list(r.values())[0], f) for n, rs in (("01", rows), ("05", L), ("07", PDPCSV), ("10", K)) for r in rs for f, v in r.items() if v and STALE.search(v)]
stale += [(os.path.basename(f), i) for f, t in docs.items() for i, line in enumerate(t.splitlines(), 1) if STALE.search(line)]
ck("no stale 'spelling pending OD-05' note anywhere; OD-05 is ADOPTED in the log", not stale and bool(re.search(r"### OD-05 — .*\n\n\*\*Disposition: ADOPTED", log)), stale[:6])
ck("no unresolved quote markers (U+27E6/U+27E7) leaked into outputs", not [f for f, t in docs.items() if "⟦" in t or "⟧" in t] and not any("⟦" in v or "⟧" in v for r in rows + L + K + PDPCSV for v in r.values() if v))

# bangles: recommended copy vs documented inventory (evidence = 2026-10-09 crawl product records)
HOST = "https://www.houseofdiams.com"
page = {c["url"].replace(HOST, "") or "/": c for c in crawl}
def shop_links(path):
    return {l for l in page[path]["internal_links"] if l.startswith("/shop/")}
BG, CL, TN = "/fine-jewellery/bracelet/bangles", "/fine-jewellery/bracelet/chain-link", "/fine-jewellery/bracelet/tennis"
inv = shop_links(BG)
def prod_text(u):
    c = page.get(u, {})
    return " ".join([c.get("title") or "", c.get("meta_description") or "", " ".join(c.get("h1s") or [])])
inv_has_bangle = any(re.search(r"bangle", prod_text(u), re.I) for u in inv)
bg = by["SUB:" + BG]
claim_cells = {f: bg[f] for f in ("Recommended Title (pre-suffix value)", "Recommended Meta", "Recommended H1")}
ck("bangles row: recommended title/meta/H1 make no 'bangle' claim unless the category's own product records describe bangles (%d products listed, %d describe a bangle)" % (len(inv), sum(bool(re.search('bangle', prod_text(u), re.I)) for u in inv)),
   inv_has_bangle or not any(re.search(r"bangle", v, re.I) for v in claim_cells.values()), claim_cells)
ck("bangles row: label/contents mismatch is HELD, status CONDITIONAL with F-E7, no keyword assigned, F-E7 asked in 11",
   bg["Status"] == "CONDITIONAL — PRODUCT/OFFER CONFIRMATION" and "F-E7" in bg["Remaining Dependencies"] and bg["Ownership Status"].startswith("HELD")
   and bg["Primary Keyword"].startswith("HELD") and any(x["Row ID"] == "SUB:" + BG and x["Assignment State"].startswith("HELD") and x["Primary Keyword"] == "—" for x in K)
   and "F-E7" in open(OUT + "/11-HOD-CLIENT-FACTS-REQUEST.md", encoding="utf-8").read())
cl_inv, tn_inv = shop_links(CL), shop_links(TN)
ck("bangles / chain-link / tennis product sets are disjoint (overlap documented as none)", not (inv & cl_inv) and not (inv & tn_inv) and not (cl_inv & tn_inv), (sorted(inv & cl_inv), sorted(inv & tn_inv)))
ck("no recommended title/meta/H1 or link anchor anywhere promises 'bangle(s)' without inventory support", inv_has_bangle or not (
   [r["Row ID"] for r in rows for f in ("Recommended Title (pre-suffix value)", "Recommended Meta", "Recommended H1") if re.search(r"bangle", r[f] or "", re.I)]
   + [l["Link ID"] for l in L if re.search(r"bangle", l["Recommended Anchor"] + l["Anchor Variants"], re.I)]))

# bespoke timeline vs shipping facts
d11 = open(OUT + "/11-HOD-CLIENT-FACTS-REQUEST.md", encoding="utf-8").read()
ck("11: the confirmed bespoke timeline is not re-asked (no 'please confirm ... starting point'); source and 'nothing to answer' stated",
   not re.search(r"please confirm that|correct starting point", d11, re.I) and "Nothing to answer here" in d11 and "SR-01" in d11 and "SR-02" in d11)
ck("log records SR-01 (start point confirmed by the project owner) and SR-02 ('insured' shipping unconfirmed, tracked under F-A1)",
   "| SR-01 |" in log and "| SR-02 |" in log and re.search(r"SR-02.*F-A1", log, re.S) is not None)
f_a1 = [l for l in d11.splitlines() if l.startswith("| F-A1 |")]
ck("F-A1 (shipping policy) covers insurance and names the BC-001 wording; shipping rows depend on F-A1", bool(f_a1) and "insurance" in f_a1[0].lower() and "BC-001" in f_a1[0]
   and "F-A1" in by["SUP-POLICIES-SHIP"]["Remaining Dependencies"] and "F-A1" in by["BC-001"]["Remaining Dependencies"] and "SR-02" in by["BC-001"]["Notes"] and "SR-01" in by["BC-001"]["Notes"])
tl = []
for r in rows:
    for f, v in r.items():
        if v and re.search(r"2[–-]3 weeks", v) and not re.search(r"6[–-]9", v) and r["Row ID"] != "BC-001":
            tl.append((r["Row ID"], f))
ck("every recommended mention of '2–3 weeks' carries the matching '6–9 days' delivery part (no partial timeline)", not tl, tl[:5])
live = [(r["Row ID"], f) for r in rows for f, v in r.items() if v and re.search(r"4[–-]6[ -]week", v)
        and not re.search(r"Live|live|current|Current|contradict|not the confirmed|REMOVE|remove|stale|’|'4", v)]
ck("'4–6 week' appears only as a described live-site defect", not live, live[:5])
ins = []
for r in rows:
    if r["Row ID"] == "BC-001":
        continue
    for f in ("Recommended Title (pre-suffix value)", "Recommended Meta", "Recommended H1", "Section Recommendations", "Recommended Schema", "GEO Opportunity", "Entity/Trust Opportunity"):
        v = r[f] or ""
        if re.search(r"\binsured\b", strip_quotes(v), re.I) and not re.search(r"remove|unconfirmed|until|F-A1|not |neutral|question", v, re.I):
            ins.append((r["Row ID"], f))
ck("'insured' appears in recommendations only as a removed/unconfirmed claim or a question (never as an asserted fact)", not ins, ins[:5])

# README counts equal master CSV counts
rd = open(OUT + "/README.md", encoding="utf-8").read()
cs = collections.Counter(r["Status"] for r in rows)
def rn(pat):
    m = re.search(pat, rd)
    return [int(x) for x in m.groups()] if m else None
exp_blocked = cs["HOD INPUT REQUIRED"] + cs["ENGINEERING INPUT REQUIRED"] + cs["GSC BASELINE REQUIRED"] + cs["CONDITIONAL — PRODUCT/OFFER CONFIRMATION"]
ck("README status counts equal the master CSV counts",
   rn(r"after the AWS migration:\*\* (\d+) of (\d+) rows") == [cs["READY FOR IMPLEMENTATION POST-AWS"], len(rows)]
   and rn(r"\*\*Final specification, content still to be written \(Class A\):\*\* (\d+) rows") == [cs["PRE-AWS PREPARATION"]]
   and rn(r"external input:\*\* (\d+) rows — HOD facts (\d+) .*?GSC baseline (\d+) .*?product/offer confirmation (\d+) ") == [exp_blocked, cs["HOD INPUT REQUIRED"], cs["GSC BASELINE REQUIRED"], cs["CONDITIONAL — PRODUCT/OFFER CONFIRMATION"]]
   and rn(r"\*\*No change / not planned:\*\* (\d+) rows") == [cs["NO CHANGE REQUIRED"] + cs["NOT PLANNED — CONDITIONAL"]]
   and rn(r"Operational file\*\* — (\d+) rows") == [len(rows)], dict(cs))
d02 = open(OUT + "/02-ON-PAGE-SEO-MASTER.md", encoding="utf-8").read()
ck("02 status table equals the master CSV counts", all(re.search(r"\| %s \| %d \|" % (re.escape(k), v), d02) for k, v in cs.items()), dict(cs))
ck("README records the calendar owner annotation as DONE (BLOG-WR-TYPES / target_owner / EDU-WB-TYPES) and the BC-001 publication hold",
   all(k in rd for k in ("BLOG_CALENDAR_FINAL.csv", "BLOG-WR-TYPES", "target_owner", "EDU-WB-TYPES", "BC-001 publication held", "HOLD PUBLICATION (pending F-A1)")) and "Outstanding actions outside this package" not in rd)
ck("147 master rows and 19 dispositions preserved; link specs = 624 (no real correction changed the link set)", len(rows) == 147 and len(L) == 624)

# 10 close-out checks (2026-10-10)
bc = by["BC-001"]
pkg_meta = json.load(open(os.path.dirname(os.path.abspath(__file__)) + "/pkg_meta.json"))
f_a1_open = "| F-A1 |" in d11 and not re.search(r"F-A1[^|\n]{0,40}\b(CONFIRMED|ANSWERED)\b", d11)
unconfirmed_in_pkg = [k for k, v in pkg_meta.items() if re.search(r"\binsured\b", json.dumps(v), re.I)]
ck("BC-001 cannot be publish-ready while F-A1 is unconfirmed: status HOD INPUT REQUIRED, action HOLD PUBLICATION, F-A1 named as blocking",
   (not f_a1_open or "bc-001" not in unconfirmed_in_pkg) or (bc["Status"] == "HOD INPUT REQUIRED" and bc["Recommended Action"].startswith("HOLD PUBLICATION")
   and "F-A1" in bc["Remaining Dependencies"] and "BLOCKS PUBLICATION" in bc["Remaining Dependencies"] and bc["HOD Facts Needed"] == "Y"),
   (bc["Status"], bc["Recommended Action"]))
ck("no packaged post whose approved meta carries an unconfirmed 'insured' claim is READY / PUBLISH (generic rule)",
   not [r["Row ID"] for r in rows if r["Row ID"].startswith("BC-") and r["Row ID"].lower() in unconfirmed_in_pkg and (r["Status"] == "READY FOR IMPLEMENTATION POST-AWS" or r["Recommended Action"].startswith("PUBLISH"))])
ck("BC-001 row still carries the approved package title unchanged and states the package was not edited (hold is a publication status only)",
   bc["Recommended Title (pre-suffix value)"] == "How Long Does a Custom Engagement Ring Take?" and "not edited" in bc["Notes"].lower() or "NOT edited" in bc["Notes"])
ck("status totals reconcile to 147 and equal the sum of the vocabulary", sum(cs[k] for k in STAT) == 147 == len(rows), dict(cs))
ck("BC-001 hold is reflected in 08 (priorities), 10 (log) and 11 (questionnaire)",
   "BC-001" in open(OUT + "/08-ON-PAGE-IMPLEMENTATION-PRIORITIES.md", encoding="utf-8").read() and "HOLD PUBLICATION" in open(OUT + "/08-ON-PAGE-IMPLEMENTATION-PRIORITIES.md", encoding="utf-8").read()
   and "publication is HELD" in log and "publication is held" in d11)

# 11 unsupported people/capability claims in recommended title/meta/H1 (2026-10-10 final consistency check)
PEOPLE = re.compile(r"\bfounders?\b|\bdesign team\b|\bour (designers|experts|craftsm[ae]n|artisans|specialists|gemologists)\b|\bwill guide you\b|\bmeet the\b", re.I)
f_c1_open = "| F-C1 |" in d11
bad = [(r["Row ID"], f) for r in rows if r["Row ID"] != "BC-001" for f in ("Recommended Title (pre-suffix value)", "Recommended Meta", "Recommended H1") if PEOPLE.search(r[f] or "")]
ck("no founder / design-team / expert-capability claim in any recommended title, meta or H1 while F-C1 is unconfirmed (BC-001 approved package excluded)", not (f_c1_open and bad), bad)
fc1 = [l for l in d11.splitlines() if l.startswith("| F-C1 |")]
ck("BRAND-ABOUT: neutral title/meta, status HOD INPUT REQUIRED with F-C1 kept, founder questions still in the questionnaire",
   by["BRAND-ABOUT"]["Recommended Title (pre-suffix value)"] == "Our Story & Values"
   and by["BRAND-ABOUT"]["Recommended Meta"] == "Learn about House of Diams, its story, values, and approach to diamond jewelry."
   and by["BRAND-ABOUT"]["Status"] == "HOD INPUT REQUIRED" and "F-C1" in by["BRAND-ABOUT"]["Remaining Dependencies"]
   and bool(fc1) and "founders" in fc1[0].lower())
ck("COM-BESPOKE: neutral meta (no unsupported 'design team will guide you'), status and confirmed timeline unchanged",
   by["COM-BESPOKE"]["Recommended Meta"] == "Design a custom engagement ring or bespoke diamond jewelry with House of Diams. Share your idea, stone and metal preferences to start a conversation."
   and by["COM-BESPOKE"]["Status"] == "READY FOR IMPLEMENTATION POST-AWS" and int(by["COM-BESPOKE"]["Meta Length"]) <= 160)

# 12 order-tracking promises (2026-10-10): not a confirmed feature/fact -> never promised in recommended metadata, titles, H1s or target questions
TRACK = re.compile(r"\btrack(?:ing|s)?\b[^.|]{0,30}\b(?:order|orders|shipment|shipments|package|parcel|delivery|purchase)\b|\b(?:order|shipment|package|parcel|delivery) tracking\b|\btracking (?:link|number|info)", re.I)
trk = [(r["Row ID"], f) for r in rows if r["Row ID"] != "BC-001" for f in ("Recommended Title (pre-suffix value)", "Recommended Meta", "Recommended H1", "Primary Questions") if TRACK.search(r[f] or "")]
ck("no order-tracking promise in any recommended title, meta, H1 or target question (not confirmed; F-A1 gates it; BC-001 approved package excluded)", not trk, trk)
fa1 = [l for l in d11.splitlines() if l.startswith("| F-A1 |")]
ck("F-A1 asks HOD about order tracking and records the live evidence (Returns 'Track My Order' button, /shipping tracking-link sentence)",
   bool(fa1) and "tracking" in fa1[0].lower() and "Track My Order" in fa1[0])
ck("SUP-POLICIES-RET / SUP-POLICIES-SHIP metas are neutral and the rows keep status HOD INPUT REQUIRED with F-A2 / F-A1",
   by["SUP-POLICIES-RET"]["Recommended Meta"] == "How returns and exchanges work at House of Diams, and how to contact us with questions about your order."
   and by["SUP-POLICIES-SHIP"]["Recommended Meta"] == "Shipping and delivery information from House of Diams: order processing and made-to-order lead times."
   and by["SUP-POLICIES-RET"]["Status"] == "HOD INPUT REQUIRED" and by["SUP-POLICIES-SHIP"]["Status"] == "HOD INPUT REQUIRED")

# 8 protection (read-only)
ref = datetime.datetime(2026, 10, 9, 19, 55).timestamp()
CAL = KW + "/FINAL-BLOG-CALENDAR/BLOG_CALENDAR_FINAL.csv"
prot = [ROOT + "/QA", KW + "/FINAL-BLOG-CALENDAR", KW + "/architecture", KW + "/dataforseo", KW + "/serp", KW + "/clusters", KW + "/competitors", KW + "/content-strategy", KW + "/blogs", KW + "/reference", KW + "/site"]
newer = []
for d in prot:
    for dp, dn, fn in os.walk(d):
        for f in fn:
            p = os.path.join(dp, f)
            if p == CAL:
                continue
            if os.path.getmtime(p) > ref:
                newer.append(p)
ck("protected research/Step 1/blog files unchanged (no mtime after Step 2 started; the one authorised calendar edit is verified separately below)", not newer, newer[:5])
envp = ROOT + "/.env"
ck(".env untouched (modification time only; contents never read)", (not os.path.exists(envp)) or os.path.getmtime(envp) < ref)
ck("approved BC-001 package files byte-for-byte as committed (git: no change under blogs/)",
   subprocess.run(["git", "-C", ROOT, "status", "--short", "--", "Keywords/content SEO/blogs"], capture_output=True, text=True).stdout.strip() == "")
# calendar diff vs git HEAD: only target_owner of BLOG-WR-TYPES may differ
import io
head_txt = subprocess.run(["git", "-C", ROOT, "show", "HEAD:Keywords/content SEO/FINAL-BLOG-CALENDAR/BLOG_CALENDAR_FINAL.csv"], capture_output=True).stdout.decode("utf-8")
cur_txt = open(CAL, encoding="utf-8", newline="").read()
ha, hb = list(csv.reader(io.StringIO(head_txt, newline=""))), list(csv.reader(io.StringIO(cur_txt, newline="")))
cdiff = []
if len(ha) == len(hb) and ha[0] == hb[0] and [r[0] for r in ha] == [r[0] for r in hb]:
    cdiff = [(ha[i][0], ha[0][j], ha[i][j], hb[i][j]) for i in range(len(ha)) for j in range(len(ha[0])) if ha[i][j] != hb[i][j]]
ck("calendar diff vs git HEAD = exactly one cell: BLOG-WR-TYPES.target_owner -> EDU-WB-TYPES (same rows, same order, same header)",
   len(ha) == len(hb) == 113 and cdiff == [("BLOG-WR-TYPES", "target_owner", "Blog (Style & Trends)", "EDU-WB-TYPES")], cdiff[:3])
g = subprocess.run(["git", "-C", ROOT, "status", "--short"], capture_output=True, text=True).stdout
tracked_changes = [l for l in g.splitlines() if l[:2].strip() in ("M", "D", "A", "R") and "On-page SEO" not in l]
ok_tracked = sorted(t.strip() for t in tracked_changes) == sorted(['D "Keywords/content SEO/CLAUDE.md"', 'M "Keywords/content SEO/FINAL-BLOG-CALENDAR/BLOG_CALENDAR_FINAL.csv"'])
ck("tracked-file changes are only the pre-existing nested CLAUDE.md deletion and the authorised calendar owner edit", ok_tracked, tracked_changes)
head = subprocess.run(["git", "-C", ROOT, "log", "-1", "--format=%h"], capture_output=True, text=True).stdout.strip()
ck("no commit created (HEAD still 94e5876)", head == "94e5876", head)

print("RESULT:", "ALL PASS" if all(res) else "FAILURES", "(%d checks)" % len(res))
sys.exit(0 if all(res) else 1)
