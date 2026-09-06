# 23. Recipe/niche content site with ad revenue

## Metrics

| Risk | Capital | Success Probability | Time to First RM | Skills Needed |
| --- | --- | --- | --- | --- |
| Low | RM200–RM800 | Low-Medium | 6–12 months | SEO, content writing, ad network setup (AdSense/Mediavine), image generation prompt engineering |

## Stack

| Layer | Choice | Why |
| --- | --- | --- |
| Site engine | Next.js 14 (static export) | Fast TTFB, ISR for recipe updates, easy programmatic pages |
| Content | Anthropic Claude Sonnet 3.5 | Long-form structured output, FAQ generation, schema compliance |
| Images | SDXL / DALL-E 3 | Original, brand-consistent food photography |
| Schema | json-ld typed v3 | Strict Schema.org Recipe validation, Rich Results eligibility |
| SEO | Ahrefs API v3 + GSC API | Keyword gap analysis, indexing monitoring, CTR alerts |
| Ads | AdSense → Ezoic → Mediavine (progressive ramp) | Higher RPM as traffic scales; Ezoic at 25k pv/mo, Mediavine at 50k |
| Hosting | Vercel + Cloudflare | Global CDN, edge caching, cheap static hosting |
| Optimisation | Sharp | Image compression, WebP conversion, responsive srcset |
| Validation | Zod | Runtime schema validation for recipe inputs/outputs |

## Execution Plan

| Week | Step | Deliverable |
| --- | --- | --- |
| 1 | Niche validation via 36-data-moat-history-agent; register domain; deploy Next.js skeleton with recipe template | Domain + skeleton site |
| 2 | Write 20 seed recipes manually (operator-tested); validate Schema.org JSON-LD; submit sitemap | 20 published recipes |
| 3 | Build automated recipe pipeline: write-up → image gen → schema → publish | 1-click batch publisher |
| 4 | Apply for AdSense; configure placeholder ad units; set up GSC alerts | AdSense live |
| 5 | Scale to 50 recipes; implement weekly content cadence (2–3 recipes/week); add internal linking | 50 recipes, IndexNow enabled |
| 6–10 | Hit 100 recipes; implement FAQ auto-generation; prune underperformers; monitor Core Web Vitals | 100 recipes, <2s LCP |
| 11–16 | Hit 200 recipes; apply to Ezoic at 25k pv/mo; add quarterly refresh workflow | Ezoic approved |
| 17–24 | Hit 50k pageviews/mo; apply to Mediavine; A/B test ad placements | Mediavine approved |

## Unit Economics

| Item | Cost (RM) | Revenue (RM) |
| --- | --- | --- |
| Vercel Pro + Cloudflare | 120/mo | – |
| Ahrefs Lite | 200/mo | – |
| Claude Sonnet per recipe | 0.30 | – |
| Image generation per recipe | 0.20 | – |
| Image storage (Cloudflare R2) | 5/mo | – |
| AdSense RPM | – | 5–15 per 1k pageviews |
| Ezoic RPM (when eligible) | – | 15–30 |
| Mediavine RPM (when eligible) | – | 30–60 |
| Break-even | ~month 6 at 100k pageviews/mo | – |
| Month 12 target | – | RM3,000–6,000/mo |

## Known Failure Modes

| Failure | Mitigation |
| --- | --- |
| Thin content flag from Google | 800+ word minimum, original photo, FAQ block, GSC Coverage monitoring |
| Ad network disapproval | Start with AdSense; reapply at traffic thresholds with site history |
| AI food image quality issues | Style brief with reference images; CLIP quality gate; Unsplash fallback |
| Google Helpful Content update impact | Original commentary, transparent authorship, operator testing provenance |
| Schema validation failure | Auto-validate with json-ld typed before publish; block deploy if invalid |
| Seasonal recipe traffic drops | Diversify niche coverage; evergreen recipe archive; quarterly refresh |

## First Milestone

**Day 90:** 50 published recipes, 10k pageviews/mo, first RM100 ad revenue (AdSense live), 95% indexing rate, Core Web Vitals all green.
