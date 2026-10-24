# -*- coding: utf-8 -*-
"""Planned Blog posts (33). 10 have approved CMS packages (values carried read-only from blogs/bc-*/seo-metadata.md);
23 get DRAFT titles/metas that must be finalised when the article is written."""
from s2_core import SCH_ART, D

PACKAGED = {  # id -> (package dir, priority, note)
 "BC-001": ("bc-001", "HIGH", "PUBLICATION HELD pending F-A1 (decided 2026-10-10). The approved package is protected and is NOT edited by Step 2 — this is a publication status only. The approved meta, intro and article say '6–9 days of insured shipping'; 'insured' is not a confirmed fact (SR-02). If HOD confirms insured shipping: publish as packaged after the normal human review. If not confirmed: a separate, explicitly authorized content revision of the package is required before publication. The bespoke timeline itself is confirmed (SR-01). APPROVED (business fact confirmed). DO NOT MODIFY BC-001. Observation only (not an edit): the approved meta says '3–4 weeks on average from design approval to delivery' and '6–9 days of insured shipping' — the confirmed fact is 'typically 2–3 weeks to make + ~6–9 days delivery, generally ~3–4 weeks from design approval to delivery, depends on the stone, never a guarantee' (start point confirmed by the project owner 2026-10-10 — SR-01). The word 'insured' is NOT in the confirmed-fact file: source-reconciliation item SR-02, covered by the shipping-policy fact F-A1. BC-001 is protected and was not changed; if F-A1 shows shipments are not insured, the package wording needs a user edit before publishing."),
 "BC-004": ("bc-004", "HIGH", "Seasonal (Christmas/Hanukkah) — publishing window matters; December refresh (BC-004-DEC-REFRESH) needs ready-to-ship business facts and is merged here."),
 "BC-035": ("bc-035", "HIGH", "33,100/mo; mixed commercial-research SERP — keep guide format and link to category pages."),
 "BC-018": ("bc-018", "HIGH", "74,000/mo; hub for the anniversary-gift series; recipient/year posts keep their own primaries (series rule)."),
 "BC-036": ("bc-036", "HIGH", "27,100/mo; boundary with BC-007 and BC-038/039 (finger/hand questions split by question)."),
 "BC-006": ("bc-006", "HIGH", "14,800/mo; boundary with EDU-RJG-NL (layering = styling; length chart = sizing)."),
 "BC-008": ("bc-008", "MEDIUM", "SERP is product-led (transactional/commercial) — keep as a guide linking to category pages; expect modest traffic."),
 "BC-009": ("bc-009", "MEDIUM", "Same series rule as BC-008."),
 "BC-003": ("bc-003", "HIGH", "18,100/mo; informational SERP."),
 "BC-007": ("bc-007", "MEDIUM", "Boundary with BLOG-WR-TYPES / EDU-WB-GUIDE / BC-022."),
}

# id: (title, meta, h1, priority, status, bf, note)
DRAFT = {
 "BC-011": ("What Is a Promise Ring? Meaning and Ideas",
   "A promise ring is a ring given as a commitment, without being an engagement. What it means, who gives one and how it differs from an engagement ring.",
   "What Is a Promise Ring? Meaning, Who Gives One, and How It Differs From an Engagement Ring", "HIGH", "PRE-AWS PREPARATION", "N", "22,200/mo; boundary with BC-039 (finger/hand) — keep exact wording separate."),
 "BC-037": ("Engagement Ring vs Wedding Ring: The Difference",
   "An engagement ring is given at the proposal and a wedding ring is exchanged at the ceremony. How they differ in style, timing and wear, and whether you need both.",
   "Engagement Ring vs Wedding Ring: What Is the Difference (and Do You Need Both)?", "HIGH", "PRE-AWS PREPARATION", "N", "18,100/mo; adjacent to BLOG-WR-TYPES/BC-007 (MEDIUM)."),
 "BC-014": ("Proposal Ideas: How to Plan a Memorable Proposal",
   "Proposal ideas and a simple planning guide, from choosing the moment and place to presenting the ring.",
   "Proposal Ideas: How to Plan a Proposal to Remember (With the Ring at the Center)", "HIGH", "PRE-AWS PREPARATION", "N", "Calendar working title uses 'she'; prefer neutral wording in H1/meta (inclusive) — copy decision for the editor."),
 "BC-015": ("Where Are Lab-Grown Diamonds Made?",
   "(HOLD — write the meta after HOD confirms the facts it will cite.)",
   "Where Are Lab-Grown Diamonds Made? (working title cites Surat, India, China and a dated 2026 market note)", "MEDIUM", "HOD INPUT REQUIRED", "Y", "Calendar: BUSINESS_FACT_REQUIRED — HOD sourcing/manufacturing statements must not be invented."),
 "BC-024": ("How Much Should an Engagement Ring Cost?",
   "How much should an engagement ring cost? There is no fixed rule — typical spending ranges, common budget guidelines and how to decide what to spend.",
   "How Much Should an Engagement Ring Cost? Average Prices, Budget Rules and How Much to Spend", "HIGH", "PRE-AWS PREPARATION", "N", "MUST_PUBLISH 2026-10-23 (6,600/mo). All figures dated and sourced; no personalized financial advice; one article owns the budget intent (user decision 2026-09-29)."),
 "BC-016": ("When Is Engagement Season?",
   "When is engagement season? Why so many proposals happen between Thanksgiving and Valentine's Day, and how that affects when to buy a ring.",
   "When Is Engagement Season? Why So Many Proposals Happen Between Thanksgiving and Valentine's Day", "MEDIUM", "PRE-AWS PREPARATION", "N", "MUST_PUBLISH 2026-10-26; small volume (170) but seasonal."),
 "BC-017": ("Christmas and New Year's Eve Proposal Ideas",
   "Festive ways to propose at Christmas or on New Year's Eve, plus a simple timeline for getting the ring ready in time.",
   "Christmas and New Year's Eve Proposal Ideas: Festive Ways to Propose (Plus a Ring-Timing Checklist)", "MEDIUM", "PRE-AWS PREPARATION", "N", "Any lead-time statement must use the confirmed bespoke fact only (typically/approximately; never a guarantee; no holiday cut-off)."),
 "BC-005": ("How Diamonds Are Cut and Polished",
   "(HOLD — write the meta after HOD confirms the workshop facts it will cite.)",
   "How Diamonds Are Cut and Polished: The Five Steps (working title cites a Surat cutting workshop)", "MEDIUM", "HOD INPUT REQUIRED", "Y", "Calendar: BUSINESS_FACT_REQUIRED — HOD workshop/process claims unconfirmed. The generic process can be written without HOD claims."),
 "BC-019": ("Best Time to Buy an Engagement Ring",
   "Is Black Friday a good time to buy an engagement ring? How sale timing, seasons and lead time affect price and choice.",
   "Is Black Friday a Good Time to Buy an Engagement Ring? The Best Time of Year to Buy Diamonds", "MEDIUM", "PRE-AWS PREPARATION", "N", "MUST_PUBLISH 2026-10-30. No discount or promotion claims for HOD."),
 "BC-021": ("What Is a Tennis Bracelet and How to Wear One",
   "A tennis bracelet is a flexible line of matching stones set around the wrist. Why it is called that, how to wear one and how to choose.",
   "What Is a Tennis Bracelet? Why It Is Called That, and How to Wear One", "MEDIUM", "PRE-AWS PREPARATION", "N", "Informational; the commercial head 'tennis bracelet' (135,000) belongs to /fine-jewellery/bracelet/tennis."),
 "BC-039": ("What Finger Does a Promise Ring Go On?",
   "Which finger and hand a promise ring is traditionally worn on, what each placement can signal and how to choose.",
   "What Finger Does a Promise Ring Go On? Placement, Hand and Meaning", "HIGH", "PRE-AWS PREPARATION", "N", "12,100/mo; boundary with BC-011 and BC-036."),
 "BC-022": ("How to Stack Rings with Your Engagement Ring",
   "How to stack rings: combinations of an engagement ring, wedding band and eternity band, with tips on order, width and metal.",
   "How to Stack Rings: Engagement Ring, Wedding Band and Eternity Band Combinations", "LOW", "PRE-AWS PREPARATION", "N", "Boundary with BC-007 and EDU-WB-GUIDE."),
 "BC-038": ("Ring Finger Meaning: What Each Finger Symbolizes",
   "What a ring on each finger is said to symbolize, from thumb to pinky, and what changes between the left and right hand.",
   "Ring Finger Meaning: What a Ring on Each Finger Symbolizes (Thumb to Pinky, Left vs Right)", "HIGH", "PRE-AWS PREPARATION", "N", "9,900/mo; boundary with BC-036/BC-039 (3 shared SERP URLs → one post)."),
 "BC-023": ("Eternity Ring Meaning and When to Give One",
   "What an eternity ring means, when couples give one, which finger it is worn on and the difference between full and half eternity.",
   "Eternity Ring Meaning: When to Give One, Which Finger, and Full vs Half Eternity", "LOW", "PRE-AWS PREPARATION", "N", "Informational; the commercial 'eternity ring/band' heads are an OD-16 one-home question."),
 "BC-025": ("Different Types of Earrings, Explained",
   "The main types of earrings — studs, huggies, hoops and drops — how they differ, and how earring backs work.",
   "Different Types of Earrings: Studs, Huggies, Hoops and Drops (Plus Earring Backs Explained)", "MEDIUM", "PRE-AWS PREPARATION", "N", "Informational; link to /fine-jewellery/earrings and the stud/hoop/drop children."),
 "BC-031": ("Engagement Ring Trends for 2027",
   "Engagement ring trends for 2027, including toi et moi, east-west, bezel, three-stone and elongated shapes, and how to choose a style that lasts.",
   "Engagement Ring Trends for 2027: Toi et Moi, East-West, Bezel, Three-Stone and Elongated Shapes", "MEDIUM", "PRE-AWS PREPARATION", "N", "MUST_PUBLISH 2026-12-01. Style heads (toi et moi, bezel, three-stone) are reserved for the COM-ER style subcategories — link, do not compete."),
 "BC-032": ("Fine Jewelry Trends for 2027",
   "Fine jewelry trends for 2027: diamond earrings, bracelets and necklaces to watch, and how to choose pieces you will keep wearing.",
   "Fine Jewelry Trends for 2027: Diamond Earrings, Bracelets and Necklaces to Watch", "MEDIUM", "PRE-AWS PREPARATION", "N", "'jewelry trends' KD 34 — highest difficulty among blog primaries."),
 "BLOG-WR-TYPES": ("Types of Wedding Rings: Band Styles Explained",
   "The main types of wedding rings and wedding band styles — classic, eternity, pavé, curved and contour — and how to choose.",
   "Types of Wedding Rings: Wedding Band Styles Explained (Classic, Eternity, Pavé, Curved, Contour and Men's Bands)", "HIGH", "PRE-AWS PREPARATION", "N", "RE-HOMED to Education 2026-10-10 (OD-04): Stage 13 tests → Education page EDU-WB-TYPES (calendar ID BLOG-WR-TYPES kept as alias; date/slot unchanged). Owns the style catalog ('types of wedding rings' 12,100); EDU-WB-GUIDE owns the buying decision; BC-037/007/022/023 stay Blog and link here."),
 "BC-034": ("Valentine's Day Proposal Ideas",
   "Romantic ways to propose on Valentine's Day, February 14, with planning tips and ring-timing advice.",
   "Valentine's Day Proposal Ideas: Romantic Ways to Propose on February 14", "MEDIUM", "PRE-AWS PREPARATION", "N", "MUST_PUBLISH 2026-12-08; any ring-timing statement uses the confirmed bespoke fact only."),
 "BLOG-ER-HISTORY": ("The History of Engagement Rings",
   "The history of engagement rings, from Roman betrothal rings to modern and lab-grown diamond rings.",
   "The History of Engagement Rings: From Roman Betrothal Rings to Lab-Grown Diamonds", "LOW", "PRE-AWS PREPARATION", "N", "FLEXIBLE slot; cite historical sources."),
 "BLOG-WB-BUYS": ("Who Buys the Wedding Bands? Etiquette Explained",
   "Who buys the wedding bands? Traditional etiquette, when to buy them and how much couples typically spend.",
   "Who Buys the Wedding Bands? Etiquette, When to Buy Them and How Much Couples Spend", "LOW", "PRE-AWS PREPARATION", "N", "Spending figures dated and sourced."),
 "BLOG-WR-HISTORY": ("Wedding Ring History and Meaning",
   "Wedding ring history and meaning: why we exchange rings, from ancient Egypt to the double-ring ceremony.",
   "Wedding Ring History and Meaning: Why We Exchange Rings, From Ancient Egypt to the Double-Ring Ceremony", "LOW", "PRE-AWS PREPARATION", "N", "FLEXIBLE slot; KD 32."),
 "BLOG-NPD": ("National Proposal Day: What It Is and Ideas",
   "What National Proposal Day (March 20) is, how it started and how to plan a spring proposal.",
   "National Proposal Day (March 20): What It Is and How to Plan a Spring Proposal, With the Ring at the Center", "LOW", "PRE-AWS PREPARATION", "N", "Verify the March 20 date and the day's origin against a source before publishing."),
}


# BC-001: the approved package (protected, unedited) contains the unconfirmed phrase 'insured shipping' (SR-02). Its PUBLICATION is held until
# F-A1 is answered. This changes the status of the future publication only — never the package.
BC001_HOLD = dict(
    status="HOD INPUT REQUIRED", bf="Y", dec="OD-08; OD-11; OD-12",
    tact="CARRY APPROVED VALUE (package unedited) — PUBLICATION HELD pending F-A1",
    mact="CARRY APPROVED VALUE (package unedited) — PUBLICATION HELD: contains 'insured shipping' (unconfirmed, F-A1/SR-02)",
    hact="CARRY APPROVED VALUE (package unedited)",
    cact="HOLD PUBLICATION pending F-A1. If HOD confirms insured shipping → publish as packaged after normal human review. If not confirmed → separate, explicitly authorized content revision before publication (the package is not edited here).",
    action="HOLD PUBLICATION (pending F-A1)",
    deps=D(hod="F-A1 (BLOCKS PUBLICATION: 'insured shipping' wording in the approved package — SR-02; package not edited here)", eng="E-01, E-02, E-07"),
)


def blog_override(rid, cal):
    from s2_load import PKG
    if rid in PACKAGED:
        d, pr, note = PACKAGED[rid]
        p = PKG[d]
        res = dict(
            title=p["title"], tact="CARRY APPROVED (package value; set in the CMS 'Article Title'; template adds the suffix)",
            meta=p["meta"].rsplit(" (", 1)[0], mact="CARRY APPROVED (CMS 'Short Intro')",
            h1=p["h1"], hact="CARRY APPROVED (CMS 'Display Title')",
            cact="PUBLISH AS PACKAGED (human review → CMS)", sect="Use the package in blogs/%s/ (cms-entry.md, article-content.html, seo-metadata.md, internal-links.md, image-requirements.md). No on-page redesign needed." % d,
            sch=SCH_ART, sact="TEMPLATE (Class B) — at CMS entry set 'Written By' to 'House of Diams' (OD-11; the package value 'HOD Team' is not edited here); package already specifies BlogPosting + BreadcrumbList; site template emits Person author and no BreadcrumbList on posts",
            prio=pr, aws="B", status="READY FOR IMPLEMENTATION POST-AWS", bf="N", gsc="N", dec="OD-11; OD-12",
            dep="Publishing into the new CMS inside the migration-safe window (E-01: content-freeze UNKNOWN); schema fixes are template-level (Class B).", notes=note)
        if rid == "BC-001":
            res.update(BC001_HOLD)
        return res
    t, m, h, pr, st, bf, note = DRAFT[rid]
    own_unresolved = t.startswith("Types of Wedding Rings")
    return dict(
        title=t, tact="DRAFT — finalize when the article is written" + (" (re-homed to Education — OD-04)" if own_unresolved else ""),
        meta=m, mact="DRAFT — FINAL DRAFT (≤155 chars guideline; answer-first; no unverified claims)" if not m.startswith("(HOLD") else "HOLD (business facts)",
        h1=h, hact="DRAFT (calendar working title; refine at writing)", cact="WRITE (calendar item; follow BLOG_PUBLISHING_CONTEXT.md)",
        sect="Write per the calendar row (secondary keywords, PAA, AEO format hint, internal_link_targets) — there is no Stage 19 brief for Blog items. Answer first; sections from the PAA; link to the Education owners named in the calendar; no FAQ padding.",
        sch=SCH_ART, sact="TEMPLATE (Class B)", prio=pr, aws="A", status=st, bf=bf, gsc="N", dec=("OD-04; OD-11" if own_unresolved else ("OD-08; OD-11" if bf == "Y" else "OD-11")),
        dep="Write now (Class A); publish inside the migration-safe window (Class B, E-01)." + (" Blocked: " + note if st != "PRE-AWS PREPARATION" else ""), notes=note)
