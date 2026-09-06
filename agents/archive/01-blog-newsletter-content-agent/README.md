# 01-blog-newsletter-content-agent

## Metrics

| Metric | Value |
|--------|-------|
| Risk | Low–Medium |
| Capital | RM500–RM1,000/month (LLM API, hosting, tools) |
| Success Probability | 65% (niche-dependent, 3–6 months to traction) |
| Time to First RM | 60–90 days (affiliate commissions + ad revenue) |
| Skills Needed | SEO copywriting, WordPress, affiliate marketing, basic analytics |

## Stack

| Layer | Choice | Why |
|-------|--------|-----|
| LLM | Anthropic Claude Sonnet 4 + GPT-4o-mini | Draft quality + cheap headline variants |
| CMS | WordPress REST API | Lowest friction for SEO, plugins, ownership |
| Newsletter | Resend + ConvertKit/MailerLite | Deliverability, automation, list growth |
| SEO Data | Ahrefs / SEMrush API | Keyword difficulty, volume, competitor tracking |
| Scheduling | Celery + Redis | Reliable async publish pipeline |
| Analytics | Supabase + custom event logging | Own your data, feed back to 36-data-moat |
| Hosting | VPS / Cloudways | Avoid shared-hosting throttle under traffic spikes |

## Execution Plan

| Week | Steps |
|------|-------|
| 1 | Finalise niche via keyword research (KD<30, vol>500, affiliate programs available). Set up WordPress + Resend. Configure Supabase tables (articles, links, revenue). |
| 2 | Write brand-voice system prompt + 3 sample articles. Run first human QA pass. Calibrate link-quota and disclosure placement. |
| 3 | Deploy Celery beat schedule (Mon/Wed/Fri articles, Tue newsletter). Enable auto-publish for supporting articles, manual gate for hero. |
| 4 | Launch weekly newsletter to seed list (50–100). Add affiliate link checker cron. Connect Supabase revenue ledger to partner dashboards. |
| 5–8 | Publish consistently; A/B test headlines and CTAs. Re-publish any article with >30 position drift. Begin internal linking program. |
| 9–12 | Introduce micro-posts (300–500 words, daily) for long-tail coverage. Optimise top 3 articles for featured snippets. Negotiate higher affiliate rates if volume warrants. |

## Unit Economics

| Cost Item | RM/month | Revenue Item | RM/month |
|-----------|----------|--------------|----------|
| LLM API (Claude + GPT-4o-mini) | 150–300 | Affiliate commissions | 800–3,000 |
| WordPress hosting + plugins | 80–150 | Display ads (Ezoic/Mediavine) | 300–1,500 |
| Resend / email tools | 40–80 | Newsletter sponsorships | 200–800 |
| SEO tools (Ahrefs/SEMrush) | 200–400 | Direct brand deals | 0–1,000 |
| Celery / VPS overhead | 50–100 | | |
| **Total** | **520–1,030** | **Total** | **1,300–6,300** |

## Known Failure Modes

| Failure | Mitigation |
|---------|-----------|
| Anthropic API 529 overload | Exponential backoff; fallback to GPT-4o-mini; queue for human review |
| Affiliate link 404/de-activated | Daily link-checker cron replaces broken links and flags affected articles |
| WordPress 401 auth expired | Alert via monitoring; rotate app password; auto-retry next schedule |
| Resend bounce rate > 5% | Auto-suppress hard bounces, switch sender domain, notify operator |

## First Milestone

**Day 30:** 8 published articles, 4 newsletters sent, first affiliate click recorded, and at least one article ranking in top 50 for its primary keyword (tracked via Ahrefs).
