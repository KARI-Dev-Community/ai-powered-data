# 26. Niche Job Board

Scrapes and curates jobs for a niche job board with AI-assisted classification, deduplication, and employer monetisation.

## Metrics

| Risk | Capital | Success Probability | Time to First RM | Skills Needed |
| --- | --- | --- | --- | --- |
| Medium | RM600–RM1,500 | Medium | 2–4 months | Web scraping, backend dev, DB design, SEO/content ops, employer sales |

## Stack

| Layer | Choice | Why |
| --- | --- | --- |
| Scraping | Playwright + httpx | JS-heavy job boards need browser; JSON APIs need raw HTTP |
| Parsing | BeautifulSoup4 + lxml | Fast HTML parsing, CSS selector-based extraction |
| Dedup / NLP | sentence-transformers + fuzzy hashing | Semantic dedup on title + company + location; AI classify category/remote/seniority |
| Database | Supabase Postgres + pgvector | JSONB for flexible fields, full-text search, vector similarity, RLS for employer isolation |
| API | FastAPI | /v1/jobs, /v1/search, /v1/employers/:id/analytics |
| Frontend | Astro + Cloudflare Pages | Static job board, fast SEO, cheap hosting |
| Payments | Stripe Checkout | Job post fees, subscriptions, refund policy enforcement |
| Scheduling | Celery + Redis | Scrape every 2–6h per source; expire posts after 30 days |
| Email | Resend | Employer notifications, renewal reminders, job alerts |
| Monitoring | Sentry | Scraper error tracking, alerting on source blocks |
| Enrichment | 36-data-moat-history-agent | Historical job-posting velocity and category trends |

## Execution Plan

| Week | Step | Deliverable |
| --- | --- | --- |
| 1 | Pick niche (e.g., "AI/ML remote roles" or "SaaS backend engineers, MY"); identify 3–5 job sources; build scrapers for each | Scraper pipeline |
| 2 | Implement fuzzy dedup + semantic embedding; build FastAPI endpoints; deploy basic Astro frontend with search + filter | Live board |
| 3 | Add employer dashboard: post a job (paid), view analytics; Stripe checkout for featured posts (RM400) and subscriptions (RM1,500/mo for 10 posts) | Monetisation live |
| 4 | Send renewal emails 7 days before post expires via Resend; set up Stripe webhooks | Automated billing |
| 5 | Launch SEO content ("Top 10 AI companies hiring now") via 01-blog-newsletter-content-agent; seed Reddit/Discord outreach | Traffic growth |
| 6–8 | Add job-alerts email via 16-email-marketing-automation-agent; A/B test featured listing placement | 500 subscribers |
| 9–12 | Hit 500 jobs on board; add salary insights; launch white-label for recruiters via 32-compliance audit | RM4,000 MRR |
| 13–24 | Expand to 2–3 niche boards; add employer analytics dashboard; hit 2,000 jobs/month | Scale |

## Unit Economics

| Item | Cost | Revenue |
| --- | --- | --- |
| Scraping infra (VPS + proxies) | RM40–80/mo | — |
| AI classification per 1k jobs | RM0.50–2.00 | — |
| 10 featured posts/mo | RM2–8 | RM3,000 |
| 5 employer subs @ RM1,200 | RM2–8 | RM6,000 |
| COGS per job post | RM0.10–0.30 | RM300–800 |
| Margin | 90%+ | — |

## Known Failure Modes

| Failure | Mitigation |
| --- | --- |
| Source blocks scraper | Rotate user-agents/proxies; fallback to official API; alert ops within 1h; pause source if persistent |
| Duplicate flood from syndicated posts | Fuzzy hash + semantic embedding dedup; cap at 3/day/source; manual review on spikes |
| Jobs expire silently (no re-scrape) | 7-day expiry grace; auto-email employers 3 days before expiry; track reappearance rate |
| Board gets no traffic | Launch SEO content first (#01); seed with free posts; run Reddit/Discord community outreach; job-alert emails |
| Platform ToS risk | Run #32 compliance audit before scraping; use official APIs where available; respect rate limits |
| Spam / scam listings | AI classifier + keyword filter; reject suspicious posts; human review for flagged listings |

## First Milestone

**Day 30:** 1 niche live (AI remote jobs), 3 sources scraping, 200+ curated jobs on board, employer dashboard with Stripe checkout, 1 paying employer (RM400), site ranking for "AI jobs remote" keyword.
