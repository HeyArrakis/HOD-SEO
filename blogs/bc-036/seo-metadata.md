# BC-036 — SEO Metadata

**Source:** `blogs/bc-036/BC-036-what-finger-does-a-wedding-ring-go-on.md` §2 and `blogs/bc-036/BC-036-qa.md`.

| Field | Value | Which CMS field sets it |
|---|---|---|
| **SEO title** | What Finger Does a Wedding Ring Go On? | **Article Title.** The site template adds " \| House of Diams", so it renders as "What Finger Does a Wedding Ring Go On? \| House of Diams" (55 characters). |
| **H1** | What Finger Does a Wedding Ring Go On? (And Which Hand for the Engagement Ring) | **Display Title** |
| **Meta description** | In the US, a wedding ring goes on the fourth finger of the left hand, with the engagement ring. Why the left hand, and which countries use the right. (149 characters) | **Short Intro** |
| **URL slug** | `/blog/what-finger-does-a-wedding-ring-go-on` | Generated automatically from **Article Title** on the first save, and fixed after that |
| **Canonical** | Generated automatically by the site for the slug | — |
| **Author (byline)** | HOD Team | **Written By** |

## Target keywords (8)

**Primary**
1. `what finger does a wedding ring go on` (27100/mo US; KD 1)

**Secondary**
2. `wedding ring finger` (18100)
3. `what hand does engagement ring go on` (6600)
4. `which hand is the ring finger` (8100)
5. `what finger does a ring go on` (880)
6. `why is the wedding ring on the left hand` (880)
7. `which hand does engagement ring go on` (1300)
8. `what hand does a wedding ring go on in america` (30)

Volumes are US monthly figures from the calendar (DataForSEO research rounds R0–R3). KD is DataForSEO's third-party difficulty estimate, not a ranking probability. No keywords outside the calendar row are targeted.

## Search intent

INFORMATIONAL (SERP-verified MIXED: retailer guides, Wikipedia, Reddit). Commercial intent: MEDIUM-HIGH (wedding bands, bridal sets). Funnel: AWARENESS.

## SERP / AEO notes (from existing research; no new paid calls)

- **SERP:** MIXED. Reddit, Heller Jewelers, Wikipedia, Brilliant Earth, Vinny & Charles; perspectives and short videos.
- **AIO:** "fourth finger of the left hand", then regional differences, why the left hand (vena amoris), stacking order.
- **PAA:** left or right; married men; which finger you propose on; right hand; disrespectful not to wear; which finger means single. Hand SERP adds: right hand engagement, why left.
- **AEO approach:** US-qualified answer first; country table; history H2; one-line hand-offs to BC-007/BC-038.

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
