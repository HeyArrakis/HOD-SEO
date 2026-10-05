# BC-001 — SEO Metadata (approved)

**Source:** `blogs/BC-001-how-long-does-a-custom-engagement-ring-take.md` §2 and `blogs/BC-001-qa.md`. Nothing here is new.

| Field | Approved value | Which CMS field sets it |
|---|---|---|
| **SEO title** | How Long Does a Custom Engagement Ring Take? | **Article Title.** The site template adds " \| House of Diams", so it renders as "How Long Does a Custom Engagement Ring Take? \| House of Diams". This is the approved variant for a CMS that adds the brand automatically. |
| **H1** | How Long Does a Custom Engagement Ring Take? From Design to Delivery | **Display Title** |
| **Meta description** | A House of Diams bespoke ring takes 3–4 weeks on average from design approval to delivery: typically 2–3 weeks of production, then 6–9 days of insured shipping. (160 characters) | **Short Intro** |
| **URL slug** | `/blog/how-long-does-a-custom-engagement-ring-take` | Generated automatically from **Article Title** on the first save, and fixed after that |
| **Canonical** | Generated automatically by the site for the slug | — |
| **Author (byline)** | HOD Team | **Written By** |

## Target keywords (7)

**Primary**
1. `how long does a custom engagement ring take`

**Secondary**
2. `custom engagement ring process`
3. `how to design your own engagement ring`
4. `custom ring cost`
5. `how is jewelry made`
6. `how are rings made`
7. `how is a diamond ring made`

No other keywords are targeted. The commercial heads "custom engagement ring" and "design your own engagement ring" stay with `/bespoke`.

## Search intent

INFORMATIONAL (SERP-verified MIXED, led by retailer process guides). Commercial assist: HIGH (bespoke inquiry). Funnel stage: CONSIDERATION.

## Schema

**Approved recommendation:** `BlogPosting` and `BreadcrumbList`. No `FAQPage`, `HowTo`, `Product`/`Offer` or `QAPage`.

**What the live site generates automatically** (from `HOD/lib/structured-data.ts` and `HOD/app/blog/[slug]/page.tsx`; there's no CMS field for schema):

| Element | Site output | Matches the approved recommendation? |
|---|---|---|
| `BlogPosting` headline / description | Article Title / Short Intro | ✅ |
| Publisher | Organization "House of Diams" with logo | ✅ |
| `FAQPage` | Only generated if the content has a heading reading "FAQ" or "Frequently asked questions". BC-001 has none, so **no FAQPage**. | ✅ |
| Author | `{"@type": "Person", "name": "HOD Team"}` | ⚠️ The approved recommendation is `Organization` "HOD Team", because it's a team, not a named person. The site hard-codes `Person`. |
| `datePublished` / `dateModified` | Uses the **Publish Date Text** string (e.g. "Oct 4, 2026"), not an ISO date | ⚠️ Not ISO 8601 |
| `BreadcrumbList` | Not generated for blog posts. The page shows "Back to Journal" instead. | ⚠️ Missing |

The three ⚠️ items are site template/code issues, not content issues. They can't be fixed from the CMS and need a separate website code change; nothing was changed here. BC-001 can publish without them.
