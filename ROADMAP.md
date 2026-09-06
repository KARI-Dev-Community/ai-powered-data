# Roadmap — Agentic Passive Income Stack

Dependency-ordered plan for a solo software developer using AI agents.
Core thesis: **build the lead machine first; products are cheap for you to build, leads are the bottleneck.**

All figures in Malaysian Ringgit (RM), converted from USD at ~RM4/USD.

---

## Phase 0 — Foundation (Week 1)

**Build once, reuse everywhere: the scraping + enrichment + outreach pipeline.**

- Google Maps / Yelp / marketplace scrapers with problem detection (unanswered reviews, no chat widget, no booking)
- Prospect DB (Supabase/Postgres), enrichment (email finder, tech-stack detection), outreach tracker
- Cost: ~RM0–RM200 | Revenue: RM0 | Exit criteria: 200+ scored prospects in DB

This single pipeline powers #17, #26, #27, and #11.

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
3. **#19 Bookkeeping agent** — stickiest product, sell to warm trust

Exit criteria: 5–10 clients → **RM4,000–RM12,000/mo**.

## Phase 4 — Compounding layer (Month 3+)

- **#1 Blog/affiliate agent** — publish real case studies; SEO compounds and feeds inbound leads back into Phase 2 (self-refilling loop)
- **#10 Micro-SaaS** — optional: package the best-received Phase-3 product as standalone SaaS using proven billing/agent infra

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

# Agentic Gap Analysis

Where current agent tech falls short in these 30 ideas — and where the gaps are opportunities.

## A. Technical gaps (what breaks in production)

| Gap | Affected ideas | Reality | Your edge |
|---|---|---|---|
| **Long-horizon reliability** — agents drift/derail after 30+ steps; nobody runs a truly unattended revenue agent | All | "Passive" = human-in-the-loop checkpoint 1–2×/week. Budget for it | Build checkpoint/rollback orchestration — this IS the product for #7/#19 |
| **Payment & auth autonomy** — agents can't safely hold credentials or make purchases (ads, domains, stock) | #3, #9, #15 | Requires human approval step → not passive | Sell "human-approved automation" as a trust feature |
| **Platform ToS / API walls** — Google, Yelp, Etsy, Amazon, YouTube actively detect & ban automated activity | #2, #8, #14, #23, #26, #27, #30 | Accounts get suspended; revenue dies overnight | Proxy/rotation + rate-limit engineering is a real moat — but keep fallback channels |
| **Output QA at scale** — LLM output quality degrades without review (hallucinated facts, broken links, bad legal/accounting advice) | #1, #12, #28, #19 | Unreviewed content = penalty/ban risk | Build eval pipelines (LLM-as-judge + spot checks); sell the QA layer, not just generation |
| **Liability + regulation** — signals, legal docs, financial data are licensed activities | #5, #28 | Regulatory risk can make ROI negative regardless of execution | Avoid #5; #28 only with a licensed partner |

## B. Market gaps (ideas missing from the list of 30)

1. **Agent-ops / monitoring-as-a-service** — every one of these 30 ideas needs uptime, drift, and cost monitoring for its agents. Sell that layer to other agent builders (#7 white-label, #11 API).
2. **Compliance-check agent for agent-builders** — ToS/regulation auditing for automated workflows. The meta-gap: you'd get paid by the same crowd running ideas #1–#30.
3. **Agent QA / eval harness as a product** — gap A4 packaged. No-code crowd can't build evals; you can.
4. **Human-approval workflow layer** — the missing piece between "full autonomy" and "manual work": approval inbox, audit trail, rollback. Sits on top of #7/#19/#30.
5. **Local-services ops agent** — the list covers review response and lead-gen but not the actual ops gap: quote-generation, scheduling, follow-up for plumbers/HVAC/roofers. Higher ticket than any idea in the doc.
6. **Data-moat products** — #11's real version: accumulate proprietary scraped history (price curves, review velocity, rental rates) that gets *more* valuable over time and can't be re-scraped by competitors. None of the 30 ideas explicitly build a data moat.

## C. Strategic conclusion

The 30 ideas mostly use agents as **content generators** (the commoditized half). The durable money is in the gaps:

- **Reliability layer** (A1–A4) — everyone building agents needs it; almost nobody sells it
- **Data moats** (B6) — one-time scraping is a commodity; accumulated history is an asset
- **Human-approval automation** (A2/B4) — the realistic "passive income" of 2026 isn't full autonomy, it's *5-minute-per-day supervised autonomy*

**Priority insert into roadmap:** B6 (data-moat history accumulation) starts in Phase 0 alongside the scraper — zero extra effort, compounds the value of everything downstream.
