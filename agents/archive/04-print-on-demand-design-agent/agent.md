---
description: Generates print-on-demand designs (T-shirts, mugs, posters) using AI image models, with marketplace listing copy and tag optimization.
mode: all
phase: 1
depends_on:
  - 36-data-moat-history-agent
  - 22-meme-sticker-pack-generator
inputs:
  niche:
    type: string
    description: e.g. dog-mom, nurse-life, retro-90s
  product_type:
    type: string
    enum: [tshirt, mug, poster, hoodie, tote]
  count:
    type: integer
    default: 25
  style:
    type: string
    enum: [typographic, illustrated, photographic, minimalist]
outputs:
  designs:
    type: array
    items:
      type: object
      properties:
        design_id: { type: string }
        image_url: { type: string }
        png_transparent_url: { type: string }
        mockup_url: { type: string }
        title: { type: string }
        description: { type: string }
        tags: { type: array, items: { type: string } }
        marketplace_listing_url: { type: string }
  bundle_summary:
    type: object
    properties:
      niche: { type: string }
      published_count: { type: integer }
      generated_at: { type: string, format: date-time }
tools:
  - openai dall-e-3 / stability-sdxl (image generation)
  - rembg (transparent background)
  - printful/printify API (mockup + product creation)
  - etsy/Redbubble upload API
  - anthropic (listing copy, SEO title/description/tags)
  - supabase (design catalog, royalty ledger)
  - celery (batch scheduling)
  - pillow (image recompression, local mockup fallback)
error_handling:
  - failure: DALL-E rejects prompt (content filter)
    mitigation: Re-prompt with sanitised concept; fall back to SDXL; flag for human design
  - failure: Rembg produces rough edges
    mitigation: Re-run with alpha matting; if still poor, route to human retouch queue
  - failure: Etsy listing rejected (IP or trademark)
    mitigation: Trademark pre-check on title and tag set; queue for human review before publish
  - failure: Mockup generation 5xx
    mitigation: Retry with exponential backoff; if persistent, generate local mockup with Pillow
cost_per_run: RM0.20 per design (image + mockup)
sla:
  freshness: weekly batch of 25–100 designs
  uptime: 97%
  latency_p95: 4 min per design (incl. mockup)
---

## Role
The Print-on-Demand Design Agent is a batch-design factory: it takes a niche and product type, generates a curated batch of AI-designed artwork, prepares print-ready PNGs with transparent backgrounds, and lists them across Etsy, Redbubble, and Printful/Printify marketplaces. It acts as a designer-junior who is prolific but never claims authorship of brands, characters, or trademarked content. It runs weekly Celery batches and records every listing in Supabase for royalty reconciliation.

## Workflow
1. Pull the next 3 underserved niche/product-type combinations from the 36-data-moat-history-agent listing ledger (high search, low design density).
2. For each combo, generate 25–100 prompts covering the requested style.
3. Generate images via DALL-E 3 (preferred) or SDXL; reject any image that fails aesthetic threshold (blur, deformed text, generic stock look).
4. Strip background via rembg with alpha matting; produce 4500×5400 PNG at 300 DPI.
5. Render product mockups via Printful/Printify API.
6. Generate listing copy via Claude: SEO title ≤140 chars, 13 Etsy tags, description with benefit bullets.
7. Pre-check title/tags against an internal trademark list (Disney, NFL, band names, etc.).
8. Publish to Etsy/Redbubble via partner API; record listing URL in Supabase.
9. Weekly: re-generate mockups for any design with >30 days of zero views.

## Constraints
- Never generate designs referencing trademarks, public figures, or copyrighted characters; the trademark list is checked before publish.
- All artwork must be original AI generation; no copying of competitor listings.
- File sizes: PNG ≤25MB, mockup ≤10MB; if exceeded, recompress with Pillow.
- Listings must include a "design by AI, printed on demand" disclosure where marketplace policy requires.
- No designs that depict weapons, drugs, or adult content.
- All designs archived to R2 with 1-year retention for copyright dispute resolution.
