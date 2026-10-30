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

## 2. Still to do in the CMS (not developer work)

Saving paused here: the auto-mode safety check stopped the next catalog save and asked for the owner's explicit OK. Nothing below has been changed yet.

| # | CMS place | Change | Fixes |
|---|---|---|---|
| a | Navbar Builder | The menu still shows "T- BAR" (the nav item keeps its own copy of the label). Re-save the item or edit its label to "T-Bar" | O-06 |
| b | Catalog → Fine Jewelry → Options | "Toi-et moi" → "Toi et Moi"; "Multi stone" → "Multi-Stone" (slugs unchanged) | O-06 |
| c | Catalog → Engagement Rings / Wedding Bands → Options | "Toi-moi Rings" → "Toi et Moi Rings"; "solid" → "Solid"; "pavé" → "Pavé" (slugs unchanged) | O-06 |
| d | Bespoke → Form Settings → Guarantees | "Fully insured worldwide delivery — complimentary to 40+ countries" → "Fully insured delivery, free to every country" | O-04 |
| e | CMS → About → Wide Banner | "Discover the artistic collaboration and love story that have lasted over half a century." contradicts "since 2014" → "Discover how House of Diams has grown since 2014." | new |
| f | Catalog → Fine Jewelry → Edit Banner | Hero title "Fine Jewellery" → "Fine Jewelry"; subtitle "Browse Fine Jewellery from the live catalog." → a real one-line intro | O-06 |
| g | Navbar Builder | Featured image alt "Fine Jewellery" → "Fine Jewelry"; show the hidden "Bespoke" item | O-06, O-15 |
| h | Products (Content step: SEO Title / H1 / Meta) | 67 product titles over 60 characters; placeholder metas (`round-radiant-drops`, `round-hoop-drops`, `round-solitaire-studs`); duplicate H1 "Round Baguette Three-Stone Ring" and duplicate metas | O-09, O-10, O-11 |
| i | Products (Basics: category / option) | Assign the 6 orphan products to their category: `elaris-emerald-twist-diamond-ring`, `east-west-oval-diamond-bezel-pendant`, `aurevane-sunburst-round-diamond-halo-stud-earrings`, `virelle-round-twist-diamond-ring`, `seraphina-oval-diamond-pendant-with-accent-bail`, `amora-heart-cut-solitaire-pendant-necklace` | O-13 |
| j | Category editors (Intro text / Buying guide) | Add a 60–120-word intro and a short buying guide on the main category pages (text from `On-page SEO/04`, facts from the confirmed list only) | GSC-03 |
| k | Blog editor (SEO title) | Shorten the blog titles over 60 characters that are **not** one of the 10 approved blog packages (the package titles stay as approved) | O-09 |

## 3. Found during this session (for the record)

- The admin login uses `auth-uat.houseofdiams.com` (realm `houseofdiams`, client `hod-admin`), the same UAT-named host as the customer login (05 Q-07).
- Dashboard "Top selling products" lists QA test items ("QA Batch Rounding Oct23", "UAT QA Metal Image Retest") and a hidden category "QA Batch Duplicate 20261023". None of them is in the public sitemap.
- The active home-page offer is "Diwali Offer", linked to the free-gift coupon.
- The policy text updated on all product pages within a few minutes (server-side data cache). A scan run immediately after saving still showed the old text.
