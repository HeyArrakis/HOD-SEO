# BC-008 — SEO Metadata

**Source:** `blogs/bc-008/BC-008-meaningful-jewelry-gifts-for-your-wife.md` §2 and `blogs/bc-008/BC-008-qa.md`.

| Field | Value | Which CMS field sets it |
|---|---|---|
| **SEO title** | Meaningful Jewelry Gifts for Your Wife | **Article Title.** The site template adds " \| House of Diams", so it renders as "Meaningful Jewelry Gifts for Your Wife \| House of Diams" (55 characters). |
| **H1** | Jewelry Gifts for Your Wife: Meaningful Diamond Pieces She'll Actually Wear | **Display Title** |
| **Meta description** | The best jewelry gifts for your wife: diamond studs, a solitaire pendant or a tennis bracelet, plus anniversary bands and ideas for the wife who has everything. (160 characters) | **Short Intro** |
| **URL slug** | `/blog/meaningful-jewelry-gifts-for-your-wife` | Generated automatically from **Article Title** on the first save, and fixed after that |
| **Canonical** | Generated automatically by the site for the slug | — |
| **Author (byline)** | HOD Team | **Written By** |

## Target keywords (5)

**Primary**
1. `jewelry gifts for wife` (320/mo US; KD 0)

**Secondary**
2. `best jewelry gifts for wife` (70)
3. `meaningful jewelry for wife` (140)
4. `christmas gifts for wife jewelry` (40)
5. `gifts for wife who has everything` (720)

Volumes are US monthly figures from the calendar (DataForSEO research rounds R0–R3). KD is DataForSEO's third-party difficulty estimate, not a ranking probability. No keywords outside the calendar row are targeted.

## Search intent

COMMERCIAL_RESEARCH (SERP-verified TRANSACTIONAL_OR_COMMERCIAL: Jared, Kay, Tiffany, Helzberg categories with The Knot and Byrdie listicles). Commercial intent: HIGH. Funnel: CONSIDERATION.

## SERP / AEO notes (from existing research; no new paid calls)

- **SERP:** TRANSACTIONAL_OR_COMMERCIAL. Jared, Mason New York, Kay, Reddit, Tiffany, The Knot, Helzberg, Byrdie.
- **AIO:** "Classic diamond stud earrings or a delicate gemstone pendant", then popular ideas (studs, personalized necklaces, stackable rings, bracelets).
- **PAA:** best jewelry for my wife; good ideas; 2:1:1 rule; wife who has everything; most unique gift; hottest gift.
- **AEO approach:** decisive answer; ideas by style; no-ring-size rule; occasion table; short Q&A.

## Schema

**Recommendation:** `BlogPosting` and `BreadcrumbList`. **Not recommended:** `FAQPage` (Google no longer shows FAQ rich results, and the site would only generate it under an "FAQ" heading, which this article avoids); `HowTo` (the reader isn't completing a task with materials/steps for a rich result); `Product`/`Offer` (no product is the page's main entity); `QAPage` (not a user-answer page); `ItemList` (not needed for a guide).

**What the live site generates automatically** (from `HOD/lib/structured-data.ts`, `HOD/lib/blog-faq.ts` and `HOD/app/blog/[slug]/page.tsx`; there's no CMS field for schema):

| Element | Site output | Matches the recommendation? |
|---|---|---|
| `BlogPosting` headline / description | Article Title / Short Intro | ✅ |
| Publisher | Organization "House of Diams" with logo | ✅ |
| `FAQPage` | Generated only under a heading that reads "FAQ"/"FAQs"/"Frequently asked questions". The Q&A heading is "More questions about jewelry gifts for your wife", which doesn't match the pattern, so **no FAQPage** is generated. | ✅ |
| Author | `{"@type": "Person", "name": "HOD Team"}` | ⚠️ Recommended: `Organization` (a team, not a person). Site template issue, same as BC-001. |
| `datePublished` / `dateModified` | Uses the **Publish Date Text** string, not an ISO date | ⚠️ Same as BC-001 |
| `BreadcrumbList` | Not generated for blog posts | ⚠️ Same as BC-001 |

The three ⚠️ items are template/code issues already logged for BC-001; they can't be fixed from the CMS and don't block this post.
