# 17. Local Business Lead-Gen

Part of **AI-Powered Data & Lead Platform**. Turn local market data into warm leads.

Finds and qualifies leads for local businesses using problem detection (bad reviews, no chat widget, no booking, slow site) and drafts personalized cold outreach. This is the lead engine.

## Metrics

| Attribute | Value |
|---|---|
| Risk | Medium |
| Capital | RM400–RM2,000 |
| Success Probability | Medium |
| Time to First RM | 1–3 months |
| Skills Needed | Web scraping, cold outreach/sales, CRM basics |

## Stack

| Layer | Choice | Why |
|---|---|---|
| Scraping | Playwright + httpx | Google Maps, Yelp, Yellow Pages |
| Enrichment | Hunter.io free tier + tech-stack detector (Wappalyzer-style) | Email + CMS/hosting detection |
| AI | Anthropic Haiku + Sonnet | Haiku for classification; Sonnet for personalized audit copy |
| Outreach | Resend + warmed domain | RM0.10/1k emails; separate from personal domain |
| Scheduling | Cal.com | Free booking page for pilot calls |
| CRM | Supabase (lightweight) | Track prospect stage, opens, replies |

## Execution Plan

### Week 1 — Pipeline + first vertical
- Build Google Maps scraper: niche + city → business name, address, phone, website, rating, review count
- Enrich: find owner email, detect tech stack, check for chat widget / booking / mobile speed
- Score: unanswered reviews + no booking + slow site = hot lead (80–100)

### Week 2 — Personalized outreach
- Draft template: 3 sentences, 1 specific observation about their business, offer free 5-point audit
- Send 20 emails/day from warmed domain; track opens (Resend) and replies
- A/B test subject lines and offers

### Week 3 — Pilot offers
- Free pilot: "I'll audit 10 businesses in your niche and deliver a PDF report — you keep the leads"
- Paid pilot: RM800/mo for 20 qualified leads + weekly report
- Target: 5 booked calls, 2–3 pilots running

### Month 2+ — Upsell
- Once trust is established, upsell to #30 (review response) and #7 (chatbot)
- Each client can buy up to 3 revenue lines: lead-gen + review response + chatbot

## Unit Economics

| Item | Cost | Revenue |
|---|---|---|
| Email + enrichment per lead | RM0.05–0.20 | — |
| Pilot (RM800/mo, 20 leads) | RM1–4/mo | RM800/mo |
| **COGS per lead** | **RM0.10–0.50** | **RM40–800/mo per client** |
| Margin | 95%+ | — |

## Known Failure Modes

| Failure | Mitigation |
|---|---|
| Low reply rate | Change offer or niche, not volume; audit > cold pitch |
| Domain gets warm → spam | Warm domain 30 days before outreach; monitor reputation |
| Legal (PDPA/CAN-SPAM) | Unsubscribe link in every email; suppress list; no bought lists |
| Client says "no leads" | Triple-check lead quality before delivery; record source of each lead |

## First Milestone

**Day 14:** 200 scored prospects in DB, 140 emails sent, 5 booked calls, 2 pilots running, first RM from a pilot.
