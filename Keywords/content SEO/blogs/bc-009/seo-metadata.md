# BC-009 — SEO Metadata

**Source:** `blogs/bc-009/BC-009-jewelry-gifts-for-your-girlfriend-diamond-ideas.md` §2 and `blogs/bc-009/BC-009-qa.md`.

| Field | Value | Which CMS field sets it |
|---|---|---|
| **SEO title** | Jewelry Gifts for Your Girlfriend: Diamond Ideas | **Article Title.** The site template adds " \| House of Diams", so it renders as "Jewelry Gifts for Your Girlfriend: Diamond Ideas \| House of Diams" (65 characters). |
| **H1** | Jewelry Gifts for Your Girlfriend: First-Christmas and Meaningful Diamond Ideas | **Display Title** |
| **Meta description** | Jewelry gifts for your girlfriend by relationship stage: first-Christmas pendants and studs, meaningful necklaces, and when a promise ring makes sense. (151 characters) | **Short Intro** |
| **URL slug** | `/blog/jewelry-gifts-for-your-girlfriend-diamond-ideas` | Generated automatically from **Article Title** on the first save, and fixed after that |
| **Canonical** | Generated automatically by the site for the slug | — |
| **Author (byline)** | HOD Team | **Written By** |

## Target keywords (5)

**Primary**
1. `jewelry gifts for girlfriend` (320/mo US; KD 0)

**Secondary**
2. `first christmas gift for girlfriend` (110)
3. `first christmas together gift` (110)
4. `necklaces for girlfriend birthday` (320)
5. `meaningful necklaces for girlfriend` (170)

Volumes are US monthly figures from the calendar (DataForSEO research rounds R0–R3). KD is DataForSEO's third-party difficulty estimate, not a ranking probability. No keywords outside the calendar row are targeted.

## Search intent

COMMERCIAL_RESEARCH (SERP-verified TRANSACTIONAL_OR_COMMERCIAL: Jared, Kay, Tiffany, Swarovski with The Knot). Commercial intent: HIGH. Funnel: CONSIDERATION.

## SERP / AEO notes (from existing research; no new paid calls)

- **SERP:** TRANSACTIONAL_OR_COMMERCIAL. Jared, Diamonds Factory, Tiffany, Reddit, Swarovski, The Knot, Kay.
- **AIO:** depends on her style and "the current stage of your relationship"; dainty necklaces, stackable rings, bracelets; tips (metal preference, match the milestone).
- **PAA:** best/good jewelry for girlfriend; 5 gift rule; 2:1:1 rule; hottest jewelry; 3 month rule.
- **AEO approach:** answer first; relationship-stage table; first-Christmas section; promise-ring hand-off.

## Schema

**Recommendation:** `BlogPosting` and `BreadcrumbList`. **Not recommended:** `FAQPage` (Google no longer shows FAQ rich results, and the site would only generate it under an "FAQ" heading, which this article avoids); `HowTo` (the reader isn't completing a task with materials/steps for a rich result); `Product`/`Offer` (no product is the page's main entity); `QAPage` (not a user-answer page); `ItemList` (not needed for a guide).

**What the live site generates automatically** (from `HOD/lib/structured-data.ts`, `HOD/lib/blog-faq.ts` and `HOD/app/blog/[slug]/page.tsx`; there's no CMS field for schema):

| Element | Site output | Matches the recommendation? |
|---|---|---|
| `BlogPosting` headline / description | Article Title / Short Intro | ✅ |
| Publisher | Organization "House of Diams" with logo | ✅ |
| `FAQPage` | Generated only under a heading that reads "FAQ"/"FAQs"/"Frequently asked questions". The Q&A heading is "More questions about jewelry gifts for a girlfriend", which doesn't match the pattern, so **no FAQPage** is generated. | ✅ |
| Author | `{"@type": "Person", "name": "HOD Team"}` | ⚠️ Recommended: `Organization` (a team, not a person). Site template issue, same as BC-001. |
| `datePublished` / `dateModified` | Uses the **Publish Date Text** string, not an ISO date | ⚠️ Same as BC-001 |
| `BreadcrumbList` | Not generated for blog posts | ⚠️ Same as BC-001 |

The three ⚠️ items are template/code issues already logged for BC-001; they can't be fixed from the CMS and don't block this post.
