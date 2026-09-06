# 11. Public Data Aggregation → API Product

Builds data pipelines and APIs that aggregate public data into a paid, rate-limited REST product. This is the fastest path to recurring revenue from the #36 data-moat foundation.

## Metrics

| Attribute | Value |
|---|---|
| Risk | Medium |
| Capital | RM400–RM2,000 |
| Success Probability | Medium |
| Time to First RM | 3–6 months |
| Skills Needed | Backend/API dev, data pipelines, DB design |

## Stack

| Layer | Choice | Why |
|---|---|---|
| Ingestion | Playwright + httpx | Mixed JS-heavy and JSON API sources |
| Storage | Supabase Postgres | Time-series + relational; free tier to start |
| API | FastAPI | Async, OpenAPI, easy auth middleware |
| Billing | Lemon Squeezy | MoR handles tax; webhooks for usage events |
| Docs | Mintlify or FastAPI built-in | Auto-generated from OpenAPI |

## Execution Plan

### Week 1–2 — Pick a dataset, validate demand
- Choose 1 dataset with clear buyers: e.g., "short-term rental nightly rates by city," "job posting volume by role," "e-commerce product catalog with images"
- Scrape 1 source manually; confirm data is stable and legally redistributable
- Post landing page on Cloudflare Pages; drive 50 targeted signups from Reddit/Discord/IndieHackers

### Week 3–4 — Build ingestion + API
- ETL pipeline: scrape → validate schema → dedupe → upsert into Postgres
- API endpoints: list entities, get by ID, timeseries, search
- Auth: API key per customer; rate limits by tier
- Billing: free tier (100 req/day), pro (RM99/mo, 10k req/day), enterprise (custom)

### Month 2 — First paying customer
- Target 5 free users; ask for feedback
- Convert 1 to pro at RM99/mo = first revenue
- Add 1 more source to increase stickiness

### Month 3+ — Scale
- Add 2–3 datasets per month
- Offer dataset exports (CSV/Parquet) for one-time buyers (RM200–500/dataset)
- Build SDKs (Python/Node) to reduce integration friction

## Unit Economics

| Item | Cost | Price |
|---|---|---|
| VPS + proxies | RM20–40/mo per dataset | — |
| Supabase | RM0–80/mo (scales) | — |
| Lemon Squeezy + payment fees | ~5% | — |
| **COGS per API call** | **RM0.002–0.01** | **RM0.01–0.05 (blended)** |
| Margin | 60–90% | — |

## Known Failure Modes

| Failure | Mitigation |
|---|---|
| Source dies or changes layout | Source-health monitor; serve last-known-good with staleness header |
| Data licensing issue | Verify ToS before ingest; keep source attribution in API meta |
| API abuse / scraping your API | Rate limits, CAPTCHA at signup, IP block on abuse |
| Cold start (no users) | Ship public dataset + landing page before API; SEO content around the dataset |

## First Milestone

**Day 21:** 1 dataset live, 30 days of clean history, API docs published, 5 free trial signups, 1 pro conversion.
