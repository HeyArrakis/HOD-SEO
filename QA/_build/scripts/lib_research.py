"""Loaders for the existing HOD SEO research (read-only). Nothing here modifies source files."""
import csv, re, json, collections, os
csv.field_size_limit(10**9)
R = "/Users/manavdesai/Desktop/HOD SEO/Keywords/content SEO/"
SCR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "evidence") + "/"


def rd(path):
    return list(csv.DictReader(open(R + path, encoding="utf-8-sig")))


registry = {x["target_id"]: x for x in rd("architecture/15_target_page_registry.csv")}
topic = {x["target_page_id"]: x for x in rd("content-strategy/17_topic_intelligence.csv")}
brief = {x["target_page_id"]: x for x in rd("content-strategy/19_brief_registry.csv")}
links_req = {x["page_id"]: x for x in rd("architecture/16_page_link_requirements.csv")}
cal_all = rd("FINAL-BLOG-CALENDAR/BLOG_CALENDAR_FINAL.csv")
cal = [x for x in cal_all if x["status"] != "UNUSED_SLOT"]
cal_by_id = {x["content_id"]: x for x in cal}
kmap_rows = rd("architecture/15_keyword_url_map.csv")
kmap = {}
for x in kmap_rows:
    kmap[x["normalized_keyword"].strip().lower()] = x
    kmap[x["keyword"].strip().lower()] = x
qcov = collections.defaultdict(list)
for x in rd("content-strategy/18_question_coverage.csv"):
    qcov[x["target_page_id"]].append(x)
ecov = collections.defaultdict(list)
for x in rd("content-strategy/18_entity_coverage.csv"):
    ecov[x["target_page_id"]].append(x)
sem = collections.defaultdict(list)
for x in rd("content-strategy/17_semantic_concepts.csv"):
    sem[x["target_page_id"]].append(x)
anchors = collections.defaultdict(list)
for x in rd("architecture/16_anchor_strategy.csv"):
    anchors[x["target_page_id"]].append(x)
link_map = rd("architecture/16_internal_link_map.csv")
bizfacts = collections.defaultdict(list)
for x in rd("content-strategy/19_business_fact_requirements.csv"):
    bizfacts[x["target_page_id"]].append(x)
gaps = collections.defaultdict(list)
for x in rd("content-strategy/18_semantic_gap_register.csv"):
    gaps[x["target_page_id"]].append(x)
existing_decisions = {x["url"].replace("https://www.houseofdiams.com", ""): x for x in rd("content-strategy/13_existing_content_decisions.csv")}
existing_inv = {x["url"].replace("https://www.houseofdiams.com", ""): x for x in rd("content-strategy/10_existing_content_inventory.csv")}
equity = {x["ranking_url"]: [] for x in rd("content-strategy/15_ranking_equity_protection.csv")}
for x in rd("content-strategy/15_ranking_equity_protection.csv"):
    equity[x["ranking_url"]].append(x)
kwlookup = json.load(open(SCR + "kwlookup.json"))
cannib = rd("architecture/15_cannibalization_check.csv")
paa_r2 = collections.defaultdict(list)
for x in rd("content-strategy/blog-calendar/revision/round2_paa_questions.csv"):
    paa_r2[x["keyword"].strip().lower()].append(x["paa_question"])
for x in rd("content-strategy/blog-calendar/final-consolidation/call2_serp_analysis.csv"):
    for q in x["paa_questions"].split(" | "):
        if q.strip():
            paa_r2[x["keyword"].strip().lower()].append(q.strip())
r2serp = {x["keyword"].strip().lower(): x for x in rd("content-strategy/blog-calendar/revision/round2_serp_analysis.csv")}
for x in rd("content-strategy/blog-calendar/final-consolidation/call2_serp_analysis.csv"):
    r2serp.setdefault(x["keyword"].strip().lower(), x)
serp185 = {x["keyword"].strip().lower(): x for x in rd("serp/analysis/18_5_targeted_serp_validation.csv")}


def kwinfo(k):
    v = kwlookup.get(k.strip().lower())
    if not v:
        return None
    return v


def fmt_kw(k):
    v = kwinfo(k)
    if not v:
        return k
    return f"{k} ({v['vol']:,}/mo)"


def split_list(s, sep=";"):
    return [p.strip() for p in s.split(sep) if p.strip()]


def strip_vol(s):
    return re.sub(r"\s*\(.*$", "", s).strip()


def req_concepts(tid, n=8):
    seen = []
    for x in sem.get(tid, []):
        if x["required_or_supporting"] == "REQUIRED" and x["concept"] not in seen:
            seen.append(x["concept"])
    return seen[:n]


def entities(tid, n=10, only_required=True):
    out = []
    for x in ecov.get(tid, []):
        if only_required and x["required_or_supporting"] != "REQUIRED":
            continue
        if x["entity"] not in out:
            out.append(x["entity"])
    return out[:n]


def top_questions(tid, n=5):
    order = {"CORE_SECTION": 0, "FAQ": 2, "SUPPORTING_SECTION": 1, "INLINE_ANSWER": 3}
    qs = [q for q in qcov.get(tid, []) if q["recommended_treatment"] in order]
    qs.sort(key=lambda q: order[q["recommended_treatment"]])
    seen, out = set(), []
    for q in qs:
        k = q["question"].lower()
        if k in seen:
            continue
        seen.add(k)
        out.append(q["question"])
        if len(out) >= n:
            break
    return out


def q_status_counts(tid):
    c = collections.Counter(q["coverage_status"] for q in qcov.get(tid, []))
    return dict(c)
