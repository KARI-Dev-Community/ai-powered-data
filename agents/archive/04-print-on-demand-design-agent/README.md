# 04-print-on-demand-design-agent

## Metrics

| Metric | Value |
|--------|-------|
| Risk | Low–Medium (marketplace saturation, IP risk) |
| Capital | RM400–RM900/month (image gen APIs, mockup API, listing fees) |
| Success Probability | 60% (niche selection + volume-dependent) |
| Time to First RM | 45–90 days (first sale on Etsy/Redbubble) |
| Skills Needed | Prompt engineering, image generation, marketplace SEO |

## Stack

| Layer | Choice | Why |
|-------|--------|-----|
| Image Gen | OpenAI DALL-E 3 (primary) / SDXL (fallback) | Prompt adherence, brand-safe, cost control |
| Background Removal | rembg (U2-Net) | Fast, batchable, alpha matting |
| Mockups | Printful / Printify API | Auto-generate product previews at 300 DPI |
| Marketplaces | Etsy API + Redbubble upload | High-intent buyers, low entry barrier |
| Copy | Anthropic Claude Sonnet 4 | SEO titles, 13-tag sets, benefit bullets |
| Storage | Supabase + R2/S3 | Design catalog, royalty ledger, asset archive |
| Scheduling | Celery + Redis | Weekly batch runs, retry on mockup failures |
| Trademark Check | Internal deny-list + USPTO/TMDB lookup | Pre-publish IP risk reduction |

## Execution Plan

| Week | Steps |
|------|-------|
| 1 | Niche validation via 36-data-moat (search vol, design density). Set up DALL-E/SDXL accounts, Etsy seller account, Printful/Printify integration. |
| 2 | Manually generate 25 designs for test niche. Run trademark pre-check. Publish first batch; measure CTR and conversion. |
| 3 | Automate weekly Celery batch (25–100 designs). Calibrate aesthetic threshold (reject blur/deformed-text). Enable Pillow fallback for mockup failures. |
| 4 | Expand to 2nd niche. A/B test style prompts (typographic vs illustrated). Monitor Etsy SEO rank for target tags. |
| 5–8 | Hit 100 designs published. Re-generate mockups for zero-view listings. Introduce Redbubble auto-upload for secondary revenue. |
| 9–12 | Negotiate bulk Printful discounts. Test limited-edition drops for urgency. Begin Pinterest organic traffic campaign. |

## Unit Economics

| Cost Item | RM/month | Revenue Item | RM/month |
|-----------|----------|--------------|----------|
| DALL-E / SDXL API | 100–200 | Etsy sales (net after Printful cut) | 400–2,000 |
| Printful/Printify mockup API | 50–100 | Redbubble royalties | 100–500 |
| VPS + Celery + Supabase | 80–150 | Direct POD orders (own store) | 0–500 |
| Etsy listing fees + ads | 50–150 | | |
| Trademark check API | 20–50 | | |
| **Total** | **300–650** | **Total** | **500–3,000** |

## Known Failure Modes

| Failure | Mitigation |
|---------|-----------|
| DALL-E rejects prompt (content filter) | Re-prompt with sanitised concept; fall back to SDXL; flag for human design |
| Rembg produces rough edges | Re-run with alpha matting; if still poor, route to human retouch queue |
| Etsy listing rejected (IP or trademark) | Trademark pre-check on title and tag set; queue for human review before publish |
| Mockup generation 5xx | Retry with exponential backoff; if persistent, generate local mockup with Pillow |

## First Milestone

**Day 30:** 50 designs published across Etsy/Redbubble, at least 1 sale recorded, average CTR > 2% on listings, and zero trademark rejections.
