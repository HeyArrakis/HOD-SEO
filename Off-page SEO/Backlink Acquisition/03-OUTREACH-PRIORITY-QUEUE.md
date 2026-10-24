# 03 — Outreach Priority Queue

Date: **2026-10-10** · Status: **planning only — nothing has been sent, no form submitted, no account created.**
Queue ranks match the `Queue rank` column in [`01-HOD-BACKLINK-ACQUISITION-DATABASE.csv`](01-HOD-BACKLINK-ACQUISITION-DATABASE.csv). P1 = ranks 1–5; ranks 6–10 are the strongest P2 rows.

AWS classification: preparing everything in this file is **Class A (pre-AWS safe)**. Sending outreach changes nothing on the site, but every target URL must exist and stay stable, so earned links should point to the homepage or to pages whose URLs survive the migration. Re-checking those links after cut-over is **Class C**.

---

## 1. Readiness gate G0 — must clear before any outreach

No row is marked `OUTREACH_READY`, because these prerequisites are open. Editors, reviewers and scoring sites (Rings.com, Carat Brands) will look at the site, and today they would find:

| # | Prerequisite | Why it blocks outreach | Owner / reference |
|---|---|---|---|
| G0-1 | `/shipping` replaced (currently placeholder "new test black / test desc") | First thing a roundup editor or reviewer checks | HOD fact F-A1 → `On-page SEO/11` |
| G0-2 | `/returns` publishes real terms | Same; Rings.com scores returns, deposit and cancellation | F-A2 |
| G0-3 | Unverified claims removed or confirmed ("IGI Certified", "Lifetime Warranty", "Complimentary Overnight Shipping") | An editor quoting these would publish unverified claims | F-B1, F-A3 |
| G0-4 | Company identity and a **named spokesperson** with an accurate role | Expert commentary needs a real, verifiable person; bylines currently conflict | F-C1 |
| G0-5 | One public contact email/phone | Editors need a reply route | F-C2 |
| G0-6 | `/bespoke` lead time corrected ("4–6 weeks" → the confirmed ~3–4 weeks) | Pitches cite the confirmed timeline; the site must match | User said this is in hand |
| G0-7 | AWS cut-over date or URL stability known, or pitches limited to stable URLs | Avoids earning links to URLs that will change | Engineering (`On-page SEO/12`) |

**Confirmed fact usable in every pitch:** bespoke pieces typically take **2–3 weeks to make**, then about **6–9 days for delivery**, so roughly **3–4 weeks in total**. This depends on the stone and is never a guarantee. Use "typically", "usually" or "about". Do not mention insured shipping (F-A1) and do not cite BC-001 while its publication is held.

## 2. Preparation that can start now (Class A)

1. **Brand fact sheet (one page):** only confirmed facts, plus fields reserved for F-C1/F-C2 answers. No lab names, warranty, awards or founder story until confirmed.
2. **Image kit:** product photos HOD owns, with real product names from the live catalog (e.g. Elowen Heart Halo Engagement Ring, Pear Duo Toi-et-Moi Two-Stone Engagement Ring, Solvienne East-West Marquise Diamond Ring). Confirm usage rights.
3. **Spokesperson bio draft** (for Qwoted/HARO), filled in once F-C1 is answered (see §4.3).
4. **Outreach log:** use the database. Update `Outreach status`, add the date in `Verification notes`, and never record private email content.
5. **Asset refreshes that improve pitch quality** (already scheduled in the calendar; do not reschedule): the shapes guide (EDU-SHP-00, 2026-11-13) and "Are lab-grown diamonds real?" (EDU-LG-01, 2026-12-02).

## 3. The queue

### 1 · GAP-002 — Bridal Musings, "Where to Buy Engagement Rings Online in 2026" — P1 (score 16)
- **Why it matters:** an established wedding publication with a yearly online-retailer roundup, read by engaged couples. This is HOD's core audience.
- **Evidence:** DataForSEO C3 shows the page linking VRAI, Clean Origin and With Clarity. The live check (2026-10-10) found 38 competitor links and none to HOD. HOD's domain is absent from C1.
- **Angle:** an online engagement-ring and bespoke option for the 2027 refresh, described with verified product and process facts.
- **Preparation:** G0, fact sheet, 3–4 product images.
- **Route:** `info@bridalmusings.com` (published on https://bridalmusings.com/start).
- **Next action:** after G0, send the draft in §4.1. One follow-up after about 10 days, then stop.
- **Also in scope:** GAP-003, the wedding-bands roundup on the same site. Include women's bands only (men's range unconfirmed, F-E3).

### 2 · GAP-001 — Love You Tomorrow, "The Best Online Custom Engagement Ring Designers" — P1 (score 14)
- **Why it matters:** the closest topical match to HOD's bespoke offer in the whole dataset. The article was updated 2026-09-25.
- **Evidence:** C2 shows links to Brilliant Earth, Blue Nile and Ritani. A browser check confirmed those links (`rel="noopener"`), the byline Kelly Warner, an affiliate disclosure, and no HOD mention.
- **Angle:** invite an evaluation of HOD's online bespoke process, with the confirmed timeline only.
- **Preparation:** G0 and a short bespoke process description. Only the steps HOD confirms (F-D1) — no CAD or consultation claims until then.
- **Route:** contact page https://loveyoutomorrow.com/contact-us/ (in site navigation; Cloudflare blocked scripted fetch).
- **Caveat:** the site is affiliate-funded. Inclusion may depend on an affiliate program HOD does not run. Never offer payment for inclusion.
- **Next action:** after G0, use the draft in §4.2.

### 3 · DPR-001 — Qwoted source profile — P1 (score 14)
- **Why it matters:** free and repeatable. Journalists, including bridal and lifestyle writers, ask for expert input there.
- **Evidence:** the platform is live (200) with a free sign-up route. Paid tiers exist; use the free tier only.
- **Angle:** answer only jewelry, diamond or bridal queries that HOD can support with verified facts (lab-grown basics, CVD vs HPHT, simulants vs lab-grown, ring sizing, custom-ring timelines).
- **Preparation:** G0-4 (named spokesperson) and the bio in §4.3.
- **Route:** https://app.qwoted.com/users/sign_up. **HOD or the user creates the account**; Claude does not.
- **Next action:** create the profile once a spokesperson is confirmed, then set alerts for "engagement ring", "lab-grown diamond" and "jewelry".

### 4 · GAP-004 (+ GAP-005, GAP-006) — The Plunge — P1 (score 14)
- **Why it matters:** an engagement-ring advice site for men, who are often the ring buyers. Competitor links on these pages carry no `nofollow`.
- **Evidence:** GAP-004 (online vs in-store buying) and GAP-005 (radiant-cut guide) are provider- and live-verified. GAP-006 (heart-shape guide) links to a Brilliant Earth product that DataForSEO reports as 404; this is not browser-confirmed.
- **Angle:** offer HOD's guide [How to choose a lab-grown diamond engagement ring online](https://www.houseofdiams.com/blog/how-to-choose-a-lab-grown-diamond-engagement-ring-online-house-of-diams) as a resource, plus radiant and heart product examples. Mention the dead heart-shape product link as a courtesy.
- **Preparation:** G0, a fact-check pass on that guide (Step 2 rates it "NO ACTION"; still re-read it before citing), and a browser re-check of the dead link.
- **Route:** About/Press pages (http://theplunge.com/aboutus). No public email was found.
- **Next action:** after G0, send one combined note (draft §4.4).

### 5 · GAP-012 — Munaluchi Bride, "MunaBling: 10 Unconventional Engagement Rings" — P1 (score 14)
- **Why it matters:** a US multicultural bridal publication with a recurring ring feature format.
- **Evidence:** C2 shows links to Brilliant Earth, Blue Nile, Ritani and Tiffany; the live check confirmed them.
- **Angle:** distinctive HOD designs that fit an "unconventional" brief: toi-et-moi, east-west marquise, pear-duo two-stone.
- **Preparation:** G0 and images.
- **Route:** https://www.munaluchibridal.com/contact/ (submission rules at /submissions/).
- **Next action:** after G0, send a design-led pitch (draft §4.5).

### 6 · WED-001 — Brides (expert commentary) — P2 (score 13)
- Brides publishes ring-shopping advice from experts. Reach it through journalist-request platforms (DPR-001/002), not cold email.
- Depends on G0-4. Editorial guidelines: https://www.brides.com/editorial-guidelines-5222899.

### 7 · PUB-001 — National Jeweler — P2 (score 13)
- A US trade magazine. Its contact page lists editorial staff, including Natalie Francisco (Associate Editor, Fashion) and Lauren McLemore (Associate Editor, Gemstones).
- Pitch genuine news only: a collection launch, or a Surat craft story once F-E6 is confirmed. It builds industry credibility more than consumer reach.

### 8 · DPR-002 — HARO (relaunched by Featured.com) — P2 (score 12)
- Press coverage says it was relaunched free in April 2025. The sign-up flow could not be verified by script (429 security checkpoint), so check it in a browser.
- Same rules as Qwoted: relevant queries only, verified facts only.

### 9 · ASSOC-001 — Lab-Grown Diamond Council — P2 (score 10)
- A trade body with a Retailers membership category, according to trade-press coverage. The site returned HTTP 525 on 2026-10-10.
- Next: re-check the site, current terms, fees and whether there is a public member directory. Joining is HOD's **business decision**; never imply membership before it exists.

### 10 · GAP-015 — Lab Diamond Reviews (Tom Thornbridge) — P2 (score 13)
- A lab-diamond specialist blog. Two of its "where to buy" articles link Brilliant Earth, Blue Nile, Ritani and Whiteflash (provider + live verified).
- Route: https://labdiamondsreviews.com/contact/. The author says he is affiliated with major vendors, so an affiliate program may be expected.

## 4. Draft outreach approaches (US English · not sent · placeholders in [brackets] need HOD confirmation)

Rules for every draft (openers are deliberately neutral — personalize only after actually reading the current article):
- No link request, no payment offer, no exact-match anchor request.
- One short follow-up at most.
- Every factual claim must be checked against the confirmed list on the day of sending.

### 4.1 Bridal Musings (GAP-002)
> Subject: An online engagement ring option for your 2027 "where to buy" guide
>
> Hi Bridal Musings team,
>
> I'm writing about your guide to where to buy engagement rings online, in case you're adding retailers for 2027. House of Diams is an online fine jewelry brand: engagement rings, wedding bands and custom pieces, with designs such as toi-et-moi, east-west and hidden-halo settings.
>
> If it's useful for your next update, I can share [3–4 product images], [return and shipping terms — link to /returns and /shipping once published], and how our custom process works. Custom pieces typically take 2–3 weeks to make, plus about 6–9 days for delivery, depending on the stone.
>
> [Name, role — F-C1] · [public contact — F-C2]

### 4.2 Love You Tomorrow (GAP-001)
> Subject: For your online custom engagement ring designers roundup
>
> Hi [Kelly],
>
> I read your roundup of online custom engagement ring designers (updated in September). House of Diams designs custom engagement rings online. A piece is typically made in 2–3 weeks and then delivered in about 6–9 days. The exact timing depends on the stone you choose, so we don't promise a fixed date.
>
> If you evaluate new designers, I'm happy to walk you through [the steps of our custom process — F-D1] and send images of finished pieces. No obligation, of course. Your readers' trust comes first.
>
> [Name, role — F-C1]

### 4.3 Qwoted / HARO source bio (DPR-001, DPR-002)
> [Name] is [role — F-C1] at House of Diams, an online fine jewelry brand offering engagement rings, wedding bands and custom jewelry. Available to comment on: how lab-grown diamonds are made (CVD vs HPHT), lab-grown diamonds vs simulants such as moissanite, ring sizing at home, and how long custom engagement rings typically take.

Do not add years of experience, credentials, labs, locations or awards until each is confirmed (F-C1, F-B1, F-E6).

### 4.4 The Plunge (GAP-004/005/006)
> Subject: A resource for your "buying online vs. in store" guide (and a dead link)
>
> Hi The Plunge team,
>
> I read your guide comparing buying an engagement ring online and in store. If it would help your readers, our guide [How to choose a lab-grown diamond engagement ring online](https://www.houseofdiams.com/blog/how-to-choose-a-lab-grown-diamond-engagement-ring-online-house-of-diams) walks through the online checks step by step.
>
> Separately, I noticed a product link in your heart-shape buyer's guide [no longer loads — re-confirm before sending]. If you need a replacement example, our [Elowen Heart Halo Engagement Ring] is a current heart-cut design.
>
> [Name, role — F-C1]

### 4.5 Munaluchi Bride (GAP-012)
> Subject: Unconventional engagement rings for a future MunaBling feature
>
> Hi Munaluchi team,
>
> I'm writing about your MunaBling feature on unconventional engagement rings. For a future edition, House of Diams has a few designs that fit that brief: a two-stone pear toi-et-moi, an east-west marquise solitaire and an oval with a twisted pavé split shank. I can send high-resolution images and product details [and confirm metal options — F-E4].
>
> [Name, role — F-C1]

## 5. What is deliberately **not** in the queue
- **Commerce/affiliate placements** (BuzzFeed, Fox News Deals, Krazy Coupon Lady, Grown Diamond; GAP-007/008/022/033/035) need an affiliate program. That is a business decision, and those links are `sponsored`.
- **Paid vendor guides and directories** (Style Me Pretty Little Black Book, Junebug membership, International Gem Society sponsorship) are excluded because paid listings that pass ranking credit fall under Google's link-spam policies.
- **Guest-post or sponsored-content sites** (HOLR Magazine; NewsWatchTV pending verification) are disqualified.
- **Forums** (PriceScope) are for monitoring brand mentions, not posting links.
