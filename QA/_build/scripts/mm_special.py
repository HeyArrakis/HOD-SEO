"""Special rows: grouping page, legacy/redirect URLs, hiphop, PDP rows, blog/education hubs, plus PDP appendix."""
import re, json, collections
import lib_research as L
from mm_core import *
import mm_helpers as H
from mm_live import base_row, finish, kwc, link_gap_text, SRC_COMMON, D19
from mm_cat import SRC_CAT, nprod, prod_txt


def special_rows():
    rows = []

    # ---------- /engagement-rings/by-design group page
    p = "/engagement-rings/by-design"
    r = base_row(p, "COMMERCIAL CATEGORY", "COM-ER-STYLES-GROUP", "Engagement Rings > By Design (grouping page)", "SUBCATEGORY_GROUP", "Engagement Rings (commercial)", "Commercial (grouping)")
    r["Primary Keyword"] = "NO PRIMARY KEYWORD — GROUPING-ONLY SEGMENT (Stage 12 D-03 removes the 'by-desgin' grouping segment in the future hierarchy)"
    r["Keyword Owner"] = "none"; r["Search Intent"] = "n/a"
    r["Existing Keyword Ownership Conflict?"] = "NO keyword — but the page is a exact duplicate of /engagement-rings (identical 61-piece grid, same boilerplate FAQ)."
    r["Cannibalization Risk"] = "HIGH — CANNIBALIZATION REVIEW REQUIRED: same subject and identical product set as /engagement-rings (61 pieces on both; both self-canonical, both in the sitemap)."
    r["Recommended SEO Title"] = "No change — decide consolidation first"; r["Recommended Meta Description"] = "—"; r["Recommended H1"] = "—"
    r["Recommended Content/Section Changes"] = "Do NOT merge or delete automatically. Options for the decision: (a) canonical → /engagement-rings and drop from sitemap; (b) 301 → /engagement-rings once the new hierarchy is chosen; (c) keep as a style index with unique copy. Choose together with the AWS URL/redirect plan (any URL change needs migration reasoning, CLAUDE.md rule 12)."
    r["Recommended Internal Links IN"] = "Header nav only today; remove from nav or keep consistent with the decision."; r["Recommended Internal Links OUT"] = "Style subcategories"
    r["Internal-Link Priority"] = "LOW"; r["Recommended Schema"] = "BreadcrumbList only."; r["Schema Validation/Review Needed?"] = "LOW"
    r["AEO Opportunity"] = "NONE"; r["GEO/AI Search Opportunity"] = "NONE"
    r["Recommended Action"] = "REVIEW"; r["Priority"] = "HIGH"
    r["Implementation Dependency"] = "IA decision on the grouping segment (D-03); redirect plan"; r["Status"] = "LIVE — DUPLICATE OF PARENT"
    r["Evidence / Source"] = SRC_CAT + "; 12_current_vs_proposed_ia.csv"; r["Notes"] = "New since Stage 1 (spelling-corrected rename of the old /by-desgin group). Whether it is intended as an index page is UNKNOWN — VERIFY with the site owner."
    rows.append(finish(r, dict(cannib=1, conflict=0), a=["decision memo"], b=["canonical/redirect/sitemap change"], c=["canonical, sitemap, status"]))

    # ---------- legacy by-desgin side-stone (REDIRECT, ranking equity)
    p = "/engagement-rings/by-desgin/side-stone-rings"
    r = base_row(p, "LEGACY / REDIRECT", "LEG-ER-SIDESTONE", "LEGACY URL — Side-stone rings (old 'by-desgin' path)", "LEGACY_URL (404)", "Engagement Rings (commercial)", "Supporting (redirect source)")
    r["Primary Keyword"] = "NONE of its own — the owned keyword ('side stones engagement rings', 1,000/mo; Stage 3 snapshot est. pos 104, DataForSEO Labs not GSC) is now carried by /engagement-rings/by-design/side-stone-rings"
    r["Keyword Owner"] = "COM-ER-SIDESTONE — ratified; URL has moved"
    r["Existing Keyword Ownership Conflict?"] = "YES (documentation) — Stage 13/15/16 record this exact URL as 'KEEP / NO_ACTION / keep current paths' (ranking-equity row 'NO_MIGRATION_RECOMMENDED'), but on 2026-10-09 it returns 404 and the content lives at /engagement-rings/by-design/side-stone-rings."
    r["Cannibalization Risk"] = "NONE (404)"
    r["Recommended SEO Title"] = "—"; r["Recommended Meta Description"] = "—"; r["Recommended H1"] = "—"
    r["Recommended Content/Section Changes"] = "Add a 1:1 301 from /engagement-rings/by-desgin/side-stone-rings → /engagement-rings/by-design/side-stone-rings (and equivalent 301s for any other old /by-desgin/* URLs that were ever indexed — all 8 tested old URLs currently return 404). Include in the AWS migration redirect map; do not rely on the 404."
    r["Recommended Internal Links IN"] = "None (retire any remaining links)"; r["Recommended Internal Links OUT"] = "—"; r["Internal-Link Priority"] = "n/a"
    r["Recommended Schema"] = "n/a"; r["Schema Validation/Review Needed?"] = "NO"; r["AEO Opportunity"] = "NONE"; r["GEO/AI Search Opportunity"] = "NONE"
    r["Recommended Action"] = "REDIRECT"; r["Priority"] = "CRITICAL"
    r["Implementation Dependency"] = "Redirect rule in the production/AWS edge or app routing; confirm in GSC (Pages report) whether the old URL was indexed"
    r["Status"] = "LEGACY URL — 404"; r["Evidence / Source"] = "Live crawl 2026-10-09 (404); content-strategy/15_ranking_equity_protection.csv; 13_existing_content_decisions.csv; architecture/12_current_vs_proposed_ia.csv"
    r["Notes"] = "Equity is small (1 ranked keyword, est. position 104 in a DataForSEO snapshot) but it is the only commercial URL in Stage 3 and the only subcategory that passes the D-07 gate. Rationale for CRITICAL: ranking-equity URL returning 404 against a documented 'preserve existing URLs' rule. Status could be intentional (spelling fix) — then the redirect is the missing step."
    rows.append(finish(r, dict(conflict=1), a=["redirect map entry (spreadsheet)"], b=["implement 301 in the AWS routing/edge config — DO NOT IMPLEMENT WITHOUT MIGRATION PLAN"], c=["301 status, target 200, GSC URL inspection"]))

    p = "/engagement-rings/by-desgin"
    r = base_row(p, "LEGACY / REDIRECT", "LEG-ER-GROUP", "LEGACY URL — Engagement rings 'by-desgin' group", "LEGACY_URL (404)", "Engagement Rings (commercial)", "Supporting (redirect source)")
    r["Primary Keyword"] = "NONE"; r["Keyword Owner"] = "none"; r["Existing Keyword Ownership Conflict?"] = "NO"; r["Cannibalization Risk"] = "NONE"
    r["Recommended Content/Section Changes"] = "Map in the redirect plan (→ /engagement-rings or → /engagement-rings/by-design, per the grouping-page decision). Low value if it was never indexed (not in the Stage 1 sitemap)."
    r["Recommended SEO Title"] = r["Recommended Meta Description"] = r["Recommended H1"] = "—"
    r["Recommended Action"] = "REDIRECT"; r["Priority"] = "LOW"; r["Implementation Dependency"] = "Grouping-page decision"
    r["Status"] = "LEGACY URL — 404"; r["Evidence / Source"] = "Live crawl 2026-10-09 (404); Stage 10 (nav-only layer)"; r["Notes"] = "Was linked in nav only (Stage 10), not in the sitemap."
    r["Internal-Link Priority"] = "n/a"; r["Recommended Schema"] = "n/a"; r["Schema Validation/Review Needed?"] = "NO"; r["AEO Opportunity"] = "NONE"; r["GEO/AI Search Opportunity"] = "NONE"
    r["Recommended Internal Links IN"] = r["Recommended Internal Links OUT"] = "—"
    rows.append(finish(r, {}, a=["redirect map entry"], b=["implement 301"], c=["status"]))

    # ---------- /hiphop
    p = "/hiphop"
    r = base_row(p, "LEGACY / REDIRECT", "COM-HIPHOP", "Hip Hop (curated collection) — now redirects to /shop", "CURATED_COLLECTION → 308 redirect", "Curated collections", "Commercial (curated, conditional)")
    r["Primary Keyword"] = "NO PRIMARY KEYWORD (curated collection; INDEXABLE_CONDITIONAL in Stage 12)"; r["Keyword Owner"] = "none"
    r["Existing Keyword Ownership Conflict?"] = "NO"; r["Cannibalization Risk"] = "LOW"
    r["Recommended Content/Section Changes"] = "Stage 1 saw /hiphop as a 'Coming Soon' placeholder in the sitemap; it now 308-redirects to /shop and is out of the sitemap — good. But its children (/hiphop/chains, /hiphop/chains/cuban-links, /hiphop/test-subcat) are still live, empty and listed in the sitemap, and /shop's meta still mentions 'hip hop jewellery'. Decide whether a Hip Hop line exists (business fact) and align children, sitemap and /shop copy."
    r["Recommended SEO Title"] = r["Recommended Meta Description"] = r["Recommended H1"] = "—"
    r["Internal-Link Priority"] = "LOW"; r["Recommended Internal Links IN"] = r["Recommended Internal Links OUT"] = "—"; r["Recommended Schema"] = "n/a"; r["Schema Validation/Review Needed?"] = "NO"
    r["AEO Opportunity"] = "NONE"; r["GEO/AI Search Opportunity"] = "NONE"
    r["Recommended Action"] = "REVIEW"; r["Priority"] = "MEDIUM"; r["Implementation Dependency"] = "Business decision (is there a Hip Hop range?)"
    r["Status"] = "LIVE — REDIRECT (308)"; r["Evidence / Source"] = SRC_COMMON + "; 12_ia_proposed_structure.csv (Curated collections: Hip Hop)"; r["Notes"] = "308 = permanent redirect."
    rows.append(finish(r, dict(links=0), a=["decision memo"], b=["child-page cleanup"], c=["redirect type/target"]))

    # ---------- removed PDPs
    for path, nm, note in (("/shop/fine-jewellery-test-product", "REMOVED — test product (was live at Stage 1)", "Stage 1 flagged this test product as live/indexable; it now returns 404 — resolved. Keep it out of the AWS content migration (do not re-import test data)."),
                           ("/shop/marquise-floral-diamond-engagement-ring", "REMOVED — product (was in Stage 1 sitemap)", "Product from the Stage 1 sitemap now 404 and absent from the live sitemap. No ranking equity recorded. If the product was discontinued, consider a 301 to the closest style page or a 410; confirm intent.")):
        r = base_row(path, "LEGACY / REDIRECT", "LEG-" + path.split("/")[-1][:30], nm, "LEGACY_URL (404)", "Shop (commercial)", "Supporting")
        r["Primary Keyword"] = "NONE"; r["Keyword Owner"] = "none"; r["Existing Keyword Ownership Conflict?"] = "NO"; r["Cannibalization Risk"] = "NONE"
        r["Recommended SEO Title"] = r["Recommended Meta Description"] = r["Recommended H1"] = "—"
        r["Recommended Content/Section Changes"] = note
        r["Internal-Link Priority"] = "n/a"; r["Recommended Internal Links IN"] = r["Recommended Internal Links OUT"] = "—"; r["Recommended Schema"] = "n/a"; r["Schema Validation/Review Needed?"] = "NO"
        r["AEO Opportunity"] = "NONE"; r["GEO/AI Search Opportunity"] = "NONE"
        r["Recommended Action"] = "REVIEW" if "marquise" in path else "NO ACTION"; r["Priority"] = "LOW"; r["Implementation Dependency"] = "—"
        r["Status"] = "LEGACY URL — 404"; r["Evidence / Source"] = "Live crawl 2026-10-09; site/01_site_inventory.csv"; r["Notes"] = note
        rows.append(finish(r, {}, a=["none"], c=["status"]))

    # ---------- PDP template row
    pdp = [x for x in crawl.values() if "/shop/" in x["url"] and x["url"] in sitemap_urls and x["status"] == 200 and "title" in x]
    n = len(pdp)
    long_t = sum(1 for x in pdp if len(x["title"]) > 60)
    plc = [x for x in pdp if " · " in x["meta_description"]]
    odd = [x for x in pdp if re.search(r"\d{8,}|-copy-", x["url"])]
    tcount = collections.Counter(x["title"] for x in pdp); mcount = collections.Counter(x["meta_description"] for x in pdp)
    dup_t = sum(c for t, c in tcount.items() if c > 1); dup_m = sum(c for t, c in mcount.items() if c > 1)
    r = base_row("/shop/<slug>", "PRODUCT PAGES", "COM-PDP", f"Product detail pages (template; {n} in live sitemap)", "PRODUCT_DETAIL_PAGE (template group)", "Shop (commercial)", "Transactional")
    r["Primary Keyword"] = "NO PRIMARY KEYWORD at template level (owns no Stage 15 keyword); product-name + attribute per page. Exception: COM-PDP-OVAL-FLORAL (see its row)."
    r["Secondary Keywords"] = "Per-product attributes (shape, metal, carat, style) from product data — not researched keywords"
    r["Search Intent"] = "TRANSACTIONAL (product)"; r["Keyword Owner"] = "COM-PDP — none"
    r["Existing Keyword Ownership Conflict?"] = "NO"; r["Cannibalization Risk"] = f"LOW–MEDIUM — {len(odd)} PDPs use numeric-ID/'-copy-' slugs for carat variants (pairs of near-identical pages); {sum(1 for t,c in tcount.items() if c>1)} duplicate title(s) found."
    r["Current SEO Title"] = f"Pattern: '<Product name> | House of Diams' ({n} crawled; {long_t} titles >60 chars; {sum(1 for x in pdp if 'House of Diams' not in x['title'])} without brand)"
    r["Current Meta Description"] = f"Descriptive product copy on most; {len(plc)} placeholder-style metas ('<Category> · <Metal> - House of Diams'); {dup_m} PDPs share a duplicated meta; ≥{sum(1 for x in pdp if len(x['meta_description'])>160)} over 160 chars"
    r["Current H1"] = "Product name (1 H1 on every crawled PDP)"; r["Current Canonical"] = f"Self-referencing on all {n} crawled PDPs"
    r["Current Indexability"] = f"INDEXABLE — HTTP 200 on all {n}; no noindex; all in sitemap (sitemap has no <lastmod>)"
    r["Current URL Status"] = f"200 ×{n} (crawl {CRAWL_DATE})"
    r["Current Schema"] = "Product + Offer (price, USD, availability) + Brand + BreadcrumbList + Organization on all PDPs; NO AggregateRating/Review markup (correct — none visible); product image URLs point to Supabase storage and a Cloudflare R2 *.r2.dev host (…/products/draft/images/…)."
    r["Recommended SEO Title"] = "<Product name> – <metal/shape/stone key attribute> | House of Diams (≤60 chars; keep product name first)"
    r["Recommended Meta Description"] = "Template: '<Name>: <1-sentence description with shape, carat, metal>. Lab-grown diamond, free insured worldwide delivery.' Replace the 6 placeholder metas and the duplicated ones first."
    r["Recommended H1"] = "Keep product name"
    r["Recommended Content/Section Changes"] = ("(1) Fix 6 placeholder-style metas and duplicate title/meta groups (list in 06-PDP-AUDIT-APPENDIX.csv). (2) Resolve the 'Gold Vermil' truncated material label visible on listings. (3) Variant strategy: 10 PDPs carry numeric-ID/'-copy-' slugs (carat variants as separate URLs) — IA D-11 prefers one URL per product with variants on-page; any change needs a redirect plan. "
        "(4) Add visible shipping/returns summary and link to certification guide (Stage 16 PDP rows: ≤3 Education links: ring size, grades). (5) Add MerchantReturnPolicy/OfferShippingDetails only after policy text is final.")
    r["Recommended Image/Alt-Text Changes"] = "Alt text per product image: '<Product name>, <view/angle>'. Initial-HTML scan found many <img> without alt (counts include UI images) — audit the rendered PDP gallery. Product image URLs will change with the R2/Supabase → AWS move: keep Product.image values valid and stable."
    r["Recommended Internal Links IN"] = H.link_summary("COM-PDP", "in"); r["Recommended Internal Links OUT"] = H.link_summary("COM-PDP", "out")
    r["Recommended Anchor Context"] = "Product names; Education anchors per 16_anchor_strategy (ring size, grades)."; r["Internal-Link Priority"] = "MEDIUM"
    r["Recommended Schema"] = "Keep Product + Offer + BreadcrumbList. Add priceValidUntil/itemCondition/shippingDetails/hasMerchantReturnPolicy only if accurate. Do NOT add review/rating or FAQ markup."
    r["Schema Validation/Review Needed?"] = "YES — re-run Rich Results Test / Merchant Center checks after AWS (image URLs, availability, price feed)."
    r["AEO Opportunity"] = "LOW"; r["Primary Questions to Answer"] = "Is it lab-grown? Which metal/carat? Delivery and returns? (answer in a spec block)"; r["Answer-First Opportunity"] = "Spec block (stone shape, carat, origin, metal, certification) above the description."
    r["PAA/Question Coverage Needed?"] = "NO"
    r["GEO/AI Search Opportunity"] = "HIGH for AI shopping surfaces: complete, consistent Product attributes (material, stone, carat, origin, certification) + stable image URLs + /llms.txt product list."
    r["Important Entities"] = "Product name; lab-grown diamond; metal (10K/14K/18K vermeil); shape; carat; IGI/GIA (verify)"; r["Entity Clarity Needed?"] = "YES — certification claim per product must be explicit."
    r["Brand/Expertise/Trust Signal Opportunity"] = "Certification report link/number where available; return policy summary."
    r["Recommended Action"] = "OPTIMIZE"; r["Priority"] = "HIGH"
    r["Implementation Dependency"] = "Product data/CMS access; template change for schema/spec block; redirect plan for variant slugs"
    r["Status"] = "LIVE — NEEDS OPTIMIZATION"
    r["Evidence / Source"] = SRC_CAT + "; 06-PDP-AUDIT-APPENDIX.csv (this task)"; r["Notes"] = "Sitemap PDP count rose 169 → 184 since Stage 1. Per-PDP audit lives in the appendix, not in this map (avoids ~184 low-signal rows)."
    gsc_na(r); r["Row Group"] = "PRODUCT PAGES"
    rows.append(finish(r, dict(meta=1, schema=1, links=1, geo=1, cannib=1), a=["metadata fixes list", "alt-text rules", "variant-URL decision memo"], b=["schema/spec-block template; image URL changes; variant redirects"], c=["Product schema validity, image URLs resolve, canonical, price/availability, CWV"]))

    # ---------- oval floral PDP
    p = "/shop/oval-floral-diamond-ring"
    r = base_row(p, "PRODUCT PAGES", "COM-PDP-OVAL-FLORAL", "Oval floral diamond ring (PDP) — keyword owner", "PRODUCT_DETAIL_PAGE", "Shop (commercial)", "Transactional")
    r["Primary Keyword"] = "marquise oval diamond (390/mo) — Stage 15 OWNER (COM-PDP-OVAL-FLORAL; Stage 3 snapshot est. pos 90, PRODUCT SERP; not GSC)"
    r["Secondary Keywords"] = "—"; r["Search Intent"] = "TRANSACTIONAL (Stage 8 PRODUCT SERP)"; r["Keyword Owner"] = "COM-PDP-OVAL-FLORAL — RATIFIED (Stage 15)"
    r["Existing Keyword Ownership Conflict?"] = "REVIEW — the product's displayed name/title changed to 'Oval Marquise Side-Stone Engagement Ring' while the slug stays 'oval-floral-diamond-ring'; it may now also compete with /engagement-rings/by-design/side-stone-rings (COM-ER-SIDESTONE) for 'side-stone' wording."
    r["Cannibalization Risk"] = "MEDIUM — title now says 'Side-Stone' (the COM-ER-SIDESTONE keyword); keep PDP wording product-specific."
    r["Recommended SEO Title"] = "Oval Marquise Diamond Engagement Ring, 2.5 ct | House of Diams"
    r["Recommended Meta Description"] = "Oval diamond engagement ring with a 2.5 ct center stone and 16 marquise accents. Free insured worldwide delivery. (FACT-CHECK specs against the product record.)"
    r["Recommended H1"] = "Oval Marquise Side-Stone Engagement Ring (keep product name)"
    r["Recommended Content/Section Changes"] = "Do NOT change the slug (ranking URL; Stage 13 NO_ACTION). Keep 'oval' and 'marquise' in the title/H1/description (they match the owned keyword 'marquise oval diamond'); avoid repeating 'side-stone' as the lead term to keep COM-ER-SIDESTONE separate. Stage 16 REQUIRED links: COM-ER, COM-ER-SIDESTONE, EDU-RJG-02."
    r["Recommended Image/Alt-Text Changes"] = "Alt text: 'Oval marquise side-stone engagement ring, <view>'."
    r["Recommended Internal Links IN"] = H.link_summary("COM-PDP-OVAL-FLORAL", "in"); r["Recommended Internal Links OUT"] = H.link_summary("COM-PDP-OVAL-FLORAL", "out") + " || " + link_gap_text("COM-PDP-OVAL-FLORAL", p)
    r["Recommended Anchor Context"] = "Product name anchors."; r["Internal-Link Priority"] = "MEDIUM"
    r["Recommended Schema"] = "Product + Offer + BreadcrumbList (present)."; r["Schema Validation/Review Needed?"] = "LOW"
    r["AEO Opportunity"] = "LOW"; r["GEO/AI Search Opportunity"] = "Product attributes in a spec block."; r["Important Entities"] = "Oval diamond; marquise accents; 2.5 ct"
    r["Entity Clarity Needed?"] = "NO"; r["Recommended Action"] = "OPTIMIZE"; r["Priority"] = "MEDIUM"
    r["Implementation Dependency"] = "Product data/CMS"; r["Status"] = "LIVE — PROTECT URL"
    r["Evidence / Source"] = SRC_CAT + "; 15_ranking_equity_protection.csv"; r["Notes"] = "Title now differs from the slug and from the owned keyword; GSC data would show whether the rename changed performance."
    rows.append(finish(r, dict(meta=1, links=1, conflict=1, cannib=1), a=["metadata drafts"], b=["none"], c=["status, canonical, schema"]))

    # ---------- COM-LG-HUB (conditional commercial lab-grown hub)
    r = new_row()
    r["URL"] = "NOT BUILT — conditional (no URL proposed; Stage 12 D-05) [COM-LG-HUB]"
    r["Page Type"] = "ORIGIN_HUB (conditional commercial)"; r["Page/Content Name"] = "Lab-Grown Diamonds — commercial hub (COM-LG-HUB)"; r["SEO Cluster / Topic"] = "Lab-Grown Diamonds (commercial) — CL-001"
    r["Page Role"] = "Commercial (conditional)"
    r["Primary Keyword"] = "UNOWNED HEAD TERMS (CL-001, Stage 15 CONDITIONAL_NOT_MAPPED, 27 keywords): lab grown diamonds (135,000), lab diamonds (27,100), lab created diamonds (12,100). Related origin×type heads in blog research: lab grown diamond rings / engagement rings (90,500 each)."
    r["Secondary Keywords"] = L_kw = kwc("lab grown diamonds", "lab diamonds", "lab grown diamond rings", "lab grown diamond engagement rings")
    r["Related/Semantic Concepts"] = "lab-grown diamond jewellery; IGI/GIA certified; CVD/HPHT (Education owns); price"
    r["Search Intent"] = "MIXED — Stage 8: retailer collection/BRAND SERPs for the head terms (commercial), informational for everything else (DISTINCT_INTENT)"
    r["Keyword Owner"] = "COM-LG-HUB — CONDITIONAL (needs business confirmation of which lab-grown products HOD sells; G18-0012)"
    r["Existing Keyword Ownership Conflict?"] = "REVIEW — the live homepage title and site positioning already target lab-grown ('Lab-Grown Diamond Engagement Rings & Fine Jewellery', PDP copy 'lab-grown diamond'), yet the dedicated commercial owner is 'conditional' and unbuilt, leaving the 135,000/mo head term unowned."
    r["Cannibalization Risk"] = "MEDIUM — homepage and /engagement-rings titles currently stand in for the missing hub; EDU-LG-00 must NOT target these heads (Stage 14 D14-05)."
    for k in ("Current SEO Title", "Current Meta Description", "Current H1", "Current Canonical", "Current Indexability", "Current Schema"):
        r[k] = "NOT LIVE — page does not exist"
    r["Current URL Status"] = "NOT BUILT"
    r["Recommended SEO Title"] = "Decision first — then e.g. 'Lab-Grown Diamond Jewellery | House of Diams' (DRAFT)"; r["Recommended Meta Description"] = "Write after the business decision"; r["Recommended H1"] = "Lab-Grown Diamond Jewellery (DRAFT)"
    r["Recommended Content/Section Changes"] = "Business decision needed: confirm the catalogue is lab-grown (all PDP copy says so) and whether to activate this hub (a curated collection page listing products with origin/certification facts, linking to EDU-LG-00/02/03/10). Reuse existing data for the decision (CL-001 SERPs validated in Stage 8); a fresh commercial SERP check would be a paid step needing approval."
    r["Recommended Internal Links IN"] = "Header nav (if activated), homepage, EDU-LG-00 hand-off"; r["Recommended Internal Links OUT"] = "EDU-LG-00, EDU-LG-02, EDU-LG-03, EDU-LG-10, category hubs"
    r["Recommended Anchor Context"] = "Avoid bare head-term anchors from Education pages until activated (16_anchor_strategy)."; r["Internal-Link Priority"] = "n/a until activated"
    r["Recommended Schema"] = "CollectionPage/ItemList + BreadcrumbList when built."; r["Schema Validation/Review Needed?"] = "At launch"
    r["AEO Opportunity"] = "LOW"; r["Primary Questions to Answer"] = "—"; r["Answer-First Opportunity"] = "—"; r["PAA/Question Coverage Needed?"] = "NO"
    r["GEO/AI Search Opportunity"] = "An explicit 'we sell lab-grown diamond jewellery' entity page is the clearest statement for AI systems of HOD's category."
    r["Important Entities"] = "Lab-grown diamond; IGI; GIA; House of Diams"; r["Entity Clarity Needed?"] = "YES"; r["Brand/Expertise/Trust Signal Opportunity"] = "Certification facts (open business fact)."
    gsc_na(r)
    r["Recommended Action"] = "REVIEW"; r["Priority"] = "HIGH"; r["Implementation Dependency"] = "Business confirmation; owner decision (D-05); keyword ratification"
    r["Status"] = "CONDITIONAL — NOT BUILT"; r["Evidence / Source"] = "architecture/12_ia_decision_log.md D-05; 15_keyword_url_map.csv (CL-001); 14_education_decision_log D14-05; 18_semantic_gap_register G18-0012"
    r["Notes"] = "Largest unowned head term in the project (135,000/mo 'lab grown diamonds'; DFS intent label NAVIGATIONAL/BRAND for part of the SERP — retailer brands dominate)."
    r["Row ID"] = "COM-LG-HUB"; r["Registry/Calendar ID"] = "COM-LG-HUB"; r["Row Group"] = "CONDITIONAL COMMERCIAL"
    rows.append(finish(r, dict(conflict=1, cannib=1), a=["decision memo"], b=["page build"], c=["n/a until built"]))

    return rows


def pdp_appendix():
    out = []
    pdp = [x for x in crawl.values() if "/shop/" in x["url"] and x["url"] in sitemap_urls and "title" in x]
    tcount = collections.Counter(x["title"] for x in pdp); mcount = collections.Counter(x["meta_description"] for x in pdp)
    for x in sorted(pdp, key=lambda z: z["url"]):
        ld = x.get("ld_json", "")
        cat = re.search(r'"category": "([^"]*)"', ld); price = re.search(r'"price": ([0-9.]+)', ld); cur = re.search(r'"priceCurrency": "([A-Z]+)"', ld)
        mat = re.search(r'"material": \["([^"]*)"', ld)
        hosts = sorted(set(re.findall(r'"image": \[(.*?)\]', ld)[:1] and re.findall(r'https://([^/"]+)/', re.findall(r'"image": \[(.*?)\]', ld)[0]) or []))
        flags = []
        if len(x["title"]) > 60: flags.append("title>60")
        if " · " in x["meta_description"]: flags.append("placeholder-style meta")
        if tcount[x["title"]] > 1: flags.append("duplicate title")
        if mcount[x["meta_description"]] > 1: flags.append("duplicate meta")
        if len(x["meta_description"]) > 160: flags.append("meta>160")
        if len(x["meta_description"]) < 70: flags.append("meta<70")
        if re.search(r"\d{8,}|-copy-", x["url"]): flags.append("numeric-ID/copy slug")
        if mat and "Vermil" in mat.group(1) and "Vermeil" not in mat.group(1): flags.append("truncated material label ('Vermil')")
        out.append({"URL": x["url"], "Status": x["status"], "Title": x["title"], "Title length": len(x["title"]), "Meta description": x["meta_description"], "Meta length": len(x["meta_description"]),
                    "H1": " | ".join(x.get("h1s", [])), "Canonical self-referencing": "Y" if x["canonical"].rstrip("/") == x["url"].rstrip("/") else "N", "Schema types": ", ".join(x.get("schema_types", [])),
                    "Schema category": cat.group(1).strip() if cat else "", "Price (schema)": price.group(1) if price else "", "Currency": cur.group(1) if cur else "", "Material (schema)": mat.group(1) if mat else "",
                    "Image hosts in schema": "; ".join(hosts), "Flags": "; ".join(flags), "In Stage 1 sitemap": "Y" if x["url"] in old_sitemap else "NEW"})
    return out
