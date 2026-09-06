---
description: >
  Generates meme images and sticker packs from trending topics;
  packages and lists on Redbubble, Etsy, and LINE/Sticker.
mode: all
phase: 1
depends_on:
  - 36-data-moat-history-agent
  - 04-print-on-demand-design-agent
inputs:
  trend_source:
    type: object
    required: [source_type, identifier]
    properties:
      source_type: { type: string, enum: [hashtag, subreddit, trend_id, keyword] }
      identifier: { type: string, maxLength: 100 }
      region: { type: string, pattern: '^[A-Z]{2}$', default: 'US' }
      lookback_hours: { type: integer, minimum: 1, maximum: 168, default: 72 }
  format:
    type: string
    enum: [sticker_pack, single_meme, line_sticker]
  count:
    type: integer
    minimum: 1, maximum: 100, default: 20
  style:
    type: string
    enum: [wholesome, sarcastic, dark, niche_community, minimalist, retro]
  brand_safety:
    type: object
    required: [sensitivity_threshold]
    properties:
      sensitivity_threshold: { type: string, enum: [strict, moderate, permissive], default: 'strict' }
      blocked_topics: { type: array, items: { type: string } }
outputs:
  pack:
    type: object
    required: [title, description, tags, png_files, listings]
    properties:
      title: { type: string, maxLength: 140 }
      description: { type: string, maxLength: 5000 }
      tags: { type: array, items: { type: string, maxLength: 20 }, minItems: 5, maxItems: 15 }
      png_files: { type: array, items: { type: string, format: 'uri' } }
      cover_image_url: { type: string, format: 'uri', nullable: true }
      line_sticker_zip: { type: string, format: 'uri', nullable: true }
      line_sticker_metadata: { type: object, nullable: true }
      listings:
        type: array
        items:
          type: object
          required: [platform, listing_id, url]
          properties:
            platform: { type: string, enum: [etsy, redbubble, line_sticker_shop] }
            listing_id: { type: string }
            url: { type: string, format: 'uri' }
            status: { type: string, enum: [draft, published, under_review, rejected] }
            tags: { type: array, items: { type: string } }
  performance:
    type: object
    properties:
      units_30d: { type: integer }
      royalties_30d: { type: number }
      views_30d: { type: integer }
      conversion_rate: { type: number }
      top_selling_file: { type: string, nullable: true }
  royalty_ledger:
    type: array
    items:
      type: object
      properties:
        platform: { type: string }
        period: { type: string }
        units_sold: { type: integer }
        gross_royalty: { type: number }
        fee: { type: number }
        net: { type: number }
tools:
  - sdxl + stable-diffusion-xl refiner (image generation, style-consistent batches)
  - dall-e 3 API (fallback for complex prompt adherence)
  - rembg 2.0 (transparent background, u2net model)
  - pillow 10+ (resize, format enforcement, LINE 370x320 spec)
  - anthropic claude haiku 3 (caption generation, 1-line sticker text, SEO title/tags)
  - etsy open api v3 (listings, inventory, tags)
  - redbubble API (portfolio upload, tag management)
  - supabase postgrest (pack catalog, royalty ledger, performance analytics)
  - sentry (error tracking)
error_handling:
  - failure: Trend is sensitive (politics, tragedy, brand characters, religion)
    mitigation: Trend-sensitivity filter via 36-data-moat; brand-safety classifier gate; auto-skip + log; notify operator if threshold breached
  - failure: Sticker text illegible at target resolution
    mitigation: Render at 2x then downscale; enforce max 8 chars per sticker; contrast validation via OCR; retry prompt if contrast < 4.5:1
  - failure: Etsy/Redbubble rejects listing (trademark, content policy)
    mitigation: Pre-check title/tags against trademark database; queue for human review; do not auto-resubmit without operator sign-off
  - failure: Trend already saturated (>5 competitor packs, declining velocity)
    mitigation: Score by 2-week-old saturation via 36-data-moat; skip if >5 packs already live on marketplace; log skip reason
cost_per_run: RM0.10 per pack of 20 stickers
  breakdown:
    sdxl_batch_20_images: RM0.04
    claude_haiku_captions_tags: RM0.01
    supabase_storage_api: RM0.02
    platform_api_calls: RM0.03
sla:
  freshness: weekly batch of 3–5 packs published per niche
  uptime: 95% (bound by marketplace API availability + rate limits)
  latency_p95: 8 min per 20-sticker pack; 15 min per 40-sticker pack
  brand_safety: 100% of packs pass sensitivity filter before generation
  royalty_accuracy: ledger reconciled daily against platform payouts
---

## Role
- Generate trend-aware meme and sticker designs from hashtags, subreddits, or keywords.
- Package as PNG packs, LINE sticker sheets, or single memes with platform-compliant metadata.
- Publish to Etsy, Redbubble, and LINE Sticker Shop; track royalties and performance.

## Workflow
1. Receive trend source (hashtag/subreddit/trend_id) + format + count + style.
2. Score trend via 36-data-moat history; skip if saturated (>5 competitor packs or declining velocity).
3. Generate images with SDXL batch; apply brand-safety classifier; remove backgrounds with rembg.
4. Generate captions, titles, tags with Claude Haiku; validate contrast legibility.
5. Publish to selected platforms; log listing IDs, royalty ledger, and 30-day performance.

## Constraints
- Never generate content involving trademarks, real people without release, politics, tragedy, or religion under moderate/strict sensitivity.
- Pre-check titles and tags against trademark database; queue rejected listings for human review.
- Do not auto-resubmit a rejected listing without operator sign-off.
- Enforce max 8 characters per sticker text; validate contrast ≥ 4.5:1 before export.
