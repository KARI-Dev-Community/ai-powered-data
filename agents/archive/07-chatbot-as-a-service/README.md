# 07-chatbot-as-a-service

## Metrics

| Metric | Value |
|--------|-------|
| Risk | Low–Medium (churn, LLM cost, support burden) |
| Capital | RM800–RM2,000/month (LLM inference, hosting, Stripe fees) |
| Success Probability | 60% (SMB willingness to pay proven; execution-dependent) |
| Time to First RM | 30–60 days (first paying seat after trial) |
| Skills Needed | FastAPI, RAG (LangChain/LlamaIndex), Supabase, Stripe, frontend embed |

## Stack

| Layer | Choice | Why |
|-------|--------|-----|
| Backend | FastAPI | Async, multi-tenant, OpenAPI-native |
| RAG | LangChain / LlamaIndex | Orchestration, chunking, retrieval tuning |
| Vector Store | Pinecone (managed) or Supabase pgvector | Managed scale vs cost efficiency |
| Embeddings | OpenAI text-embedding-3-small | High quality, low cost, fast |
| Generation | OpenAI GPT-4o-mini / Anthropic Claude Haiku | Speed + cost for chat; Haiku for safety |
| Channels | WhatsApp Cloud API + Instagram Graph API | SMB-native channels, no app download |
| Billing | Stripe (per-seat) | prorations, customer portal, tax auto-calc |
| Storage | Supabase (row-level multi-tenant) | PII encryption, PDPA-ready, audit log |
| Scheduling | Celery + Redis | Daily re-index, stale-chunk purge |

## Execution Plan

| Week | Steps |
|------|-------|
| 1 | Scaffold FastAPI multi-tenant backend. Set up Supabase with tenant_id RLS. Integrate Stripe checkout + webhook. |
| 2 | Build RAG pipeline: Playwright crawl → LlamaIndex chunk → OpenAI embed → pgvector store. Test with 1 tenant's docs. |
| 3 | Deploy web widget embed snippet. Provision WhatsApp + Instagram channels via Meta Cloud API. Test message → reply flow. |
| 4 | Soft-launch to 5 beta tenants (free). Collect CSAT. Calibrate refusal-on-no-context and citation formatting. |
| 5–8 | Open paid seats. Implement daily re-index cron. Build tenant dashboard (conversations, handoff rate, CSAT). |
| 9–12 | Add human-handoff escalation path (Slack/WhatsApp to agent). Introduce usage-based soft cap + auto-upsell via Stripe. |

## Unit Economics

| Cost Item | RM/month | Revenue Item | RM/month |
|-----------|----------|--------------|----------|
| OpenAI / Anthropic API | 300–800 | Seat subscriptions (RM50–200/seat) | 1,000–5,000 |
| Pinecone / Supabase | 100–300 | Setup fees | 0–500 |
| VPS + Redis + Celery | 150–300 | | |
| Stripe fees (2.9% + RM2) | variable | | |
| **Total** | **550–1,400** | **Total** | **1,000–5,500** |

## Known Failure Modes

| Failure | Mitigation |
|---------|-----------|
| Source URL scraper blocked | Fall back to sitemap.xml; queue for manual upload if blocked |
| LLM hallucinates a price or policy | Strict RAG with refusal-on-no-context; cite source span in every reply |
| Channel API down (e.g., WhatsApp) | Queue messages, retry with backoff, alert tenant via email |
| Tenant over quota | Soft-cap, then hard-cap; auto-upsell seat via Stripe customer portal |

## First Milestone

**Day 30:** 5 beta tenants onboarded, 500+ conversations served, average CSAT ≥ 4.0/5, first Stripe subscription activated, and knowledge-base re-index proven stable for 7 consecutive days.
