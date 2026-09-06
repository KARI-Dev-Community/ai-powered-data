# Technical Setup — AI-Powered Data & Lead Platform

Turn local market data into warm leads.

All figures in Malaysian Ringgit (RM). Total running cost: **~RM60–200/mo + RM40 domain**.

---

## Hardware

| Item | Requirement | Cost |
|---|---|---|
| Your Linux machine | Any 8GB+ RAM laptop — everything runs on APIs, no GPU needed | RM0 |
| VPS (always-on scraper + API hosting) | 2 vCPU / 4GB — Hetzner CX22 (~RM20/mo) or DigitalOcean Singapore (RM26/mo, lower latency from Malaysia) | RM20–26/mo |

## Software stack (all free/open source)

| Layer | Pick | Why |
|---|---|---|
| Language | **TypeScript/Node** or Python 3.12 — whichever you're fastest in | Speed of iteration > everything |
| Scraping | **Playwright** (JS-heavy sites) + raw **httpx/curl + JSON APIs** where possible | Playwright only where needed; plain HTTP is 10× cheaper |
| Scheduling | **GitHub Actions cron** (free) for daily scrapes; systemd timers / node-cron on VPS for frequent runs | Zero infra to start |
| Database | **SQLite** locally → **Supabase Postgres** (free tier) when remote access/auth needed | Also feeds #11/#34 |
| API framework (#11) | **FastAPI** (Python) or **Hono** (Node) | Deploys anywhere in minutes |
| Billing | **Lemon Squeezy** or **Paddle** (merchant of record — no SST/company-registration hassle); **Billplz/FPX** if selling to Malaysian SMBs | MoR handles global sales tax for you |
| Email outreach (#17) | **Amazon SES** (RM0.16/1k emails) or **Resend** + a separately-warmed domain | Never cold-email from your main domain |
| Landing pages | **Astro** static on **Cloudflare Pages** (free) | One landing page per product |
| Repo/CI | **GitHub** (free) | Actions doubles as your scheduler |
| AI APIs | **Anthropic + OpenAI** keys, ~RM20–80/mo to start | Haiku / GPT-4o-mini for classification & QA; bigger models only where they earn it |

## Accounts checklist (Week 0)

- [ ] Dedicated domain (~RM40/yr) — separate from personal email; this warms up for cold outreach
- [ ] Hetzner or DigitalOcean account → VPS
- [ ] Supabase project (free tier)
- [ ] Lemon Squeezy or Paddle account (or Billplz for MYR/FPX local clients)
- [ ] Amazon SES or Resend account
- [ ] Anthropic + OpenAI API keys with **hard monthly spend caps**
- [ ] GitHub repo: `ai-powered-data`
- [ ] Optional: Loom account (free tier) for video audits in #17

## First sprint — 5 days

### Day 1–2 — Phase 0 (scraper + prospect DB)

```bash
mkdir -p ai-powered-data/{scrapers,enrichment,outreach,api}
```

- One scraper: Google Maps businesses for a niche+city → dedupe → SQLite with name, phone, email, website, review count, unanswered-review estimate
- Score each prospect: bad reviews + no chat widget + slow site = hot

### Day 3 — Productize (#11/#27)

- Wrap the pipeline in FastAPI: `/v1/businesses?niche=hvac&city=dallas`
- Deploy to VPS; landing page on Cloudflare Pages with a Lemon Squeezy buy button

### Day 4–5 — Lead engine (#17)

- Enrichment (Hunter.io free tier or your own email finder)
- Agent-generated personalized audits; 20 emails/day from the warmed domain

### Ongoing

- Start #36's history logging **on day 1** — the archive table is free and compounds
- Activate agents via the repo pattern:

```bash
mkdir -p .kilo/agent && cp agents/active/36-data-moat-history-agent/agent.md .kilo/agent/
```

## Malaysia-specific notes

- **Payments:** a merchant-of-record (Lemon Squeezy/Paddle) avoids SST/e-invoicing paperwork entirely; use Billplz only once selling locally at volume
- **SST:** register only if/when revenue exceeds the SST threshold — plan to stay under it early
- **Time zone:** schedule outreach to US/EU clients for *their* 9am, not yours

## Where this fits

See [`ROADMAP.md`](./ROADMAP.md) for the phase plan this checklist implements (this is the Week 0–1 material for Phases 0–2).
