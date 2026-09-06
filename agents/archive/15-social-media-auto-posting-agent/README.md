# 15. Social media auto-posting & growth agent

## Metrics

| Risk | Capital | Success Probability | Time to First RM | Skills Needed |
| --- | --- | --- | --- | --- |
| Low | RM200–RM800/mo | Medium | 2–4 months | API integration (social platforms), content calendar planning |

## Stack

| Layer | Choice | Why |
| --- | --- | --- |
| Platforms | Meta Graph API + TikTok Business + X API v2 + LinkedIn | Official, reliable, future-proof |
| Creative | SDXL + Runway + ElevenLabs | Image, video, voice in one stack |
| Copy | Anthropic Claude Sonnet 4 | Platform-native tone, character limits |
| Scheduling | Celery + Redis | Cron, retries, idempotency |
| Analytics | Supabase + per-platform export | One source of truth |
| Listening | Apify (optional) | Trend surfacing |

## Execution Plan

| Week | Step |
| --- | --- |
| 1 | Pick brand + 3 platforms, set up API apps, design pillar set |
| 2 | Manually create first 30 posts as seed content and voice reference |
| 3 | Build the agent: calendar → creative → copy → schedule |
| 4 | Wire analytics harvest; engagement-aware re-weighting |
| 5 | Onboard 2 client brands (paid pilot) |
| 6-10 | Scale to 5 brands, monthly performance reviews |
| 11-12 | Add 36-data-moat-history-agent for trend-driven topic selection |

## Unit Economics

| Item | Cost (RM) | Revenue (RM) |
| --- | --- | --- |
| API costs (X + Meta) | 50/mo | – |
| Creative per post | 0.20 | – |
| Compute (Celery) | 20/mo | – |
| Per-brand management fee | – | 500–2,000/mo |
| Performance bonus (option) | – | 5–10% of attributed revenue |
| Break-even | 2 paying brands | – |

## Known Failure Modes

| Failure | Mitigation |
| --- | --- |
| Platform rate limit | Per-platform backoff, queue overflow |
| Shadowban signal | Throttle post frequency, switch pillar mix |
| Asset copyright issue | Trademark pre-check, regenerate with sanitised prompt |
| Engagement drops | Weekly pillar re-weight, kill underperformers |

## First Milestone
Day 30: 1 brand live, 30 posts published, 1,000 followers gained, first 2 paying brand clients.