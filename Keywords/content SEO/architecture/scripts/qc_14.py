#!/usr/bin/env python3
"""Stage 14 QC — Education architecture.

Run: python3 architecture/scripts/qc_14.py
Exit code 0 only if every check passes.
"""
import csv, glob, hashlib, json, os, re, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
P = lambda *a: os.path.join(ROOT, *a)
rd = lambda f: list(csv.DictReader(open(P(f))))

ARCH = "architecture/14_education_architecture.csv"
HIER = "architecture/14_education_hierarchy.csv"
CONS = "architecture/14_education_cluster_consolidation.csv"
PTF = "architecture/14_education_page_type_framework.csv"
MAP = "content-strategy/14_education_existing_content_mapping.csv"
MDS = ["architecture/14_education_decision_log.md", "architecture/14_education_summary.md"]
OUT_CSV = [ARCH, HIER, CONS, PTF, MAP]

results = []
def check(name, ok, detail=""):
    results.append((name, ok, detail))

reg = {r["cluster_id"] for r in rd("clusters/11_cluster_registry.csv")}
arch, hier, cons, ptf, mp = rd(ARCH), rd(HIER), rd(CONS), rd(PTF), rd(MAP)
s13 = rd("content-strategy/13_existing_content_decisions.csv")
topics = {t["topic_id"]: t for t in arch}

# 1. All output files exist
for f in OUT_CSV + MDS:
    check(f"output exists: {f}", os.path.isfile(P(f)))

# 2. Every referenced cluster exists
refs = set()
for f in OUT_CSV + MDS:
    refs |= set(re.findall(r"CL-\d{3}", open(P(f)).read()))
bad = sorted(refs - reg)
check("every referenced Stage 11 cluster exists", not bad, f"invalid: {bad}" if bad else f"{len(refs)} distinct cluster IDs referenced")

# 3. Every Stage 11 cluster has exactly one PRIMARY row
prim = {}
for r in cons:
    if r["assignment_role"] == "PRIMARY":
        prim.setdefault(r["cluster_id"], []).append(r["education_topic_id"])
multi = {k: v for k, v in prim.items() if len(v) > 1}
missing = sorted(reg - set(prim))
check("no cluster assigned to multiple PRIMARY topics", not multi, str(multi))
check("all 89 Stage 11 clusters have a PRIMARY decision", not missing and len(prim) == len(reg), f"missing: {missing}; primaries={len(prim)} registry={len(reg)}")
check("assignment_role controlled (PRIMARY/SECONDARY)", all(r["assignment_role"] in ("PRIMARY", "SECONDARY") for r in cons))
sec_orphan = [r["cluster_id"] for r in cons if r["assignment_role"] == "SECONDARY" and r["cluster_id"] not in prim]
check("every SECONDARY row has a PRIMARY row for the same cluster", not sec_orphan, str(sec_orphan))
pairs = [(r["cluster_id"], r["education_topic_id"]) for r in cons]
check("no duplicate cluster-topic pairs", len(pairs) == len(set(pairs)))
sec_same = [r["cluster_id"] for r in cons if r["assignment_role"] == "SECONDARY" and r["education_topic_id"] in prim.get(r["cluster_id"], [])]
check("SECONDARY never points to the cluster's own PRIMARY topic", not sec_same, str(sec_same))

# 4. Controlled values
EV = {"HIGH", "MEDIUM", "LOW", "INSUFFICIENT_EVIDENCE"}
RISK = {"LOW", "MEDIUM", "HIGH", "INSUFFICIENT_EVIDENCE"}
DEC = {"DEDICATED_RESOURCE", "CONSOLIDATE_INTO_TOPIC", "CONDITIONAL_RESOURCE", "DEFER", "EXCLUDE_NOT_EDUCATION", "EXCLUDE_OFF_SCOPE"}
HUBDEC = {"KEEP", "MERGE", "SPLIT", "CONDITIONAL", "DEFER"}
STAT = {"PROPOSED", "PROPOSED_PROVISIONAL", "CONDITIONAL", "DEFERRED"}
SEP = {"YES", "NO", "CONDITIONAL", "DEFERRED"}
SERPV = {"YES", "NO", "PARTIAL"}
EXACT = {"UPDATE_IN_PLACE", "MOVE_TO_EDUCATION", "RETARGET", "DEFER", "NONE"}
INTENT = {"INFORMATIONAL", "COMMERCIAL_RESEARCH", "MIXED", "TRANSACTIONAL", "NAVIGATIONAL"}
def ctl(name, rows, col, allowed):
    badv = sorted({r[col] for r in rows if r[col] not in allowed})
    check(f"controlled values: {name}.{col}", not badv, f"bad: {badv}")
ctl("consolidation", cons, "evidence_level", EV)
ctl("consolidation", cons, "cannibalization_risk", RISK)
ctl("consolidation", cons, "decision", DEC)
ctl("architecture", arch, "evidence_level", EV)
ctl("architecture", arch, "cannibalization_risk", RISK)
ctl("architecture", arch, "architecture_status", STAT)
ctl("architecture", arch, "separate_page_required", SEP)
ctl("architecture", arch, "SERP_validation_available", SERPV)
ctl("architecture", arch, "existing_content_action", EXACT)
ctl("architecture", arch, "primary_intent", INTENT)
hubs = [h for h in hier if h["node_type"] == "HUB"]
ctl("hierarchy(hubs)", hubs, "hub_decision", HUBDEC)
ctl("hierarchy", hier, "evidence_level", EV)
ptypes = {r["page_type"] for r in ptf}
badpt = sorted({t["proposed_page_type"] for t in arch} - ptypes)
check("every topic page type is defined in the page-type framework", not badpt, str(badpt))
badpt2 = sorted({h["page_type"] for h in hier} - ptypes - {"n/a"})
check("every hierarchy page type is defined in the framework", not badpt2, str(badpt2))

# 5. Uniqueness and orphans
tids = [t["topic_id"] for t in arch]
check("no duplicate Education topic IDs", len(tids) == len(set(tids)))
hids = [h["hierarchy_id"] for h in hier]
check("no duplicate hierarchy IDs", len(hids) == len(set(hids)))
hidset = set(hids)
badpar = [h["hierarchy_id"] for h in hier if h["parent_id"] and h["parent_id"] not in hidset]
check("every hierarchy parent exists", not badpar, str(badpar))
roots = [h for h in hier if not h["parent_id"]]
check("exactly one hierarchy root", len(roots) == 1)
topic_nodes = [h["topic_or_pillar_id"] for h in hier if h["node_type"] == "TOPIC"]
orph = sorted(set(tids) - set(topic_nodes))
dup_nodes = sorted({x for x in topic_nodes if topic_nodes.count(x) > 1})
check("no orphan topic records (every topic has exactly one hierarchy node)", not orph and not dup_nodes, f"orphans {orph}; dup {dup_nodes}")
unk = sorted(set(topic_nodes) - set(tids))
check("no hierarchy node points to an unknown topic", not unk, str(unk))
merged_hubs = {h["hierarchy_id"] for h in hubs if h["hub_decision"] == "MERGE"}
under_merged = [h["hierarchy_id"] for h in hier if h["parent_id"] in merged_hubs]
check("no topic sits under a MERGE (not-proposed) hub", not under_merged, str(under_merged))
badct = sorted(set(r["education_topic_id"] for r in cons) - set(tids) - {"NONE"})
check("every consolidation topic ID exists in the inventory", not badct, str(badct))
excl_bad = [r["cluster_id"] for r in cons if r["decision"].startswith("EXCLUDE") and r["education_topic_id"] != "NONE"]
check("EXCLUDE decisions carry no Education topic", not excl_bad, str(excl_bad))
none_bad = [r["cluster_id"] for r in cons if r["education_topic_id"] == "NONE" and not r["decision"].startswith("EXCLUDE")]
check("topic NONE only used with EXCLUDE decisions", not none_bad, str(none_bad))

# 6. Internal consistency topic <-> consolidation
cnt_bad = []
for t in arch:
    n = sum(1 for r in cons if r["education_topic_id"] == t["topic_id"] and r["assignment_role"] == "PRIMARY")
    if str(n) != t["cluster_count"]:
        cnt_bad.append((t["topic_id"], t["cluster_count"], n))
check("topic cluster_count equals its PRIMARY consolidation rows", not cnt_bad, str(cnt_bad))
stat_bad = []
for r in cons:
    if r["assignment_role"] != "PRIMARY" or r["education_topic_id"] == "NONE":
        continue
    s = topics[r["education_topic_id"]]["architecture_status"]
    d = r["decision"]
    if (d == "CONDITIONAL_RESOURCE" and s != "CONDITIONAL") or (d == "DEFER" and s != "DEFERRED") or \
       (d in ("DEDICATED_RESOURCE", "CONSOLIDATE_INTO_TOPIC") and s not in ("PROPOSED", "PROPOSED_PROVISIONAL", "CONDITIONAL")):
        stat_bad.append((r["cluster_id"], d, s))
check("PRIMARY decisions consistent with topic status", not stat_bad, str(stat_bad))

# 7. Stage 13 existing content accounted for
murls = {r["existing_url"]: r for r in mp}
s13urls = [r["url"] for r in s13]
dropped = [u for u in s13urls if u not in murls]
check("no Stage 13 content row silently dropped", not dropped and len(mp) == len(s13), f"dropped {dropped}")
cand = [r for r in s13 if r["action"] in ("MOVE_TO_EDUCATION", "UPDATE_IN_PLACE", "RETARGET", "DEFER")]
unmapped = [r["url"] for r in cand if murls.get(r["url"], {}).get("education_topic_id") not in topics]
check(f"all {len(cand)} Stage 13 Education candidates map to a valid Education topic", not unmapped, str(unmapped))
pres = [r["url"] for r in s13 if murls[r["url"]]["stage13_action"] != r["action"] or murls[r["url"]]["stage13_migration_risk"] != r["migration_risk"]]
check("Stage 13 action and migration-risk values preserved exactly", not pres, str(pres))
hi = [r["url"] for r in s13 if r["migration_risk"] == "HIGH" and murls[r["url"]]["stage14_migration_status"] != "STAY_AT_CURRENT_URL_EDUCATION_OWNED"]
check("HIGH-risk URLs (CVD vs HPHT, lab-vs-natural) not recommended to move", not hi, str(hi))
dfr = [r["url"] for r in s13 if r["action"] == "DEFER" and murls[r["url"]]["stage14_migration_status"] != "DEFERRED"]
check("Stage 13 DEFER rows remain DEFERRED", not dfr, str(dfr))
# topic existing_content_action agrees with Stage 13 for mapped topics
agree = []
for r in s13:
    m = murls[r["url"]]
    if m["education_topic_id"] in topics and topics[m["education_topic_id"]]["existing_content_action"] != r["action"]:
        agree.append((m["education_topic_id"], r["action"]))
check("topic existing_content_action agrees with Stage 13", not agree, str(agree))

# 8. No final URLs introduced
inv = set()
for f in ["content-strategy/10_existing_content_inventory.csv", "content-strategy/13_existing_content_decisions.csv"]:
    for r in rd(f):
        for v in r.values():
            for u in re.findall(r"https?://[^\s,;|)]+", v or ""):
                inv.add(u.rstrip("/."))
inv_paths = {re.sub(r"https?://(www\.)?houseofdiams\.com", "", u) or "/" for u in inv}
new_urls, new_paths = [], []
HOD_PATH = re.compile(r"(?<![\w.-])/(blog|education|shop|engagement-rings|wedding-bands|fine-jewellery|faq|collection|bespoke|lab-grown[\w-]*|natural[\w-]*)(/[\w./-]*)?")
for f in OUT_CSV + MDS:
    txt = open(P(f)).read()
    for u in re.findall(r"https?://[^\s,;|)\"'`]+", txt):
        if u.rstrip("/.") not in inv:
            new_urls.append((f, u))
    for m in HOD_PATH.finditer(txt):
        p = m.group(0).rstrip("/.,")
        if p not in inv_paths:
            new_paths.append((f, p))
check("no new URLs introduced (only existing inventory URLs appear)", not new_urls, str(new_urls[:5]))
check("no new HOD site paths introduced", not new_paths, str(new_paths[:8]))
slash = [h["hierarchy_id"] for h in hier if "/" in h["conceptual_path_not_a_url"]]
check("hierarchy conceptual paths contain no slug/URL separators", not slash, str(slash))

# 9. No redirects / canonical tags prescribed
TERMS = re.compile(r"\b(301|302|redirect\w*|canonical\w*|rel=)", re.I)
csv_hits = []
for f in OUT_CSV:
    for i, row in enumerate(csv.reader(open(P(f)))):
        for cell in row:
            if TERMS.search(cell):
                csv_hits.append((f, i, cell[:80]))
check("no redirect/canonical prescriptions in CSV outputs", not csv_hits, str(csv_hits[:5]))
NEG = re.compile(r"\b(no|not|never|nor|without|neither)\b|DO_NOT|Stage 13|not a canonical tag|out of scope", re.I)
md_hits = []
for f in MDS:
    for n, line in enumerate(open(P(f)), 1):
        if TERMS.search(line) and not NEG.search(line):
            md_hits.append((f, n, line.strip()[:100]))
check("no redirect/canonical prescriptions in markdown (every mention negated or attributed to Stage 13)", not md_hits, str(md_hits[:5]))

# 10. No live-site / upstream files modified; no new raw API files
man = json.load(open(P("architecture/scripts/14_upstream_checksums.json")))
changed = [f for f, h in man.items() if not os.path.isfile(P(f)) or hashlib.sha256(open(P(f), "rb").read()).hexdigest() != h]
check(f"upstream files unchanged since the Stage 14 build ({len(man)} files incl. site/ and dataforseo/raw/)", not changed, str(changed))
check("no new DataForSEO raw files (still 3)", len(glob.glob(P("dataforseo/raw/*"))) == 3)
check("no new SERP raw files (still 100)", len(glob.glob(P("serp/raw/08_stage8_by_id/*.json"))) == 100)
stage14_raw = [f for f in glob.glob(P("**/*14*raw*"), recursive=True)]
check("no Stage 14 raw API output files", not stage14_raw, str(stage14_raw))
site_like = [f for f in glob.glob(P("**/*"), recursive=True)
             if os.path.basename(f) in ("robots.txt", "sitemap.xml") or f.endswith((".liquid", ".tsx", ".jsx"))]
check("no website code/robots/sitemap files created in the project", not site_like, str(site_like))
for prev in ["architecture/scripts/qc_12.py", "content-strategy/scripts/qc_13.py"]:
    r = subprocess.run([sys.executable, P(prev)], cwd=ROOT, capture_output=True, text=True)
    check(f"earlier-stage QC still passes: {prev}", r.returncode == 0, (r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout + r.stderr).strip() else "")

# 11. No credentials leaked
cred = [f for f in OUT_CSV + MDS + ["architecture/scripts/build_14_csvs.py"]
        if re.search(r"(password|api[_-]?key|DATAFORSEO_LOGIN|DATAFORSEO_PASSWORD|Bearer\s+\w)", open(P(f)).read(), re.I)]
check("no credentials in Stage 14 files", not cred, str(cred))

# report
fails = [r for r in results if not r[1]]
for name, ok, detail in results:
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail and (not ok or 'referenced' in name) else ""))
print(f"\n{len(results) - len(fails)}/{len(results)} checks passed")
sys.exit(1 if fails else 0)
