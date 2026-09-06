# 24. Fitness/meal plan generator app

## Metrics

| Risk | Capital | Success Probability | Time to First RM | Skills Needed |
| --- | --- | --- | --- | --- |
| Medium | RM1,200–RM4,000 | Low-Medium | 4–8 months | Mobile/web app dev, domain knowledge (nutrition, exercise science), subscription billing, PDF rendering |

## Stack

| Layer | Choice | Why |
| --- | --- | --- |
| Plan generation | Anthropic Claude Sonnet 3.5 | Best long-form structured output; supports JSON schema enforcement |
| PDF | WeasyPrint 60 | Branded on-demand PDFs with custom fonts, page numbers, watermarks |
| Billing | Stripe | Subscriptions, dunning, invoices, tax calculation |
| Database | Supabase (Postgres + RLS) | User data, progress tracking, audit logs, row-level security |
| Email | Resend | Transactional emails (delivery, weekly check-ins, renewal reminders) |
| Progress | Next.js 14 dashboard | Weights, adherence, photos, streak tracking |
| Validation | Zod | Runtime schema enforcement, safety gate validation |
| Auth | Clerk or Supabase Auth | OAuth, email/password, session management |

## Execution Plan

| Week | Step | Deliverable |
| --- | --- | --- |
| 1 | Build intake form, Zod validation, safety gate, Lemon Squeezy checkout | Live checkout flow |
| 2 | Build plan generator + PDF renderer for 2 plan types | PDF delivery working |
| 3 | Build progress dashboard (weights, adherence, photos) | Dashboard live |
| 4 | Wire weekly check-in email via Resend; Stripe webhook handling | Automated emails |
| 5 | Soft launch at RM49/mo, 20 paying users; gather NPS feedback | 20 users |
| 6–10 | Iterate on plan quality; add 3rd plan type (performance); raise to RM79/mo | Improved retention |
| 11–12 | Add 36-data-moat-history-agent for trend-driven plan angles (keto, intermittent fasting) | Content marketing |
| 13–16 | Launch annual plan at RM799/yr; add referral program; hit 50 subscribers | RM2,500 MRR |
| 17–24 | Operator oversight workflow via 34-human-approval-workflow-agent; safety audit | Compliant ops |

## Unit Economics

| Item | Cost (RM) | Revenue (RM) |
| --- | --- | --- |
| LLM per full plan | 0.50 | – |
| Stripe fees (1.8% + RM0.30) | – | on revenue |
| Hosting (Vercel + Supabase) | 150/mo | – |
| Resend transactional | 20/mo | – |
| PDF storage (Cloudflare R2) | 5/mo | – |
| Subscription price (monthly) | – | 49–99/mo |
| Annual plan | – | 399–799/yr |
| Break-even | ~10 paying subscribers | – |
| Month 12 target | – | RM5,000–8,000 MRR |

## Known Failure Modes

| Failure | Mitigation |
| --- | --- |
| Implausible intake values (BMI <14 or >50) | Zod validation + soft-warn; require operator confirmation for borderline values |
| Extreme deficit/surplus in plan | Clamp to safe ranges per ACSM; surface disclaimer; flag for operator review |
| Injury report from user | Immediately suspend plan via RLS; escalate to operator within 1h; document in audit log |
| Payment failure / dunning exhausted | Stripe dunning with 3-day grace; suspend access after 3 failures; retain data 90 days |
| Plan quality complaints | Weekly NPS survey; operator review of 1-star feedback; iterate on prompt engineering |
| PDPA compliance breach | Encrypt user data at rest; delete 12 months post-cancellation; audit logs immutable |

## First Milestone

**Day 60:** 30 paying subscribers, RM1,500 MRR, first NPS survey >40, zero safety incidents, automated weekly check-in emails live, plan delivery P95 <60s.
