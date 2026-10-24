"""Rows for live core pages, commercial categories, subcategories, PDP template, legacy/redirect URLs."""
import re
import lib_research as L
from mm_core import *
import mm_helpers as H

SRC_COMMON = "Live crawl 2026-10-09 (this task, read-only GET, curl); site/01_site_inventory.csv (Stage 1, 2026-09-17); architecture/12_ia_proposed_structure.csv; architecture/16_page_link_requirements.csv"
D19 = "Commercial keyword ownership is a documented DATA GAP (Stage 12 D-19; Stage 15 summary §11-12: commercial hubs own no keyword; the D-19 commercial supplement was never approved/run)."


def kwc(*terms):
    """Format candidate commercial head-term evidence from existing datasets (NOT ratified ownership)."""
    out = []
    for t in terms:
        v = L.kwinfo(t)
        if v:
            out.append(f"{t} ({v['vol']:,}/mo; KD {v['kd']}; DFS intent: {v['intent']})")
        else:
            out.append(f"{t} (not measured in project datasets)")
    return "; ".join(out)


def base_row(path, group, rid, name, ptype, cluster, role):
    r = new_row()
    r["URL"] = (BASE + path) if path.startswith("/") else path
    r["Page Type"] = ptype
    r["Page/Content Name"] = name
    r["SEO Cluster / Topic"] = cluster
    r["Page Role"] = role
    r.update(cur_fields(path) if path.startswith("/") else {})
    gsc_na(r)
    r["Row ID"] = rid
    r["Registry/Calendar ID"] = rid
    r["Row Group"] = group
    return r


def finish(r, flags=None, a=(), b=(), c=()):
    r["_aws"] = [list(a), list(b), list(c)]
    r["AWS Migration Dependency"] = aws_text(a, b, c)
    r["AWS Class (A/B/C)"] = aws_class(a, b, c)
    flags = flags or {}
    for k, col in (("meta", "Flag: Metadata Opp"), ("h1", "Flag: H1 Opp"), ("links", "Flag: Internal-Link Opp"), ("schema", "Flag: Schema Opp"),
                   ("aeo", "Flag: AEO Opp"), ("geo", "Flag: GEO/Entity Opp"), ("conflict", "Flag: Ownership Conflict"),
                   ("cannib", "Flag: Cannibalization Review"), ("blocked", "Flag: AWS-Blocked")):
        r[col] = yn(flags.get(k))
    return r


def link_gap_text(pid, path):
    cr_ = cr(path)
    if not cr_ or "internal_links" not in cr_:
        return ""
    miss, ok = H.missing_required_out(pid, cr_["internal_links"], path)
    parts = []
    if miss:
        parts.append("Stage 16 REQUIRED outgoing links to live pages NOT found on the crawled page: " + ", ".join(H.disp(x) for x in miss))
    if ok:
        parts.append("already present: " + ", ".join(ok))
    return " | ".join(parts)


# ---------------------------------------------------------------- core pages
def core_rows():
    rows = []

    # ------------------------------------------------------------ HOMEPAGE
    r = base_row("/", "CORE LIVE", "NAV-HOME", "Homepage", "HOMEPAGE", "Brand / overall offer", "Navigational (brand) + Hub")
    r["Primary Keyword"] = "NO PRIMARY KEYWORD — BRAND / OVERALL OFFER (owns no Stage 15 keyword; Stage 12 D-18: target brand + overall offer, not category subjects)"
    r["Secondary Keywords"] = "Brand terms only (\"house of diams\"); volume not measured in project datasets — UNKNOWN. Do NOT target 'lab grown diamonds' (135,000; CL-001 head term held for conditional COM-LG-HUB)."
    r["Related/Semantic Concepts"] = "House of Diams; luxury diamond jewellery; Surat workshop; New York office; engagement rings; bespoke; lab-grown diamonds (positioning)"
    r["Search Intent"] = "NAVIGATIONAL (brand) / COMMERCIAL entry"
    r["Keyword Owner"] = "NAV-HOME — brand only (no Stage 15 keyword)"
    r["Existing Keyword Ownership Conflict?"] = "REVIEW — Stage 10 OV-13: current <title> ('Lab-Grown Diamond Engagement Rings & Fine Jewellery') targets the same subject as /engagement-rings and the CL-001 head terms held for COM-LG-HUB. Not an ownership change; a title-level overlap."
    r["Cannibalization Risk"] = "MEDIUM — CANNIBALIZATION REVIEW REQUIRED (homepage title vs /engagement-rings, OV-13)"
    r["Recommended SEO Title"] = "House of Diams | Luxury Diamond Jewellery & Bespoke Rings"
    r["Recommended Meta Description"] = "Luxury diamond jewellery crafted in Surat, India: engagement rings, wedding bands and bespoke designs, with free insured worldwide delivery."
    r["Recommended H1"] = "House of Diams: Luxury Diamond Jewellery, Crafted for Your Story (keep 'The Beginning of Forever' as the hero sub-line)"
    r["Recommended Content/Section Changes"] = ("(1) Add a short factual brand/entity intro (who, where, since when) using only confirmed facts — the FAQ already states a family-run manufacturer in Surat in the trade since 2014 and About lists a New York office. "
        "(2) Remove or date-check the expired-looking 'September sale … HOUSEOFDIAMS2026' promo block (crawl date 2026-10-09). "
        "(3) Verify trust badges against policy pages before keeping them: 'IGI Certified', 'Lifetime Warranty', 'Complimentary Overnight Shipping' (Shipping page contains no timeline detail; certification labs are an open business fact per progress.md). "
        "(4) Add one contextual link to the lab-grown vs natural explainer (Stage 16 recommended).")
    r["Recommended Image/Alt-Text Changes"] = f"Hero and category tiles should carry descriptive alt text (what the piece is). Initial HTML shows {cr('/')['img_count']} <img> tags, {cr('/')['img_no_alt']} without alt text (includes UI icons — VERIFY rendered DOM)."
    r["Recommended Internal Links IN"] = "Global header logo (all pages) — structural only. " + H.link_summary("NAV-HOME", "in")
    r["Recommended Internal Links OUT"] = H.link_summary("NAV-HOME", "out") + " || " + link_gap_text("NAV-HOME", "/")
    r["Recommended Anchor Context"] = "Category links use category names (e.g. 'Engagement Rings', 'Bespoke'); lab-grown explainer link: descriptive anchor per 16_anchor_strategy (EDU-LG-02), never the bare head term 'lab grown diamonds'."
    r["Internal-Link Priority"] = "HIGH (hub for all commercial paths)"
    r["Recommended Schema"] = "Keep Organization (add sameAs for Instagram/Pinterest profiles already linked in the footer; add founder/foundingDate ONLY if confirmed). Optional WebSite. Do NOT add Product, FAQPage or Review markup to the homepage."
    r["Schema Validation/Review Needed?"] = "YES — validate Organization (logo URL is /logo.jpeg; Google logo guidelines), confirm telephone/address consistency (+91 number; Surat + New York addresses) after AWS migration."
    r["AEO Opportunity"] = "LOW for the homepage itself. Brand-fact answers (who is House of Diams, where is it based, is it legitimate) are better served by /about and /faq; ensure the homepage states them in one scannable block."
    r["Primary Questions to Answer"] = "Who is House of Diams? Where are the pieces made? What can I buy / commission here?"
    r["Answer-First Opportunity"] = "Two-sentence brand definition in the first screen of body copy."
    r["PAA/Question Coverage Needed?"] = "NO (brand page)"
    r["GEO/AI Search Opportunity"] = "HIGH-VALUE entity anchor: consistent brand description, location (Surat workshop, New York office), category list and policies across Home, About, FAQ, Organization schema and the existing /llms.txt (200 OK, lists primary pages and ~50 products)."
    r["Important Entities"] = "House of Diams (Organization); Surat, India; New York, US; founders (per /about); engagement rings; bespoke jewellery"
    r["Entity Clarity Needed?"] = "YES — brand facts appear in four places with minor inconsistencies (info@ vs Admin@ email on /returns; +91 phone only; Home title says 'Lab-Grown … Fine Jewellery' while llms.txt says 'luxury diamond jewellery')."
    r["Brand/Expertise/Trust Signal Opportunity"] = "Link to About (founders, milestones) and certification/returns policy from trust badges; avoid unsupported superlatives."
    r["Recommended Action"] = "OPTIMIZE"; r["Priority"] = "HIGH"
    r["Implementation Dependency"] = "CMS/code access for <title>/<meta> and H1 (not determinable from crawl); business confirmation of trust claims; ownership decision on homepage vs COM-ER/COM-LG-HUB title wording."
    r["Status"] = "LIVE — NEEDS OPTIMIZATION"
    r["Evidence / Source"] = SRC_COMMON + "; 12_ia_decision_log.md D-18; Stage 10 OV-13"
    r["Notes"] = "Title currently has no brand name. 'Jewellery' vs 'jewelry' spelling for the US market is an open decision (Stage 12 D-15) — recommended text uses 'diamond jewellery' only where the site already does; revisit after D-15. Crawl originated outside the US (site set detected_country=IN cookie); the footer shows 'United States (USD)' — VERIFY US-visitor view post-AWS."
    rows.append(finish(r, dict(meta=1, h1=1, links=1, schema=1, geo=1, cannib=1, conflict=1),
                       a=["metadata drafts", "intro copy", "link plan", "claim verification list"], b=["Organization/WebSite schema edits (template)"], c=["canonical, indexability, 200 status, US-visitor rendering, CWV baseline"]))

    # ------------------------------------------------------------ /shop
    r = base_row("/shop", "CORE LIVE", "COM-SHOP", "Shop All (all-products listing)", "ALL_PRODUCTS_LISTING", "Shop (commercial)", "Commercial (listing)")
    r["Primary Keyword"] = "NO PRIMARY KEYWORD — ALL-PRODUCTS LISTING (owns no Stage 15 keyword; must not compete with category hubs)"
    r["Secondary Keywords"] = "—"; r["Related/Semantic Concepts"] = "diamond jewellery catalogue; categories: engagement rings, wedding bands, earrings, necklaces, bracelets"
    r["Search Intent"] = "COMMERCIAL / navigational (browse)"; r["Keyword Owner"] = "COM-SHOP — none"
    r["Existing Keyword Ownership Conflict?"] = "NO"; r["Cannibalization Risk"] = "LOW–MEDIUM — near-duplicate of category listings by design (184 pieces vs 61/…); keep non-competing title."
    r["Recommended SEO Title"] = "Shop All Diamond Jewellery | House of Diams"
    r["Recommended Meta Description"] = "Browse every House of Diams piece — engagement rings, wedding bands, earrings, necklaces and bracelets — with free insured worldwide delivery."
    r["Recommended H1"] = "Shop All Diamond Jewellery"
    r["Recommended Content/Section Changes"] = "Current meta mentions 'hip hop jewellery' although /hiphop now 308-redirects here — align copy with the real catalogue. Add 2–3 sentences of orienting copy with links to the category hubs. Paginated URLs (?page=N) self-canonicalise with identical <title>/H1: add page number to the title/H1 or confirm the intended pagination policy."
    r["Recommended Image/Alt-Text Changes"] = "Product-card images: alt = product name + key attribute (e.g. 'Elowen oval halo engagement ring, 10K yellow gold')."
    r["Recommended Internal Links IN"] = H.link_summary("COM-SHOP", "in") + " (header 'Shop All' link already exists)"
    r["Recommended Internal Links OUT"] = H.link_summary("COM-SHOP", "out") + " || " + link_gap_text("COM-SHOP", "/shop")
    r["Recommended Anchor Context"] = "Category names as anchors; PDP links = product names."
    r["Internal-Link Priority"] = "MEDIUM"
    r["Recommended Schema"] = "BreadcrumbList (present). Optional CollectionPage/ItemList (no Google rich-result benefit for products — low value). No FAQPage."
    r["Schema Validation/Review Needed?"] = "LOW — validate BreadcrumbList after migration."
    r["AEO Opportunity"] = "NONE (listing)."; r["Primary Questions to Answer"] = "—"; r["Answer-First Opportunity"] = "—"; r["PAA/Question Coverage Needed?"] = "NO"
    r["GEO/AI Search Opportunity"] = "Catalogue is exposed to AI crawlers via /llms.txt (lists ~50 products) — keep it in sync after AWS URL/image changes."
    r["Important Entities"] = "House of Diams product catalogue; product categories"; r["Entity Clarity Needed?"] = "NO"
    r["Brand/Expertise/Trust Signal Opportunity"] = "Show shipping/returns summary near the listing (verify facts)."
    r["Recommended Action"] = "OPTIMIZE"; r["Priority"] = "MEDIUM"
    r["Implementation Dependency"] = "Template change for pagination titles; IA decision D-07 for indexability of ?page=N"
    r["Status"] = "LIVE — NEEDS OPTIMIZATION"
    r["Evidence / Source"] = SRC_COMMON + "; Stage 12: Shop All INDEXABLE_CONDITIONAL"
    r["Notes"] = "?sort=… and facet parameters are handled correctly (noindex,follow + canonical to /shop) — protect this behaviour in the AWS build."
    rows.append(finish(r, dict(meta=1, h1=1, links=1), a=["metadata/copy drafts", "link plan"], b=["pagination title template"], c=["canonical + noindex on parameters, sitemap inclusion, product count, CWV"]))

    # ------------------------------------------------------------ /collection
    r = base_row("/collection", "CORE LIVE", "COM-COLLECTION", "Collection (filtered browse view)", "FILTER_STATE / EMPTY LISTING", "Shop (commercial)", "Supporting (utility)")
    r["Primary Keyword"] = "NO PRIMARY KEYWORD — filtered view; Stage 12 classes it NON_INDEXABLE (FILTER_STATE)"
    r["Search Intent"] = "n/a"; r["Keyword Owner"] = "none"; r["Existing Keyword Ownership Conflict?"] = "NO"
    r["Cannibalization Risk"] = "LOW (empty) — but an indexable empty page in the sitemap is an index-quality risk (D-13)"
    r["Recommended SEO Title"] = "No change until the indexability decision is made (see actions)"; r["Recommended Meta Description"] = "—"; r["Recommended H1"] = "—"
    r["Recommended Content/Section Changes"] = "Page renders '0 pieces / No pieces match your filters'. Decide: (a) noindex + remove from sitemap until it holds products, or (b) populate with a real curated collection and give it unique copy. Stage 12 recommends non-indexable."
    r["Recommended Internal Links IN"] = "Only where a populated collection exists (currently linked from /llms.txt and the homepage 'Collection' block)."
    r["Recommended Internal Links OUT"] = "—"; r["Internal-Link Priority"] = "LOW"
    r["Recommended Schema"] = "None required."; r["Schema Validation/Review Needed?"] = "NO"
    r["AEO Opportunity"] = "NONE"; r["GEO/AI Search Opportunity"] = "Remove from /llms.txt while empty."
    r["Recommended Action"] = "REVIEW"; r["Priority"] = "HIGH"
    r["Implementation Dependency"] = "Business decision (is a 'Collection' showcase planned?); sitemap/robots template change"
    r["Status"] = "LIVE — EMPTY INDEXABLE PAGE"
    r["Evidence / Source"] = SRC_COMMON + "; 12_ia_decision_log.md D-07, D-13"
    r["Notes"] = "Stage 1 reported the same empty state (2026-09-17) — still empty on 2026-10-09."
    rows.append(finish(r, dict(meta=0, links=0), a=["decision memo"], b=["noindex / sitemap exclusion"], c=["status, indexability, sitemap membership"]))

    # ------------------------------------------------------------ /bespoke
    r = base_row("/bespoke", "CORE LIVE", "COM-BESPOKE", "Bespoke / Custom Jewellery (service page)", "SERVICE_PAGE", "Bespoke / Custom", "Commercial / Transactional (enquiry)")
    r["Primary Keyword"] = ("NO RATIFIED PRIMARY (D-19 gap). Candidate head-term evidence, NOT ownership: " + kwc("custom engagement ring", "design your own engagement ring", "custom jewelry", "bespoke engagement ring") +
                            ". The BC-001 calendar row states these commercial heads 'stay with COM-BESPOKE' — a boundary note, not a Stage 15 mapping.")
    r["Secondary Keywords"] = "custom engagement rings (40,500); custom rings (12,100, KD 70); 'bespoke jewellery' / 'bespoke jewelry' not measured"
    r["Related/Semantic Concepts"] = "CAD design; made-to-order; consultation; stone selection; Surat workshop; certification; timeline"
    r["Search Intent"] = "TRANSACTIONAL / commercial investigation (DataForSEO labels; SERP not validated for these heads)"
    r["Keyword Owner"] = "COM-BESPOKE — no Stage 15 keyword (ownership gap, see Notes)"
    r["Existing Keyword Ownership Conflict?"] = "REVIEW — calendar BC-001 asserts COM-BESPOKE owns 'custom engagement ring' (40,500) and 'design your own engagement ring' (5,400) but Stage 15 maps neither; ratification needed."
    r["Cannibalization Risk"] = "MEDIUM — BC-001 (informational, 'how long does a custom engagement ring take') is a sibling; boundary documented in calendar."
    r["Recommended SEO Title"] = "Bespoke Diamond Jewellery & Custom Engagement Rings | House of Diams"
    r["Recommended Meta Description"] = "Design a one-of-a-kind ring or jewellery piece with House of Diams. Free design consultation and CAD sketch, made in our Surat workshop and delivered insured."
    r["Recommended H1"] = "Bespoke Diamond Jewellery: Design Your Own Piece"
    r["Recommended Content/Section Changes"] = ("(1) CORRECT the lead-time claim: the page says '4-6 week typical lead time' but the confirmed HOD fact is 'typically 2–3 weeks to make + ~6–9 days delivery (~3–4 weeks), stone-dependent, never a guarantee' (BC-001 package notes the user is handling this). "
        "(2) Replace the form-only layout with indexable explanatory copy: process steps, what is included, FAQs (already partly present under 'Bespoke FAQ'). "
        "(3) Verify 'Full IGI / GIA certification included' and '40+ countries' claims. (4) Link to the BC-001 timeline article when it is live (Stage 16 CONDITIONAL).")
    r["Recommended Image/Alt-Text Changes"] = "Add real workshop/CAD/finished-piece photos with descriptive alt text; current page is carousel + form."
    r["Recommended Internal Links IN"] = H.link_summary("COM-BESPOKE", "in")
    r["Recommended Internal Links OUT"] = H.link_summary("COM-BESPOKE", "out") + " || " + link_gap_text("COM-BESPOKE", "/bespoke")
    r["Recommended Anchor Context"] = "From BC-001/BLOG-CRAFT: 'Start your own commission' / 'design your own bespoke piece' (descriptive CTAs)."
    r["Internal-Link Priority"] = "HIGH"
    r["Current Schema"] = r["Current Schema"] + " (no Service/FAQ markup)"
    r["Recommended Schema"] = "Organization + BreadcrumbList. Service markup optional (no Google rich result) — only if it mirrors visible facts. FAQPage NOT recommended (FAQ rich results deprecated May 2026 per VERIFICATION_AUDIT_2026-10-04)."
    r["Schema Validation/Review Needed?"] = "LOW"
    r["AEO Opportunity"] = "MEDIUM — the page already has a 'Bespoke FAQ' (how does the process begin, timeline, cost); answer-first wording would help AI Overviews/answers."
    r["Primary Questions to Answer"] = "How does the bespoke process work? How long does a custom ring take? What does it cost? What certification is included?"
    r["Answer-First Opportunity"] = "Timeline answer in the first paragraph (confirmed fact only, hedged)."
    r["PAA/Question Coverage Needed?"] = "PARTIAL — timeline question routed to BC-001; cost PAA routed to BC-024 (calendar boundaries)."
    r["GEO/AI Search Opportunity"] = "Explain the manufacturing chain (design → CAD → casting → setting, Surat workshop) in plain facts; ensure consistency with BC-001/BC-005."
    r["Important Entities"] = "Bespoke/custom jewellery; CAD; IGI/GIA (to verify); Surat workshop; House of Diams"
    r["Entity Clarity Needed?"] = "YES — certification labs and lead time are inconsistent/unconfirmed."
    r["Brand/Expertise/Trust Signal Opportunity"] = "Founders' trade background (About), workshop photos, sample CAD render, confirmed timeline."
    r["Recommended Action"] = "OPTIMIZE"; r["Priority"] = "CRITICAL"
    r["Implementation Dependency"] = "Business fact confirmation (lead time, certification, countries); copy/CMS edit"
    r["Status"] = "LIVE — FACT CONFLICT"
    r["Evidence / Source"] = SRC_COMMON + "; content-strategy/blog-calendar/revision/confirmed_business_facts.md; blogs/bc-001/README.md; blog_keyword_research.csv (commercial candidates)"
    r["Notes"] = "Priority CRITICAL because a public page contradicts a confirmed business fact that the BC-001 article and holiday-timing posts will state publicly. Copy fix is independent of the AWS migration (A) but should be coordinated with the engineering freeze."
    rows.append(finish(r, dict(meta=1, h1=1, links=1, schema=0, aeo=1, geo=1, conflict=1, cannib=1), a=["correct lead-time copy", "metadata drafts", "FAQ rewrite"], b=["any template change"], c=["status/canonical/indexability, form submission still works"]))

    # ------------------------------------------------------------ /about
    r = base_row("/about", "CORE LIVE", "BRAND-ABOUT", "About House of Diams", "BRAND_PAGE", "Brand & Support", "Supporting (brand / E-E-A-T)")
    r["Primary Keyword"] = "NO PRIMARY KEYWORD — BRAND / SUPPORTING PAGE"; r["Search Intent"] = "NAVIGATIONAL (brand) / trust"; r["Keyword Owner"] = "BRAND-ABOUT — none"
    r["Existing Keyword Ownership Conflict?"] = "NO"; r["Cannibalization Risk"] = "LOW"
    r["Recommended SEO Title"] = "About House of Diams | Family-Run Diamond Jewellery Makers, Surat"
    r["Recommended Meta Description"] = "Meet the founders of House of Diams: a family-run diamond manufacturer in Surat, India, in the trade since 2014, with a New York office and direct-to-client jewellery."
    r["Recommended H1"] = "About House of Diams"
    r["Recommended Content/Section Changes"] = ("Current meta is generic ('our founders, milestones…'). Content is substantive (founders, journey, milestones 2014–2025, values) but: (1) the 'Certified Jewelery' value tile contains a product description (1.00-ct marquise pendant) — likely a CMS placeholder; (2) 'Jewelery' misspelling; (3) co-founder named 'Akshar korat' (lower-case) while blog author fields show 'Krish Babriya, Co-founder' — reconcile names/roles; (4) 'Conflict Free'/'Ethically' claims need substantiation wording. "
        "Add factual 'How we make it' section linking to /bespoke and the Education certification guide.")
    r["Recommended Image/Alt-Text Changes"] = "Founder and workshop photos with descriptive alt text (name, role, place)."
    r["Recommended Internal Links IN"] = H.link_summary("BRAND-ABOUT", "in") + " ; add contextual in-links from BC-001 and Craft posts (calendar)."
    r["Recommended Internal Links OUT"] = H.link_summary("BRAND-ABOUT", "out") + " || " + link_gap_text("BRAND-ABOUT", "/about")
    r["Recommended Anchor Context"] = "'the House of Diams story' / 'our workshop in Surat' (BC-001 package)."
    r["Internal-Link Priority"] = "MEDIUM"
    r["Recommended Schema"] = "AboutPage (optional) + Organization with founder (Person) and foundingDate ONLY after the founder names/dates are confirmed; BreadcrumbList."
    r["Schema Validation/Review Needed?"] = "YES — after entity facts confirmed."
    r["AEO Opportunity"] = "MEDIUM — 'Who owns House of Diams / is it legitimate' answers."; r["Primary Questions to Answer"] = "Who founded House of Diams? Where are the pieces made? Since when?"
    r["Answer-First Opportunity"] = "One-paragraph company summary at top."; r["PAA/Question Coverage Needed?"] = "NO"
    r["GEO/AI Search Opportunity"] = "PRIMARY entity source for AI answers about the brand: make founders, locations, dates unambiguous and consistent with Organization schema and llms.txt."
    r["Important Entities"] = "House of Diams; Akshar Korat (co-founder, as published); Surat; New York; milestones 2014–2025"
    r["Entity Clarity Needed?"] = "YES — founder naming/roles inconsistent across About and blog bylines."
    r["Brand/Expertise/Trust Signal Opportunity"] = "HIGH — first-hand trade experience is HOD's strongest E-E-A-T asset."
    r["Recommended Action"] = "OPTIMIZE"; r["Priority"] = "MEDIUM"
    r["Implementation Dependency"] = "Business confirmation of founder names/roles/dates; CMS/copy edit"
    r["Status"] = "LIVE — NEEDS OPTIMIZATION"; r["Evidence / Source"] = SRC_COMMON
    r["Notes"] = "Stage 1 (2026-09-17) found NO H1 on /about; the live page now has an H1 — the site has been changing during this project."
    rows.append(finish(r, dict(meta=1, links=1, schema=1, aeo=1, geo=1), a=["copy + metadata drafts", "fact confirmation"], b=["schema template"], c=["canonical, status"]))

    # ------------------------------------------------------------ /contact (redirect)
    r = base_row("/contact", "CORE LIVE", "BRAND-CONTACT", "Contact (now a modal; URL redirects)", "BRAND_PAGE (planned) → modal", "Brand & Support", "Supporting")
    r["Primary Keyword"] = "NO PRIMARY KEYWORD — SUPPORTING PAGE"; r["Search Intent"] = "NAVIGATIONAL"; r["Keyword Owner"] = "BRAND-CONTACT — none"
    r["Existing Keyword Ownership Conflict?"] = "REVIEW — Stage 12 IA proposes /contact as an L1 INDEXABLE_PERMANENT page and Stage 1 listed it in the sitemap; the live site now 307-redirects it to /?contact=open and has dropped it from the sitemap."
    r["Cannibalization Risk"] = "LOW"
    r["Recommended SEO Title"] = "Contact House of Diams | Enquiries, Bespoke & Support"
    r["Recommended Meta Description"] = "Contact House of Diams for product enquiries, bespoke orders and support. Email, phone/WhatsApp or visit our New York office; replies within 24 hours."
    r["Recommended H1"] = "Contact House of Diams"
    r["Recommended Content/Section Changes"] = "Decide whether a crawlable /contact page exists (recommended by Stage 12 for NAP/trust and because FAQ copy tells users to use 'houseofdiams.com/contact'). If the modal pattern stays, keep the 307 intentionally but update FAQ/Returns copy and Organization schema to the real contact path; a temporary (307) redirect is not a signal to consolidate."
    r["Recommended Internal Links IN"] = H.link_summary("BRAND-CONTACT", "in"); r["Recommended Internal Links OUT"] = "—"
    r["Recommended Anchor Context"] = "'contact us' / 'book a bespoke consultation'"; r["Internal-Link Priority"] = "MEDIUM"
    r["Recommended Schema"] = "ContactPage (optional) + Organization ContactPoint (already present in sitewide Organization JSON-LD)."
    r["Schema Validation/Review Needed?"] = "LOW"
    r["AEO Opportunity"] = "NONE"; r["GEO/AI Search Opportunity"] = "NAP consistency: info@ vs Admin@ emails, +91 phone, NY address."
    r["Important Entities"] = "House of Diams; contact channels"; r["Entity Clarity Needed?"] = "YES (email/phone variants)"
    r["Recommended Action"] = "REVIEW"; r["Priority"] = "MEDIUM"
    r["Implementation Dependency"] = "Product/UX decision; redirect behaviour must be preserved or deliberately changed in the AWS build"
    r["Status"] = "LIVE — REDIRECT (307)"; r["Evidence / Source"] = SRC_COMMON + "; live sitemap diff (contact removed)"
    r["Notes"] = "307 = temporary redirect. Header/footer 'Contact Us' links point to /contact."
    rows.append(finish(r, dict(links=1, conflict=1), a=["decision memo"], b=["contact page build/keep decision"], c=["redirect type and target, sitemap"]))

    # ------------------------------------------------------------ /faq
    r = base_row("/faq", "CORE LIVE", "SUP-FAQ", "FAQ / Help", "FAQ_HELP", "Brand & Support", "Supporting (service/policy answers)")
    r["Primary Keyword"] = "NO PRIMARY KEYWORD — SUPPORTING PAGE (Stage 12 D-18: service/policy answers; one-line topic answers link to the Education owner)"
    r["Search Intent"] = "NAVIGATIONAL / support"; r["Keyword Owner"] = "SUP-FAQ — none"
    r["Existing Keyword Ownership Conflict?"] = "REVIEW — FAQ answers lab-grown vs natural, CVD vs HPHT, 4Cs questions that Stage 14/15 assign to Education owners (EDU-LG-02, EDU-LG-03, EDU-4C-00). Stage 10 flagged POSSIBLE_OVERLAP."
    r["Cannibalization Risk"] = "MEDIUM — topic questions on FAQ duplicate Education-owned intents; keep to one-line answers + link."
    r["Recommended SEO Title"] = "FAQ | Orders, Shipping, Returns & Lab-Grown Diamonds | House of Diams"
    r["Recommended Meta Description"] = "Answers to common questions about House of Diams orders, shipping, returns, certification and lab-grown diamonds."
    r["Recommended H1"] = "Frequently Asked Questions"
    r["Recommended Content/Section Changes"] = "Trim topic answers (lab-grown vs natural, CVD/HPHT, 4Cs) to one line each with a link to the Education owner (Stage 16 REQUIRED outgoing links: EDU-LG-01, EDU-LG-02, EDU-CERT-00, EDU-RJG-02, SUP-POLICIES, BRAND-CONTACT). Fix reference to 'houseofdiams.com/contact' (now a modal redirect)."
    r["Recommended Internal Links IN"] = H.link_summary("SUP-FAQ", "in"); r["Recommended Internal Links OUT"] = H.link_summary("SUP-FAQ", "out") + " || " + link_gap_text("SUP-FAQ", "/faq")
    r["Recommended Anchor Context"] = "Descriptive anchors to Education owners (e.g. 'lab-grown vs natural diamonds compared')."
    r["Internal-Link Priority"] = "MEDIUM"
    r["Recommended Schema"] = "BreadcrumbList only. FAQPage markup is present today but FAQ rich results were deprecated (2026-05-08); keeping valid, visible-content-matching FAQPage is harmless but gives no search feature — do not invest in it."
    r["Schema Validation/Review Needed?"] = "YES — confirm FAQPage Q&A text exactly mirrors visible text; decide keep/remove."
    r["AEO Opportunity"] = "MEDIUM — concise policy/brand answers are the right job for this page."; r["Primary Questions to Answer"] = "Is House of Diams legitimate? Do you ship internationally? What if I don't like it? How long does delivery take?"
    r["Answer-First Opportunity"] = "Already question→answer; ensure first sentence answers directly."; r["PAA/Question Coverage Needed?"] = "NO (policy FAQs)"
    r["GEO/AI Search Opportunity"] = "Strong source for brand/legitimacy answers — keep facts consistent with About/Organization schema."
    r["Important Entities"] = "House of Diams; IGI/GIA; CVD; HPHT; lab-grown diamond"; r["Entity Clarity Needed?"] = "YES (certification labs)"
    r["Recommended Action"] = "OPTIMIZE"; r["Priority"] = "MEDIUM"
    r["Implementation Dependency"] = "Education owners must exist/live for link targets; business confirmation of policy facts"
    r["Status"] = "LIVE — NEEDS OPTIMIZATION"; r["Evidence / Source"] = SRC_COMMON + "; 12_ia_decision_log.md D-18; 14_education_decision_log D14-30"
    r["Notes"] = "Stage 1 found NO H1 on /faq; live page now has H1 'How May We Help You?' (not descriptive — acceptable for a support page but 'Frequently Asked Questions' is clearer)."
    rows.append(finish(r, dict(meta=1, h1=1, links=1, schema=1, conflict=1, cannib=1), a=["copy edits", "link plan"], b=["schema decision (template)"], c=["canonical, status"]))

    # ------------------------------------------------------------ /shipping
    r = base_row("/shipping", "CORE LIVE", "SUP-POLICIES-SHIP", "Shipping policy", "POLICY_PAGE", "Brand & Support", "Supporting (policy)")
    r["Primary Keyword"] = "NO PRIMARY KEYWORD — POLICY PAGE"; r["Search Intent"] = "NAVIGATIONAL / trust"; r["Keyword Owner"] = "SUP-POLICIES — none"
    r["Existing Keyword Ownership Conflict?"] = "NO"; r["Cannibalization Risk"] = "LOW"
    r["Recommended SEO Title"] = "Shipping & Delivery | House of Diams"
    r["Recommended Meta Description"] = "House of Diams shipping and delivery information: insured worldwide shipping, processing times for made-to-order pieces and order tracking."
    r["Recommended H1"] = "Shipping & Delivery"
    r["Recommended Content/Section Changes"] = ("DEFECT: visible placeholder text 'new test black / test desc' on the live page. The visible body has no concrete timelines even though header badges promise 'Free Worldwide Insured Shipping' and the homepage badge says 'Complimentary Overnight Shipping' — shipping cut-offs are a still-open business fact (progress.md). "
        "Add: regions served, processing vs transit times, insured/signature terms, duties/taxes for US, bespoke lead time (confirmed fact, hedged).")
    r["Recommended Internal Links IN"] = H.link_summary("SUP-POLICIES", "in") + " ; also from PDPs and BC-004 holiday posts"; r["Recommended Internal Links OUT"] = "FAQ, Returns, Contact, Bespoke"
    r["Recommended Anchor Context"] = "'shipping and delivery details'"; r["Internal-Link Priority"] = "MEDIUM"
    r["Recommended Schema"] = "WebPage/BreadcrumbList. Consider OfferShippingDetails inside Product/Offer (or Organization-level shipping policy) only once the policy facts are final — must match visible text."
    r["Schema Validation/Review Needed?"] = "YES (when policy facts final)"
    r["AEO Opportunity"] = "MEDIUM — 'how long does delivery take' is a high-intent support question."; r["Primary Questions to Answer"] = "How long does delivery take? Is shipping insured/free? Do you ship to the US? Are duties included?"
    r["Answer-First Opportunity"] = "Delivery timeline table."; r["PAA/Question Coverage Needed?"] = "NO"
    r["GEO/AI Search Opportunity"] = "Accurate policy text is what AI assistants quote about delivery — vagueness here risks wrong answers."
    r["Important Entities"] = "House of Diams; insured shipping; made-to-order"; r["Entity Clarity Needed?"] = "YES"
    r["Recommended Action"] = "OPTIMIZE"; r["Priority"] = "HIGH"
    r["Implementation Dependency"] = "Business facts (shipping cut-offs, timelines, countries)"; r["Status"] = "LIVE — PLACEHOLDER TEXT VISIBLE"
    r["Evidence / Source"] = SRC_COMMON + "; progress.md (open business facts)"; r["Notes"] = "Placeholder removal is a content fix independent of AWS (A)."
    rows.append(finish(r, dict(meta=1, links=1, schema=1), a=["copy/facts, placeholder removal"], b=["schema template"], c=["status, canonical"]))

    # ------------------------------------------------------------ /returns
    r = base_row("/returns", "CORE LIVE", "SUP-POLICIES-RET", "Returns & Exchanges policy", "POLICY_PAGE", "Brand & Support", "Supporting (policy)")
    r["Primary Keyword"] = "NO PRIMARY KEYWORD — POLICY PAGE"; r["Search Intent"] = "NAVIGATIONAL / trust"; r["Keyword Owner"] = "SUP-POLICIES — none"
    r["Existing Keyword Ownership Conflict?"] = "NO"; r["Cannibalization Risk"] = "LOW"
    r["Recommended SEO Title"] = "Returns & Exchanges (15-Day Returns) | House of Diams"
    r["Recommended Meta Description"] = "House of Diams returns and exchanges: how our 15-day returns work, what is eligible and how to start a return or track an order."
    r["Recommended H1"] = "Returns & Exchanges"
    r["Recommended Content/Section Changes"] = "The visible body shows the 'Is House of Diams legitimate?' FAQ answer, a Quick Actions block and contact details but NO actual return terms (window, condition, bespoke exclusions, refund method) — the header badge says '15-Day Returns'. Contact email on this page is Admin@houseofdiams.com while the rest of the site uses info@. Needs a complete policy (business facts) and one canonical contact email."
    r["Recommended Internal Links IN"] = H.link_summary("SUP-POLICIES", "in") + " ; PDPs"; r["Recommended Internal Links OUT"] = "FAQ, Shipping, Contact"
    r["Recommended Anchor Context"] = "'returns and exchanges policy'"; r["Internal-Link Priority"] = "MEDIUM"
    r["Recommended Schema"] = "Replace page-level FAQPage with WebPage/BreadcrumbList; consider MerchantReturnPolicy (Organization or Offer level) once terms are final and visible."
    r["Schema Validation/Review Needed?"] = "YES"
    r["AEO Opportunity"] = "MEDIUM"; r["Primary Questions to Answer"] = "What is the return window? Can bespoke pieces be returned? How do I start a return?"
    r["Answer-First Opportunity"] = "Return window in the first sentence."; r["PAA/Question Coverage Needed?"] = "NO"
    r["GEO/AI Search Opportunity"] = "Clear return terms are a Merchant/AI-shopping trust signal."
    r["Important Entities"] = "House of Diams; returns; exchanges"; r["Entity Clarity Needed?"] = "YES"
    r["Recommended Action"] = "OPTIMIZE"; r["Priority"] = "HIGH"; r["Implementation Dependency"] = "Business facts (return terms)"
    r["Status"] = "LIVE — THIN POLICY CONTENT"; r["Evidence / Source"] = SRC_COMMON
    r["Notes"] = "FAQPage schema on this page is attached to a non-FAQ body."
    rows.append(finish(r, dict(meta=1, links=1, schema=1), a=["copy/facts"], b=["schema template"], c=["status, canonical"]))

    # ------------------------------------------------------------ privacy/terms
    for path, nm, rid in (("/privacy-policy", "Privacy Policy", "SUP-POLICIES-PRIV"), ("/terms", "Terms & Conditions", "SUP-POLICIES-TERMS")):
        r = base_row(path, "CORE LIVE", rid, nm, "POLICY_PAGE", "Brand & Support", "Supporting (legal)")
        r["Primary Keyword"] = "NO PRIMARY KEYWORD — LEGAL / SUPPORTING PAGE"; r["Search Intent"] = "n/a"; r["Keyword Owner"] = "SUP-POLICIES — none"
        r["Existing Keyword Ownership Conflict?"] = "NO"; r["Cannibalization Risk"] = "NONE"
        r["Recommended SEO Title"] = f"{nm} | House of Diams"; r["Recommended Meta Description"] = f"{nm} for House of Diams."
        r["Recommended H1"] = nm; r["Recommended Content/Section Changes"] = "No SEO changes needed. Legal review is outside SEO scope. (Legal owner to confirm completeness.)"
        r["Recommended Internal Links IN"] = "Footer (global)"; r["Recommended Internal Links OUT"] = "—"; r["Internal-Link Priority"] = "LOW"
        r["Recommended Schema"] = "None required."; r["Schema Validation/Review Needed?"] = "NO"
        r["AEO Opportunity"] = "NONE"; r["GEO/AI Search Opportunity"] = "NONE"; r["Recommended Action"] = "NO ACTION"; r["Priority"] = "LOW"
        r["Implementation Dependency"] = "—"; r["Status"] = "LIVE — OK"; r["Evidence / Source"] = SRC_COMMON; r["Notes"] = "Indexable utility page; acceptable. Optional: noindex is NOT required."
        rows.append(finish(r, {}, a=["none"], c=["status, canonical after migration"]))

    return rows
