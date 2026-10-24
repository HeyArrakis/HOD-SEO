# 07 — PDP On-Page SEO

Generated 2026-10-10. Companion: `07-PDP-PRIORITY-ACTIONS.csv` (23 PDPs needing special treatment). **The 184 product pages are governed by templates and rules; they are not rewritten one by one.** Product URLs never change in this package.

## 1. Evidence (QA/06 + live re-read 2026-10-09)

* 184 PDPs (categories: Fine Jewellery 112, Engagement Rings 61, Wedding Bands 7, T- BAR 4). All 200, self-canonical, USD in schema (US/IP behavior to verify), 178 priced for 10K Yellow Gold, 5 for 10K White Gold, 1 for '18K Gold Vermil'.
* Titles = `<Product name> | House of Diams`; **65 exceed 60 rendered characters**; 2 products share one title; 6 have placeholder-style metas ("Stud Earrings · 10K White Gold - House of Diams"); 3 metas exceed 160 characters; 10 PDPs have numeric-ID / `-copy-` slugs (carat variants as separate URLs).
* Product descriptions are substantive (shape, carat, setting, closure, dimensions, SKU, 'Best for') — but also contain **unverified claims**: "IGI certified GH / VVS diamonds", a shipping block ("Worldwide insured shipping is complimentary…", "In-stock pieces usually ship within 2-3 business days") and a "Care & Warranty" block. Header badges say "Complimentary Insured Shipping / 15-Day Returns". None of these is a confirmed HOD fact (F-B1).

## 2. Title template (pre-suffix; the template adds ` | House of Diams`)

`[{Total carat} ct ]{Shape} [Lab-Grown ]Diamond {Product type}[, {distinguishing feature}]` — order of priority when space is short: **shape + product type > carat > distinguishing feature > origin word > metal**. Target ≤~43 characters pre-suffix (≤60 rendered; a display guideline).

* Use the **product record** for every word (shape, carat, type, stone type). Do not add 'Lab-Grown' unless the record's Stone Type says so (the spec table does show 'Lab Grown Diamond').
* **Keep the existing name** when it is already descriptive and short; do not rename for its own sake. Collection names alone ("Adeline", "Elyra") never stand as the title.
* Titles must be unique: where two products would collide, add the true differentiator (bail style, setting, carat).

| Current (rendered) | Template result (illustrative — fact-check vs product record) |
|---|---|
| Adeline 2 CTW Round Diamond Solitaire Stud Earrings (68 rendered) | Round Solitaire Diamond Stud Earrings, 2 ct (≈44 pre-suffix) |
| Alternating Pear Lab-Grown Diamond Eternity Ring (53) | KEEP — already ≤60 rendered |
| Milgrain Bezel Round Lab-Grown Diamond Necklace 1.00 Carat (>60) | Round Milgrain Bezel Diamond Necklace, 1.00 ct |
| Oval Marquise Side-Stone Engagement Ring | 2.5 ct Oval Marquise Diamond Engagement Ring |

## 3. Meta-description template

`{Product type} with {shape/stone description} ({carat} total) in {setting/metal note}. {One factual differentiator}. {Metal availability as shown on the page}.` ≤~155 characters. Built from the description and spec table only. **Never** include certification, shipping, returns, warranty or "free". Replace the six placeholder metas first (drafts in the CSV); trim the three >160 character metas at a sentence boundary.

## 4. H1 and description rules

* H1 = the visible product name (unchanged). It must equal the schema `name` (see §7).
* Description first sentence: product type, stone shape, carat, setting, metal. Then design details. Avoid cloning descriptions across carat variants (near-duplicate risk — vary the carat/size facts that genuinely differ).
* Specs table kept (shape, total carat, center stone, setting, closure, dimensions, SKU, style, best for). State the stone type per product from the record.
* Certification: show a lab and report number **only where a report exists for that piece**; no blanket "IGI certified" (F-B1).
* Shipping/returns/warranty sections: replace the per-PDP copy with a short summary linking to /shipping and /returns once those are final.

## 5. Variants and near-duplicates

* IA D-11: one URL per product, variants on the page. Ten PDPs are separate URLs for carat variants (e.g. 1 CT vs 2 CT east-west emerald pendant; milgrain bezel necklace 1.00 vs 1.50; 2.62 vs 3.62 ct three-stone ring; two round solitaire pendants). **ADOPTED (OD-14): keep these URLs; do not merge, delete or redirect them without a supported consolidation plan and GSC/URL evidence.** Keep each self-canonical with carat in title/meta so each is unique; review after cut-over with GSC data (G-01).
* Metal choices (10K/14K × yellow/white/rose) are on-page options, not URLs.
* Duplicate-risk pairs: Aurelia vs Elyra round solitaire pendants (same title; differ by bail style).

## 6. Image / alt text

Gallery alt = `<product name>, <view>`; primary image first; product video poster alt; card images = name + one attribute; decorative icons `alt=""`. Do not rename files or change hosts before AWS; after AWS keep old image URLs resolvable and update schema `image`, OG tags and `/llms.txt`.

## 7. Product / Offer schema — CURRENT / RECOMMENDED / WHY / DEPENDENCY / VALIDATION

| Property | CURRENT | RECOMMENDED | WHY | DEPENDENCY | VALIDATION |
|---|---|---|---|---|---|
| name | Internal name ('Oval Floral Diamond Ring') ≠ visible H1 on the checked PDP | = visible H1 | Mismatched names confuse shopping surfaces | Class B (product data/template) | Name equals H1 on 3 PDPs |
| sku | UUID in JSON-LD; visible SKU (e.g. RG038993) differs | = visible SKU | Stable merchant identifier | Class B | sku equals visible SKU |
| description | Present | = visible description (no unverified claims) | Consistency | OD-08 | — |
| material / offers.price | Six metals listed; one price (default variant) | Default variant material with its price, or ProductGroup/variants if variant URLs/params exist | Price must describe what is listed | Class B; engineering decision | Rich Results Test |
| BreadcrumbList | Home › Shop › Product (visible: Home / Engagement Rings / By Design) | Home › Category › Subcategory › Product = visible | Markup must match the page | Class B | Breadcrumb equals visible path |
| image | Supabase / Cloudflare R2 URLs | Stable post-AWS URLs; all gallery images | Hosts change with AWS | Class B; keep old URLs resolving | Image URLs 200 |
| Offer.priceCurrency / availability | USD (crawl from IN also showed USD in schema; cookies were IN/INR) | USD for US/Googlebot; availability accurate | Currency by IP risk | Engineering confirm | Request from a US IP |
| shippingDetails / hasMerchantReturnPolicy | Absent | Add only when policies are final | Avoid unconfirmed promises in markup | OD-08; Class B | Matches visible policy |
| aggregateRating / review | Absent | Do not add without genuine, displayed reviews | Guideline compliance | — | — |

## 8. Internal-link rules for PDPs

* Breadcrumb: Home › Category › Subcategory › Product (visible and schema identical); PDP URLs stay flat.
* ≤3 Education links as **template UI labels** ("Find your ring size", "What do these diamond grades mean?") — NAVIGATIONAL, not keyword strings (Stage 16 §5). Ring PDPs must link the ring-size guide (REQUIRED for the ranking PDP).
* Related-products module links PDP → other PDPs only; a product never links to itself.
* Bespoke CTA where the product is customisable — only if HOD confirms product-level customization (Stage 16 §6.5: unconfirmed).
* Link to /shipping and /returns once final.

## 9. Priority PDPs (see CSV)

| PDP | Issues | Priority | Action |
|---|---|---|---|
| aurelia-round-solitaire-diamond-pendant | duplicate title | HIGH | DIFFERENTIATE title (bail style) — two products share one title |
| cushion-solitaire-studs | placeholder-style meta; duplicate meta; meta<70 | HIGH | REPLACE title + meta from the product record (fact-check specs); H1/name unchanged |
| elyra-round-solitaire-diamond-pendant | duplicate title | HIGH | DIFFERENTIATE title (bail style) — two products share one title |
| princess-halo-stud-earrings | placeholder-style meta; meta<70 | HIGH | REPLACE title + meta from the product record (fact-check specs); H1/name unchanged |
| radiant-halo-drops | placeholder-style meta; duplicate meta; meta<70 | HIGH | REPLACE title + meta from the product record (fact-check specs); H1/name unchanged |
| round-hoop-drops | placeholder-style meta; duplicate meta; meta<70 | HIGH | REPLACE title + meta from the product record (fact-check specs); H1/name unchanged |
| round-radiant-drops | placeholder-style meta; meta<70 | HIGH | REPLACE title + meta from the product record (fact-check specs); H1/name unchanged |
| round-solitaire-studs | placeholder-style meta; duplicate meta; meta<70 | HIGH | REPLACE title + meta from the product record (fact-check specs); H1/name unchanged |
| emerald-horizon-diamond-pendant-1786691308867 | numeric-ID/copy slug | MEDIUM | KEEP URL; unique carat-specific title/meta already; decide variant consolidation (OD-14);… |
| emerald-horizon-diamond-pendant-1786691308867-co | numeric-ID/copy slug | MEDIUM | KEEP URL; unique carat-specific title/meta already; decide variant consolidation (OD-14);… |
| floating-four-prong-diamond-necklace-17879988481 | numeric-ID/copy slug; title>60 (rendered) | MEDIUM | KEEP URL; unique carat-specific title/meta already; decide variant consolidation (OD-14);… |
| floating-four-prong-diamond-necklace-17879988481 | numeric-ID/copy slug; title>60 (rendered) | MEDIUM | KEEP URL; unique carat-specific title/meta already; decide variant consolidation (OD-14);… |
| milgrain-bezel-round-diamond-necklace-1788000835 | numeric-ID/copy slug; title>60 (rendered) | MEDIUM | KEEP URL; unique carat-specific title/meta already; decide variant consolidation (OD-14);… |
| milgrain-bezel-round-diamond-necklace-1788000835 | numeric-ID/copy slug; title>60 (rendered) | MEDIUM | KEEP URL; unique carat-specific title/meta already; decide variant consolidation (OD-14);… |
| oval-floral-diamond-ring | Stage 15 ranking PDP; JSON-LD name ≠ H1; sku UUID ≠ visible SKU; titl… | MEDIUM | see COM-PDP-OVAL-FLORAL row in 01 |
| round-baguette-three-stone-ring-1787141900680 | duplicate meta; numeric-ID/copy slug; title>60 (rendered) | MEDIUM | KEEP URL; unique carat-specific title/meta already; decide variant consolidation (OD-14);… |
| round-baguette-three-stone-ring-1787142818857 | duplicate meta; numeric-ID/copy slug; title>60 (rendered) | MEDIUM | KEEP URL; unique carat-specific title/meta already; decide variant consolidation (OD-14);… |
| round-diamond-split-bail-solitaire-pendant-17866 | numeric-ID/copy slug | MEDIUM | KEEP URL; unique carat-specific title/meta already; decide variant consolidation (OD-14);… |
| round-diamond-split-bail-solitaire-pendant-17866 | numeric-ID/copy slug | MEDIUM | KEEP URL; unique carat-specific title/meta already; decide variant consolidation (OD-14);… |
| serenelle-pear-pav-ring | truncated material label ('Vermil') | MEDIUM | FIX material label in product data ('18K Gold Vermil' → verify; likely vermeil); correct … |
| elowen-cushion-halo-engagement-ring | meta>160; title>60 (rendered) | LOW | TRIM meta to ≤155 chars at a sentence boundary |
| elowen-emerald-halo-engagement-ring | meta>160; title>60 (rendered) | LOW | TRIM meta to ≤155 chars at a sentence boundary |
| emerald-cut-eight-prong-diamond-pendant | meta>160; title>60 (rendered) | LOW | TRIM meta to ≤155 chars at a sentence boundary |

## 10. Sequencing

1. **Now (Class A):** approve templates; fact-check the six placeholder-meta drafts and the two title differentiators against the product records; list the full set of titles >60 rendered characters for template-based rewrite.
2. **After AWS (Class B):** apply title/meta templates in the CMS/product data; fix schema name/sku/material/breadcrumb; replace per-PDP shipping/warranty copy; update image URLs.
3. **After AWS (Class C):** re-crawl all 184 PDPs: title uniqueness, length distribution, schema validity, canonical, 200s, USD for a US request.
