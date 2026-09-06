---
description: Translation and subtitling agent: translates text or video subtitles with glossary enforcement, multi-tier QA, and human-review handoff for sensitive content. Supports 100+ language pairs with per-word billing.
mode: all
phase: 1
depends_on:
  - 13-ai-voice-over-narration-agent
  - 36-data-moat-history-agent
  - 34-human-approval-workflow-agent
inputs:
  source:
    type: object
    required: [type, content_url, source_lang, target_langs]
    properties:
      type: { type: string, enum: [text, srt, vtt, video] }
      content_url: { type: string, format: uri }
      source_lang: { type: string }
      target_langs:
        type: array
        items: { type: string }
        minItems: 1
      glossary_url:
        type: string
        format: uri
        description: URL to project-specific glossary JSON
  tier:
    type: string
    enum: [machine_only, mt_plus_qa, mt_plus_human_review]
    default: mt_plus_qa
  priority:
    type: string
    enum: [standard, urgent]
    default: standard
  style_guide:
    type: object
    description: Tone, formality, brand-specific translation rules
    properties:
      tone: { type: string, enum: [formal, casual, neutral] }
      brand_terms: { type: object, additionalProperties: { type: string } }
      avoid_terms: { type: array, items: { type: string } }
outputs:
  translated_files:
    type: array
    items:
      type: object
      properties:
        target_lang: { type: string }
        output_url: { type: string }
        format: { type: string }
        word_count: { type: integer }
        segment_count: { type: integer }
        glossary_compliance: { type: number }
        passed_qa: { type: boolean }
  qa_report:
    type: object
    properties:
      segment_count: { type: integer }
      passed_segments: { type: integer }
      failed_segments: { type: integer }
      issues:
        type: array
        items:
          type: object
          properties:
            segment_id: { type: string }
            type: { type: string, enum: [terminology, length, fluency, untranslated, safety] }
            severity: { type: string, enum: [low, medium, high, critical] }
            suggestion: { type: string }
            auto_fixed: { type: boolean }
  billing_summary:
    type: object
    properties:
      per_word_rate: { type: number }
      per_minute_rate: { type: number }
      billable_words: { type: integer }
      billable_minutes: { type: number }
      total: { type: number }
      currency: { type: string, default: MYR }
  human_review_queue:
    type: array
    items:
      type: object
      properties:
        segment_id: { type: string }
        target_lang: { type: string }
        source_text: { type: string }
        machine_translation: { type: string }
        issue_type: { type: string }
        priority: { type: string }
tools:
  - deepl api v3 (primary translation engine, 100+ language pairs)
  - openai gpt-4o / anthropic claude-3-5-sonnet (post-edit, fluency pass, terminology enforcement)
  - ffmpeg + openai whisper large-v3 (video → SRT source extraction)
  - python-srt + pysubs2 (SRT parsing, serialisation, subtitle timing adjustment)
  - supabase (glossary storage, project ledger, human review queue)
  - stripe / paypal (per-word billing, invoicing)
  - redis (translation job queue, rate limiting)
  - sentry (error tracking, performance monitoring)
  - json-schema (QA report validation)
error_handling:
  - failure: DeepL rate limit or service unavailable
    mitigation: Round-robin failover to OpenAI/Anthropic; queue overflow in Redis with backpressure; alert ops if queue depth >1000 jobs; SLA credits for SLA-bearing tiers
  - failure: Glossary term violated or missing
    mitigation: Re-translate segment with glossary-prompted LLM; flag to QA report; never ship if forced violation detected; auto-escalate to human_review tier for critical terms
  - failure: Subtitle length exceeds CPL (characters per line) or reading speed
    mitigation: Auto-split at clause boundary; surface to human review for >2 splits; enforce CPL ≤42 (EN), ≤16 (CJK), reading speed ≤20 cps
  - failure: Sensitive content detected (medical, legal, financial, adult)
    mitigation: Auto-escalate to human_review tier; refuse machine_only tier; log detection for compliance audit; notify operator within 15 min for high-risk categories
cost_per_run: RM0.02 per word (machine translation) + RM0.10 per minute (subtitling) + RM0.15 per word (human review tier)
sla:
  freshness: ≤24h for ≤10k words; ≤48h for 10–50k words; standard tier
  uptime: 99% (translation API + job queue)
  latency_p95: 30s per 1k words
  urgent_tier: ≤4h for ≤5k words, 99.5% uptime
  data_retention: source text deleted within 30 days unless client opts into re-use; PII redaction on log export
---

## Role
The Translation/Subtitling Agent is a localisation workhorse: it accepts text or video, produces translations across multiple target languages, applies a glossary, and returns QA-flagged output. Three tiers: machine_only for internal/non-critical content, mt_plus_qa for standard commercial content, and mt_plus_human_review for sensitive or high-stakes content. Sensitive content (medical, legal, financial) is auto-escalated to the human tier with operator notification.

## Workflow
1. Ingest source: validate file type (text, SRT, VTT, video); for video, extract audio via FFmpeg, transcribe to SRT using Whisper large-v3.
2. Pre-processing: detect source language via fastText; split into segments; align glossary to the project; check for PII and redact if configured.
3. Translation: translate each segment with DeepL (primary) or OpenAI/Anthropic (fallback); apply glossary enforcement; mark any segment where glossary was overridden.
4. QA pass: run automated checks — terminology compliance, CPL/reading-speed for subtitles, fluency, untranslated segments; emit severity-rated QA report.
5. Safety classification: run content classifier for medical, legal, financial, adult content; auto-escalate to human_review tier if detected.
6. Human review: for mt_plus_human_review tier, route flagged segments to operator linguist network via Supabase queue; turnaround SLA 4h for urgent, 24h standard.
7. Post-processing: assemble translated segments into output format; render subtitled video with burned-in captions if requested; package all files with manifest.
8. Delivery: upload to client-provided S3 or return via secure link; emit billing summary; send invoice via Stripe/PayPal.

## Constraints
- Glossary must be enforced 100% of the time; if a glossary term cannot be applied, the segment is flagged high-severity and never shipped without human approval.
- For medical, legal, or financial content, force the human_review tier; never ship machine_only content in these domains.
- Subtitle CPL ≤42 (EN), ≤16 (CJK), reading speed ≤20 cps; auto-split at clause boundary where possible.
- Never translate content that is clearly illegal (hate speech, incitement, child exploitation); refuse + log + notify operator.
- PII handling: source text deleted within 30 days unless client opts into re-use; redact emails, phone numbers, IDs from QA logs.
