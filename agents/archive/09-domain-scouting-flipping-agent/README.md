# Domain Scouting & Flipping Agent

## Metrics

| Metric | Value |
|--------|-------|
| Risk | Medium-High |
| Capital | RM 50–RM 500 per domain |
| Success Probability | 25–40% (highly comp-dependent) |
| Time to First RM | 1–4 weeks (aftermarket close) |
| Skills Needed | SEO analysis, marketplace negotiation, basic valuation |

## Stack

| Layer | Choice | Why |
|-------|--------|-----|
| Scraping | Playwright + httpx | Bypass bot protection on GoDaddy/Sedo/Afternic closeout pages |
| Backlink Data | Majestic / Ahrefs API | Industry-standard DR/RD metrics; Majestic cheaper for bulk |
| WHOIS History | Whoxy API | Historical ownership + drop-date signal |
| Registrar | Namecheap / Porkbun API | Low-fee .com/.net; bulk backorder support |
| Marketplace | Sedo / Afternic / Dan.com | Aftermarket listings with existing traffic |
| Data Ledger | Supabase | Track candidates, comps, outcomes for moat history |
| Outreach | Resend | High deliverability, PDPA-friendly audit log |
| Scoring | Pandas | Reproducible comp-model + brandability heuristics |

## Execution Plan

| Week | Task |
|------|------|
| 1 | Set up Playwright scrapers for GoDaddy closeouts + expired list per TLD. Integrate Whoxy + Majestic API. Build Supabase candidates table. |
| 2 | Build scoring model: DR, RD, keyword volume, brandability score. Validate against 20 known sales. |
| 3 | Enable backorder flow via Namecheap API for .com drops. Set max-bid ceiling rules. |
| 4 | Integrate aftermarket scrapers (Sedo, Afternic, Dan.com). Build outreach-draft generator with ZeroBounce verification. |
| 5 | Run first weekly batch: 500-domain scan, 10 outreach emails. Review hit rate; adjust scoring thresholds. |
| 6–8 | Expand to 2k domains/scan. Add A/B outreach templates. Track win rate in Supabase. |
| 9–12 | Scale to 5k domains/scan with auction-close monitoring. Target 2–3 domain closes/month. |

## Unit Economics

| Item | Cost | Revenue |
|------|------|---------|
| Scan 5k domains | RM 1.00 | — |
| Outreach email | RM 0.05 | — |
| Domain registration (expired) | RM 30–RM 200 | — |
| Domain purchase (aftermarket) | RM 100–RM 500 | — |
| Resale premium (avg) | — | 30–200% over purchase |
| Holding cost/yr | RM 30–RM 100 | — |

**Break-even:** Flip 1 of 5–10 scanned domains above 3x cost.

## Known Failure Modes

| Failure | Mitigation |
|---------|-----------|
| Auction snipe loses (outbid last second) | Set max-bid ceiling; track win-rate; adjust comp model |
| Drop-catch fails (backorder not fulfilled) | Use multiple backorder providers; rotate per TLD |
| Outreach email bounces / spam | Verify emails via ZeroBounce before send; surface for manual outreach |
| Comparable-sales data stale | Refresh comps table daily; ignore comps >180 days old for >RM1k domains |
| Trademark conflict on brandable name | Pre-check USPTO/EUIPO trademark DB before outreach |
| Domain quality degrades (penalised by Google) | Check Wayback for spam history; reject if >50% spam snapshots |

## First Milestone

**Day 14:** First domain scan of 500 candidates completed, 3 outreach emails sent, 0 purchases made (learning baseline). Target: by Day 30, close first expired domain below RM200 with est_value > RM600.
