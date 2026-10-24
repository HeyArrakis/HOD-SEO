# -*- coding: utf-8 -*-
"""Subcategory specs — FINAL after Step 2A (keywords assigned in s2_final.A; empty pages per s2_final.EMPTY)."""
from s2_core import SCH_CAT, IMG_CAT, D
import s2_final as F

# path: (title, meta, h1, outline, education_links, boundary_note, priority)
POP = {
"/engagement-rings/by-design/side-stone-rings": ("Side-Stone Engagement Rings",
    "Shop side-stone engagement rings: a center diamond flanked by smaller stones for extra sparkle and a distinctive profile.",
    "Side-Stone Engagement Rings",
    "Define a side-stone ring in one sentence; how side-stone differs from three-stone and halo; what to weigh (center shape and size, accent-stone shape, band width, metal). Feature /shop/oval-floral-diamond-ring (Stage 16 REQUIRED) without making 'side-stone' its lead term.",
    "EDU-SHP-00 (shapes), EDU-4C-00 (4Cs)", "Stage 15 OWNER of 'side stones engagement rings' (1,000; est. pos 104 = DataForSEO estimate). The PDP keeps 'oval/marquise' as its lead terms.", "HIGH"),
"/engagement-rings/by-design/solitare-rings": ("Solitaire Engagement Rings",
    "Shop solitaire engagement rings: a single center diamond in classic and sculptural settings.",
    "Solitaire Engagement Rings",
    "Define a solitaire (one center stone, no side stones); how the setting changes the look (prong count, bezel-style, raised); how to choose center shape → EDU-SHP-00 and quality → EDU-4C-00. Fix the visible 'Solitare' typo in the category NAME (slug unchanged).",
    "EDU-SHP-00, EDU-4C-00", "Distinct from /fine-jewellery/necklaces/solitare (necklaces).", "MEDIUM"),
"/engagement-rings/by-design/halo-ring": ("Halo Engagement Rings",
    "Shop halo engagement rings: a center diamond framed by a ring of smaller stones, in a range of center-stone shapes.",
    "Halo Engagement Rings",
    "Define a halo (center stone surrounded by smaller diamonds); effect on apparent size; variants (single halo, hidden halo) only if the catalog shows them; link shapes (EDU-SHP-00) and 4Cs (EDU-4C-00).",
    "EDU-SHP-00, EDU-4C-00", "Settings explanation → EDU-RJG-01.", "MEDIUM"),
"/engagement-rings/by-design/toi-moi-rings": ("Toi et Moi Engagement Rings",
    "Shop toi et moi rings: two diamonds set side by side on one band, in modern and classic designs.",
    "Toi et Moi Engagement Rings",
    "Explain 'toi et moi' (two stones, 'you and me'); how to choose two shapes that pair well → EDU-SHP-00; BC-031 (engagement ring trends) reserves toi et moi style heads for this page. Inventory watch: 1 product.",
    "EDU-SHP-00", "Necklace page /fine-jewellery/necklaces/toi-et-moi must not use ring-intent heads (disjoint product sets).", "MEDIUM"),
"/engagement-rings/by-design/pave": ("Pavé Engagement Rings",
    "Shop pavé engagement rings with small diamonds set closely along the band for continuous sparkle.",
    "Pavé Engagement Rings",
    "Define pavé; benefits/trade-offs (sparkle vs maintenance — generally accepted facts only); link EDU-RJG-01 (settings guide, owner confirmed) and EDU-4C-00. No keyword assigned (no measured demand) — page stays a populated navigational listing.",
    "EDU-4C-00, EDU-RJG-01", "Distinct from the empty /wedding-bands/for-her/pavee.", "MEDIUM"),
"/engagement-rings/by-design/nature-inspired-rings": ("Nature-Inspired Engagement Rings",
    "Shop nature-inspired engagement rings with vine, leaf and floral designs.",
    "Nature-Inspired Engagement Rings",
    "Describe the motifs shown (vine, leaf, floral) from the actual catalog only; how motif interacts with center shape; link EDU-SHP-00. No keyword assigned (no measured demand).",
    "EDU-SHP-00", "Navigational style listing.", "MEDIUM"),
"/engagement-rings/by-design/three-stone-rings": ("Three-Stone Engagement Rings",
    "Shop three-stone engagement rings: a center diamond flanked by two stones, often read as past, present and future.",
    "Three-Stone Engagement Rings",
    "Define three-stone; symbolism (commonly 'past, present, future' — present as tradition, not a HOD claim); ways to combine shapes; link EDU-SHP-00 and EDU-4C-00.",
    "EDU-SHP-00, EDU-4C-00", "BC-031 reserves this head for the commercial page; 4 products.", "MEDIUM"),
"/engagement-rings/by-design/bezel-rings": ("Bezel Engagement Rings",
    "Shop bezel engagement rings, where a smooth metal rim holds the center diamond securely.",
    "Bezel Engagement Rings",
    "Define bezel (metal rim around the stone); practical points (low profile, snag resistance — generally accepted); link EDU-RJG-01. Inventory watch: 2 products.",
    "EDU-4C-00, EDU-RJG-01", "Settings explanation → EDU-RJG-01.", "MEDIUM"),
"/wedding-bands/for-her": ("— (canonical to /wedding-bands)", "— (none)", "Women's Diamond Wedding Bands",
    "FINAL (OD-01/OD-16): this page lists the identical 7 products as /wedding-bands, so it is a duplicate listing. Canonical → /wedding-bands, out of the sitemap, nav label unchanged; restore as a distinct indexable child (owning 'wedding bands for women') only if a men's range exists (F-E3). Visible H1 uses US wording.",
    "—", "Reversible default.", "MEDIUM"),
"/wedding-bands/for-her/eternity": ("Diamond Eternity Bands & Rings for Women",
    "Shop diamond eternity bands and rings for women: full and half-eternity designs in a range of diamond shapes.",
    "Diamond Eternity Bands & Rings for Women",
    "Define eternity (stones all the way around vs half/three-quarter — only if the catalog shows both); how to size and stack; link BC-023 'eternity ring meaning' when live and EDU-RJG-02. 6 products.",
    "EDU-RJG-02; BC-023 when live", "SINGLE HOME for eternity commercial intent (OD-16): /fine-jewellery/rings/eternity-rings stays empty/noindex. 'eternity band'/'eternity ring' are DFS-informational — SERP check via GSC.", "MEDIUM"),
"/wedding-bands/for-her/anniversay": ("Diamond Anniversary Rings & Bands",
    "Shop diamond anniversary rings and bands, a row of diamonds to mark a milestone or complete a ring stack.",
    "Diamond Anniversary Rings & Bands",
    "Define anniversary band; occasion framing; link BC-018/BC-035 anniversary gift guides (approved packages). Fix the visible 'Anniversay' typo in the category NAME (slug unchanged). Inventory watch: 1 product.",
    "BC-018, BC-035 when live", "Blog posts BC-018/BC-035 stay informational; this page is the commercial destination.", "MEDIUM"),
"/fine-jewellery/earrings/stud-earrings": ("Diamond Stud Earrings",
    "Shop diamond stud earrings in solitaire and halo styles and a range of diamond shapes.",
    "Diamond Stud Earrings",
    "Define studs; how to choose (total carat weight per pair vs per stone, shape, setting, metal); link EDU-4C-07 carat guide (planned) and EDU-4C-00. Strongest earrings child.",
    "EDU-4C-07 (planned), EDU-4C-00", "Hub keeps 'diamond earrings'; this child owns 'diamond stud earrings'. Informational stud queries stay with EDU-4C-07.", "HIGH"),
"/fine-jewellery/earrings/hoops-huggies": ("Diamond Hoop & Huggie Earrings",
    "Shop diamond hoop and huggie earrings, from slim huggies to statement hoops.",
    "Diamond Hoop & Huggie Earrings",
    "Short guide: hoop vs huggie (size/closure — generally accepted definitions); link BC-025 'different types of earrings' when live.",
    "BC-025 when live", "BC-025 stays informational.", "MEDIUM"),
"/fine-jewellery/earrings/drop-dangle": ("Diamond Drop & Dangle Earrings",
    "Shop diamond drop and dangle earrings with movement and sparkle.",
    "Diamond Drop & Dangle Earrings",
    "Short guide: drop vs dangle; occasion use; link BC-025 when live. Fix 'Drops' naming consistency across PDPs (Radiant Halo Drops etc. have placeholder metas).",
    "BC-025 when live", "—", "MEDIUM"),
"/fine-jewellery/necklaces/solitare": ("Diamond Solitaire Necklaces",
    "Shop diamond solitaire necklaces and pendants: a single stone on a fine chain.",
    "Diamond Solitaire Necklaces",
    "Define solitaire pendant; chain length and carat considerations; link the necklace length chart (EDU-RJG-NL) and BC-006. Fix the visible 'Solitare' typo in the category NAME (slug unchanged).",
    "EDU-RJG-NL, BC-006", "Product set is disjoint from /pendant-necklace (0 overlap): 'solitaire'-qualified heads here, generic 'pendant' heads there (OD-16).", "MEDIUM"),
"/fine-jewellery/necklaces/pendant-necklace": ("Diamond Pendant Necklaces",
    "Shop diamond pendant necklaces in bezel, marquise and sculptural designs.",
    "Diamond Pendant Necklaces",
    "Intro to the pendant styles actually present; chain-length guidance by link. 3 products (inventory watch); disjoint from the solitaire and T-bar sets.",
    "EDU-RJG-NL, BC-006", "'solitaire' qualified terms → solitaire child; T-bar → /t-bar.", "MEDIUM"),
"/fine-jewellery/necklaces/charm-necklace": ("Diamond Charm Necklaces",
    "Shop diamond charm necklaces: small, meaningful pendants on a fine chain.",
    "Diamond Charm Necklaces",
    "Intro: what 'charm necklace' means in this catalog; gifting framing; link BC-004/BC-008 when live.",
    "BC-004, BC-008 when live", "—", "MEDIUM"),
"/fine-jewellery/necklaces/multi-stone": ("Multi-Stone Diamond Necklaces",
    "Shop multi-stone diamond necklaces that combine several diamond cuts in one design.",
    "Multi-Stone Diamond Necklaces",
    "Intro on multi-stone designs; link the shapes guide EDU-SHP-00. Normalize the visible name 'Multi stone' → 'Multi-Stone'. No keyword assigned (no measured demand).",
    "EDU-SHP-00", "Navigational listing.", "MEDIUM"),
"/fine-jewellery/necklaces/lariat-necklace": ("Diamond Lariat Necklaces",
    "Shop diamond lariat necklaces with a drop-through design.",
    "Diamond Lariat Necklaces",
    "Define lariat (chain passes through a loop / ends hang free); styling note; link BC-006 layering when live. Inventory watch: 1 product.",
    "BC-006 when live", "—", "MEDIUM"),
"/fine-jewellery/necklaces/toi-et-moi": ("Toi et Moi Diamond Necklaces",
    "Shop toi et moi diamond necklaces that pair two cuts in one pendant.",
    "Toi et Moi Diamond Necklaces",
    "Explain 'toi et moi' pendant; differentiate from the ring page; fix the visible name 'Toi-et moi'. No keyword assigned.",
    "EDU-SHP-00", "Keeps 'necklace' in title/H1; ring-intent toi et moi heads belong to the ring child (OD-16).", "MEDIUM"),
"/fine-jewellery/bracelet/tennis": ("Diamond Tennis Bracelets",
    "Shop diamond tennis bracelets: a continuous line of diamonds set around the wrist.",
    "Diamond Tennis Bracelets",
    "Define tennis bracelet in one sentence; how to choose (total carat weight, length/fit, clasp safety — generally accepted); link the bracelet size chart (EDU-RJG-BR) and BC-021 'what is a tennis bracelet' when live.",
    "EDU-RJG-BR, BC-021", "Child owns the commercial head 'tennis bracelet' (135,000); BC-021 stays informational ('what is a tennis bracelet' 3,600). Merchandising check (F-E7): some listed items are named link bracelets (e.g. 'Solara Loop Round Diamond Link Bracelet').", "HIGH"),
"/fine-jewellery/bracelet/bangles": ("Diamond Link Bracelets",
    "Shop House of Diams diamond link bracelets in open-link designs set with pavé diamonds.",
    "Diamond Link Bracelets",
    "INTERIM, SCOPED TO THE CURRENT CONTENTS (apply only after F-E7): a short intro on diamond link bracelets only (what a link bracelet is; wrist-size note → EDU-RJG-BR). Do NOT write 'bangle', 'cuff' or 'bangle bracelet' in the title, H1, intro or anchors — the 2 listed products are both named link bracelets and no product in the catalog is described as a bangle. Re-check the wording against the category contents at implementation time.",
    "EDU-RJG-BR", "HELD — taxonomy (F-E7): no keyword assigned; 'gold bangles' (27,100) considered and not adopted (metal-led, no bangle products). Product sets of /bangles (2), /chain-link (1) and /tennis (8) are disjoint (crawl 2026-10-09), but /bangles and /chain-link are both link/chain-style, so their scope overlaps until HOD confirms the taxonomy.", "MEDIUM"),
"/fine-jewellery/bracelet/chain-link": ("Diamond Chain & Link Bracelets",
    "Shop diamond chain and link bracelets from House of Diams.",
    "Diamond Chain & Link Bracelets",
    "Short intro on chain/link designs; sizing note → EDU-RJG-BR. Normalize the visible name 'chain & Link'. Inventory watch: 1 product (Rosette Five-Flower Bracelet, a chain bracelet). Contents check (crawl 2026-10-09): no product overlap with /bracelet/bangles or /bracelet/tennis.",
    "EDU-RJG-BR", "Naming overlaps in scope with /bracelet/bangles (link bracelets) — one home per product; shared taxonomy question F-E7. No product is listed on both pages.", "MEDIUM"),
}

# Category label vs contents mismatch (correction pass 2026-10-10): the visible name 'Bangles' is not supported by the 2 listed products (both link bracelets).
HOLD_TAXONOMY = {
    "/fine-jewellery/bracelet/bangles": dict(
        name="Diamond Link Bracelets (category currently labeled 'Bangles')",
        related="diamond link bracelet; pavé link bracelet; wrist size and fit; metal options",
        cann="LOW on product overlap (0 shared products with /chain-link and /tennis); scope overlaps with /bracelet/chain-link until F-E7 is answered",
        tact="HOLD — interim wording scoped to the current contents (link bracelets); apply only after F-E7. Replaces the unsupported 'Link & Bangle' wording",
        mact="HOLD — interim wording; no bangle claim",
        hact="HOLD — interim wording; keep the visible name 'Bangles' only if HOD confirms bangle products",
        cact="HOLD — confirm taxonomy (F-E7), then ADD UNIQUE INTRO scoped to link bracelets",
        status="CONDITIONAL — PRODUCT/OFFER CONFIRMATION",
        deps=D(hod="F-E7 (blocking: bangle products vs the 'Bangles' label; rename or fold into Chain & Link)", eng="E-01, E-02, E-08"),
        dec="OD-01; OD-05",
        notes="HELD: label 'Bangles' vs 2 link bracelets (F-E7). Taxonomy not inferable from the catalog; interim wording is supported by the product records.",
        dep="Metadata/intro/schema via CMS or code (E-02, E-08) — only after HOD answers F-E7; no URL change."),
}

FOR_HIM = ("/wedding-bands/for-him", "/wedding-bands/for-him/classic", "/wedding-bands/for-him/diamonds", "/wedding-bands/for-him/designer",
           "/hiphop/chains", "/hiphop/chains/cuban-links")
EDOC = {e[0]: e for e in F.EMPTY}


def sub_row(path, s1):
    rid = "SUB:" + path
    if path in POP:
        t, m, h, outline, edu, bound, prio = POP[path]
        side = path.endswith("side-stone-rings")
        dup = path == "/wedding-bands/for-her"
        dec = "OD-01; OD-05"
        if side:
            dec = "OD-01; OD-05; OD-06"
        if any(k in path for k in ("eternity", "toi", "solitare", "pendant", "stud", "tennis")):
            dec += "; OD-16"
        deps = D(eng="E-01, E-02, E-08")
        if dup:
            deps = D(hod="F-E3 (men's range)", eng="E-01, E-05")
        if side:
            deps = D(eng="E-01, E-02, E-08", gsc="G-02 (non-blocking)")
        res = dict(
            title=t, tact=("HOLD — canonical to /wedding-bands; out of sitemap (OD-01/OD-16)" if dup else "REPLACE — FINAL" + (" (Stage 15 owner)" if side else " (keyword assigned under OD-01)")),
            meta=m, mact="HOLD" if dup else "REPLACE — FINAL", h1=h, hact="REPLACE — FINAL" + (" (user-facing label only)" if dup else " (current 'Explore X' pattern + typos inherited from category names)"),
            cact="CANONICAL + SITEMAP EXCLUSION" if dup else "ADD UNIQUE INTRO + CLEAN UP",
            sect=(outline if dup else ("Add a unique, short intro (guideline ~80–150 words, not a target): " + outline + " | Education links (Stage 16: category pages ≤5 Education links): " + edu +
                  " | Replace the boilerplate FAQ block (see schema). | Boundary: " + bound)),
            sch=SCH_CAT, sact="UPDATE (Class B)", aeo="NONE (listing) — informational questions belong to the Education owners linked above.", qs="—",
            geo="Keep category attributes (metal, stone type, shape) consistent with the PDPs' Product schema.", trust="No shipping/returns/certification claims until F-A1/F-A2/F-B1.",
            img=IMG_CAT, prio=prio, aws="B",
            dep="Metadata/intro/schema via CMS or code (E-02, E-08); visible-name typo fixes need the CMS category name only (no URL change)" + ("; ships together with the by-desgin→by-design 301 (R-08)" if side else "") + ".",
            dec=dec, status="READY FOR IMPLEMENTATION POST-AWS", deps=deps, notes=bound)
        if path in HOLD_TAXONOMY:
            res.update(HOLD_TAXONOMY[path])
        elif path == "/fine-jewellery/bracelet/chain-link":
            res["cann"] = ("MEDIUM — hub ('diamond bracelet') and child ('chain bracelet') own different heads (OD-01); scope overlaps with /bracelet/bangles "
                           "until F-E7 is answered (no product is listed on both)")
        return res
    ed = EDOC[path]
    note = ed[3]
    test = path.endswith("test-subcat")
    cond = path in FOR_HIM
    pr = {"/engagement-rings/round-rings": "HIGH", "/hiphop/test-subcat": "CRITICAL"}.get(path, "MEDIUM")
    return dict(
        title="— (no metadata work: " + ("test artifact — removed)" if test else "empty page, noindex until populated)"),
        tact="REMOVE (OD-07 adopted)" if test else "HOLD — noindex until populated (OD-07 adopted)",
        meta="— (none)", mact="HOLD", h1="— (none)", hact="HOLD",
        cact="REMOVE: 404/410, delete the record, out of sitemap" if test else "NOINDEX + REMOVE FROM SITEMAP/NAV",
        sect=("FINAL (OD-07): " + ed[1] + ". " + ed[2] + ". " + note + ". If populated later, run the D-07 gate (demand, SERP type, inventory, distinctness, one home, business fit, stability) before indexing; the keyword reserved for the page (if any) is in the keyword log."),
        sch="None — page is not indexable; if kept, BreadcrumbList only.", sact="NO CHANGE", aeo="NONE.", qs="—", geo="Remove from /llms.txt where listed.", trust="—", img="None while empty.",
        prio=pr, aws="B", dep="noindex/sitemap/nav rule (E-05, E-13); verify after AWS (Class C).", dec="OD-07" + ("; OD-08" if cond else ""),
        status="READY FOR IMPLEMENTATION POST-AWS",
        deps=D(hod="F-E3 (only if the range is later populated)" if cond else "", eng="E-01, E-05, E-13"), notes=note)
