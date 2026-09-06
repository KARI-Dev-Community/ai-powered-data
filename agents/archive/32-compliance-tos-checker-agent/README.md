# 32. Compliance/ToS-Checker Agent for Agent Builders

Audits automated workflows and agent products for platform ToS violations, regulatory exposure, and ban risk. The meta-gap: paid by the same crowd building ideas #1–#30 in this repo.

## Metrics

| Attribute | Value |
|---|---|
| Risk | Low |
| Capital | RM0–RM400 |
| Success Probability | Medium-High |
| Time to First RM | 1–2 months |
| Skills Needed | Web scraping, API/ToS analysis, regulatory awareness, report writing, Stripe billing |

## Why it's a gap

7 of the 30 ideas in this repo depend on platforms (Google, Yelp, Etsy, Amazon, YouTube) that actively detect and ban automation. Builders discover this *after* their revenue dies overnight. Nobody sells pre-flight risk audits for agent workflows. The same compliance check can be packaged as a product: audit your workflow before you build, not after you get banned.

## Pricing model

- RM600–RM2,000 one-time audit per workflow (detailed report + remediation list)
- RM200–RM400/mo ongoing monitoring (ToS pages change silently; re-audit on change)
- Volume deal for agencies: audit their entire client portfolio quarterly (RM500/audit)
- White-label report: agencies resell as their own compliance review (RM300/audit + RM100/mo monitoring)

## Stack

| Layer | Choice | Why |
|---|---|---|
| ToS fetch | httpx + Playwright | Most ToS pages are static; some load JS-heavy with bot detection |
| ToS parsing | Anthropic Claude | Extract key clauses (scraping, automation, rate limits, resale) from raw text |
| Analysis engine | OpenAI GPT-4o + rule-based matcher | Combine LLM clause analysis with hardcoded rule checks for speed and consistency |
| Storage | Supabase | Store ToS versions, audit reports, client workflows, change history |
| Workflow ingest | Code upload + URL import | Accept GitHub repo link or direct file upload; validate before processing |
| Notifications | Resend | Audit complete, re-audit due, new ToS version detected for client workflows |
| Billing | Stripe | One-time audits + recurring monitoring subscriptions; usage metering |
| Baseline data | 36-data-moat-history-agent | Historical ToS version archive for change detection and compliance trend analysis |
| Monitoring | 31-agent-ops-monitoring-agent | Alert on failed audit runs, ToS fetch failures, SLA breaches |

## Execution Plan

### Week 1 — Audit engine + first targets
- Build ToS fetcher: download + cache terms for Google, Yelp, Etsy, Amazon, Facebook, YouTube
- Parse ToS with Claude: extract scraping, automation, rate-limit, resale clauses
- Build rule engine: map workflow actions to ToS risks (e.g., "scrape > 100 pages/hr" → rate-limit risk)
- Audit your own repo's ideas first (audit 5 workflows as portfolio content)

### Week 2 — Report generator + landing page
- Generate structured risk report: violation, evidence (quoted clause), likelihood, fix
- Astro landing page: upload workflow + description, get instant risk summary
- Price: free instant summary (3 flags); RM600 for full audit (all flags + remediation)
- Publish 2 sanitized sample audits as lead magnets

### Week 3 — First paying client
- Target: agencies white-labeling agents (#29) — they carry ToS liability for every client
- Offer audit + monitoring bundle: RM600 audit + RM200/mo ToS-change alerts
- First agent builder (idea #1 or #8 from this repo) audited = first RM
- Set up Stripe billing: one-time audit + recurring monitoring

### Month 2+ — Scale
- Add regulatory database: CAN-SPAM, GDPR, CCPA, FTC endorsement rules, financial-licensing triggers
- Build API: agencies integrate compliance check into their workflow builder
- Launch "safe-to-build" certification badge for audited agents (marketing for #1–#30 builders)
- Volume tier: RM3,000/mo for unlimited audits of up to 10 client workflows

## Unit Economics

| Item | Cost | Revenue |
|---|---|---|
| ToS fetch + Claude parse per audit | RM0.20–0.80 | — |
| Storage + infra | RM10–20/mo | — |
| 1 full audit (1 platform) | RM0.50 | RM600 |
| 1 audit + monitoring bundle | RM2–5/mo | RM800 upfront + RM200/mo |
| 10 audits/mo (agency tier) | RM20 | RM3,000 |
| **COGS per audit** | **RM0.50–2.00** | **RM600–2,000** |
| Margin | 85%+ | — |
| Break-even | 1 audit | — |

## Known Failure Modes

| Failure | Mitigation |
|---|---|
| ToS page unavailable (JS block) | Fallback to ToS archive or API terms; flag as "unverifiable" in report; alert ops within 24h |
| False positive flag | Log for human review; suppress similar flags for 7 days; tune classifier thresholds based on feedback |
| ToS changes without notice | Monitoring tier: daily check + diff against cached version; alert client within 24h of change |
| Jurisdiction unknown | Default to most restrictive known regulation (GDPR); recommend client add jurisdiction to profile |
| Platform sues for scraping ToS | Only fetch ToS publicly; never automate scraping of platform data; cite fair-use for ToS access; host on Malaysian infrastructure |
| Audit API overload | Rate-limit incoming requests; queue batch audits; degrade to cached ToS during peak load |

## First Milestone

**Day 14:** 5 platform ToS parsed + cached, rule engine maps 10 workflow actions to risks, 3 sample audits generated (sanitized), landing page live with instant risk summary, 1 paying audit client (RM600).

---

This idea is implemented by [`agent.md`](./agent.md) in this folder.

### Activating the agent (copy, don't move)

To use this agent in Kilo, **copy** `agent.md` into `.kilo/agent/`:

```bash
mkdir -p .kilo/agent
cp 32-compliance-tos-checker-agent/agent.md .kilo/agent/32-compliance-tos-checker-agent.md
```
