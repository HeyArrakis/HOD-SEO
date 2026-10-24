# -*- coding: utf-8 -*-
"""Authored Step 2 specs (FINAL after Step 2A resolution, 2026-10-10): core live pages, hubs, commercial categories, PDP, legacy URLs.
All titles are PRE-SUFFIX values: the live template appends ' | House of Diams' (verified 2026-10-09: <title> = og:title + ' | House of Diams';
the homepage uses an absolute title with no suffix). American English throughout; slugs never change."""

BF_NOTE = ("Do not repeat 'free insured worldwide delivery', '15-day returns', 'IGI/GIA certified', "
           "'lifetime warranty' or 'overnight shipping' in titles, metas or schema until HOD confirms them (F-A1/F-A2/F-A3/F-B1).")

SCH_CAT = ("BreadcrumbList (keep as-is). Retire the boilerplate FAQPage (same Q&A repeated on 35 pages; FAQ rich results "
           "discontinued 2026-05) or replace it with visible, category-specific Q&A WITHOUT FAQPage markup. "
           "CollectionPage/ItemList optional (no Google feature; low value).")
IMG_CAT = ("Product-card alt = product name + one key attribute; hero/banner alt describes what the image shows; decorative "
           "icons alt=\"\". Audit the RENDERED DOM first (initial-HTML counts include UI icons and lazy images). No file renames; "
           "image hosts unchanged until AWS (Class B).")
SCH_ART = ("BlogPosting (or Article) + BreadcrumbList (currently missing on articles); author = Organization 'House of Diams' unless a named "
           "person is verified (OD-11); ISO 8601 datePublished/dateModified; image URL valid after AWS. No FAQPage/HowTo; "
           "QAPage invalid for site-authored Q&A.")

CORE = {}


def D(hod="", eng="", gsc="", block=False):
    """Remaining-dependency descriptor."""
    return dict(hod=hod, eng=eng, gsc=gsc, gscblock=block)


CORE["NAV-HOME"] = dict(
    name="Homepage",
    title="House of Diams | Luxury Diamond Jewelry & Bespoke Rings", tact="REPLACE — FINAL (brand-led; origin-neutral per OD-02)",
    meta="Explore House of Diams: diamond engagement rings, wedding bands, earrings, necklaces and bracelets, plus bespoke designs made to order.",
    mact="REPLACE — FINAL",
    h1="THE BEGINNING OF FOREVER", hact="KEEP — acceptable brand-hero H1; not changed for its own sake. Topical signal comes from the title and the visible intro.",
    cact="EXPAND (entity intro) + CLEAN UP (expired promo, unverified badges)",
    sect=("1) Add a 2–3 sentence visible brand statement under the hero: House of Diams makes diamond engagement rings, wedding bands, fine jewelry and bespoke pieces. Do NOT add founding year, 'family-run', locations or manufacturing statements until HOD confirms them (F-C1). "
          "2) 'Shop By Category' tiles → crawlable links with plain US category names (Engagement Rings, Wedding Bands, Fine Jewelry, Bespoke). "
          "3) One link to the Education index and one to the lab-grown vs natural comparison (Stage 16 OPTIONAL) — the homepage must not host the comparison (D-18). "
          "4) Remove the 'September sale … HOUSEOFDIAMS2026' block (expired-looking) unless merchandising confirms it is live. "
          "5) Remove the trust badges 'IGI Certified', 'Lifetime Warranty' and 'Complimentary Overnight Shipping' (UNCONFIRMED) or replace with neutral links to /shipping and /returns; restore specific claims only after F-A1/F-A3/F-B1."),
    sch="Organization (present): add @id, one consistent email/telephone (F-C2), sameAs only for profiles HOD confirms (Instagram is linked on-page), logo per Google spec. Optional WebSite (name only — no sitelinks searchbox). No Product/FAQ.",
    sact="UPDATE (Class B)", aeo="LOW (navigational). Entity questions are asked of AI answers ('What is House of Diams?', 'Where is House of Diams based?') — answer once, consistently, on /about; echo only verified facts in the homepage intro.",
    qs="What is House of Diams? | Where is House of Diams based? | Is House of Diams legitimate?",
    geo="One brand description repeated identically on Home, About, FAQ, Organization schema and /llms.txt — verified facts only.",
    trust="Replace unverifiable badges with neutral policy links; one contact set everywhere (info@ vs Admin@ on /returns today).",
    img=IMG_CAT.replace("Product-card alt", "Category-tile and product-card alt"), prio="HIGH", aws="B",
    dep="Metadata/copy via CMS or code (E-02); promo removal needs merchandising confirmation.", dec="OD-02; OD-05; OD-08",
    status="READY FOR IMPLEMENTATION POST-AWS", deps=D(hod="F-A1, F-A3, F-B1, F-C1 (optional enhancements — page ships without them)", eng="E-01, E-02"),
    notes="Overlap with /engagement-rings (OV-13) is removed by a brand-led title. If HOD later confirms F-E1 (all stones lab-grown) a variant 'House of Diams | Lab-Grown Diamond Jewelry & Bespoke Rings' is available; not recommended before then. Homepage <title> is absolute (no template suffix).")

CORE["COM-SHOP"] = dict(
    name="Shop (all products)",
    title="Shop All Diamond Jewelry", tact="REPLACE — FINAL",
    meta="Browse the full House of Diams collection: diamond engagement rings, wedding bands, earrings, necklaces and bracelets.", mact="REPLACE — FINAL",
    h1="Shop All Diamond Jewelry", hact="REPLACE (low value; 'Explore Our Collection' is generic)",
    cact="MINOR EXPAND + PAGINATION RULE",
    sect=("1) 2–3 orienting sentences with links to the category hubs. 2) Current meta mentions ⟦'hip hop jewellery'⟧ (verbatim current-site text) although /hiphop 308-redirects here — use the US-spelled, catalog-accurate meta above. "
          "3) Paginated URLs (?page=N): self-referencing canonical and 'Page N' in title/H1 for N>1 (E-06). "
          "4) Ensure the ranking PDP /shop/oval-floral-diamond-ring is reachable in one click from a category hub (Stage 16 REQUIRED)."),
    sch="BreadcrumbList (present). No further schema.", sact="NO CHANGE",
    aeo="NONE (listing).", qs="—", geo="Low; keep catalog attributes consistent with PDP schema.", trust="Link to /shipping and /returns once policies are final.",
    img=IMG_CAT, prio="MEDIUM", aws="B", dep="Pagination template (E-06).", dec="OD-05",
    status="READY FOR IMPLEMENTATION POST-AWS", deps=D(eng="E-01, E-02, E-06"), notes="No ownership issue. Utility listing — do not over-invest.")

CORE["COM-COLLECTION"] = dict(
    name="Collection (empty filtered view)",
    title="— (no metadata work: empty page)", tact="HOLD — noindex until populated (OD-07 adopted)",
    meta="— (none)", mact="HOLD", h1="— (none)", hact="HOLD",
    cact="NOINDEX + REMOVE FROM SITEMAP/NAV/llms.txt",
    sect=("Page holds 0 products ('Explore Collection'). Stage 12 D-13/P-EMPTY: no empty page may be indexable. FINAL: noindex,follow; remove from sitemap, nav and /llms.txt; no redirect (no equity; a redirect would hide a template defect). "
          "If engineering confirms /collection is a retired route, a 301 → /shop is acceptable."),
    sch="None.", sact="NO CHANGE", aeo="NONE.", qs="—", geo="Remove from /llms.txt (lists /collection).", trust="—", img="None — page should not be indexable.",
    prio="HIGH", aws="B", dep="Sitemap/robots/template rule (E-05); verify after AWS (Class C).", dec="OD-07",
    status="READY FOR IMPLEMENTATION POST-AWS", deps=D(eng="E-01, E-05"), notes="Index-integrity item; one site-level rule covers all empty pages (see 10-DECISIONS-RESOLUTION-LOG.md §OD-07).")

CORE["COM-BESPOKE"] = dict(
    name="Bespoke / custom jewelry",
    title="Custom Engagement Rings & Bespoke Jewelry", tact="REPLACE — FINAL (assigned: 'custom engagement ring')",
    meta="Design a custom engagement ring or bespoke diamond jewelry with House of Diams. Share your idea, stone and metal preferences to start a conversation.",
    mact="REPLACE — FINAL",
    h1="Custom Engagement Rings and Bespoke Diamond Jewelry", hact="REPLACE — FINAL. Current 'Explore Bespoke Collection' describes a collection; the page is an enquiry/service page.",
    cact="REWRITE (trust-critical) + EXPAND",
    sect=("1) CORRECT the lead time. Live: '4-6 week typical lead time'. CONFIRMED (HOD): bespoke pieces typically take 2–3 weeks to make, followed by approximately 6–9 days for delivery — generally about 3–4 weeks from design approval to delivery, depending on the stone selected; not guaranteed. "
          "Suggested wording: 'Bespoke pieces typically take 2–3 weeks to make, followed by approximately 6–9 days for delivery — generally about 3–4 weeks from design approval to delivery, depending on the stone selected. This is an estimate, not a guaranteed delivery date.' (always 'typically / approximately'; no holiday cut-off). "
          "2) Replace the form-only layout with indexable explanatory copy: how a commission works (only steps HOD confirms — F-D1), what to prepare (idea, stone, metal, budget — taken from the page's own FAQ), what happens after submitting. "
          "3) REMOVE (or neutral wording) until confirmed: 'Full IGI / GIA certification included', 'Fully insured worldwide delivery — complimentary to 40+ countries', 'Free design consultation — CAD sketch included', 'reply within 24 hours', 'cut, set, and finished in the diamond capital of the world'. "
          "4) Make the FAQ answers visible in initial HTML (the 'How long does a bespoke piece take?' answer is collapsed) and use the confirmed timeline; add 'Can I design my own engagement ring?'. State no prices (route cost questions to BC-024). "
          "5) Boundary: BC-001 owns the long timeline explanation — /bespoke carries a 1–2 line answer + link. Remove empty 'Hip Hop' from the piece-type list/'More to Explore' (F-E3)."),
    sch="BreadcrumbList (add). Service/ProfessionalService optional — no Google feature, low value. Keep Organization.", sact="ADD (Class B)",
    aeo="HIGH-VALUE: 'How long does a custom engagement ring take?' (1–2 sentence answer with the confirmed range + link to BC-001); 'How does the bespoke process work?'; 'Can I design my own engagement ring?'.",
    qs="How long does a custom engagement ring take? | How does the bespoke process work? | Can I design my own engagement ring? | What should I send to start a bespoke piece?",
    geo="Explain the make chain in plain facts HOD confirms; identical wording with BC-001/BC-005. No certification/insurance/country claims until confirmed.",
    trust="Lead time now matches the confirmed fact; remaining claims removed until F-D1/F-B1 answered. Show a real contact route.",
    img="Use real HOD photography/CAD examples only (image-requirements in the BC-001 package); descriptive alt per image; no stock images implying HOD work.",
    prio="CRITICAL", aws="B", dep="Copy via CMS/code (E-02); user stated they are handling the /bespoke copy.", dec="OD-01; OD-05; OD-08",
    status="READY FOR IMPLEMENTATION POST-AWS", deps=D(hod="F-D1, F-B1 (enhance process copy; removal of unverified claims does not wait)", eng="E-01, E-02"),
    notes="Lead-time fix is CONFIRMED; the start point 'from design approval' was stated by the user on 2026-10-10 (confirmed_business_facts.md says 'production and delivery', not the start point — see 10-DECISIONS-RESOLUTION-LOG.md §OD-08).")

CORE["BRAND-ABOUT"] = dict(
    name="About",
    title="Our Story & Values", tact="REPLACE — NEUTRAL INTERIM ('About House of Diams' would repeat the brand with the suffix; 'Founders' wording only after HOD confirms names/roles — F-C1)",
    meta="Learn about House of Diams, its story, values, and approach to diamond jewelry.", mact="REPLACE — NEUTRAL INTERIM (no founder/milestone claim until F-C1)",
    h1="About House of Diams", hact="KEEP — clear, matches intent.",
    cact="CORRECT + CLARIFY (trust-critical)",
    sect=("1) Fix the 'Certified Jewelery' value tile (it contains a product description — CMS placeholder) and the 'Jewelery' misspelling (US 'Jewelry'). "
          "2) Founder names/roles: page shows 'Akshar korat co founder' (lower-case) while blog bylines show 'Krish Babriya, Co-founder' — keep only what HOD confirms (F-C1); until then use neutral wording and no Person schema. "
          "3) 'Journey' blurb says 'a love story … over half a century' while Milestones start in 2014 — remove or correct (F-C1). "
          "4) Value claims 'Conflict Free', 'Ethically Certified' — remove unless HOD defines and evidences them. "
          "5) Add a short entity-facts block (what HOD makes; locations/dates only as confirmed) matching Organization schema. 6) Link to Bespoke, the certification explainer and Contact."),
    sch="AboutPage + Organization (@id) + BreadcrumbList. Add Person (founder) ONLY with confirmed names/roles; foundingDate only if confirmed.", sact="ADD/UPDATE (Class B)",
    aeo="MEDIUM — answer-first facts block: who founded House of Diams, where pieces are made, since when (confirmed facts only).",
    qs="Who founded House of Diams? | Where is House of Diams based? | Where are House of Diams pieces made? | Since when has House of Diams been in the trade?",
    geo="PRIMARY entity source for AI answers about the brand — must agree with Organization schema, /faq, /returns and /llms.txt.",
    trust="Founder names/roles, locations, dates: single source of truth from HOD.",
    img="Founder/workshop photos: real, descriptive alt (who/where); decorative icons alt=\"\".", prio="HIGH", aws="B",
    dep="Founder/company facts (F-C1) — the page's purpose is these facts.", dec="OD-05; OD-08; OD-11",
    status="HOD INPUT REQUIRED", deps=D(hod="F-C1", eng="E-01, E-02"),
    notes="Placeholder/typo fixes and removal of unverifiable claims can be applied without waiting; the entity block needs F-C1.")

CORE["BRAND-CONTACT"] = dict(
    name="Contact (currently a modal)",
    title="Contact Us", tact="CREATE — FINAL (OD-09 adopted: real /contact page)",
    meta="Contact House of Diams about an order, a product, a bespoke piece, wholesale or press.", mact="CREATE — FINAL (adjust topics to F-C2 answer)",
    h1="Contact House of Diams", hact="CREATE — FINAL",
    cact="BUILD A CRAWLABLE /contact PAGE",
    sect=("Live: /contact → 307 → /?contact=open (modal); not in the sitemap; the FAQ already points to 'houseofdiams.com/contact'. FINAL: ship a real page — 200, indexable, self-canonical, in the sitemap, linked from header/footer; /?contact=open canonicalises to /contact. "
          "Required content: contact methods HOD designates public (F-C2: one email, phone/WhatsApp, address), an enquiry form with fields Full name*, Email*, Phone/WhatsApp, Country*, Enquiry topic*, Message* (10–5,000 characters — mirroring the existing bespoke form), the enquiry topics HOD actually offers (the modal lists Product, Bespoke, B2B Wholesale, Press/Media, General), and a reply-time statement only if confirmed. "
          "Do not invent addresses, hours or response times."),
    sch="ContactPage + Organization (single consistent email/phone/address) + BreadcrumbList.", sact="ADD (Class B)",
    aeo="LOW.", qs="How do I contact House of Diams? | What is House of Diams' email, phone and address?",
    geo="NAP consistency: info@ (site-wide) vs Admin@ (/returns); +91 phone only; New York address 36 W 44th St, Suite 1000B — HOD designates the public set.",
    trust="Publish a reply-time claim only if confirmed.", img="None needed.", prio="MEDIUM", aws="B",
    dep="Public contact details (F-C2); page build (E-12).", dec="OD-09; OD-08",
    status="HOD INPUT REQUIRED", deps=D(hod="F-C2", eng="E-01, E-12"), notes="Until the page exists the 307-to-modal behavior stays; header/footer link target changes with the page.")

CORE["SUP-FAQ"] = dict(
    name="FAQ",
    title="FAQs: Orders, Shipping, Returns & Diamonds", tact="REPLACE — FINAL",
    meta="Answers to common questions about House of Diams orders, shipping, returns, diamonds and bespoke jewelry.", mact="REPLACE — FINAL",
    h1="Frequently Asked Questions", hact="REPLACE (low priority; 'How May We Help You?' is not descriptive)",
    cact="RESTRUCTURE (one-line answer + link)",
    sect=("1) Group questions under plain headings (Orders & shipping / Returns / Diamonds / Bespoke / Care). "
          "2) Topic answers (lab-grown vs natural, CVD vs HPHT, 4Cs, certification, ring size) become ONE line each with a link to the Education owner: EDU-LG-02, EDU-LG-03, EDU-4C-00, EDU-CERT-00, EDU-RJG-02 (OD-10 adopted; Stage 14 D14-30). "
          "3) Policy answers use neutral wording that links to /shipping and /returns until F-A1/F-A2 are answered; no specific timelines or windows. 4) Fix the 'houseofdiams.com/contact' reference to the real /contact page."),
    sch="WebPage + BreadcrumbList. FAQPage markup on /faq itself is harmless (no rich result since 2026-05) — do not extend it to other pages; retire it elsewhere.", sact="UPDATE (Class B)",
    aeo="MEDIUM — FAQ answers on policy are quoted by AI answers; they must be accurate. Topic depth stays on Education pages (no duplicate long answers).",
    qs="Is House of Diams legitimate? | How long does a bespoke order take? | What is your returns process? | Are your diamonds certified? | How do I find my ring size?",
    geo="Mirror the brand-facts block from /about; avoid contradicting policy pages.", trust="No shipping/returns/certification specifics until F-A1/F-A2/F-B1.",
    img="None.", prio="MEDIUM", aws="B", dep="Education owners are live (they are).", dec="OD-05; OD-10; OD-08",
    status="READY FOR IMPLEMENTATION POST-AWS", deps=D(hod="F-A1, F-A2, F-B1 (policy answers upgrade once confirmed)", eng="E-01, E-02"),
    notes="Cannibalization risk MEDIUM resolved by the one-line + link rule.")

CORE["SUP-POLICIES-SHIP"] = dict(
    name="Shipping policy",
    title="Shipping & Delivery", tact="REPLACE — FINAL",
    meta="Shipping and delivery information from House of Diams: order processing and made-to-order lead times.", mact="REPLACE — FINAL (after the page itself is fixed; no order-tracking promise until F-A1 confirms it)",
    h1="Shipping", hact="KEEP — acceptable.",
    cact="REWRITE (trust-critical) — remove placeholder, add policy",
    sect=("CURRENT PROBLEM: visible placeholder text 'new test black / test desc'; no concrete timelines although the header says 'Complimentary Insured Shipping', the homepage badge says 'Complimentary Overnight Shipping' and PDPs say 'Worldwide insured shipping is complimentary. In-stock pieces usually ship within 2-3 business days'. "
          "CONFIRMED FACT: bespoke timeline only (typically 2–3 weeks to make + approximately 6–9 days delivery; generally about 3–4 weeks from design approval to delivery; stone-dependent; not guaranteed). "
          "MISSING (F-A1): regions served; processing vs transit times; carriers; insurance/signature; US duties/taxes; free-shipping terms; holiday order-by dates. "
          "ACTION: delete the placeholder block now; write the policy from confirmed facts under plain headings (Processing, Delivery, Insurance, Duties & taxes, Bespoke & made-to-order; add a Tracking section only if HOD confirms order tracking — F-A1); link from PDPs, FAQ and footer. OWNER: HOD (facts), content editor (copy)."),
    sch="WebPage + BreadcrumbList. OfferShippingDetails / hasShippingService on Offers only after the policy is final.", sact="ADD (conditional, Class B)",
    aeo="MEDIUM — 'How long does House of Diams shipping take?' is a likely AI-answer query; answer with confirmed terms only.",
    qs="How long does shipping take? | Is shipping insured? | Are duties and taxes included for US orders? | How long does a bespoke order take to arrive?",
    geo="Single shipping statement reused on PDP, FAQ, footer badge.", trust="Remove 'overnight' and 'free worldwide' claims unless confirmed.", img="None.",
    prio="CRITICAL", aws="B", dep="All shipping facts (F-A1); the CMS edit to delete the placeholder may be possible before AWS (E-01/E-02).", dec="OD-08",
    status="HOD INPUT REQUIRED", deps=D(hod="F-A1", eng="E-01, E-02"), notes="Public test artifact on a trust page → CRITICAL.")

CORE["SUP-POLICIES-RET"] = dict(
    name="Returns & exchanges policy",
    title="Returns & Exchanges", tact="REPLACE — FINAL (apply when the policy is published)",
    meta="How returns and exchanges work at House of Diams, and how to contact us with questions about your order.", mact="REPLACE — FINAL (no return window mentioned until F-A2; no order-tracking promise until F-A1 confirms it)",
    h1="Returns & Exchanges", hact="KEEP — correct.",
    cact="REWRITE (trust-critical) — add the actual policy",
    sect=("CURRENT PROBLEM: the visible body is the 'Is House of Diams legitimate?' answer, a Quick Actions block and contact details — NO return terms. Header badge says 'Complimentary 15-Day Returns' (unverified). Email here is Admin@houseofdiams.com vs info@ elsewhere; hours 'Mon-SUN · 9am-12pm' look inconsistent. "
          "CONFIRMED FACT: none. MISSING (F-A2): return/exchange window, condition, exclusions (bespoke/made-to-order, engraved), refund method and timing, return shipping, how to start a return. "
          "ACTION: publish a complete policy under plain headings; move the legitimacy answer to /about and /faq (F-C1); one contact email (F-C2); remove FAQPage from this page; add MerchantReturnPolicy once terms are final."),
    sch="REMOVE FAQPage (attached to a non-FAQ body). Add WebPage + BreadcrumbList; MerchantReturnPolicy (Organization- or Offer-level) only when terms are final.", sact="UPDATE (Class B)",
    aeo="MEDIUM — 'What is House of Diams' return policy?' answered with confirmed terms only.", qs="What is the return policy? | Can I return a bespoke piece? | How do I start an exchange? | Who pays return shipping?",
    geo="Single returns statement reused on PDP, FAQ, footer badge.", trust="Do not publish '15-day' anywhere until confirmed.", img="None.",
    prio="HIGH", aws="B", dep="All returns facts (F-A2); schema = Class B.", dec="OD-08",
    status="HOD INPUT REQUIRED", deps=D(hod="F-A2, F-C2", eng="E-01, E-02, E-08"), notes="Title/H1 are fine today; the page content is the defect.")

CORE["SUP-POLICIES-PRIV"] = dict(
    name="Privacy policy", title="Privacy Policy", tact="KEEP (current 'Privacy Policy | House of Diams' is correct)",
    meta="— (leave as is)", mact="KEEP", h1="Privacy Notice", hact="KEEP", cact="NONE (legal content is outside SEO scope)",
    sect="No on-page SEO change. Optional: align H1 'Privacy Notice' with the nav label 'Privacy Policy' (cosmetic).",
    sch="None.", sact="NO CHANGE", aeo="NONE.", qs="—", geo="—", trust="Legal review is the business's responsibility.", img="None.",
    prio="LOW", aws="C", dep="Verify after AWS: 200, self-canonical, indexable, in sitemap.", dec="", status="NO CHANGE REQUIRED", deps=D(), notes="")

CORE["SUP-POLICIES-TERMS"] = dict(
    name="Terms & conditions", title="Terms & Conditions", tact="KEEP",
    meta="— (leave as is)", mact="KEEP", h1="Terms & Conditions", hact="KEEP", cact="NONE (legal content is outside SEO scope)",
    sect="No on-page SEO change. Check the terms do not contradict /shipping and /returns once those are final.",
    sch="None.", sact="NO CHANGE", aeo="NONE.", qs="—", geo="—", trust="Legal review is the business's responsibility.", img="None.",
    prio="LOW", aws="C", dep="Verify after AWS: 200, self-canonical, indexable.", dec="", status="NO CHANGE REQUIRED", deps=D(), notes="")

CORE["BLOG-HUB"] = dict(
    name="Blog index",
    title="Blog: Jewelry Gift Ideas, Style & Stories", tact="REPLACE — FINAL (OD-12: section name is 'Blog'; current title is just 'Blog')",
    meta="Gift ideas, style advice and stories from House of Diams, with links to our diamond and jewelry guides.", mact="REPLACE — FINAL",
    h1="Stories from House of Diams", hact="KEEP — descriptive heading that does not conflict with the section name 'Blog' (OD-12).",
    cact="RESTRUCTURE + NAMING",
    sect=("1) Standardize the public name to 'Blog' in nav, title, breadcrumbs and article back-links ('Back to Journal' → 'Back to Blog'); the URL /blog is unchanged (no /journal). "
          "2) Pagination: /blog?page=N gets a self-referencing canonical and the title 'Blog – Page N' (today page 2 canonicalises to /blog). "
          "3) The index lists the 10 Education-owned /blog articles until their Education path exists (Stage 16) — never remove a listing before that; list planned Blog posts chronologically; categories become pages only when they hold real posts (Stage 13). "
          "4) Descriptive card anchors (article title), not 'Read more'. 5) Organization byline (OD-11)."),
    sch="CollectionPage or Blog (optional) + BreadcrumbList; Organization as publisher.", sact="ADD (Class B)", aeo="NONE (index).", qs="—",
    geo="Consistent author/publisher entity across posts.", trust="Organization byline unless a named person is verified.", img="Card images: alt = article topic; lazy-load below fold.",
    prio="MEDIUM", aws="B", dep="Pagination/title support in the template (E-06); byline/breadcrumb template (E-07).", dec="OD-05; OD-11; OD-12",
    status="READY FOR IMPLEMENTATION POST-AWS", deps=D(eng="E-01, E-02, E-06, E-07"), notes="")

CORE["EDU-ROOT"] = dict(
    name="Education index",
    title="Diamond Guides: 4Cs, Lab-Grown & Metals", tact="REPLACE — FINAL",
    meta="Plain-English guides to lab-grown and natural diamonds, the 4Cs, certification, metals and ring sizing from House of Diams.", mact="REPLACE — FINAL",
    h1="Diamond & Jewelry Guides", hact="REPLACE — FINAL (US spelling). Current 'Education' is a nav label, not a descriptive heading.",
    cact="EXPAND (hub structure per Stage 14)",
    sect=("1) List the eight Stage 14 topic hubs (Lab-Grown, Natural, 4Cs, Shapes, Certification, Metals, Ring & Jewelry Guides, Diamond properties) with one-line descriptions; until hub pages exist, list the 11 Education-owned articles by topic (OD-13: URLs unchanged). "
          "2) Today the page lists 1 article (GIA vs IGI) although 10 more live at /blog; its H2 is the article's own <title> string including '| House of Diams' (template bug). "
          "3) Required links (Stage 16): EDU-4C-00, EDU-CERT-00, EDU-SHP-00 (missing today) and EDU-LG-00 at launch (2026-10-21). 4) No URL moves in this phase."),
    sch="CollectionPage (optional) + BreadcrumbList.", sact="ADD (Class B)", aeo="NONE (index) — make each guide's direct question obvious in its link text.", qs="—",
    geo="Hub = the entity map of HOD's diamond knowledge; keep topic names identical to page titles.", trust="Show 'last updated' on child guides, not on the index.", img="Topic-card images: descriptive alt.",
    prio="HIGH", aws="B", dep="First new hub (EDU-LG-00, 2026-10-21) needs this index to link it (Stage 16 REQUIRED).", dec="OD-05; OD-13",
    status="READY FOR IMPLEMENTATION POST-AWS", deps=D(eng="E-01, E-02"), notes="")


def cat(name, title, meta, h1, sect, prio, dec="OD-01; OD-05", notes="", deps=None):
    return dict(name=name, title=title, tact="REPLACE — FINAL (keyword assigned under OD-01)", meta=meta, mact="REPLACE — FINAL",
        h1=h1, hact="REPLACE — FINAL ('Explore X' is generic).",
        cact="ADD UNIQUE INTRO + CLEAN UP", sect=sect, sch=SCH_CAT, sact="UPDATE (Class B)",
        aeo="LOW (commercial listing) — a 2-sentence category definition above the grid; buying questions are answered by linked Education owners, not duplicated.",
        qs="Which style/type should I choose? (answered by the linked Education owner)", geo="Clear category definition + attributes (metal, stone type, shape) consistent with PDP Product schema.",
        trust="Link to certification, returns and bespoke only with confirmed facts. State stone origin at product level only until F-E1.", img=IMG_CAT, prio=prio, aws="B",
        dep="Metadata/intro/schema changes via CMS or code (E-02, E-08).", dec=dec, status="READY FOR IMPLEMENTATION POST-AWS",
        deps=deps or D(eng="E-01, E-02, E-08"), notes=notes)


CORE["COM-ER"] = cat("Engagement rings (category hub)",
    "Diamond Engagement Rings: Halo & Solitaire",
    "Shop diamond engagement rings in halo, solitaire, pavé, three-stone, bezel and side-stone styles, plus bespoke options.",
    "Diamond Engagement Rings",
    ("1) Unique intro (short; guideline ~100–200 words, not a target): what is here (styles with links to the style subcategories), how to choose (shape → EDU-SHP-00, quality → EDU-4C-00, size → EDU-RJG-02), and a bespoke link (/bespoke). "
     "2) Stone origin only at product level until HOD confirms F-E1; then the intro may state it once, supporting the secondary heads 'lab grown diamond engagement rings' (90,500) and 'lab grown diamond rings' (90,500) on this URL (no separate landing page, D-05). "
     "3) Replace the sitewide boilerplate 'Engagement Rings FAQ' with category-specific visible Q&A or remove it. "
     "4) Surface the ranking PDP /shop/oval-floral-diamond-ring and /engagement-rings/by-design/side-stone-rings (Stage 16 REQUIRED). 5) ?page=N: self-canonical + 'Page N' in title/H1 (E-06). "
     "6) The identical /engagement-rings/by-design grouping page canonicalises here (OD-06); PDP breadcrumbs must stop linking to it (E-13)."), "HIGH",
    dec="OD-01; OD-02; OD-05; OD-06", deps=D(hod="F-E1 (activates origin-qualified secondary heads)", eng="E-01, E-02, E-06, E-08, E-13"),
    notes="Assigned primary 'engagement ring' (673,000/mo). Evidence: volume + DFS intent; SERP not validated.")
CORE["COM-WB"] = cat("Wedding bands (category hub)",
    "Diamond Wedding Bands: Eternity & More",
    "Shop women's diamond wedding bands: eternity, half-eternity and anniversary styles, with guidance on metals and ring size.",
    "Diamond Wedding Bands",
    ("1) Unique intro with links to the metals guides (EDU-MET-01 live, EDU-MET-00 planned), ring size (EDU-RJG-02), the wedding-band buying guide (EDU-WB-GUIDE) and the types guide (EDU-WB-TYPES) once live. "
     "2) The hub and /wedding-bands/for-her list the identical 7 products: the hub owns the intent while the range is women's-only (OD-01); /for-her canonicalises here and leaves the sitemap until a distinct men's range exists (F-E3). "
     "3) Do not publish a men's-band proposition. 4) Calendar boundary note reserves 'matching wedding band' (6,600) for this hub — add a matching-bands section only if matching-set products exist (VERIFY inventory). "
     "5) Eternity: /wedding-bands/for-her/eternity is the single home (OD-16); /fine-jewellery/rings/eternity-rings stays empty/noindex."), "MEDIUM",
    dec="OD-01; OD-05; OD-16", deps=D(hod="F-E3", eng="E-01, E-02, E-05, E-08"),
    notes="Assigned primary 'diamond wedding bands' (18,100/mo); secondary 'wedding bands for women' (60,500/mo) held on the hub. Core area but small inventory (7 products) → MEDIUM.")
CORE["COM-FJ"] = cat("Fine jewelry (umbrella)",
    "Fine Diamond Jewelry Collection",
    "Explore House of Diams fine diamond jewelry: earrings, necklaces and pendants, bracelets and rings.",
    "Fine Diamond Jewelry",
    ("1) Route to Earrings / Necklaces & Pendants / Bracelets (Stage 16 REQUIRED outgoing) and to the 4Cs guide. 2) Currently a product grid + boilerplate FAQ. "
     "3) No keyword is assigned (no measured demand for 'fine jewelry'/'diamond jewelry'; 'luxury jewelry' is brand-dominated). The visible label becomes 'Fine Jewelry' (US spelling); the slug /fine-jewellery is unchanged. 4) Do not duplicate the child categories' copy."), "MEDIUM",
    dec="OD-01; OD-05", notes="No keyword by design — navigational umbrella.")
CORE["COM-FJ-EARRINGS"] = cat("Earrings (category)",
    "Diamond Earrings: Studs, Hoops & Drops",
    "Shop diamond earrings: solitaire and halo studs, hoops and huggies, and drop styles in a range of diamond shapes.",
    "Diamond Earrings",
    ("1) Short buying guidance: choosing studs vs hoops vs drops, link to 4Cs (EDU-4C-00), metals (EDU-MET-00 when live), carat guide EDU-4C-07 (planned) and BC-025 'different types of earrings' when live. "
     "2) The empty 'Tennis' and 'Personalized & Charm' child tabs are removed from the hub/nav until populated (OD-07). "
     "3) Broad head stays on the hub; 'diamond stud earrings' belongs to the stud child (OD-16)."), "HIGH", dec="OD-01; OD-05; OD-07; OD-16",
    notes="Assigned primary 'diamond earrings' (74,000/mo).", deps=D(eng="E-01, E-02, E-08, E-13"))
CORE["COM-FJ-NECKLACES"] = cat("Necklaces & pendants (category)",
    "Diamond Necklaces & Pendants",
    "Shop diamond necklaces and pendants: solitaire, toi et moi, multi-stone, charm and lariat styles.",
    "Diamond Necklaces & Pendants",
    ("1) Unique intro + link to the planned necklace length chart (EDU-RJG-NL) and BC-006 'necklace layering' (approved package). 2) The hub's empty children (tennis necklace, initials) leave the nav until populated (OD-07). "
     "3) /t-bar remains a separate curated collection with a disjoint product set (OD-16)."), "HIGH", dec="OD-01; OD-05; OD-07; OD-16",
    notes="Assigned primary 'diamond necklace' (49,500/mo).", deps=D(eng="E-01, E-02, E-08, E-13"))
CORE["COM-FJ-BRACELETS"] = cat("Bracelets (category)",
    "Diamond Bracelets: Chain, Link & Tennis",
    "Shop diamond bracelets: chain, link and tennis styles.",
    "Diamond Bracelets",
    ("1) Unique intro + link to the planned bracelet size chart (EDU-RJG-BR) and BC-021 'what is a tennis bracelet' when live. 2) 11 products. "
     "3) Slug is singular '/bracelet' — leave (URL change = migration). 4) 'tennis bracelet' (135,000) belongs to the tennis CHILD: the hub title lists tennis last and does not lead with it."), "MEDIUM",
    dec="OD-01; OD-05; OD-16", notes="Assigned primary 'diamond bracelet' (27,100/mo).", deps=D(eng="E-01, E-02, E-08"))
CORE["COM-FJ-RINGS"] = cat("Fine-jewelry rings (category)",
    "Diamond Statement & Fashion Rings",
    "Shop House of Diams diamond fashion and statement rings, designed to wear beyond engagement rings and wedding bands.",
    "Diamond Statement & Fashion Rings",
    ("The page lists 2 products (an Asscher statement row ring and a four-petal pear/marquise ring); its only child /fine-jewellery/rings/eternity-rings is empty. FINAL: keep the page with a descriptive, non-bridal title; NO keyword assigned ('diamond ring' 110,000 is ambiguous across engagement/wedding/fashion intent and is HELD — see keyword log). "
     "Unique intro explaining the difference from engagement rings and wedding bands, linking to both. Inventory watch: review with GSC Queries at 90 days; merchandising to add products."), "MEDIUM",
    dec="OD-01; OD-05; OD-16", notes="HELD — ambiguous head + thin inventory; reversible default is a descriptive title.", deps=D(eng="E-01, E-02, E-08"))
CORE["COM-CURATED-TBAR"] = cat("T-Bar (curated collection)",
    "T-Bar Necklaces & Pendants",
    "Shop the House of Diams T-bar collection: knot, ridged and interlocking T-bar necklaces and pendants.",
    "T-Bar Necklaces & Pendants",
    ("1) Curated-collection page type (D-14), placement unchanged. 4 products; zero overlap with /fine-jewellery/necklaces/pendant-necklace, so no merge and one home for 't bar necklace' (OD-16). "
     "2) Fix the visible name typo 'T- BAR' → 'T-Bar' in the collection name (URL unchanged). 3) Do not add 'diamond' to the title unless the product records confirm diamonds in every T-bar piece."), "MEDIUM",
    dec="OD-01; OD-05; OD-16", notes="Assigned primary 't bar necklace' (2,400/mo); inventory watch (4 products).", deps=D(eng="E-01, E-02, E-08"))
CORE["COM-ER-STYLES-GROUP"] = cat("Engagement rings — 'By Design' grouping page",
    "— (no metadata work: canonicalised to /engagement-rings)", "— (none)", "Engagement Ring Styles",
    ("Identical 24 = 24 initial-HTML products and the same boilerplate FAQ as /engagement-rings, indexable, self-canonical and in the sitemap. FINAL (OD-06): canonical → /engagement-rings, remove from the sitemap, stop linking to it (PDP breadcrumb 'By Design', nav); keep the 8 child style URLs untouched. "
     "The page remains reachable for users; the visible H1 becomes 'Engagement Ring Styles' (US wording). A redirect is the later alternative once no internal link points here and GSC shows no standalone demand."), "HIGH",
    dec="OD-06", notes="No keyword by design.", deps=D(eng="E-01, E-05, E-13", gsc="G-03 (non-blocking)"))
CORE["COM-ER-STYLES-GROUP"]["tact"] = "HOLD — canonical to /engagement-rings (OD-06 adopted)"
CORE["COM-ER-STYLES-GROUP"]["mact"] = "HOLD"
CORE["COM-ER-STYLES-GROUP"]["hact"] = "REPLACE — user-facing label only"
CORE["COM-ER-STYLES-GROUP"]["aeo"] = "NONE."

CORE["COM-PDP"] = dict(
    name="Product page template (184 PDPs)",
    title="{Shape} {Product type}, {Carat} ct — see 07-PDP-ON-PAGE-SEO.md for the template", tact="TEMPLATE RULE (not a per-page edit)",
    meta="{Product type} with a {shape} diamond ({carat} ct total) in {metal}, {setting}. {Stone type}. See details, metal options and price. — spec in 07", mact="TEMPLATE RULE",
    h1="Visible product name (unchanged); must equal the schema name", hact="KEEP product names; align schema name with H1",
    cact="TEMPLATE FIXES + PRIORITY PDPs", sect="See 07-PDP-ON-PAGE-SEO.md: title/meta/H1 templates, description rules, specs, variants (OD-14: keep URLs), alt text, schema, links. Per-PDP issues: 6 placeholder metas, 2 duplicate titles, 65 titles >60 rendered chars, 10 numeric-ID/'-copy-' slug variants, 1 truncated material label ('Gold Vermil').",
    sch="Product + Offer + Brand + BreadcrumbList (present). Fix: name = visible H1; sku = visible SKU (JSON-LD uses a UUID; page shows e.g. RG038993); material/price must describe the same default variant; BreadcrumbList must match the visible path; no ratings/reviews unless genuine; shipping/return details only when final; image URLs change with AWS.",
    sact="UPDATE (Class B/C)", aeo="LOW–MEDIUM — product facts in a spec table are extraction-friendly; no FAQ boilerplate.", qs="What is the metal/stone/carat/setting? | Is the diamond lab-grown? | What size/ring size options exist?",
    geo="HIGH for AI shopping surfaces: complete, consistent Product attributes + stable image URLs + /llms.txt product list.", trust="Certification per product only if a report exists (lab + number); never a blanket claim (F-B1).",
    img="Product images: '<product name>, <view>' (e.g. 'Oval Marquise Diamond Engagement Ring, side view'); first image = primary; no keyword stuffing; video poster alt. Image host change is Class B.",
    prio="HIGH", aws="B", dep="Template/CMS changes after AWS (Class B); per-PDP shipping/warranty/'IGI certified' text replaced by neutral policy links until facts arrive.", dec="OD-08; OD-14",
    status="READY FOR IMPLEMENTATION POST-AWS", deps=D(hod="F-A1, F-A2, F-A3, F-B1, F-E4 (upgrade PDP claims once confirmed)", eng="E-01, E-02, E-09, E-10"),
    notes="Do not rewrite all 184 PDPs; apply templates and fix the flagged list (07-PDP-PRIORITY-ACTIONS.csv).")

CORE["COM-PDP-OVAL-FLORAL"] = dict(
    name="Oval Marquise engagement ring (ranking PDP)",
    title="2.5 ct Oval Marquise Diamond Engagement Ring", tact="REPLACE — FINAL (OD-15); apply only after the GSC baseline (ranking URL)",
    meta="Oval engagement ring with a 2.5 ct oval lab-grown center diamond and 16 marquise side stones in a raised four-prong setting, available in 10K and 14K gold.",
    mact="REPLACE — FINAL (fact-check specs against the product record)",
    h1="Oval Marquise Diamond Engagement Ring", hact="REPLACE — FINAL (OD-15); align the Product schema name; 'Side-Stone' is not the lead term so COM-ER-SIDESTONE stays separate",
    cact="MINOR (do NOT change slug)", sect=("Keep 'oval' and 'marquise' in title/H1/description (owned keyword). JSON-LD name is 'Oval Floral Diamond Ring' while the H1 is 'Oval Marquise Side-Stone Engagement Ring' — make both 'Oval Marquise Diamond Engagement Ring'. "
        "Meta says '2.500 ct center … 16 marquise accents'; the spec table shows total carat 4.10 ct — keep center vs total wording explicit. Add the ring-size guide link (Stage 16 REQUIRED)."),
    sch="Product: name = H1; sku = visible SKU (RG038993); description = visible description; material list vs single price → align to the default variant; BreadcrumbList to match the visible path.", sact="UPDATE (Class B)",
    aeo="LOW.", qs="What is the center stone size? | What metals is it available in? | What is the ring size range?", geo="Consistent attributes with the Side-Stone category.", trust="Origin 'Lab Grown Diamond' is shown in the spec table; certification not shown — do not claim.",
    img="Gallery alt: 'Oval Marquise Diamond Engagement Ring, <view>'.", prio="MEDIUM", aws="B", dep="GSC baseline for the ranking URL (est. pos 90 is a DataForSEO estimate).", dec="OD-15",
    status="GSC BASELINE REQUIRED", deps=D(eng="E-01, E-02, E-09", gsc="G-01, G-02 (blocking live change)", block=True),
    notes="Stage 13 NO_ACTION on URL. Stage 16 REQUIRED links: COM-ER, COM-ER-SIDESTONE, EDU-RJG-02. Spec is final; only the live change waits for the baseline.")

CORE["LEG-ER-SIDESTONE"] = dict(
    name="Legacy URL: /engagement-rings/by-desgin/side-stone-rings (404)",
    title="— (301 redirect; no page)", tact="N/A", meta="—", mact="N/A", h1="—", hact="N/A", cact="REDIRECT 301 → /engagement-rings/by-design/side-stone-rings",
    sect="Redirect R-08 in the developer redirect map (10-DECISIONS-RESOLUTION-LOG.md §OD-06): 1:1 301 from /engagement-rings/by-desgin/side-stone-rings to /engagement-rings/by-design/side-stone-rings (target confirmed 200, self-canonical). Then update the research registry URL record (ownership unchanged).",
    sch="None.", sact="N/A", aeo="N/A", qs="—", geo="—", trust="—", img="N/A", prio="CRITICAL", aws="B",
    dep="Redirect implementation = Class B; verify 301 + final 200 after AWS (Class C).", dec="OD-06",
    status="READY FOR IMPLEMENTATION POST-AWS", deps=D(eng="E-01, E-03, E-04", gsc="G-03 (confirm indexed state; non-blocking — a 1:1 redirect is the safe direction)"),
    notes="Ranking-equity risk: the Stage 15 keyword-owner URL returns 404 with no 301 today.")
CORE["LEG-ER-GROUP"] = dict(
    name="Legacy URL: /engagement-rings/by-desgin (grouping)",
    title="— (301 redirect; no page)", tact="N/A", meta="—", mact="N/A", h1="—", hact="N/A", cact="REDIRECT 301 → /engagement-rings/by-design",
    sect="Redirect R-09: 1:1 to the corresponding valid group URL (which itself canonicalises to /engagement-rings, OD-06). Part of the by-desgin set (group + 8 style URLs).",
    sch="None.", sact="N/A", aeo="N/A", qs="—", geo="—", trust="—", img="N/A", prio="LOW", aws="B", dep="Redirect implementation = Class B.", dec="OD-06",
    status="READY FOR IMPLEMENTATION POST-AWS", deps=D(eng="E-01, E-03, E-04", gsc="G-03 (non-blocking)"), notes="")
CORE["COM-HIPHOP"] = dict(
    name="/hiphop (308 → /shop)",
    title="— (redirect; no page)", tact="N/A", meta="—", mact="N/A", h1="—", hact="N/A", cact="KEEP 308 → /shop; keep children out of sitemap/nav",
    sect="/hiphop 308-redirects to /shop; /hiphop/chains, /hiphop/chains/cuban-links and /hiphop/test-subcat are still in the sitemap (empty/test). Header nav and the /bespoke piece-type list still expose 'Hip Hop'. FINAL: keep the redirect; children noindex + out of sitemap/nav (test item removed); reinstate a populated collection only after HOD confirms the range (F-E3).",
    sch="None.", sact="N/A", aeo="N/A", qs="—", geo="—", trust="Hip Hop range existence is UNCONFIRMED.", img="N/A", prio="LOW", aws="C",
    dep="Verify after AWS: 308 → /shop persists. Re-opening a Hip Hop collection needs the range confirmed (F-E3).", dec="OD-07; OD-08",
    status="NO CHANGE REQUIRED", deps=D(hod="F-E3 (only if a Hip Hop range is reinstated)", eng="E-05, E-13"), notes="Children rows carry the noindex/sitemap handling.")
CORE["LEG-fine-jewellery-test-product"] = dict(
    name="Legacy URL: /shop/fine-jewellery-test-product (404)",
    title="—", tact="N/A", meta="—", mact="N/A", h1="—", hact="N/A", cact="NONE — keep 404 (or 410)",
    sect="Test product removed. Ensure no internal links or /llms.txt entries still point to it.", sch="None.", sact="N/A", aeo="N/A", qs="—", geo="—", trust="—", img="N/A",
    prio="LOW", aws="C", dep="Verify 404/410 persists after AWS.", dec="", status="NO CHANGE REQUIRED", deps=D(), notes="")
CORE["LEG-marquise-floral-diamond-engagement-ring"] = dict(
    name="Legacy URL: /shop/marquise-floral-diamond-engagement-ring (404)",
    title="—", tact="N/A", meta="—", mact="N/A", h1="—", hact="N/A", cact="301 to the nearest equivalent ONLY if GSC shows equity; otherwise leave 404/410",
    sect="Product removed from the catalog (404). If the GSC Pages export shows impressions/links, 301 to the nearest equivalent (/shop/oval-floral-diamond-ring or /engagement-rings); otherwise leave 404/410. No redirect to an irrelevant page.",
    sch="None.", sact="N/A", aeo="N/A", qs="—", geo="—", trust="—", img="N/A", prio="LOW", aws="B", dep="GSC Pages export (G-01).", dec="OD-06; OD-18",
    status="GSC BASELINE REQUIRED", deps=D(eng="E-03, E-04", gsc="G-01 (blocking)", block=True), notes="")
