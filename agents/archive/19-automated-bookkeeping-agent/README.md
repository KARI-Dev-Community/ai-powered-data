# 19. Automated bookkeeping/invoice agent

## Metrics

| Metric | Value |
| --- | --- |
| Risk | Medium |
| Capital Required | RM800–RM2,000 |
| Success Probability | Medium (60–75% with 3+ clients in month 3) |
| Time to First RM | 2–4 months |
| Skills Needed | Accounting basics, Xero/QuickBooks API integration, backend dev (Python/Celery), OCR pipeline ops |

## Stack

| Layer | Choice | Why |
| --- | --- | --- |
| Accounting APIs | Xero / QuickBooks / Wave / MYOB | Ubiquitous SMB choices; OAuth 2.0 standard |
| OCR | AWS Textract AnalyzeExpense | Multi-format, table-aware, handles rotated receipts |
| Categorisation | Anthropic Claude Sonnet 4 | Rule + history aware; 5k-txn batch within context |
| Reconciliation | pandas + numpy | Fast ledger matching, variance detection |
| Report PDF | WeasyPrint 60+ | Branded monthly report, QR-signed, repeatable |
| Delivery | Resend | Client-ready email with review links |
| Audit | Supabase (PostgREST) | 7-year audit log, encrypted token vault, signed storage |
| Queue | Redis + Celery 5 + Flower | Async OCR / categorisation, retry, DLQ, monitoring |
| Tracking | Sentry | Error tracking across API boundaries |

## Execution Plan

| Week | Step |
| --- | --- |
| 1 | Xero/QuickBooks OAuth 2.0 flow + transaction pull; store encrypted refresh tokens in Supabase Vault |
| 2 | OCR + categorisation pipeline; validate on 3 sample SMB clients; tune confidence threshold |
| 3 | Reconciliation engine + unmatched queue; integrate 11-public-data-aggregation-api for industry benchmarks |
| 4 | Draft invoice flow with 34-human-approval-workflow-agent gate; Resend approval emails |
| 5 | Produce branded monthly PDF (P&L, balance sheet, cash-flow); Resend delivery; archive to Supabase |
| 6–10 | Onboard 5–10 paying SMB clients; refine per-industry rules; tune confidence thresholds |
| 11–12 | Add 36-data-moat-history-agent for industry benchmarking; IRBM-ready accountant pack export |

## Unit Economics

| Item | Cost (RM) | Revenue (RM) |
| --- | --- |
| Claude Sonnet 5k txns | 0.18/client/mo | – |
| Textract OCR 50 receipts | 0.10/client/mo | – |
| Celery shared worker | 0.07/client/mo | – |
| Supabase storage + API | 0.05/client/mo | – |
| Resend + infra | 0.08/client/mo | – |
| **Variable cost per client** | **0.48/client/mo** | – |
| Per-client monthly fee | – | 200–800 |
| One-time setup fee | – | 500 |
| Gross margin per client | – | ~85% |
| Break-even | 5 paying clients in month 3 | – |

## Known Failure Modes

| Failure | Mitigation |
| --- | --- |
| Bank CSV/OFX schema drift | Header fingerprint + schema-detect on first row; prompt operator for column mapping; version scraper per bank domain; retry with legacy parser |
| Receipt OCR confidence < 0.60 | Route to 34-human-approval-workflow-agent review queue; block auto-categorisation; auto-retry with Textract AnalyzeExpense |
| Accounting API rate limit / 5xx | Batch writes via Celery rate-limited pool; exponential backoff with full jitter; circuit-breaker after 3 failures; DLQ + alert |
| Mis-categorised transaction | Client feedback loop retrains category rules nightly; full audit trail in Supabase; monthly variance >5% triggers review ticket |

## First Milestone

**Day 60:** 5 paying clients, first month-end close delivered on time, RM1,500 MRR, zero manual overrides on >80% of transactions.
