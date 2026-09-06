# 27. Price-Tracking / Deal-Alert Bot

Tracks product prices and sends deal alerts. Built on top of #36's history layer; uses derivative signals (velocity, moving averages) instead of naive "price < target" checks.

## Metrics

| Attribute | Value |
|---|---|
| Risk | Low |
| Capital | RM200–RM600 |
| Success Probability | Medium |
| Time to First RM | 2–3 months |
| Skills Needed | Web scraping, notification systems (email/SMS APIs) |

## Stack

| Layer | Choice | Why |
|---|---|---|
| Scraping | Playwright + httpx | Retailer sites vary; some need browser |
| Database | Supabase Postgres (shared with #36) | Price history lives in data-moat archive |
| API | FastAPI | `/v1/alerts`, `/v1/watchlist`, `/v1/history/:sku` |
| Notify | Resend (email) + Twilio (SMS optional) | Low cost, good deliverability |
| Frontend | Astro + Cloudflare Pages | Static watchlist management page |

## Execution Plan

### Week 1 — MVP scraper + watchlist
- Pick 1 category (electronics, fashion, or home goods)
- Scrape 50 SKUs manually to build initial history
- Build `/v1/watchlist` POST endpoint; user adds SKU + target price
- Send email alert when price drops below target AND 30-day low

### Week 2 — Deal scoring
- Replace naive threshold with score: `(30d_low - current) / 30d_low * velocity_factor`
- Velocity factor: price dropping fast = higher score even if not at all-time low
- Add category-wide comparison (is this SKU cheaper than 80% of similar items?)

### Week 3 — User-facing product
- Astro page: search/add products, set target price, view price chart
- Email template: clean, 1-click "view deal" link, unsubscribe
- 10 beta users from Reddit/niche forums

### Week 4–6 — Monetize
- Free: 5 watchlists, email alerts only
- Pro (RM9.90/mo): 50 watchlists, SMS alerts, price-history CSV export
- Launch on ProductHunt; target deal-seeking communities

## Unit Economics

| Item | Cost | Revenue |
|---|---|---|
| Hosting + proxies | RM20–40/mo | — |
| AI (deal copy generation) | RM5–15/mo | — |
| **COGS per user** | **RM1–3/mo** | **RM9.90/mo** |
| Margin | 70–90% | — |
| Break-even | 5–10 pro users | — |

## Known Failure Modes

| Failure | Mitigation |
|---|---|
| Retailer blocks scraper | Rotate proxies, fall back to official affiliate feeds where available |
| False positive alert (price then back up) | Add 15-min price-stability check before sending |
| User adds non-purchasable SKU | Validate availability at add-time; mark unavailable in UI |
| SMS costs spike | Start email-only; SMS as paid add-on (RM1/alert or included in pro) |

## First Milestone

**Day 10:** 50 SKUs tracked, 7 days of history, 5 beta users receiving alerts, 1 alert conversion (user clicked through and bought).
