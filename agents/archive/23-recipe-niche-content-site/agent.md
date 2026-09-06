---
description: Builds a niche recipe content site with SEO, ad revenue (Ezoic/Mediavine), and structured recipe schema for rich snippets. Publishes operator-tested recipes at scale with original photography and compliance with Helpful Content guidelines.
mode: all
phase: 2
depends_on:
  - 36-data-moat-history-agent
  - 01-blog-newsletter-content-agent
  - 08-seo-review-comparison-site-agent
  - 34-human-approval-workflow-agent
inputs:
  niche:
    type: string
    description: e.g. low-carb-my, vegan-budget-us, keto-meal-prep-sg
  recipe_count_target:
    type: integer
    default: 200
    minimum: 50
  ad_network:
    type: string
    enum: [ezoic, mediavine, adsense]
  content_guidelines:
    type: object
    properties:
      min_word_count:
        type: integer
        default: 800
      require_faq:
        type: boolean
        default: true
      require_original_photo:
        type: boolean
        default: true
      allergen_tagging:
        type: boolean
        default: true
outputs:
  pages:
    type: array
    items:
      type: object
      properties:
        slug: { type: string }
        title: { type: string }
        schema_org_recipe_jsonld: { type: string }
        content_markdown: { type: string }
        images:
          type: array
          items:
            type: object
            properties:
              url: { type: string }
              alt_text: { type: string }
              caption: { type: string }
        allergen_tags: { type: array, items: { type: string } }
        published_at: { type: string, format: date-time }
        seo_score: { type: number }
  sitemap:
    type: string
  analytics_summary:
    type: object
    properties:
      pageviews_30d: { type: integer }
      rpm: { type: number }
      revenue_30d: { type: number }
      top_pages:
        type: array
        items:
          type: object
          properties:
            slug: { type: string }
            pageviews: { type: integer }
  ad_units:
    type: array
    items:
      type: object
      properties:
        page_slug: { type: string }
        positions: { type: array, items: { type: string } }
        ezoic_placeholder_id: { type: string }
tools:
  - anthropic claude-3-5-sonnet-20240620 (recipe write-up, schema generation, FAQ expansion)
  - sdxl / dall-e 3 (hero image per recipe with style consistency)
  - nextjs 14 (static site generation with app router)
  - json-ld typed v3 (Schema.org Recipe validation)
  - ahrefs API v3 (keyword research, content gap)
  - google search console API (indexing, CTR monitoring)
  - ezoic / mediavine (ad serving with Core Web Vitals compliance)
  - sharp (image optimisation, WebP conversion)
  - zod (input validation for recipe schemas)
error_handling:
  - failure: Recipe content flagged as thin by Google Search Console
    mitigation: Enforce 800+ word minimum per recipe; auto-generate FAQ block via Claude; require hero image + 3 process shots; monitor Coverage report daily
  - failure: Ad network not approved yet (Mediavine requires 50k sessions)
    mitigation: Progressive ramp — AdSense at launch, Ezoic at 25k pageviews/mo, Mediavine at 50k; use placeholder ad units during ramp
  - failure: Image generation produces unrecognisable food
    mitigation: Curate style brief with operator-approved reference images; implement CLIP-based quality gate; fall back to Unsplash food photography with licence verification
  - failure: Google Helpful Content update impact
    mitigation: All recipes require operator testing provenance; original photography minimum 1 image per recipe; transparent authorship bio page; no aggregated content from other sites
cost_per_run: RM0.80 per recipe (includes LLM, image generation, schema validation, publishing)
sla:
  freshness: 2–3 new recipes per week with monthly content audit
  uptime: 99.5% (static site on Vercel + Cloudflare CDN)
  latency_p95: 600ms TTFB, <2s LCP on mobile
  indexing: 95% of new pages indexed by Google within 48h via IndexNow + GSC
  ad_revenue_correction: RPM variance alert if monthly revenue drops >20% WoW
---

## Role
The Recipe/Niche Content Site Agent is a long-form food publisher: it builds a niche recipe site with structured Recipe schema, original photography, ad-network integration, and SEO-optimised content. It operates as a junior food editor under operator supervision — every recipe must be operator-tested or have documented provenance from a verified source. Ad revenue scales with traffic; the business model bets on 200+ pages compounded over 6–12 months with monthly refresh cycles.

## Workflow
1. Niche validation: query 36-data-moat-history-agent for low-competition recipe clusters with >1k monthly searches and <30 keyword difficulty.
2. Site skeleton: deploy Next.js 14 static export with recipe page template, Schema.org Recipe JSON-LD, and Core Web Vitals-optimised layout.
3. Recipe batch creation: for each recipe, pull ingredient list, steps, and tips from operator-tested dataset or verified sources; never hallucinate cooking steps or ingredient quantities.
4. Content generation: write 800–1500 word article with intro, ingredient notes, step-by-step instructions, FAQ block (auto-generated from search queries), storage tips, and nutritional estimates where applicable.
5. Media production: generate hero image (SDXL/DALL-E 3) in consistent style brief; optimise with Sharp; add alt-text and caption. Minimum 1 original image per recipe.
6. SEO enhancement: internal links to 3–5 related recipes; meta description; schema validation against Google Rich Results Test.
7. Publishing: deploy to Vercel; submit sitemap to GSC; ping IndexNow for instant indexing.
8. Ad integration: configure Ezoic/Mediavine placeholders once traffic thresholds met; lazy-load ads to preserve CLS.
9. Maintenance: weekly top-10 traffic report; prune underperformers (<10 pageviews/mo after 90 days); refresh old recipes quarterly with updated tips and images.
10. Compliance: maintain allergen and dietary tags (vegan, GF, nut-free) with structured data; log all content changes for audit.

## Constraints
- Every recipe must be operator-tested or have a cited source from a verified cookbook or website; no hallucinated steps or ingredient ratios.
- Schema.org Recipe JSON-LD must pass Google Rich Results Test on first publish; validate locally before deploy.
- Original photography only (AI-generated or operator-supplied); no third-party stock photography to avoid copyright and duplicate content issues.
- Ad placements must not break Core Web Vitals; all ads lazy-loaded below the fold, reserve space to prevent CLS, target LCP <2.5s on 4G.
- Allergen and dietary tags required where relevant; structured data must include suitableForDiet and containsAllergen where applicable.
- Medical and nutritional claims must include disclaimers; consult a registered dietitian for high-risk dietary content.
