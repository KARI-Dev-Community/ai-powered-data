# Customer / User Journey

Audience: business team, sales, product.

This document maps the end-to-end experience for each customer type, from first touch to expansion.

---

## 1. Customer Segments

| Segment | Who they are | Primary product | Price point |
|---|---|---|---|
| **Data API buyers** | E-commerce ops, VC research, competitor intel teams | #11 Public data API | RM200–800/mo per dataset |
| **Lead-gen clients** | Local service agencies, SMB owners, B2B services firms | #17 Lead-gen engine | RM800–2,000/mo per niche |
| **Review management clients** | Restaurants, clinics, trades, professional services | #30 Review response | RM800/mo retainer |
| **Chatbot upsell clients** | Existing review clients, service businesses with high inquiry volume | #7 White-label chatbot | RM1,500–3,000/mo |
| **Dataset export buyers** | Non-technical buyers who want CSV/JSON snapshots | #11 Exports | RM400–1,000 one-time |

---

## 2. Journey Map: Data API Buyer

### Stage 1 — Discovery
- **Touchpoint:** Product Hunt / LinkedIn / niche community (e-commerce ops, indie hacker forums)
- **Mindset:** "I need competitor pricing / market signals without building a scraper"
- **Asset:** Landing page with live demo dataset + pricing page

### Stage 2 — Signup
- **Touchpoint:** `/v1/datasets/{dataset_name}/entities` free trial
- **Action:** Get API key via `/v1/sources` registration or direct sales outreach
- **Friction point:** API key delivery must be <5 minutes

### Stage 3 — First call
- **Touchpoint:** Onboarding email with OpenAPI spec, sample curl request, 1-page getting-started guide
- **Mindset:** "Can I trust this data freshness and schema stability?"
- **Proof:** Show `scraped_at`, `provenance`, `schema_version` in every response

### Stage 4 — Usage
- **Touchpoint:** Daily/weekly API calls; `/v1/timeseries` for historical queries
- **Value moment:** First time they run a time-series query and see 90 days of clean history
- **Support:** Uptime SLA 99.5%, p95 <200ms, usage logging visible to customer

### Stage 5 — Expansion
- **Trigger:** They hit rate limit or need a new vertical
- **Upsell:** Higher tier (RM400→800/mo), additional dataset, custom source build (2× price)

### Stage 6 — Retention
- **Touchpoint:** Monthly usage report + new dataset announcements
- **Churn risk:** Schema drift or source downtime without proactive alert
- **Mitigation:** Source health endpoint, proactive emails when we add new sources

---

## 3. Journey Map: Lead-Gen Client

### Stage 1 — Discovery
- **Touchpoint:** Cold email / referral / LinkedIn
- **Mindset:** "I need more qualified leads but don't have time to hunt"
- **Asset:** Personalized email referencing their specific pain point (unanswered review, slow site)

### Stage 2 — Pilot offer
- **Touchpoint:** Email reply → scheduling call → pilot agreement
- **Action:** Sign 30-day pilot: 20 scored leads, free
- **Friction point:** Trust — they've been burned by agencies before
- **Proof:** Show sample prospect report (name, score, observed pain signal, suggested outreach angle)

### Stage 3 — Onboarding
- **Touchpoint:** Kickoff call + 48-hour turnaround
- **Action:** Define niche, ideal customer profile, deliverability channel (email/LinkedIn)
- **Mindset:** "Will these leads actually respond?"

### Stage 4 — First delivery
- **Touchpoint:** Weekly lead CSV / CRM integration / direct outreach on their behalf
- **Value moment:** First booked call or reply from a lead
- **Metric:** Reply rate ≥15% = product-market fit signal

### Stage 5 — Conversion
- **Trigger:** 2–3 booked calls or positive reply rate during pilot
- **Action:** Convert to RM800–2,000/mo retainer
- **Pricing logic:** Per niche, per geography, per lead volume

### Stage 6 — Retention / Expansion
- **Touchpoint:** Weekly report: leads sent, replies, calls booked, closed deals
- **Upsell paths:**
  - Add review management (#30) = bundle RM2,000/mo
  - Add chatbot (#7) = bundle RM2,500/mo
  - Expand to new niche/city = additional retainer
- **Churn risk:** Lead quality drops or reply rates fall below 10%
- **Mitigation:** Monthly quality review, adjust scoring weights, rotate niches

---

## 4. Journey Map: Review Response Client

### Stage 1 — Discovery
- **Touchpoint:** Cold email / outbound call / referral from existing lead-gen client
- **Mindset:** "I know I should respond to reviews but I don't have time / don't know what to say"
- **Asset:** Email showing 3 of their unanswered reviews with example responses drafted

### Stage 2 — Pilot offer
- **Touchpoint:** Email reply → quick close (no long sales cycle)
- **Action:** 30-day free pilot: respond to all new reviews within 24 hours
- **Friction point:** Access to their Google Business Profile / Facebook page
- **Mitigation:** Simple onboarding: owner adds email as manager, we handle the rest

### Stage 3 — Onboarding
- **Touchpoint:** 15-minute setup call
- **Action:** Connect accounts, set approval rules, define escalation criteria
- **Mindset:** "Will this sound like me? Will it handle negative reviews correctly?"

### Stage 4 — First response
- **Touchpoint:** First review posted → AI draft → approval notification → posted response
- **Value moment:** Owner sees a thoughtful, on-brand reply within hours
- **Metric:** Response rate 100%, approval rate ≥90% (most drafts posted without edits)

### Stage 5 — Conversion
- **Trigger:** Owner sees consistent quality during pilot
- **Action:** RM800/mo retainer, monthly billing, 30-day notice cancellation

### Stage 6 — Retention / Expansion
- **Touchpoint:** Monthly report: reviews captured, responses posted, sentiment trend
- **Upsell paths:**
  - Chatbot (#7) for booking and FAQ automation
  - Review request automation (post-job follow-up emails)
- **Churn risk:** Reputation score plateaus or they lose interest
- **Mitigation:** Quarterly business review, show trend graphs, highlight competitors' review rates

---

## 5. Journey Map: Chatbot Client (Upsell)

### Stage 1 — Trigger
- **Context:** Existing review response client
- **Touchpoint:** Sales conversation during monthly review
- **Mindset:** "I'm getting more reviews and calls now, but I can't answer them all"

### Stage 2 — Demo
- **Touchpoint:** Live demo on their website / Facebook page
- **Action:** Show chatbot handling common questions, booking, FAQ
- **Value moment:** Bot answers a question in their voice, 24/7, without them touching anything

### Stage 3 — Pilot
- **Touchpoint:** 14-day pilot on their site/FB page
- **Action:** Configure intents, handoff rules, escalation to human
- **Metric:** 80%+ deflection rate, customer satisfaction ≥4/5

### Stage 4 — Launch
- **Touchpoint:** Go-live + training
- **Action:** RM1,500–3,000/mo, white-labeled if agency
- **Ownership:** Client owns conversations; we own the infrastructure and tuning

### Stage 5 — Optimization
- **Touchpoint:** Monthly tuning report
- **Action:** Add intents, improve fallback messages, A/B test greetings
- **Expansion:** Add WhatsApp, Instagram, Telegram channels

---

## 6. Anti-Patterns (What We Avoid)

| Anti-pattern | Why it hurts | What we do instead |
|---|---|---|
| Long onboarding (>7 days) | Client loses momentum, churn before first value | Ship first deliverable within 48 hours |
| Generic templates without personalization | Low reply rates, brand damage | Every touch references a specific observed problem |
| Overpromising results | Expectation mismatch, churn, refunds | Clear scope, no guarantee clauses, pilot before retainer |
| Lock-in / exit barriers | Client fear, bad reputation | Month-to-month contracts, data export on request |
| Hidden fees | Trust destruction | Transparent pricing, usage-based API billing visible to customer |
| Selling data as a commodity | Price war with scrapers | Sell history, schema stability, AI QA — things money can't buy |

---

## 7. Key Metrics by Segment

| Segment | Activation metric | Retention metric | Expansion metric |
|---|---|---|---|
| Data API | First successful API call within 1 hour of signup | Monthly active API keys, p95 latency | Tiers, datasets, custom sources |
| Lead-gen | First booked call within 14 days | Reply rate ≥15%, weekly delivery consistency | New niches, add-on services |
| Review response | First response posted within 24 hours | Approval rate ≥90%, sentiment trend | Chatbot upsell, review request automation |
| Chatbot | First deflection within 48 hours of go-live | Handoff accuracy, CSAT ≥4/5 | New channels, agency white-label |

---

## 8. Ideal Customer Profile (ICP)

**Primary ICP:**
- Malaysian or Singaporean SMB owner or agency principal
- 5–50 employees, RM500k–5M annual revenue
- Active on Google Maps / Facebook with reviews
- Already spending RM1,000+/mo on marketing that isn't working
- Speaks English, willing to try new tools if ROI is clear

**Secondary ICP:**
- Data buyer: e-commerce ops manager, growth lead, startup founder
- Needs market signals, competitor pricing, or lead enrichment
- Comfortable with APIs, willing to pay for clean data

---

## 9. Journey Gaps We're Actively Fixing

| Gap | Current state | Target state |
|---|---|---|
| API self-serve signup | Manual key delivery | Automated key generation + usage dashboard |
| Lead-gen CRM integration | CSV export | Direct HubSpot/Zoho/Sheet sync |
| Review approval UX | Email threads | Web dashboard with approve/reject/edit |
| Source health visibility | Internal only | Customer-visible status page |
| Billing automation | Manual invoices | Stripe/Lemon Squeezy self-serve |
