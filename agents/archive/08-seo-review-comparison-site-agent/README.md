# 08-seo-review-comparison-site-agent

## Metrics

| Metric | Value |
|--------|-------|
| Risk | Medium (Google algo changes, niche saturation) |
| Capital | RM600–RM1,500/month (scraping, LLM, hosting, SEO tools) |
| Success Probability | 55% (niche selection + authority building) |
| Time to First RM | 90–180 days (first affiliate sale + ad revenue) |
| Skills Needed | SEO, Next.js/WordPress, Playwright, Schema.org, affiliate marketing |

## Stack

| Layer | Choice | Why |
|-------|--------|-----|
| CMS | Next.js (primary) / WordPress (legacy) | Static generation for speed, ISR for freshness |
| LLM | Anthropic Claude Sonnet 4 | Long-form coherence, original analysis generation |
| Scraping | Playwright + residential proxies | Retailer spec/price extraction, stealth |
| SEO Data | Ahrefs / SEMrush API | Keyword difficulty, SERP tracking, site audits |
| Structured Data | json-ld generator (custom) | Product, Review, FAQ, HowTo schemas |
| Hosting | Vercel + Cloudflare R2/S3 | Edge CDN, ISR, cheap asset storage |
| Billing / Lead Capture | Resend | Newsletter opt-in, automation |
| Storage | Supabase | Price history, click ledger, scan logs |

## Execution Plan

| Week | Steps |
|------|-------|
| 1 | Niche selection via 36-data-moat (KD<25, vol>2k, low brand-density). Register domain, set up Next.js on Vercel, configure Supabase. |
| 2 | Build Playwright scraper for 3+ retailers. Calibrate price/spec extraction selectors. Test Schema.org JSON-LD output with Google Rich Results Test. |
| 3 | Generate first site skeleton: 1 pillar listicle, 2 reviews, 2 comparisons, 1 buyer guide. Human QA on pillar; auto-publish supporting with QA gate. |
| 4 | Submit sitemap to Google Search Console. Wire newsletter opt-in via Resend. Begin internal linking program (3 links per 1k words). |
| 5–8 | Add 2 more products per week. Weekly price/spec refresh via Celery. Monitor rankings via Ahrefs; A/B test titles for CTR. |
| 9–12 | Hit 50-page milestone. Quarterly content audit: remove under-performers, add new SKUs. Begin Pinterest + Reddit traffic diversification. |

## Unit Economics

| Cost Item | RM/month | Revenue Item | RM/month |
|-----------|----------|--------------|----------|
| LLM API (Claude Sonnet 4) | 200–400 | Affiliate commissions | 800–4,000 |
| Playwright + proxies | 150–300 | Display ads (Ezoic/Mediavine) | 300–1,500 |
| Vercel + R2/S3 | 100–200 | Direct brand deals | 0–1,000 |
| Ahrefs / SEMrush | 200–400 | Newsletter sponsorships | 200–800 |
| Resend + domain | 40–80 | | |
| **Total** | **690–1,380** | **Total** | **1,300–7,300** |

## Known Failure Modes

| Failure | Mitigation |
|---------|-----------|
| Retailer scraper blocked | Rotate residential proxy; fall back to Google Shopping API |
| Affiliate link dead | Daily link-checker; auto-redirect to closest match |
| Google Helpful Content update | Add original test/measurement data, expert quotes, transparent methodology |
| Site deindexed | Diversify traffic (newsletter, Pinterest, Reddit); re-submit sitemap |

## First Milestone

**Day 30:** 15 pages published, sitemap submitted, first affiliate click recorded, at least 1 page in top 50 for its target keyword, and zero Google Search Console errors.
