# 03-dropshipping-trend-scraping-agent

## Metrics

| Metric | Value |
|--------|-------|
| Risk | Medium–High (platform ToS, supplier reliability) |
| Capital | RM300–RM800/month (proxies, APIs, scraping infra) |
| Success Probability | 50% (margin compression, ad spend risk) |
| Time to First RM | 30–90 days (winning product + first sale) |
| Skills Needed | Playwright, e-commerce ops, Meta Ads, supply-chain basics |

## Stack

| Layer | Choice | Why |
|-------|--------|-----|
| Scraping | Playwright + Bright Data residential proxies | Stealth, Malaysia-targeted geo-rotation |
| HTTP | httpx | Fast async for API endpoints (TikTok, Meta) |
| Parsing | BeautifulSoup4 + pandas | Lightweight, batch scoring |
| Ad Intelligence | Meta Ad Library API + TikTok Creative Center | Organic vs paid trend separation |
| Supplier | Alibaba / 1688 search API | FOB pricing, MOQ, lead-time enrichment |
| Scheduling | Celery + Redis | 6h scan cron, daily digest |
| Storage | Supabase | Product ledger, trend history, scan logs |
| Notifications | Resend | Daily operator digest with top 10 candidates |

## Execution Plan

| Week | Steps |
|------|-------|
| 1 | Define verticals (pet, home, beauty). Set up Bright Data proxy, Playwright profiles for Shopee/Lazada/TikTok. Configure Supabase tables. |
| 2 | Run first manual scan across 3 platforms. Calibrate trend_score weights. Validate margin calculation formula with operator. |
| 3 | Automate 6h Celery scan cron. Set daily 09:00 MYT Resend digest. Enable 2-platform cross-validation filter. |
| 4 | Integrate Alibaba/1688 supplier enrichment. Build link re-validation cron. Test fallback chains (Pexels→Pixabay→SDXL for creative). |
| 5–8 | Run scans; track candidates through to sale or dead-end. Refine margin model with real payment-gateway and return-rate data. |
| 9–12 | Introduce automated ad-creative download from Meta/TikTok. Begin A/B testing landing-page variants for top-scoring products. |

## Unit Economics

| Cost Item | RM/month | Revenue Item | RM/month |
|-----------|----------|--------------|----------|
| Bright Data residential proxies | 300–600 | Dropshipping margin (first product) | 500–3,000 |
| Meta/TikTok API access | 0–100 | Subsequent products (scaled) | 1,000–10,000 |
| VPS (Playwright + Celery) | 100–200 | | |
| Supabase / storage | 50–100 | | |
| **Total** | **450–1,000** | **Total** | **1,500–13,000** |

## Known Failure Modes

| Failure | Mitigation |
|---------|-----------|
| Playwright stealth detected, IP blocked | Rotate residential proxy pool; reduce concurrency; back off |
| Supplier link 404 or out of stock | Re-validate links daily; mark candidate as "supplier-dead" and surface replacement |
| Trend signal false positive (spike from ad spend not organic) | Cross-validate with at least 2 platforms before recommending |
| Ad library API rate limit | Cache responses for 24h; distribute scans across the day |

## First Milestone

**Day 30:** 72 scans completed, 50+ product candidates surfaced, at least 1 product with margin >40% and 3-platform signal validation, first daily digest sent to operator.
