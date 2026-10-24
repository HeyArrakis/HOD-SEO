# 03 — Title & Meta Optimization

Generated 2026-10-10. All values are **recommendations**; nothing was changed on the site. Companion data: `01-ON-PAGE-SEO-MASTER.csv` (columns *Recommended Title (pre-suffix value)*, *Rendered Title Preview*, *Rendered Length*, *Recommended Meta*, *Meta Length*, *Title/Meta Action*).

## 1. Brand-suffix verification (required before writing titles)

Read-only GET on 2026-10-09 (Step 2):

| URL | og:title | <title> |
|---|---|---|
| / | Lab-Grown Diamond Engagement Rings & Fine Jewellery | Lab-Grown Diamond Engagement Rings & Fine Jewellery (no suffix) |
| /engagement-rings | Engagement Rings | Engagement Rings \| House of Diams |
| /bespoke | Bespoke | Bespoke \| House of Diams |
| /shop/adeline-round-solitaire-stud-earrings | Adeline 2 CTW Round Diamond Solitaire Stud Earrings | … \| House of Diams |
| /blog/lab-grown-vs-natural-diamonds-the-honest-comparison-house-of-diams | Lab-Grown vs Natural Diamonds: The Honest Comparison | … \| House of Diams |

**Rule:** enter the *pre-suffix* value; the template adds ` | House of Diams` (17 characters). So a rendered title of ≤60 characters needs a pre-suffix value of ≤~43. Homepage is the exception (absolute title, brand written into the value). The About, Contact and Privacy rows are worded so the brand is not repeated.

## 2. Title rules applied

1. One primary topic per title, matching the page's owner and search intent; no exact-match forcing; no stacked keywords.
2. Unique across the set (automated check: 0 duplicates among 107 recommended rendered titles).
3. Front-load the distinguishing words; ≤~60 rendered characters is a **display guideline** — 23 rows exceed it (listed in §7); those are live titles kept deliberately (key terms front-loaded) or approved package values.
4. American English is the confirmed rule (OD-05 adopted): jewelry, color, center, customize. Slugs such as `/fine-jewellery/` are never changed — only visible names, titles, metas, H1s and anchors.
5. **Commercial and Education titles are FINAL**: keyword ownership was resolved on 2026-10-10 (`10-DECISIONS-RESOLUTION-LOG.md`, `10-COMMERCIAL-KEYWORD-ASSIGNMENTS.csv`). Live changes on ranking-equity URLs still wait for the GSC baseline (see Status).
6. No shipping, returns, warranty, certification, "free" or "best/cheapest" wording anywhere.

## 3. Meta-description rules applied

Accurate to the page, answer-first where the page answers a question, one clear value statement, no keyword stuffing, no unverified promises, written for US searchers, unique. ~120–160 characters is a display guideline only. Where a page cannot yet support a promise (e.g. /returns has no terms) the meta is deliberately neutral.

### Step 1 draft claims removed

| Step 1 draft (QA/05) | Why not adopted | Treatment |
|---|---|---|
| …with free insured worldwide delivery (home, shop, categories, subcategories) | Shipping/insurance terms are an open business fact (progress.md); /shipping is a placeholder | Removed from every meta |
| …how our 15-day returns work (/returns) | No return terms exist on the page; '15-Day' unconfirmed | Neutral meta; policy to be written first |
| Family-Run Diamond Jewellery Makers, Surat / in the trade since 2014 (/about) | Founding year / family-run / Surat are published on-site but not in the confirmed-facts list | Generic About meta; facts added only after HOD confirms |
| Free design consultation and CAD sketch (/bespoke) | Page claim, unconfirmed | Meta describes the inquiry, not the offer terms |
| …in 10K gold (categories/subcategories) | Inventory claim that can drift; PDP metal lists show 10K and 14K | Metal omitted at category level |
| Lab-grown positioning in hub metas (e.g. /engagement-rings) | OD-02 adopted: no separate lab-grown hub; origin stated at product level until F-E1 | Origin-neutral hub metas; origin stated at PDP level where the product record says so |

## 4. Live pages — titles

| Row | Current title | Recommended (pre-suffix) | Rendered len | Action | Status |
|---|---|---|---|---|---|
| NAV-HOME | Lab-Grown Diamond Engagement Rings & Fine Jewellery | House of Diams \| Luxury Diamond Jewelry & Bespoke Rings | 55 | REPLACE — FINAL (brand-led; origin-neutral per OD-02) | READY FOR IMPLEMENTATION POST-AWS |
| COM-SHOP | Shop \| House of Diams | Shop All Diamond Jewelry | 41 | REPLACE — FINAL | READY FOR IMPLEMENTATION POST-AWS |
| COM-COLLECTION | Collection \| House of Diams | — (no metadata work: empty page) |  | HOLD — noindex until populated (OD-07 adopted) | READY FOR IMPLEMENTATION POST-AWS |
| COM-BESPOKE | Bespoke \| House of Diams | Custom Engagement Rings & Bespoke Jewelry | 58 | REPLACE — FINAL (assigned: 'custom engagement ring') | READY FOR IMPLEMENTATION POST-AWS |
| BRAND-ABOUT | About \| House of Diams | Our Story & Values | 35 | REPLACE — NEUTRAL INTERIM ('About House of Diams' would repeat the br… | HOD INPUT REQUIRED |
| BRAND-CONTACT | House of Diams | Contact Us | 27 | CREATE — FINAL (OD-09 adopted: real /contact page) | HOD INPUT REQUIRED |
| SUP-FAQ | FAQ \| House of Diams | FAQs: Orders, Shipping, Returns & Diamonds | 59 | REPLACE — FINAL | READY FOR IMPLEMENTATION POST-AWS |
| SUP-POLICIES-SHIP | Shipping \| House of Diams | Shipping & Delivery | 36 | REPLACE — FINAL | HOD INPUT REQUIRED |
| SUP-POLICIES-RET | Returns \| House of Diams | Returns & Exchanges | 36 | REPLACE — FINAL (apply when the policy is published) | HOD INPUT REQUIRED |
| SUP-POLICIES-PRIV | Privacy Policy \| House of Diams | Privacy Policy | 31 | KEEP (current 'Privacy Policy \| House of Diams' is correct) | NO CHANGE REQUIRED |
| SUP-POLICIES-TERMS | Terms & Conditions \| House of Diams | Terms & Conditions | 35 | KEEP | NO CHANGE REQUIRED |
| BLOG-HUB | Blog \| House of Diams | Blog: Jewelry Gift Ideas, Style & Stories | 58 | REPLACE — FINAL (OD-12: section name is 'Blog'; current title is just… | READY FOR IMPLEMENTATION POST-AWS |
| EDU-ROOT | Education \| House of Diams | Diamond Guides: 4Cs, Lab-Grown & Metals | 56 | REPLACE — FINAL | READY FOR IMPLEMENTATION POST-AWS |
| COM-ER | Engagement Rings \| House of Diams | Diamond Engagement Rings: Halo & Solitaire | 59 | REPLACE — FINAL (keyword assigned under OD-01) | READY FOR IMPLEMENTATION POST-AWS |
| COM-WB | Wedding Bands \| House of Diams | Diamond Wedding Bands: Eternity & More | 55 | REPLACE — FINAL (keyword assigned under OD-01) | READY FOR IMPLEMENTATION POST-AWS |
| COM-FJ | Fine Jewellery \| House of Diams | Fine Diamond Jewelry Collection | 48 | REPLACE — FINAL (keyword assigned under OD-01) | READY FOR IMPLEMENTATION POST-AWS |
| COM-FJ-EARRINGS | Earrings \| Fine Jewellery \| House of Diams | Diamond Earrings: Studs, Hoops & Drops | 55 | REPLACE — FINAL (keyword assigned under OD-01) | READY FOR IMPLEMENTATION POST-AWS |
| COM-FJ-NECKLACES | Necklaces \| Fine Jewellery \| House of Diams | Diamond Necklaces & Pendants | 45 | REPLACE — FINAL (keyword assigned under OD-01) | READY FOR IMPLEMENTATION POST-AWS |
| COM-FJ-BRACELETS | Bracelet \| Fine Jewellery \| House of Diams | Diamond Bracelets: Chain, Link & Tennis | 56 | REPLACE — FINAL (keyword assigned under OD-01) | READY FOR IMPLEMENTATION POST-AWS |
| COM-FJ-RINGS | Rings \| Fine Jewellery \| House of Diams | Diamond Statement & Fashion Rings | 50 | REPLACE — FINAL (keyword assigned under OD-01) | READY FOR IMPLEMENTATION POST-AWS |
| COM-CURATED-TBAR | T- BAR \| House of Diams | T-Bar Necklaces & Pendants | 43 | REPLACE — FINAL (keyword assigned under OD-01) | READY FOR IMPLEMENTATION POST-AWS |
| COM-ER-STYLES-GROUP | By Design \| Engagement Rings \| House of Diams | — (no metadata work: canonicalized to /engagement-rings) |  | HOLD — canonical to /engagement-rings (OD-06 adopted) | READY FOR IMPLEMENTATION POST-AWS |
| COM-PDP | Pattern: '<Product name> \| House of Diams' (184 crawled; 65… | {Shape} {Product type}, {Carat} ct — see 07-PDP-ON-PAGE-SEO.md for the template |  | TEMPLATE RULE (not a per-page edit) | READY FOR IMPLEMENTATION POST-AWS |
| COM-PDP-OVAL-FLORAL | Oval Marquise Side-Stone Engagement Ring \| House of Diams | 2.5 ct Oval Marquise Diamond Engagement Ring | 61 | REPLACE — FINAL (OD-15); apply only after the GSC baseline (ranking U… | GSC BASELINE REQUIRED |

## 5. Commercial subcategories — titles (40 rows; empty/test pages are HELD)

| Row | Current title | Recommended (pre-suffix) | Rendered len | Action | Status |
|---|---|---|---|---|---|
| /engagement-rings/by-design/side-stone-rings | Side Stone Rings \| Engagement Rings \| House of Diams | Side-Stone Engagement Rings | 44 | REPLACE — FINAL (Stage 15 owner) | READY FOR IMPLEMENTATION POST-AWS |
| /engagement-rings/by-design/solitare-rings | Solitare Rings \| Engagement Rings \| House of Diams | Solitaire Engagement Rings | 43 | REPLACE — FINAL (keyword assigned under OD-01) | READY FOR IMPLEMENTATION POST-AWS |
| /engagement-rings/by-design/halo-ring | Halo Ring \| Engagement Rings \| House of Diams | Halo Engagement Rings | 38 | REPLACE — FINAL (keyword assigned under OD-01) | READY FOR IMPLEMENTATION POST-AWS |
| /engagement-rings/by-design/toi-moi-rings | Toi-moi Rings \| Engagement Rings \| House of Diams | Toi et Moi Engagement Rings | 44 | REPLACE — FINAL (keyword assigned under OD-01) | READY FOR IMPLEMENTATION POST-AWS |
| /engagement-rings/by-design/pave | Pavé Rings \| Engagement Rings \| House of Diams | Pavé Engagement Rings | 38 | REPLACE — FINAL (keyword assigned under OD-01) | READY FOR IMPLEMENTATION POST-AWS |
| /engagement-rings/by-design/nature-inspired-rings | Nature Inspired Rings \| Engagement Rings \| House of Diams | Nature-Inspired Engagement Rings | 49 | REPLACE — FINAL (keyword assigned under OD-01) | READY FOR IMPLEMENTATION POST-AWS |
| /engagement-rings/by-design/three-stone-rings | Three Stone Rings \| Engagement Rings \| House of Diams | Three-Stone Engagement Rings | 45 | REPLACE — FINAL (keyword assigned under OD-01) | READY FOR IMPLEMENTATION POST-AWS |
| /engagement-rings/by-design/bezel-rings | Bezel Rings \| Engagement Rings \| House of Diams | Bezel Engagement Rings | 39 | REPLACE — FINAL (keyword assigned under OD-01) | READY FOR IMPLEMENTATION POST-AWS |
| /engagement-rings/round-rings | Round rings \| Engagement Rings \| House of Diams | — (no metadata work: empty page, noindex until populated) |  | HOLD — noindex until populated (OD-07 adopted) | READY FOR IMPLEMENTATION POST-AWS |
| /wedding-bands/for-her | For Her \| Wedding Bands \| House of Diams | — (canonical to /wedding-bands) |  | HOLD — canonical to /wedding-bands; out of sitemap (OD-01/OD-16) | READY FOR IMPLEMENTATION POST-AWS |
| /wedding-bands/for-him | For Him \| Wedding Bands \| House of Diams | — (no metadata work: empty page, noindex until populated) |  | HOLD — noindex until populated (OD-07 adopted) | READY FOR IMPLEMENTATION POST-AWS |
| /wedding-bands/for-her/nature | Nature \| Wedding Bands \| House of Diams | — (no metadata work: empty page, noindex until populated) |  | HOLD — noindex until populated (OD-07 adopted) | READY FOR IMPLEMENTATION POST-AWS |
| /wedding-bands/for-her/solid | solid \| Wedding Bands \| House of Diams | — (no metadata work: empty page, noindex until populated) |  | HOLD — noindex until populated (OD-07 adopted) | READY FOR IMPLEMENTATION POST-AWS |
| /wedding-bands/for-her/cigar-band | Cigar Band \| Wedding Bands \| House of Diams | — (no metadata work: empty page, noindex until populated) |  | HOLD — noindex until populated (OD-07 adopted) | READY FOR IMPLEMENTATION POST-AWS |
| /wedding-bands/for-her/eternity | Eternity \| Wedding Bands \| House of Diams | Diamond Eternity Bands & Rings for Women | 57 | REPLACE — FINAL (keyword assigned under OD-01) | READY FOR IMPLEMENTATION POST-AWS |
| /wedding-bands/for-her/anniversay | Anniversay \| Wedding Bands \| House of Diams | Diamond Anniversary Rings & Bands | 50 | REPLACE — FINAL (keyword assigned under OD-01) | READY FOR IMPLEMENTATION POST-AWS |
| /wedding-bands/for-her/pavee | pavé \| Wedding Bands \| House of Diams | — (no metadata work: empty page, noindex until populated) |  | HOLD — noindex until populated (OD-07 adopted) | READY FOR IMPLEMENTATION POST-AWS |
| /wedding-bands/for-him/classic | Classic \| Wedding Bands \| House of Diams | — (no metadata work: empty page, noindex until populated) |  | HOLD — noindex until populated (OD-07 adopted) | READY FOR IMPLEMENTATION POST-AWS |
| /wedding-bands/for-him/diamonds | Diamonds \| Wedding Bands \| House of Diams | — (no metadata work: empty page, noindex until populated) |  | HOLD — noindex until populated (OD-07 adopted) | READY FOR IMPLEMENTATION POST-AWS |
| /wedding-bands/for-him/designer | Designer \| Wedding Bands \| House of Diams | — (no metadata work: empty page, noindex until populated) |  | HOLD — noindex until populated (OD-07 adopted) | READY FOR IMPLEMENTATION POST-AWS |
| /fine-jewellery/earrings/stud-earrings | Stud Earrings \| Fine Jewellery \| House of Diams | Diamond Stud Earrings | 38 | REPLACE — FINAL (keyword assigned under OD-01) | READY FOR IMPLEMENTATION POST-AWS |
| /fine-jewellery/earrings/hoops-huggies | Hoops & Huggies \| Fine Jewellery \| House of Diams | Diamond Hoop & Huggie Earrings | 47 | REPLACE — FINAL (keyword assigned under OD-01) | READY FOR IMPLEMENTATION POST-AWS |
| /fine-jewellery/earrings/drop-dangle | Drop & Dangle \| Fine Jewellery \| House of Diams | Diamond Drop & Dangle Earrings | 47 | REPLACE — FINAL (keyword assigned under OD-01) | READY FOR IMPLEMENTATION POST-AWS |
| /fine-jewellery/earrings/tennis-earrings | Tennis Earrings \| Fine Jewellery \| House of Diams | — (no metadata work: empty page, noindex until populated) |  | HOLD — noindex until populated (OD-07 adopted) | READY FOR IMPLEMENTATION POST-AWS |
| /fine-jewellery/earrings/personalized-charm | Personalized & Charm \| Fine Jewellery \| House of Diams | — (no metadata work: empty page, noindex until populated) |  | HOLD — noindex until populated (OD-07 adopted) | READY FOR IMPLEMENTATION POST-AWS |
| /fine-jewellery/necklaces/solitare | Solitare \| Fine Jewellery \| House of Diams | Diamond Solitaire Necklaces | 44 | REPLACE — FINAL (keyword assigned under OD-01) | READY FOR IMPLEMENTATION POST-AWS |
| /fine-jewellery/necklaces/pendant-necklace | Pendant Necklace \| Fine Jewellery \| House of Diams | Diamond Pendant Necklaces | 42 | REPLACE — FINAL (keyword assigned under OD-01) | READY FOR IMPLEMENTATION POST-AWS |
| /fine-jewellery/necklaces/charm-necklace | Charm Necklace \| Fine Jewellery \| House of Diams | Diamond Charm Necklaces | 40 | REPLACE — FINAL (keyword assigned under OD-01) | READY FOR IMPLEMENTATION POST-AWS |
| /fine-jewellery/necklaces/multi-stone | Multi stone \| Fine Jewellery \| House of Diams | Multi-Stone Diamond Necklaces | 46 | REPLACE — FINAL (keyword assigned under OD-01) | READY FOR IMPLEMENTATION POST-AWS |
| /fine-jewellery/necklaces/lariat-necklace | Lariat Necklace \| Fine Jewellery \| House of Diams | Diamond Lariat Necklaces | 41 | REPLACE — FINAL (keyword assigned under OD-01) | READY FOR IMPLEMENTATION POST-AWS |
| /fine-jewellery/necklaces/toi-et-moi | Toi-et moi \| Fine Jewellery \| House of Diams | Toi et Moi Diamond Necklaces | 45 | REPLACE — FINAL (keyword assigned under OD-01) | READY FOR IMPLEMENTATION POST-AWS |
| /fine-jewellery/necklaces/tennis-necklace | Tennis Necklace \| Fine Jewellery \| House of Diams | — (no metadata work: empty page, noindex until populated) |  | HOLD — noindex until populated (OD-07 adopted) | READY FOR IMPLEMENTATION POST-AWS |
| /fine-jewellery/necklaces/initials | Initials \| Fine Jewellery \| House of Diams | — (no metadata work: empty page, noindex until populated) |  | HOLD — noindex until populated (OD-07 adopted) | READY FOR IMPLEMENTATION POST-AWS |
| /fine-jewellery/bracelet/tennis | Tennis \| Fine Jewellery \| House of Diams | Diamond Tennis Bracelets | 41 | REPLACE — FINAL (keyword assigned under OD-01) | READY FOR IMPLEMENTATION POST-AWS |
| /fine-jewellery/bracelet/bangles | Bangles \| Fine Jewellery \| House of Diams | Diamond Link Bracelets | 39 | HOLD — interim wording scoped to the current contents (link bracelets… | CONDITIONAL — PRODUCT/OFFER CONFIRMATION |
| /fine-jewellery/bracelet/chain-link | chain & Link \| Fine Jewellery \| House of Diams | Diamond Chain & Link Bracelets | 47 | REPLACE — FINAL (keyword assigned under OD-01) | READY FOR IMPLEMENTATION POST-AWS |
| /fine-jewellery/rings/eternity-rings | Eternity Rings \| Fine Jewellery \| House of Diams | — (no metadata work: empty page, noindex until populated) |  | HOLD — noindex until populated (OD-07 adopted) | READY FOR IMPLEMENTATION POST-AWS |
| /hiphop/chains | Chains \| hiphop \| House of Diams | — (no metadata work: empty page, noindex until populated) |  | HOLD — noindex until populated (OD-07 adopted) | READY FOR IMPLEMENTATION POST-AWS |
| /hiphop/chains/cuban-links | Cuban Links \| hiphop \| House of Diams | — (no metadata work: empty page, noindex until populated) |  | HOLD — noindex until populated (OD-07 adopted) | READY FOR IMPLEMENTATION POST-AWS |
| /hiphop/test-subcat | test subcat \| hiphop \| House of Diams | — (no metadata work: test artifact — removed) |  | REMOVE (OD-07 adopted) | READY FOR IMPLEMENTATION POST-AWS |

## 6. Existing Education articles — titles

| Row | Current title | Recommended (pre-suffix) | Rendered len | Action | Status |
|---|---|---|---|---|---|
| EDU-LG-03 | CVD vs HPHT Lab-Grown Diamonds: What Buyers Should Know \| H… | CVD vs HPHT Lab-Grown Diamonds: What Buyers Should Know | 72 | KEEP — already aligned with 'hpht vs cvd'; 19 ranked keywords (best D… | GSC BASELINE REQUIRED |
| EDU-LG-02 | Lab-Grown vs Natural Diamonds: The Honest Comparison \| Hous… | Lab-Grown vs Natural Diamonds: The Honest Comparison | 69 | KEEP — aligned with 'lab grown vs natural diamonds'; ranking-equity U… | GSC BASELINE REQUIRED |
| EDU-MET-01 | 14K vs 18K Gold for Diamond Jewellery: Which Is Better? \| H… | 14K vs 18K Gold (and 10K) for Diamond Jewelry | 62 | REPLACE — FINAL (OD-03 resolved; US spelling OD-05); apply only after… | GSC BASELINE REQUIRED |
| EDU-LG-10 | How to Choose a Lab-Grown Diamond: The Complete Buyer’s Gui… | How to Choose a Lab-Grown Diamond: The Complete Buyer's Guide | 78 | KEEP — aligned with 'how to choose a lab grown diamond' (est. pos 35)… | GSC BASELINE REQUIRED |
| EDU-LG-01 | Are Lab-Grown Diamonds Real? A Complete Buyer’s Guide \| Hou… | Are Lab-Grown Diamonds Real? A Complete Buyer's Guide | 70 | KEEP — already aligned with 'are lab grown diamonds real' (14,800) [r… | READY FOR IMPLEMENTATION POST-AWS |
| EDU-4C-00 | The 4Cs of Lab-Grown Diamonds Explained: Cut, Colour, Clari… | The 4Cs of Diamonds Explained | 46 | REPLACE — FINAL (OD-03 resolved). Current: 'The 4Cs of Lab-Grown Diam… | READY FOR IMPLEMENTATION POST-AWS |
| EXIST-BLOG-ER-ONLINE | How to Choose a Lab-Grown Diamond Engagement Ring Online \| … | How to Choose a Lab-Grown Diamond Engagement Ring Online | 73 | KEEP — no on-page change in this phase (OD-13 adopted) [rendered 73 c… | NO CHANGE REQUIRED |
| EDU-SHP-00 | The Best Lab-Grown Diamond Shapes for Engagement Rings \| Ho… | Diamond Shapes: Chart and How to Choose | 56 | REPLACE — FINAL (OD-03 resolved). Current: 'The Best Lab-Grown Diamon… | READY FOR IMPLEMENTATION POST-AWS |
| EDU-RJG-02 | How to Find Your Ring Size at Home: Complete Ring Size Guid… | Ring Size Chart: How to Measure Your Size | 58 | REPLACE — FINAL (OD-03 resolved). Current: 'How to Find Your Ring Siz… | READY FOR IMPLEMENTATION POST-AWS |
| EDU-CERT-00 | IGI Certification for Lab-Grown Diamonds: What It Means \| H… | What a Lab-Grown Diamond Certificate Shows | 59 | REPLACE — ships TOGETHER with EDU-CERT-01 (Stage 13 RETARGET). Curren… | READY FOR IMPLEMENTATION POST-AWS |
| EDU-CERT-01 | Lab-Grown Diamond Certification Explained: GIA vs IGI \| Hou… | GIA vs IGI Lab-Grown Diamond Certification | 59 | REPLACE — ships TOGETHER with EDU-CERT-00. Current 'Lab-Grown Diamond… | READY FOR IMPLEMENTATION POST-AWS |

(Existing ranking-equity URLs keep their titles; changes need a GSC baseline. EDU-CERT-00 and EDU-CERT-01 change together.)

### Planned Education pages — final draft titles (primary keyword ratified under OD-03/OD-04)

| Row | Current title | Recommended (pre-suffix) | Rendered len | Action | Status |
|---|---|---|---|---|---|
| EDU-LG-00 | NOT LIVE — page does not exist | What Are Lab-Grown Diamonds? | 45 | FINAL — primary ratified 2026-10-10 (OD-03); adjust only if the writt… | PRE-AWS PREPARATION |
| EDU-LG-05 | NOT LIVE — page does not exist | Do Lab-Grown Diamonds Hold Their Value? | 56 | FINAL — primary ratified 2026-10-10 (owner confirmed); adjust only if… | PRE-AWS PREPARATION |
| EDU-LG-07 | NOT LIVE — page does not exist | Are Lab-Grown Diamonds Ethical? | 48 | FINAL — primary ratified 2026-10-10 (owner confirmed); adjust only if… | PRE-AWS PREPARATION |
| EDU-LG-08 | NOT LIVE — page does not exist | Do Lab-Grown Diamonds Get Cloudy? | 50 | FINAL — primary ratified 2026-10-10 (owner confirmed); adjust only if… | PRE-AWS PREPARATION |
| EDU-LG-09 | NOT LIVE — page does not exist | How to Tell If a Diamond Is Real | 49 | FINAL — primary ratified 2026-10-10 (OD-03); adjust only if the writt… | PRE-AWS PREPARATION |
| EDU-NAT-00 | NOT LIVE — page does not exist | How Are Diamonds Formed? | 41 | FINAL — primary ratified 2026-10-10 (owner confirmed); adjust only if… | PRE-AWS PREPARATION |
| EDU-4C-01 | NOT LIVE — page does not exist | Diamond Clarity Chart: FL to I3 Explained | 58 | FINAL — primary ratified 2026-10-10 (OD-03); adjust only if the writt… | PRE-AWS PREPARATION |
| EDU-4C-02 | NOT LIVE — page does not exist | SI Clarity Diamonds: SI1 vs SI2 Explained | 58 | FINAL — primary ratified 2026-10-10 (owner confirmed); adjust only if… | PRE-AWS PREPARATION |
| EDU-4C-03 | NOT LIVE — page does not exist | VVS Diamonds: VVS1 vs VVS2 Explained | 53 | FINAL — primary ratified 2026-10-10 (OD-03); adjust only if the writt… | PRE-AWS PREPARATION |
| EDU-4C-05 | NOT LIVE — page does not exist | Diamond Color Scale: D-to-Z Chart | 50 | FINAL — primary ratified 2026-10-10 (OD-03); adjust only if the writt… | PRE-AWS PREPARATION |
| EDU-4C-06 | NOT LIVE — page does not exist | Diamond Cut: Grades, Cut vs Shape and Sparkle | 62 | FINAL — primary ratified 2026-10-10 (OD-03); adjust only if the writt… | PRE-AWS PREPARATION |
| EDU-4C-07 | NOT LIVE — page does not exist | Diamond Carat Size Chart by Shape | 50 | FINAL — primary ratified 2026-10-10 (OD-03); adjust only if the writt… | PRE-AWS PREPARATION |
| EDU-MET-00 | NOT LIVE — page does not exist | Jewelry Metals Guide: White Gold vs Platinum | 61 | FINAL — primary ratified 2026-10-10 (OD-03); adjust only if the writt… | PRE-AWS PREPARATION |
| EDU-RJG-01 | NOT LIVE — page does not exist | Engagement Ring Settings Guide | 47 | FINAL — primary ratified 2026-10-10 (OD-04); adjust only if the writt… | PRE-AWS PREPARATION |
| EDU-GEN-01 | NOT LIVE — page does not exist | What Are Diamonds Made Of? | 43 | FINAL — primary ratified 2026-10-10 (owner confirmed); adjust only if… | PRE-AWS PREPARATION |
| EDU-RJG-03 | NOT LIVE — page does not exist | How to Clean a Diamond Ring at Home | 52 | FINAL — primary ratified 2026-10-10 (OD-04); adjust only if the writt… | PRE-AWS PREPARATION |
| EDU-RJG-BR | NOT LIVE — page does not exist | Bracelet Size Chart: How to Measure Your Wrist | 63 | FINAL — primary ratified 2026-10-10 (OD-04); adjust only if the writt… | PRE-AWS PREPARATION |
| EDU-RJG-NL | NOT LIVE — page does not exist | Necklace Length Chart: Find Your Length | 56 | FINAL — primary ratified 2026-10-10 (OD-04); adjust only if the writt… | PRE-AWS PREPARATION |
| EDU-INS | NOT LIVE — page does not exist | Engagement Ring Insurance: Is It Worth It? | 59 | FINAL — primary ratified 2026-10-10 (OD-04); adjust only if the writt… | PRE-AWS PREPARATION |
| EDU-WB-GUIDE | NOT LIVE — page does not exist | How to Choose a Wedding Band | 45 | FINAL — primary ratified 2026-10-10 (OD-04); adjust only if the writt… | PRE-AWS PREPARATION |
| BLOG-WR-TYPES | NOT LIVE — page does not exist | Types of Wedding Rings: Band Styles Explained | 62 | DRAFT — finalize when the article is written (re-homed to Education —… | PRE-AWS PREPARATION |

### Planned Blog posts — titles (10 approved package values carried unchanged; 23 drafts)

| Row | Current title | Recommended (pre-suffix) | Rendered len | Action | Status |
|---|---|---|---|---|---|
| BC-001 | NOT LIVE — page does not exist | How Long Does a Custom Engagement Ring Take? | 61 | CARRY APPROVED VALUE (package unedited) — PUBLICATION HELD pending F-… | HOD INPUT REQUIRED |
| BC-004 | NOT LIVE — page does not exist | Christmas Jewelry Gifts: A Holiday Gift Guide | 62 | CARRY APPROVED (package value; set in the CMS 'Article Title'; templa… | READY FOR IMPLEMENTATION POST-AWS |
| BC-035 | NOT LIVE — page does not exist | 10 Year Anniversary Gift Ideas: Tin and Diamond | 64 | CARRY APPROVED (package value; set in the CMS 'Article Title'; templa… | READY FOR IMPLEMENTATION POST-AWS |
| BC-018 | NOT LIVE — page does not exist | Anniversary Gifts by Year: Traditional and Modern | 66 | CARRY APPROVED (package value; set in the CMS 'Article Title'; templa… | READY FOR IMPLEMENTATION POST-AWS |
| BC-036 | NOT LIVE — page does not exist | What Finger Does a Wedding Ring Go On? | 55 | CARRY APPROVED (package value; set in the CMS 'Article Title'; templa… | READY FOR IMPLEMENTATION POST-AWS |
| BC-006 | NOT LIVE — page does not exist | Necklace Layering: How to Layer Necklaces | 58 | CARRY APPROVED (package value; set in the CMS 'Article Title'; templa… | READY FOR IMPLEMENTATION POST-AWS |
| BC-008 | NOT LIVE — page does not exist | Meaningful Jewelry Gifts for Your Wife | 55 | CARRY APPROVED (package value; set in the CMS 'Article Title'; templa… | READY FOR IMPLEMENTATION POST-AWS |
| BC-009 | NOT LIVE — page does not exist | Jewelry Gifts for Your Girlfriend: Diamond Ideas | 65 | CARRY APPROVED (package value; set in the CMS 'Article Title'; templa… | READY FOR IMPLEMENTATION POST-AWS |
| BC-003 | NOT LIVE — page does not exist | Push Present: What It Is and Jewelry Ideas | 59 | CARRY APPROVED (package value; set in the CMS 'Article Title'; templa… | READY FOR IMPLEMENTATION POST-AWS |
| BC-007 | NOT LIVE — page does not exist | How to Wear an Engagement Ring and Wedding Band | 64 | CARRY APPROVED (package value; set in the CMS 'Article Title'; templa… | READY FOR IMPLEMENTATION POST-AWS |
| BC-011 | NOT LIVE — page does not exist | What Is a Promise Ring? Meaning and Ideas | 58 | DRAFT — finalize when the article is written | PRE-AWS PREPARATION |
| BC-037 | NOT LIVE — page does not exist | Engagement Ring vs Wedding Ring: The Difference | 64 | DRAFT — finalize when the article is written | PRE-AWS PREPARATION |
| BC-014 | NOT LIVE — page does not exist | Proposal Ideas: How to Plan a Memorable Proposal | 65 | DRAFT — finalize when the article is written | PRE-AWS PREPARATION |
| BC-015 | NOT LIVE — page does not exist | Where Are Lab-Grown Diamonds Made? | 51 | DRAFT — finalize when the article is written | HOD INPUT REQUIRED |
| BC-024 | NOT LIVE — page does not exist | How Much Should an Engagement Ring Cost? | 57 | DRAFT — finalize when the article is written | PRE-AWS PREPARATION |
| BC-016 | NOT LIVE — page does not exist | When Is Engagement Season? | 43 | DRAFT — finalize when the article is written | PRE-AWS PREPARATION |
| BC-017 | NOT LIVE — page does not exist | Christmas and New Year's Eve Proposal Ideas | 60 | DRAFT — finalize when the article is written | PRE-AWS PREPARATION |
| BC-005 | NOT LIVE — page does not exist | How Diamonds Are Cut and Polished | 50 | DRAFT — finalize when the article is written | HOD INPUT REQUIRED |
| BC-019 | NOT LIVE — page does not exist | Best Time to Buy an Engagement Ring | 52 | DRAFT — finalize when the article is written | PRE-AWS PREPARATION |
| BC-021 | NOT LIVE — page does not exist | What Is a Tennis Bracelet and How to Wear One | 62 | DRAFT — finalize when the article is written | PRE-AWS PREPARATION |
| BC-039 | NOT LIVE — page does not exist | What Finger Does a Promise Ring Go On? | 55 | DRAFT — finalize when the article is written | PRE-AWS PREPARATION |
| BC-022 | NOT LIVE — page does not exist | How to Stack Rings with Your Engagement Ring | 61 | DRAFT — finalize when the article is written | PRE-AWS PREPARATION |
| BC-038 | NOT LIVE — page does not exist | Ring Finger Meaning: What Each Finger Symbolizes | 65 | DRAFT — finalize when the article is written | PRE-AWS PREPARATION |
| BC-023 | NOT LIVE — page does not exist | Eternity Ring Meaning and When to Give One | 59 | DRAFT — finalize when the article is written | PRE-AWS PREPARATION |
| BC-025 | NOT LIVE — page does not exist | Different Types of Earrings, Explained | 55 | DRAFT — finalize when the article is written | PRE-AWS PREPARATION |
| BC-031 | NOT LIVE — page does not exist | Engagement Ring Trends for 2027 | 48 | DRAFT — finalize when the article is written | PRE-AWS PREPARATION |
| BC-032 | NOT LIVE — page does not exist | Fine Jewelry Trends for 2027 | 45 | DRAFT — finalize when the article is written | PRE-AWS PREPARATION |
| BC-034 | NOT LIVE — page does not exist | Valentine's Day Proposal Ideas | 47 | DRAFT — finalize when the article is written | PRE-AWS PREPARATION |
| BLOG-ER-HISTORY | NOT LIVE — page does not exist | The History of Engagement Rings | 48 | DRAFT — finalize when the article is written | PRE-AWS PREPARATION |
| BLOG-WB-BUYS | NOT LIVE — page does not exist | Who Buys the Wedding Bands? Etiquette Explained | 64 | DRAFT — finalize when the article is written | PRE-AWS PREPARATION |
| BLOG-WR-HISTORY | NOT LIVE — page does not exist | Wedding Ring History and Meaning | 49 | DRAFT — finalize when the article is written | PRE-AWS PREPARATION |
| BLOG-NPD | NOT LIVE — page does not exist | National Proposal Day: What It Is and Ideas | 60 | DRAFT — finalize when the article is written | PRE-AWS PREPARATION |

## 7. Rendered titles above 60 characters

| Row | Rendered title | Length | Disposition |
|---|---|---|---|
| COM-PDP-OVAL-FLORAL | 2.5 ct Oval Marquise Diamond Engagement Ring \| House of Diams | 61 | draft — tighten at writing if possible |
| EDU-LG-03 | CVD vs HPHT Lab-Grown Diamonds: What Buyers Should Know \| House of Diams | 72 | kept: key terms front-loaded |
| EDU-LG-02 | Lab-Grown vs Natural Diamonds: The Honest Comparison \| House of Diams | 69 | kept: key terms front-loaded |
| EDU-MET-01 | 14K vs 18K Gold (and 10K) for Diamond Jewelry \| House of Diams | 62 | draft — tighten at writing if possible |
| EDU-LG-10 | How to Choose a Lab-Grown Diamond: The Complete Buyer's Guide \| House of Diams | 78 | kept: key terms front-loaded |
| EDU-LG-01 | Are Lab-Grown Diamonds Real? A Complete Buyer's Guide \| House of Diams | 70 | kept: key terms front-loaded |
| EXIST-BLOG-ER-ONLINE | How to Choose a Lab-Grown Diamond Engagement Ring Online \| House of Diams | 73 | kept: key terms front-loaded |
| EDU-4C-06 | Diamond Cut: Grades, Cut vs Shape and Sparkle \| House of Diams | 62 | draft — tighten at writing if possible |
| EDU-MET-00 | Jewelry Metals Guide: White Gold vs Platinum \| House of Diams | 61 | draft — tighten at writing if possible |
| EDU-RJG-BR | Bracelet Size Chart: How to Measure Your Wrist \| House of Diams | 63 | draft — tighten at writing if possible |
| BC-001 | How Long Does a Custom Engagement Ring Take? \| House of Diams | 61 | approved package value |
| BC-004 | Christmas Jewelry Gifts: A Holiday Gift Guide \| House of Diams | 62 | approved package value |
| BC-035 | 10 Year Anniversary Gift Ideas: Tin and Diamond \| House of Diams | 64 | approved package value |
| BC-018 | Anniversary Gifts by Year: Traditional and Modern \| House of Diams | 66 | approved package value |
| BC-009 | Jewelry Gifts for Your Girlfriend: Diamond Ideas \| House of Diams | 65 | approved package value |
| BC-007 | How to Wear an Engagement Ring and Wedding Band \| House of Diams | 64 | approved package value |
| BC-037 | Engagement Ring vs Wedding Ring: The Difference \| House of Diams | 64 | draft — tighten at writing if possible |
| BC-014 | Proposal Ideas: How to Plan a Memorable Proposal \| House of Diams | 65 | draft — tighten at writing if possible |
| BC-021 | What Is a Tennis Bracelet and How to Wear One \| House of Diams | 62 | draft — tighten at writing if possible |
| BC-022 | How to Stack Rings with Your Engagement Ring \| House of Diams | 61 | draft — tighten at writing if possible |
| BC-038 | Ring Finger Meaning: What Each Finger Symbolizes \| House of Diams | 65 | draft — tighten at writing if possible |
| BLOG-WR-TYPES | Types of Wedding Rings: Band Styles Explained \| House of Diams | 62 | draft — tighten at writing if possible |
| BLOG-WB-BUYS | Who Buys the Wedding Bands? Etiquette Explained \| House of Diams | 64 | draft — tighten at writing if possible |

## 8. Meta descriptions — live pages

| Row | Current meta (truncated) | Recommended meta | Len | Action |
|---|---|---|---|---|
| NAV-HOME | Shop certified lab-grown diamond jewellery, engagement rings, wedding… | Explore House of Diams: diamond engagement rings, wedding bands, earrings, necklaces and bracelets, plus bespoke designs made to order. | 135 | REPLACE — FINAL |
| COM-SHOP | Browse our collection of fine jewellery and hip hop jewellery with ce… | Browse the full House of Diams collection: diamond engagement rings, wedding bands, earrings, necklaces and bracelets. | 118 | REPLACE — FINAL |
| COM-COLLECTION | Explore House of Diams collection pieces in a dedicated browse-only e… | — (none) |  | HOLD |
| COM-BESPOKE | Commission a bespoke piece. From CAD to setting, crafted in Surat wit… | Design a custom engagement ring or bespoke diamond jewelry with House of Diams. Share your idea, stone and metal preferences to start a conversation. | 149 | REPLACE — FINAL |
| BRAND-ABOUT | Learn about House of Diams: our founders, milestones, and values. | Learn about House of Diams, its story, values, and approach to diamond jewelry. | 79 | REPLACE — NEUTRAL INTERIM (no founder/m… |
| BRAND-CONTACT | Luxury diamond jewellery, crafted in Surat, India. | Contact House of Diams about an order, a product, a bespoke piece, wholesale or press. | 86 | CREATE — FINAL (adjust topics to F-C2 a… |
| SUP-FAQ | Frequently asked questions about House of Diams orders, diamonds, shi… | Answers to common questions about House of Diams orders, shipping, returns, diamonds and bespoke jewelry. | 105 | REPLACE — FINAL |
| SUP-POLICIES-SHIP | Shipping timelines and delivery details from House of Diams. | Shipping and delivery information from House of Diams: order processing and made-to-order lead times. | 101 | REPLACE — FINAL (after the page itself … |
| SUP-POLICIES-RET | Returns and exchange information from House of Diams. | How returns and exchanges work at House of Diams, and how to contact us with questions about your order. | 104 | REPLACE — FINAL (no return window menti… |
| SUP-POLICIES-PRIV | Privacy policy for House of Diams. | — (leave as is) |  | KEEP |
| SUP-POLICIES-TERMS | Terms and conditions for House of Diams. | — (leave as is) |  | KEEP |
| BLOG-HUB | Read House of Diams journal articles on diamonds, jewellery craft, bu… | Gift ideas, style advice and stories from House of Diams, with links to our diamond and jewelry guides. | 103 | REPLACE — FINAL |
| EDU-ROOT | Learn about diamonds, jewellery, craftsmanship, care, and confident b… | Plain-English guides to lab-grown and natural diamonds, the 4Cs, certification, metals and ring sizing from House of Diams. | 123 | REPLACE — FINAL |
| COM-ER | Browse Engagement Rings from the live catalog. | Shop diamond engagement rings in halo, solitaire, pavé, three-stone, bezel and side-stone styles, plus bespoke options. | 119 | REPLACE — FINAL |
| COM-WB | Browse Wedding Bands from the live catalog. | Shop women's diamond wedding bands: eternity, half-eternity and anniversary styles, with guidance on metals and ring size. | 122 | REPLACE — FINAL |
| COM-FJ | Browse Fine Jewellery from the live catalog. | Explore House of Diams fine diamond jewelry: earrings, necklaces and pendants, bracelets and rings. | 99 | REPLACE — FINAL |
| COM-FJ-EARRINGS | Browse Earrings in Fine Jewellery. | Shop diamond earrings: solitaire and halo studs, hoops and huggies, and drop styles in a range of diamond shapes. | 113 | REPLACE — FINAL |
| COM-FJ-NECKLACES | Browse Necklaces in Fine Jewellery. | Shop diamond necklaces and pendants: solitaire, toi et moi, multi-stone, charm and lariat styles. | 97 | REPLACE — FINAL |
| COM-FJ-BRACELETS | Browse Bracelet in Fine Jewellery. | Shop diamond bracelets: chain, link and tennis styles. | 54 | REPLACE — FINAL |
| COM-FJ-RINGS | Browse Rings in Fine Jewellery. | Shop House of Diams diamond fashion and statement rings, designed to wear beyond engagement rings and wedding bands. | 116 | REPLACE — FINAL |
| COM-CURATED-TBAR | Browse T- BAR from the live catalog. | Shop the House of Diams T-bar collection: knot, ridged and interlocking T-bar necklaces and pendants. | 101 | REPLACE — FINAL |
| COM-ER-STYLES-GROUP | Browse By Design in Engagement Rings. | — (none) |  | HOLD |
| COM-PDP | Descriptive product copy on most; 6 placeholder-style metas ('<Catego… | {Product type} with a {shape} diamond ({carat} ct total) in {metal}, {setting}. {Stone type}. See details, metal options and price. — spec in 07 | 144 | TEMPLATE RULE |
| COM-PDP-OVAL-FLORAL | Shop an oval side-stone engagement ring with a 2.500 ct center diamon… | Oval engagement ring with a 2.5 ct oval lab-grown center diamond and 16 marquise side stones in a raised four-prong setting, available in 10K and 14K gold. | 155 | REPLACE — FINAL (fact-check specs again… |

### Subcategories

| Row | Current meta (truncated) | Recommended meta | Len | Action |
|---|---|---|---|---|
| /engagement-rings/by-design/side-stone-rings | Browse Side Stone Rings in Engagement Rings. | Shop side-stone engagement rings: a center diamond flanked by smaller stones for extra sparkle and a distinctive profile. | 121 | REPLACE — FINAL |
| /engagement-rings/by-design/solitare-rings | Browse Solitare Rings in Engagement Rings. | Shop solitaire engagement rings: a single center diamond in classic and sculptural settings. | 92 | REPLACE — FINAL |
| /engagement-rings/by-design/halo-ring | Browse Halo Ring in Engagement Rings. | Shop halo engagement rings: a center diamond framed by a ring of smaller stones, in a range of center-stone shapes. | 115 | REPLACE — FINAL |
| /engagement-rings/by-design/toi-moi-rings | Browse Toi-moi Rings in Engagement Rings. | Shop toi et moi rings: two diamonds set side by side on one band, in modern and classic designs. | 96 | REPLACE — FINAL |
| /engagement-rings/by-design/pave | Browse Pavé Rings in Engagement Rings. | Shop pavé engagement rings with small diamonds set closely along the band for continuous sparkle. | 97 | REPLACE — FINAL |
| /engagement-rings/by-design/nature-inspired-rings | Browse Nature Inspired Rings in Engagement Rings. | Shop nature-inspired engagement rings with vine, leaf and floral designs. | 73 | REPLACE — FINAL |
| /engagement-rings/by-design/three-stone-rings | Browse Three Stone Rings in Engagement Rings. | Shop three-stone engagement rings: a center diamond flanked by two stones, often read as past, present and future. | 114 | REPLACE — FINAL |
| /engagement-rings/by-design/bezel-rings | Browse Bezel Rings in Engagement Rings. | Shop bezel engagement rings, where a smooth metal rim holds the center diamond securely. | 88 | REPLACE — FINAL |
| /wedding-bands/for-her/eternity | Browse Eternity in Wedding Bands. | Shop diamond eternity bands and rings for women: full and half-eternity designs in a range of diamond shapes. | 109 | REPLACE — FINAL |
| /wedding-bands/for-her/anniversay | Browse Anniversay in Wedding Bands. | Shop diamond anniversary rings and bands, a row of diamonds to mark a milestone or complete a ring stack. | 105 | REPLACE — FINAL |
| /fine-jewellery/earrings/stud-earrings | Browse Stud Earrings in Fine Jewellery. | Shop diamond stud earrings in solitaire and halo styles and a range of diamond shapes. | 86 | REPLACE — FINAL |
| /fine-jewellery/earrings/hoops-huggies | Browse Hoops & Huggies in Fine Jewellery. | Shop diamond hoop and huggie earrings, from slim huggies to statement hoops. | 76 | REPLACE — FINAL |
| /fine-jewellery/earrings/drop-dangle | Browse Drop & Dangle in Fine Jewellery. | Shop diamond drop and dangle earrings with movement and sparkle. | 64 | REPLACE — FINAL |
| /fine-jewellery/necklaces/solitare | Browse Solitare in Fine Jewellery. | Shop diamond solitaire necklaces and pendants: a single stone on a fine chain. | 78 | REPLACE — FINAL |
| /fine-jewellery/necklaces/pendant-necklace | Browse Pendant Necklace in Fine Jewellery. | Shop diamond pendant necklaces in bezel, marquise and sculptural designs. | 73 | REPLACE — FINAL |
| /fine-jewellery/necklaces/charm-necklace | Browse Charm Necklace in Fine Jewellery. | Shop diamond charm necklaces: small, meaningful pendants on a fine chain. | 73 | REPLACE — FINAL |
| /fine-jewellery/necklaces/multi-stone | Browse Multi stone in Fine Jewellery. | Shop multi-stone diamond necklaces that combine several diamond cuts in one design. | 83 | REPLACE — FINAL |
| /fine-jewellery/necklaces/lariat-necklace | Browse Lariat Necklace in Fine Jewellery. | Shop diamond lariat necklaces with a drop-through design. | 57 | REPLACE — FINAL |
| /fine-jewellery/necklaces/toi-et-moi | Browse Toi-et moi in Fine Jewellery. | Shop toi et moi diamond necklaces that pair two cuts in one pendant. | 68 | REPLACE — FINAL |
| /fine-jewellery/bracelet/tennis | Browse Tennis in Fine Jewellery. | Shop diamond tennis bracelets: a continuous line of diamonds set around the wrist. | 82 | REPLACE — FINAL |
| /fine-jewellery/bracelet/bangles | Browse Bangles in Fine Jewellery. | Shop House of Diams diamond link bracelets in open-link designs set with pavé diamonds. | 87 | HOLD — interim wording; no bangle claim |
| /fine-jewellery/bracelet/chain-link | Browse chain & Link in Fine Jewellery. | Shop diamond chain and link bracelets from House of Diams. | 58 | REPLACE — FINAL |

### Existing Education articles

| Row | Current meta (truncated) | Recommended meta | Len | Action |
|---|---|---|---|---|
| EDU-LG-03 | When shopping for a lab-grown diamond, you've likely come across the … | CVD and HPHT are the two main ways lab-grown diamonds are made. Both produce real diamonds. Here is how the methods differ and what to check when you buy. | 154 | REPLACE (current meta is the article's … |
| EDU-LG-02 | Choosing between a lab-grown diamond and a natural diamond is one of … | Lab-grown and natural diamonds are both real diamonds. Compare origin, price, quality and long-term value before you choose. | 124 | REPLACE (current meta is the article in… |
| EDU-MET-01 | Choosing between 14K and 18K gold is just as important as choosing th… | 14K gold is about 58% pure gold and 18K about 75%. Compare color, durability and value to choose the right gold for diamond jewelry. | 132 | REPLACE (current meta is the article in… |
| EDU-LG-10 | Choosing a lab-grown diamond becomes much easier once you know which … | How to choose a lab-grown diamond: which of cut, color, clarity and carat matter most, why certification matters and the mistakes to avoid. | 139 | REPLACE (current meta is the article in… |
| EDU-LG-01 | Everything you need to know about lab-grown diamonds, how they are ma… | Yes. Lab-grown diamonds are real diamonds with the same carbon crystal structure as mined stones. How they differ from simulants and how to verify one. | 151 | REPLACE (current meta is generic: 'Ever… |
| EDU-4C-00 | Buying a diamond becomes much easier once you understand the 4Cs—Cut,… | The 4Cs — cut, color, clarity and carat — explained, including how lab-grown diamonds are graded and which C matters most for how a diamond looks. | 146 | REPLACE (current meta is the article in… |
| EXIST-BLOG-ER-ONLINE | Buying an engagement ring online can feel overwhelming, especially wh… | — (no change) |  | KEEP |
| EDU-SHP-00 | Choosing the perfect diamond shape is one of the most exciting parts … | Compare the main diamond shapes — round, oval, pear, emerald, cushion and more — and how shape affects sparkle, apparent size and price in a ring. | 146 | REPLACE |
| EDU-RJG-02 | Finding the correct ring size is one of the most important steps when… | Find your ring size at home: measure an existing ring or your finger, use our ring size chart, and learn when to size up or down. | 129 | REPLACE |
| EDU-CERT-00 | When buying a lab-grown diamond, one of the most important documents … | What a lab-grown diamond certificate (a GIA or IGI report) shows, why it matters and how to check one before you buy. | 117 | REPLACE |
| EDU-CERT-01 | A grading report is one of the most important documents to understand… | GIA vs IGI for lab-grown diamonds: what each report shows, how their grading approaches differ and how to verify a report number. | 129 | REPLACE |

### Planned Education pages (drafts)

| Row | Current meta (truncated) | Recommended meta | Len | Action |
|---|---|---|---|---|
| EDU-LG-00 | NOT LIVE — page does not exist | Lab-grown diamonds are real diamonds made in a laboratory rather than mined. What they are, other names for them, how they are made and how they compare. | 153 | FINAL DRAFT (answer-first; adjust only … |
| EDU-LG-05 | NOT LIVE — page does not exist | Do lab-grown diamonds hold their value? How lab-grown diamond prices work, what to expect on resale and how they compare with natural diamonds. | 143 | FINAL DRAFT (answer-first; adjust only … |
| EDU-LG-07 | NOT LIVE — page does not exist | Are lab-grown diamonds ethical? The environmental and sourcing questions, what is and is not known, and what to ask a seller. | 125 | FINAL DRAFT (answer-first; adjust only … |
| EDU-LG-08 | NOT LIVE — page does not exist | Do lab-grown diamonds get cloudy? What causes a hazy look, how clarity and fluorescence affect appearance, and how durable lab-grown diamonds are. | 146 | FINAL DRAFT (answer-first; adjust only … |
| EDU-LG-09 | NOT LIVE — page does not exist | How to tell if a diamond is real: simple at-home checks, what a jeweler's tester can and cannot show, and why lab-grown diamonds pass a diamond tester. | 151 | FINAL DRAFT (answer-first; adjust only … |
| EDU-NAT-00 | NOT LIVE — page does not exist | How are diamonds formed? Natural diamond formation deep in the earth, how diamonds reach the surface, and how this differs from growing a diamond in a lab. | 155 | FINAL DRAFT (answer-first; adjust only … |
| EDU-4C-01 | NOT LIVE — page does not exist | A diamond clarity chart from Flawless to I3: what each grade means, which grades look clean to the eye and which clarity to buy. | 128 | FINAL DRAFT (answer-first; adjust only … |
| EDU-4C-02 | NOT LIVE — page does not exist | SI1 vs SI2 diamonds: what SI clarity means, when an SI diamond is eye-clean and when to avoid it. | 97 | FINAL DRAFT (answer-first; adjust only … |
| EDU-4C-03 | NOT LIVE — page does not exist | What VVS1 and VVS2 mean, how VVS compares with VS and flawless, and whether a VVS diamond is worth the price. | 109 | FINAL DRAFT (answer-first; adjust only … |
| EDU-4C-05 | NOT LIVE — page does not exist | The diamond color scale from D to Z: what each grade looks like, how color affects value and which color to buy. | 112 | FINAL DRAFT (answer-first; adjust only … |
| EDU-4C-06 | NOT LIVE — page does not exist | Diamond cut explained: what cut grade means, how cut differs from shape and how cut drives a diamond's brilliance. | 114 | FINAL DRAFT (answer-first; adjust only … |
| EDU-4C-07 | NOT LIVE — page does not exist | A diamond carat size chart: carat to millimeters by shape, how big each carat looks and what size diamond studs to choose. | 122 | FINAL DRAFT (answer-first; adjust only … |
| EDU-MET-00 | NOT LIVE — page does not exist | Compare white gold, platinum, and yellow, white and rose gold for diamond jewelry: durability, color, care and cost. | 116 | FINAL DRAFT (answer-first; adjust only … |
| EDU-RJG-01 | NOT LIVE — page does not exist | Engagement ring settings explained: prong, bezel, halo, pavé, solitaire and more, and how to choose the right setting. | 118 | FINAL DRAFT (answer-first; adjust only … |
| EDU-GEN-01 | NOT LIVE — page does not exist | What are diamonds made of? Carbon, how its structure gives a diamond its hardness, and how durable a diamond really is. | 119 | FINAL DRAFT (answer-first; adjust only … |
| EDU-RJG-03 | NOT LIVE — page does not exist | How to clean a diamond ring and diamond earrings at home: safe steps, what to avoid and everyday-wear care. | 107 | FINAL DRAFT (answer-first; adjust only … |
| EDU-RJG-BR | NOT LIVE — page does not exist | A bracelet size chart: how to measure your wrist, how much room to add and how to choose the right fit, including tennis bracelets. | 131 | FINAL DRAFT (answer-first; adjust only … |
| EDU-RJG-NL | NOT LIVE — page does not exist | A necklace length chart: what each length looks like, how to measure and which length suits a pendant. | 102 | FINAL DRAFT (answer-first; adjust only … |
| EDU-INS | NOT LIVE — page does not exist | Engagement ring insurance: whether it is worth it, what it typically costs and covers, and how to insure a ring. | 112 | FINAL DRAFT (answer-first; adjust only … |
| EDU-WB-GUIDE | NOT LIVE — page does not exist | How to choose a wedding band: metal, width and fit, and how to pair it with your engagement ring in an oval, solitaire or halo style. | 133 | FINAL DRAFT (answer-first; adjust only … |
| BLOG-WR-TYPES | NOT LIVE — page does not exist | The main types of wedding rings and wedding band styles — classic, eternity, pavé, curved and contour — and how to choose. | 122 | DRAFT — FINAL DRAFT (≤155 chars guideli… |

### Planned Blog posts (10 approved carried unchanged; 23 drafts)

| Row | Current meta (truncated) | Recommended meta | Len | Action |
|---|---|---|---|---|
| BC-001 | NOT LIVE — page does not exist | A House of Diams bespoke ring takes 3–4 weeks on average from design approval to delivery: typically 2–3 weeks of production, then 6–9 days of insured shipping. | 160 | CARRY APPROVED VALUE (package unedited)… |
| BC-004 | NOT LIVE — page does not exist | The best Christmas jewelry gifts are diamond studs, a solitaire pendant and a tennis bracelet. Ideas by budget and recipient, plus Hanukkah timing. | 147 | CARRY APPROVED (CMS 'Short Intro') |
| BC-035 | NOT LIVE — page does not exist | The traditional 10 year anniversary gift is tin or aluminum; the modern gift is diamond jewelry. Gift ideas for both traditions, and how to combine them. | 153 | CARRY APPROVED (CMS 'Short Intro') |
| BC-018 | NOT LIVE — page does not exist | Anniversary gifts by year: the full traditional and modern list, from paper for the 1st to diamond for the 60th, plus the diamond, gold and platinum years. | 155 | CARRY APPROVED (CMS 'Short Intro') |
| BC-036 | NOT LIVE — page does not exist | In the US, a wedding ring goes on the fourth finger of the left hand, with the engagement ring. Why the left hand, and which countries use the right. | 149 | CARRY APPROVED (CMS 'Short Intro') |
| BC-006 | NOT LIVE — page does not exist | How to layer necklaces: space them about 2 inches apart, finest chain on top, heaviest at the bottom. Lengths, example stacks and how to stop tangling. | 151 | CARRY APPROVED (CMS 'Short Intro') |
| BC-008 | NOT LIVE — page does not exist | The best jewelry gifts for your wife: diamond studs, a solitaire pendant or a tennis bracelet, plus anniversary bands and ideas for the wife who has everything. | 160 | CARRY APPROVED (CMS 'Short Intro') |
| BC-009 | NOT LIVE — page does not exist | Jewelry gifts for your girlfriend by relationship stage: first-Christmas pendants and studs, meaningful necklaces, and when a promise ring makes sense. | 151 | CARRY APPROVED (CMS 'Short Intro') |
| BC-003 | NOT LIVE — page does not exist | A push present is a gift for a new mother to mark the birth of a baby. What it means, when to give one, and diamond jewelry ideas that suit life with a newborn. | 160 | CARRY APPROVED (CMS 'Short Intro') |
| BC-007 | NOT LIVE — page does not exist | Traditionally the wedding band goes on first, with the engagement ring on top. Alternatives, wedding-day etiquette and whether to solder your rings together. | 157 | CARRY APPROVED (CMS 'Short Intro') |
| BC-011 | NOT LIVE — page does not exist | A promise ring is a ring given as a commitment, without being an engagement. What it means, who gives one and how it differs from an engagement ring. | 149 | DRAFT — FINAL DRAFT (≤155 chars guideli… |
| BC-037 | NOT LIVE — page does not exist | An engagement ring is given at the proposal and a wedding ring is exchanged at the ceremony. How they differ in style, timing and wear, and whether you need both. | 162 | DRAFT — FINAL DRAFT (≤155 chars guideli… |
| BC-014 | NOT LIVE — page does not exist | Proposal ideas and a simple planning guide, from choosing the moment and place to presenting the ring. | 102 | DRAFT — FINAL DRAFT (≤155 chars guideli… |
| BC-015 | NOT LIVE — page does not exist | (HOLD — write the meta after HOD confirms the facts it will cite.) |  | HOLD (business facts) |
| BC-024 | NOT LIVE — page does not exist | How much should an engagement ring cost? There is no fixed rule — typical spending ranges, common budget guidelines and how to decide what to spend. | 148 | DRAFT — FINAL DRAFT (≤155 chars guideli… |
| BC-016 | NOT LIVE — page does not exist | When is engagement season? Why so many proposals happen between Thanksgiving and Valentine's Day, and how that affects when to buy a ring. | 138 | DRAFT — FINAL DRAFT (≤155 chars guideli… |
| BC-017 | NOT LIVE — page does not exist | Festive ways to propose at Christmas or on New Year's Eve, plus a simple timeline for getting the ring ready in time. | 117 | DRAFT — FINAL DRAFT (≤155 chars guideli… |
| BC-005 | NOT LIVE — page does not exist | (HOLD — write the meta after HOD confirms the workshop facts it will cite.) |  | HOLD (business facts) |
| BC-019 | NOT LIVE — page does not exist | Is Black Friday a good time to buy an engagement ring? How sale timing, seasons and lead time affect price and choice. | 118 | DRAFT — FINAL DRAFT (≤155 chars guideli… |
| BC-021 | NOT LIVE — page does not exist | A tennis bracelet is a flexible line of matching stones set around the wrist. Why it is called that, how to wear one and how to choose. | 135 | DRAFT — FINAL DRAFT (≤155 chars guideli… |
| BC-039 | NOT LIVE — page does not exist | Which finger and hand a promise ring is traditionally worn on, what each placement can signal and how to choose. | 112 | DRAFT — FINAL DRAFT (≤155 chars guideli… |
| BC-022 | NOT LIVE — page does not exist | How to stack rings: combinations of an engagement ring, wedding band and eternity band, with tips on order, width and metal. | 124 | DRAFT — FINAL DRAFT (≤155 chars guideli… |
| BC-038 | NOT LIVE — page does not exist | What a ring on each finger is said to symbolize, from thumb to pinky, and what changes between the left and right hand. | 119 | DRAFT — FINAL DRAFT (≤155 chars guideli… |
| BC-023 | NOT LIVE — page does not exist | What an eternity ring means, when couples give one, which finger it is worn on and the difference between full and half eternity. | 129 | DRAFT — FINAL DRAFT (≤155 chars guideli… |
| BC-025 | NOT LIVE — page does not exist | The main types of earrings — studs, huggies, hoops and drops — how they differ, and how earring backs work. | 107 | DRAFT — FINAL DRAFT (≤155 chars guideli… |
| BC-031 | NOT LIVE — page does not exist | Engagement ring trends for 2027, including toi et moi, east-west, bezel, three-stone and elongated shapes, and how to choose a style that lasts. | 144 | DRAFT — FINAL DRAFT (≤155 chars guideli… |
| BC-032 | NOT LIVE — page does not exist | Fine jewelry trends for 2027: diamond earrings, bracelets and necklaces to watch, and how to choose pieces you will keep wearing. | 129 | DRAFT — FINAL DRAFT (≤155 chars guideli… |
| BC-034 | NOT LIVE — page does not exist | Romantic ways to propose on Valentine's Day, February 14, with planning tips and ring-timing advice. | 100 | DRAFT — FINAL DRAFT (≤155 chars guideli… |
| BLOG-ER-HISTORY | NOT LIVE — page does not exist | The history of engagement rings, from Roman betrothal rings to modern and lab-grown diamond rings. | 98 | DRAFT — FINAL DRAFT (≤155 chars guideli… |
| BLOG-WB-BUYS | NOT LIVE — page does not exist | Who buys the wedding bands? Traditional etiquette, when to buy them and how much couples typically spend. | 105 | DRAFT — FINAL DRAFT (≤155 chars guideli… |
| BLOG-WR-HISTORY | NOT LIVE — page does not exist | Wedding ring history and meaning: why we exchange rings, from ancient Egypt to the double-ring ceremony. | 104 | DRAFT — FINAL DRAFT (≤155 chars guideli… |
| BLOG-NPD | NOT LIVE — page does not exist | What National Proposal Day (March 20) is, how it started and how to plan a spring proposal. | 91 | DRAFT — FINAL DRAFT (≤155 chars guideli… |

## 9. Validation after AWS (Class C)

Fetch the rendered `<title>`, meta description, canonical and H1 for every row marked `REPLACE`/`CARRY APPROVED`; confirm the suffix is still appended once, the homepage title is absolute, and no duplicate titles/metas exist in the crawl.
