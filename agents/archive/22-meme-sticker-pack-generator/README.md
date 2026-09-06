# 22. Meme/sticker pack generator

## Metrics

| Metric | Value |
| --- | --- |
| Risk | Low |
| Capital Required | RM0–RM200 |
| Success Probability | Low (20–40% without trend-moat; 40–60% with 36-data-moat integration) |
| Time to First RM | 1–2 months |
| Skills Needed | Image-gen prompting, trend awareness, marketplace listing, basic brand-safety review |

## Stack

| Layer | Choice | Why |
| --- | --- | --- |
| Image generation | SDXL + Stable Diffusion XL Refiner | Volume batch, style-consistent, 20–40 images per prompt set |
| Fallback image gen | DALL-E 3 API | Prompt adherence for complex scenes |
| Background removal | rembg 2.0 (u2net) | Free, on-device, batch-capable |
| Format enforcement | Pillow 10+ | LINE 370x320 spec, PNG transparency, Etsy print-ready DPI |
| Captions / copy | Anthropic Claude Haiku 3 | Fast, cheap caption generation, SEO title/tags |
| Listings | Etsy Open API v3 + Redbubble API | Direct upload, tag management, inventory sync |
| LINE Sticker Shop | Manual upload via LINE Creators Market | Required by LINE; ZIP + metadata pre-packaged |
| Trend data | 36-data-moat-history-agent | Rising, not yet saturated; brand-safety classifier |
| Catalog | Supabase postgrest | Pack catalog, royalty ledger, performance analytics |
| Tracking | Sentry | Error tracking across marketplace API failures |

## Execution Plan

| Week | Step |
| --- | --- |
| 1 | Open Etsy + Redbubble shops; set up LINE Creators account; install SDXL + rembg locally |
| 2 | Generate 5 packs manually, list on Etsy as seed; validate format, tags, title compliance |
| 3 | Build agent pipeline: trend → prompt → image → pack → listing; integrate 36-data-moat for trend scoring |
| 4 | Add trend-sensitivity filter and trademark pre-check; enforce 8-char text cap + contrast validation |
| 5 | Layer in LINE Sticker Shop format (370x320 PNGs, ZIP + metadata) and upload pipeline |
| 6–8 | Compound: 3–5 packs/week; kill underperformers (<5 sales in 14 days); double winners |
| 9–12 | Add 04-print-on-demand-design-agent for physical sticker fulfilment via Printful; A/B test pricing |

## Unit Economics

| Item | Cost (RM) | Revenue (RM) |
| --- | --- |
| SDXL batch 20 images | 0.04/pack | – |
| Claude Haiku captions + tags | 0.01/pack | – |
| Supabase storage + API | 0.02/pack | – |
| Platform API calls | 0.03/pack | – |
| **Variable cost per pack** | **0.10/pack** | – |
| Etsy listing fee | 0.20/listing | – |
| Etsy transaction (6.5%) | – | on revenue |
| Redbubble base margin | – | 10–20% of sale price |
| Avg digital pack sale | – | 5–20 |
| Avg physical sticker sale | – | 8–30 |
| Break-even | 20–50 pack sales | – |
| Gross margin | – | ~80–95% |

## Known Failure Modes

| Failure | Mitigation |
| --- | --- |
| Sensitive trend (politics, tragedy, religion) | Brand-safety classifier gate via 36-data-moat; auto-skip + log; notify operator if threshold breached |
| Sticker text illegible at target resolution | Render at 2x then downscale; enforce max 8 chars per sticker; contrast validation via OCR; retry prompt if contrast < 4.5:1 |
| Etsy/Redbubble rejects listing (trademark, content) | Pre-check title/tags against trademark database; queue for human review; do not auto-resubmit without operator sign-off |
| Trend already saturated (>5 competitor packs) | Score by 2-week-old saturation via 36-data-moat; skip if >5 packs already live on marketplace; log skip reason |

## First Milestone

**Day 30:** 20 packs published across 2–3 marketplaces, first 5 sales, RM100 revenue, top-performing pack identified for volume scaling.
