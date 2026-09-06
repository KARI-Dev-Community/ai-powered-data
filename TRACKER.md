# Tracker — Progress, Finance, and Decision Log

The control layer for the ROI plan in [`ROADMAP.md`](./ROADMAP.md). If a number isn't recorded here, it didn't happen. Update at least weekly.

All figures in Malaysian Ringgit (RM).

---

## 1. Phase status board

| Phase | Status | Gate metric | Current | Target | Last updated |
|---|---|---|---|---|---|
| 0 — Foundation | ☐ Not started | Scored prospects in DB | 0 | 200 | |
| 1 — Quick wins (#27, #11) | ☐ Not started | Combined revenue | RM0 | RM100/mo | |
| 2 — Lead engine (#17) | ☐ Not started | Pilots converting | 0 | 2 | |
| 3 — Monetize (#30→#7→#19) | ☐ Not started | MRR | RM0 | RM4,000/mo | |
| 4 — Compound (#1, #10) | ☐ Not started | Total MRR | RM0 | RM8,000–12,000/mo | |

Status values: ☐ Not started · ◐ In progress · ☑ Done · ✗ Blocked

## 2. Active idea ledger

Only track ideas that are past "idea" stage. Drop anything you're not working on.

| Idea | Stage | Clients/Units | MRR | Hours spent | Next action |
|---|---|---|---|---|---|
| #27 deal bot | idea / build / live / dead | 0 | RM0 | 0 | |
| #11 data API | | 0 | RM0 | 0 | |
| #17 lead-gen | | — | — | 0 | |
| #30 review response | | 0 | RM0 | 0 | |
| #7 chatbot | | 0 | RM0 | 0 | |
| #19 bookkeeping | | 0 | RM0 | 0 | |
| #36 data moat (archive) | | — | — | 0 | start logging day 1 |

## 3. Finance ledger (monthly)

One row per month. Net = income − expenses. ROI = net ÷ total expenses.

| Month | Income | Expenses | Net | MRR | Churn | Notes |
|---|---|---|---|---|---|---|
| 2026-08 | RM0 | RM0 | RM0 | RM0 | — | Project start |

**Recurring expense budget (target):**

| Item | Budget |
|---|---|
| VPS | RM20–26/mo |
| Domain | RM40/yr |
| Email sending (SES/Resend) | RM5–15/mo |
| AI APIs (Anthropic + OpenAI, capped) | RM20–80/mo |
| Tooling/misc | RM0–40/mo |
| **Total** | **~RM60–200/mo** |

## 4. Kill criteria (decision rules)

Rules decided in advance so emotion doesn't drive them. If a trigger fires, act — don't renegotiate with yourself.

| Trigger | Rule |
|---|---|
| No replies after 200 personalized outreach emails | Change the offer or the target niche, not the volume |
| An idea at RM0 for 90 days after going live | Demote it; move the hours to the current top earner |
| 2 consecutive months of net-negative on an idea | Kill it or reprice; no third month |
| Hours on an idea exceed 2× its MRR contribution | Automate, delegate, or drop |
| A phase gate unmet 60 days past its target date | Stop adding; diagnose the bottleneck before proceeding |

## 5. Weekly time budget

Fixed weekly allocation; protects the plan from day-job bleed.

| Block | Hours/wk |
|---|---|
| Build (Phase 0–1 infra, agents) | 6 |
| Outreach & sales (Phase 2–3) | 4 |
| Client delivery & QA | 3 |
| Review: update this tracker + roadmap | 1 |
| **Total** | **~14** |

## 6. Decision log

Date · decision · rationale · revisit date.

| Date | Decision | Rationale | Revisit |
|---|---|---|---|
| 2026-08-29 | Project initialized; stack = TS/Python + Supabase + Lemon Squeezy | Matches TECHNICAL-SETUP.md | — |
