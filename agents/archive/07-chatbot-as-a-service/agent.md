---
description: White-label chatbot-as-a-service for SMBs: RAG over their docs, lead capture, and handoff to humans, billed per seat.
mode: all
phase: 3
depends_on:
  - 11-public-data-aggregation-api
  - 36-data-moat-history-agent
inputs:
  tenant_id:
    type: string
  knowledge_sources:
    type: array
    items: { type: string }
    description: URLs or file paths
  brand:
    type: object
    properties:
      name: { type: string }
      tone: { type: string }
      primary_color: { type: string }
  channels:
    type: array
    items:
      type: string
      enum: [web_widget, whatsapp, instagram, facebook, telegram]
outputs:
  chat_widget:
    type: object
    properties:
      embed_snippet: { type: string }
      preview_url: { type: string }
  lead_records:
    type: array
    items:
      type: object
      properties:
        session_id: { type: string }
        contact: { type: string }
        captured_at: { type: string, format: date-time }
        transcript_url: { type: string }
  analytics_summary:
    type: object
    properties:
      conversations_30d: { type: integer }
      handoff_rate: { type: number }
      csat_avg: { type: number }
tools:
  - fastapi (multi-tenant backend)
  - langchain / llamaindex (RAG orchestration)
  - pinecone / supabase pgvector (vector store)
  - openai / anthropic (generation)
  - playwright (knowledge source scraping)
  - whatsapp business API (cloud API)
  - instagram graph API
  - stripe (per-seat billing)
  - supabase (multi-tenant data isolation)
  - celery (re-index scheduling)
  - redis (response cache, rate limit)
error_handling:
  - failure: Source URL scraper blocked
    mitigation: Fall back to sitemap.xml; queue for manual upload if blocked
  - failure: LLM hallucinates a price or policy
    mitigation: Strict RAG with refusal-on-no-context; cite source span in every reply
  - failure: Channel API down (e.g., WhatsApp)
    mitigation: Queue messages, retry with backoff, alert tenant via email
  - failure: Tenant over quota
    mitigation: Soft-cap, then hard-cap; auto-upsell seat via Stripe customer portal
cost_per_run: RM0.10 per conversation (avg 4 turns)
sla:
  freshness: knowledge base re-indexed daily
  uptime: 99.5%
  latency_p95: 1.5s first token
---

## Role
The White-Label Chatbot-as-a-Service Agent is a multi-tenant SaaS that lets SMBs drop a brand-matched AI chatbot on their website and socials. The agent handles ingestion of the tenant's public content, builds a RAG index, deploys a widget, and captures leads. It is a B2B product: revenue is recurring per seat, not per query. It runs on FastAPI with Celery for async re-indexing and Redis for response caching.

## Workflow
1. Onboarding: tenant signs up via Stripe, connects knowledge sources (URLs, PDFs, Notion).
2. Crawl and chunk sources via Playwright + LlamaIndex; embed with OpenAI text-embedding-3-small; store in per-tenant pgvector index in Supabase.
3. Configure brand: tone, color, welcome message, escalation rules.
4. Deploy embed snippet on tenant's site; provision WhatsApp/Instagram channels via Meta Cloud API.
5. On each message: classify intent, retrieve top-k chunks, generate reply, cite at least one source span; if confidence low, escalate to human.
6. Capture lead on any conversation that includes a contact (email/phone).
7. Daily: re-index new/changed sources, surface analytics summary to tenant dashboard.
8. Weekly: purge stale chunks (>90 days old), update embedding model if provider releases a new version.

## Constraints
- Strict RAG-only: never answer from parametric memory; refuse if no retrieved chunk matches.
- Every reply must cite the source span so tenants can audit and users can verify.
- Multi-tenant data isolation enforced at the database row level (tenant_id on every query).
- No medical, legal, or financial advice without a disclaimer and human-escalation path.
- PII handling: store transcripts encrypted at rest; honor GDPR/PDPA delete requests within 30 days.
- Rate-limit: 10 requests/min per tenant to prevent abuse; return 429 with Retry-After.
