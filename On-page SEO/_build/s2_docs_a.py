# -*- coding: utf-8 -*-
"""Docs 02, 03, 04."""
import collections, re

TODAY = "2026-10-10"
VERIFIED = "2026-10-09"


def esc(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def mdt(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        out.append("| " + " | ".join(esc(c) for c in r) + " |")
    return "\n".join(out)


def short(s, n=110):
    s = (s or "").replace("\n", " ")
    return s if len(s) <= n else s[: n - 1] + "…"


def pth(u):
    return u.replace("https://www.houseofdiams.com", "") or "/"


def counts(rows):
    c = {}
    for k in ("Priority", "Status", "AWS Class", "Row Group", "Recommended Action"):
        c[k] = collections.Counter(r[k] for r in rows)
    c["bf"] = sum(1 for r in rows if r["HOD Facts Needed"] == "Y")
    c["gsc"] = sum(1 for r in rows if r["GSC Data Needed"] == "Y")
    return c


def doc03(rows):
    live = [r for r in rows if r["Row Group"] in ("CORE LIVE", "HUBS", "COMMERCIAL CATEGORY", "PRODUCT PAGES")]
    sub = [r for r in rows if r["Row Group"] == "COMMERCIAL SUBCATEGORY"]
    ex = [r for r in rows if r["Row Group"] == "EXISTING ARTICLES (Education-owned)"]
    pe = [r for r in rows if r["Row Group"] == "PLANNED EDUCATION"]
    pb = [r for r in rows if r["Row Group"] == "PLANNED BLOG"]

    def trow(r):
        return [r["Row ID"].replace("SUB:", ""), short(r["Current Title"], 60), r["Recommended Title (pre-suffix value)"], r["Rendered Length"], short(r["Title Action"], 70), r["Status"]]

    def mrow(r):
        return [r["Row ID"].replace("SUB:", ""), short(r["Current Meta"], 70), r["Recommended Meta"], r["Meta Length"], short(r["Meta Action"], 40)]

    th = ["Row", "Current title", "Recommended (pre-suffix)", "Rendered len", "Action", "Status"]
    mh = ["Row", "Current meta (truncated)", "Recommended meta", "Len", "Action"]
    ovr = [r for r in rows if isinstance(r["Rendered Length"], int) and r["Rendered Length"] > 60]
    p = ["""# 03 — Title & Meta Optimization

Generated %s. All values are **recommendations**; nothing was changed on the site. Companion data: `01-ON-PAGE-SEO-MASTER.csv` (columns *Recommended Title (pre-suffix value)*, *Rendered Title Preview*, *Rendered Length*, *Recommended Meta*, *Meta Length*, *Title/Meta Action*).

## 1. Brand-suffix verification (required before writing titles)

Read-only GET on 2026-10-09 (Step 2):

%s

**Rule:** enter the *pre-suffix* value; the template adds ` | House of Diams` (17 characters). So a rendered title of ≤60 characters needs a pre-suffix value of ≤~43. Homepage is the exception (absolute title, brand written into the value). The About, Contact and Privacy rows are worded so the brand is not repeated.

## 2. Title rules applied

1. One primary topic per title, matching the page's owner and search intent; no exact-match forcing; no stacked keywords.
2. Unique across the set (automated check: 0 duplicates among %d recommended rendered titles).
3. Front-load the distinguishing words; ≤~60 rendered characters is a **display guideline** — %d rows exceed it (listed in §7); those are live titles kept deliberately (key terms front-loaded) or approved package values.
4. American English is the confirmed rule (OD-05 adopted): jewelry, color, center, customize. Slugs such as `/fine-jewellery/` are never changed — only visible names, titles, metas, H1s and anchors.
5. **Commercial and Education titles are FINAL**: keyword ownership was resolved on 2026-10-10 (`10-DECISIONS-RESOLUTION-LOG.md`, `10-COMMERCIAL-KEYWORD-ASSIGNMENTS.csv`). Live changes on ranking-equity URLs still wait for the GSC baseline (see Status).
6. No shipping, returns, warranty, certification, "free" or "best/cheapest" wording anywhere.

## 3. Meta-description rules applied

Accurate to the page, answer-first where the page answers a question, one clear value statement, no keyword stuffing, no unverified promises, written for US searchers, unique. ~120–160 characters is a display guideline only. Where a page cannot yet support a promise (e.g. /returns has no terms) the meta is deliberately neutral.

### Step 1 draft claims removed

%s

## 4. Live pages — titles

%s

## 5. Commercial subcategories — titles (%d rows; empty/test pages are HELD)

%s

## 6. Existing Education articles — titles

%s

(Existing ranking-equity URLs keep their titles; changes need a GSC baseline. EDU-CERT-00 and EDU-CERT-01 change together.)

### Planned Education pages — final draft titles (primary keyword ratified under OD-03/OD-04)

%s

### Planned Blog posts — titles (10 approved package values carried unchanged; 23 drafts)

%s

## 7. Rendered titles above 60 characters

%s

## 8. Meta descriptions — live pages

%s

### Subcategories

%s

### Existing Education articles

%s

### Planned Education pages (drafts)

%s

### Planned Blog posts (10 approved carried unchanged; 23 drafts)

%s

## 9. Validation after AWS (Class C)

Fetch the rendered `<title>`, meta description, canonical and H1 for every row marked `REPLACE`/`CARRY APPROVED`; confirm the suffix is still appended once, the homepage title is absolute, and no duplicate titles/metas exist in the crawl.
""" % (
        TODAY,
        mdt(["URL", "og:title", "<title>"], [["/", "Lab-Grown Diamond Engagement Rings & Fine Jewellery", "Lab-Grown Diamond Engagement Rings & Fine Jewellery (no suffix)"],
             ["/engagement-rings", "Engagement Rings", "Engagement Rings | House of Diams"], ["/bespoke", "Bespoke", "Bespoke | House of Diams"],
             ["/shop/adeline-round-solitaire-stud-earrings", "Adeline 2 CTW Round Diamond Solitaire Stud Earrings", "… | House of Diams"],
             ["/blog/lab-grown-vs-natural-diamonds-the-honest-comparison-house-of-diams", "Lab-Grown vs Natural Diamonds: The Honest Comparison", "… | House of Diams"]]),
        len([r for r in rows if isinstance(r["Rendered Length"], int)]), len(ovr),
        mdt(["Step 1 draft (QA/05)", "Why not adopted", "Treatment"], [
            ["…with free insured worldwide delivery (home, shop, categories, subcategories)", "Shipping/insurance terms are an open business fact (progress.md); /shipping is a placeholder", "Removed from every meta"],
            ["…how our 15-day returns work (/returns)", "No return terms exist on the page; '15-Day' unconfirmed", "Neutral meta; policy to be written first"],
            ["Family-Run Diamond Jewellery Makers, Surat / in the trade since 2014 (/about)", "Founding year / family-run / Surat are published on-site but not in the confirmed-facts list", "Generic About meta; facts added only after HOD confirms"],
            ["Free design consultation and CAD sketch (/bespoke)", "Page claim, unconfirmed", "Meta describes the enquiry, not the offer terms"],
            ["…in 10K gold (categories/subcategories)", "Inventory claim that can drift; PDP metal lists show 10K and 14K", "Metal omitted at category level"],
            ["Lab-grown positioning in hub metas (e.g. /engagement-rings)", "OD-02 adopted: no separate lab-grown hub; origin stated at product level until F-E1", "Origin-neutral hub metas; origin stated at PDP level where the product record says so"]]),
        mdt(th, [trow(r) for r in live]), len(sub), mdt(th, [trow(r) for r in sub]), mdt(th, [trow(r) for r in ex]),
        mdt(th, [trow(r) for r in pe]), mdt(th, [trow(r) for r in pb]),
        mdt(["Row", "Rendered title", "Length", "Disposition"], [[r["Row ID"].replace("SUB:", ""), r["Rendered Title Preview"], r["Rendered Length"],
             "kept: key terms front-loaded" if r["Title Action"].startswith("KEEP") else ("approved package value" if r["Title Action"].startswith("CARRY") else "draft — tighten at writing if possible")] for r in ovr]),
        mdt(mh, [mrow(r) for r in live if r["Recommended Meta"]]), mdt(mh, [mrow(r) for r in sub if r["Recommended Meta"] and not r["Recommended Meta"].startswith("—")]),
        mdt(mh, [mrow(r) for r in ex]), mdt(mh, [mrow(r) for r in pe]), mdt(mh, [mrow(r) for r in pb]))]
    return p[0]


def doc04(rows):
    by = {r["Row ID"]: r for r in rows}
    live_ids = [r for r in rows if r["Row Group"] in ("CORE LIVE", "HUBS", "COMMERCIAL CATEGORY", "EXISTING ARTICLES (Education-owned)", "PRODUCT PAGES")]
    sub = [r for r in rows if r["Row Group"] == "COMMERCIAL SUBCATEGORY"]

    def hrow(r):
        return [r["Row ID"].replace("SUB:", ""), short(r["Current H1"], 60), r["Recommended H1"], short(r["H1 Action"], 80)]

    keep = [r["Row ID"] for r in rows if r["H1 Action"].startswith("KEEP") or r["H1 Action"].startswith("CARRY")]
    p = ["""# 04 — H1 & Content Optimization

Generated %s. Specifications only — no page was edited. Companion columns in the CSV: *Recommended H1*, *H1 Action*, *Content Action*, *Section Recommendations*.

## 1. H1 rules applied

* One clear H1 per page that names the page's subject in plain words and matches its search intent and owner; distinct from the `<title>` when that helps (the title is shorter and front-loaded; the H1 may be fuller).
* **Keep an acceptable H1.** %d rows are marked `KEEP`/`CARRY APPROVED` (e.g. homepage tagline, About, Shipping, Returns, the live article H1s that already contain the target terms). No change is recommended for its own sake.
* Generic "Explore <X>" H1s on category pages are replaced by the plain name; where the visible name contains a typo inherited from the category record ("Solitare", "Anniversay", "chain & Link", "T- BAR") the fix is to the **category name field**, never the slug.
* H1s follow the keyword assignments of 2026-10-10 (`OD-01`, `OD-03`, `OD-04`); an H1 change on a ranking-equity URL is applied only after the GSC baseline.
* Pages that should not be indexable while empty (17 subcategories + /collection) get **no H1 work** (HOLD, `OD-07`).

## 2. H1 table

%s

### Subcategories

%s

## 3. Content specifications — what to change on each important page

Each block is the `Content Action` and `Section Recommendations` cell of the CSV. Where a decision is pending the block says so.

%s

## 4. Content pattern for commercial category pages (hubs and subcategories)

1. **Definition line** (one sentence, plain words): what the category is.
2. **Short unique intro** (guideline ~80–200 words — not a target): what makes the category distinct, how to choose (shape, metal, size) with 1–2 descriptive Education links (Stage 16: category pages ≤5 Education links), a bespoke link where it fits.
3. **Product grid** with descriptive card names; pagination title/H1 rule for page ≥2.
4. **Optional visible Q&A (2–4 questions) only if specific to the category** — no sitewide boilerplate, **no FAQPage markup**.
5. **Trust line only with confirmed facts** (HOD questionnaire F-A1…F-E7).
6. **Not allowed:** keyword stuffing, repeating the same paragraph across categories, shipping/returns/certification promises, men's-band or Hip Hop propositions while those ranges are empty/unconfirmed.

## 5. Content pattern for Education pages (new and refreshed)

Answer-first: **question → direct answer → explanation → evidence/context → details → next action.** Use tables/steps/lists only where the SERP and the topic need them (grading scales, comparison tables, measuring steps). Define entities once and consistently; cite primary sources (GIA, IGI, standards bodies) where a factual claim is made; show a visible "last updated" date; no arbitrary word-count target; internal links per Stage 16/19 with descriptive anchors (`05`). New pages follow `19_content_briefs.csv` (sections and required questions) — the CSV row lists the brief's sections.

## 6. Trust-critical pages — CURRENT PROBLEM / CONFIRMED FACT / MISSING FACT / ACTION / OWNER / DEPENDENCY

**Only confirmed HOD business fact:** bespoke jewelry typically takes 2–3 weeks to make, then approximately 6–9 days delivery; generally about 3–4 weeks in total; depends on the stone selected; never a guarantee (`confirmed_business_facts.md`, user-supplied 2026-09-29). Everything else is UNCONFIRMED.

%s

### Site-wide trust items to resolve once (then reuse everywhere)

%s

## 7. Planned pages

The 20 new Education pages and 33 Blog posts are specified by their Stage 19 briefs / calendar rows (see `Section Recommendations` in the CSV and `09` for the ownership items that must be ratified first). The 10 packaged posts need no further on-page design. BC-001's publication is held pending F-A1 ('insured shipping' wording); the package itself was not touched.
""" % (TODAY, len(keep),
       mdt(["Row", "Current H1", "Recommended H1", "Action"], [hrow(r) for r in live_ids]),
       mdt(["Row", "Current H1", "Recommended H1", "Action"], [hrow(r) for r in sub if not r["Recommended H1"].startswith("—")]),
       "\n\n".join("### %s — %s\n* **Content action:** %s\n* **Sections / changes:** %s\n* **Status:** %s · **Priority:** %s · **AWS:** %s%s" % (
           r["Row ID"], r["Page Name"], r["Content Action"], r["Section Recommendations"], r["Status"], r["Priority"], r["AWS Class"],
           (" · **Decision resolution:** " + r["Decision Resolution"]) if r["Decision Resolution"] else "")
           for r in rows if r["Row Group"] in ("CORE LIVE", "HUBS", "COMMERCIAL CATEGORY", "PRODUCT PAGES", "EXISTING ARTICLES (Education-owned)") and r["Status"] != "NO CHANGE REQUIRED"),
       mdt(["Page", "CURRENT PROBLEM", "CONFIRMED FACT", "MISSING FACT (HOD must supply)", "RECOMMENDED ACTION", "OWNER", "DEPENDENCY"], [
           ["/shipping", "Visible placeholder text 'new test black / test desc'; no concrete timelines; badges elsewhere promise 'Complimentary Insured Shipping' / 'Overnight Shipping'", "Bespoke timeline only", "Regions served; processing vs transit times (in-stock vs made-to-order); carriers; insurance/signature terms; US duties/taxes; free-shipping terms; holiday order-by dates", "Delete the placeholder; write the policy from confirmed facts; align header/home/PDP statements", "HOD (facts) + content editor", "F-A1; CMS edit timing E-01/E-02; schema (OfferShippingDetails) after AWS"],
           ["/returns", "Body shows only the 'Is House of Diams legitimate?' answer + contact; NO return terms; Admin@ vs info@ email; odd hours", "None", "Return/exchange window, condition, exclusions (bespoke/made-to-order), refund method/timing, return shipping, how to start a return", "Publish the full policy; move the legitimacy answer to /about & /faq; one contact email; remove FAQPage from this page; MerchantReturnPolicy once final", "HOD + content editor", "F-A2, F-C2; schema Class B (E-08)"],
           ["/bespoke", "'4-6 week typical lead time' contradicts the confirmed fact; unverified 'Full IGI / GIA certification included', 'insured delivery complimentary to 40+ countries', 'Free design consultation — CAD sketch', 'within 24 hours'; form-only page", "Typically 2–3 weeks to make + ~6–9 days delivery = generally ~3–4 weeks from design approval to delivery (start point stated by the user 2026-10-10), stone-dependent, not a guarantee", "Which of the other claims are true; what a commission includes; real process steps; price guidance (route to BC-024)", "Replace lead time with the confirmed wording (applied); remove the other claims until confirmed; add explanatory copy; visible FAQ answers", "HOD (user said they are handling the copy)", "Title/H1 final (OD-01); F-D1, F-B1; E-02"],
           ["/about", "Placeholder tile ('Certified Jewelery' shows a pendant description); 'Jewelery' typo; founder 'Akshar korat co founder' vs bylines 'Krish Babriya, Co-founder'; 'half a century' vs 2014; 'Conflict Free'/'Ethically Certified' values", "None (Surat/2014/NY office published but unconfirmed)", "Founder names/roles; founding year; locations; what 'conflict free'/'ethically certified' mean and their evidence", "Correct placeholders; reconcile founders; add an entity-facts block that matches Organization schema", "HOD + content editor", "F-C1; schema (AboutPage, Person) after AWS"],
           ["/contact", "307 to a modal; not in sitemap; FAQ references houseofdiams.com/contact; email/phone variants (info@ vs Admin@; +91 only)", "None", "Public email, phone(s), address, response-time statement", "Build a real /contact page (OD-09 adopted); one contact set everywhere; ContactPage schema", "HOD", "OD-09 adopted (build page); F-C2; E-12"]]),
       mdt(["Item", "Where it appears today", "Status"], [
           ["Certification lab(s) and 'IGI Certified' / 'IGI / GIA' wording", "Home badge, /bespoke, PDP descriptions, FAQ", "UNCONFIRMED — HOD INPUT (F-B1)"],
           ["'Lifetime Warranty' / 'Care & Warranty' text", "Home badge, every PDP", "UNCONFIRMED"],
           ["'Complimentary (Overnight) Insured Shipping', '15-Day Returns'", "Header badge, home badge, PDP shipping block", "UNCONFIRMED"],
           ["Contact email, phone, address, hours", "Footer, /returns, modal", "Inconsistent"],
           ["Founder names/roles, founding year, locations", "/about, /faq, /returns, blog bylines", "Inconsistent / UNCONFIRMED"],
           ["Hip Hop range; natural-diamond offer; platinum; cleaning/appraisal services", "Nav (Hip Hop), calendar notes", "UNCONFIRMED"],
           ["Expired-looking 'September sale … HOUSEOFDIAMS2026' promo", "Homepage, PDP", "Merchandising owner to confirm/remove"]]))]
    return p[0]
