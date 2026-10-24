"""Step 2 loader: reads Step 1 outputs + source-of-truth files READ-ONLY and exposes lookups."""
import csv, json, re, collections, ast

ROOT = "/Users/manavdesai/Desktop/HOD SEO"
KW = ROOT + "/Keywords/content SEO"
SITE = "https://www.houseofdiams.com"


def rd(path):
    return list(csv.DictReader(open(path, encoding="utf-8-sig")))


S1 = rd(ROOT + "/QA/01-MASTER-SEO-IMPLEMENTATION-MAP.csv")
S1_BY = {r["Row ID"]: r for r in S1}
CAL = {r["content_id"]: r for r in rd(KW + "/FINAL-BLOG-CALENDAR/BLOG_CALENDAR_FINAL.csv")}
REG = {r["target_id"]: r for r in rd(KW + "/architecture/15_target_page_registry.csv")}
KMAP = rd(KW + "/architecture/15_keyword_url_map.csv")
BRIEFS = rd(KW + "/content-strategy/19_content_briefs.csv")
BRIEFREG = {r["target_page_id"]: r for r in rd(KW + "/content-strategy/19_brief_registry.csv")}
LINKMAP = rd(KW + "/architecture/16_internal_link_map.csv")
LINKREQ = rd(KW + "/architecture/16_page_link_requirements.csv")
ANCHORS = rd(KW + "/architecture/16_anchor_strategy.csv")
QMAP = rd(KW + "/content-strategy/17_question_map.csv")
PDP = rd(ROOT + "/QA/06-PDP-AUDIT-APPENDIX.csv")
CRAWL = {}
for x in json.load(open(ROOT + "/QA/_build/evidence/crawl/crawl.json")):
    p = x["url"].replace(SITE, "") or "/"
    CRAWL[p] = x
import os
PKG = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pkg_meta.json")))


PAA2 = rd(KW + "/content-strategy/blog-calendar/revision/round2_paa_questions.csv")
S185 = rd(KW + "/serp/analysis/18_5_targeted_serp_validation.csv")


def paa_for(keyword):
    """PAA / recurring questions already captured in the calendar rounds or Stage 18.5 (no new research)."""
    k = (keyword or "").lower().strip()
    out = []
    for x in PAA2:
        if x["keyword"].lower().strip() == k and x["paa_question"] not in out:
            out.append(x["paa_question"])
    if not out:
        for x in S185:
            if x["keyword"].lower().strip() == k:
                out = [q.strip() for q in x["recurring_questions"].split(";") if q.strip()]
    return out


def path_of(url):
    return (url or "").replace(SITE, "") or "/"


def stage15_top(target_id, n=4):
    rows = [x for x in KMAP if x["target_id"] == target_id]
    def vol(x):
        try:
            return int(float(x["search_volume"]))
        except Exception:
            return -1
    rows.sort(key=lambda x: -vol(x))
    return [(x["keyword"], x["search_volume"]) for x in rows[:n]], len(rows)


def brief_sections(target_id):
    out = []
    for b in BRIEFS:
        if b["target_page_id"] == target_id and b["heading_level"] in ("H1", "H2"):
            out.append((b["importance"], b["heading"]))
    return out


def content_state(path):
    c = CRAWL.get(path)
    if not c:
        return "NOT LIVE / not crawled"
    h2 = [h for h in c.get("h2s", []) if h and h != "Contact Us"][:8]
    return "%s words; %s imgs (%s without alt in initial HTML); H2: %s" % (
        c.get("word_count"), c.get("img_count"), c.get("img_no_alt"), " / ".join(h2) if h2 else "none beyond template")


def live_links(path):
    c = CRAWL.get(path)
    if not c:
        return None
    il = c.get("internal_links")
    if isinstance(il, str):
        try:
            il = ast.literal_eval(il)
        except Exception:
            il = []
    return set(il or [])


if __name__ == "__main__":
    print(len(S1), len(CAL), len(REG), len(KMAP), len(BRIEFS), len(LINKMAP), len(CRAWL))
    print(stage15_top("EDU-4C-06"))
    print(brief_sections("EDU-4C-06")[:6])
    print(content_state("/bespoke"))
