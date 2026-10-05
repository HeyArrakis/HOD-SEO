# BC-004 — SEO Metadata

**Source:** `blogs/bc-004/BC-004-christmas-jewelry-gifts-a-holiday-gift-guide.md` §2 and `blogs/bc-004/BC-004-qa.md`.

| Field | Value | Which CMS field sets it |
|---|---|---|
| **SEO title** | Christmas Jewelry Gifts: A Holiday Gift Guide | **Article Title.** The site template adds " \| House of Diams", so it renders as "Christmas Jewelry Gifts: A Holiday Gift Guide \| House of Diams" (62 characters). |
| **H1** | Christmas Jewelry Gifts: A Holiday Diamond Gift Guide by Budget, Recipient and Style | **Display Title** |
| **Meta description** | The best Christmas jewelry gifts are diamond studs, a solitaire pendant and a tennis bracelet. Ideas by budget and recipient, plus Hanukkah timing. (147 characters) | **Short Intro** |
| **URL slug** | `/blog/christmas-jewelry-gifts-a-holiday-gift-guide` | Generated automatically from **Article Title** on the first save, and fixed after that |
| **Canonical** | Generated automatically by the site for the slug | — |
| **Author (byline)** | HOD Team | **Written By** |

## Target keywords (10)

**Primary**
1. `christmas jewelry gifts` (390/mo US; KD 0)

**Secondary**
2. `holiday jewelry gift guide` (50)
3. `jewelry gift guide` (140)
4. `jewelry gift ideas` (260)
5. `best jewelry gifts` (110)
6. `jewelry gifts for mom` (1000)
7. `hanukkah jewelry` (140)
8. `last minute jewelry gifts` (30)
9. `jewelry stocking stuffers` (30)
10. `christmas jewelry gifts for her` (10)

Volumes are US monthly figures from the calendar (DataForSEO research rounds R0–R3). KD is DataForSEO's third-party difficulty estimate, not a ranking probability. No keywords outside the calendar row are targeted.

## Search intent

COMMERCIAL_RESEARCH (SERP-verified MIXED: retailer gift guides and category pages). Commercial intent: HIGH. Funnel: CONSIDERATION.

## SERP / AEO notes (from existing research; no new paid calls)

- **SERP:** MIXED. Top results: Jared, Oak & Luna, Shane Co. (category pages), The Jewellery Room, Gabriel & Co. (gift guides). Popular-products and images features present.
- **AIO:** "Popular Christmas Jewelry Ideas": festive novelty, personalized, and classic fine jewelry (diamond studs, tennis bracelets, gold hoops).
- **PAA:** best jewelry to give at Christmas; 5 gift rule; hottest gift/jewelry; in style in 2026; 2:1:1 rule.
- **AEO approach:** answer-first pick of three pieces; comparison table; budget table without prices; recipient H3s; dated Hanukkah answer.

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
