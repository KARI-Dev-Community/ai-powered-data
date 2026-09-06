# 36. Data-Moat History Accumulation

Part of **AI-Powered Data & Lead Platform**. Turn local market data into warm leads.

Accumulates proprietary scraped history into datasets and APIs that grow more valuable over time. This is the compounding layer for every other product.

## Metrics

| Attribute | Value |
|---|---|
| Risk | Low-Medium |
| Capital | RM400–RM1,200/mo |
| Success Probability | Medium |
| Time to First RM | 3–6 months |
| Skills Needed | Data pipelines, DB design, web scraping, API product design |

## Why this first

Every other idea in this repo either generates data or consumes data. #36 owns the history layer. A 90-day price history is a commodity; a 3-year price history with velocity and anomaly signals is a moat.

## Stack

| Layer | Choice | Why |
|---|---|---|
| Scraping | Playwright + httpx | JS-heavy sites need browser; JSON APIs need raw HTTP |
| Storage | Supabase Postgres | Time-series queries, row-level security, easy backups |
| API | FastAPI (Python) | Async, OpenAPI auto-doc, deploy anywhere |
| Scheduling | GitHub Actions cron + Celery beat | Free daily runs; Celery for intraday |
| Compute | Hetzner CX22 (RM20/mo) | Always-on scraper + API host |

## Execution Plan

### Week 1 — Source registry + first scraper
- Pick 1 vertical (e.g., used laptops on Shopee/Lazada, short-term rentals on Airbnb, B2B SaaS pricing pages)
- Define schema: `source_id`, `entity_id`, `timestamp`, `raw_json`, `derived_metrics`
- Build 1 scraper, run it daily, validate schema consistency

### Week 2–3 — API skeleton
- Deploy FastAPI with `/v1/timeseries`, `/v1/snapshot`, `/v1/sources/health`
- Add API-key auth, rate limiting, usage logging
- Write OpenAPI spec and a 1-page getting-started guide

### Week 4 — First customer
- Cold outreach to 20 data-hungry teams (e-commerce ops, VC research, competitor intel)
- Offer: free 30-day trial of 1 dataset, then RM200–800/mo per dataset
- Close 1 paying customer = validation

### Month 2+ — Compound
- Add 2–3 more sources per month
- Build derivative signals (price-drop velocity, review velocity, category churn)
- Package monthly dataset exports for non-API buyers

## Unit Economics

| Item | Cost | Price |
|---|---|---|
| Scrape 1M records/mo | RM60–120 (VPS + proxies) | — |
| API compute + bandwidth | RM20–40 | — |
| **COGS per dataset** | **RM80–160/mo** | **RM400–2,000/mo** |
| Margin | 75–95% | — |

## Known Failure Modes

| Failure | Mitigation |
|---|---|
| Source layout change breaks scraper | Source-health probe; alert before data gap; versioned scrapers |
| Storage cost grows unbounded | Partition by month; archive cold partitions to R2/S3 |
| Competitor re-scrapes same data | Speed = moat; accumulate history they can't buy |
| Customer asks for source not in catalog | Build custom source for 2× price; don't give away pipeline |

## First Milestone

**Day 14:** 1 source live, 14 days of clean history, API returning time-series queries with < 200ms p95 latency, 1 free trial user onboarded.
