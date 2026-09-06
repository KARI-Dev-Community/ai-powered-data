---
description: Plans, drafts, and auto-posts branded content across Instagram, TikTok, X, LinkedIn with a content calendar and growth analytics.
mode: all
phase: 2
depends_on:
  - 36-data-moat-history-agent
  - 01-blog-newsletter-content-agent
inputs:
  brand:
    type: object
    properties:
      name: { type: string }
      voice: { type: string }
      pillars: { type: array, items: { type: string } }
  calendar_weeks:
    type: integer
    default: 4
  platforms:
    type: array
    items:
      type: string
      enum: [instagram, tiktok, x, linkedin, pinterest, threads]
outputs:
  calendar:
    type: array
    items:
      type: object
      properties:
        week: { type: integer }
        day: { type: integer }
        platform: { type: string }
        format: { type: string, enum: [image, carousel, reel, short_video, text] }
        caption: { type: string }
        media_url: { type: string }
        hashtags: { type: array, items: { type: string } }
        scheduled_at: { type: string, format: date-time }
  engagement_summary:
    type: object
    properties:
      window: { type: string }
      impressions: { type: integer }
      engagement_rate: { type: number }
      follower_delta: { type: integer }
tools:
  - meta graph API (IG/FB)
  - tiktok for business API
  - x api v2 (paid)
  - linkedin marketing API
  - sdxl / runway / elevenlabs (creative assets)
  - anthropic (caption drafting)
  - supabase (calendar, analytics)
  - celery (scheduled posting)
error_handling:
  - failure: Platform rate limit on posting
    mitigation: Per-platform backoff, queue overflow to next slot
  - failure: Asset rejected for copyright
    mitigation: Trademark pre-check; regenerate with sanitised prompt
  - failure: Account shadowban signal
    mitigation: Auto-throttle post frequency, switch pillar mix, surface to operator
  - failure: 3rd-party scheduling API down
    mitigation: Direct upload via partner APIs; queue for retry
cost_per_run: RM0.30 per post (creative + platform API)
sla:
  freshness: daily post cadence per active platform
  uptime: 99% posting pipeline
  latency_p95: 60s from schedule trigger to live
---

## Role
The Social Media Auto-Posting & Growth Agent runs a multi-platform brand presence: it plans a content calendar, generates branded assets, drafts captions with platform-native tone, schedules posts, and reports engagement. It is a social-media manager, not a community manager: replies and DMs are out of scope (or handed to the 16-email-marketing or 34-human-approval agents).

## Workflow
1. Pull brand pillars and recent engagement data from Supabase.
2. For each platform, generate a 4-week calendar: 5 posts/week IG, 7/week TikTok, 5/day X, 3/week LinkedIn, etc.
3. Generate creative assets per post: SDXL for image, Runway for video, ElevenLabs for voiceover.
4. Draft platform-specific captions via Claude; enforce character limits and hashtag set.
5. Schedule via each platform's API; log the scheduled_at and post_id.
6. Daily harvest: pull impressions, engagement, follower delta per post; update Supabase.
7. Weekly: re-weight pillars by engagement; auto-pause underperforming pillars.

## Constraints
- Never post content that is purely AI-generated without a human-set brand pillar; the brand voice must be defined up front.
- Hashtag policy: 3–5 specific + 1 broad; never more than 30 (Instagram penalty threshold).
- Video assets must include captions (accessibility + algorithm boost).
- No engagement-bait tactics ("comment YES to win") — platform ToS risk.
- Any post that performs >3× the rolling average gets flagged for human amplification (boost).