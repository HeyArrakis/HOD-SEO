# Platform snapshot — 2026-11-01

Read in the owner's Chrome. Read-only: no setting was changed. This file is the baseline for the next audit.

## Google Search Console (domain property `sc-domain:houseofdiams.com`)

### Performance, last 3 months (31 Jul – 30 Oct 2026)

| Metric | Value |
|---|---|
| Clicks | 219 |
| Impressions | 20,400 |
| CTR | 1.1 % |
| Avg position | 23.9 |

- **Brand vs non-brand** (query table, 1,000 rows):

  | | Clicks | Impressions |
  |---|---|---|
  | Brand ("house of diams" and variants) | 143 | 1,052 |
  | Non-brand (987 queries) | **6** | **12,411** |

- **Non-brand positions:**

  | Position | Queries |
  |---|---|
  | 1–3 | 20 |
  | 4–10 | 181 |
  | 11–20 | 119 |
  | 21–50 | 515 |
  | 50+ | 152 |

- **Top non-brand queries by impressions:**

  | Query (variants) | Impressions | Position |
  |---|---|---|
  | lab grown diamonds vs natural diamonds | 1,061 | 27 |
  | lab grown vs natural diamond | 705 | 26 |
  | lab grown vs natural diamonds | 351 | 30.8 |
  | difference between lab grown and natural diamonds | 195 | 31 |
  | how to layer necklaces | 172 | **3.3, 0 clicks** |
  | what finger does a wedding ring go on | 123 | 39 |
  | pave engagement rings | 121 | 73 |

- **Striking distance (position 4–20, by impressions):**
  - how to layer necklaces (172, 3.3)
  - aurevelle (103, 6.6)
  - diamond shapes (39, 11.1)
  - push present (37, 18)
  - best engagement rings (28, 7.4)
  - best engagement ring styles (26, 10.5)
  - diamond gift for wife (22, 9)
  - is 14k diamond good (22, 11.5)
  - best lab created diamond engagement rings (20, 4.7)
  - heart shaped bridal sets (20, 5.3)
  - why 18k gold is used in diamond jewellery (19, 9.7)
  - best lab grown diamonds (17, 3.4)
- **Pages:** 245 rows, of which **199 are `www.` URLs** carrying 18,330 impressions. These are from before the 31 Oct 301; impressions move to the apex URLs over time.

  | Page | Impressions | Position | Clicks |
  |---|---|---|---|
  | `/blog/lab-grown-vs-natural-diamonds-the-honest-comparison-house-of-diams` | 6,256 | 26.5 | 4 |
  | `/` | 1,681 | 6.9 | 166 |
  | `/blog/14k-vs-18k-gold-for-diamond-jewellery-which-is-better-house-of-diams` | 1,142 | 11.6 | 4 |
  | `/blog/what-finger-does-a-wedding-ring-go-on` | 1,133 | 39.8 | 0 |
  | `/blog/how-to-find-your-ring-size-at-home-complete-ring-size-guide-house-of-diams` | 1,049 | 27.5 | 3 |
  | `/blog/cvd-vs-hpht-lab-grown-diamonds-what-buyers-should-know-house-of-diams` | 921 | 32.5 | 2 |
  | `/blog/the-best-lab-grown-diamond-shapes-for-engagement-rings-house-of-diams` | 845 | 8.2 | 1 |
  | `/engagement-rings/by-desgin/pave` (now 301 → `/by-design/pave`) | 487 | 70.9 | — |
  | `/blog/the-4cs-of-lab-grown-diamonds-explained…` | 321 | 8.7 | 1 |

  This table is the **baseline for the refresh articles** that were waiting on Search Console data (Step 2 status `GSC BASELINE REQUIRED`).

### Indexing (data as of 23 Oct)

148 pages indexed, 453 not indexed:

| Reason | Pages | Detail |
|---|---|---|
| Page with redirect | 101 | |
| Crawled – currently not indexed | 190 | 139 are `www/_next/image` resizer URLs; about 50 are real pages (some product pages, by-design and fine-jewellery option pages, newer blog posts) |
| Discovered – currently not indexed | 113 | All old `www` URLs |
| Excluded by noindex | 18 | |
| 404 | 14 | Old `by-desgin` URLs (now 301), `/b2b`, `/education/education-copy`, 3 old test or timestamped product slugs, `/$`, `/&`, `/house-of-diams-favicon.ico` |
| 5xx | 5 | Old blog URLs `/blog/cvd-vs-natural-diamonds`, `/blog/choosing-your-engagement-ring`, `/blog/hip-hop-jewellery-culture-meets-craft`, `/blog/surat-diamond-capital`, `/blog/the-4cs-decoded-simply`. **They return 404 now, with no 301.** |
| Alternative page with canonical | 8 | |
| Blocked by robots | 2 | |
| 403 | 1 | |
| Redirect error | 1 | |

### Other reports

- **Sitemaps:** only `https://www.houseofdiams.com/sitemap.xml` is submitted (read 1 Nov, 246 URLs, success). The apex sitemap is not submitted.
- **Experience:** Core Web Vitals "No data" (not enough Chrome traffic for CrUX). HTTPS: 70 good, 0 bad.
- **Shopping (as of 30 Oct):** product snippets 22 valid / 0 invalid; merchant listings 22 valid / 0 invalid. Warnings on 22 items: missing `hasMerchantReturnPolicy` and missing `shippingDetails` (both added on 31 Oct, so these need "Validate fix"), and **duplicate field `material`** (still live).
- **Enhancements:** breadcrumbs 62 valid / 0 invalid.
- **Manual actions:** none. **Security issues:** none.
- **Links:** 5 external links from 3 sites (scamadviser.com, sonderai.agency, deepnlp.org); 5,388 internal links.

## GA4 (property `a399123979 / p543052053`)

- **Last 7 days:** 33 active users, 110 sessions, 1K events, 16 key events.
- **Last 28 days (4–31 Oct):**
  - **Events:** 4,768 in total.

    | Event | Count |
    |---|---|
    | user_engagement | 1,769 |
    | page_view | 1,685 |
    | session_start | 522 |
    | scroll | 515 |
    | first_visit | 150 |
    | add_to_cart | 51 |
    | form_start | 42 |
    | click | 33 |
    | file_download | 1 |

  - **No** `view_item`, `begin_checkout`, `purchase` or `generate_lead`.
  - **Revenue ₹0.00.** The property currency is **INR**.
- **Session sources:**

  | Source | Sessions |
  |---|---|
  | (direct) | 214 |
  | google / organic | 132 |
  | **accounts.google.com / referral** (the login flow, which should be excluded) | 82 |
  | **chatgpt.com / ai-assistant** | **46** (10 users) |
  | search.google.com / referral | 37 |

- **Top cities:** Surat 46, Satara 27, i.e. internal traffic that is not filtered.
- **Realtime (1 Nov):** `page_view` arrives (6 in 30 minutes).

## Google Tag Manager (`GTM-TJ5HTTSD`, workspace 7)

- **Tags (4):** Conversion Linker (All Pages), "GA4 - houseofdiams.com" Google tag (Initialization – All Pages), Microsoft Clarity (All Pages), Pinterest Tag 2613658569447 (All Pages).
- **No GA4 event tags and no custom-event triggers**, so the site's dataLayer ecommerce and lead events never reach GA4.
- Clarity and Pinterest have no consent requirement. Lighthouse flags them as third-party cookies set before consent.

## Ahrefs (free plan)

| Project | Health | DR | Referring domains | Organic (est.) |
|---|---|---|---|---|
| Apex `*.houseofdiams.com` | **100** (0 errors, 71 warnings, 611 notices) | **4** | 734 | 19 visits/month, 8 keywords |
| Old `www` project | 69 | — | 2 | — |

- **Apex project details:** AI Discoverability score **100** (crawl in progress on 1 Nov; 702 URLs).
- **New warning:** "Structured data has Google rich results validation error" on **182 product pages**: `Missing required deliveryTime property` in `OfferShippingDetails`.
- **Each product's JSON-LD** lists 249 countries in `applicableCountry` and 249 `shippingDestination` entries (about 15 KB of JSON-LD per product page).
- **Referring domains:** of the top 50 by DR, **46 are flagged SPAM** (buybacklinks.agency, seoexpress.shop, thebacklinks.shop …). Non-spam: scamadviser.com (DR 81), crunch.id (DR 60).

## Google Merchant Center (account 5837491424)

- **Products:** 236, all approved (0 limited, 0 disapproved). The site feed `/feeds/google-products.xml` has 182 items, so **about 54 extra products** in Merchant Center are from another source.
- **Clicks (28 days):** 90 free-listing clicks.
- **Store quality:** "Missing signals" for the United States, Australia and India.
- **Shipping:** policies set for all countries, "Standard Free Shipping".
- **Returns:** the policy "Standard for United Arab Emirates +101 more" is **Rejected**: "Return information provided does not match your online store". It states **15 days, customer pays shipping + 35 % restocking fee**. The fee is not on the site and is not a confirmed fact.
- **Feed:** handling time 10–14 days (not confirmed by the owner); availability `in_stock`; condition `new`; mpn present; `identifier_exists` set; material = the default metal.

## Google Business Profile

- 1 business, **verified**: "House of Diams", service-area business ("Canada, France and 5 other areas").
- **Category:** Jewelry manufacturer.
- **Website:** set.
- **Phone:** **missing** ("Add place's phone number").
- **Hours:** "Open 24 hours".
- **Reviews:** **none** ("Get reviews").
- **Photos:** it prompts "Add photos".
- **Products:** synced.
- **Pending:** 1 "Google update" to review.

## Bing, Pinterest, IndexNow

- `msvalidate.01` and `p:domain_verify` meta tags are present.
- An IndexNow route exists (`app/api/cron/indexnow`); its schedule is not confirmed.
