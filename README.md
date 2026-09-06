# Agentic Income Stack

A dependency-ordered plan and executable codebase for building AI-agent passive income systems. Current focus: **5 active agents** across Phase 0–3.

## Active Agents

| # | Agent | Phase | Dependencies |
|---|---|---|---|
| 36 | Data-Moat History Accumulation | 0 | — |
| 27 | Price-Tracking / Deal-Alert Bot | 1 | 36 |
| 11 | Public Data Aggregation → API | 1 | 36 |
| 17 | Local Business Lead-Gen | 2 | 36 |
| 30 | Customer Review Response | 3 | 36 |

All other ideas are archived in `archive/`.

## Directory Layout

```
agents/
├── active/
│   ├── 36-data-moat-history-agent/   # Phase 0: compounding data layer
│   ├── 27-price-tracking-deal-alert-bot/  # Phase 1: consumer product
│   ├── 11-public-data-aggregation-api/    # Phase 1: B2B API product
│   ├── 17-local-business-lead-gen-agent/  # Phase 2: lead engine
│   └── 30-customer-review-response-agent/ # Phase 3: first upsell
└── archive/                       # Inactive ideas (36 total)
db/                            # Shared Postgres schema
scrapers/                      # Reusable scraping infra
app/api/v1/                    # FastAPI skeleton
scripts/                       # Validation + tooling
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
# 1. Clone + install
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium

# 2. Configure
cp .env.example .env
# Fill in Supabase + API keys

# 3. Run validation
python3 scripts/validate-agents.py

# 4. Start API
uvicorn app.api.v1.main:app --reload --port 8000

# 5. Run first scraper
python3 scrapers/google-maps/scraper.py
```

## Roadmap

See [`ROADMAP.md`](./ROADMAP.md) for the phase plan and KPI gates.

## Tracker

See [`TRACKER.md`](./TRACKER.md) for progress, finance, and kill criteria.
