# 18. AI resume/LinkedIn optimization service

## Metrics

| Risk | Capital | Success Probability | Time to First RM | Skills Needed |
| --- | --- | --- | --- | --- |
| Low | RM0–RM400 | Medium-High | 1–2 months | Prompt engineering, career-coaching knowledge, freelance marketing |

## Stack

| Layer | Choice | Why |
| --- | --- | --- |
| Generation | Anthropic Claude Sonnet 4 | Strongest at structured rewrite |
| ATS format | python-docx + weasyprint | DOCX + PDF, no tables |
| Billing | Lemon Squeezy (or Stripe) | Per-package or subscription |
| Storage | Supabase | Client ledger, NDA trail |
| Delivery | Resend + signed download URLs | Secure, audit-friendly |
| Review | 34-human-approval agent | First 50 clients get a human pass |

## Execution Plan

| Week | Step |
| --- | --- |
| 1 | Build the rewrite + DOCX/PDF pipeline, set up Lemon Squeezy |
| 2 | Manually rewrite 5 resumes as seed + benchmark quality |
| 3 | List on Fiverr, Upwork, Reddit r/careerguidance |
| 4 | Add LinkedIn package + cover letter, raise price |
| 5 | Onboard 10 paying clients, collect testimonials |
| 6-10 | Scale to 30 clients/month, build interview-prep upsell |
| 11-12 | Add 36-data-moat-history-agent for industry trend signals |

## Unit Economics

| Item | Cost (RM) | Revenue (RM) |
| --- | --- | --- |
| LLM per package | 0.30 | – |
| Lemon Squeezy fees (5%) | – | on revenue |
| Resume only | – | 99 |
| Resume + LinkedIn | – | 199 |
| Full bundle | – | 349 |
| Break-even | 1 client/day | – |

## Known Failure Modes

| Failure | Mitigation |
| --- | --- |
| ATS flags resume as AI | Mix client phrasing, add metrics, vary sentence length |
| No JD provided | Default rewrite + 3 clarifying questions |
| Client dissatisfaction | Unlimited revisions, human review for first 50 |
| PII handling | 30-day delete default, signed URLs, encrypted at rest |

## First Milestone
Day 30: 10 paid clients, RM2,000 revenue, 5 testimonials, first repeat customer.