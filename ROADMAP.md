# Roadmap — AI-Powered Data & Lead Platform

Turn local market data into warm leads.

Dependency-ordered plan for a solo operator using AI agents.
Core thesis: **build the data moat first, then the lead machine; products are cheap to ship, warm leads are the bottleneck.**

All figures in Malaysian Ringgit (RM), converted from USD at ~RM4/USD.

---

## Phase 0 — Foundation (Week 1)

**Build once, reuse everywhere: the scraping + enrichment + outreach pipeline.**

- Google Maps / Yelp / marketplace scrapers with problem detection (unanswered reviews, no chat widget, no booking)
- Prospect DB (Supabase/Postgres), enrichment (email finder, tech-stack detection), outreach tracker
- Cost: ~RM0–RM200 | Revenue: RM0 | Exit criteria: 200+ scored prospects in DB

This single pipeline powers #36, #17, #27, and #11.

## Phase 1 — Quick wins (Week 1–2)

| Idea | Why first | Target |
|---|---|---|
| **#27 Price-tracking/deal bot** | Weekend build, live portfolio piece | RM200–RM1,200/mo |
| **#11 Public data API** | Same pipeline, packaged as paid API | RM400–RM2,000/mo |

Exit criteria: 2 live products, first recurring dollars, billing + deploy infra proven.

## Phase 2 — Lead engine (Month 1–2) ← critical path

- **#17 Lead-gen agent**: personalized cold email + Loom video audits, 20 audits/week, free-pilot offer
- Compliance basics: warmed domain, unsubscribe, CAN-SPAM/GDPR
- Exit criteria: 5+ booked calls, 2–3 pilots running

## Phase 3 — Monetize leads (Month 2–4)

Sell to Phase-2 leads in upsell order (one client → up to three revenue lines):

1. **#30 Review response** — easiest sell, RM800/mo retainer after free pilot
2. **#7 White-label chatbot** — upsell to same clients ("reviews → booking bot")
3. **#35 Local-services ops** — quotes, scheduling, follow-up for the same niches

Exit criteria: 5–10 clients → **RM4,000–RM12,000/mo**.

## Phase 4 — Compounding layer (Month 3+)

- Publish case studies and market reports from the data layer; SEO feeds inbound leads back into Phase 2
- Optional: package the best-received Phase-3 product as standalone SaaS using proven billing/agent infra

---

## KPI gates (don't advance until met)

| Gate | Metric |
|---|---|
| P0 → P1 | 200 scored prospects |
| P1 → P2 | 2 products live, RM400/mo combined |
| P2 → P3 | 2 pilots converting |
| P3 → P4 | RM4,000/mo retainers, 3 testimonials |
| P4 | RM8,000–RM12,000/mo total, <10 hrs/wk maintenance |

---

# Gap Analysis

Where current agent tech falls short for this platform — and where the gaps are opportunities.

## A. Technical gaps (what breaks in production)

| Gap | Affected products | Reality | Your edge |
|---|---|---|---|
| **Long-horizon reliability** — agents drift/derail after 30+ steps | All | Human-in-the-loop checkpoint 1–2×/week | Checkpoint/rollback via #34 |
| **Payment & auth autonomy** — agents can't safely hold credentials | Outreach, billing | Requires human approval | Sell "human-approved automation" as a trust feature |
| **Platform ToS / API walls** — Google, Yelp actively detect automated activity | #17, #27, #30 | Accounts get suspended; revenue dies overnight | Proxy/rotation + rate-limit engineering; official API fallbacks |
| **Output QA at scale** — LLM drafts degrade without review | #17, #30, #7 | Unreviewed copy = brand damage | LLM-as-judge evals + #34 approval inbox |
| **PDPA / data handling** — scraped contacts and client customer data | #17, #30, #35 | Regulatory risk if resold or retained carelessly | Collect minimally; outreach-only; delete on request |

## B. Product gaps still on the roadmap

1. **#34 Human-approval workflow** — approval inbox, audit trail, rollback. Sits on top of #7 / #30 / outreach.
2. **#35 Local-services ops** — quote-generation, scheduling, follow-up for plumbers/HVAC/roofers. Higher ticket than lead-gen alone.
3. **#7 White-label chatbot** — booking/FAQ bot upsell to review and lead-gen clients.

## C. Strategic conclusion

Durable money is in the data layer and the lead machine, not content generation:

- **Data moats** — one-time scraping is a commodity; accumulated history is an asset
- **Warm leads** — scored prospects with observed pain beat impressions
- **Human-approval automation** — realistic operations in 2026 aren't full autonomy; they're *5-minute-per-day supervised autonomy*

**Priority:** #36 data-moat history starts in Phase 0 alongside the scraper — zero extra effort, compounds everything downstream.
