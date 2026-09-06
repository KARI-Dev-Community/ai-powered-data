# 31. Agent-Ops Monitoring as a Service

Monitors, alerts, and reports on the health, drift, and cost of other people's production AI agents. Sells the "reliability layer" that every agent builder (ideas #1–#30) needs but almost nobody provides.

## Metrics

| Attribute | Value |
|---|---|
| Risk | Low |
| Capital | RM600–RM1,500/mo |
| Success Probability | Medium-High |
| Time to First RM | 1–2 months |
| Skills Needed | Backend dev, API design, observability tooling, LLM eval techniques, Stripe billing |

## Why it's a gap

Every idea in this repo that reaches production has the same unmet needs: uptime checks, output-drift detection, cost-anomaly alerts, and client-facing health reports. Agent builders are prompt-talented but ops-weak. You provide the reliability layer they can't build themselves. This agent also monitors #33 (QA harness) and routes failures from #34 (approval layer).

## Pricing model

- RM400–RM1,200/mo per client agent monitored (tiered by probe frequency + alert channels)
- RM200/mo self-serve tier (single agent, email alerts only)
- White-label to agencies running agents for SMBs (pairs with #29 dropservicing)
- RM500/mo add-on: weekly report PDF sent to client's clients (for agencies to resell)

## Stack

| Layer | Choice | Why |
|---|---|---|
| Probes | httpx + Playwright | HTTP checks for API endpoints; browser for UI-based agent dashboards |
| Storage | Supabase Postgres | Store probe history, baselines, anomaly classifications, audit logs |
| Scheduling | Celery + Redis | Run probes every 5–60 min per agent; configurable per tier; distributed across workers |
| LLM judge | OpenAI GPT-4o + Anthropic Claude | Cross-model evaluation to avoid self-preference bias; majority voting for consistency |
| Alerts | Resend (email) + Slack webhook + Twilio (SMS) | Multi-channel; SMS for critical only; Slack for team inbox |
| Dashboards | Grafana | Client-facing uptime + cost graphs; embeddable white-label panels |
| Billing | Stripe | Tiered subscription; usage-based overages for high-volume probe clients |
| Report gen | Celery + Supabase | Weekly roll-up reports with SLA scorecards; S3 archival for compliance |
| Baseline data | 36-data-moat-history-agent | Historical performance baselines for drift detection and trend analysis |

## Execution Plan

### Week 1 — Probe engine + first target
- Build probe scheduler: configurable frequency per agent (5–60 min)
- Implement uptime, latency, error-rate collection (httpx)
- Instrument your own #17 agent as the first monitored target (dogfooding)
- Set up baseline: first 24h of "normal" data stored in Supabase

### Week 2 — Cost + drift detection
- Track token/API spend per probe cycle; integrate with OpenAI/Anthropic usage APIs
- Build LLM-as-judge: same prompt to GPT-4o and Claude; compare outputs for drift using cosine similarity
- Cost-anomaly detection: spike > 3× baseline, runaway retries, loop detection
- Alert engine: severity tiers (critical/warning/info); email + Slack

### Week 3 — Client self-serve + billing
- Astro frontend: connect your agent via API key, set schedule + cost cap + alert channels
- Stripe tier: RM200/mo self-serve (1 agent, email only); RM600/mo pro (5 agents, all channels)
- First 3 clients free for 30 days (founder friends building agents)
- Weekly report: uptime %, avg latency, cost/run, drift score, SLA scorecard

### Month 2+ — Scale
- Add support for #33 (QA harness) — monitor eval pass rates as a proxy for quality health
- Add support for #34 (approval layer) — alert on stuck approvals > 48h
- White-label dashboard for agencies managing agents for SMBs
- Package: "Agent Reliability Stack" = #31 + #33 + #34 bundled retainer

## Unit Economics

| Item | Cost | Revenue |
|---|---|---|
| Probing cost per agent | RM10–30/mo (VPS + API calls) | — |
| LLM judge per 1k evaluations | RM5–15 | — |
| Stripe fees | ~3% | — |
| 1 self-serve client @ RM200 | RM15 | RM200 |
| 1 pro client @ RM600 | RM40 | RM600 |
| 10 agents monitored (agency) @ RM1,200 | RM150 | RM1,200 |
| **COGS per client** | **RM15–100/mo** | **RM200–1,200/mo** |
| Margin | 80–90% | — |
| Break-even | 3–4 self-serve clients | — |

## Known Failure Modes

| Failure | Mitigation |
|---|---|
| False alert fatigue | Tune thresholds after 3 false positives; log all sensitivity adjustments in compliance DB |
| Probe itself causes cost overrun | Hard cap on probe frequency; halt probes at cost cap; alert before 80% of budget consumed |
| Platform change breaks baseline | Retrain baseline on "known good" runs; version baseline + require manual re-baseline on significant model changes |
| Client agent goes dark (no response) | Retry with backoff; if 3 consecutive timeouts, mark down + page on-call; don't alert after-hours for planned downtime |
| PII in failing samples | Never log full payloads; redact PII in alert; store only in encrypted, time-limited S3 vault |
| LLM judge API outage | Fall back to rule-based heuristic judge (regex, schema, latency heuristics); flag as reduced-confidence assessment |

## First Milestone

**Day 45:** Probe engine live (uptime + latency + cost tracking), 1 LLM judge for drift detection, cost-anomaly alerting working, 1 self-serve client dashboard live, first 3 beta clients onboarded (free), first RM200/month client signed up.

---

This idea is implemented by [`agent.md`](./agent.md) in this folder.

### Activating the agent (copy, don't move)

To use this agent in Kilo, **copy** `agent.md` into `.kilo/agent/`:

```bash
mkdir -p .kilo/agent
cp 31-agent-ops-monitoring-agent/agent.md .kilo/agent/31-agent-ops-monitoring-agent.md
```
