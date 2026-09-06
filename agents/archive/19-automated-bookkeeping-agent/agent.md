---
description: >
  Bookkeeping and invoice agent for SMBs: categorises transactions,
  reconciles accounts, drafts invoices, and produces monthly reports.
mode: all
phase: 3
depends_on:
  - 11-public-data-aggregation-api
  - 34-human-approval-workflow-agent
inputs:
  client:
    type: object
    required: [client_id, accounting_software, oauth_token]
    properties:
      client_id: { type: string, pattern: '^[a-f0-9-]{36}$' }
      accounting_software: { type: string, enum: [xero, quickbooks, wave, myob] }
      oauth_token: { type: string, description: 'AES-256-GCM encrypted refresh token' }
      chart_of_accounts: { type: object, description: 'GL accounts + vendor/customer mappings' }
      industry_rules: { type: object, description: 'custom category rules, thresholds' }
      notification_emails: { type: array, items: { type: string, format: 'email' } }
  period:
    type: object
    required: [month, year]
    properties:
      month: { type: integer, minimum: 1, maximum: 12 }
      year: { type: integer, minimum: 2020 }
  raw_inputs:
    type: object
    properties:
      bank_statement_csv_url: { type: string, format: 'uri', nullable: true }
      ofx_url: { type: string, format: 'uri', nullable: true }
      receipt_urls: { type: array, items: { type: string, format: 'uri' } }
      prior_period_gl_export_url: { type: string, format: 'uri', nullable: true }
outputs:
  categorised_transactions:
    type: array
    items:
      type: object
      required: [txn_id, date, amount, payee, category, confidence, needs_review]
      properties:
        txn_id: { type: string }
        date: { type: string, format: date }
        amount: { type: number }
        payee: { type: string }
        category: { type: string }
        subcategory: { type: string, nullable: true }
        confidence: { type: number, minimum: 0, maximum: 1 }
        needs_review: { type: boolean }
        rule_version: { type: string }
        matched_bank_entry: { type: string, nullable: true }
  monthly_report_pdf:
    type: string
    description: 'Signed URL to branded PDF (P&L, balance sheet, cash-flow narrative)'
  invoices_drafted:
    type: array
    items:
      type: object
      properties:
        invoice_id: { type: string }
        client_name: { type: string }
        amount: { type: number }
        due_date: { type: string, format: date }
        line_items: { type: array }
        status: { type: string, enum: [draft, pending_approval, approved, posted] }
  reconciliation_status:
    type: object
    required: [matched, unmatched, variance, bank_feed_status]
    properties:
      matched: { type: integer }
      unmatched: { type: array, items: { type: string } }
      variance: { type: number }
      bank_feed_status: { type: string, enum: [connected, degraded, disconnected] }
  journal_entries:
    type: array
    items:
      type: object
      description: 'Adjustment entries awaiting client sign-off'
  close_checklist:
    type: object
    description: 'Items requiring human review before period close'
  audit_log_hash: { type: string, description: 'SHA-256 root hash of 7-year audit trail' }
tools:
  - xero / quickbooks / wave / myob REST API
  - aws textract (receipt OCR, multi-format)
  - anthropic claude sonnet 4 (categorisation + cash-flow narrative)
  - pandas + numpy (ledger reconciliation engine, variance analysis)
  - weasyprint 60+ (branded monthly report PDF, QR-signed)
  - resend (client delivery, review notifications, audit alerts)
  - supabase postgrest (7-year audit log, encrypted token vault, signed storage)
  - redis + celery 5 + flower (async OCR / categorisation task queue, monitoring)
  - sentry (error tracking)
  - pandas-profiling (anomaly detection pre-categorisation)
error_handling:
  - failure: Bank CSV/OFX schema drift (header rename, new columns)
    mitigation: Header fingerprint + schema-detect on first row; prompt operator for column mapping; version scraper per bank domain; retry with legacy parser
  - failure: Receipt OCR confidence below 0.60 or unsupported format
    mitigation: Route to 34-human-approval-workflow-agent review queue; block auto-categorisation; auto-retry with Textract AnalyzeExpense
  - failure: Xero/QuickBooks/Wave API rate limit or 5xx degradation
    mitigation: Batch writes via Celery rate-limited pool; exponential backoff with full jitter; circuit-breaker after 3 failures; queue for retry with DLQ alert
  - failure: Mis-categorised transaction detected by operator or anomaly model
    mitigation: Client feedback loop retrains category rules nightly; full audit trail in Supabase; monthly variance report triggers review ticket
cost_per_run: RM0.40 per client per period
  breakdown:
    claude_sonnet_5k_txns: RM0.18
    textract_ocr_50_receipts: RM0.10
    celery_worker_shared: RM0.07
    supabase_storage_log: RM0.05
sla:
  freshness: monthly close delivered by 5th business day of following month
  uptime: 99.5% (bound by accounting-software SLO + our API layer)
  latency_p95: 5 min for 500-txn month; 20 min for 5k-txn enterprise client
  retention: audit logs retained 7 years per IRBM / LNS requirements
  data_residency: all processing within ap-southeast-1 (AWS SG)
---

## Role
- Integrate with accounting APIs (Xero, QuickBooks, Wave, MYOB) via OAuth 2.0.
- Ingest bank statements (CSV/OFX) and receipts (Textract OCR), then categorise transactions using rule + history-aware LLM classification.
- Reconcile accounts with pandas/numpy variance analysis; flag mismatches for human review.
- Draft invoices, generate signed PDF reports (P&L, balance sheet, cash-flow narrative), and maintain a 7-year append-only audit trail.

## Workflow
1. Client onboard: connect accounting software, upload bank feed + receipts, confirm chart of accounts.
2. Ingest + OCR: parse CSV/OFX, run Textract on receipts, normalise to ledger schema.
3. Categorise + reconcile: Claude Sonnet batches 5k transactions; pandas matches against GL; variance report flags outliers.
4. Review gate: low-confidence categorisations and reconciliation mismatches queue to human approval.
5. Deliver: monthly PDF report via Resend; invoices drafted and posted on approval; audit log hashed and stored in Supabase.

## Constraints
- Never auto-post invoices or journal entries without explicit client approval; approval workflow is mandatory.
- Encrypt all OAuth refresh tokens (AES-256-GCM); never log raw credentials or PII.
- Retain audit logs 7 years per IRBM/LNS requirements; archive cold partitions to S3-compatible storage.
- Route OCR failures and API degradation to the human-approval workflow; never silently drop transactions.
