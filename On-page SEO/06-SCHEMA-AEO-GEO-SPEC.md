# 06 — Schema, AEO, GEO/Entity & Image Spec

Generated 2026-10-10. **Specification only. Template/schema/image-host changes are Class B (wait for AWS); validation is Class C.** Principles: mark up only what the page visibly shows; Google needs no special markup for AI features; FAQ rich results were discontinued (2026-05) — **FAQPage is not recommended anywhere**, HowTo has no feature, QAPage is invalid for site-authored Q&A; no ratings/reviews markup without genuine reviews; nothing here guarantees AI Overview or AI-answer visibility.

## 1. Schema — CURRENT / RECOMMENDED / WHY / DEPENDENCY / VALIDATION

| Page type | CURRENT (live crawl 2026-10-09) | RECOMMENDED | WHY | IMPLEMENTATION DEPENDENCY | VALIDATION NEEDED |
|---|---|---|---|---|---|
| Sitewide | Organization + ContactPoint + PostalAddress (Surat IN, New York US) | Keep; add @id; one email/phone; confirmed sameAs; founder/foundingDate only when confirmed | Single entity signal across AI/search surfaces | Class B template; OD-08 facts | Org @id resolves; contact data = visible contact data |
| Homepage | Organization only | Optional WebSite (name only). No Product/FAQ | Clarifies site entity; no feature to chase | Class B | WebSite name matches brand |
| Category / subcategory / shop | BreadcrumbList + Organization; **FAQPage on 35 pages (boilerplate repeated)** | BreadcrumbList only; retire boilerplate FAQPage; optional visible category-specific Q&A WITHOUT FAQPage markup | FAQ rich results discontinued; duplicated Q&A across pages is noise | Class B template | No FAQPage left on listing pages; breadcrumbs valid |
| PDP (184) | Product + Offer + Brand + BreadcrumbList; no ratings; images on Supabase / R2 hosts | Keep Product/Offer; name = H1; sku = visible SKU; default-variant material/price; BreadcrumbList = visible path; shipping/returns details only when final; image URLs updated after AWS; never fake reviews | Prevents mismatches between markup and visible content | Class B/C; OD-08; OD-14 | Rich Results Test on 3 PDPs; currency USD for US |
| Articles (Blog + Education) | BlogPosting + `Person` author (names vary) + ImageObject; dates ISO on live articles; no BreadcrumbList | BlogPosting/Article + BreadcrumbList; author = Organization or a real named expert (OD-11); ISO dates; **no FAQPage/HowTo** | Consistent attribution; navigation context | Class B template (CMS has no schema field); OD-11 | 2 articles incl. one CMS-generated post (package notes claim non-ISO dates — VERIFY) |
| /about | Organization only | AboutPage + Organization @id; Person only for confirmed founders | Primary entity page | Class B; OD-08 | Person names match visible page |
| /contact (if built) | n/a (modal) | ContactPage + Organization | NAP consistency | Class B; OD-09 | Contact data identical sitewide |
| /faq | FAQPage | WebPage + BreadcrumbList; FAQPage on /faq alone is harmless but earns no rich result — do not extend | Visible Q&A page is the only legitimate FAQPage context | Class B | Visible Q&A = markup Q&A |
| /returns, /shipping | FAQPage on /returns attached to a non-FAQ body; none on /shipping | WebPage + BreadcrumbList; MerchantReturnPolicy / OfferShippingDetails when terms are final | Remove mismatched markup; add policy structure only with facts | Class B; OD-08 | Policy markup = visible policy |
| /bespoke | Organization only | BreadcrumbList; Service optional (no Google feature) | Low value; keep simple | Class B | — |
| Hubs (/blog, /education) | Organization only | CollectionPage/Blog optional + BreadcrumbList | Context only | Class B | — |

### Organization specification (sitewide)

| Property | Recommended | Status |
|---|---|---|
| `@type`, `name`, `url`, `logo` | Organization "House of Diams", https://www.houseofdiams.com, logo meeting Google's guidelines | Present — verify logo spec |
| `@id` | Stable `https://www.houseofdiams.com/#organization` reused by WebSite/AboutPage/Product `brand`/`publisher` | ADD |
| `contactPoint` | ONE email + telephone pair HOD designates as public (today info@ site-wide vs Admin@ on /returns; +91 phone only) | HOD INPUT REQUIRED (F-C2) |
| `address` | Surat (IN) and New York (US) as currently published | VERIFY with HOD |
| `sameAs` | Only profiles HOD confirms (Instagram linked on-page; Pinterest VERIFY) | ADD after confirmation |
| `founder`, `foundingDate` | Only after names/roles/year are confirmed | HOD INPUT REQUIRED (F-C1) |
| `hasMerchantReturnPolicy`, shipping | Only after /returns and /shipping facts are final | HOD INPUT REQUIRED (F-A1, F-A2) |

## 2. Product / PDP schema

See `07-PDP-ON-PAGE-SEO.md` §7 (name = visible H1; sku = visible SKU; one default-variant material/price; BreadcrumbList = visible path; no reviews; shipping/returns only when final; image URLs after the AWS host change).

## 3. AEO — answer-first specification

**Pattern for every informational page:** question (H1/H2 phrased as the user asks) → **direct answer in 1–2 sentences** → explanation → evidence/context (dated, sourced) → details (table/list/steps *only* where the content is genuinely tabular or sequential) → next action (link). Do **not** add FAQ blocks for their own sake; map the PAA questions the research found into headings or answer blocks; keep one owner per question (Stage 18 ownership), and link rather than repeat.

**Where AEO work matters most (from the research: AI Overview present on the calendar SERP):** ring size chart (165,000), diamond shapes (60,500), diamond cut (60,500), diamond clarity chart (33,100), 10-year anniversary gift (33,100), how to tell if a diamond is real (18,100) — all Education/Blog pages still to be written or refreshed (primary keywords now ratified, OD-03).

| Row | Lead question | AEO opportunity | Status |
|---|---|---|---|
| COM-BESPOKE | How long does a custom engagement ring take? | HIGH-VALUE: 'How long does a custom engagement ring take?' (1–2 sentence answer with the confirmed range + link to BC-0… | READY FOR IMPLEMENTATION POST-AWS |
| EDU-LG-03 | Which is better, CVD or HPHT? | HIGH — AI Overview present on the topic; answer-first block + comparison table are the extractable units. | GSC BASELINE REQUIRED |
| EDU-LG-02 | Is it better to buy a real diamond or a lab-grown diamond? | HIGH — comparison table + one-sentence answer. | GSC BASELINE REQUIRED |
| EDU-MET-01 | Is 18K or 14K gold better? | HIGH — direct comparison + table. | GSC BASELINE REQUIRED |
| EDU-LG-01 | Are lab grown diamonds real? | HIGH — AI Overview present; one-sentence answer is the extractable unit. | READY FOR IMPLEMENTATION POST-AWS |
| EDU-4C-00 | Is F VS2 a good diamond? | HIGH — grading tables are extractable. | READY FOR IMPLEMENTATION POST-AWS |
| EDU-SHP-00 | What shape diamond should I get? | HIGH — shape chart. | READY FOR IMPLEMENTATION POST-AWS |
| EDU-RJG-02 | What is my ring size? | HIGH — chart + step list; PAA: 4 uncovered. | READY FOR IMPLEMENTATION POST-AWS |
| EDU-CERT-00 | Are lab grown diamonds certified? | HIGH — definition block + 'what a report includes' list. | READY FOR IMPLEMENTATION POST-AWS |
| EDU-CERT-01 | Which is best, IGI or GIA? | HIGH — comparison table. | READY FOR IMPLEMENTATION POST-AWS |
| EDU-LG-00 | How are synthetic diamonds made? | HIGH — AI Overview present on the calendar SERP | PRE-AWS PREPARATION |
| EDU-LG-05 | Are lab grown diamonds cheaper? | HIGH — AI Overview present on the calendar SERP | PRE-AWS PREPARATION |
| EDU-LG-07 | Are lab grown diamonds ethical? | HIGH — AI Overview present on the calendar SERP | PRE-AWS PREPARATION |
| EDU-LG-08 | Do lab grown diamonds get cloudy? | HIGH — AI Overview present on the calendar SERP | PRE-AWS PREPARATION |
| EDU-LG-09 | Do lab grown diamonds pass a diamond tester? | HIGH — AI Overview present on the calendar SERP | PRE-AWS PREPARATION |
| EDU-NAT-00 | How are diamonds formed? | HIGH — AI Overview present on the calendar SERP | PRE-AWS PREPARATION |
| EDU-4C-01 | What is the best clarity for a diamond? | HIGH — AI Overview present on the calendar SERP | PRE-AWS PREPARATION |
| EDU-4C-02 | Is SI2 a good diamond? | HIGH — AI Overview present on the calendar SERP | PRE-AWS PREPARATION |
| EDU-4C-03 | What does VVS mean in a diamond? | HIGH — AI Overview present on the calendar SERP | PRE-AWS PREPARATION |
| EDU-4C-05 | Is diamond color grade GH good? | HIGH — AI Overview present on the calendar SERP | PRE-AWS PREPARATION |
| EDU-4C-06 | What is super ideal cut diamond? | HIGH — AI Overview present on the calendar SERP | PRE-AWS PREPARATION |
| EDU-MET-00 | What type of metal is best for wedding bands? | HIGH — AI Overview present on the calendar SERP | PRE-AWS PREPARATION |
| EDU-RJG-01 | What are the different diamond settings? | HIGH — AI Overview present on the calendar SERP | PRE-AWS PREPARATION |
| EDU-GEN-01 | What are diamonds made of? | HIGH — AI Overview present on the calendar SERP | PRE-AWS PREPARATION |
| EDU-RJG-03 | How do I make my diamond ring shiny again? | HIGH — AI Overview present on the calendar SERP | PRE-AWS PREPARATION |
| EDU-RJG-NL | How do I know what length necklace to get? | HIGH — AI Overview present on the calendar SERP | PRE-AWS PREPARATION |
| EDU-INS | Is it worth getting insurance on an engagement ring? | HIGH — AI Overview present on the calendar SERP | PRE-AWS PREPARATION |
| EDU-WB-GUIDE | How to find a lost wedding band? | HIGH — AI Overview present on the calendar SERP | PRE-AWS PREPARATION |
| BC-001 | How long does a custom engagement ring take? | HIGH — AI Overview present; PAA 4 | HOD INPUT REQUIRED |
| BC-004 | What is the best jewelry to give as a Christmas gift? | HIGH — AI Overview present; PAA 4 | READY FOR IMPLEMENTATION POST-AWS |
| BC-035 | What is a traditional gift for a 10 year anniversary? | HIGH — AI Overview present; PAA 4 | READY FOR IMPLEMENTATION POST-AWS |
| BC-018 | Is $300 enough for a wedding gift from a couple? | HIGH — AI Overview present; PAA 8 | READY FOR IMPLEMENTATION POST-AWS |
| BC-036 | Is the wedding ring on the left or right finger? | HIGH — AI Overview present; PAA 5 | READY FOR IMPLEMENTATION POST-AWS |
| BC-006 | What is the rule for layering necklaces? | HIGH — AI Overview present; PAA 5 | READY FOR IMPLEMENTATION POST-AWS |

**Commercial pages:** AEO is LOW — a one/two-sentence category definition above the grid and links to the Education owners; the questions stay on Education pages. **Policy pages:** AEO is about *accuracy* — shipping/returns answers are quoted by AI systems, so they must match the policy exactly (F-B1).

## 4. GEO / entity / trust

Treated as part of SEO (Google has no separate algorithm): make the brand and its facts understandable, consistent and attributable.

| Entity / fact | Today | Needed | Pages that must agree |
|---|---|---|---|
| Brand description (what House of Diams is and sells) | Different on Home / About / FAQ / /returns | One approved description | Home, About, FAQ, Organization schema, /llms.txt |
| Locations (Surat workshop, New York office) | /about and schema; /returns calls Surat "Headquarters & Workshop" | Confirmed list | About, Contact, schema, footer |
| Founders / roles / year | 'Akshar korat co founder'; bylines 'Krish Babriya, Co-founder'; 2014 vs 'half a century' | Confirmed names, roles, year | About, bylines, Person schema |
| Contact details | info@ / Admin@; +91 only | One public set | footer, About, Contact, FAQ, schema |
| Certification stance | 'IGI Certified', 'IGI / GIA', per-product 'IGI certified GH / VVS' | Which labs, which products, report available? | Home, Bespoke, PDP, FAQ, EDU-CERT pages |
| Shipping / returns / warranty | Contradictory or placeholder | Final policies | Header badge, Home, PDP, FAQ, policy pages |
| Authorship of articles | 'House of Diams Jewellery Team', 'HOD Team', 'Krish Babriya, Co-founder' | ADOPTED (OD-11): 'House of Diams' organization byline; a named person only where identity, role and credentials are verified; visible byline and schema must match | All articles, schema |
| Sources | Few external citations | Cite GIA/IGI/standards bodies for factual claims; visible 'last updated' | Education pages |

**Site-level GEO actions:** keep `/llms.txt` accurate and regenerated after AWS (it lists ~50 of 184 products and the empty `/collection`; it is optional and not a ranking factor); keep the robots.txt AI-crawler allowances only as a deliberate decision; one fact source mirrored in About/FAQ/schema/llms.txt; never state an unconfirmed HOD fact (bespoke timing = typically 2–3 weeks + ~6–9 days delivery, ~3–4 weeks, stone-dependent, never a guarantee).

## 5. Image & alt-text SEO

| Image class | Needed? | Rule |
|---|---|---|
| Product gallery images | Audit rendered DOM; alt where missing | `<product name>, <view>` (e.g. "Oval Marquise Diamond Engagement Ring, side view"); first image is primary; no keyword stuffing; don't invent visual facts (stone origin/certification) |
| Category/hub hero & tiles | Yes | Describe what the image shows or the category it links to; decorative flourishes `alt=""` |
| Product cards in grids | Yes | Product name + one key attribute |
| Article diagrams, charts, tables-as-images | Yes (Education/Blog) | Describe the information, not "chart"; keep real data in HTML tables |
| Craft/bespoke/workshop photography | Yes | Real HOD photos only, descriptive alt; no stock images implying HOD work |
| UI icons, badges | Decorative | `alt=""` (they inflate the missing-alt counts) |
| Open Graph / schema `image` | Yes | Absolute, stable URLs; must resolve after AWS |

Observed (initial HTML, includes icons/lazy images — treat as a **flag to audit the rendered DOM**, not a defect count): /: 46 imgs / 14 without alt; /engagement-rings: 80 imgs / 46 without alt; /fine-jewellery/earrings: 77 imgs / 43 without alt; /shop/oval-floral-diamond-ring: 51 imgs / 25 without alt; /bespoke: 25 imgs / 14 without alt. **Do not rename image files. Do not change the image hosts before AWS.** After AWS: keep old Supabase/R2 URLs resolving or 301 (Google Images), update Product/BlogPosting `image`, OG tags and `/llms.txt`.

## 6. Validation checklist (Class C, after AWS)

Rich Results Test + Schema.org validator on: home, 1 category, 1 subcategory, 3 PDPs (different categories), 2 articles, /faq, /returns, /about, /bespoke. Check: no FAQPage outside /faq (if kept at all), BreadcrumbList on articles/PDP matches visible path, Product `name`/`sku`/`price`/`priceCurrency: USD` correct for a US/Googlebot request (geo/currency cookies are set from IP), `image` URLs 200, one Organization `@id`, author consistent. Search Console: confirm the "Search generative AI" setting is not excluding the property (GSC access currently unavailable → VERIFY).
