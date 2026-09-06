# AI-Powered Data & Lead Platform

Turn local market data into warm leads.

Collects proprietary local-market data, scores prospects, and delivers ready-to-act leads to local service businesses — with AI quality control at every step.

## Products

| # | Product | Role |
|---|---|---|
| 36 | Data-Moat History | Compounding local-market history layer |
| 27 | Price-Tracking / Deal Alerts | Consumer signal product on the same data |
| 11 | Public Data API | B2B access to scored, time-series datasets |
| 17 | Local Business Lead-Gen | Warm leads from observed market pain |
| 30 | Customer Review Response | Reputation ops upsell on the same leads |

Related follow-ons (#7 chatbot, #34 approval, #35 local-services ops) live in `agents/archive/`.

## Directory Layout

```
agents/
├── active/
│   ├── 36-data-moat-history-agent/
│   ├── 27-price-tracking-deal-alert-bot/
│   ├── 11-public-data-aggregation-api/
│   ├── 17-local-business-lead-gen-agent/
│   └── 30-customer-review-response-agent/
└── archive/
db/
scrapers/
app/api/v1/
scripts/
web/
```

## How to use an agent

Agents in these folders are **inactive by default**. Kilo only loads agents from `.kilo/agent/`.

To activate one, **copy** (not move) its `agent.md` into `.kilo/agent/`:

```bash
mkdir -p .kilo/agent
cp agents/active/36-data-moat-history-agent/agent.md .kilo/agent/36-data-moat-history-agent.md
```

To deactivate, delete the copy in `.kilo/agent/` (the original folder is untouched).

## Quick Start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium

cp .env.example .env
# Fill in Supabase + API keys

python3 scripts/validate-agents.py
uvicorn app.api.v1.main:app --reload --port 8000
python3 scrapers/google-maps/scraper.py
```

## Docs

- [`ROADMAP.md`](./ROADMAP.md) — phase plan and KPI gates
- [`TRACKER.md`](./TRACKER.md) — progress, finance, kill criteria
- [`BUSINESS-PROPOSAL.md`](./BUSINESS-PROPOSAL.md) — product, market, GTM
- [`CUSTOMER-JOURNEY.md`](./CUSTOMER-JOURNEY.md) — segment journeys
- [`SYSTEM-DESIGN.md`](./SYSTEM-DESIGN.md) — architecture
- [`TECHNICAL-SETUP.md`](./TECHNICAL-SETUP.md) — stack and accounts
