# BC-035 — SEO Metadata

**Source:** `blogs/bc-035/BC-035-10-year-anniversary-gift-ideas-tin-and-diamond.md` §2 and `blogs/bc-035/BC-035-qa.md`.

| Field | Value | Which CMS field sets it |
|---|---|---|
| **SEO title** | 10 Year Anniversary Gift Ideas: Tin and Diamond | **Article Title.** The site template adds " \| House of Diams", so it renders as "10 Year Anniversary Gift Ideas: Tin and Diamond \| House of Diams" (64 characters). |
| **H1** | 10 Year Anniversary Gift Ideas: Tin, Aluminum and the Modern Diamond Tradition | **Display Title** |
| **Meta description** | The traditional 10 year anniversary gift is tin or aluminum; the modern gift is diamond jewelry. Gift ideas for both traditions, and how to combine them. (153 characters) | **Short Intro** |
| **URL slug** | `/blog/10-year-anniversary-gift-ideas-tin-and-diamond` | Generated automatically from **Article Title** on the first save, and fixed after that |
| **Canonical** | Generated automatically by the site for the slug | — |
| **Author (byline)** | HOD Team | **Written By** |

## Target keywords (6)

**Primary**
1. `10 year anniversary gift` (33100/mo US; KD 0)

**Secondary**
2. `10 year anniversary gift traditional and modern` (2400)
3. `10 year anniversary gift for wife` (2900)
4. `anniversary gift 10th` (8100)
5. `10 year anniversary gift modern` (140)
6. `10 year anniversary gift for couple` (170)

Volumes are US monthly figures from the calendar (DataForSEO research rounds R0–R3). KD is DataForSEO's third-party difficulty estimate, not a ranking probability. No keywords outside the calendar row are targeted.

## Search intent

COMMERCIAL_RESEARCH (SERP-verified MIXED: Amazon/Etsy, retailer listicles, Reddit). Commercial intent: HIGH. Funnel: CONSIDERATION.

## SERP / AEO notes (from existing research; no new paid calls)

- **SERP:** MIXED. Amazon, Beyond Memories, Reddit, Groovy Girl Gifts, Lime & Lou; shopping features present.
- **AIO:** "tin or aluminum … modern gift is diamond jewelry", then Traditional / Modern Diamond / Sentimental sections.
- **PAA:** traditional gift; what represents 10 years; good gift; symbol; is it a big deal; what stone.
- **AEO approach:** both answers in the first sentence; traditional vs modern table; ideas mirror the AIO sections; short Q&A.

## Schema

**Recommendation:** `BlogPosting` and `BreadcrumbList`. **Not recommended:** `FAQPage` (Google no longer shows FAQ rich results, and the site would only generate it under an "FAQ" heading, which this article avoids); `HowTo` (the reader isn't completing a task with materials/steps for a rich result); `Product`/`Offer` (no product is the page's main entity); `QAPage` (not a user-answer page); `ItemList` (not needed for a guide).

**What the live site generates automatically** (from `HOD/lib/structured-data.ts`, `HOD/lib/blog-faq.ts` and `HOD/app/blog/[slug]/page.tsx`; there's no CMS field for schema):

| Element | Site output | Matches the recommendation? |
|---|---|---|
| `BlogPosting` headline / description | Article Title / Short Intro | ✅ |
| Publisher | Organization "House of Diams" with logo | ✅ |
| `FAQPage` | Generated only under a heading that reads "FAQ"/"FAQs"/"Frequently asked questions". The Q&A heading is "10th anniversary questions, answered", which doesn't match the pattern, so **no FAQPage** is generated. | ✅ |
| Author | `{"@type": "Person", "name": "HOD Team"}` | ⚠️ Recommended: `Organization` (a team, not a person). Site template issue, same as BC-001. |
| `datePublished` / `dateModified` | Uses the **Publish Date Text** string, not an ISO date | ⚠️ Same as BC-001 |
| `BreadcrumbList` | Not generated for blog posts | ⚠️ Same as BC-001 |

The three ⚠️ items are template/code issues already logged for BC-001; they can't be fixed from the CMS and don't block this post.
