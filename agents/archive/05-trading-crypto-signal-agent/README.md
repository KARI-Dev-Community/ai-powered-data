# 05-trading-crypto-signal-agent

## Metrics

| Metric | Value |
|--------|-------|
| Risk | High (regulatory, strategy decay, market volatility) |
| Capital | RM600–RM2,000/month (exchange fees, API data, infra) |
| Success Probability | 40% (strategy-dependent, requires live track record) |
| Time to First RM | 60–120 days (first paying subscriber after proving track record) |
| Skills Needed | Quantitative finance, Python, backtesting, Telegram bot dev |

## Stack

| Layer | Choice | Why |
|-------|--------|-----|
| Data | CCXT (crypto) / Alpaca (equities) | Unified API for 100+ exchanges + equities |
| Backtesting | vectorbt / backtrader | Vectorised speed, event-driven precision |
| Indicators | TA-Lib + pandas / numpy | Battle-tested, extensive indicator library |
| Signal API | FastAPI | Low-latency signal serving, auth per tier |
| Delivery | Telegram Bot API | Subscriber-native, no extra app download |
| Billing | Lemon Squeezy | Tax-compliant SaaS billing, webhook-driven downgrades |
| Storage | Supabase + Redis | Signal history, subscriber ledger, real-time cache |
| Scheduling | Celery + Redis | Market-session-aligned signal generation |

## Execution Plan

| Week | Steps |
|------|-------|
| 1 | Define strategy registry (3–5 strategies). Backtest each on 2+ years out-of-sample data. Minimum 100 trades per strategy. |
| 2 | Set up CCXT + Alpaca connectors. Build FastAPI signal endpoint. Deploy Telegram bot with tier-based group/channel logic. |
| 3 | Integrate Lemon Squeezy for subscription billing. Wire webhook → subscriber tier → signal eligibility in Supabase. |
| 4 | Enable live paper-trading mode for 2 weeks. Log every signal + outcome. Validate latency <5s end-to-end. |
| 5–8 | Soft-launch free tier to build track record. Weekly re-rank strategies by rolling Sharpe; auto-pause any below threshold. |
| 9–12 | Open pro/VIP tiers. Publish public Sharpe/drawdown dashboard. Begin weekly performance email to subscribers. |

## Unit Economics

| Cost Item | RM/month | Revenue Item | RM/month |
|-----------|----------|--------------|----------|
| Exchange API + data feeds | 100–300 | Pro tier (RM50/month × subs) | 500–5,000 |
| Lemon Squeezy + Stripe fees | 50–150 | VIP tier (RM200/month × subs) | 200–2,000 |
| VPS + GPU (backtest + inference) | 200–500 | Free → paid conversion | 100–500 |
| Telegram ads / channel promotion | 50–200 | | |
| **Total** | **400–1,150** | **Total** | **800–7,500** |

## Known Failure Modes

| Failure | Mitigation |
|---------|-----------|
| Exchange API down | Round-robin across 3 exchanges; pause signals and notify subscribers |
| Strategy produces consecutive losing signals | Auto-pause after 5 stop-losses in a row; surface to operator |
| Telegram rate limit | Batch signals; use single channel post with grouped media |
| Subscriber payment fails | Lemon Squeezy webhook → downgrade to free tier within 24h |

## First Milestone

**Day 30:** 3 strategies live with 100+ trade backtests, paper-trading log populated, free Telegram channel active with 100+ members, and latency verified <5s end-to-end.
