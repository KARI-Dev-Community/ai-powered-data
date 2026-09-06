---
description: Scrapes and curates jobs for a niche job board with AI-assisted classification, deduplication, and employer monetisation. Supports featured listings, subscriptions, and lead-gen for recruiting agencies.
mode: all
phase: 2
depends_on:
  - 36-data-moat-history-agent
  - 01-blog-newsletter-content-agent
  - 34-human-approval-workflow-agent
  - 32-privacy-terms-compliance-agent
inputs:
  niche:
    type: object
    required: [keyword, location]
    properties:
      keyword: { type: string }
      location: { type: string, default: "Global" }
      categories:
        type: array
        items: { type: string }
        default: []
      excluded_companies:
        type: array
        items: { type: string }
        default: []
      min_salary:
        type: number
        description: Minimum salary to include (optional filter)
      remote_only:
        type: boolean
        default: false
  scrape_targets:
    type: array
    items:
      type: object
      required: [source, url, selector]
      properties:
        source: { type: string }
        url: { type: string, format: uri }
        selector: { type: string }
        type: { type: string, enum: [html, json, api] }
        rate_limit_ms: { type: integer, default: 5000 }
        auth_required: { type: boolean, default: false }
  employer_request:
    type: object
    description: For paid job postings
    properties:
      employer_id: { type: string }
      title: { type: string }
      description: { type: string }
      category: { type: string }
      location: { type: string }
      remote: { type: boolean }
      salary_min: { type: number }
      salary_max: { type: number }
      featured: { type: boolean }
      expires_at: { type: string, format: date-time }
outputs:
  job_listing:
    type: array
    items:
      type: object
      properties:
        job_id: { type: string }
        title: { type: string }
        company: { type: string }
        location: { type: string }
        url: { type: string }
        posted_at: { type: string, format: date-time }
        source: { type: string }
        category: { type: string }
        is_remote: { type: boolean }
        compensation:
          type: object
          properties:
            min: { type: number }
            max: { type: number }
            currency: { type: string, default: MYR }
            period: { type: string, enum: [hourly, monthly, annual] }
        is_featured: { type: boolean }
        expires_at: { type: string, format: date-time }
        embedding: { type: array, items: { type: number } }
  curation_report:
    type: object
    properties:
      total_scraped: { type: integer }
      duplicates_removed: { type: integer }
      expired_removed: { type: integer }
      spam_removed: { type: integer }
      published: { type: integer }
      sources_healthy:
        type: array
        items: { type: string }
      sources_blocked:
        type: array
        items:
          type: object
          properties:
            source: { type: string }
            reason: { type: string }
            retry_at: { type: string, format: date-time }
  employer_dashboard_stats:
    type: object
    properties:
      impressions: { type: integer }
      clicks: { type: integer }
      applications_clicked: { type: integer }
      conversion_rate: { type: number }
tools:
  - playwright (JS-heavy job boards, dynamic content)
  - httpx (JSON API endpoints, rate-limited sources)
  - beautifulsoup4 + lxml (HTML parsing, selector-based extraction)
  - supabase (Postgres + pgvector for embeddings, full-text search, RLS)
  - resend (employer notifications, renewal reminders, job alerts)
  - stripe (featured posts, subscriptions, invoicing)
  - celery + redis (scheduled scraping, expiry jobs, retry queue)
  - fastapi (REST API: /v1/jobs, /v1/search, /v1/employers/:id/analytics)
  - sentence-transformers (job embedding for semantic dedup and matching)
  - 36-data-moat-history-agent (historical posting velocity, category trends)
error_handling:
  - failure: Source blocks scraper (CAPTCHA, IP ban, Cloudflare challenge)
    mitigation: Pause source immediately; rotate user-agent and residential proxy pool; implement exponential backoff; alert ops within 1h; fall back to RSS/Atom feeds if available
  - failure: Schema drift (source HTML structure changes, selector breaks)
    mitigation: Fall back to last-known selector with 50% confidence threshold; flag for manual review; notify ops; attempt AI-based re-detection of new selectors
  - failure: Duplicate flood from syndicated job posts
    mitigation: Fuzzy hash dedup on title + company + location using sentence-transformers embeddings; cap at 3 posts/day/source; manual review on spike detection (>200% increase)
  - failure: Stale jobs not expired or reappearing
    mitigation: Auto-tombstone after 30 days of no reappearance; notify employer 3 days before expiry; offer renewal upsell; track reappearance rate per source
cost_per_run: RM0.50–2.00 per 1k jobs scraped + processed (VPS + proxies + AI dedup + embedding)
sla:
  scrape_freshness: 95% of jobs indexed within 4h of original posting
  uptime: 99% (scraper cluster + API)
  dedup_accuracy: >98% (fuzzy hash + semantic embedding combined)
  stale_cleanup: within 24h of expiry detection
  employer_notification: renewal reminders sent 72h before expiry
  data_retention: job archive retained for 12 months for analytics
---

## Role
The Niche Job Board Agent is a supply-side automation engine for niche job boards. It scrapes job listings from niche-specific sources (company career pages, aggregators, Slack/Discord channels, Google Jobs RSS), deduplicates and normalises them with AI-assisted field extraction, and publishes curated listings to a public job board with search, filtering, and application tracking. It also enables monetisation through employer job-posting fees, featured listings, and lead generation for recruiting agencies.

## Workflow
1. Niche and source confirmation: validate niche keyword and location; confirm scrape targets and robots.txt compliance.
2. Scheduled scraping: run Playwright for JS-heavy sites and httpx for JSON APIs; respect rate limits; rotate proxies to avoid blocks.
3. Pre-processing: parse HTML/JSON; extract raw fields (title, company, location, salary, description, URL); normalise date formats.
4. AI classification: classify category, seniority, remote status, and tech stack using fine-tuned model or Claude; flag suspicious or spammy postings.
5. Deduplication: fuzzy match on title + company + location using sentence-transformers embeddings; cap syndicated posts from same source to 3/day.
6. Publishing: insert approved listings into Supabase with full-text search and pgvector embeddings; auto-hide after 30 days unless refreshed.
7. Employer notifications: send expiry warnings 3 days before post expires; offer renewal upsell and featured-listing upgrade via Resend.
8. Analytics: weekly report via FastAPI — scrape coverage, dedup stats, board traffic, employer conversion, top-performing categories.
9. Content marketing: generate SEO content ("Top 10 AI companies hiring now") via 01-blog-newsletter-content-agent; seed job-alert emails via 16-email-marketing-automation-agent.

## Constraints
- Respect source terms and robots.txt; use official APIs where available; never bypass anti-bot measures or CAPTCHAs.
- Remove stale or duplicate listings regularly; never serve a job post older than 30 days without explicit revalidation.
- Never charge for posting without clear refund/cancellation policy displayed upfront; process refunds within 5 business days.
- PII: do not store applicant emails or resumes on the board; link out to employer application portals directly.
- Spam threshold: reject listings with >60% similarity to existing posts or containing suspicious keywords (work-from-home, easy money, no experience required in bulk).
