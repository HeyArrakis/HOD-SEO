# BC-018 — SEO Metadata

**Source:** `blogs/bc-018/BC-018-anniversary-gifts-by-year-traditional-and-modern.md` §2 and `blogs/bc-018/BC-018-qa.md`.

| Field | Value | Which CMS field sets it |
|---|---|---|
| **SEO title** | Anniversary Gifts by Year: Traditional and Modern | **Article Title.** The site template adds " \| House of Diams", so it renders as "Anniversary Gifts by Year: Traditional and Modern \| House of Diams" (66 characters). |
| **H1** | Anniversary Gifts by Year: The Traditional and Modern List (and Where Diamonds Fit) | **Display Title** |
| **Meta description** | Anniversary gifts by year: the full traditional and modern list, from paper for the 1st to diamond for the 60th, plus the diamond, gold and platinum years. (155 characters) | **Short Intro** |
| **URL slug** | `/blog/anniversary-gifts-by-year-traditional-and-modern` | Generated automatically from **Article Title** on the first save, and fixed after that |
| **Canonical** | Generated automatically by the site for the slug | — |
| **Author (byline)** | HOD Team | **Written By** |

## Target keywords (9)

**Primary**
1. `anniversary gifts by year` (74000/mo US; KD 11)

**Secondary**
2. `traditional anniversary gifts` (9900)
3. `modern anniversary gifts by year` (1000)
4. `what anniversary is diamond` (1300)
5. `diamond anniversary` (2900)
6. `60th anniversary diamond` (140)
7. `what is the 50th anniversary gift` (590)
8. `what is the 60th anniversary gift` (260)
9. `anniversary jewelry` (1600)

Volumes are US monthly figures from the calendar (DataForSEO research rounds R0–R3). KD is DataForSEO's third-party difficulty estimate, not a ranking probability. No keywords outside the calendar row are targeted.

## Search intent

INFORMATIONAL (SERP-verified INFORMATIONAL: by-year guides from The Knot, NYT, Wikipedia, Jared, Helzberg). Commercial intent: HIGH (eternity/anniversary bands, fine jewelry). Funnel: AWARENESS.

## SERP / AEO notes (from existing research; no new paid calls)

- **SERP:** INFORMATIONAL. Berkshire Ridge, The Knot, Wikipedia, NYT, Historic Newspapers, Jared, Helzberg.
- **AIO:** Early years (1–10) list, then milestone years (15–60).
- **PAA:** anniversary for each year; normal anniversary gifts; 5 years called; off-topic items (wedding-gift budget, longest marriage).
- **AEO approach:** definition-first; one full table; one-sentence answers for diamond, gold, 60th and platinum questions under their own H2s.

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
