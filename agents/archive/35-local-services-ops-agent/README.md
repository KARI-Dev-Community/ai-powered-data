# 35. Local-services ops agent (quotes, scheduling, follow-up)

Handles quoting, scheduling, and customer follow-up for local service businesses — plumbers, HVAC, roofers, cleaners. Covers revenue-generating operations, not just reputation.

## Metrics

| Attribute | Value |
|---|---|
| Risk | Medium |
| Capital | RM400–RM2,000/mo |
| Success Probability | Medium-High |
| Time to First RM | 1–3 months |
| Skills Needed | API integration (SMS/calendar/CRM), prompt engineering, hospitality-ops logic, Stripe billing |

## Why it's a gap

The repo covers local businesses only on the reputation side (#30 review response) and lead side (#17). The actual money gap for a plumber is the quote-to-book pipeline: missed calls = lost jobs, slow quotes = lost jobs, no follow-up = lost rebooking. An agent that recovers even 2 jobs/month pays for itself many times over — an easy ROI pitch.

## Pricing model

- RM1,200–RM2,400/mo per business (justified vs. 1–2 recovered jobs)
- Per-lead pricing option: RM20–RM60 per qualified lead handled
- Vertical expansion: one niche (HVAC) at a time; rate cards are vertical-specific

## Stack

| Layer | Choice | Why |
|---|---|---|
| Ingest channels | Twilio (SMS/voice) + web form + missed-call-textback | Local customers call/text; SMS is primary channel in MY/SG |
| Quote engine | Anthropic Claude + Supabase | Parse lead details, apply rate-card rules, generate branded quote |
| Scheduling | Cal.com + Google Calendar API | Slot availability, buffer rules, technician assignment |
| Follow-up | Celery + Redis + Twilio | Review requests (2h post-job), rebooking nudges, dormant win-back |
| Payments | Stripe | Deposit collection at quote acceptance; split payment links |
| Notifications | Resend (email) + Twilio (SMS) | Confirmations, reminders, follow-up sequences |
| Storage | Supabase Postgres | Rate cards, leads, quotes, appointments, follow-up state machine |
| Monitoring | #34 approval workflow | Alert on missed-call recovery lag, quote turnaround SLA breaches |
| Baseline data | 36-data-moat-history-agent | Historical conversion rates, service demand patterns for scheduling optimization |

## Execution Plan

### Week 1 — Core quoting + scheduling
- Build lead ingestion: Twilio webhook for SMS/missed-call-textback; web form for inquiries
- Build quote engine: load rate card from Supabase; apply urgency multiplier + travel fee; generate quote with Stripe payment link
- Integrate Cal.com + Google Calendar API: book job with buffer rules; send calendar invite
- Test with 1 HVAC business (friend/family): full quote-to-book flow end-to-end

### Week 2 — Follow-up + notifications
- Build post-job follow-up sequence: review request at 2h, rebooking reminder at service interval, dormant nudge at 90 days
- Resend email templates + Twilio SMS templates per brand voice config
- Weekly owner report: leads handled, quotes sent, conversion rate, revenue booked, missed-call recovery stats
- Dogfood with #17 lead-gen agent: #17 passes lead → #35 quotes + books

### Week 3 — First paying client + vertical packaging
- Package as "HVAC Ops-in-a-Box": rate card templates, SMS scripts, follow-up sequences pre-built for HVAC
- Price: RM1,200/mo per business; RM500 setup for custom rate card
- First client = local HVAC business with 5–10 missed calls/week
- Track: missed calls recovered, quotes sent, jobs booked, revenue attributed to agent

### Month 2+ — Vertical expansion + scale
- Add vertical templates: plumbing, roofing, cleaning (each has unique rate-card structure + service intervals)
- Build agency tier: manage 10+ local businesses from one dashboard; white-label for marketing agencies
- Integrate with #30 (review response): auto-request review after job complete; feed positive reviews back to #17 for lead gen
- Add "emergency dispatch" mode: for after-hours emergencies, auto-escalate to on-call human + send confirmation SMS

## Unit Economics

| Item | Cost | Revenue |
|---|---|---|
| Twilio + Cal.com + Google Calendar API | RM30–50/mo | — |
| LLM quote generation per lead | RM0.10–0.40 | — |
| Resend + storage | RM10–20/mo | — |
| 1 business @ RM1,200/mo | RM50–100/mo | RM1,200 |
| 10 businesses (agency) @ RM1,200 | RM500/mo | RM12,000 |
| **COGS per business** | **RM50–100/mo** | **RM1,200/mo** |
| Margin | 85–90% | — |
| Break-even | 1 business (recovering 1 job/month pays for it) | — |

## Known Failure Modes

| Failure | Mitigation |
|---|---|
| Rate card mismatch quotes wrong price | Double-check rate card JSON schema on ingest; validate total = Σ(line_items) before sending; flag discrepancy to owner |
| Scheduling conflict (double-book) | Pause auto-booking if calendar sync lag > 5 min; verify slot availability with exclusive lock before confirming |
| SMS delivery failure (Twilio) | Retry via email + voice callback; escalate to owner if 2 consecutive failures across all channels |
| Customer ghost after quote | Auto-follow-up at 1h, 24h, 72h; if no response after 3 attempts, mark lost and feed reason to #17 for lead quality tuning |
| Emergency job misrouted to auto-quote | Emergency keyword + urgency=emergency bypasses auto-quote; immediately page human dispatcher via Slack + SMS |
| Calendar sync lag causes stale slots | Cache availability snapshot with 5-min TTL; verify with exclusive write lock at booking time; alert ops if sync lag persists |

## First Milestone

**Day 30:** Full quote-to-book flow live (SMS/web → quote → calendar → confirmation), post-job follow-up sequence active, 1 HVAC business onboarded (RM1,200/mo), missed-call-textback recovering 3+ jobs/week, first RM1,200/month recurring revenue.

---

This idea is implemented by [`agent.md`](./agent.md) in this folder.

### Activating the agent (copy, don't move)

To use this agent in Kilo, **copy** `agent.md` into `.kilo/agent/`:

```bash
mkdir -p .kilo/agent
cp 35-local-services-ops-agent/agent.md .kilo/agent/35-local-services-ops-agent.md
```
