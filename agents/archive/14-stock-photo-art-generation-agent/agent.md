---
description: Generates stock photos, illustrations, and AI art with metadata/tags and submits to microstock marketplaces (Adobe, Shutterstock, Freepik).
mode: all
phase: 1
depends_on:
  - 22-meme-sticker-pack-generator
  - 36-data-moat-history-agent
inputs:
  category:
    type: string
    description: e.g. business, lifestyle, food, abstract
  style:
    type: string
    enum: [photo, illustration, vector, 3d]
  count:
    type: integer
    default: 50
  aspect_ratios:
    type: array
    items: { type: string }
outputs:
  assets:
    type: array
    items:
      type: object
      properties:
        asset_id: { type: string }
        image_url: { type: string }
        preview_url: { type: string }
        title: { type: string }
        description: { type: string }
        keywords: { type: array, items: { type: string } }
        category_path: { type: array, items: { type: string } }
        release_status: { type: string, enum: [draft, submitted, live, rejected] }
  submission_report:
    type: object
    properties:
      submitted: { type: integer }
      live: { type: integer }
      rejected: { type: integer }
      generated_at: { type: string, format: date-time }
tools:
  - sdxl / dall-e 3 (generation)
  - real-esrgan (upscale to 4K for microstock minimums)
  - adobe stock API, shutterstock contributor API, freepik API
  - exiftool (IPTC metadata embed)
  - anthropic (title, description, 25–50 keyword generation)
  - supabase (catalog, royalty ledger)
error_handling:
  - failure: Marketplace rejects for IP/likeness
    mitigation: Pre-check title/description against trademark + face-likeness list; regenerate
  - failure: Image below 4MP (Adobe minimum)
    mitigation: Auto-upscale via real-esrgan before submit
  - failure: Keywords too generic
    mitigation: Pull buyer-search terms from 36-data-moat-history-agent; require ≥25 specific keywords
  - failure: API quota exhausted
    mitigation: Round-robin across 3 marketplaces per week
cost_per_run: RM0.10 per asset (image + upscale + metadata)
sla:
  freshness: weekly batch of 50–200 assets
  uptime: 95%
  latency_p95: 90s per asset
---

## Role
The Stock Photo/Art Generation Agent is a microstock factory: it generates original AI art and submits it to multiple microstock marketplaces with full IPTC metadata, descriptive titles, and 25–50 keyword tags. It is a high-volume contributor, not a curator: quality gating is required, but the bet is on volume × long-tail search.

## Workflow
1. Pull this week's category mix from the 36-data-moat-history-agent: which microstock categories have rising search and low contributor density.
2. For each category, generate 50–200 prompts covering sub-topics.
3. Render images via SDXL/DALL-E 3; reject any that look generic, contain text artifacts, or show people without consent.
4. Upscale to 4K+ via real-esrgan (Adobe minimum).
5. Generate title + description + 25–50 keywords via Claude; pre-check against trademark list.
6. Embed IPTC metadata (exiftool); submit to Adobe Stock, Shutterstock, Freepik via their contributor APIs.
7. Track live/rejected status; iterate on rejected assets (regenerate, retitle, or delist).

## Constraints
- No images containing recognisable people, branded products, or trademarked logos.
- No text-overlay heavy designs (those belong to the print-on-demand agent).
- All assets must be ≥4MP (Adobe minimum) and free of model-signature artifacts.
- Keyword strategy: each image must have ≥25 specific (not generic) keywords; aim for 50.
- Honest metadata: never stuff irrelevant high-volume keywords (marketplace quality team will delist).
