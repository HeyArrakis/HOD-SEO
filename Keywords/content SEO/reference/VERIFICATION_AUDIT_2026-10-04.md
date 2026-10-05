# Verification Audit: CLAUDE.md, SEO_PLAYBOOK.md, BLOG_PUBLISHING_CONTEXT.md

Verification date: **2026-10-04**. This is an audit only; none of the three files was changed during it.

**Method.** Every material claim was checked against Tier 1 sources fetched on 2026-10-04: Google Search Central docs and blog, Search Console Help, Google Trends Help, Ahrefs, DataForSEO, modelcontextprotocol.io and Claude Help. Project-specific claims were checked against the local project files. HOD business facts were checked only for consistency between files, not against the web.

**File codes.** CL = CLAUDE.md · PB = reference/SEO_PLAYBOOK.md · BPC = reference/BLOG_PUBLISHING_CONTEXT.md

**Classification codes.** A Verified fact · B Industry practice · C Project rule · D Framework/opinion · E Source-specific tactic · F Outdated · G Unverified · H Incorrect

---

## 1. Audit table

### SEO_PLAYBOOK.md

| File | Section | Claim / Rule | Class | Status | Evidence | Source | Recommended Action |
|---|---|---|---|---|---|---|---|
| PB | Evidence Levels | Four-label system | C | 🔵 PROJECT RULE | Internal convention | — | Keep |
| PB | §1 | SEO → AEO → GEO → AI Visibility shown as a chain | D | 🟣 FRAMEWORK | Google: "optimizing for generative AI search is optimizing for the search experience, and thus still SEO" | [AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) | Keep; optionally note AEO/GEO sit *inside* SEO for Google |
| PB | §2 | "SEO formula" labelled as a framework | D | 🟣 FRAMEWORK | Labelled correctly | — | Keep |
| PB | §2 | Sustainable visibility needs a combination of factors; rankings ≠ quality | B | 🟡 INDUSTRY PRACTICE | Reasonable; matches Google's "many signals" framing | [How Search Works – ranking](https://www.google.com/search/howsearchworks/how-search-works/ranking-results/) | Keep |
| PB | §3 | Crawling → indexing → serving | A | ✅ VERIFIED | Google describes the same three stages | [How Search Works](https://developers.google.com/search/docs/fundamentals/how-search-works) | Keep |
| PB | §4 | Google does not index every page it crawls | A | ✅ VERIFIED | "Indexing and serving aren't guaranteed" | [AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) | Keep |
| PB | §4 | Crawled-not-indexed has many causes; backlinks are not the default explanation | A/B | ✅ VERIFIED | Causes such as duplication, canonicalization and spam match Google's docs | [Spam policies](https://developers.google.com/search/docs/essentials/spam-policies), canonicalization docs | Keep |
| PB | §4 | Google weighs quality, relevance, links and more; not "content-agnostic" | A | ✅ VERIFIED | Google describes relevance, quality and usability systems | [How Search Works – ranking](https://www.google.com/search/howsearchworks/how-search-works/ranking-results/) | Keep |
| PB | §5 | PageRank is still part of Google's ranking systems | A | ✅ VERIFIED | Called "one of our core ranking systems… evolved a lot" (updated 2025-12-10) | [Ranking systems guide](https://developers.google.com/search/docs/appearance/ranking-systems-guide) | Keep |
| PB | §5 | Google doesn't publicly confirm that clicks are a direct ranking factor | A | ⚠️ NEEDS UPDATE | Incomplete. Google says publicly: "We use aggregated and anonymised interaction data to assess whether search results are relevant to queries." The current wording implies Google confirms nothing about interaction data. | [How Search Works – ranking](https://www.google.com/search/howsearchworks/how-search-works/ranking-results/) | Reword (see §2, item 1) |
| PB | §7–8 | Keyword-universe workflow | B | 🟡 INDUSTRY PRACTICE | Standard methodology | — | Keep |
| PB | §9 | Ahrefs KD is Ahrefs' own metric, "largely based on backlink profiles of top-ranking pages" | A | ✅ VERIFIED | Ahrefs: trimmed mean of referring domains to the top-10 pages, plotted on a logarithmic 0–100 scale | [Ahrefs KD](https://ahrefs.com/blog/keyword-difficulty/), [help article](https://help.ahrefs.com/en/articles/72265-what-does-kd-stand-for-in-keywords-explorer) | Optional: use Ahrefs' exact wording |
| PB | §9 | DataForSEO calculates its own KD | A | ✅ VERIFIED | Built from backlink-based domain and page rank of the top-10 results; specific to location and language | [DataForSEO KD](https://dataforseo.com/help-center/what-is-keyword-difficulty-and-how-is-it-calculated) | Keep |
| PB | §9 | KD is not a Google metric and not a ranking probability | A | ✅ VERIFIED | "Third-party tools don't have access to our internal ranking data" | [Third-party SEO guidance](https://developers.google.com/search/docs/fundamentals/third-party-seo) (2026-06-05) | Keep; could cite |
| PB | §10–11 | Filtering thresholds; intent categories | B | 🟡 INDUSTRY PRACTICE | Labelled correctly | — | Keep |
| PB | §12 | "340 keywords → 19 pages" | E | 🟡 INDUSTRY PRACTICE (label) | The example is an anecdote from the source notes, while the method is industry practice | — | Optional: label the example as a source anecdote |
| PB | §12 | Clustering instead of one page per keyword | B | 🟡 INDUSTRY PRACTICE | Supported by Google: you don't need to capture "every variation"; its systems understand synonyms | [AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) | Keep; could cite |
| PB | §13–16 | Architecture first; page types; prioritization | B/D | 🟣 FRAMEWORK | Labelled correctly | — | Keep |
| PB | §17 | Topical authority is "not a publicly documented Google ranking score" | B | ⚠️ NEEDS UPDATE | Slightly inaccurate. Google has documented a **news-specific "topic authority" system** since 2023. General "topical authority" for ecommerce/blog SEO remains an industry concept. | [Understanding news topic authority](https://developers.google.com/search/blog/2023/05/understanding-news-topic-authority) | Add one sentence (see §2, item 2) |
| PB | §18–19 | Cornerstone and hub-and-spoke are frameworks, not ranking formulas | D | 🟣 FRAMEWORK | Labelled correctly | — | Keep |
| PB | §20 | Use-case expansion; very large example site | E | 🟠 SOURCE-SPECIFIC | Anecdote, labelled | — | Keep |
| PB | §21 | Dedicated FAQ pages only with distinct intent; no thin pages | E | 🟠 SOURCE-SPECIFIC | Matches Google: creating separate content for every query variation "primarily to manipulate rankings… violates" the scaled content abuse policy | [AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) | Keep; could cite |
| PB | §21 | "Google restricts FAQ rich results to well-known government and health sites" | F | ⚠️ NEEDS UPDATE (OUTDATED) | True from Aug 2023 to May 2026. FAQ rich results were **deprecated on 2026-05-08**, stopped showing from **2026-05-07**, and their documentation was **removed on 2026-06-15**. No site is eligible now. | [Documentation updates log](https://developers.google.com/search/updates), [2023 change](https://developers.google.com/search/blog/2023/08/howto-faq-changes) | Rewrite (see §2, item 3) |
| PB | §21 | QAPage: one question, user-submitted answers (forums, support) | A | ✅ VERIFIED | Matches the current doc (updated 2026-09-08). Site-authored FAQs, multi-question pages and blog posts are explicitly invalid. | [QAPage](https://developers.google.com/search/docs/appearance/structured-data/qapage) | Keep; optionally add "not for blog posts" |
| PB | §21 | FAQPage/QAPage schema doesn't automatically improve rankings | A | ✅ VERIFIED | The structured data intro presents it as an appearance feature; Google stated the FAQ deprecation "won't affect how pages are ranked" | [Structured data intro](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data) | Keep |
| PB | §22–23 | Answer-first / "Core" principle | D | 🟣 FRAMEWORK | Labelled correctly | — | Keep |
| PB | §23 | Don't claim AI reads only the start of a page | A | ✅ VERIFIED | Google: its systems "understand the nuance of multiple topics on a page and show the relevant piece" | [AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) | Keep |
| PB | §23 | "Where retrieval systems split pages into chunks, self-contained sections… help" | B | ⚠️ NEEDS UPDATE | Google now explicitly lists "chunking" as something to ignore: "There's no requirement to break your content into tiny pieces for AI to better understand it… There's no ideal page length." | [AI optimization guide – Mythbusting](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) | Reword (see §2, item 4) |
| PB | §24 | E-E-A-T isn't itself a ranking factor; systems use signals related to it | A | ✅ VERIFIED | "While E-E-A-T itself isn't a specific ranking factor…" (updated 2026-10-01) | [Helpful content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) | Keep |
| PB | §24 | Trust is the most important member | A | ✅ VERIFIED | "Of these aspects, trust is most important" | same | Keep |
| PB | §24 | Quality Rater Guidelines context | A | ✅ VERIFIED | Also: "Rater data is not used directly in our ranking algorithms" | same | Optional: add this line |
| PB | §25 | Entity SEO | B | 🟡 INDUSTRY PRACTICE | Labelled correctly | — | Keep |
| PB | §26 | Brand mentions as an authority component | B | ⚠️ NEEDS UPDATE (minor) | Google says other prominent sites linking or *referring* to content is a quality factor, but "seeking inauthentic 'mentions'… isn't as helpful as it might seem" | [How Search Works – ranking](https://www.google.com/search/howsearchworks/how-search-works/ranking-results/), [AI guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) | Add one sentence (see §2, item 5) |
| PB | §27 | Site reputation abuse; legitimate third-party publishing distinguished | A | ✅ VERIFIED | Policy updated 2026-08-28; wire services, syndicated news, UGC forums and disclosed affiliate content are listed as *not* abuse | [Spam policies](https://developers.google.com/search/docs/essentials/spam-policies) | Keep |
| PB | §27 | Publishing on a strong platform doesn't transfer its authority | B | 🟡 INDUSTRY PRACTICE | Logical, but not Google's wording | — | Keep; it's correctly unlabelled as Google |
| PB | §28 | Exact-match domain system | A | ✅ VERIFIED | "…don't give too much credit for content hosted under domains designed to exactly match particular queries" | [Ranking systems guide](https://developers.google.com/search/docs/appearance/ranking-systems-guide) | Keep |
| PB | §28 | Extra domains risk doorway or link-scheme problems | A | ✅ VERIFIED | Doorway abuse and link spam are defined in the policies | [Spam policies](https://developers.google.com/search/docs/essentials/spam-policies) | Keep |
| PB | §29 | Technical SEO list | B | 🟡 INDUSTRY PRACTICE | Standard | — | Keep |
| PB | §30 | Rich-result eligibility, not a guarantee or ranking boost | A | ✅ VERIFIED | — | [Structured data intro](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data) | Keep |
| PB | §30 | JSON-LD recommended; markup must reflect visible content | A | ✅ VERIFIED | "JSON-LD (Recommended)"; "don't add structured data about information that is not visible" | same | Keep |
| PB | §30 | No special schema needed for generative AI search | A | ✅ VERIFIED | "There's also no special schema.org structured data that you need to add" | [AI features](https://developers.google.com/search/docs/appearance/ai-features) | Keep |
| PB | §30 | Example types (Organization, Product, Article, Breadcrumb, LocalBusiness, Event, Review) | A | ✅ VERIFIED | None of these is on Google's 2025–2026 deprecation lists (Book Actions, Course Info, ClaimReview, Estimated Salary, Learning Video, Special Announcement, Vehicle Listing, Practice Problem, FAQ) | [Simplifying search results](https://developers.google.com/search/blog/2025/06/simplifying-search-results), [updates log](https://developers.google.com/search/updates) | Optional: note that FAQ rich results are gone |
| PB | §31 | CWV are part of page-experience guidance; relevance and helpfulness weigh more | A | ⚠️ NEEDS UPDATE (minor) | Underplays Google's wording. Google says: "Core Web Vitals are used by our ranking systems"; "There is no single signal"; it shows "the most relevant content, even if the page experience is sub-par" (updated 2026-09-22). | [Page experience](https://developers.google.com/search/docs/appearance/page-experience) | Reword (see §2, item 6) |
| PB | §32 | Googlebot fetches about 2 MB per URL, excluding PDFs; bytes past the cutoff aren't fetched, rendered or indexed | A | ✅ VERIFIED (core) / ⚠️ precision | Confirmed: "Googlebot currently fetches up to 2MB for any individual URL (excluding PDFs)… including the HTTP header." **PDFs have a 64 MB limit** rather than being simply "excluded". Each referenced CSS/JS resource has **its own separate 2 MB counter**. Other Google crawlers default to **15 MB**. The limit "is not set in stone". The source is a **Search Central blog post dated 2026-03-31**, plus the Googlebot doc updated 2026-02-03; the playbook calls it "March 2026 documentation". | [Inside Googlebot (blog, 2026-03-31)](https://developers.google.com/search/blog/2026/03/crawler-blog-post), [Googlebot doc](https://developers.google.com/search/docs/crawling-indexing/googlebot), [Crawler overview](https://developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers) | Add precision (see §2, item 7) |
| PB | §32 | Put title, canonical and essential structured data early; keep HTML lean. Currently labelled "[Source-specific tactic → adapted]" | A | ⚠️ NEEDS UPDATE (label) | **Google itself recommends this.** "Place your most critical elements — like meta tags, `<title>` elements, `<link>` elements, canonicals, and essential structured data — higher up in the HTML document." "Keep your HTML lean." | [Inside Googlebot](https://developers.google.com/search/blog/2026/03/crawler-blog-post) | Relabel as [Google-confirmed] best practice; keep "apply when relevant" |
| PB | §33 | URL change = migration; mapping, redirects, canonicals, internal links, monitoring; temporary fluctuation | A | ✅ VERIFIED | "Expect temporary fluctuation in site ranking during the move." Updated 2026-08-20. Google also says 301s "don't cause a loss in PageRank" and to keep redirects "generally at least 1 year". | [Site move with URL changes](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes) | Keep; optionally add the two specifics |
| PB | §33 | URL-refresh tactic | E | 🟠 SOURCE-SPECIFIC | Labelled and off by default | — | Keep |
| PB | §34 | Links matter, but quality over quantity; link spam | A/B | ✅ VERIFIED | Prominent sites linking is "generally a good sign"; buying links violates policy | [Ranking](https://www.google.com/search/howsearchworks/how-search-works/ranking-results/), [Spam policies](https://developers.google.com/search/docs/essentials/spam-policies) | Keep |
| PB | §35–36 | Competitor and backlink analysis | B | 🟡 INDUSTRY PRACTICE | — | — | Keep |
| PB | §37 | **"Ahrefs — primary SEO research tool used in this project"** | H | ❌ INCORRECT | No project file uses Ahrefs. cost-log.csv lists only DataForSEO endpoints, CLAUDE.md requires the DataForSEO MCP, and the Ahrefs connector is unauthenticated in this environment. The line came from the user's study notes, not from what this project actually does. | Local: cost-log.csv, progress.md, CLAUDE.md | Fix (see §2, item 8) |
| PB | §37 | GSC "strongly recommended" | A | ✅ VERIFIED | "We strongly encourage using our first-party tool, Google Search Console" | [Third-party SEO guidance](https://developers.google.com/search/docs/fundamentals/third-party-seo) | Keep |
| PB | §37 | SuperSEO, GTM, Semrush roles | C | 🔵 PROJECT RULE | Tool choices | — | Keep |
| PB | §38 | GSC metrics: clicks, impressions, CTR, average position; dimensions | A | ✅ VERIFIED | Matches Help Center definitions | [Performance report](https://support.google.com/webmasters/answer/7576553) | Keep |
| PB | §38 / §42 | No mention of GSC's **Generative AI performance report** | — | ⚠️ NEEDS UPDATE (gap) | New report covering impressions in AI Overviews and AI Mode, rolled out worldwide by 2026-08-31. A separate report covers Discover generative features. | [Gen AI performance report](https://support.google.com/webmasters/answer/16984139) | Add (see §2, item 9) |
| PB | §39 | GA4 measures behaviour and conversions after arrival | B | 🟡 INDUSTRY PRACTICE | Generic and accurate; GA4 docs not re-fetched | — | Keep |
| PB | §40 | Trends shows relative interest on a 0–100 index, not absolute volume | A | ✅ VERIFIED | Normalised to total searches by geography and time, scaled 0–100, based on a sample | [Trends FAQ](https://support.google.com/trends/answer/4365533) | Optional: add "sampled" |
| PB | §41 | SERP inspection | B | 🟡 INDUSTRY PRACTICE | — | — | Keep |
| PB | §42 | "Measure AI visibility separately where possible"; third-party trackers are directional | B | ⚠️ NEEDS UPDATE | Still valid for ChatGPT, Perplexity and others, but Google now provides first-party AI Overview / AI Mode impression data. Google also warns: "No third-party tool has access to our internal ranking or AI systems." | [Gen AI report](https://support.google.com/webmasters/answer/16984139), [AI guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) | Reword (see §2, item 9) |
| PB | §43 | AEO/GEO are industry terms; Google treats AI-search optimization as SEO | A | ✅ VERIFIED | Verbatim in the May 2026 guide | [AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) | Keep; cite the 2026-05-15 guide |
| PB | §43 | No special optimization or markup needed | A | ✅ VERIFIED | "There are no additional requirements… nor other special optimizations necessary." | [AI features](https://developers.google.com/search/docs/appearance/ai-features) | Keep |
| PB | §43 | Eligibility = crawlable/indexable/snippet-eligible | A | ⚠️ NEEDS UPDATE (gap) | There is now one extra condition: the site must be **included in the "Search generative AI" setting in Search Console**. It defaults to *include*, so it only blocks a site that has opted out. | [AI guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), [GSC setting](https://support.google.com/webmasters/answer/16908024) | Add (see §2, item 10) |
| PB | §43 | Scaled low-value AI content risks scaled content abuse | A | ✅ VERIFIED | "Using generative AI tools… to generate many pages without adding value" (policy updated 2026-08-28) | [Spam policies](https://developers.google.com/search/docs/essentials/spam-policies) | Keep |
| PB | §43 | "What not to assume" list | A | ✅ VERIFIED | Each item matches Google's 2026 myth-busting | [AI guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) | Keep. Gap: add "llms.txt is ignored by Google Search" (clarified 2026-06-15) |
| PB | §44 | GEO definition; AI systems differ in retrieval | B | 🟡 INDUSTRY PRACTICE | Reasonable | — | Keep. Optional: Google describes RAG and query fan-out for its own features |
| PB | §45–46 | CITE is a framework, not Google's; parts align with Google | D | 🟣 FRAMEWORK | Alignment is strong: Google asks for "a unique point of view", first-hand experience and "non-commodity content" | [AI guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) | Keep; could cite as support for "Take a Position" |
| PB | §47–48 | Context as moat; Claude as architect | D | 🟣 FRAMEWORK | — | — | Keep |
| PB | §49 | A Claude Project with about 10 instruction areas; WordPress endpoints | E | 🟠 SOURCE-SPECIFIC | Claude Projects with knowledge and instructions do exist. The 10-area setup and WordPress workflow are the source's own and not HOD facts (HOD's CMS isn't recorded in the project). | [Claude Projects](https://support.claude.com/en/articles/9517075-what-are-projects) | Keep. Never assume WordPress for HOD |
| PB | §50 | AI use isn't itself against policy; scaled low-value content is | A | ✅ VERIFIED | Matches the gen-AI content guidance (updated 2026-10-01) | [Gen AI content](https://developers.google.com/search/docs/fundamentals/using-gen-ai-content) | Keep |
| PB | §50 | (gap) 2026-10-01 guidance: fact-check *all* AI-generated elements and consider disclosure | A | ⚠️ NEEDS UPDATE (gap) | "Manually factcheck and review all AI-generated content… before publishing": main content, titles, meta descriptions, structured data and alt text. It also suggests "adding information on how your content was created". The page notes AI-generated **ecommerce images** need IPTC `DigitalSourceType: TrainedAlgorithmicMedia`; the exact scope (Merchant listings / Shopping) needs confirming. | [Gen AI content](https://developers.google.com/search/docs/fundamentals/using-gen-ai-content) | Add (see §2, item 11). Relevant to HOD if AI product imagery is used |
| PB | §51, §55–61 | Audit before creation; agent; monitoring (Make/n8n) | D | 🟣 FRAMEWORK | — | — | Keep |
| PB | §52–54 | MCP is an open integration standard; freshness depends on the provider | A | ✅ VERIFIED | "MCP… is an open-source standard for connecting AI applications to external systems." DataForSEO Labs is a database, while SERP API calls are live. | [modelcontextprotocol.io](https://modelcontextprotocol.io/docs/getting-started/intro), [DataForSEO Labs](https://docs.dataforseo.com/v3/dataforseo_labs-overview-2/) | Keep |
| PB | §62 | Newsletter sources exist | A | ✅ VERIFIED | AI Marketers was launched by Aleyda Solis in 2025, alongside SEOFOMO. Growth Memo, The SEO Notebook and the Marie Haynes newsletter are long-established. | [Aleyda on X](https://x.com/aleyda/status/1884590081215795431) | Keep |
| PB | §64 | AI output ≠ SEO outcome | A/D | ✅ VERIFIED | "A high quantity of pages doesn't make a website higher quality or more relevant" | [AI guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) | Keep |
| PB | §65 | Transcripts aid accessibility and discoverability; no "can't understand audio" claim | B | 🟡 INDUSTRY PRACTICE | Correctly hedged | — | Keep |
| PB | §66–67, §69–71 | Entity system; stack; AI pipeline; principles; mental model | D | 🟣 FRAMEWORK | Labelled correctly | — | Keep |
| PB | §68 step 24 | Update only when material; no cosmetic date changes | A | ✅ VERIFIED | "Are you changing the date of pages to make them seem fresh when the content has not substantially changed?" | [Helpful content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) | Keep |

### BLOG_PUBLISHING_CONTEXT.md

| File | Section | Claim / Rule | Class | Status | Evidence | Source | Recommended Action |
|---|---|---|---|---|---|---|---|
| BPC | §1–2 | Project is the source of truth; calendar CSV controls dates and topics | C | 🔵 PROJECT RULE | File exists (112 items + header) | Local | Keep |
| BPC | §3 | "SEO → AEO → GEO → AI VISIBILITY" as successive stages | D | ⚠️ NEEDS UPDATE (minor) | Reads as if AEO/GEO come after SEO, whereas PB §43 and Google treat them as part of SEO | [AI guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) | Add one clarifying line (see §2, item 12) |
| BPC | §4–5, §7, §9, §13, §20, §22 | Keyword→intent thinking; existing-content check; intent; PAA use; topical system; ownership stop-and-flag; write workflow | C | 🔵 PROJECT RULE | Deliberate HOD rules | — | Keep |
| BPC | §6 | Natural keyword use; no forcing variations | C/A | ✅ VERIFIED | Google: no need to capture "every variation"; synonyms are understood | [AI guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) | Keep |
| BPC | §8 | Answer-first; tables, lists, FAQs where useful | D | 🟣 FRAMEWORK | Matches Google's "organized by paragraphs and sections, along with headings" | same | Keep. Don't chunk artificially (see PB §23) |
| BPC | §10 | E-E-A-T / trust; no fabrication | C/A | ✅ VERIFIED | Consistent with Google; "trust is most important" | [Helpful content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) | Keep |
| BPC | §11 | Bespoke: typically 2–3 weeks to make, ~6–9 days delivery, ~3–4 weeks total, stone-dependent, never a guarantee | C | 🔵 PROJECT RULE (HOD fact) | Same in CL and the calendar. progress.md (L491, user decision 2026-09-29) records "2–3 weeks + ~6–9 days, never guaranteed"; "~3–4 weeks total" and "depends on stone" appear in the calendar and your own text, not in that log line | Local | Keep. Optionally log the full fact once in decision-log.md |
| BPC | §12 | Use Stage 16/19 link requirements | C | 🔵 PROJECT RULE | Files exist | Local | Keep |
| BPC | §14–15 | Workflow; default structure; "FAQ only when useful" | C | 🔵 PROJECT RULE | Consistent with Google. FAQ blocks no longer earn a rich result. | [Updates log](https://developers.google.com/search/updates) | Keep. Optionally add "FAQPage markup no longer produces Google rich results" |
| BPC | §16 | SEO elements incl. schema, breadcrumbs, canonical | A/C | ✅ VERIFIED | Breadcrumb, Article and Product structured data are still supported | Structured data gallery | Keep |
| BPC | §17 | Alt text describes the image naturally; no stuffing | A | ✅ VERIFIED | "Avoid filling alt attributes with keywords… may cause your site to be seen as spam" (updated 2026-03-02) | [Image SEO](https://developers.google.com/search/docs/appearance/google-images) | Keep |
| BPC | §18 | Tactics off by default; 2 MB distinction | C | 🔵 PROJECT RULE | Matches CL after today's fix | — | Keep. Note PB §32 should be relabelled to match (item 7) |
| BPC | §19 | SuperSEO skill names | C | ✅ VERIFIED | All eight named skills exist in this environment | Skill list | Keep |
| BPC | §21 | Approval **before any paid call** | C | 🔵 PROJECT RULE | Conflicts with CL "non-trivial spend" (see matrix) | — | Align CL (item 13) |
| BPC | §23 | QA, then human review unless autonomous publishing is requested | C | 🔵 PROJECT RULE | Consistent with CL's definition of "publish" | — | Keep |
| BPC | §24 | Measure with GSC, rankings… "AI visibility where available" | C/A | ⚠️ NEEDS UPDATE (minor) | Google AI-feature visibility is now available in GSC's Generative AI performance report | [Gen AI report](https://support.google.com/webmasters/answer/16984139) | Name the report (item 9) |

### CLAUDE.md

| File | Section | Claim / Rule | Class | Status | Evidence | Source | Recommended Action |
|---|---|---|---|---|---|---|---|
| CL | Project / Business / Website context | HOD scope; site rebuild; existing blog not final | C | 🔵 PROJECT RULE | — | — | Keep |
| CL | SEO principles 1–12, 16–20 | Intent first; no thin or parameter pages; avoid page explosion | B/C | 🔵 PROJECT RULE | Consistent with Google's scaled-content and duplicate-content guidance | — | Keep |
| CL | Principles 13–15 | Don't invent metrics; paid competition ≠ organic KD; KD is not a probability | A/C | ✅ VERIFIED | DataForSEO "competition" is Google Ads data; KD is a third-party estimate | [DataForSEO KD](https://dataforseo.com/help-center/what-is-keyword-difficulty-and-how-is-it-calculated), [Google third-party guidance](https://developers.google.com/search/docs/fundamentals/third-party-seo) | Keep |
| CL | DataForSEO rules | Estimate, then confirm, then log; cheapest endpoint; Labs over Ads | C | 🔵 PROJECT RULE | Followed in cost-log.csv | Local | Keep |
| CL | DataForSEO rules | Clickstream increases cost | A | ✅ VERIFIED | `include_clickstream_data: true` doubles the request cost | [DataForSEO clickstream pricing](https://dataforseo.com/pricing/keywords-data/clickstream-api-pricing) | Keep |
| CL | DataForSEO rule 5 | "get user confirmation for non-trivial spend" | C | ⚠️ NEEDS UPDATE | Conflicts with BPC §21 ("before any paid call"). Actual practice per progress.md is that "each paid call [was] individually approved". | Local | Align to "every paid call" (item 13) |
| CL | Market settings | Verify US/English IDs before the first paid call | C | ✅ VERIFIED (done) | README records 2840 / en, confirmed 2026-09-17 | Local | Keep |
| CL | File naming list 01–16 | Sequential output names | F | ⚠️ NEEDS UPDATE (OUTDATED) | Actual outputs differ. For example, `07_hod_master_keyword_database.csv` exists but the listed `06_hod_master_keywords.csv` doesn't; `architecture/15_keyword_url_map.csv` exists instead of `12_hod_keyword_url_map.csv`; there is no `16_hod_internal_linking.csv`; the stages ran to 19 (plus 18.5). | Local `find` | Mark as the original plan and point to progress.md and the file map (item 14) |
| CL | Cost tracking | cost-log.csv + progress.md | C | 🔵 PROJECT RULE | Both maintained | Local | Keep |
| CL | Security | Credentials live only in the Claude Desktop MCP config | C/G | ❓ UNVERIFIED (location only) | The DataForSEO MCP server now says it prefers OAuth Bearer tokens, with login/password as an env fallback. Which method this install uses isn't verifiable from here. The rule itself (never put credentials in files) stands. | DataForSEO MCP server instructions | Optional: "credentials stay in the MCP connection/config (OAuth or env), never in project files" |
| CL | Website safety | Research only; no live-site, CMS, robots or redirect changes | C | 🔵 PROJECT RULE | — | — | Keep |
| CL | Final quality standard | "answer the 20 questions listed in README.md" | H | ❌ INCORRECT | README.md (70 lines) contains no question list; nothing in it ends in "?" | Local | Restore the 20 questions to README or reword (item 15) |
| CL | Blog production | Calendar authority; ownership; facts; tactics; 2 MB line; SuperSEO; meaning of "publish" | C | 🔵 PROJECT RULE | Consistent with BPC | — | Keep |
| CL | Blog production – file map | 17 paths | C | ✅ VERIFIED | All 17 paths exist | Local `test -e` | Keep |

---

## 2. Corrections in detail (every ⚠️ / ❌ / ❓)

1. **PB §5 clicks (⚠️).** *Why:* the current text says Google doesn't confirm any role for interaction data, but Google publicly states it uses aggregated interaction data. *Suggested wording:* "Google says it uses 'aggregated and anonymised interaction data to assess whether search results are relevant to queries.' It does not publish how this is used, so avoid simplistic claims such as 'more clicks = higher rankings'. In this project, clicks, impressions, CTR and position are Search Console *measurement* data." *Source:* How Search Works – ranking results. **Change file: yes.**
2. **PB §17 topical authority (⚠️).** *Why:* Google documents a news-only "topic authority" system. *Add:* "Google documents a news-specific 'topic authority' system (2023). For non-news sites such as HOD, 'topical authority' remains an industry strategy rather than a published Google score." *Source:* Search Central blog, 2023-05. **Change: yes.**
3. **PB §21 FAQ rich results (⚠️ outdated).** *Suggested wording:* "**[Google-confirmed]** FAQ rich results were deprecated: they stopped appearing in Google Search on 2026-05-07, and Google removed the documentation on 2026-06-15. From August 2023 to May 2026 they had been limited to authoritative government and health sites. FAQPage remains a valid schema.org type and can stay on a page harmlessly, but it no longer produces a Google rich result. Add on-page FAQs only for users." *Source:* Search documentation updates log; 2023 HowTo/FAQ blog. **Change: yes, high priority.**
4. **PB §23 chunking (⚠️).** *Suggested wording:* "For Google Search, Google says there is 'no requirement to break your content into tiny pieces' and 'no ideal page length'; its systems can pick out the relevant part of a multi-topic page. Use clear sections and headings for readers. Some other retrieval systems split pages into chunks, but don't restructure HOD content just to suit that." *Source:* AI optimization guide (2026-05-15). **Change: yes.**
5. **PB §26 brand mentions (⚠️ minor).** *Add:* "Google counts other prominent sites linking to *or referring to* content as a quality factor, and warns that 'seeking inauthentic mentions… isn't as helpful as it might seem.' Earn genuine mentions; don't manufacture them." **Change: yes.**
6. **PB §31 page experience (⚠️ minor).** *Suggested wording:* "**[Google-confirmed]** 'Core Web Vitals are used by our ranking systems', but 'there is no single [page experience] signal', and Google shows the most relevant content 'even if the page experience is sub-par'. Good page experience can help where many pages are equally helpful." *Source:* Page experience doc (2026-09-22). **Change: yes.**
7. **PB §32 2 MB precision and label (⚠️).** *Add:* "PDFs have a 64 MB limit. The 2 MB count includes HTTP headers and applies to uncompressed data. Each referenced CSS/JS file has its own 2 MB counter. Other Google crawlers default to 15 MB, and image/video crawlers vary. Google says the limit 'is not set in stone'. Sources: Search Central blog 'Inside Googlebot' (2026-03-31) and the Googlebot doc (updated 2026-02-03)." Also **relabel** the early-placement and lean-HTML guidance as **[Google-confirmed] best practice**, because Google recommends it directly. Keep the project rule that it's applied only when relevant. **Change: yes.**
8. **PB §37 Ahrefs (❌).** *Suggested wording:* "DataForSEO (via MCP) is this project's primary keyword, SERP and competitor data source. Ahrefs appears in the original study notes; it isn't connected or used in this project's research so far. Its KD is Ahrefs' own metric." **Change: yes, high priority** (it currently contradicts CLAUDE.md).
9. **PB §38/§42 and BPC §24 Generative AI report (⚠️).** *Add:* "Search Console's **Generative AI performance report** shows impressions of your links in AI Overviews and AI Mode (available worldwide since 2026-08-31; Discover has its own report). It reports impressions only. Use third-party trackers for ChatGPT, Perplexity and others, as directional samples. Google warns that no third-party tool has access to its internal ranking or AI systems." **Change: yes.**
10. **PB §43 eligibility (⚠️ gap).** *Add:* "A site must also be included in Search Console → Settings → **Search generative AI**. It defaults to *include*; check that HOD hasn't been set to *exclude*. Google Search ignores llms.txt and other AI-specific files, which neither help nor harm." **Change: yes.** Also an HOD action: check the GSC setting.
11. **PB §50 AI content QA (⚠️ gap).** *Add:* "Google's 2026-10-01 guidance: manually fact-check every AI-generated element (body, titles, meta descriptions, structured data, alt text) before publishing, and consider telling readers how content was made. AI-generated ecommerce images should carry IPTC `DigitalSourceType: TrainedAlgorithmicMedia` metadata. Confirm the exact scope (Merchant/Shopping) before relying on this." **Change: yes.** The IPTC scope should be confirmed against Merchant Center policy.
12. **BPC §3 (⚠️ minor).** *Add:* "For Google, AEO/GEO are part of SEO, not separate algorithms. This chain is a planning framework." **Change: yes.**
13. **CL DataForSEO rule 5 (⚠️).** *Suggested wording:* "Run only after the estimate is understood and the user has approved **each paid call**." This matches BPC §21 and actual practice. **Change: yes.**
14. **CL file naming (⚠️ outdated).** *Suggested wording:* "Original planned numbering. Actual outputs are stage-numbered within folders (Stages 1–19, plus 18.5); progress.md and the Blog production file map are the authoritative index." **Change: yes.**
15. **CL "20 questions" (❌).** README.md has no questions. Either restore the 20 questions to README.md (the user would need to supply them, or point to where they live) or reword the line to "…should allow us to answer site coverage, demand, intent, clustering, page-type, existing-content, architecture and blog/education strategy questions." **Change: yes; needs the user's input.**
16. **CL credentials location (❓).** This can't be verified from inside the session. Optional rewording is in the table. **Change: optional.**

**Out of scope but noticed:** README.md "Status: Workspace initialized. Keyword research has not started yet." is stale; Stages 1–19 are done.

---

## 3. Overclaim search (all three files)

| Term | Hits | Verdict |
|---|---|---|
| ranking factor | PB L176, L277 | Justified: both are negations ("not a specific ranking factor"; "not a list of ranking factors") |
| Google uses | PB L176 | Justified: "a framework Google uses" is accurate |
| direct ranking | PB L72, L218 | Justified: both negations |
| guarantee(s/d) | PB L62, 88, 139, 218; BPC L70, 79; CL L63, 141 | Justified: all are negations or the HOD "never a guarantee" rule |
| improves rank | PB L158 | Justified: negation (FAQ schema doesn't automatically improve rankings) |
| Google treats | PB L297 | Justified: matches the May 2026 guide verbatim |
| required | PB L297, 309; BPC L91; CL L87 | Justified: "no special markup required" is verified; the BPC/CL hits are project rules (BUSINESS_FACT_REQUIRED, etc.) |
| must | PB L220, 307; CL L55–66 | Justified: L220 matches Google's structured-data rule; L307 and CL are project rules |
| essential | PB L234 | Justified: Google's own phrase "essential structured data" |
| real-time | PB L351 | Justified: correctly conditioned on the provider |
| never / always | various | Project rules or HOD facts; no Google claim uses "always" |
| Google rewards / penalizes / prefers / wants; boosts rankings; major ranking signal; AI understands / reads / ranks; Google considers; best practice | 0 | — |

No unjustified overclaim wording remains. The open issues are about substance (outdated or incomplete facts), not wording.

---

## 4. Consistency matrix

| Topic | CLAUDE.md | SEO_PLAYBOOK.md | BLOG_PUBLISHING_CONTEXT.md | Consistent? |
|---|---|---|---|---|
| Primary data tool | DataForSEO MCP | **Ahrefs "primary… in this project"** (§37) | DataForSEO (§21) | ❌ PB contradicts both |
| Paid-call approval | "non-trivial spend" | — | "before any paid call" | ❌ CL vs BPC |
| 2 MB | Googlebot limit documented; tactic applied selectively | Fact = Google-confirmed; tactic labelled "source-specific → adapted" | Same as CL | 🟡 Consistent in rule; PB label understates that Google recommends the tactic |
| AEO/GEO | (via BPC) | Part of SEO per Google (§43) | Chain implies separate stages (§3, §25) | 🟡 Wording only |
| Meaning of "publish" | QA'd draft for human review; no CMS without explicit OK | n/a | Human review unless autonomous publishing requested | ✅ |
| Bespoke facts | 2–3 wk + ~6–9 d ≈ 3–4 wk; stone-dependent; never guaranteed | n/a | Same | ✅ (progress.md logs only part of it) |
| URL changes | Never without migration reasoning; no live changes | Migration, not a refresh tactic | Preserve URLs | ✅ |
| Schema | n/a | Eligibility only; no special AI schema; FAQ wording outdated | "schema where applicable" | 🟡 PB FAQ line outdated |
| Freshness | n/a | Material updates only | Measure → refresh | ✅ |
| Ownership / cannibalization | Stop and flag | Audit before creation | Stop and flag | ✅ |
| Off-by-default tactics | URL refresh, EMD, clicks/PageRank, parasite | Same, labelled | Same | ✅ |
| AI visibility measurement | — | Third-party trackers; "separately where possible" | "where available" | 🟡 Both miss the GSC Gen AI report |
| Output naming | 01–16 list | — | — | ❌ CL list vs actual files |
| Quality standard | "20 questions in README" | — | — | ❌ README has none |

---

## 5. Summary

### Overall result (≈110 material claims assessed)

| Category | Share |
|---|---|
| Factually verified | ~34% |
| Industry practice | ~13% |
| Project rules | ~25% |
| Frameworks | ~11% |
| Source-specific | ~4% |
| Needs update | ~11% |
| Incorrect / unverified | ~2% (2 incorrect, 1 unverified) |

### Critical issues
1. **PB §37** says Ahrefs is the project's primary tool. That is wrong and contradicts CLAUDE.md.
2. **PB §21** FAQ rich-result rules are **outdated**: the feature was fully deprecated in May–June 2026.
3. **CL "Final quality standard"** points to 20 README questions that don't exist.
4. **CL vs BPC**: different thresholds for approving paid DataForSEO calls.
5. **PB §43** is missing the new Search Console "Search generative AI" setting, which affects eligibility.
6. **PB §42 / BPC §24** miss GSC's first-party Generative AI performance report.
7. **PB §23** chunking advice conflicts with Google's May 2026 myth-busting.
8. **PB §5** understates Google's public statement on interaction data.
9. **PB §32** mislabels Google's own byte-placement best practice as source-specific and lacks precision (64 MB PDFs, headers, per-resource counters, 15 MB default).
10. **CL file-naming list** is outdated relative to the actual outputs.
11. **PB §50** is missing Google's 2026-10-01 AI-content QA guidance, which is relevant to HOD's AI imagery.
12. **PB §31** understates "Core Web Vitals are used by our ranking systems".

### Current as of 2026-10-04
- **CLAUDE.md**: READY WITH MINOR FIXES (approval threshold, file-naming note, README reference)
- **SEO_PLAYBOOK.md**: READY WITH MINOR FIXES. One factual error and one outdated fact are high priority; the rest are precision additions.
- **BLOG_PUBLISHING_CONTEXT.md**: READY WITH MINOR FIXES (AEO/GEO line; GSC Gen AI report)

### Recommended edits (in order)
1. PB §37: replace the Ahrefs line with DataForSEO as the project's primary source (item 8).
2. PB §21: rewrite FAQ rich results as deprecated in 2026 (item 3).
3. CL: align paid-call approval to "every paid call" (item 13).
4. CL: fix the "20 questions" reference, using the user's input (item 15).
5. PB §43: add the GSC Search generative AI setting and the llms.txt clarification (item 10).
6. PB §38/§42 and BPC §24: add the GSC Generative AI performance report (item 9).
7. PB §23: replace the chunking sentence (item 4).
8. PB §5: add Google's interaction-data statement (item 1).
9. PB §32: add precision and relabel the byte-placement guidance as Google-confirmed (item 7).
10. PB §50: add the 2026-10-01 AI-content QA guidance (item 11).
11. PB §31: page-experience wording (item 6).
12. PB §17 and §26: news topic authority; inauthentic mentions (items 2, 5).
13. BPC §3: AEO/GEO clarification (item 12).
14. CL: note that the file-naming list is the original plan (item 14).
15. Optional: CL credentials wording (item 16); PB §12 anecdote label; PB §24 rater-data line; PB §33 one-year redirect and PageRank specifics.
