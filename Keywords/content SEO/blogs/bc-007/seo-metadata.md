# BC-007 — SEO Metadata

**Source:** `blogs/bc-007/BC-007-how-to-wear-an-engagement-ring-and-wedding-band.md` §2 and `blogs/bc-007/BC-007-qa.md`.

| Field | Value | Which CMS field sets it |
|---|---|---|
| **SEO title** | How to Wear an Engagement Ring and Wedding Band | **Article Title.** The site template adds " \| House of Diams", so it renders as "How to Wear an Engagement Ring and Wedding Band \| House of Diams" (64 characters). |
| **H1** | How to Wear Your Engagement Ring and Wedding Band: Order, Wedding-Day Etiquette and Soldering | **Display Title** |
| **Meta description** | Traditionally the wedding band goes on first, with the engagement ring on top. Alternatives, wedding-day etiquette and whether to solder your rings together. (157 characters) | **Short Intro** |
| **URL slug** | `/blog/how-to-wear-an-engagement-ring-and-wedding-band` | Generated automatically from **Article Title** on the first save, and fixed after that |
| **Canonical** | Generated automatically by the site for the slug | — |
| **Author (byline)** | HOD Team | **Written By** |

## Target keywords (6)

**Primary**
1. `how to wear engagement ring and wedding band` (3600/mo US; KD 0)

**Secondary**
2. `which ring goes on first wedding or engagement` (720)
3. `do you wear your engagement ring on your wedding day` (1000)
4. `does the wedding band go on first` (880)
5. `correct way proper way to wear wedding ring set` (480)
6. `should engagement ring and wedding band match` (10)

Volumes are US monthly figures from the calendar (DataForSEO research rounds R0–R3). KD is DataForSEO's third-party difficulty estimate, not a ranking probability. No keywords outside the calendar row are targeted.

## Search intent

INFORMATIONAL (SERP-verified INFORMATIONAL: Royal Asscher, Vogue, VRAI guides; Reddit; Facebook). Commercial intent: HIGH. Funnel: RETENTION.

## SERP / AEO notes (from existing research; no new paid calls)

- **SERP:** INFORMATIONAL. Royal Asscher, Reddit, Facebook, Vogue, VRAI, Brilliant Earth.
- **AIO:** Traditional order; On your wedding day; Alternative ways; Soldering vs separate.
- **PAA:** wear both all the time; wear together; which goes first; why not wear engagement ring on wedding day; which finger you propose on; 2:1:1 rule.
- **AEO approach:** order answer first; alternatives table; numbered wedding-day steps; "match" H2; soldering pros/cons table.

## Schema

**Recommendation:** `BlogPosting` and `BreadcrumbList`. **Not recommended:** `FAQPage` (Google no longer shows FAQ rich results, and the site would only generate it under an "FAQ" heading, which this article avoids); `HowTo` (the reader isn't completing a task with materials/steps for a rich result); `Product`/`Offer` (no product is the page's main entity); `QAPage` (not a user-answer page); `ItemList` (not needed for a guide).

**What the live site generates automatically** (from `HOD/lib/structured-data.ts`, `HOD/lib/blog-faq.ts` and `HOD/app/blog/[slug]/page.tsx`; there's no CMS field for schema):

| Element | Site output | Matches the recommendation? |
|---|---|---|
| `BlogPosting` headline / description | Article Title / Short Intro | ✅ |
| Publisher | Organization "House of Diams" with logo | ✅ |
| `FAQPage` | Generated only under a heading that reads "FAQ"/"FAQs"/"Frequently asked questions". This article has no heading matching that pattern, so **no FAQPage** is generated. | ✅ |
| Author | `{"@type": "Person", "name": "HOD Team"}` | ⚠️ Recommended: `Organization` (a team, not a person). Site template issue, same as BC-001. |
| `datePublished` / `dateModified` | Uses the **Publish Date Text** string, not an ISO date | ⚠️ Same as BC-001 |
| `BreadcrumbList` | Not generated for blog posts | ⚠️ Same as BC-001 |

The three ⚠️ items are template/code issues already logged for BC-001; they can't be fixed from the CMS and don't block this post.
