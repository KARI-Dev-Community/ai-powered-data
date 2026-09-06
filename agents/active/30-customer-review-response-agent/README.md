# 30. Customer Review Response / Reputation Agent

Monitors and responds to customer reviews across Google, Yelp, TripAdvisor, and Facebook on behalf of local-business clients. Easiest sell in the Phase 3 upsell chain because every business owner understands review reputation.

## Metrics

| Attribute | Value |
|---|---|
| Risk | Low |
| Capital | RM400–RM1,200 |
| Success Probability | Medium-High |
| Time to First RM | 1–3 months |
| Skills Needed | API integration (Google/Yelp), copywriting, sentiment analysis basics |

## Stack

| Layer | Choice | Why |
|---|---|---|
| Ingest | Google My Business API, Yelp Fusion, TripAdvisor API | Official APIs; fallback to Playwright if quota limits |
| AI | Anthropic Haiku/Sonnet | Draft response, classify sentiment, flag legal issues |
| Storage | Supabase | Store review history, response drafts, client config |
| Notify | Resend + Slack webhook | Alert client when human approval needed |
| Approval | Custom inbox (Astro + Serverless) | Client reviews drafts, clicks approve |

## Execution Plan

### Week 1 — Ingest + triage
- Connect 1 client's Google Business Profile; ingest reviews via API
- Classify: sentiment (positive/neutral/negative), priority (legal/safety = P0)
- Draft response for non-P0 reviews; route P0 to human immediately

### Week 2 — Brand voice + approval flow
- Collect brand-voice examples from client (past responses, tone guidelines)
- Fine-tune drafts: 2–3 options per review, tone-matched, factually grounded
- Build approval inbox: client sees draft + original review, clicks Approve/Edit/Reject

### Week 3 — Multi-platform + reporting
- Add Yelp and TripAdvisor connections
- Weekly report: reviews ingested, avg response time, sentiment trend, flagged issues
- Client pays RM800/mo retainer after free 2-week pilot

### Month 2+ — Scale
- 5–10 clients at RM800/mo = RM4,000–8,000/mo
- Add #7 chatbot upsell to same clients ("respond to reviews → capture bookings")

## Unit Economics

| Item | Cost | Revenue |
|---|---|---|
| AI + API per review | RM0.02–0.10 | — |
| 50 reviews/client/mo | RM1–5/mo | RM800/mo |
| **COGS per client** | **RM2–10/mo** | **RM800/mo** |
| Margin | 98%+ | — |

## Known Failure Modes

| Failure | Mitigation |
|---|---|
| API quota exceeded | Queue reviews; process when quota resets; alert client |
| Client rejects all drafts | Collect better brand-voice samples; add tone slider |
| Negative review escalates to legal | Auto-escalate P0 (rating ≤ 2 or legal keywords) within 15 min |
| Fake review posted | Flag for human; do not auto-respond; advise client on platform appeal |

## First Milestone

**Day 14:** 1 client live, 2-week pilot complete, weekly report delivered, client converts to RM800/mo retainer.
