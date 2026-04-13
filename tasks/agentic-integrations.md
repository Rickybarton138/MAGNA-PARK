# Agentic AI API Integrations — magna-park

Priority: **P3 — Secondary** (active — socials setup)
Master plan: `~/agentic-ai-apis/INTEGRATION_PLAN.md`

## Prerequisite
Apify MCP must be connected. See master plan.

## Agents to wire in

Reuse the astra-removals SEO stack (same agents, different target):

| Agent | Purpose |
|---|---|
| [Employee-in-a-Box: SEO/AEO/GEO Auditor](https://apify.com/gmangabeira2/employee-in-a-box-seo-aeo-geo-auditor) | Monthly SEO + Answer Engine + Generative Engine audit for Bournemouth self-storage keywords |
| [Keyword Opportunity Finder](https://apify.com/trovevault/keyword-opportunity-finder) | People Also Ask scraping — "self storage Bournemouth", "container storage Dorset", etc. |
| [Long-Tail Keyword Discovery](https://apify.com/powerai/long-tail-keyword-discovery) | Long-tail keyword batches per local area |
| [AI Content Writer](https://apify.com/erinle_sam/ai-content-writer) | Blog post generation with local SEO focus |
| [AI Brand Visibility](https://apify.com/adityalingwal/ai-brand-visibility) | Weekly GEO tracking — ChatGPT/Gemini/Perplexity mentions for "self storage Bournemouth" |
| [Comments Analyzer Agent](https://apify.com/apify/comments-analyzer-agent) | Reputation monitoring |
| [Advanced Social Media Agent](https://apify.com/fiery_dream/advanced-social-media-agent) | Social media analytics for the socials setup work |

## Environment vars
```
APIFY_TOKEN=
```

## Next action
Once socials are live, run SEO/AEO/GEO Auditor against magna-park domain to baseline. Then weekly AI Brand Visibility check to monitor Bournemouth storage search visibility.
