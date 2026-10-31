# CMS changes — 2026-10-31

**What this is:** a log of the content changes made directly in the House of Diams admin (`manage.houseofdiams.com`). They were made at the owner's request on 2026-10-31, in Chrome while signed in as the owner. Each change has its before/after text so it can be undone. These changes are **not** developer work and are deliberately left out of `DEVELOPER-HANDOFF/05-…`.

**Rule applied:** only confirmed HOD facts (`Keywords/content SEO/content-strategy/blog-calendar/revision/confirmed_business_facts.md`). Unconfirmed claims were removed, never replaced with guesses. No URL slug was changed: every name edit that auto-regenerated a slug was set back to the original before saving.

**Live check after saving:** `post_cms_scan_2026-10-31.json` is a fresh scan of all 246 sitemap URLs. It found 0 pages with "30 days", "UPS", "craftsmanship warranty", "2-3 business days", the old "Rose gold" label, a `www.` hero link or the `uat.` top-bar link. `/t-bar` still returns 200. Krish Babariya's founder slide renders with photo and bio.

## 1. Changes made and verified live

| # | CMS place | Before | After | Fixes (05 ID) |
|---|---|---|---|---|
| 1 | Catalog Setup → Policies → **Standard Shipping** (body) | "Worldwide insured shipping is complimentary. In-stock pieces usually ship within 2-3 business days. Made-to-order pieces vary by complexity and destination. Duties and taxes may apply depending on the delivery country." | "Free, insured overnight shipping to every country, with no order cut-off time. Made-to-order pieces vary by complexity and destination. Duties and taxes may apply depending on the delivery country." | O-01 |
| 2 | Catalog Setup → Policies → **Standard Care & Warranty** (body) | "… Every House of Diams piece includes a craftsmanship warranty and support for care guidance." | "… Every House of Diams piece includes a free lifetime warranty, free resizing and free annual cleaning." | O-01 |
| 3 | CMS → **Service Banner** → block 1 (shown on every product page) | Title "complimentary shipping & returns"; text "We offer complimentary UPS Overnight shipping on items available for immediate purchase. Learn more / Enjoy complimentary returns on items returned within 30 days of delivery. Learn more" | Title "complimentary shipping & 15-day returns"; text "We offer free, insured overnight shipping to every country, with no order cut-off time. Learn more / Returns are accepted within 15 days of delivery for unworn pieces; return shipping and duties are paid by the customer. Learn more" | O-01 |
| 4 | **Coupons** → HOUSEOFDIAMS2026 (title) | "September sale" (the free-gift offer runs 1 Sep – 31 Dec 2026) | "Free gift offer" (offer, gift, minimum and dates unchanged) | O-02 |
| 5 | CMS → About → **Founders** | "Akshar korat" / "co founder"; "Krish" / "Founder" / bio "Bio" (placeholder) | "Akshar Korat" / "Co-founder"; "Krish Babariya" / "Founder" / bio "Krish Babariya founded House of Diams together with Akshar Korat. The business has been in the diamond trade since 2014 and works from Surat, India." | O-05 |
| 6 | CMS → About → **Timeline** | 2018 "New York office opens"; 2020 "Established networks in 20+ countries" | Both rows deleted (to restore: add them back with the same year and label) | O-05, S-02 |
| 7 | CMS → About → **Values** | "Conflict Free" and "Ethically" cards; "Certified Jewelry" text was a product description ("A 1.00-carat marquise-cut lab-grown diamond …") | Both cards deleted; "Certified Jewelry" text = "Our pieces come with IGI or GIA certificates." | O-05 |
| 8 | CMS → Contact → **Contact Info** card 3 | Label "Atelier . India"; value "Surat, Gujarat india"; note "India · Headquarters & Workshop · By appointment only PRAGATI IT WORLD, 831,  yogi chowk, Surat, Gujarat 395010" | "Atelier · India"; "Surat, Gujarat, India"; "India · Headquarters & Workshop · By appointment only · 831, Pragati IT World, Yogi Chowk, Surat, Gujarat 395010" | O-06 (footer "india") |
| 9 | CMS → Support → **Announcement Bar** | "Free Worldwide Shipping" linked to `https://uat.houseofdiams.com/fine-jewellery/earrings/stud-earrings` (a test host); "Fine Jwelery Available" | Link `/shipping`; "Fine Jewelry Available" | O-07 |
| 10 | CMS → Home → **Hero** slide 1 | Button link `https://www.houseofdiams.com/engagement-rings`; paragraph "Discover Engagement rings , Crafted for Your Love Story" | `/engagement-rings`; "Discover engagement rings, crafted for your love story" | T-08 |
| 11 | Catalog Setup → Categories → **T- BAR** | Name "T- BAR" (slug `t-bar`) | Name "T-Bar" (slug `t-bar`, link `/t-bar` unchanged) | O-06 |
| 12 | Catalog Setup → **Metals** | "10K Rose gold" (purity "10k", label "10k Rose gold"); "Rose gold" 14K | "Rose Gold", purity "10K", label "10K Rose Gold"; "Rose Gold" 14K (slugs `10k-rose-gold` / `14k-rose-gold` unchanged) | O-06, S-01 (material values) |

## 2. Second CMS session (31 Oct, afternoon, after the developer's last release)

Same rules: confirmed facts only, US English, no slug changed (every option rename was checked: slug identical before and after). Saved in the admin and read back; "Live" = seen in the public HTML.

| # | CMS place | Before | After | Live |
|---|---|---|---|---|
| 13 | Navbar Builder → T-Bar (re-saved) | Menu label "T- BAR " (stale copy) | "T-Bar" | Yes |
| 14 | Navbar Builder → Bespoke | Hidden | Visible in the menu (`/bespoke`) | Yes |
| 15 | Catalog → Fine Jewelry → Options | "Toi-et moi" (`toi-et-moi`); "Multi stone" (`multi-stone`) | "Toi et Moi"; "Multi-Stone" (slugs unchanged) | Yes |
| 16 | Catalog → Engagement Rings → Options | "Toi-moi Rings" (`toi-moi-rings`) | "Toi et Moi Rings" (slug unchanged) | Yes |
| 17 | Catalog → Wedding Bands → Options | "solid" (`solid`); "pavé" (`pavee`) | "Solid"; "Pavé" (slugs unchanged) | Yes |
| 18 | Bespoke → Form Settings → Guarantees | "Fully insured worldwide delivery — complimentary to 40+ countries" | "Fully insured delivery, free to every country" | Yes |
| 19 | Bespoke → Form Settings → Preferred Stone | "CVD Colourless Diamond", "CVD Fancy Colour Diamond" | "CVD Colorless Diamond", "CVD Fancy Color Diamond" (US English) | — |
| 20 | CMS → About → Wide Banner | Title "The Journey"; text "Discover the artistic collaboration and love story that have lasted over half a century." | "THE JOURNEY"; "Discover how House of Diams has grown since 2014." | Yes |
| 21 | Catalog → Fine Jewelry → Edit Banner (banner itself is disabled) | Title "Fine Jewellery"; subtitle "Browse Fine Jewellery from the live catalog." | "Fine Jewelry"; "Diamond earrings, rings, necklaces and bracelets, with free insured shipping to every country." | Yes (page data) |
| 22 | CMS → Home → Offer Section | "Exclusive offer" / "Get a Free Gift on" / "Get a Free Gift" / "orders over 1000$" / "Get Your Coupon Code" | "EXCLUSIVE OFFER" / "GET A FREE GIFT ON" / "GET A FREE GIFT" / "On orders over $1,000." / "GET YOUR COUPON CODE" | Saved |
| 23 | CMS → Collection (home banner) | "Collection" / button "Explore Collection" | "COLLECTION" / "EXPLORE COLLECTION" | Yes |
| 24 | CMS → Bespoke (home showcase) | "Bespoke Atelier" / "Made Only for You" / "Start Bespoke Enquiry" / alt "…bespoke jewellery showcase" | "BESPOKE ATELIER" / "MADE ONLY FOR YOU" / "START BESPOKE INQUIRY" / alt "…bespoke jewelry showcase" | Yes |
| 25 | CMS → About → Values | "Certified Jewelry", "Built to Last", "Bespoke By Nature", "Precision Crafted" | Same words in capitals | Yes |
| 26 | CMS → Service Banner (product pages) | "complimentary shipping & 15-day returns", "complimentary gift wrap", "Complimentary Shipping" | Same words in capitals | Yes |
| 27 | CMS → Blog → Blog Hero | "Stories from House of Diams" / "Discover jewellery, craftsmanship…" / "Explore Stories" | "STORIES FROM HOUSE OF DIAMS" / "Discover jewelry, craftsmanship…" / "EXPLORE STORIES" | Yes |
| 28 | CMS → Support → FAQ | Test item "Quetsion QA" / "Anaswering as QA" live on `/faq` (and in FAQPage schema) | Set to inactive (not deleted) | Yes (gone) |
| 29 | CMS → Support → FAQ | 15 questions/answers in UK spelling (jewellery, colour, centre, personalised, metre) | US spelling; links such as `/fine-jewellery` left unchanged | Yes |
| 30 | Products → Content → SEO Title (67 products) | Titles 61–77 characters rendered, SKU codes in 7 titles | ≤ 60 rendered (4 at 61): collection name, SKU and the extra "Lab-Grown" word removed; shape, product type and carat kept; all unique. Full list: `pdp_seo_titles_2026-10-31.csv` | Rolling out (server data cache, up to ~30 min per page) |
| 31 | Products → Content → On-page H1 (2 products) | Both "Round Baguette Three-Stone Ring" | "3.62 ct Round & Baguette Three-Stone Ring" / "2.62 ct Round & Baguette Three-Stone Ring" | Rolling out |
| 32 | Products → Content → SEO Meta (8 products) | Placeholder metas ("Stud Earrings · 10K White Gold - House of Diams", …) on `round-hoop-drops`, `round-solitaire-studs`, `cushion-solitaire-studs`, `radiant-halo-drops`, `round-radiant-drops`, `princess-halo-stud-earrings`; one duplicate meta on the two three-stone rings | Metas from `On-page SEO/07-PDP-PRIORITY-ACTIONS.csv`, every number checked against the product description; the two rings now name 3.62 ct / 2.62 ct | Rolling out |
| 33 | CMS → Blog → SEO title (4 articles) + Education → SEO title (1) | Article titles over 60 characters | Approved Step 2 titles (status READY): "The 4Cs of Diamonds Explained", "Diamond Shapes: Chart and How to Choose", "Ring Size Chart: How to Measure Your Size", "What a Lab-Grown Diamond Certificate Shows", "GIA vs IGI Lab-Grown Diamond Certification" (the two certificate titles ship together). Article titles and URLs unchanged | 4Cs live; rest rolling out |

**Checked and not needed:**
- **"6 orphan products" (old item i).** All six already have a category. They are listed on page 2–3 of their category pages, for example `east-west-oval-diamond-bezel-pendant` on `/fine-jewellery/necklaces/solitare?page=2`. The crawl script does not follow `?page=` links, so it reported them as orphans.
- **"Why house of diams" (cart) and the Contact H1.** These are in code, not the CMS. The Contact hero in the CMS ("Let's Connect") is not used on the live page.

**Left on purpose:**
- **Founder names.** They feed the hidden site data (schema), so capitals come from CSS (TY-01).
- **The four homepage blog tiles.** Their text is each article's card title, which is also used on `/blog`; capitals come from CSS.
- **"14K vs 18K Gold" article title.** The Step 2 spec says to change it only after the Search Console baseline.
- **The 10 approved blog package titles.** Unchanged.

## 3. Found during this session (for the record)

- The admin login uses `auth-uat.houseofdiams.com` (realm `houseofdiams`, client `hod-admin`), the same UAT-named host as the customer login (05 Q-07).
- Dashboard "Top selling products" lists QA test items ("QA Batch Rounding Oct23", "UAT QA Metal Image Retest") and a hidden category "QA Batch Duplicate 20261023". None of them is in the public sitemap.
- The active home-page offer is "Diwali Offer", linked to the free-gift coupon.
- The policy text updated on all product pages within a few minutes (server-side data cache). A scan run immediately after saving still showed the old text.
- Product SEO fields refresh more slowly: about 30 minutes per product page after saving (no CloudFront caching; `cache-control: private, no-cache`).
- The Navbar Builder has no field for the featured image alt. It still reads "Fine Jewellery" after re-saving, so it moved to the code list (05 O-16).
- CMS → Summary → "Summary Info" still has the placeholder title "title for summary". The component is not placed on any public page, so nothing shows.
- The Navbar Builder lists a "Hip Hop" item (`/hiphop`) marked Visible. It does not render on the live site, so it was left alone.
