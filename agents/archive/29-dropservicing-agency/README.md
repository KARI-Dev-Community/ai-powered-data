# 29. Dropservicing Agency

Coordinates a dropservicing agency: clients, vendors, and delivery.

## Metrics

| Attribute | Value |
|---|---|
| Risk | Medium |
| Capital | RM1,000–RM3,000 |
| Success Probability | Medium |
| Time to First RM | 2–4 months |
| Skills Needed | Project management, vendor sourcing, QA, client communication, Stripe Connect, legal contracts |

## Why it's a gap

Dropservicing agencies are common on Fiverr/Upwork, but they lack process. Clients get inconsistent quality, missed deadlines, and no visibility. This agent is the "operating system" for a dropservicing agency: it handles vendor matching, milestone tracking, escrow, QC, and client communication — turning a chaotic freelance network into a repeatable service business. Precedent data from #36 informs vendor scoring; #17 feeds warm local business leads; #11 validates vendor background.

## Pricing model

- 15–25% margin on each order (client pays RM2,000, vendor gets RM1,500, agent keeps RM500)
- RM200–500 per order managed (for agencies that just want the platform, not vendor sourcing)
- Monthly retainer: RM1,500 (unlimited small tasks within scope)

## Stack

| Layer | Choice | Why |
|---|---|---|
| Order mgmt | Supabase | Track order lifecycle, vendor scores, client contracts |
| Vendor pool | Notion database + API | Structured vendor profiles, past work, ratings, capacity |
| Vendor background | 11-public-data-aggregation-api | Business registration, dispute history, review aggregation |
| Lead intake | 17-local-business-lead-gen-agent | Feeds warm leads from local business pipeline |
| Precedent data | 36-data-moat-history-agent | Historical order outcomes, vendor performance, pricing benchmarks |
| Escrow/payments | Stripe Connect | Hold client funds; release to vendor on approval; take margin |
| Communication | Twilio SMS + Resend email | Notify client + vendor on milestone updates |
| SOW generation | Anthropic Claude | Auto-generate scope of work from intake form |
| PDF contracts | pdf-lib | Generate branded order contracts and invoices |
| Scheduling | Celery + Redis | Reminders, deadline tracking, escalation timers |
| Auth | Clerk | Separate client + vendor login portals |

## Execution Plan

### Week 1 — Order + vendor system
- Build order lifecycle DB: created → vendor matched → SOW signed → in progress → QC → approved → paid
- Recruit 5 initial vendors across 2 service types (graphic design, copywriting)
- Build intake form → auto-generate SOW via Claude
- Set up Stripe Connect for escrow
- Integrate 11 for vendor background checks and 17 for lead feed

### Week 2 — QC + tracking
- Add milestone checkpoints: draft review, revision round, final approval
- Build QC checklist: does it meet brief? On brand? Error-free?
- Set up vendor scorecard: rating, on-time rate, revision count, client feedback
- Connect to 17 for lead intake (if targeting local businesses)

### Week 3 — First order
- Manual-first: you handle sourcing + QA; agent handles everything else
- Run 3 orders for friends/connections at cost; collect feedback
- Refine SOW templates and QC checklist
- First paying order = first RM (margin)

### Month 2+ — Scale
- Grow vendor pool to 20 across 5 service categories
- Add auto-vendor-matching: match order to best-fit vendor from pool
- Launch monthly retainer option for recurring clients (social posts, monthly copy)
- Build vendor marketplace: let other agencies onboard their vendors to your platform

## Unit Economics

| Item | Cost | Revenue |
|---|---|---|
| Vendor payout | RM1,200 (for a RM1,500 order) | — |
| Stripe + platform fees | RM80 | — |
| AI (SOW + QC) per order | RM3–12 | — |
| Platform per order | RM1,293–1,292 | RM500 |
| 10 orders/mo retainer | RM0 | RM1,500 |
| **COGS per order** | **RM1,283–1,304** | **RM1,500** (~13% margin) or RM500 platform fee (40–50% margin) |
| **Break-even** | **6–8 orders/mo at 20% margin** | — |

## Known Failure Modes

| Failure | Mitigation |
|---|---|
| Vendor misses deadline | Auto-notify client; offer expedited replacement vendor; hold 20% until next milestone |
| Scope creep mid-order | Freeze order; require signed scope change + revised quote before continuing |
| Quality doesn't match vendor's portfolio | QC checklist before client delivery; 1 free revision round; 3rd strike = refund |
| Payment dispute | Hold escrow; gather evidence (deliverables + chat logs); route to dispute manager within 24h |
| Vendor pool too small | Grow vendors by 3/week via outreach; maintain backup vendors for each category |
| Vendor background check fails | Re-run via 11-public-data-aggregation-api; suspend vendor until cleared |

## First Milestone

**Day 35:** Order lifecycle system live, 5 vetted vendors onboarded, Stripe Connect escrow working, first 3 test orders completed (friends at cost), 1 paying client order (RM1,500 project, RM300 margin).

---

This idea is implemented by [`agent.md`](./agent.md) in this folder.

### Activating the agent (copy, don't move)

To use this agent in Kilo, **copy** `agent.md` into `.kilo/agent/` — do not move it, so this folder keeps its own copy:

```bash
mkdir -p .kilo/agent
cp 29-dropservicing-agency/agent.md .kilo/agent/29-dropservicing-agency.md
```
