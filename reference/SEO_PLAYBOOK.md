# SEO & AEO Playbook — Study Notes

Strategic reference for HOD content production. Apply its principles during execution; do not copy it into CLAUDE.md.

Source: merged notes from 14 notebook images plus David Quaid / SEO-AEO material, corrected after a web-verification audit (2026-10). Core SEO principles are kept separate from source-specific tactics (see also BLOG_PUBLISHING_CONTEXT.md §18).

## Evidence Levels

Labels are applied where the distinction matters, not to every paragraph.

- **[Google-confirmed]** — directly supported by official Google documentation.
- **[Industry practice]** — widely used SEO methodology, but not necessarily an official Google ranking rule.
- **[Framework]** — a strategic methodology used by this project or derived from source material.
- **[Source-specific tactic]** — a tactic, experiment, anecdote or opinion from a particular practitioner/source. Never present it as a universal Google rule.

In practice: separate "Google officially says…" from "SEO practitioners commonly do…" from "our project strategy is…".

---

## 1. The Big Picture

SEO should be treated as a **system**, not a collection of random blog posts or isolated tricks.

Business → Search Demand → Keywords → Intent → Clusters → Site Architecture → Content → Internal Links → Authority → Rankings → Measurement → Iteration

Modern search adds: **SEO → AEO → GEO → AI Visibility** — a **[Framework]** for planning, not Google's architecture. For Google, AEO/GEO are industry terms and optimizing for AI search is part of SEO (see §43).

- SEO = Search Engine Optimization
- AEO = Answer Engine Optimization
- GEO = Generative Engine Optimization

Objective: make the website easy for search engines and AI systems to discover, understand, retrieve, trust, cite, and associate with a subject/entity.

## 2. What SEO Is Trying to Achieve

**[Framework]** A strategic model, not Google's literal ranking formula:

Technical SEO + Keyword Research + Good Content + Fast Website + Schema + Backlinks + Brand Mentions + Meaningful Updates → stronger organic visibility over time.

Sustainable organic visibility generally requires a combination of technical accessibility, relevant content, strong information architecture, useful internal/external references, authority/trust, and continuous improvement. Rankings alone are not a complete measure of website quality.

Layers:
- **Technical** — can search engines access and understand the site?
- **Content** — useful, relevant, comprehensive information?
- **Search demand** — targeting what people actually search for?
- **Authority** — credible signals and links?
- **Entity** — is the brand understood as a recognizable entity?
- **AI** — can answer engines retrieve, understand and cite the content?

## 3. Crawling, Indexing & Ranking

**[Google-confirmed]** Google describes Search in three stages: crawling, indexing, and serving search results (where ranking happens).

- **Crawling** — a search engine discovers and fetches a URL.
- **Indexing** — it decides whether/how the page is stored in its index.
- **Ranking** — the indexed page is evaluated for a query and may appear in results.

Crawled ≠ Indexed ≠ Ranked. Journey: URL exists → discovered → crawled → evaluated → indexed → ranked.

## 4. Crawled but Not Indexed

A technically crawlable page is not guaranteed to be indexed. **[Google-confirmed]** Google does not index every page it crawls.

Being crawled but not indexed can have many causes. Lack of external links can be one contributing factor, but it is not the sole or typical explanation. Other causes include quality/helpfulness, duplication, canonicalization, crawl/indexing issues, technical accessibility, spam policies, and Google's indexing decisions. Also check search demand, internal linking and site architecture.

Google evaluates content quality, relevance, usefulness, context, links, technical accessibility, and many other signals/systems. Do not describe Google as "content-agnostic."

## 5. PageRank

**[Google-confirmed]** PageRank is Google's link-analysis system based on relationships between pages (Page A links → Page B can contribute signals to B). Links remain one input among many systems; it is not the whole ranking picture.

**[Google-confirmed]** Google publicly states that it uses aggregated and anonymised interaction data to assess whether search results are relevant to queries. This should not be simplified into "clicks are a direct ranking factor" or treated as a standalone optimization target. In this project, clicks, impressions, CTR and query-level performance are Search Console measurement metrics.

## 6. SEO Is Not Just Keywords

Move from "put the keyword on the page" to understanding the search ecosystem: demand, intent, related queries, topic relationships, entities, competitors, existing SERPs, supporting questions, commercial opportunities, content gaps, internal linking, authority.

## 7. Keyword Research Workflow

Seed keyword → Keyword universe → Filtering → Search intent → Clustering → Prioritization → Page architecture → Content

## 8. Keyword Universe

Generate a large universe first rather than five keywords → five articles. Collect: search volume, keyword difficulty, intent, SERP information, related terms, commercial relevance.

## 9. Keyword Difficulty (KD)

**[Industry practice]** A third-party tool metric (often 0–100) estimating ranking difficulty. Ahrefs KD is Ahrefs' own Keyword Difficulty metric (largely based on the backlink profiles of top-ranking pages); DataForSEO and other tools calculate their own versions. None of these is a Google metric or a guaranteed ranking probability. Higher KD generally suggests stronger competition (better content, more authority, more relevant links).

## 10. Keyword Filtering

**[Industry practice]** Thresholds are project choices, not Google rules.

Example rules: volume above a threshold, KD below a chosen threshold, intent classification (informational / commercial / transactional / navigational) → appropriate page type.

## 11. Search Intent

**[Industry practice]** The bridge between keyword research and architecture.
- **Informational** — "what is X", "how does X work" → blog/resource.
- **Commercial** — "best X", "X vs Y", "X reviews", "X pricing" → comparison, category, product or commercial content.
- **Transactional** — "buy X", "hire a plumber" → product/service page.

## 12. Keyword Clustering

**[Industry practice]** Example from the source notes: **340 keywords → 19 pages.** Keywords do not equal URLs. Clustering avoids cannibalization, thin pages, duplicate content, unnecessary URLs, poor architecture.

## 13. Keyword Universe → Page Architecture

**[Framework]** Build the architecture first: universe → cluster → intent → decide which pages exist → build architecture → write/migrate content. Reverses "publish blogs and figure out structure later."

## 14. Don't Let the Existing Blog Define the Architecture

Business/Products → Search demand → Keyword clusters → Page architecture → Final blogs. The blog is a component of the architecture, not the architecture itself.

## 15. Page Types

- Commercial/service intent → service page
- Product intent → product/category page
- Informational intent → blog/resource
- Broad topic → hub/cornerstone page
- Specific subtopic → supporting/spoke page

## 16. Prioritization

Not every keyword has equal business value or the same page type. Consider demand, business value, intent, competition, existing authority, content difficulty, conversion potential, strategic importance.

## 17. Topical Authority

**[Industry practice]** Build comprehensive, interconnected coverage around a subject rather than isolated articles — a topic ecosystem of a main topic plus supporting subtopics.

Topical authority is an industry SEO strategy describing comprehensive coverage of a subject, strong internal linking, relevant supporting content, and demonstrated expertise. It is a useful strategic concept, not a publicly documented Google ranking score.

Google also documents a separate news-specific "topic authority" system for news surfaces. That should not be conflated with the broader SEO industry concept of topical authority used for ecommerce and content strategy.

## 18. Cornerstone Content

**[Framework]** (Yoast concept.) Broad, comprehensive, business-critical, high-priority page covering a major topic; the central hub. Supporting articles link back to it.

## 19. Hub-and-Spoke Architecture

**[Framework]** Hub-and-spoke and cornerstone content are information-architecture/content-strategy frameworks. They help organize topics and internal links; they are not guaranteed Google ranking formulas.

- **Hub** — broad, authoritative page.
- **Spokes** — specific supporting pages.
- Linking: Spoke → Hub; Hub → Spoke where useful; Spoke ↔ related Spoke.

## 20. Use-Case Analysis

**[Source-specific tactic]** (David Quaid material.) Map every situation in which users need the product: who, why, when, where, what problem, what technical situation, what alternatives, pre-purchase questions, post-purchase questions. Use cases can generate keywords → pages → supporting content, but each candidate page still has to pass the keyword-ownership, intent and SERP checks. The source's anecdotal example of a very large use-case site (tens of thousands of pages) is a case study, not a model to copy.

## 21. FAQ Strategy

**[Source-specific tactic]** Instead of one giant /faq page, some important questions can become dedicated pages. A dedicated page can be useful when it satisfies a distinct search intent and provides enough standalone value to justify its existence. Do not create thin FAQ pages merely to target individual queries, and do not assume every question or query variation deserves its own page.

Keep three things separate:
- **FAQ content** — normal on-page questions and answers.
- **FAQPage structured data** — markup for a page of site-authored FAQs. **[Google-confirmed]** Google discontinued FAQ rich-result eligibility in 2026 (no longer shown in Search from May 2026). FAQ content itself remains normal useful on-page content, but do not plan content or structured data around FAQ rich-result eligibility.
- **QAPage structured data** — **[Google-confirmed]** for pages with one question where users can submit answers (forums, product-support pages that accept user answers). Not for site-authored FAQs, multi-question pages, or blog posts answering a question.

Neither FAQPage nor QAPage schema automatically improves rankings.

## 22. Content Clarity

Give users the answer immediately. Avoid long intros, filler, delayed answers.

Question → Direct answer → Explanation → Evidence → Details → Next action

## 23. The "Core" Principle

**[Framework]** The direct answer appears near the beginning of the page, then: why, exceptions, maintenance/conditions, signals, expert perspective, sources.

Answer-first structure is useful for users and can improve clarity for AI/search systems, but do not claim that AI systems only evaluate the beginning of a page. There is no universal rule that the first section is the only or primary part AI systems understand.

Use clear headings, logical sections and self-contained explanations for human readability and content clarity. Do not treat technical "chunking" as a Google requirement or ranking tactic. **[Google-confirmed]** Google's AI-search guidance says there is no requirement to break content into tiny pieces for AI to understand it, and no ideal page length.

## 24. E-E-A-T

Experience, Expertise, Authoritativeness, Trustworthiness.

**[Google-confirmed]** E-E-A-T is a framework Google uses (notably in its Search Quality Rater Guidelines and helpful-content guidance) to discuss qualities of helpful, trustworthy content. Google explicitly states that E-E-A-T itself is not a specific ranking factor. Search systems use many signals that can identify aspects related to experience, expertise, authoritativeness and trustworthiness.

- Trust is the most important member of the family.
- First-hand experience can be valuable.
- Author credibility and sourcing matter.
- Treat E-E-A-T as a content-quality framework, not a single ranking signal.

In practice, demonstrate who created the content, relevant expertise, first-hand experience, sources, credentials, organization information, transparent methodology, evidence.

## 25. Entity SEO

**[Industry practice]** Optimize for brand and knowledge connections: Brand → Product → Founder → Organization → Industry → Location → Experts → Topics → Publications → Reviews → Mentions. Establish a coherent entity footprint.

## 26. Brand Mentions

**[Industry practice]** Treated by practitioners as an authority/visibility component across publications, forums, social, industry sites, directories, reviews, podcasts, communities.

Do not pursue artificial or inauthentic mentions simply to manufacture an SEO signal. **[Google-confirmed]** Google specifically cautions that inauthentic mentions are not necessarily helpful.

## 27. Parasite SEO

**[Source-specific tactic]** — explanatory only; **not a strategy for House of Diams.** The source describes using high-authority platforms (Medium, Substack, LinkedIn, Reddit, GitHub, Instagram, Facebook, Claude Artifacts) to rank content on the host's strength.

**[Google-confirmed]** Publishing third-party content primarily to exploit a host site's ranking signals can violate Google's site reputation abuse spam policy. Publishing on an authoritative platform also does not transfer its authority to your own domain.

Distinguish:
- **Legitimate third-party publishing** — genuine contributions, PR, expert commentary, community participation, brand profiles that serve that platform's audience.
- **Parasite SEO** — content placed mainly to borrow the host's ranking signals.

## 28. Keyword-Rich / Exact-Match Domains

**[Source-specific tactic]** The source describes specialized keyword domains targeting search areas and linking to a primary brand. This is not a recommendation to buy keyword domains for SEO advantage.

**[Google-confirmed]** Google has an exact-match domain system intended to prevent excessive ranking credit from domains that closely match queries. Domain relevance can still have practical branding/semantic value, but an exact-match domain should not be treated as a shortcut to rankings. Extra domains also fragment the brand and can create doorway-page/link-scheme risk.

## 29. Technical SEO

Crawlability, indexability, URL structure, canonicals, metadata, page speed, schema, internal linking, site architecture, HTML structure, technical performance.

## 30. Schema

Structured data helps search engines understand page information (Organization, Product, Article, Breadcrumbs, LocalBusiness, Events, Reviews where eligible).

**[Google-confirmed]**
- Structured data can make pages eligible for certain rich-result features. It does not guarantee rich results and should not be described as a direct ranking boost.
- JSON-LD is the recommended format where supported.
- Markup must accurately represent the visible page content.
- Google does not require special schema specifically for generative AI search features.

## 31. Page Speed

**[Google-confirmed]** Google states that Core Web Vitals are used by its ranking systems. They are one part of page experience and are not a single ranking signal or a substitute for relevance and helpfulness. Google can still show highly relevant content even when page experience is sub-par. Speed also affects user experience, mobile experience and conversion. Good content + technical quality + speed belong to the same system.

## 32. The 2 MB Googlebot Fetch Limit / Byte-Level Optimization

**[Google-confirmed]** Googlebot currently fetches up to 2 MB for an individual URL, including HTTP headers. PDFs have a separate 64 MB limit. Referenced CSS and JavaScript resources have their own fetch limits. Other Google crawlers may have different limits. Bytes beyond the cutoff are not fetched, rendered or indexed. Google notes the limit is not set in stone and may change.

This is a documented Googlebot fetching limit, not a universal 2 MB limit for every search engine, crawler, browser or AI system.

**[Google-confirmed]** Google's crawler guidance recommends placing critical elements — meta tags, title, link elements, canonical and essential structured data — high in the HTML so they are unlikely to fall below the cutoff, and keeping HTML lean:
- Keep important metadata, canonical, title, essential structured data and critical content early in the HTML where practical.
- Keep HTML lean (avoid inlined bloat, oversized scripts/styles, duplicated markup).

The source material's fuller byte-level audit is **[Source-specific tactic]**; apply it only when relevant to a technical SEO task.

## 33. URL Changes (formerly "URL Refreshing")

**[Google-confirmed]** Changing URLs should be treated as a migration, not a ranking reset or freshness tactic. URL changes require careful URL mapping, redirects, canonical handling, internal-link updates and monitoring. Google notes that migrations can cause temporary ranking fluctuations.

**[Source-specific tactic]** The source describes unpublishing a poorly performing page and republishing it on a slightly different slug for a "fresh start." This is an experimental third-party tactic, not an official Google recommendation, and is off by default for HOD (it would also discard accumulated links and history). The useful underlying idea: a stale page may need strategic restructuring rather than endless superficial edits.

## 34. Backlinks

Backlink = another site links to yours. Referring domain = a domain that links to yours.

Relevant, credible links can contribute to discoverability, authority and ranking systems, but backlink quantity alone is not a reliable measure of SEO strength. Link volume is not the goal. **[Google-confirmed]** Links bought or manipulated to pass ranking credit violate Google's link-spam policies.

**[Industry practice]** Analyse number of referring domains, relevance, authority/quality, link context, competitor profiles, linkable assets.

## 35. Competitor Backlink Analysis

Understand link profiles, referring domains, link opportunities — and alongside it, keyword and content gaps.

## 36. Competitor Analysis

Identify competitors → analyse keywords, pages, content, backlinks, topics, architecture → find keyword gaps, content gaps, backlink opportunities.

## 37. SEO Data Stack

**[Framework]** This project's stack — a choice, not a universal requirement.

| Tool | Role |
|---|---|
| DataForSEO (via MCP) | Primary SEO research/data source for this project's research stages (keyword metrics, SERP and competitor data) |
| Ahrefs | Third-party SEO platform from the original study notes; KD metric reference. Not used in this project's research stages |
| Google Search Console | First-party Google search performance/debugging data — strongly recommended |
| GA4 | Behavioural/conversion analytics after users arrive |
| Google Trends | Useful for trend/interest and seasonality analysis |
| Google SERPs | Actual search-result inspection |
| Google Tag Manager | Tracking implementation |
| SuperSEO | AI-assisted search/SERP/content analysis |
| Semrush | Optional — not currently needed |

## 38. Google Search Console

First-party Google data: queries, impressions, clicks, CTR, average position, indexed pages, search appearance, page indexing reports, URL inspection. These are measurement and debugging signals; do not read them as a list of ranking factors.

**[Google-confirmed]** Search Console now also reports performance in eligible generative AI search features such as AI Overviews and AI Mode (Generative AI performance report, impression-based; Discover has its own report). Treat these as an additional first-party visibility/measurement layer, and keep traditional Search performance metrics separate from AI visibility metrics where appropriate. The AI reports do not provide every ranking or visibility detail.

## 39. GA4

What happens after arrival: organic search → landing page → behaviour → engagement → conversion. Ask not only "did we get a click?" but "did the traffic create business value?"

## 40. Google Trends

Is a topic growing, declining, seasonal, region-specific, or spiking? Trends shows relative interest (indexed 0–100), not absolute search volume. Volume alone is not sufficient.

## 41. Google SERP Itself

Manual inspection shows what Google ranks, intent, formats, SERP features, competitor positioning, question patterns, commercial vs informational intent. Tool data + actual SERP observation.

## 42. AI Visibility

**[Industry practice]** Measure LLM mentions: when people ask ChatGPT, Gemini, Perplexity or other generative experiences about the topic, does the brand appear? For Google's own AI features, use the Search Console Generative AI performance report (§38). For other AI systems, mention-tracking tools are third-party and their methods vary; AI answers are non-deterministic, so treat results as directional samples. **[Google-confirmed]** Google notes that no third-party tool has access to its internal ranking or AI systems.

## 43. AEO — Answer Engine Optimization

**[Industry practice]** AEO and GEO are industry terms/frameworks, not separate official Google algorithms. **[Google-confirmed]** Google treats optimizing for its AI features (AI Overviews, AI Mode) as part of normal SEO: the same fundamentals apply, and no special optimization or markup is required. AI-search visibility is a useful additional objective, not a separate discipline with its own confirmed ranking formula.

Traditional SEO: Query → Search results → Website. AEO: Question → Answer → Source. Content becomes more direct, structured, explicit, question-oriented, retrievable.

**[Google-confirmed]** Google Search Console now includes a "Search generative AI" setting controlling whether the property is included in Google's generative AI search experiences. It defaults to inclusion unless the site opts out. HOD workflow: before diagnosing missing AI-search visibility, verify that the property has not opted out. Do not change the setting as part of content work.

`llms.txt` is not required for Google Search or Google's AI search features.

What to emphasize for AI search:
- Search fundamentals still matter — the page has to be crawlable, indexable and eligible to be shown with a snippet.
- Retrieval/discoverability matters.
- Clear structure helps.
- Unique information and first-hand experience matter.
- Strong entities, sources and references can help understanding.
- AI-generated content must provide real value. **[Google-confirmed]** Scaled low-value content (AI or not) can violate Google's scaled content abuse policy.

What not to assume: that AI search has one known ranking formula, that all LLMs rank pages the same way, that AI systems only read the first section, that special schema is required, that every query variation needs its own page, or that more AI-generated pages automatically create more visibility.

## 44. GEO — Generative Engine Optimization

**[Industry practice]** Increase the likelihood that a generative system understands the content, associates it with the right topic/entity, retrieves it, mentions the brand, and cites it. Different AI systems use different retrieval sources and methods.

## 45. The CITE Framework (AEO)

**[Framework]** From the source material — not an official Google framework. Parts of it align with Google's guidance favouring helpful, original, experience-informed content, but CITE itself is not a Google standard.

- **C — Core.** Give the direct answer immediately; no long intros, generic context or marketing fluff.
- **I — Intent by Occasion.** What situation caused the question? The occasion changes the answer (e.g. "best running shoes" for a beginner vs marathon vs injury vs trail vs budget).
- **T — Take a Position.** A clear, defensible point of view supported by evidence. Not "there are many factors," but "for X situation, prioritize Y because…"
- **E — Entity & Endorsement.** Connect content to credible entities: author credentials, background, organization, research, certifications, industry experience, published work, milestones. Who is saying this, and why trust it?

## 46. CITE + E-E-A-T

**[Framework]** CITE makes the content direct, intent-aware, distinctive, entity-connected. E-E-A-T describes a source that is experienced, expert, authoritative, trustworthy. Together: good answer structure + credible source.

## 47. Context as a Competitive Moat

Give AI the company's business model, audience, voice, products, services, expertise, methodology, positioning, design system, SEO architecture, content rules and workflow. AI then operates inside that context.

## 48. Claude as an SEO Architect

Not "write me a blog," but "help architect and execute the website's information system": research, architecture, planning, generation, HTML, auditing, internal linking, technical checks, publishing, monitoring.

## 49. Claude Project Context

Codified instruction areas: (1) project definition — a build-and-publish framework, not a copywriting tool; (2) operating principles — architect, not merely writer; (3) voice & language; (4) frameworks (e.g. CITE); (5) content architecture (hub-and-spoke); (6) design system; (7) technical workflow (JSON, WordPress endpoints, auth, publishing); (8) audit protocol — audit existing inventory for duplication, cannibalization, coverage and consolidation before creating content.

## 50. AI Should Not Become a Content Mill

Bad: AI → 100 blogs → publish. **[Google-confirmed]** Google's guidance is that using AI to generate content is not itself against its policies, but generating many pages primarily to manipulate rankings without adding value is scaled content abuse.

**[Google-confirmed]** Google's current guidance recommends manually fact-checking AI-generated content before publishing, including main content, titles, meta descriptions, structured data and image alt text.

AI-generated ecommerce/product imagery may have additional metadata/disclosure considerations depending on the Google product/surface involved. Verify the current Google requirements before implementing any image metadata workflow.
Better: Business strategy → Search demand → Architecture → Content plan → AI execution → Human review → Publishing → Measurement → Iteration.

## 51. Audit Before Creation

Before a new page: Does the topic exist? Does an existing page target this intent? Would this cannibalize? Should the existing page be improved or merged? Create only when a genuine gap exists.

## 52–54. SEO MCP

**[Industry practice]** Claude Code / GPT → Query → MCP → API call → SEO data provider → data → AI analysis. MCP is an integration/orchestration layer between the AI assistant and SEO APIs. Its freshness and accuracy depend on the underlying data source/API — it is "real-time" only where the provider is (e.g. live SERP endpoints vs periodically updated keyword databases).

Data categories: SERP data (rankings, featured snippets); keyword research (volume, difficulty, trends); backlink analysis (link profiles, referring domains); on-page (meta tags, speed); domain analysis (traffic, tech stack, authority); competitor analysis (keyword/content gaps); content analysis (topic clusters, intent mapping); business data (local listings/leads); AI visibility (LLM mention tracking).

## 55–56. Automated Keyword Research Agent

**[Framework]** FIND (universe) → FILTER (volume, KD, intent, business relevance) → CLUSTER (topic/page clusters) → PRIORITIZE (which page, content type, order, business value) → BUILD (page architecture).

Example (plumbing): 340 keywords → 19 clusters; water heater repair / emergency plumber / drain cleaning → service pages; water heater cost / how to unclog a drain → blog.

## 57. SEO Architecture vs Content Calendar

Content calendar: "What should we publish this month?" Architecture: "What pages should this website have in the first place?" Architecture comes first; the calendar executes it.

## 58–61. Monitoring Agent

**[Framework]** SEO newsletters/industry sources → monitoring agent → collect updates → Claude compares with context → relevant? what's affected? → proposed actions → Google Sheet (update, date, source, relevance, pages affected, action, status) → Telegram notification.

Make.com or n8n — tool choice is secondary. Define outcome → workflow → tool.

## 62. SEO Newsletter Intelligence

Sources: SEO FOMO and AI Marketers (Aleyda Solis), Growth Memo (Kevin Indig), The SEO Notebook (Steve Toth), Marie Haynes Newsletter. The system should answer "does this matter to our website?", not forward everything.

## 63. Context-Loaded AI

A website-specific agent knows what the company sells, audience, brand, existing and important pages, architecture, keywords, tone, methodology, goals, tech stack.

## 64. AI Output ≠ SEO Outcome

100 articles/FAQs/metas/posts do not automatically create rankings, traffic, authority, citations or conversions. Outcome depends on the broader system.

## 65. Multimedia & AI Retrieval

Providing a transcript can improve accessibility, text-based discoverability, and the ability of search/retrieval systems to process the information. Do not claim that search engines or AI systems categorically cannot understand audio. Workflow: podcast → transcript → key takeaways → structured page → references.

## 66. SEO as an Entity/Knowledge System

Brand ├ Products ├ Services ├ People ├ Experts ├ Topics ├ Locations ├ Publications ├ Reviews ├ Backlinks ├ Mentions └ Content. The website is a structured representation of the business and its expertise; external sites reinforce those relationships.

## 67. Modern SEO Stack

**[Framework]** A layered planning model, not a ranking formula.

1. **Technical** — crawlability, indexing, speed, metadata, schema, URLs
2. **Search demand** — keyword research, volume, KD, trends, SERP analysis
3. **Architecture** — universe, clusters, intent, hubs, spokes, hierarchy
4. **Content** — core answers, supporting content, use cases, FAQs, cornerstone pages, expert perspectives
5. **Authority** — backlinks, referring domains, mentions, E-E-A-T, entities
6. **AI search** — AEO, GEO, AI visibility, LLM mentions, citability
7. **Automation** — MCP, SEO APIs, agents, n8n/Make, Sheets, Telegram

## 68. Complete SEO Workflow

**[Framework]** 1. Understand the business → 2. Define products/services → 3. Research demand → 4. Generate universe → 5. Filter → 6. Intent → 7. Cluster → 8. Competitors → 9. Content gaps → 10. Backlink gaps → 11. Site architecture → 12. Hubs/cornerstones → 13. Spokes → 14. Map keywords → pages → 15. Build/update core pages → 16. Supporting content → 17. Internal linking → 18. Technical SEO → 19. Schema → 20. Authority/backlinks/mentions → 21. AEO → 22. GEO/AI visibility → 23. Measure → 24. Update → 25. Repeat

On step 24: update content when information has materially changed, become outdated, or can be meaningfully improved. Do not change dates or make superficial edits simply to create an appearance of freshness.

## 69. The AI-Powered Version

AI SEO agent → (keyword research, SERP data, competitor analysis) → SEO MCP → SEO APIs → current data (freshness depends on the source) → AI interpretation → **human strategic review** → site architecture → execution → measurement → monitoring.

## 70. Core SEO Philosophy — 10 Principles

**[Framework]** This project's operating principles.

1. **Strategy before content** — start with "what should the website own?"
2. **Search demand before page creation.**
3. **Keywords → clusters → pages** — not one page per keyword.
4. **Architecture before publishing.**
5. **Blogs support the business** — topics, hubs, products, services, authority.
6. **Authority matters** — relevant links, referring domains, mentions, entities, expertise, trust (quality over volume).
7. **Answer first** — then explain.
8. **Be distinctive** — experience, evidence, original analysis, defensible opinions, unique methodology.
9. **Context is the AI moat.**
10. **Automate execution, not judgment.**

## 71. The Final Mental Model

**[Framework]** A mental model of how the pieces relate, not Google's ranking pipeline.

```
                    BUSINESS
                        ↓
                 SEARCH DEMAND
                        ↓
                KEYWORD UNIVERSE
                        ↓
                FILTER + INTENT
                        ↓
                  CLUSTERING
                        ↓
               PAGE ARCHITECTURE
             ┌──────────┴──────────┐
           HUBS                  SPOKES
       / CORNERSTONE          / SUPPORTING
             └──────────┬──────────┘
                 INTERNAL LINKS
                        ↓
                TOPICAL AUTHORITY
        ┌───────────────┼────────────────┐
      CONTENT       BACKLINKS       BRAND / ENTITY
        └───────────────┼────────────────┘
                  SEARCH VISIBILITY
             ┌──────────┴──────────┐
            SEO                   AEO
        Search ranking        Direct answers
             └──────────┬──────────┘
                       GEO
                        ↓
                 AI VISIBILITY → LLM MENTIONS
                        ↓
                  MEASUREMENT → ITERATION

   Underneath: AI agent → MCP → SEO APIs → source data
               → research/analysis → automation → Sheets / Telegram → change tracking
```

**The single biggest takeaway:** build a search-driven information architecture around real business demand, establish topical and entity authority through interconnected content and external signals, structure information so humans and answer engines can retrieve it, and use AI + data + automation to continuously research, execute, monitor and improve the system.
