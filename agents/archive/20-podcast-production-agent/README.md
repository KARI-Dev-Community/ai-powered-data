# 20. Podcast production agent

## Metrics

| Metric | Value |
| --- | --- |
| Risk | Low |
| Capital Required | RM400–RM1,200 |
| Success Probability | Medium (50–70% with consistent 2x/week cadence by month 3) |
| Time to First RM | 1–3 months |
| Skills Needed | Audio editing, transcription tool usage, show-notes writing, RSS/publishing config, basic DAW concepts |

## Stack

| Layer | Choice | Why |
| --- | --- | --- |
| Audio editing | Descript or Riverside | Multitrack, filler/silence removal, overdub |
| Transcript | OpenAI Whisper large-v3 | Word-level timestamps, speaker diarisation, 40+ languages |
| Copy | Anthropic Claude Sonnet 4 | Show notes, social clips, SEO titles, chapter summaries |
| Artwork | SDXL + real-ESRGAN | Episode art variants at 3000x3000, style-consistent |
| Publishing | Spotify for Podcasters + Apple Podcasts Connect + YouTube Data API v3 | Official, no third-party intermediaries |
| Analytics | Supabase + Spotify/Apple APIs | Downloads, completion, geo, device, first-72h CTR |
| Scheduling | Cal.com REST API | Guest scheduling, timezone-aware invites, reminders |
| Music | Epidemic Sound / Artlist | Licensed library; no copyright strikes |
| Audio QA | ffmpeg 6+ loudnorm | LUFS normalisation, true-peak limiting, noise reduction |

## Execution Plan

| Week | Step |
| --- | --- |
| 1 | Pick niche, register RSS feed, set up Spotify/Apple/YouTube channels; configure Cal.com guest booking |
| 2 | Record 3 pilot episodes manually to lock the format; baseline audio QA metrics |
| 3 | Build agent pipeline: ingest → transcribe → edit → notes → artwork → publish |
| 4 | Wire guest scheduling + reminder automation via Cal.com; auto-send briefing doc |
| 5 | First 10 episodes shipped; iterate on intro/outro length and show-notes template |
| 6–10 | Scale to 2 episodes/week; cross-publish to YouTube with auto-chapters; harvest analytics |
| 11–12 | Add 36-data-moat-history-agent for topic selection + trend velocity; A/B test publish times |

## Unit Economics

| Item | Cost (RM) | Revenue (RM) |
| --- | --- |
| Whisper large-v3 per episode | 0.30/ep | – |
| Claude Sonnet show notes + copy | 0.40/ep | – |
| SDXL artwork | 0.25/ep | – |
| ffmpeg + Celery render | 0.20/ep | – |
| Supabase + API calls | 0.15/ep | – |
| Spotify/Apple/YouTube API | 0.20/ep | – |
| **Variable cost per episode** | **1.50/ep** | – |
| Descript / Riverside | 50–200/mo | – |
| Music license | 30–60/mo | – |
| Sponsor per 1k downloads | – | 30–80 |
| Listener support / Patreon | – | 5–20/patron/mo |
| Break-even | ~50 sponsorships/year or 100 patrons | – |

## Known Failure Modes

| Failure | Mitigation |
| --- | --- |
| Guest cancels < 24h before recording | Solo bonus episode from cached outline; re-cut show notes; notify operator and subscribers; preserve cadence |
| Audio quality below threshold (SNR, peak, LUFS) | Re-encode with ffmpeg noise reduction + EQ; if persistent across 2 attempts, trigger re-record SOP; alert operator |
| Apple/Spotify/RSS ingest validation failure | Validate RSS via Podbase pre-publish; surface and fix validation errors; block publish until green; alert operator |
| Show notes hallucinate guest bio or quotes | Pull guest bio + quotes only from operator-supplied brief; never from LLM memory; validate against source document |

## First Milestone

**Day 60:** 8 episodes live across 3 platforms, 1,000 cumulative downloads, first sponsor inquiry received, MRR RM0 → RM200 from early patronage.
