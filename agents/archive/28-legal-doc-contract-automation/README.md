# 28. Legal Doc / Contract-Drafting Automation

Drafts legal documents and contracts from templates, with lawyer review required.

## Metrics

| Attribute | Value |
|---|---|
| Risk | Medium-High |
| Capital | RM2,000–RM5,000 |
| Success Probability | Medium |
| Time to First RM | 3–6 months |
| Skills Needed | Legal domain knowledge/partnership, prompt engineering, compliance review, web dev, PDF generation, e-signature integration |

## Why it's a gap

Small businesses and startups waste RM500–2,000 per contract on lawyers who use templates anyway. The real value is not replacing lawyers but handling the 80% of routine contracts (NDAs, SaaS terms, service agreements) that can be auto-drafted from a template library, then reviewed by a lawyer only when red-flag clauses appear. The agent routes complex docs to a network of partner lawyers, creating a two-sided marketplace. Precedent data from #36 informs risk scoring; #32 catches compliance drift before drafts are issued.

## Pricing model

- RM99–299 one-time per document (template-based, lawyer-reviewed flag)
- RM800–1,500/mo subscription for startups (10 docs + unlimited NDAs)
- RM200–500 per lawyer-routed review (agent handles intake, lawyer charges on top)

## Stack

| Layer | Choice | Why |
|---|---|---|
| Intake | Typeform + Astro | Guided Q&A; conditional logic per doc type |
| AI | Anthropic Claude 3.5 Sonnet | Best-in-class contract drafting, clause extraction |
| Compliance | 32-compliance-tos-checker-agent | Automated ToS and regulatory checks before draft |
| Templates | Versioned Markdown library | Each jurisdiction + doc type = one template; tagged with version |
| Precedent | 36-data-moat-history-agent | Historical clause performance and dispute data |
| Storage | Supabase | Templates, drafts, client data encrypted at rest |
| PDF/E-sign | pdf-lib + HelloSign API | Signed deliverables and audit trail |
| Review routing | Clerk auth + Notion API | Partner lawyers see assigned reviews in a dashboard |
| Payments | Stripe | Per-doc or subscription; split payments to lawyers |
| Notifications | Resend | Draft ready, lawyer review assigned, client sign-off |
| Lead intake | 17-local-business-lead-gen-agent | Feeds warm leads from local business pipeline |

## Execution Plan

### Week 1 — Template library + intake
- Build intake form for 2 doc types: NDA (mutual) and SaaS Terms of Service
- Write 2 templates with clause placeholders; store in Supabase with version tags
- Build Astro frontend for intake → draft → review flow
- Connect 32 for compliance pre-checks and 36 for precedent queries
- Connect Stripe for per-doc pricing

### Week 2 — Draft generation + review flags
- Claude generates doc from template + intake answers
- Run automated checks: clause conflicts, missing definitions, jurisdiction mismatch
- Flag docs needing lawyer review (regulated clauses, unusual terms)
- Set up review routing: flagged docs → partner lawyer dashboard
- Integrate pdf-lib for PDF export and HelloSign for e-signature

### Week 3 — Lawyer network + pilot
- Recruit 3 part-time contract lawyers via local bar community
- Run 5 free pilots with startup founders; collect feedback
- Refine templates based on lawyer suggestions
- First paid doc = first RM

### Month 2+ — Scale
- Add 3 more doc types per month (employment, IP assignment, vendor agreement)
- Launch subscription tier for startups (RM800/mo, 10 docs)
- Build lawyer rating system; grow network to 10 partners
- Add precedent-driven risk scoring per clause

## Unit Economics

| Item | Cost | Revenue |
|---|---|---|
| Claude token per doc | RM0.50–2.00 | — |
| Template storage + infra | RM20–50/mo | — |
| 10 docs/mo (startup plan) | RM5–20 | RM800 |
| Lawyer-routed review | RM5–10 | RM200–500 |
| **COGS per doc** | **RM0.70–2.50** | **RM99–299** |
| Margin | 90%+ | — |

## Known Failure Modes

| Failure | Mitigation |
|---|---|
| Doc generates wrong clause for jurisdiction | Tag every template with jurisdiction; enforce jurisdiction filter at intake |
| Lawyer review backlog | Set max queue (5 per lawyer); auto-escalate if > 48h pending |
| Client expects full legal advice | Clear TOS: "not legal advice, lawyer review required"; require checkbox on intake |
| Template drift (law changes) | Quarterly review; version-control all templates; flag outdated docs |
| PII leak | Encrypt all client data; never log intake answers; redact in reports |
| Compliance miss | Run 32-compliance-tos-checker-agent before draft delivery |

## First Milestone

**Day 45:** NDA + SaaS Terms templates live, 3 partner lawyers onboarded, intake form + Stripe checkout live, 3 free pilot docs generated with lawyer feedback, 1 paying startup customer (RM99 for NDA).

---

This idea is implemented by [`agent.md`](./agent.md) in this folder.

### Activating the agent (copy, don't move)

To use this agent in Kilo, **copy** `agent.md` into `.kilo/agent/` — do not move it, so this folder keeps its own copy:

```bash
mkdir -p .kilo/agent
cp 28-legal-doc-contract-automation/agent.md .kilo/agent/28-legal-doc-contract-automation.md
```
