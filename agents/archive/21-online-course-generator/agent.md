---
description: >
  Generates online courses end-to-end: outline, scripts, slides, video,
  quizzes, and platform publishing (Teachable/Thinkific).
mode: all
phase: 3
depends_on:
  - 12-kindle-self-publishing-agent
  - 20-podcast-production-agent
  - 13-ai-voice-over-narration-agent
inputs:
  course:
    type: object
    required: [title, audience, level]
    properties:
      title: { type: string, maxLength: 120 }
      audience: { type: string }
      level: { type: string, enum: [beginner, intermediate, advanced] }
      price_usd: { type: number, minimum: 9.99 }
      categories: { type: array, items: { type: string } }
      prerequisites: { type: array, items: { type: string } }
  scope:
    type: object
    required: [modules, lessons_per_module]
    properties:
      modules: { type: integer, minimum: 1, maximum: 12 }
      lessons_per_module: { type: integer, minimum: 1, maximum: 20 }
      min_video_min_per_lesson: { type: integer, minimum: 3, maximum: 30, default: 6 }
      max_video_min_per_lesson: { type: integer, minimum: 5, maximum: 45, default: 15 }
  sme_brief:
    type: object
    description: 'Human SME validation artefacts'
    properties:
      outline_approved: { type: boolean }
      outline_feedback: { type: string, nullable: true }
      script_sample_approved: { type: boolean }
      brand_guidelines_url: { type: string, format: 'uri', nullable: true }
      disclaimers: { type: array, items: { type: string } }
  launch:
    type: object
    properties:
      platform: { type: string, enum: [teachable, thinkific, both] }
      coupon_codes: { type: array, items: { type: object } }
      drip_schedule_days: { type: array, items: { type: integer } }
outputs:
  course_outline:
    type: object
    required: [modules]
    properties:
      title: { type: string }
      description: { type: string }
      learning_objectives: { type: array, items: { type: string } }
      modules:
        type: array
        items:
          type: object
          required: [title, lessons]
          properties:
            title: { type: string }
            description: { type: string }
            lessons:
              type: array
              items:
                type: object
                required: [title, objectives]
                properties:
                  title: { type: string }
                  objectives: { type: array, items: { type: string } }
                  estimated_minutes: { type: integer }
                  slide_references: { type: array, items: { type: string } }
  lesson_scripts:
    type: array
    items:
      type: object
      required: [lesson_id, word_count, wpm_checked]
      properties:
        lesson_id: { type: string }
        script_text: { type: string }
        word_count: { type: integer }
        wpm_checked: { type: boolean }
        cue_points: { type: array, items: { type: object } }
        sme_reviewed: { type: boolean }
  slide_decks:
    type: array
    items:
      type: object
      required: [lesson_id, slide_count, file_url]
      properties:
        lesson_id: { type: string }
        slide_count: { type: integer }
        file_url: { type: string, format: 'uri' }
        thumbnail_url: { type: string, format: 'uri', nullable: true }
        brand_compliant: { type: boolean }
  video_lessons:
    type: array
    items:
      type: object
      required: [lesson_id, duration_sec, file_url]
      properties:
        lesson_id: { type: string }
        duration_sec: { type: integer }
        file_url: { type: string, format: 'uri' }
        captions_url: { type: string, format: 'uri' }
        aspect_ratio: { type: string, enum: [16x9, 9x16], default: '16x9' }
        bitrate_kbps: { type: integer }
  quizzes:
    type: array
    items:
      type: object
      required: [lesson_id, questions]
      properties:
        lesson_id: { type: string }
        questions:
          type: array
          items:
            type: object
            required: [type, prompt, options, correct_index, explanation]
            properties:
              type: { type: string, enum: [mcq, case_study, true_false] }
              prompt: { type: string }
              options: { type: array, items: { type: string } }
              correct_index: { type: integer }
              explanation: { type: string }
              application_level: { type: boolean }
  platform_package:
    type: object
    required: [teachable_csv]
    properties:
      teachable_csv: { type: string, description: 'Base64-encoded CSV bundle' }
      thinkific_zip_url: { type: string, format: 'uri', nullable: true }
      drip_schedule: { type: array }
      coupon_codes: { type: array }
tools:
  - anthropic claude sonnet 4 (outline, scripts, quizzes, learning objectives)
  - sdxl + real-ESRGAN (slide art, upscaled 1920x1080)
  - python-pptx (slide deck generation, master template)
  - elevenlabs (voiceover, SSML-tuned pacing)
  - ffmpeg 6 + movit (slide-to-video, captions, motion scenes)
  - whisper large-v3 (auto-caption generation + timing sync)
  - teachable / thinkific REST API (bulk upload, drip, coupon creation)
  - stripe CLI + API (direct checkout fallback, webhook validation)
  - supabase postgrest (course catalog, sales ledger, completion tracking)
  - sentry (error tracking)
error_handling:
  - failure: Platform rejects upload (format, size, codec)
    mitigation: Validate against Teachable/Thinkific spec pre-export; re-encode to H.264 1080p; surface platform error code
  - failure: AI voiceover sounds robotic or pacing off
    mitigation: SSML pauses, sentence rewrite for natural cadence, pronunciation hints; ElevenLabs voice clone fallback
  - failure: Quizzes too easy (low signal, high completion but low retention)
    mitigation: 30% distractors, 1 application-level case-study question per module; A/B test difficulty per cohort
  - failure: Low completion rate post-launch
    mitigation: Add 1 progress email per module via 16-email-marketing-agent; surface drop-off analytics to operator; unlock micro-certificate
cost_per_run: RM80 per 10-lesson course
  breakdown:
    claude_outline_scripts_quizzes: RM35
    elevenlabs_voiceover_10_lessons: RM20
    sdxl_slide_art: RM8
    ffmpeg_render_storage: RM7
    supabase_catalog_api: RM5
    platform_api_calls: RM5
sla:
  freshness: 1–2 courses per month production throughput
  uptime: 99% platform SLO (Teachable/Thinkific)
  latency_p95: 1 week per 10-lesson module; 3 weeks end-to-end for full course
  sme_review_sla: script batch delivered to SME within 48h of outline approval
  caption_accuracy: ≥95% word-level accuracy per Whisper large-v3 baseline
---

## Role
- Design curriculum outlines, lesson scripts, slide decks, video lessons, quizzes, and platform packages.
- Validate against SME briefs; flag unapproved content for human review before publish.
- Package for Teachable/Thinkific with drip schedules, coupon codes, and completion tracking.

## Workflow
1. Receive course brief (title, audience, level, modules, SME validation artefacts).
2. Generate outline → SME review → scripts → slides → video → quizzes in sequence.
3. Produce platform package: Teachable CSV bulk upload, Thinkific zip, drip schedule.
4. SME review gate: scripts and quizzes flagged as `sme_reviewed: false` cannot proceed to video generation.
5. Publish to platform; set up Stripe checkout webhooks; track completion in Supabase.

## Constraints
- All medical, legal, or financial claims must be flagged for SME review; never auto-publish unvalidated content.
- Quizzes must include at least one application-level case-study question per module; never ship trivial-only assessments.
- Encrypt all API keys and OAuth tokens; never log credentials.
- Low course completion rates trigger a review ticket; do not auto-modify curriculum without operator sign-off.
