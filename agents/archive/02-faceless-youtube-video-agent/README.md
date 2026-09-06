# 02-faceless-youtube-video-agent

## Metrics

| Metric | Value |
|--------|-------|
| Risk | Medium |
| Capital | RM800–RM1,500/month (TTS, storage, API quotas) |
| Success Probability | 55% (algorithm-dependent, 3–6 months to 1,000 subs) |
| Time to First RM | 90–180 days (YPP + affiliate shelf) |
| Skills Needed | Video editing (ffmpeg), scriptwriting, thumbnail design, YouTube SEO |

## Stack

| Layer | Choice | Why |
|-------|--------|-----|
| Scripting | Anthropic Claude Sonnet 4 | Long-form coherence, TTS formatting |
| TTS | ElevenLabs (primary) / OpenAI TTS (fallback) | Natural voice, cost-efficient fallback |
| B-Roll | Pexels / Pixabay / SDXL | Licensed stock + generative fallback |
| Assembly | ffmpeg | Industry-standard, scriptable, no GUI dependency |
| Captions | Whisper (word-level timestamps) | Free, accurate, word-level SRT |
| Thumbnails | SDXL + human review gate | Rapid A/B variants, brand control |
| Upload | YouTube Data API v3 | Programmatic scheduling, quota management |
| Storage | Cloudflare R2 / S3 | Cheap video archive, CDN-backed |
| Scheduling | Celery + Redis | Batch processing, retry on transient failures |

## Execution Plan

| Week | Steps |
|------|-------|
| 1 | Niche validation via 36-data-moat (watch-time/CTR signals). Set up YouTube channel, brand assets, ElevenLabs voice clone, R2 bucket. |
| 2 | Produce 5 test videos manually; calibrate script style, B-roll tagging, and thumbnail A/B workflow. Human-review gate on first batch. |
| 3 | Automate script → render → upload pipeline via Celery. Set YouTube quota throttle (50/day). Enable auto-captions. |
| 4 | Release 3 videos per week on schedule. Log impressions/CTR/watch-time to Supabase. Tune thumbnail prompts based on early CTR. |
| 5–8 | Hit 50-video milestone; re-evaluate top-performing topics. Introduce Shorts repurposing pipeline (vertical cut + captions). |
| 9–12 | Apply for YPP. Negotiate affiliate shelf links (Amazon, Teachable). Begin community post / poll cadence to boost engagement. |

## Unit Economics

| Cost Item | RM/month | Revenue Item | RM/month |
|-----------|----------|--------------|----------|
| ElevenLabs + OpenAI TTS | 150–300 | YPP ad revenue (1k subs) | 100–500 |
| R2 / S3 storage + egress | 50–100 | Affiliate shelf commissions | 200–1,000 |
| SDXL inference (GPU or API) | 100–250 | Brand sponsorships (10k+ subs) | 0–2,000 |
| SEO tools (Ahrefs/SEMrush) | 200–400 | Memberships / channel memberships | 100–500 |
| VPS (Celery, ffmpeg workers) | 80–150 | | |
| **Total** | **580–1,200** | **Total** | **400–4,000** |

## Known Failure Modes

| Failure | Mitigation |
|---------|-----------|
| ElevenLabs quota exceeded | Fallback to OpenAI TTS; degrade voice profile to closest match |
| Stock footage API returns no results | Switch to Pexels → Pixabay → SDXL-generated B-roll |
| YouTube upload 403 (quota) | Throttle uploads to 50/day; queue overflow until next day |
| Whisper transcript misalignment | Re-run with word-level timestamps; burn-in subtitles via ffmpeg |

## First Milestone

**Day 30:** 12 videos uploaded, 5,000 total views, average CTR > 4%, and at least one video ranking in YouTube search top 10 for its target keyword.
