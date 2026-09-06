# Stock Photo / Art Generation Agent

## Metrics

| Metric | Value |
|--------|-------|
| Risk | Low |
| Capital | RM 100–RM 500/mo (API credits + storage) |
| Success Probability | 60–80% (volume game) |
| Time to First RM | 2–8 weeks (marketplace review cycle) |
| Skills Needed | Prompt engineering, metadata SEO, basic image editing |

## Stack

| Layer | Choice | Why |
|-------|--------|-----|
| Generation | SDXL (primary) / DALL-E 3 | SDXL free + controllable; DALL-E 3 for tricky compositions |
| Upscaling | Real-ESRGAN | Open-source 4x upscaler; meets Adobe 4MP minimum |
| Metadata | ExifTool | IPTC/XMP title, description, keywords; industry standard |
| Metadata Prompting | Anthropic Claude | Generate 25–50 specific keywords from buyer-search data |
| Marketplaces | Adobe Stock, Shutterstock, Freepik APIs | Top 3 by contributor earnings; round-robin submit |
| Data Ledger | Supabase | Asset catalog, royalty tracking, rejection reason log |
| Topic Intelligence | 36-data-moat-history-agent | Identify rising categories with low contributor density |

## Execution Plan

| Week | Task |
|------|------|
| 1 | Pull rising microstock categories from 36-data-moat-history-agent. Select 3 test categories. |
| 2 | Build SDXL prompt library per category. Test 10 images; validate ≥4MP, no artifacts. |
| 3 | Integrate Real-ESRGAN upscaler. Batch-test 50 images; measure rejection rate. |
| 4 | Build Claude keyword prompt using buyer-search terms. Test metadata quality. |
| 5 | Embed IPTC metadata via ExifTool. Submit batch of 50 to Adobe Stock via API. |
| 6 | Review rejection reasons. Adjust prompt library + keyword strategy. |
| 7–8 | Add Shutterstock + Freepik submission. Round-robin across 3 marketplaces. |
| 9–12 | Scale to 200 assets/week. Target 60% live rate. Track royalties in Supabase. |

## Unit Economics

| Item | Cost | Revenue |
|------|------|---------|
| SDXL generation (local GPU) | RM 0 (electricity) | — |
| DALL-E 3 fallback | RM 0.04/image | — |
| Real-ESRGAN upscale | RM 0 (local) | — |
| Adobe Stock royalty | — | 33% of sale (standard license) |
| Shutterstock royalty | — | 15–40% of sale (level-dependent) |
| Freepik royalty | — | RM 0.10–RM 0.50/download |
| Storage (Supabase + S3) | RM 5–RM 20/mo | — |

**Break-even:** 100 live assets × 1 download/mo × RM 0.10 avg = RM 10/mo covers storage.

## Known Failure Modes

| Failure | Mitigation |
|---------|-----------|
| Marketplace rejects for IP/likeness | Pre-check title/description against trademark + face-likeness list; regenerate |
| Image below 4MP (Adobe minimum) | Auto-upscale via Real-ESRGAN before submit; validate resolution in code |
| Keywords too generic | Pull buyer-search terms from 36-data-moat-history-agent; require ≥25 specific keywords |
| API quota exhausted (marketplace) | Round-robin across 3 marketplaces per week; surface to operator if all down |
| Model-signature artifacts (SDXL watermark) | Add artifact-detection gate; reject and regenerate before submit |
| Category saturation | Monitor 36-data-moat-history-agent contributor-density metric; rotate categories |

## First Milestone

**Day 14:** First 50-image batch submitted to Adobe Stock with metadata embedded. Target: by Day 30, ≥30 assets live and ≥5 downloads recorded.
