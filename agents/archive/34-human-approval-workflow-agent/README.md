# 34. Human-Approval Workflow Layer

Provides the human-approval layer for semi-autonomous agents — approval inbox, audit trail, one-click rollback. Realistic 2026 operations: 5 minutes per day of supervised autonomy.

## Metrics

| Attribute | Value |
|---|---|
| Risk | Low |
| Capital | RM500–RM1,500/mo |
| Success Probability | Medium-High |
| Time to First RM | 2–3 months |
| Skills Needed | Backend dev, workflow orchestration, auth/audit design, UX for approvals, Stripe billing |

## Why it's a gap

Agents can't safely hold payment credentials or make purchases (see gap analysis A2), so every serious agent deployment has a hidden manual step with no tooling. The market jumped from "manual" to "full autonomy" and skipped the layer in between — which is the layer that actually works. This agent wraps any agent workflow with a configurable approval gate, turning risky autonomous actions into safe supervised ones.

## Pricing model

- RM200–RM600/mo per agent wrapped (tiered by action volume)
- RM120/mo self-serve (single agent, email approvals only)
- RM300/mo team tier (up to 5 agents, Slack + web inbox, 2FA, dual-approve)
- Enterprise: audit-trail export + custom policy editor + SOC2 compliance (RM800+/mo)

## Stack

| Layer | Choice | Why |
|---|---|---|
| Action interception | FastAPI middleware | Wraps any API-based agent; hooks into action pipeline with zero client code changes |
| Approval inbox | Astro + Serverless functions | Web UI: action detail, payload diff, risk level, estimated cost, one-click approve/edit/reject |
| Notifications | Resend (email) + Slack webhook | Daily digest at 8am; urgent items sent immediately; critical via Twilio SMS |
| Audit log | Supabase (append-only) | Hash-chained entries: who approved what, when, with what diff; immutable for compliance |
| Auth | Clerk Auth | Per-user auth; team access control; 2FA for regulated tiers |
| Payments | Stripe | Tiered subscription; usage-based overages for high action volume |
| Rollback engine | Celery + Redis | Reversible actions: auto-rollback on failure; irreversible: manual override + post-hoc review |
| Policy engine | JSONB config per agent | Risk tiers × auto/hold/dual-approve per action type; version-controlled |
| Monitoring | 31-agent-ops-monitoring-agent | Alert on stuck approvals, policy violations, audit log integrity, worker crashes |
| Baseline data | 36-data-moat-history-agent | Historical approval patterns for autonomy-threshold proposals and anomaly detection |
| Human escalation | Slack + Twilio | On-call rotation for unapproved actions, rollback failures, audit corruption |

## Execution Plan

### Week 1 — Core interception + inbox
- Build FastAPI middleware: intercept action → check risk tier → route to approval queue or auto-approve
- Approval inbox (web): action, payload diff, risk level, estimated cost, one-click Approve/Edit/Reject
- Daily digest via Resend (email) + Slack webhook
- Risk tiers: read-only (auto), reversible (hold), irreversible (dual), regulated (always human)

### Week 2 — Audit trail + rollback
- Append-only audit log in Supabase with hash chain: entry_id + previous_hash + content_hash
- One-click rollback for reversible actions (payment refunds, email sends, calendar events)
- Post-hoc review for irreversible actions (audit trail only, no auto-rollback)
- Wrap your own #30 agent first — you need this for safe review posting

### Week 3 — Policy + self-serve
- Policy config UI: set risk tier per action type; auto / hold / dual-approve
- Astro self-serve: connect agent via API key; configure policies; view audit log
- Stripe checkout: RM120/mo self-serve, RM200/mo for 1 agent
- First client = you, wrapping your own #30 or #17 agent

### Month 2+ — Scale
- Add "learn from approvals" engine: after N consecutive approvals of same action class, propose raising autonomy (never auto-raise)
- Team tier: multiple approvers, approval chains, 2FA, Slack-based escalation policies
- Bundle with #30 (review response) + #17 (lead-gen) as reliability add-on (RM400–800/mo)
- White-label: agencies resell to their agent clients with custom branding + SOC2-ready audit export

## Unit Economics

| Item | Cost | Revenue |
|---|---|---|
| Storage + action logging | RM10–20/mo | — |
| Notifications per 100 actions | RM0.10 | — |
| 1 self-serve client @ RM120 | RM2 | RM120 |
| 1 client @ RM600 (5 agents) | RM10 | RM600 |
| 50 agencies @ RM300 (team resold) | RM500 | RM15,000 |
| **COGS per client** | **RM2–20/mo** | **RM120–600/mo** |
| Margin | 80–90% | — |
| Break-even | 2–3 self-serve clients | — |

## Known Failure Modes

| Failure | Mitigation |
|---|---|
| Urgent approval sits unreviewed | Escalate after 2h: SMS to on-call approver; auto-reject after 24h with audit log + client notification |
| Rollback fails mid-reversal | Atomic rollback: if reverse fails, halt; log in audit trail; page on-call via Slack + Twilio with manual override link |
| Audit log corrupted/tampered | Hash-chained entries; verify chain integrity every 15 min; halt approvals on mismatch; forensic recovery from S3 backup |
| Unapproved tier-2+ action requested under pressure | Refuse execution; log attempt; alert security team via SMS + Slack; never allow override without dual-approval |
| Too many low-risk actions flood inbox | Batch into daily digest; auto-approve read-only actions; only hold reversible+; configurable batch size per client |
| Approver unavailable (out of office) | Auto-route to backup approver; if no backup, auto-reject with audit log; never auto-approve regulated actions |

## First Milestone

**Day 40:** Action interception + approval inbox live (web + email + Slack), append-only audit log with hash chain, rollback working for 1 reversible action type (email send), self-serve dashboard live with 1 connected agent (#30 review-response), first paying client (RM120/mo self-serve).

---

This idea is implemented by [`agent.md`](./agent.md) in this folder.

### Activating the agent (copy, don't move)

To use this agent in Kilo, **copy** `agent.md` into `.kilo/agent/`:

```bash
mkdir -p .kilo/agent
cp 34-human-approval-workflow-agent/agent.md .kilo/agent/34-human-approval-workflow-agent.md
```
