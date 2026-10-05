# BC-001 — QA Record

**Article:** How Long Does a Custom Engagement Ring Take? From Design to Delivery
**File:** `blogs/BC-001-how-long-does-a-custom-engagement-ring-take.md`
**QA date:** 2026-10-04 (updated the same day after HOD owner confirmation)
**Status:** **READY FOR FINAL HUMAN REVIEW — BUSINESS FACTS CONFIRMED**
(previously: READY FOR HUMAN REVIEW — BUSINESS FACT CONFIRMATION REQUIRED)
**Paid DataForSEO calls:** none ($0.00). This draft uses only existing project research.
**Published:** no. The article awaits final human review; nothing has been sent to the CMS.

---

## 1. Confirmed HOD business facts (HOD owner, 2026-10-04)

| # | Fact | Confirmed wording |
|---|---|---|
| 1 | Customer-facing timeline | **3–4 weeks on average, from design approval to delivery** |
| 2 | Production | **2–3 weeks**, covering the full production process: CAD development, diamond selection and sorting, ring making, quality checks, polishing, packaging |
| 3 | Shipping | **An additional 6–9 days** of insured shipping from the HOD facility to the customer's doorstep |
| 4 | Before the timeline | Initial enquiries and consultations happen **before** the timeline starts. The production timeline begins once the customer approves the design. For a new bespoke design, the process can include sketching, a dedicated CAD model, diamond selection and sorting, ring making, quality checks, polishing, packaging and insured delivery. |
| 5 | 4–6 weeks | **Not** the standard HOD estimate |
| 6 | Timeline start | When the customer **approves the design** |
| 7 | Holiday | **No confirmed** Christmas/holiday order-by cutoff. The workshop continues operating over Christmas. Shipping may take longer because of holiday transport delays. No specific date is to be given. |
| 8 | Author | Byline **HOD Team**. Bio: "The team behind House of Diams shares insights into bespoke engagement rings, diamond selection, and the process of bringing a ring design to life." |

The article also keeps "can vary depending on the stone selected". This comes from the original confirmed fact (2026-09-29; CLAUDE.md) and wasn't withdrawn by the new confirmation.

## 2. Timeline conflict: RESOLVED

| Before | Resolution |
|---|---|
| Confirmed fact said ~3–4 weeks with no start point; live /bespoke said "4-6 week typical lead time" | HOD confirms that **3–4 weeks from design approval to delivery** is the correct customer-facing average, and that 4–6 weeks is not the standard estimate. The article uses 3–4 weeks throughout and contains no 4–6 week figure. |
| The draft implied design and stone selection were extra time on top of the 3–4 weeks (lines 22, 43, 78, 117 and 130 of the previous draft) | Corrected. Inquiry, consultation and design development are described as happening **before** the clock starts. CAD, diamond selection and sorting, making, QC, polishing and packaging are described as **inside** the 2–3 week production period. |

## 3. Required verifications

| Check | Result | Where |
|---|---|---|
| 3–4 weeks is the average from design approval to delivery | ✅ | Opening answer, table total row, "Making time vs. delivery time", step-by-step intro, factors table, holiday step 2, custom vs ready-to-buy table, conclusion, meta description, JSON-LD description, graphic spec |
| 2–3 weeks is production (CAD, diamond selection and sorting, making, QC, polishing, packaging) | ✅ | Table row 3, "Production" bullet, steps 3–4, "How is a diamond ring made?" intro, "rushed" H3 |
| 6–9 days is insured shipping | ✅ | Table row 4, "Insured shipping" bullet, step 5, meta description |
| 4–6 weeks isn't presented as the standard | ✅ | No 4–6 figure in the article. It appears only in the editor note about the live /bespoke page. |
| The timeline starts at design approval, not at inquiry | ✅ | Opening para 3, table row 2, "When does the clock start?", steps 1–2, factors row "Reaching design approval", holiday steps 2–3, custom vs ready-to-buy row, conclusion, graphic spec ("never show it as starting at inquiry") |
| Design/stone selection isn't presented as extra time after the 3–4 weeks | ✅ | "on top of" and "plus your design and stone decisions" are removed. The line under the table says diamond selection and sorting "are already part of the 3–4 weeks". |
| No invented stage durations | ✅ | Inquiry/consultation and design development are "no set length". No duration is given for CAD, diamond selection or any other sub-step. |
| No holiday cutoff | ✅ | "This is planning guidance, not an order-by date." No date is given anywhere. |
| Workshop operates over Christmas | ✅ | Holiday section |
| Holiday shipping delays possible | ✅ | Step 5, factors row "Holiday shipping", holiday section |
| "December is a busy period for jewelers and shipping carriers" removed | ✅ | Replaced by the confirmed holiday-shipping row |
| "starting in the fall rather than in December" replaced | ✅ | Now reads: "Start well ahead of your proposal date rather than leaving the order until December." |
| Author is HOD Team | ✅ | Byline under the H1, "About the author" box with the confirmed bio verbatim, JSON-LD `author` |
| No individual author implied | ✅ | JSON-LD author is an `Organization` named "HOD Team" (a team, not a `Person`) |
| No timeline presented as a guarantee | ✅ | Every figure carries "on average", "typically", "approximately" or "about". "Guarantee" appears only in denials: "not a guaranteed date", "averages, not guarantees", "an average, not a guarantee". |

## 4. Full consistency pass

| Element | Result | Notes |
|---|---|---|
| Article body | ✅ | Searched for "3–4 weeks", "2–3 weeks", "6–9 days", "4–6", "design", "stone", "delivery", "timeline", "fall rather", "busy period", "on top of", "plus your design", "cutoff", "order-by" and "Person". No outdated or contradictory statement remains. |
| H1 / SEO title | ✅ Unchanged | "From Design to Delivery" is consistent with the approval-to-delivery timeline. The title makes no timeline claim. |
| Meta description | ✅ Updated | "A House of Diams bespoke ring takes 3–4 weeks on average from design approval to delivery: typically 2–3 weeks of production, then 6–9 days of insured shipping." (160 characters) |
| Timeline table | ✅ Restructured | 1 Inquiry & consultation (before the timeline) → 2 Design development & approval (the timeline starts) → 3 Production, typically 2–3 weeks → 4 Insured shipping, ~6–9 days → total 3–4 weeks on average |
| Timeline graphic spec and alt text | ✅ Updated | Shows design approval as the start point, with production and shipping split |
| Visual 3 | ✅ Updated | It's now "CAD model beside the finished ring", placed at step 3. It no longer claims the CAD is approved before making. |
| Byline / author box | ✅ | HOD Team plus the confirmed bio |
| BlogPosting schema | ✅ | Author `Organization` "HOD Team"; the description matches the meta description. FAQPage/HowTo/Product are still excluded. |
| Internal links | ✅ Unchanged | 5 live links (`/bespoke` CTA and `/blog` breadcrumb are REQUIRED; plus `/about`, the shapes guide and `/engagement-rings`), and 2 conditional links (EDU-RJG-01, EDU-MET-00) |
| CTA | ✅ | "Start your own commission" → `/bespoke`. The conclusion now states the 3–4 weeks from approval. |
| Structure | ✅ Preserved | Same H2 order. Step H3s 3–5 are renamed to match the confirmed production sequence ("CAD model and diamond selection", "Making, quality checks and finishing", "Insured delivery"). |
| Topic, keywords, intent, ownership, calendar | ✅ Unchanged | |
| Word count | ~1,865 article words (was ~1,650) | The increase is the stage-by-stage clarification and the author box; there's no padding. |

## 5. Fact-check log (current draft)

| Statement | Basis | Verdict |
|---|---|---|
| 3–4 weeks on average from design approval to delivery | HOD owner confirmation, 2026-10-04 | ✅ |
| Production typically takes 2–3 weeks and covers CAD, diamond selection and sorting, making, QC, polishing and packaging | HOD owner confirmation | ✅ |
| Approximately 6–9 days of insured shipping from House of Diams to your door | HOD owner confirmation ("from the HOD facility to the customer's doorstep") | ✅ |
| For a new bespoke design, production includes sketching and a dedicated CAD model | HOD owner confirmation | ✅ |
| Inquiry, consultation and design development happen before the timeline; "no set length" | HOD owner confirmation (no duration given, so none stated) | ✅ |
| Can vary depending on the stone selected | Original confirmed fact (2026-09-29) | ✅ |
| The workshop continues operating over Christmas; holiday transport delays can lengthen shipping | HOD owner confirmation | ✅ |
| Industry quotes range from about 4–12 weeks, and some workshops quote several months | Stage R2 SERP (AIO; morgancojewellery; diamondateliers; gerardmccabe) | ✅ Unchanged |
| Generic making steps (wax/resin model, lost-wax casting, assembly, setting, finishing) | BC-010 AIO; framed as "methods vary by jeweler" | ✅ Not attributed to HOD |
| "In general", complex details add making steps | AIO; framed as general | ⚠️ General industry statement, kept as "in general". The generic stone-sourcing claim ("a specific shape, size or quality can take longer to source") was **removed** in the 2026-10-04 cleanup; the factors table keeps only the confirmed "can vary depending on the stone selected". |
| Cost is influenced by choices such as the stone, the metal and the complexity of the design | General; no ranking of components | ✅ The unsupported claim "the stone (often the largest part of the price in a diamond ring)" was **removed** in the 2026-10-04 cleanup |
| Author: HOD Team plus the bio | HOD owner confirmation (bio verbatim) | ✅ |
| No HOD claims about certification, Surat, sourcing, insurance terms beyond "insured shipping", countries served, consultation fees, rush service or awards | — | ✅ None made |

## 6. Remaining items for human review

| # | Item | Severity | Notes |
|---|---|---|---|
| 1 | **Live /bespoke page still says "4-6 week typical lead time"** | HIGH (website, not article) | HOD confirms this isn't the standard estimate. Until the page is corrected, the article and its CTA destination disagree. Correcting it is a website edit, so it needs the user's explicit go-ahead and is outside this task. |
| 2 | **Live /bespoke page says "Full CAD rendering approved by you before a single stone is cut"** | MEDIUM (website, not article) | The confirmed sequence puts CAD development inside production, after design approval. The article follows the confirmed sequence and doesn't say whether the customer reviews the CAD model. HOD may want to align the /bespoke wording, or confirm whether customers see the CAD during production. |
| 3 | `content-strategy/blog-calendar/revision/confirmed_business_facts.md` still holds the 2026-09-29 wording (no start point, no stage breakdown) | LOW | Not modified, because research files are out of scope. Consider updating it with the user's approval so future posts (BC-004, BC-014, BC-017, BC-034 and others) use the confirmed approval-to-delivery framing. |
| 4 | Original images | LOW | Visuals 1, 3 and 4 need real HOD photography. Otherwise publish with the timeline graphic only. |
| 5 | Schema placeholders | LOW | `[LOGO_URL]`, `[PUBLISH_DATE]`, `[LAST_MODIFIED_DATE]`, `[HERO_IMAGE_URL]` and `[FINAL_SLUG]` are filled at publish time. |
| 6 | Conditional links | LOW | EDU-RJG-01 and EDU-MET-00 aren't live yet; publish their anchors as plain text. |

## 7. Conflicts

- **Calendar/architecture:** none. Topic, date, keywords, intent and ownership are unchanged.
- **Business facts:** the article-level conflict is resolved. Website-level inconsistencies on /bespoke remain (§6 items 1–2).
- **Cannibalization:** none identified.
