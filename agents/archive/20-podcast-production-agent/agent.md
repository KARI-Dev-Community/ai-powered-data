---
description: >
  Podcast production agent: planning, scheduling guests, AI-edited audio,
  show notes, transcripts, and episode publishing.
mode: all
phase: 2
depends_on:
  - 36-data-moat-history-agent
  - 13-ai-voice-over-narration-agent
inputs:
  show:
    type: object
    required: [name, niche, cadence]
    properties:
      name: { type: string, maxLength: 80 }
      niche: { type: string }
      cadence: { type: string, enum: [weekly, biweekly, monthly] }
      rss_feed_url: { type: string, format: 'uri', nullable: true }
      language: { type: string, pattern: '^[a-z]{2}(-[A-Z]{2})?$', default: 'en-US' }
      explicit_flag: { type: boolean, default: false }
  episode:
    type: object
    required: [topic, raw_audio_url]
    properties:
      topic: { type: string, maxLength: 200 }
      guest: { type: object, nullable: true }
      guest_brief: { type: string, description: 'operator-supplied bio + 5 talking points + disclaimers' }
      raw_audio_url: { type: string, format: 'uri' }
      raw_audio_format: { type: string, enum: [wav, mp3, m4a, aiff], default: 'wav' }
      length_min: { type: integer, minimum: 5, maximum: 180, default: 30 }
      record_date: { type: string, format: date-time }
      target_peak_dbtp: { type: number, default: -1.0 }
  production_profile:
    type: object
    required: [music_library]
    properties:
      music_library: { type: string, enum: [epidemic, artlist, in_house] }
      intro_outro_sec: { type: integer, minimum: 5, maximum: 60, default: 30 }
      target_peak_dbtp: { type: number, default: -1.0 }
      highlight_reel_durations: { type: array, items: { type: integer }, default: [30, 60] }
outputs:
  audio_master:
    type: string
    description: 'Signed URL to normalised, mastered MP3/AAC (target LUFS -16)'
  episode_artwork:
    type: string
    description: 'SDXL-generated 3000x3000 cover image URL'
  show_notes_markdown:
    type: string
    description: 'Markdown with title, summary ≤300 words, 5 key takeaways, links, disclaimer'
  transcript:
    type: object
    properties:
      text: { type: string }
      segments:
        type: array
        items:
          type: object
          properties:
            start: { type: number }
            end: { type: number }
            text: { type: string }
            speaker: { type: string, nullable: true }
  chapters:
    type: array
    items:
      type: object
      required: [timestamp_sec, title]
      properties:
        timestamp_sec: { type: integer }
        title: { type: string }
        summary: { type: string }
  highlight_reels:
    type: array
    items:
      type: object
      properties:
        duration_sec: { type: integer }
        url: { type: string }
        caption: { type: string }
        aspect_ratio: { type: string, enum: [16x9, 9x16, 1x1], default: '9x16' }
  publish_package:
    type: object
    required: [rss_payload, spotify_apple_urls, episode_id]
    properties:
      rss_payload: { type: string }
      spotify_apple_urls: { type: array, items: { type: string } }
      youtube_url: { type: string, nullable: true }
      youtube_chapters: { type: array, nullable: true }
      episode_id: { type: string }
      publish_status: { type: string, enum: [draft, published, failed] }
  analytics:
    type: object
    description: 'Downloads, completion %, CTR, geo, device in first 72h'
tools:
  - descript / riverside.fm (multitrack audio editing, filler removal)
  - openai whisper large-v3 (transcript + word-level timestamps + speaker diarisation)
  - anthropic claude sonnet 4 (show notes, titles, social copy, chapter summaries)
  - sdxl + upscaler (episode artwork + chapter thumbnails, 3000x3000)
  - spotify for podcasters API + apple podcasts connect API (publishing, analytics)
  - youtube data api v3 (upload + auto-chapters)
  - podbase API (RSS validation pre-publish)
  - supabase postgrest (episode catalog, analytics, booking calendar)
  - cal.com REST API (guest scheduling, timezone-aware invites)
  - ffmpeg 6+ (noise reduction, loudnorm, format normalisation, highlight reel cutting)
  - sentry (error tracking)
error_handling:
  - failure: Guest cancels within 24h of recording
    mitigation: Switch to solo episode from cached outline; re-cut show notes; tag as bonus; notify operator and subscribers
  - failure: Audio quality below threshold (SNR, peak, LUFS mismatch)
    mitigation: Re-encode with ffmpeg noise reduction + EQ; if persistent across 2 attempts, trigger re-record SOP; notify operator
  - failure: Apple/Spotify/RSS ingest validation failure
    mitigation: Validate RSS via Podbase pre-publish; surface and fix validation errors; block publish until green; alert operator
  - failure: Show notes hallucinate guest bio, quotes, or stats
    mitigation: Pull guest bio + quotes only from operator-supplied brief; never from LLM memory; validate against source document
cost_per_run: RM1.50 per episode (60 min)
  breakdown:
    whisper_large_v3: RM0.30
    claude_sonnet_show_notes: RM0.40
    sdxl_artwork: RM0.25
    ffmpeg_render_celery: RM0.20
    supabase_storage_api: RM0.15
    api_calls_spotify_apple_youtube: RM0.20
sla:
  freshness: episode published within 48h of recording delivery
  uptime: 99% editing + publishing pipeline
  latency_p95: 6h end-to-end for a 60-min episode
  audio_qa: peak ≤ -1 dBTP, true-peak ≤ -2 dBTP, LUFS -16 ±1
  retention: master audio + raw files retained 90 days; transcript + metadata indefinitely
---

## Role
- Plan episodes, schedule guests via Cal.com, and manage show calendars.
- Produce AI-edited audio: raw recording → transcription (Whisper) → noise reduction (ffmpeg) → mastering (LUFS -16) → highlight reels.
- Write show notes, chapters, transcripts with speaker diarisation, and social clips.
- Publish to Spotify, Apple Podcasts, YouTube via official APIs; validate RSS pre-publish.

## Workflow
1. Receive raw audio + episode brief (topic, guest bio, talking points).
2. Transcribe with Whisper large-v3; edit with Descript/Riverside; master with ffmpeg.
3. Generate show notes, chapters, and social clips with Claude Sonnet; validate all facts against operator-supplied brief.
4. Produce episode artwork with SDXL; validate RSS via Podbase.
5. Publish package: Spotify/Apple upload + YouTube chapters + RSS update; log analytics.

## Constraints
- Never hallucinate guest bios, quotes, or stats; source all show-note claims from the operator-supplied brief only.
- Honour explicit flag; apply platform-mandated AI-disclosure labels where required.
- Block publish if RSS validation fails; never silently drop a failed episode.
- Preserve speaker intent during editing; do not remove substantive content without operator approval.
