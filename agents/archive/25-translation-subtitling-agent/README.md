# 25. Translation/subtitling agent

## Metrics

| Risk | Capital | Success Probability | Time to First RM | Skills Needed |
| --- | --- | --- | --- | --- |
| Low | RM200–RM800 | Medium | 1–3 months | Multilingual QA, API integration (translation tools), subtitle timing, glossary management |

## Stack

| Layer | Choice | Why |
| --- | --- | --- |
| Translation engine | DeepL API v3 | Best quality for 100+ language pairs; glossary support |
| Post-edit / fluency | OpenAI GPT-4o / Anthropic Claude | Fix awkward phrasing, enforce style guide, terminology consistency |
| Video transcription | OpenAI Whisper large-v3 | Accurate multilingual ASR, diarisation support |
| Subtitle processing | python-srt + pysubs2 | SRT/VTT parsing, timing adjustment, CPL enforcement |
| Database | Supabase | Glossary storage, project ledger, human review queue |
| Billing | Stripe / PayPal | Per-word invoicing, tiered pricing, subscription for high-volume clients |
| Queue | Redis + BullMQ | Translation job queue, rate limiting, retry logic |
| Monitoring | Sentry | Error tracking, performance monitoring, alerting |

## Execution Plan

| Week | Step | Deliverable |
| --- | --- | --- |
| 1 | Set up DeepL API + OpenAI fallback; build basic text translation endpoint | /v1/translate working |
| 2 | Implement SRT/VTT parsing; subtitle CPL enforcement; reading-speed checks | Subtitle pipeline |
| 3 | Build glossary enforcement; QA report generation; billing summary | QA reports |
| 4 | Add human review queue via Supabase; Stripe webhook billing | Human review live |
| 5 | Integrate Whisper for video transcription; test with 10 sample videos | Video → SRT → translate |
| 6–8 | Soft launch to 5 beta clients; gather feedback on quality and speed | 5 paying clients |
| 9–12 | Add style guide support; urgent tier SLA; client portal | Production-ready |

## Unit Economics

| Item | Cost (RM) | Revenue (RM) |
| --- | --- | --- |
| DeepL API (per 1M chars) | 25 | – |
| OpenAI post-edit (per 1M tokens) | 14 | – |
| Whisper transcription (per hour) | 0.30 | – |
| Hosting (VPS + Redis + Supabase) | 150/mo | – |
| Human reviewer (per 1k words) | 30–60 | – |
| Machine-only rate | – | 0.02/word |
| MT+QA rate | – | 0.04/word |
| MT+human review rate | – | 0.15/word |
| Subtitle rate (per min) | – | 0.10–0.30/min |
| Break-even | ~10 small projects/mo | – |
| Month 6 target | – | RM2,000–4,000/mo |

## Known Failure Modes

| Failure | Mitigation |
| --- | --- |
| DeepL rate limit or downtime | Round-robin to OpenAI/Anthropic; Redis queue with backpressure; SLA credits |
| Glossary term violation | Re-translate with glossary-prompted LLM; flag high-severity; auto-escalate to human review |
| Subtitle CPL / reading-speed breach | Auto-split at clause boundary; human review if >2 splits per subtitle |
| Sensitive content misclassified | Multi-layer classifier; auto-escalate medical/legal/financial to human review tier |
| PII leak in QA logs | Redact emails, phones, IDs; auto-delete source text in 30 days; audit log encryption |

## First Milestone

**Day 30:** 3 paying clients, 50k words translated, 0 safety incidents, 95% glossary compliance rate, average delivery <24h for standard tier.
