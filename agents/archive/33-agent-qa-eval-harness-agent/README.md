# 33. Agent QA / Eval-Harness as a Product

Runs automated quality evaluation on LLM/agent outputs — factuality, format, links, tone — and gates bad output before it ships. The "no-code crowd can't build evals" moat.

## Metrics

| Attribute | Value |
|---|---|
| Risk | Low |
| Capital | RM200–RM800/mo |
| Success Probability | Medium-High |
| Time to First RM | 2–3 months |
| Skills Needed | Backend dev, LLM eval techniques, deterministic testing, data pipelines, Stripe billing |

## Why it's a gap

Unreviewed LLM output = hallucinated facts, broken links, off-brand tone, and platform penalties. Content-agent operators (#1, #8, #12, #23) know this and have no QA layer. Dev-heavy operators have evals; the prompt-only majority doesn't. This is the automated quality gate that every agent pipeline needs: deterministic checks + LLM-judge scoring, with regression detection and hold-for-review on failure.

## Pricing model

- RM400–RM1,200/mo per content pipeline evaluated (scheduled or per-batch pricing)
- RM1,000–RM2,000 setup fee for rubric definition + first eval suite
- Per-eval usage pricing for high-volume publishers (RM0.01–0.05 per eval)
- Bundle with #31 monitoring as "Agent Reliability Stack" retainer (RM1,000–1,800/mo)

## Stack

| Layer | Choice | Why |
|---|---|---|
| Eval scheduler | Celery + Redis | Run checks per-batch or on schedule; distributed across workers for volume |
| Deterministic checks | Python (regex + jsonschema + linkchecker + pii-scan) | Format, schema, link liveness — fast and exact; run before LLM judge |
| LLM judge | OpenAI GPT-4o + Anthropic Claude Haiku | Different model from generator to avoid self-preference bias; dual-judge consensus |
| Storage | Supabase Postgres | Eval results, rubric versions, quality trends, immutable audit log |
| API | FastAPI | `/v1/eval/batch`, `/v1/eval/:id/results`, `/v1/quality/trend` |
| Notifications | Resend + Slack webhook | Regression alerts, weekly quality reports, quarantine notifications |
| Billing | Stripe | Tiered by eval volume; usage-based overages for high-volume publishers |
| Baseline data | 36-data-moat-history-agent | Historical quality baselines for regression detection |
| Health monitoring | 31-agent-ops-monitoring-agent | Alert on failed eval runs, schedule drift, Celery worker crashes |
| Human approval | 34-human-approval-workflow-agent | Route high-stakes gated content to human reviewer before release |

## Execution Plan

### Week 1 — Core eval engine
- Build deterministic checks: schema validator (jsonschema), regex format checks, link liveness checker, PII scanner
- Build LLM judge interface: same prompt to GPT-4o and Claude; score 1–10 for factuality, tone, format
- Define your first eval rubric: use #1 blog agent as target (factuality = citations present; format = markdown headings; tone = brand voice)
- Store results in Supabase with immutable log

### Week 2 — Regression detection + gating
- Build regression detector: compare latest batch vs. previous good run; flag > 15% drop in avg score
- On failure: quarantine output, send hold-for-review email to client via Resend
- Auto-route to #34 (human approval) for gated content review
- First 3 test runs on your own #1 agent — capture fail cases as demo

### Week 3 — Client product + pricing
- Astro dashboard: connect pipeline, define rubric, view scores, configure alerting
- Pricing: RM400/mo per pipeline (100 evals/day); RM1,000 setup for custom rubric
- First client = content agency running #8 YouTube agent (they're getting demonetized for bad scripts)
- Ship with #31 monitoring: alert when eval run fails

### Month 2+ — Scale
- Add tone/brand-voice judging: fine-tune judge prompts per client brand guidelines
- Build eval-template library: "Blog Post QA," "YouTube Script QA," "Email Sequence QA"
- Bundle with #31 + #34 as "Agent Reliability Stack" retainer (RM1,500/mo for 3 agents)
- Publish benchmark-style quality reports as inbound content (feeds #1)

## Unit Economics

| Item | Cost | Revenue |
|---|---|---|
| Deterministic checks per 100 evals | RM0.10 | — |
| LLM judge per 100 evals | RM0.50–2.00 | — |
| Infra (Celery + storage) | RM10–20/mo | — |
| 1 client @ RM400/mo | RM2–5/mo | RM400 |
| 1 high-volume client @ RM1,200/mo | RM20–50/mo | RM1,200 |
| 10 clients (agency bundle) @ RM1,200 | RM200 | RM12,000 |
| **COGS per client** | **RM5–100/mo** | **RM400–1,200/mo** |
| Margin | 75–90% | — |
| Break-even | 2–3 clients | — |

## Known Failure Modes

| Failure | Mitigation |
|---|---|
| Judge is inconsistent (score varies per run) | Use 2 judges (GPT-4o + Claude); take average/majority; require consensus before gating |
| Self-preference bias (judge matches generator) | Always use a different model or heavily different prompt for judge; verify model ID in metadata |
| Regression alert on random noise | Require 2 consecutive runs below threshold before alerting; use moving average of 3 runs |
| False gate (good content quarantined) | Allow client to override quarantine with 1 click; log override for rubric tuning; track false-gate rate |
| PII in eval output | Redact PII before logging; store full output only in encrypted, time-limited S3 vault |
| Judge API outage | Fall back to rule-based heuristic judge; flag as reduced-confidence assessment; alert ops via #31 |

## First Milestone

**Day 30:** Eval engine live (deterministic + LLM judge), regression detection working, hold-for-review flow with Resend notifications, rubric defined for #1 blog agent, 2 client pipelines onboarded (RM800 total setup), first quality trend report delivered.

---

This idea is implemented by [`agent.md`](./agent.md) in this folder.

### Activating the agent (copy, don't move)

To use this agent in Kilo, **copy** `agent.md` into `.kilo/agent/`:

```bash
mkdir -p .kilo/agent
cp 33-agent-qa-eval-harness-agent/agent.md .kilo/agent/33-agent-qa-eval-harness-agent.md
```
