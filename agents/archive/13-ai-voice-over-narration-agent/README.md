# AI Voice-Over Narration Agent

## Metrics

| Metric | Value |
|--------|-------|
| Risk | Low |
| Capital | RM 0–RM 200 (ElevenLabs subscription) |
| Success Probability | 80%+ (spec-driven, deterministic pipeline) |
| Time to First RM | Same day (client delivery) |
| Skills Needed | Audio editing, ACX specs, basic ElevenLabs API use |

## Stack

| Layer | Choice | Why |
|-------|--------|-----|
| Primary TTS | ElevenLabs | Best emotion + pace control; voice cloning with consent |
| Fallback TTS | OpenAI TTS | Cheaper fallback; maps well to ElevenLabs voice profiles |
| Audio Processing | Sox + FFmpeg | Industry-standard loudness normalisation; -19 LUFS target |
| Alignment / Diarization | OpenAI Whisper | Post-render speaker timing validation |
| Billing | Stripe (per-character) | Granular metering; auto-charge on job completion |
| Data Ledger | Supabase | Track jobs, voice profiles, royalty splits |
| Storage | S3-compatible (via Supabase or dedicated) | Long-lived audio asset storage with signed URLs |

## Execution Plan

| Week | Task |
|------|------|
| 1 | Build script-parser: split plain text into speaker segments. Define voice-profile schema. |
| 2 | Integrate ElevenLabs TTS API + OpenAI TTS fallback. Test 10 script samples. |
| 3 | Build sox loudness-normalisation pipeline (-19 LUFS ACX spec). Validate with 5 test files. |
| 4 | Integrate Whisper alignment; flag diarization drift >0.5s. |
| 5 | Add chapter-split logic for audiobooks >650MB. Emit per-chapter manifest. |
| 6 | Wire Stripe per-character billing. Test subscription vs. one-off payment flows. |
| 7 | Add voice-clone consent gate (Supabase form upload). Block jobs without consent. |
| 8–10 | Batch-test 50 scripts. Measure p95 latency. Target <90s per 1k chars. |
| 11–12 | Document operator runbook. Package as reusable agent for 12-kindle + 25-translation pipelines. |

## Unit Economics

| Item | Cost | Revenue |
|------|------|---------|
| ElevenLabs (Creator plan) | RM 80–RM 300/mo | — |
| OpenAI TTS fallback | RM 0.015 / 1k chars | — |
| Storage (S3/Supabase) | RM 0.05/GB/mo | — |
| Per-job billing (1k chars) | — | RM 0.40–RM 1.20 |
| Audiobook project (50k chars) | — | RM 20–RM 60 |

**Break-even:** ~5 audiobook chapters/month covers ElevenLans subscription.

## Known Failure Modes

| Failure | Mitigation |
|---------|-----------|
| ElevenLabs quota exceeded | Auto-fallback to OpenAI TTS with mapped voice profile; alert operator |
| Loudness outside ACX spec (-23 to -18 LUFS) | Re-normalise with sox; reject if RMS still out of spec after 2 attempts |
| Voice clone consent missing | Block job until consent form uploaded to Supabase; never render |
| Audio > 650MB (Audible chapter limit) | Auto-split by chapter; emit per-chapter manifest with metadata |
| Whisper alignment drift >1s | Flag segment; offer manual re-render or silent-replace option |
| TTS provider latency spike | Cache common phrases; pre-warm voice profiles at job start |

## First Milestone

**Day 14:** First end-to-end audiobook chapter rendered, normalised to ACX spec, and delivered to client. Target: by Day 30, deliver 5 audiobook chapters with 0 loudness rejects.
