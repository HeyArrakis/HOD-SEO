# BC-003 — SEO Metadata

**Source:** `blogs/bc-003/BC-003-push-present-what-it-is-and-jewelry-ideas.md` §2 and `blogs/bc-003/BC-003-qa.md`.

| Field | Value | Which CMS field sets it |
|---|---|---|
| **SEO title** | Push Present: What It Is and Jewelry Ideas | **Article Title.** The site template adds " \| House of Diams", so it renders as "Push Present: What It Is and Jewelry Ideas \| House of Diams" (59 characters). |
| **H1** | Push Presents: What They Are, When to Give One, and Jewelry Ideas She'll Keep | **Display Title** |
| **Meta description** | A push present is a gift for a new mother to mark the birth of a baby. What it means, when to give one, and diamond jewelry ideas that suit life with a newborn. (160 characters) | **Short Intro** |
| **URL slug** | `/blog/push-present-what-it-is-and-jewelry-ideas` | Generated automatically from **Article Title** on the first save, and fixed after that |
| **Canonical** | Generated automatically by the site for the slug | — |
| **Author (byline)** | HOD Team | **Written By** |

## Target keywords (6)

**Primary**
1. `push present` (18100/mo US; KD 0)

**Secondary**
2. `what is a push present` (5400)
3. `push present ideas` (8100)
4. `push present meaning` (1600)
5. `when do you give a push present` (210)
6. `when did push presents become a thing` (260)

Volumes are US monthly figures from the calendar (DataForSEO research rounds R0–R3). KD is DataForSEO's third-party difficulty estimate, not a ranking probability. No keywords outside the calendar row are targeted.

## Search intent

INFORMATIONAL (SERP-verified INFORMATIONAL: Ice Carats, Robinsons, Blue Nile guides; Reddit; social). Commercial intent: HIGH. Funnel: AWARENESS.

## SERP / AEO notes (from existing research; no new paid calls)

- **SERP:** INFORMATIONAL. Ice Carats, Reddit, Robinsons, Instagram, The Bump; "what is a push present" adds Wikipedia, Blue Nile.
- **AIO:** definition, then Meaning and Purpose (recognition, timing, modern view incl. adoption/surrogacy) and Popular Gift Ideas (personalized jewelry, classic luxury, postpartum support).
- **PAA:** typical push present; average cost; how common; what to buy; how soon after birth.
- **AEO approach:** definition-first; history H2; timing table; idea H3s; practical new-mom advice; honest "not required" section.

## Schema

**Recommendation:** `BlogPosting` and `BreadcrumbList`. **Not recommended:** `FAQPage` (Google no longer shows FAQ rich results, and the site would only generate it under an "FAQ" heading, which this article avoids); `HowTo` (the reader isn't completing a task with materials/steps for a rich result); `Product`/`Offer` (no product is the page's main entity); `QAPage` (not a user-answer page); `ItemList` (not needed for a guide).

**What the live site generates automatically** (from `HOD/lib/structured-data.ts`, `HOD/lib/blog-faq.ts` and `HOD/app/blog/[slug]/page.tsx`; there's no CMS field for schema):

| Element | Site output | Matches the recommendation? |
|---|---|---|
| `BlogPosting` headline / description | Article Title / Short Intro | ✅ |
| Publisher | Organization "House of Diams" with logo | ✅ |
| `FAQPage` | Generated only under a heading that reads "FAQ"/"FAQs"/"Frequently asked questions". The Q&A heading is "More questions about push presents", which doesn't match the pattern, so **no FAQPage** is generated. | ✅ |
| Author | `{"@type": "Person", "name": "HOD Team"}` | ⚠️ Recommended: `Organization` (a team, not a person). Site template issue, same as BC-001. |
| `datePublished` / `dateModified` | Uses the **Publish Date Text** string, not an ISO date | ⚠️ Same as BC-001 |
| `BreadcrumbList` | Not generated for blog posts | ⚠️ Same as BC-001 |

The three ⚠️ items are template/code issues already logged for BC-001; they can't be fixed from the CMS and don't block this post.
