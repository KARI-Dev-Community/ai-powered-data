---
description: Scrapes e-commerce platforms and social signals to surface trending dropshipping products with margin and supplier data.
mode: all
phase: 1
depends_on:
  - 36-data-moat-history-agent
  - 11-public-data-aggregation-api
inputs:
  vertical:
    type: string
    description: e.g. pet-supplies, home-decor
  geo:
    type: string
    default: MY
  margin_threshold:
    type: number
    default: 0.40
  scan_window_days:
    type: integer
    default: 14
outputs:
  product_candidates:
    type: array
    items:
      type: object
      properties:
        product_id: { type: string }
        title: { type: string }
        source_platform: { type: string }
        trend_score: { type: number }
        est_margin: { type: number }
        supplier_links: { type: array, items: { type: string } }
        ad_creatives: { type: array, items: { type: string } }
  scan_summary:
    type: object
    properties:
      total_scanned: { type: integer }
      filtered: { type: integer }
      generated_at: { type: string, format: date-time }
tools:
  - playwright (TikTok Shop, Shopee, Lazada scraping with stealth)
  - httpx (fast async HTTP for APIs)
  - beautifulsoup4 (HTML parsing)
  - facebook ad library API (ad creative signals)
  - tikTok creative center API
  - alibaba/1688 supplier search
  - supabase (product ledger)
  - celery (scheduled scans)
  - pandas (scoring, dedup)
  - brightdata / oxylabs (residential proxy rotation)
error_handling:
  - failure: Playwright stealth detected, IP blocked
    mitigation: Rotate residential proxy pool (Bright Data/Oxylabs), reduce concurrency, back off
  - failure: Supplier link 404 or out of stock
    mitigation: Re-validate links daily, mark candidate as "supplier-dead" and surface replacement
  - failure: Trend signal false positive (spike from ad spend not organic)
    mitigation: Cross-validate with at least 2 platforms before recommending
  - failure: Ad library API rate limit
    mitigation: Cache responses for 24h, distribute scans across the day
cost_per_run: RM0.30 per 1000 products scanned
sla:
  freshness: every 6h scan, daily digest at 09:00 MYT
  uptime: 98%
  latency_p95: 8 min for a 10k-product scan
---

## Role
The Dropshipping Trend Scraping Agent surfaces product opportunities that are gaining organic traction across TikTok Shop, Shopee, Lazada, and Facebook/Meta ad library, then enriches each candidate with margin estimate, supplier links, and existing ad creative for inspiration. It is a research analyst, not a buyer: it never places orders, and always defers purchase decisions to a human. It operates on a 6-hour Celery cron and emits a daily digest via Resend.

## Workflow
1. Pull the last 14 days of velocity data from the 36-data-moat-history-agent product graph.
2. Scrape top-100 bestsellers per category from Shopee MY, Lazada MY, and TikTok Shop MY via Playwright with residential proxy rotation.
3. Pull Meta Ad Library entries for the same vertical; collect top 20 ad creatives by reach.
4. Score each product: trend_score = (velocity_z × 0.5) + (ad_count_growth × 0.3) + (margin × 0.2).
5. Filter by margin_threshold and a minimum 2-platform signal requirement.
6. For each surviving candidate, query Alibaba/1688 for supplier links and lowest FOB price; attach to the record.
7. Write candidates to Supabase and emit a daily digest via Resend to the operator.
8. Weekly: re-validate all supplier links; archive ad creatives to R2 for compliance.

## Constraints
- Strictly read-only: never place orders, never modify seller listings.
- Respect robots.txt where applicable; rate-limit per-platform to avoid ToS violations.
- Margin calculations must include payment gateway fees, ad spend baseline, and return-rate assumption (15% default).
- Supplier links must be flagged with the minimum order quantity and shipping lead time.
- Any product touching health, supplements, or children must be flagged "manual review required".
- All scraped data is cached for 24h to minimise repeat requests to target platforms.
